#!/usr/bin/env python3
"""Calcula clasificacion final fase de grupos WC2026 a partir de marcadores proyectados.
Reglas FIFA: pts, dif goles, goles a favor. Mejores terceros: top 8 por (pts, dg, gf)."""

# (grupo, equipoA, golesA, golesB, equipoB)
R = [
# J1
("A","Mexico",2,0,"Sudafrica"),("A","Corea",1,1,"Chequia"),
("B","Canada",2,1,"Bosnia"),("B","Qatar",0,2,"Suiza"),
("C","Brasil",2,1,"Marruecos"),("C","Haiti",0,1,"Escocia"),
("D","EEUU",2,1,"Paraguay"),("D","Australia",1,2,"Turquia"),
("E","Alemania",3,0,"Curazao"),("E","CostaMarfil",1,1,"Ecuador"),
("F","PaisesBajos",2,1,"Japon"),("F","Suecia",1,0,"Tunez"),
("G","Belgica",2,0,"Egipto"),("G","Iran",1,0,"NuevaZelanda"),
("H","Espana",2,0,"CaboVerde"),("H","ArabiaSaudita",0,2,"Uruguay"),
("I","Francia",2,1,"Senegal"),("I","Irak",0,2,"Noruega"),
("J","Argentina",2,0,"Argelia"),("J","Austria",2,0,"Jordania"),
("K","Portugal",2,0,"RDCongo"),("K","Uzbekistan",0,2,"Colombia"),
("L","Inglaterra",2,1,"Croacia"),("L","Ghana",1,1,"Panama"),
# J2
("A","Chequia",2,0,"Sudafrica"),("A","Mexico",2,1,"Corea"),
("B","Suiza",2,0,"Bosnia"),("B","Canada",2,0,"Qatar"),
("C","Escocia",1,2,"Marruecos"),("C","Brasil",3,0,"Haiti"),
("D","EEUU",2,1,"Australia"),("D","Turquia",2,0,"Paraguay"),
("E","Alemania",2,0,"CostaMarfil"),("E","Ecuador",2,0,"Curazao"),
("F","PaisesBajos",2,0,"Suecia"),("F","Tunez",0,1,"Japon"),
("G","Belgica",2,0,"Iran"),("G","NuevaZelanda",0,1,"Egipto"),
("H","Espana",3,0,"ArabiaSaudita"),("H","Uruguay",2,0,"CaboVerde"),
("I","Francia",3,0,"Irak"),("I","Noruega",2,1,"Senegal"),
("J","Argentina",2,1,"Austria"),("J","Jordania",0,2,"Argelia"),
("K","Portugal",3,0,"Uzbekistan"),("K","Colombia",2,0,"RDCongo"),
("L","Inglaterra",2,0,"Ghana"),("L","Panama",1,2,"Croacia"),
# J3
("A","Chequia",1,2,"Mexico"),("A","Sudafrica",0,2,"Corea"),
("B","Suiza",1,1,"Canada"),("B","Bosnia",2,1,"Qatar"),
("C","Escocia",1,1,"Brasil"),("C","Marruecos",3,1,"Haiti"),
("D","Turquia",1,2,"EEUU"),("D","Paraguay",1,0,"Australia"),
("E","Ecuador",1,1,"Alemania"),("E","Curazao",0,3,"CostaMarfil"),
("F","Japon",2,1,"Suecia"),("F","Tunez",0,1,"PaisesBajos"),
("G","Egipto",1,0,"Iran"),("G","NuevaZelanda",0,2,"Belgica"),
("H","CaboVerde",1,0,"ArabiaSaudita"),("H","Uruguay",1,2,"Espana"),
("I","Noruega",1,2,"Francia"),("I","Senegal",1,0,"Irak"),
("J","Argelia",1,0,"Austria"),("J","Jordania",0,2,"Argentina"),
("K","Colombia",1,1,"Portugal"),("K","RDCongo",1,0,"Uzbekistan"),
("L","Panama",0,2,"Inglaterra"),("L","Croacia",2,1,"Ghana"),
]

from collections import defaultdict
T = defaultdict(lambda:{"g":"","pj":0,"pg":0,"pe":0,"pp":0,"gf":0,"gc":0,"pts":0})

def add(g,team,gf,gc):
    t=T[team]; t["g"]=g; t["pj"]+=1; t["gf"]+=gf; t["gc"]+=gc
    if gf>gc: t["pg"]+=1; t["pts"]+=3
    elif gf==gc: t["pe"]+=1; t["pts"]+=1
    else: t["pp"]+=1

for g,a,ga,gb,b in R:
    add(g,a,ga,gb); add(g,b,gb,ga)

def dg(t): return t["gf"]-t["gc"]
def key(item): t=item[1]; return (-t["pts"],-dg(t),-t["gf"])

groups=defaultdict(list)
for name,t in T.items(): groups[t["g"]].append((name,t))

out=["# Clasificacion Final Proyectada — Fase de Grupos\n",
     "> Segun marcadores proyectados (no reales). Reglas FIFA: pts > dif goles > goles favor.\n"]
thirds=[]
qualified_1_2=[]
for g in sorted(groups):
    tabla=sorted(groups[g],key=key)
    out.append(f"\n## Grupo {g}\n")
    out.append("| Pos | Equipo | PJ | G | E | P | GF | GC | DG | Pts |")
    out.append("|:--:|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|")
    for i,(name,t) in enumerate(tabla,1):
        mark=" ✅" if i<=2 else (" ⭐" if i==3 else "")
        out.append(f"| {i}{mark} | {name} | {t['pj']} | {t['pg']} | {t['pe']} | {t['pp']} | "
                   f"{t['gf']} | {t['gc']} | {dg(t):+d} | **{t['pts']}** |")
    qualified_1_2.append((g,tabla[0][0],tabla[1][0]))
    n,t=tabla[2]; thirds.append((g,n,t["pts"],dg(t),t["gf"]))

# mejores terceros
thirds_sorted=sorted(thirds,key=lambda x:(-x[2],-x[3],-x[4]))
out.append("\n---\n\n## Mejores terceros (8 clasifican)\n")
out.append("| # | Grupo | Equipo | Pts | DG | GF | ¿Clasifica? |")
out.append("|:--:|:--:|---|:--:|:--:|:--:|:--:|")
for i,(g,n,p,d,gf) in enumerate(thirds_sorted,1):
    ok="✅ SÍ" if i<=8 else "❌ NO"
    out.append(f"| {i} | {g} | {n} | {p} | {d:+d} | {gf} | {ok} |")

best8=set(x[0] for x in thirds_sorted[:8])
out.append("\n## Resumen clasificados a 32avos\n")
out.append("| Grupo | 1º | 2º | 3º (clasifica?) |")
out.append("|:--:|---|---|---|")
third_by_g={g:(n,p,d) for g,n,p,d,gf in thirds}
for g,first,second in qualified_1_2:
    tn,tp,td=third_by_g[g]
    q="✅" if g in best8 else "❌"
    out.append(f"| {g} | {first} | {second} | {tn} {q} |")

import os
path="/Users/erickhein/TechWorkspace/active_projects/misc/polla_mundial_2026/partidos/analisis/_clasificacion_final_proyectada.md"
open(path,"w").write("\n".join(out)+"\n")
print("OK ->",os.path.basename(path))
print("\nMejores terceros (orden):")
for i,(g,n,p,d,gf) in enumerate(thirds_sorted,1):
    print(f"  {i}. {n} (Gr{g}) {p}pts {d:+d}dg {gf}gf {'IN' if i<=8 else 'OUT'}")
