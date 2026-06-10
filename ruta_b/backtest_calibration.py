#!/usr/bin/env python3
"""F6 — Backtest del modelo de gol contra Mundiales 2018/2022.
Valida Dixon-Coles + Elo->lambda con RPS/Brier/log-loss + reliability + LOTO-CV.
Compara DC vs Poisson puro. Decide perillas (gate)."""
import json, math, numpy as np
B="/Users/erickhein/TechWorkspace/active_projects/misc/polla_mundial_2026/ruta_b/"
WC={y:json.load(open(B+f"backtest/wc{y}.json")) for y in(2018,2022)}
MAXG=9; FACT=np.array([math.factorial(k) for k in range(MAXG+1)])
def pois_vec(l):
    k=np.arange(MAXG+1); return np.exp(-l)*l**k/FACT
def dc_mat(lh,la,rho):
    M=np.outer(pois_vec(lh),pois_vec(la))
    M[0,0]*=1-lh*la*rho;M[0,1]*=1+lh*rho;M[1,0]*=1+la*rho;M[1,1]*=1-rho
    s=M.sum();return M/s if s>0 else M
def cats(M):  # P(home),P(draw),P(away)
    return float(np.tril(M,-1).sum()),float(np.trace(M)),float(np.triu(M,1).sum())

def lam_from_elo(rh,ra,base,c,host=0):
    d=(rh-ra)/400.0
    lh=base*math.exp(c*d+0.12*host); la=base*math.exp(-c*d-0.12*host)
    return min(max(lh,.15),4.5),min(max(la,.15),4.5)

def matches(years):
    out=[]
    for y in years:
        d=WC[y]; elo=d.get("elo_pre",{}); host={2018:"russia",2022:"qatar"}[y]
        for m in d["group_results"]:
            h,a=m["home"],m["away"]; rh=elo.get(h,1500); ra=elo.get(a,1500)
            o=0 if m["hg"]>m["ag"] else(1 if m["hg"]==m["ag"] else 2)
            out.append((rh,ra,o,1 if h==host else(-1 if a==host else 0)))
    return out

def rps(p,o):  # p=(H,D,A), o in 0/1/2 ; ordered ranked prob score
    oc=[0,0,0]; oc[o]=1
    c1=p[0]-oc[0]; c2=p[0]+p[1]-oc[0]-oc[1]
    return 0.5*(c1*c1+c2*c2)
def brier(p,o):
    oc=[0,0,0]; oc[o]=1; return sum((p[i]-oc[i])**2 for i in range(3))
def logl(p,o):
    return -math.log(max(p[o],1e-9))

def evaluate(data,base,c,rho):
    rp=br=ll=0
    for rh,ra,o,hs in data:
        lh,la=lam_from_elo(rh,ra,base,c,hs); p=cats(dc_mat(lh,la,rho))
        s=sum(p); p=[x/s for x in p]
        rp+=rps(p,o); br+=brier(p,o); ll+=logl(p,o)
    n=len(data); return rp/n,br/n,ll/n

def fit(train,rho):
    best=None
    for base in np.arange(1.15,1.65,0.05):
        for c in np.arange(0.25,1.05,0.05):
            r,_,_=evaluate(train,base,c,rho)
            if best is None or r<best[0]: best=(r,base,c)
    return best[1],best[2]

ALL=matches([2018,2022])
print(f"Partidos backtest (grupos 2018+2022): {len(ALL)}")
# grid global
b,c=fit(ALL,-0.13)
print(f"\nMejor ajuste (DC, rho=-0.13): base={b:.2f}, c={c:.2f}")
for tag,rho in [("Dixon-Coles",-0.13),("Poisson puro",0.0)]:
    r,br_,ll=evaluate(ALL,b,c,rho)
    print(f"  {tag:13} RPS={r:.4f}  Brier={br_:.4f}  LogLoss={ll:.4f}")

# baseline naive: prob base historica del Mundial (H .47 D .25 A .28 aprox sin localia -> usar .40/.27/.33)
base_p=[0.40,0.27,0.33]
rp=np.mean([rps(base_p,o) for *_,o,_ in [(0,0,m[2],0) for m in ALL]])
rp_base=np.mean([rps(base_p,m[2]) for m in ALL])
print(f"  {'Baseline fijo':13} RPS={rp_base:.4f}  (predice {base_p})")

# LOTO-CV
print("\nLOTO-CV (entrena en uno, testea en el otro):")
for tr,te in [([2018],[2022]),([2022],[2018])]:
    bb,cc=fit(matches(tr),-0.13)
    r_dc,_,_=evaluate(matches(te),bb,cc,-0.13)
    r_po,_,_=evaluate(matches(te),bb,cc,0.0)
    print(f"  train {tr} -> test {te}: base={bb:.2f} c={cc:.2f} | RPS DC={r_dc:.4f} vs Poisson={r_po:.4f}  -> DC {'MEJOR' if r_dc<r_po else 'no mejora'}")

# reliability (bins de P(home win))
print("\nReliability P(victoria favorito-home):")
preds=[]
for rh,ra,o,hs in ALL:
    lh,la=lam_from_elo(rh,ra,b,c,hs); p=cats(dc_mat(lh,la,-0.13)); s=sum(p)
    preds.append((p[0]/s, 1 if o==0 else 0))
preds.sort()
for lo,hi in [(0,.2),(.2,.35),(.35,.5),(.5,.65),(.65,1)]:
    grp=[(pp,oo) for pp,oo in preds if lo<=pp<hi]
    if grp:
        print(f"  pred {lo:.2f}-{hi:.2f}: predicho {np.mean([g[0] for g in grp]):.2f}  real {np.mean([g[1] for g in grp]):.2f}  (n={len(grp)})")

# verdict sobre la concentracion de v2
print("\n--- Veredicto gate ---")
v2=json.load(open(B+"mc_results_v2.json"))
print("Campeon v2 top5:", [(t,p) for t,p,_ in v2["champion"][:5]])
print("Bota v2: mediana", v2["gb_goals_median"], "(real: 2018=6, 2022=8)")
print("KO winners 2018/2022 reales para chequear acierto del modelo:")
acc=tot=0
for y in(2018,2022):
    d=WC[y]; elo=d.get("elo_pre",{})
    for m in d.get("ko_results",[]):
        rh,ra=elo.get(m["home"],1500),elo.get(m["away"],1500)
        fav=m["home"] if rh>=ra else m["away"]
        if "winner" in m: tot+=1; acc+= (fav==m["winner"])
print(f"  acierto 'favorito Elo avanza' = {acc}/{tot} = {100*acc/max(tot,1):.0f}%")
