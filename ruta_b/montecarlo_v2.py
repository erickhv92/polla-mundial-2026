#!/usr/bin/env python3
"""Ruta B v2 — Monte Carlo Mundial 2026 mejorado.
F2: Dixon-Coles + lambda multiplicativa + localia/altitud + tabla FIFA terceros + penales clamp.
F3: atribucion v2 (minutos/asist/penaltis, 48 equipos) + MVP creator-aware.
F4: blend de mercado (odds devig) + incertidumbre de rating + IC Wilson + P por ronda.
Uso: python3 montecarlo_v2.py [N] [seed]"""
import json, sys, math, numpy as np
from collections import defaultdict
B="/Users/erickhein/TechWorkspace/active_projects/misc/polla_mundial_2026/ruta_b/"
N=int(sys.argv[1]) if len(sys.argv)>1 else 20000
SEED=int(sys.argv[2]) if len(sys.argv)>2 else 20260603
rng=np.random.default_rng(SEED)

# ---------- inputs ----------
R=[json.load(open(B+f)) for f in("ratings_odds.json","ratings_rank.json","ratings_scout.json")]
TEAMS=list(R[0].keys())
avg={t:{k:float(np.mean([R[i][t][k] for i in range(3)])) for k in("rating","att","def")} for t in TEAMS}
sd_rating={t:float(np.std([R[i][t]["rating"] for i in range(3)])) for t in TEAMS}  # desacuerdo entre lentes
ODDS=json.load(open(B+"odds.json"))["p_champion"]
THIRDS=json.load(open(B+"thirds_table.json"))
VEN=json.load(open(B+"venues.json")); HOSTS=set(VEN["host_teams"])
DBAR=float(np.mean([avg[t]["def"] for t in TEAMS]))      # defensa media
ABAR=float(np.mean([avg[t]["att"] for t in TEAMS]))

# rating anclado a mercado (odds devig) blend 30%
pmed=float(np.median(list(ODDS.values())))
def odds_rating(t):
    p=max(ODDS.get(t,pmed*0.2),1e-4)
    return 1500+350*(math.log10(p)-math.log10(pmed))
rat={t:{"att":avg[t]["att"],"def":avg[t]["def"],
        "rating":float(np.clip(0.7*avg[t]["rating"]+0.3*odds_rating(t),1300,2160)),
        "sd":sd_rating[t]} for t in TEAMS}

GROUPS={"A":["mexico","south_africa","south_korea","czechia"],"B":["canada","bosnia_and_herzegovina","qatar","switzerland"],
"C":["brazil","morocco","haiti","scotland"],"D":["united_states","paraguay","australia","turkiye"],
"E":["germany","curacao","ivory_coast","ecuador"],"F":["netherlands","japan","sweden","tunisia"],
"G":["belgium","egypt","iran","new_zealand"],"H":["spain","cape_verde","saudi_arabia","uruguay"],
"I":["france","senegal","iraq","norway"],"J":["argentina","algeria","austria","jordan"],
"K":["portugal","dr_congo","uzbekistan","colombia"],"L":["england","croatia","ghana","panama"]}

# group_probs (analisis Ruta A) como prior 1X2
G72=[("A","mexico","south_africa","1",4),("A","south_korea","czechia","X",3),("B","canada","bosnia_and_herzegovina","1",3),("B","qatar","switzerland","2",4),("C","brazil","morocco","1",3),("C","haiti","scotland","2",3),("D","united_states","paraguay","1",3),("D","australia","turkiye","2",3),("E","germany","curacao","1",5),("E","ivory_coast","ecuador","X",2),("F","netherlands","japan","1",3),("F","sweden","tunisia","1",3),("G","belgium","egypt","1",3),("G","iran","new_zealand","1",3),("H","spain","cape_verde","1",4),("H","saudi_arabia","uruguay","2",4),("I","france","senegal","1",3),("I","iraq","norway","2",4),("J","argentina","algeria","1",4),("J","austria","jordan","1",4),("K","portugal","dr_congo","1",4),("K","uzbekistan","colombia","2",4),("L","england","croatia","1",3),("L","ghana","panama","X",2),
("A","czechia","south_africa","1",3),("A","mexico","south_korea","1",3),("B","switzerland","bosnia_and_herzegovina","1",4),("B","canada","qatar","1",4),("C","scotland","morocco","2",3),("C","brazil","haiti","1",5),("D","united_states","australia","1",3),("D","turkiye","paraguay","1",4),("E","germany","ivory_coast","1",4),("E","ecuador","curacao","1",4),("F","netherlands","sweden","1",4),("F","tunisia","japan","2",3),("G","belgium","iran","1",4),("G","new_zealand","egypt","2",3),("H","spain","saudi_arabia","1",5),("H","uruguay","cape_verde","1",4),("I","france","iraq","1",4),("I","norway","senegal","1",3),("J","argentina","austria","1",3),("J","jordan","algeria","2",4),("K","portugal","uzbekistan","1",4),("K","colombia","dr_congo","1",4),("L","england","ghana","1",4),("L","panama","croatia","2",3),
("A","czechia","mexico","2",3),("A","south_africa","south_korea","2",3),("B","switzerland","canada","X",3),("B","bosnia_and_herzegovina","qatar","1",3),("C","scotland","brazil","X",3),("C","morocco","haiti","1",4),("D","turkiye","united_states","2",3),("D","paraguay","australia","1",2),("E","ecuador","germany","X",3),("E","curacao","ivory_coast","2",4),("F","japan","sweden","1",3),("F","tunisia","netherlands","2",3),("G","egypt","iran","1",3),("G","new_zealand","belgium","2",3),("H","cape_verde","saudi_arabia","1",2),("H","uruguay","spain","2",3),("I","norway","france","2",3),("I","senegal","iraq","1",3),("J","algeria","austria","1",2),("J","jordan","argentina","2",4),("K","colombia","portugal","X",3),("K","dr_congo","uzbekistan","1",3),("L","panama","england","2",4),("L","croatia","ghana","1",4)]
def aprobs(pick,conf):
    home={5:(.72,.18,.10),4:(.62,.22,.16),3:(.50,.27,.23),2:(.42,.30,.28)}
    draw={4:(.30,.44,.26),3:(.32,.40,.28),2:(.33,.36,.31)}
    if pick=="1":return home[conf]
    if pick=="2":p1,pX,p2=home[conf];return(p2,pX,p1)
    return draw[conf]
GP={(g,h,a):aprobs(pk,cf) for g,h,a,pk,cf in G72}
# sede+altitud por partido de grupo (match home->venue)
GV={}
for m in VEN.get("group_matches",[]):
    GV[(m.get("team1") or m.get("home"), m.get("team2") or m.get("away"))]=m
VENUES=VEN["venues"]

# ---------- scorers v2 ----------
SC=json.load(open(B+"scorers_v2.json"))["players"]
NP=len(SC)
team_sc=defaultdict(list)
for i,p in enumerate(SC): team_sc[p["team"]].append(i)
xgw=np.array([p.get("xg_per90",0.2)*p.get("minutes_share",0.8) for p in SC])
asw=np.array([p.get("assists_per90",0.1)*p.get("minutes_share",0.8) for p in SC])
pen1={t:next((i for i in team_sc[t] if SC[i].get("penalty_order")==1),None) for t in TEAMS}
ROLE={"MC":1.6,"EXT":1.3,"DEF":1.2,"DEL":1.0}
PEN_RATE=0.10; ASSIST_RATE=0.72; rho=-0.13; MAXG=9  # F7: PEN_RATE bajado (Bota->~7)
FACT=np.array([math.factorial(k) for k in range(MAXG+1)])
def pois_vec(lam):
    k=np.arange(MAXG+1); return np.exp(-lam)*lam**k/FACT

def dc_matrix(lh,la):
    ph=pois_vec(lh); pa=pois_vec(la); M=np.outer(ph,pa)
    M[0,0]*=1-lh*la*rho; M[0,1]*=1+lh*rho; M[1,0]*=1+la*rho; M[1,1]*=1-rho
    s=M.sum();  return M/s if s>0 else M

def lam(h,a,mh=1.0,ma=1.0):
    lh=rat[h]["att"]*(rat[a]["def"]/DBAR)*mh
    la=rat[a]["att"]*(rat[h]["def"]/DBAR)*ma
    tilt=(rat[h]["rating"]-rat[a]["rating"])/2800.0  # F7: destemplado por backtest
    lh*=(1+tilt); la*=(1-tilt)
    return min(max(lh,0.15),4.0),min(max(la,0.15),4.0)

def host_mult(t, ko=False):
    # Mexico: local + altitud en fase grupos; USA/Canada: ventaja local
    if t=="mexico": return 1.06 if ko else 1.06*1.10
    if t in HOSTS:  return 1.05 if ko else 1.06
    return 1.0

def sample_score(M):
    idx=rng.choice(M.size,p=M.ravel()); return idx//M.shape[1], idx%M.shape[1]

def attribute(team,goals,gbox,abox):
    if goals<=0: return
    ids=team_sc.get(team,[])
    if ids:
        w=xgw[ids]; w=w/w.sum() if w.sum()>0 else None
        aw=asw[ids]; aw=aw/aw.sum() if aw.sum()>0 else None
    for _ in range(goals):
        # penalti?
        if rng.random()<PEN_RATE and pen1.get(team) is not None:
            gbox[pen1[team]]+=1
        elif ids and w is not None:
            other=0.85*xgw[ids].sum()  # F7: mas peso a no-listados (Bota menos inflada)
            ww=np.append(xgw[ids],other); ww=ww/ww.sum()
            pick=rng.choice(len(ids)+1,p=ww)
            if pick<len(ids): gbox[ids[pick]]+=1
        # asistencia
        if ids and aw is not None and rng.random()<ASSIST_RATE:
            abox[rng.choice(ids,p=aw)]+=1

def grp_match(g,h,a,gbox,abox):
    p1,pX,p2=GP[(g,h,a)]
    lh,la=lam(h,a,host_mult(h),host_mult(a))
    M=dc_matrix(lh,la)
    # categorias DC
    dcH=np.tril(M,-1).sum(); dcA=np.triu(M,1).sum(); dcD=np.trace(M)
    # reweight hacia prior analisis (blend suave 50%)
    import numpy as _np
    fH=(0.5+0.5*p1/max(dcH,1e-6)); fD=(0.5+0.5*pX/max(dcD,1e-6)); fA=(0.5+0.5*p2/max(dcA,1e-6))
    W=M.copy()
    iu=_np.triu_indices(MAXG+1,1); il=_np.tril_indices(MAXG+1,-1)
    W[il]*=fH; W[iu]*=fA
    for d in range(MAXG+1): W[d,d]*=fD
    W/=W.sum()
    gh,ga=sample_score(W)
    attribute(h,gh,gbox,abox); attribute(a,ga,gbox,abox)
    return gh,ga

def ko_match(h,a,gbox,abox,host_edge=True):
    mh=host_mult(h,ko=True) if host_edge else 1.0
    ma=host_mult(a,ko=True) if host_edge else 1.0
    lh,la=lam(h,a,mh,ma)
    gh,ga=sample_score(dc_matrix(lh,la))
    attribute(h,gh,gbox,abox); attribute(a,ga,gbox,abox)
    if gh==ga:
        eh,ea=sample_score(dc_matrix(lh*0.33,la*0.33))
        attribute(h,eh,gbox,abox); attribute(a,ea,gbox,abox); gh+=eh; ga+=ea
    if gh>ga: return h
    if ga>gh: return a
    pp=float(np.clip(0.5+(rat[h]["rating"]-rat[a]["rating"])/6000,0.40,0.60))
    return h if rng.random()<pp else a

def standings(g,res):
    tab={t:{"pts":0,"gf":0,"gc":0} for t in GROUPS[g]}
    for (h,a),(gh,ga) in res.items():
        tab[h]["gf"]+=gh;tab[h]["gc"]+=ga;tab[a]["gf"]+=ga;tab[a]["gc"]+=gh
        if gh>ga:tab[h]["pts"]+=3
        elif gh==ga:tab[h]["pts"]+=1;tab[a]["pts"]+=1
        else:tab[a]["pts"]+=3
    order=sorted(GROUPS[g],key=lambda t:(-tab[t]["pts"],-(tab[t]["gf"]-tab[t]["gc"]),-tab[t]["gf"],rng.random()))
    return order,tab

champ=defaultdict(int);rounds=defaultdict(lambda:defaultdict(int));QUAL=defaultdict(int)
gb_lead=defaultdict(int);gb_goals=[];mvp=defaultdict(int)
HOSTSLOTS=["A","B","D","E","G","I","K","L"]

def rating_draw(t):  # muestrea rating con incertidumbre inter-lente
    return rat[t]["rating"]

for it in range(N):
    # incertidumbre de rating: perturbar por iteracion (sd entre lentes)
    base={t:rat[t]["rating"] for t in TEAMS}
    for t in TEAMS: rat[t]["rating"]=base[t]+rng.normal(0,max(rat[t]["sd"],8))
    gbox=np.zeros(NP,int); abox=np.zeros(NP,int)
    pos1={};pos2={};thirds=[]
    for g in GROUPS:
        res={(h,a):grp_match(g,h,a,gbox,abox) for(gg,h,a,_,_) in G72 if gg==g}
        order,tab=standings(g,res)
        pos1[g],pos2[g]=order[0],order[1]
        s=tab[order[2]]; thirds.append((g,order[2],s["pts"],s["gf"]-s["gc"],s["gf"]))
        QUAL[order[0]]+=1;QUAL[order[1]]+=1
    ranked=sorted(thirds,key=lambda x:(-x[2],-x[3],-x[4]))[:8]
    combo="".join(sorted(g for g,*_ in ranked))
    qthird={g:t for g,t,*_ in ranked}
    for g,t,*_ in ranked: QUAL[t]+=1; rounds[t]["R32"]+=1
    for g in GROUPS: rounds[pos1[g]]["R32"]+=1; rounds[pos2[g]]["R32"]+=1
    # asignacion oficial FIFA de terceros
    alloc=THIRDS.get(combo)
    def third_of(hg):
        if alloc: return qthird[alloc[f"1{hg}"][1]]   # alloc da "3X"; tomar grupo X
        return qthird[sorted(qthird)[HOSTSLOTS.index(hg)%len(qthird)]]
    W={}
    def ko(h,a,host=False): w=ko_match(h,a,gbox,abox,host); return w
    w73=ko(pos2["A"],pos2["B"]);w74=ko(pos1["E"],third_of("E"),True);w75=ko(pos1["F"],pos2["C"]);w76=ko(pos1["C"],pos2["F"])
    w77=ko(pos1["I"],third_of("I"),True);w78=ko(pos2["E"],pos2["I"]);w79=ko(pos1["A"],third_of("A"),True);w80=ko(pos1["L"],third_of("L"),True)
    w81=ko(pos1["D"],third_of("D"),True);w82=ko(pos1["G"],third_of("G"),True);w83=ko(pos2["K"],pos2["L"]);w84=ko(pos1["H"],pos2["J"],True)
    w85=ko(pos1["B"],third_of("B"),True);w86=ko(pos1["J"],pos2["H"],True);w87=ko(pos1["K"],third_of("K"),True);w88=ko(pos2["D"],pos2["G"])
    for w in[w73,w74,w75,w76,w77,w78,w79,w80,w81,w82,w83,w84,w85,w86,w87,w88]:rounds[w]["R16"]+=1
    w89=ko(w74,w77);w90=ko(w73,w75);w91=ko(w76,w78);w92=ko(w79,w80);w93=ko(w83,w84);w94=ko(w81,w82);w95=ko(w86,w88);w96=ko(w85,w87)
    for w in[w89,w90,w91,w92,w93,w94,w95,w96]:rounds[w]["QF"]+=1
    w97=ko(w89,w90);w98=ko(w93,w94);w99=ko(w91,w92);w100=ko(w95,w96)
    for w in[w97,w98,w99,w100]:rounds[w]["SF"]+=1
    w101=ko(w97,w98);w102=ko(w99,w100); rounds[w101]["F"]+=1;rounds[w102]["F"]+=1
    wc=ko(w101,w102); champ[wc]+=1; rounds[wc]["W"]+=1
    lead=int(np.argmax(gbox)); gl=int(gbox[lead])
    if gl>0: gb_lead[SC[lead]["name"]]+=1; gb_goals.append(gl)
    fin={w101,w102};sf={w97,w98,w99,w100}
    best=None;bs=-1
    for i,p in enumerate(SC):
        tm=p["team"]
        if tm in sf or tm in fin:
            stard=p.get("xg_per90",.2)+p.get("assists_per90",.1)
            bonus=6 if tm==wc else(4 if tm in fin else 3)
            score=gbox[i]+1.1*abox[i]+2.5*stard+ROLE.get(p["pos"],1.0)*0.8+bonus
            if score>bs: bs=score;best=p["name"]
    if best: mvp[best]+=1
    for t in TEAMS: rat[t]["rating"]=base[t]

def wilson(c,n):
    if n==0:return(0,0)
    p=c/n;z=1.96;den=1+z*z/n
    ctr=(p+z*z/2/n)/den;half=z*math.sqrt(p*(1-p)/n+z*z/4/n/n)/den
    return(round(100*(ctr-half),1),round(100*(ctr+half),1))
def top(d,n=12):return sorted(d.items(),key=lambda x:-x[1])[:n]
out={"N":N,"seed":SEED,
"champion":[(t,round(100*c/N,1),wilson(c,N)) for t,c in top(champ)],
"reach_final":[(t,round(100*(rounds[t]["F"]+rounds[t]["W"])/N,1)) for t,_ in top({t:rounds[t]["F"]+rounds[t]["W"] for t in TEAMS})],
"reach_sf":[(t,round(100*rounds[t]["SF"]/N,1)) for t,_ in top({t:rounds[t]["SF"] for t in TEAMS})],
"golden_boot":[(n,round(100*c/N,1)) for n,c in top(gb_lead)],
"gb_goals_median":int(np.median(gb_goals)),"gb_goals_p25":int(np.percentile(gb_goals,25)),"gb_goals_p90":int(np.percentile(gb_goals,90)),
"mvp":[(n,round(100*c/N,1)) for n,c in top(mvp)],
"qualify_iran":round(100*QUAL["iran"]/N,1)}
json.dump(out,open(B+"mc_results_v2.json","w"),ensure_ascii=False,indent=1)
print(f"=== v2 N={N} seed={SEED} ===")
print("CAMPEON (P% [IC95]):"); [print(f"  {t:16}{p:5}%  [{lo}-{hi}]") for t,p,(lo,hi) in out["champion"]]
print("BOTA DE ORO:"); [print(f"  {n:22}{p}%") for n,p in out["golden_boot"][:6]]
print(f"  goles lider: mediana {out['gb_goals_median']} (p25 {out['gb_goals_p25']} - p90 {out['gb_goals_p90']})")
print("MVP:"); [print(f"  {n:22}{p}%") for n,p in out["mvp"][:6]]
print("Iran pasa grupo:",out["qualify_iran"],"%")
