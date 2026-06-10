#!/usr/bin/env python3
"""Ruta B — Monte Carlo Mundial 2026. 10.000 torneos completos (grupos incluidos).
Ratings = promedio de 3 lentes decorreladas. Grupos: probs de los 72 analisis (Ruta A)
texturizadas con ratings para goles. Eliminatoria: modelo Poisson via ratings.
Salida: P(campeon), % por ronda, Bota de Oro + conteo, MVP proxy."""
import json, numpy as np
from collections import defaultdict
rng = np.random.default_rng(20260603)
B = "/Users/erickhein/TechWorkspace/active_projects/misc/polla_mundial_2026/ruta_b/"

# ---- 1. ratings: promedio 3 lentes ----
R = [json.load(open(B+f)) for f in ("ratings_odds.json","ratings_rank.json","ratings_scout.json")]
TEAMS = list(R[0].keys())
rat = {t: {k: float(np.mean([R[i][t][k] for i in range(3)])) for k in ("rating","att","def")} for t in TEAMS}

GROUPS = {
 "A":["mexico","south_africa","south_korea","czechia"],
 "B":["canada","bosnia_and_herzegovina","qatar","switzerland"],
 "C":["brazil","morocco","haiti","scotland"],
 "D":["united_states","paraguay","australia","turkiye"],
 "E":["germany","curacao","ivory_coast","ecuador"],
 "F":["netherlands","japan","sweden","tunisia"],
 "G":["belgium","egypt","iran","new_zealand"],
 "H":["spain","cape_verde","saudi_arabia","uruguay"],
 "I":["france","senegal","iraq","norway"],
 "J":["argentina","algeria","austria","jordan"],
 "K":["portugal","dr_congo","uzbekistan","colombia"],
 "L":["england","croatia","ghana","panama"]}

# ---- 2. group_probs de los 72 analisis (pick + confianza -> 1X2) ----
# (grupo, home, away, pick, conf)
G72 = [
("A","mexico","south_africa","1",4),("A","south_korea","czechia","X",3),
("B","canada","bosnia_and_herzegovina","1",3),("B","qatar","switzerland","2",4),
("C","brazil","morocco","1",3),("C","haiti","scotland","2",3),
("D","united_states","paraguay","1",3),("D","australia","turkiye","2",3),
("E","germany","curacao","1",5),("E","ivory_coast","ecuador","X",2),
("F","netherlands","japan","1",3),("F","sweden","tunisia","1",3),
("G","belgium","egypt","1",3),("G","iran","new_zealand","1",3),
("H","spain","cape_verde","1",4),("H","saudi_arabia","uruguay","2",4),
("I","france","senegal","1",3),("I","iraq","norway","2",4),
("J","argentina","algeria","1",4),("J","austria","jordan","1",4),
("K","portugal","dr_congo","1",4),("K","uzbekistan","colombia","2",4),
("L","england","croatia","1",3),("L","ghana","panama","X",2),
("A","czechia","south_africa","1",3),("A","mexico","south_korea","1",3),
("B","switzerland","bosnia_and_herzegovina","1",4),("B","canada","qatar","1",4),
("C","scotland","morocco","2",3),("C","brazil","haiti","1",5),
("D","united_states","australia","1",3),("D","turkiye","paraguay","1",4),
("E","germany","ivory_coast","1",4),("E","ecuador","curacao","1",4),
("F","netherlands","sweden","1",4),("F","tunisia","japan","2",3),
("G","belgium","iran","1",4),("G","new_zealand","egypt","2",3),
("H","spain","saudi_arabia","1",5),("H","uruguay","cape_verde","1",4),
("I","france","iraq","1",4),("I","norway","senegal","1",3),
("J","argentina","austria","1",3),("J","jordan","algeria","2",4),
("K","portugal","uzbekistan","1",4),("K","colombia","dr_congo","1",4),
("L","england","ghana","1",4),("L","panama","croatia","2",3),
("A","czechia","mexico","2",3),("A","south_africa","south_korea","2",3),
("B","switzerland","canada","X",3),("B","bosnia_and_herzegovina","qatar","1",3),
("C","scotland","brazil","X",3),("C","morocco","haiti","1",4),
("D","turkiye","united_states","2",3),("D","paraguay","australia","1",2),
("E","ecuador","germany","X",3),("E","curacao","ivory_coast","2",4),
("F","japan","sweden","1",3),("F","tunisia","netherlands","2",3),
("G","egypt","iran","1",3),("G","new_zealand","belgium","2",3),
("H","cape_verde","saudi_arabia","1",2),("H","uruguay","spain","2",3),
("I","norway","france","2",3),("I","senegal","iraq","1",3),
("J","algeria","austria","1",2),("J","jordan","argentina","2",4),
("K","colombia","portugal","X",3),("K","dr_congo","uzbekistan","1",3),
("L","panama","england","2",4),("L","croatia","ghana","1",4)]

def probs(pick, conf):
    home={5:(.72,.18,.10),4:(.62,.22,.16),3:(.50,.27,.23),2:(.42,.30,.28)}
    draw={4:(.30,.44,.26),3:(.32,.40,.28),2:(.33,.36,.31)}
    if pick=="1": return home[conf]
    if pick=="2": p1,pX,p2=home[conf]; return (p2,pX,p1)
    return draw[conf]

GP = {}
for g,h,a,pk,cf in G72:
    p1,pX,p2 = probs(pk,cf); GP[(g,h,a)] = (p1,pX,p2)
json.dump({f"{g}|{h}|{a}":GP[(g,h,a)] for g,h,a,_,_ in G72},
          open(B+"group_probs.json","w"), indent=1)

# ---- 3. scorers ----
SC = json.load(open(B+"scorers.json"))["players"]
team_scorers = defaultdict(list)
for i,p in enumerate(SC):
    w = p["goals_per90"] + (0.15 if p.get("penalty_taker") else 0)
    team_scorers[p["team"]].append((i, w))
NP = len(SC)
OTHER_W = 1.2  # peso de goleadores no listados por equipo

def lam(home, away, neutral=True):
    lh = (rat[home]["att"] + rat[away]["def"])/2 * (1.0 if neutral else 1.05)
    la = (rat[away]["att"] + rat[home]["def"])/2 * (1.0 if neutral else 0.95)
    return min(max(lh,0.2),3.6), min(max(la,0.2),3.6)

def attribute(team, goals, goalbox):
    lst = team_scorers.get(team, [])
    if goals<=0: return
    ids=[i for i,_ in lst]+[-1]; ws=np.array([w for _,w in lst]+[OTHER_W])
    ws=ws/ws.sum()
    for _ in range(goals):
        pick=rng.choice(len(ids),p=ws)
        if ids[pick]>=0: goalbox[ids[pick]]+=1

def group_match(g,h,a,goalbox):
    p1,pX,p2=GP[(g,h,a)]
    cat=rng.choice(3,p=[p1,pX,p2])  # 0 home,1 draw,2 away
    lh,la=lam(h,a)
    for _ in range(25):
        gh,ga=rng.poisson(lh),rng.poisson(la)
        c=0 if gh>ga else (1 if gh==ga else 2)
        if c==cat: break
    else:
        if cat==0: gh,ga=max(gh,ga)+0 if gh>ga else (ga+1,ga)[0],min(gh,ga); gh,ga=(max(gh,ga),min(gh,ga))
        elif cat==2: gh,ga=(min(gh,ga),max(gh,ga))
        else: ga=gh
    attribute(h,gh,goalbox); attribute(a,ga,goalbox)
    return gh,ga

def knockout(h,a,goalbox):
    lh,la=lam(h,a)
    gh,ga=rng.poisson(lh),rng.poisson(la)
    attribute(h,gh,goalbox); attribute(a,ga,goalbox)
    if gh==ga:  # prorroga
        eh,ea=rng.poisson(lh*0.33),rng.poisson(la*0.33)
        attribute(h,eh,goalbox); attribute(a,ea,goalbox); gh+=eh; ga+=ea
    if gh>ga: return h
    if ga>gh: return a
    pp=0.5+(rat[h]["rating"]-rat[a]["rating"])/4000
    return h if rng.random()<min(max(pp,0.35),0.65) else a

def standings(g,res):
    tab={t:{"pts":0,"gf":0,"gc":0} for t in GROUPS[g]}
    for (h,a),(gh,ga) in res.items():
        tab[h]["gf"]+=gh; tab[h]["gc"]+=ga; tab[a]["gf"]+=ga; tab[a]["gc"]+=gh
        if gh>ga: tab[h]["pts"]+=3
        elif gh==ga: tab[h]["pts"]+=1; tab[a]["pts"]+=1
        else: tab[a]["pts"]+=3
    order=sorted(GROUPS[g],key=lambda t:(-tab[t]["pts"],-(tab[t]["gf"]-tab[t]["gc"]),-tab[t]["gf"], rng.random()))
    return order, tab

THIRD_HOSTS=["A","B","D","E","G","I","K","L"]  # winners que reciben un 3º (skeleton FIFA26)

def assign_thirds(third_groups):
    # asigna 8 terceros a 8 hosts evitando mismo grupo (matching valido, greedy)
    hosts=THIRD_HOSTS[:]; tg=sorted(third_groups); res={}
    used=set()
    for host in hosts:
        cand=[t for t in tg if t not in used and t!=host]
        if not cand: cand=[t for t in tg if t not in used]
        pick=cand[0]; res[host]=pick; used.add(pick)
    return res  # host_group -> third_group

# contadores
champ=defaultdict(int); rounds=defaultdict(lambda: defaultdict(int))  # team->round->count
gb_lead=defaultdict(int); gb_goals=[]; mvp=defaultdict(int)
QUAL=defaultdict(int)  # pasa de grupo
N=10000
DEPTH={"R32":1,"R16":2,"QF":3,"SF":4,"F":5,"W":6}

for it in range(N):
    goalbox=np.zeros(NP,dtype=int)
    pos1={};pos2={};thirds=[]
    by_match=defaultdict(dict)
    # grupos
    for g in GROUPS:
        res={}
        for (gg,h,a,_,_) in G72:
            if gg==g: res[(h,a)]=group_match(g,h,a,goalbox)
        order,tab=standings(g,res)
        pos1[g],pos2[g]=order[0],order[1]
        t3=order[2]; s=tab[t3]; thirds.append((g,t3,s["pts"],s["gf"]-s["gc"],s["gf"]))
        QUAL[order[0]]+=1; QUAL[order[1]]+=1
    # mejores 8 terceros por (pts, dg, gf) reales
    ranked=sorted(thirds,key=lambda x:(-x[2],-x[3],-x[4]))[:8]
    qthird={g:t for g,t,_,_,_ in ranked}
    for g,t,_,_,_ in ranked: QUAL[t]+=1; rounds[t]["R32"]+=1
    for g in GROUPS:
        rounds[pos1[g]]["R32"]+=1; rounds[pos2[g]]["R32"]+=1
    amap=assign_thirds(list(qthird.keys()))
    T=lambda hg: qthird[amap[hg]]
    W={}
    def ko(name,h,a):
        w=knockout(h,a,goalbox); W[name]=w; return w
    # R32
    w73=ko("73",pos2["A"],pos2["B"]); w74=ko("74",pos1["E"],T("E"))
    w75=ko("75",pos1["F"],pos2["C"]); w76=ko("76",pos1["C"],pos2["F"])
    w77=ko("77",pos1["I"],T("I"));    w78=ko("78",pos2["E"],pos2["I"])
    w79=ko("79",pos1["A"],T("A"));    w80=ko("80",pos1["L"],T("L"))
    w81=ko("81",pos1["D"],T("D"));    w82=ko("82",pos1["G"],T("G"))
    w83=ko("83",pos2["K"],pos2["L"]); w84=ko("84",pos1["H"],pos2["J"])
    w85=ko("85",pos1["B"],T("B"));    w86=ko("86",pos1["J"],pos2["H"])
    w87=ko("87",pos1["K"],T("K"));    w88=ko("88",pos2["D"],pos2["G"])
    for w in [w73,w74,w75,w76,w77,w78,w79,w80,w81,w82,w83,w84,w85,w86,w87,w88]:
        rounds[w]["R16"]+=1
    # R16
    w89=ko("89",w74,w77); w90=ko("90",w73,w75); w91=ko("91",w76,w78); w92=ko("92",w79,w80)
    w93=ko("93",w83,w84); w94=ko("94",w81,w82); w95=ko("95",w86,w88); w96=ko("96",w85,w87)
    for w in [w89,w90,w91,w92,w93,w94,w95,w96]: rounds[w]["QF"]+=1
    # QF
    w97=ko("97",w89,w90); w98=ko("98",w93,w94); w99=ko("99",w91,w92); w100=ko("100",w95,w96)
    for w in [w97,w98,w99,w100]: rounds[w]["SF"]+=1
    # SF
    w101=ko("101",w97,w98); w102=ko("102",w99,w100)
    rounds[w101]["F"]+=1; rounds[w102]["F"]+=1
    # Final
    wc=ko("104",w101,w102); champ[wc]+=1; rounds[wc]["W"]+=1
    # Bota de oro
    lead=int(np.argmax(goalbox)); gl=int(goalbox[lead])
    if gl>0:
        gb_lead[SC[lead]["name"]]+=1; gb_goals.append(gl)
    # MVP proxy: calidad*profundidad + goles, equipos en SF+
    finalists={w101,w102}; sfs={w97,w98,w99,w100}
    best=None;bs=-1
    for i,p in enumerate(SC):
        tm=p["team"]
        if tm in sfs or tm in finalists:
            bonus=6 if tm==wc else (4 if tm in finalists else 3)
            score=goalbox[i]*1.0 + p["goals_per90"]*3 + bonus
            if score>bs: bs=score; best=p["name"]
    if best: mvp[best]+=1

# ---- salida ----
def top(d,n=12): return sorted(d.items(),key=lambda x:-x[1])[:n]
out={"N":N,
 "champion":[(t,round(100*c/N,1)) for t,c in top(champ)],
 "qualify_group":[(t,round(100*QUAL[t]/N,1)) for t,_ in sorted(QUAL.items(),key=lambda x:-x[1])],
 "reach_final":[(t,round(100*(rounds[t]["F"]+rounds[t]["W"])/N,1)) for t,_ in top({t:rounds[t]["F"]+rounds[t]["W"] for t in TEAMS})],
 "reach_sf":[(t,round(100*(rounds[t]["SF"])/N,1)) for t,_ in top({t:rounds[t]["SF"] for t in TEAMS})],
 "golden_boot":[(n,round(100*c/N,1)) for n,c in top(gb_lead)],
 "gb_goals_median":int(np.median(gb_goals)),"gb_goals_p10":int(np.percentile(gb_goals,10)),"gb_goals_p90":int(np.percentile(gb_goals,90)),
 "mvp":[(n,round(100*c/N,1)) for n,c in top(mvp)]}
json.dump(out,open(B+"mc_results.json","w"),ensure_ascii=False,indent=1)
print("=== CAMPEON (P%) ==="); [print(f"  {t:16} {p}%") for t,p in out["champion"]]
print("=== LLEGA A FINAL ==="); [print(f"  {t:16} {p}%") for t,p in out["reach_final"][:8]]
print("=== BOTA DE ORO (P lider) ==="); [print(f"  {n:22} {p}%") for n,p in out["golden_boot"][:8]]
print(f"=== GOLES DEL LIDER: mediana {out['gb_goals_median']} (p10 {out['gb_goals_p10']} - p90 {out['gb_goals_p90']}) ===")
print("=== MVP proxy ==="); [print(f"  {n:22} {p}%") for n,p in out["mvp"][:6]]
print("=== Irán pasa de grupo? ==="); print("  iran:",dict(out["qualify_group"]).get("iran"),"%")
