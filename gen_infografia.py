#!/usr/bin/env python3
"""infografia_polla.png — resumen visual completo (vertical, compartible).
4 respuestas + resultados de los 12 grupos + árbol de eliminatoria hasta la final."""
import json, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
B="/Users/erickhein/TechWorkspace/active_projects/misc/polla_mundial_2026/"
MC=json.load(open(B+"ruta_b/mc_results_v2.json"))

NAVY="#13294b"; GOLD="#e3a81e"; INK="#1c2530"; GREY="#9aa3b0"; GREEN="#1f9d61"; RED="#c0485a"
CARD="#f5f7fa"; LINE="#cfd6df"; BG="#ffffff"

fig=plt.figure(figsize=(12,21),dpi=100); fig.patch.set_facecolor(BG)
ax=fig.add_axes([0,0,1,1]); ax.axis("off"); ax.set_xlim(0,120); ax.set_ylim(0,210)

# ---------- HEADER ----------
ax.add_patch(Rectangle((0,200),120,10,color=NAVY))
ax.add_patch(Rectangle((0,199),120,1,color=GOLD))
ax.text(60,205.3,"POLLA MUNDIAL 2026",ha="center",va="center",color="white",fontsize=34,fontweight="bold")
ax.text(60,201.4,"Pronóstico — Ruta agéntica + Monte Carlo 30.000 torneos (calibrado con backtest 2018/22)",
        ha="center",va="center",color="#cfd9e8",fontsize=12)

# ---------- 4 RESPUESTAS ----------
ans=[("1","CAMPEÓN","España","≈ Francia · empate"),
     ("2","MEJOR JUGADOR","Mbappé","alt. Yamal/Messi"),
     ("3","BOTA DE ORO","Mbappé",f"{MC['golden_boot'][0][1]}% líder"),
     ("4","GOLES BOTA","7","rango 6–9")]
cw=27.5; x0=4
for i,(n,lab,a,sub) in enumerate(ans):
    x=x0+i*(cw+1.3); y=184
    ax.add_patch(FancyBboxPatch((x,y),cw,12.5,boxstyle="round,pad=0.3,rounding_size=1.4",fc=CARD,ec=LINE,lw=1))
    ax.add_patch(Circle((x+3.5,y+9),2.1,color=NAVY))
    ax.text(x+3.5,y+9,n,ha="center",va="center",color="white",fontsize=14,fontweight="bold")
    ax.text(x+7,y+9.2,lab,ha="left",va="center",color=GREY,fontsize=9.5,fontweight="bold")
    ax.text(x+2.5,y+4.7,a,ha="left",va="center",color=NAVY,fontsize=17,fontweight="bold")
    ax.text(x+2.5,y+1.8,sub,ha="left",va="center",color=GREEN,fontsize=9)

# ---------- GRUPOS ----------
ax.text(6,179,"RESULTADOS DE GRUPOS",ha="left",va="center",color=NAVY,fontsize=15,fontweight="bold")
ax.text(60,179,"clasifican 1º · 2º · mejores 8 terceros",ha="left",va="center",color=GREY,fontsize=10)
# (equipo, estado): q=clasifica 1/2, t_in=mejor tercero, t_out=tercero fuera, out=eliminado
G={
"A":[("México","q"),("Corea","q"),("Chequia","t_in"),("Sudáfrica","out")],
"B":[("Suiza","q"),("Canadá","q"),("Bosnia","t_in"),("Qatar","out")],
"C":[("Brasil","q"),("Marruecos","q"),("Escocia","t_in"),("Haití","out")],
"D":[("EEUU","q"),("Turquía","q"),("Paraguay","t_in"),("Australia","out")],
"E":[("Alemania","q"),("Ecuador","q"),("C. Marfil","t_in"),("Curazao","out")],
"F":[("P. Bajos","q"),("Japón","q"),("Suecia","t_in"),("Túnez","out")],
"G":[("Bélgica","q"),("Egipto","q"),("Irán","t_out"),("N. Zelanda","out")],
"H":[("España","q"),("Uruguay","q"),("Cabo Verde","t_out"),("A. Saudí","out")],
"I":[("Francia","q"),("Noruega","q"),("Senegal","t_in"),("Irak","out")],
"J":[("Argentina","q"),("Argelia","q"),("Austria","t_in"),("Jordania","out")],
"K":[("Portugal","q"),("Colombia","q"),("RD Congo","t_out"),("Uzbekistán","out")],
"L":[("Inglaterra","q"),("Croacia","q"),("Ghana","t_out"),("Panamá","out")]}
COL={"q":NAVY,"t_in":GREEN,"t_out":RED,"out":GREY}
gw=27.5; gh=22.5
for idx,(g,rows) in enumerate(G.items()):
    c=idx%4; r=idx//4
    x=4+c*(gw+1.3); y=152-r*(gh+1.5)
    ax.add_patch(FancyBboxPatch((x,y),gw,gh,boxstyle="round,pad=0.2,rounding_size=1",fc=CARD,ec=LINE,lw=1))
    ax.add_patch(Rectangle((x+0.6,y+gh-4.4),gw-1.2,3.8,color=NAVY))
    ax.text(x+1.8,y+gh-2.5,f"Grupo {g}",ha="left",va="center",color="white",fontsize=11,fontweight="bold")
    for j,(team,stt) in enumerate(rows):
        ry=y+gh-7.5-j*3.9
        ax.add_patch(Circle((x+2.2,ry),0.7,color=COL[stt]))
        ax.text(x+4,ry,team,ha="left",va="center",color=COL[stt] if stt!="out" else GREY,
                fontsize=11,fontweight="bold" if stt in("q","t_in") else "normal")
        ax.text(x+gw-1.5,ry,str(j+1),ha="right",va="center",color=GREY,fontsize=9.5)

# ---------- BRACKET ----------
ax.text(6,93.5,"CAMINO A LA FINAL",ha="left",va="center",color=NAVY,fontsize=15,fontweight="bold")
ax.text(48,93.5,"cuadro final (Ruta A) · desde octavos",ha="left",va="center",color=GREY,fontsize=10)
ax.text(114,93.5,"MC: España≈Francia 15.7%",ha="right",va="center",color=GREY,fontsize=9)

cols=[
 ["Alemania","Francia","Corea","Marruecos","Croacia","España","EEUU","Bélgica",
  "Brasil","Ecuador","México","Inglaterra","Argentina","Turquía","Suiza","Portugal"],
 ["Francia","Marruecos","España","Bélgica","Brasil","Inglaterra","Argentina","Portugal"],
 ["Francia","España","Inglaterra","Argentina"],
 ["España","Inglaterra"],
 ["España"]]
labels=["OCTAVOS","CUARTOS","SEMIS","FINAL","CAMPEÓN"]
xcol=[8,34,60,84,106]; YT=86; YB=6; H=YT-YB
def yslot(col,i): n=len(col); return YT-(i+0.5)*(H/n)
for ci,col in enumerate(cols):
    ax.text(xcol[ci]+(11 if ci<4 else 6)/2 if ci<4 else xcol[ci],YT+2.2,labels[ci],
            ha="center",va="center",color=NAVY,fontsize=9.5,fontweight="bold")
nxt=lambda ci,i: cols[ci+1][i//2] if ci+1<len(cols) else None
for ci,col in enumerate(cols):
    bw=20 if ci==0 else 17
    for i,team in enumerate(col):
        y=yslot(col,i); x=xcol[ci]
        adv = (ci<len(cols)-1 and team==cols[ci+1][i//2]) or (ci==len(cols)-1)
        champ = team=="España"
        fc = GOLD if champ else (NAVY if adv else "white")
        ec = GOLD if champ else (NAVY if adv else LINE)
        tc = "white" if (champ or adv) else GREY
        ax.add_patch(FancyBboxPatch((x,y-1.6),bw,3.2,boxstyle="round,pad=0.1,rounding_size=0.6",
                     fc=fc,ec=ec,lw=1.2,zorder=3))
        ax.text(x+1.4,y,team,ha="left",va="center",color=tc,fontsize=10,
                fontweight="bold" if (champ or adv) else "normal",zorder=4)
        # conector al siguiente
        if ci<len(cols)-1:
            yn=yslot(cols[ci+1],i//2); xn=xcol[ci+1]
            xm=x+bw+ (xn-(x+bw))/2
            ax.plot([x+bw,xm],[y,y],color=LINE,lw=1.1,zorder=1)
            ax.plot([xm,xm],[y,yn],color=LINE,lw=1.1,zorder=1)
            ax.plot([xm,xn],[yn,yn],color=LINE,lw=1.1,zorder=1)
# sello campeon
ax.text(xcol[4]+3,yslot(cols[4],0)-4.0,"CAMPEÓN",ha="left",va="center",color=GOLD,fontsize=12,fontweight="bold")
ax.add_patch(Circle((xcol[4]+1.0,yslot(cols[4],0)),0.9,color=GOLD,zorder=5))
ax.text(6,2.5,"3er puesto: Argentina   ·   48 fichas · 103 análisis partido a partido · backtest RPS 0.220 < baseline",
        ha="left",va="center",color=GREY,fontsize=9.5)

fig.savefig(B+"infografia_polla.png",facecolor=BG,bbox_inches="tight",pad_inches=0.25)
print("OK -> infografia_polla.png")
