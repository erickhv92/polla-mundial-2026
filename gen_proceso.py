#!/usr/bin/env python3
"""proceso_infografia.png — cómo se hizo: pipeline, recursos y coste."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
B="/Users/erickhein/TechWorkspace/active_projects/misc/polla_mundial_2026/"
NAVY="#13294b"; GOLD="#e3a81e"; INK="#1c2530"; GREY="#9aa3b0"; GREEN="#1f9d61"
CARD="#f5f7fa"; LINE="#cfd6df"; BG="#ffffff"

fig=plt.figure(figsize=(12,19),dpi=100); fig.patch.set_facecolor(BG)
ax=fig.add_axes([0,0,1,1]); ax.axis("off"); ax.set_xlim(0,120); ax.set_ylim(0,190)

# HEADER
ax.add_patch(Rectangle((0,180),120,10,color=NAVY)); ax.add_patch(Rectangle((0,179),120,1,color=GOLD))
ax.text(60,185.2,"CÓMO SE HIZO",ha="center",va="center",color="white",fontsize=33,fontweight="bold")
ax.text(60,181.4,"Proceso, recursos y coste — Polla Mundial 2026 (código + trabajo agéntico)",
        ha="center",va="center",color="#cfd9e8",fontsize=12)

# PIPELINE
ax.text(5,175,"PIPELINE DEL ANÁLISIS",ha="left",va="center",color=NAVY,fontsize=15,fontweight="bold")
steps=[
 ("1","Scouting de 48 selecciones","Workflow paralelo: plantel, estrellas, forma, cuotas","50 agentes","1.8M tok",NAVY),
 ("2","Calendario de fase de grupos","12 agentes (1/grupo) → 72 partidos, hora España","12 agentes","0.2M tok",NAVY),
 ("3","Ruta A · análisis de grupos","72 partidos analizados uno a uno (J1·J2·J3), con presión","71 agentes","1.85M tok",NAVY),
 ("4","Ruta A · eliminatoria","32avos→final simulados + bracket oficial FIFA (495 filas)","38 agentes","0.9M tok",NAVY),
 ("5","Ruta B · datos + investigación","Goleadores 48, cuotas devig, terceros, backtest, best-practices","12 agentes","0.4M tok",NAVY),
 ("6","Motor Monte Carlo + backtest","Dixon-Coles · 30.000 torneos · validado 2018/22","CÓDIGO","coste ≈ 0",GREEN),
 ("7","Visualización","App Streamlit + infografías","CÓDIGO","coste ≈ 0",GREEN),
]
for i,(n,t,d,a,tk,clr) in enumerate(steps):
    y=171-i*15.7; x=4
    ax.add_patch(FancyBboxPatch((x,y-12.5),112,12.5,boxstyle="round,pad=0.3,rounding_size=1.2",fc=CARD,ec=LINE,lw=1))
    ax.add_patch(Circle((x+6,y-6.3),3,color=clr))
    ax.text(x+6,y-6.3,n,ha="center",va="center",color="white",fontsize=16,fontweight="bold")
    ax.text(x+12,y-3.6,t,ha="left",va="center",color=NAVY,fontsize=14.5,fontweight="bold")
    ax.text(x+12,y-8.5,d,ha="left",va="center",color="#56606e",fontsize=11)
    # chips derecha
    cax=x+112-1.5
    ax.add_patch(FancyBboxPatch((cax-22,y-9.2),21,3.6,boxstyle="round,pad=0.15,rounding_size=0.8",
                 fc=("#eaf4ee" if clr==GREEN else "#e9edf3"),ec="none"))
    ax.text(cax-11.5,y-7.4,tk,ha="center",va="center",color=(GREEN if clr==GREEN else NAVY),fontsize=11,fontweight="bold")
    ax.add_patch(FancyBboxPatch((cax-22,y-4.9),21,3.6,boxstyle="round,pad=0.15,rounding_size=0.8",
                 fc=(GREEN if clr==GREEN else NAVY),ec="none"))
    ax.text(cax-11.5,y-3.1,a,ha="center",va="center",color="white",fontsize=11,fontweight="bold")

# RECURSOS
ax.text(5,57,"RECURSOS TOTALES",ha="left",va="center",color=NAVY,fontsize=15,fontweight="bold")
tiles=[("~185","subagentes lanzados"),("~6M","tokens de trabajo"),
       ("30.000","torneos simulados · 3,1M partidos"),("~45","archivos generados")]
tw=27.5
for i,(big,lab) in enumerate(tiles):
    x=4+i*(tw+1.3); y=40
    ax.add_patch(FancyBboxPatch((x,y),tw,12.5,boxstyle="round,pad=0.3,rounding_size=1.2",fc=NAVY,ec="none"))
    ax.text(x+tw/2,y+8.2,big,ha="center",va="center",color=GOLD,fontsize=22,fontweight="bold")
    ax.text(x+tw/2,y+3.0,lab,ha="center",va="center",color="white",fontsize=10)

# COSTE
ax.text(5,33,"REPARTO DEL COSTE",ha="left",va="center",color=NAVY,fontsize=15,fontweight="bold")
ax.text(60,33,"el trabajo agéntico domina; la simulación en código fue casi gratis",
        ha="left",va="center",color=GREY,fontsize=10)
bx,bw=4,112; by=25
ax.add_patch(FancyBboxPatch((bx,by),bw,4.4,boxstyle="round,pad=0,rounding_size=0.8",fc=NAVY,ec="none"))
ax.add_patch(Rectangle((bx+bw*0.95,by),bw*0.05,4.4,color=GOLD))
ax.text(bx+bw*0.475,by+2.2,"AGÉNTICO  ~95%  (scouting + 103 análisis + research)",ha="center",va="center",color="white",fontsize=11,fontweight="bold")
ax.text(bx+bw*0.975,by+2.2,"código 5%",ha="center",va="center",color=NAVY,fontsize=9,fontweight="bold")

ax.add_patch(FancyBboxPatch((4,16),112,6.5,boxstyle="round,pad=0.3,rounding_size=1",fc="#fff7e6",ec=GOLD,lw=1.2))
ax.text(60,19.2,"Coste estimado: ≈ 6M tokens de subagentes  ·  orden de magnitud de cientos de USD  ·  ~95% en la fase agéntica",
        ha="center",va="center",color=INK,fontsize=12,fontweight="bold")

ax.text(60,9,"De una narrativa única (Ruta A) a una distribución calibrada y validada (Ruta B v2).",
        ha="center",va="center",color="#56606e",fontsize=11)
ax.text(60,5.2,"Insight: el motor en código simuló 3,1M partidos a coste casi nulo; los agentes aportaron el juicio y los datos.",
        ha="center",va="center",color=GREY,fontsize=10)

fig.savefig(B+"proceso_infografia.png",facecolor=BG,bbox_inches="tight",pad_inches=0.25)
print("OK -> proceso_infografia.png")
