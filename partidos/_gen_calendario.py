#!/usr/bin/env python3
"""Genera calendario fase de grupos WC2026 + indice de seguimiento.
Convierte hora local de sede a hora España (Madrid, CEST UTC+2)."""
from datetime import datetime, timedelta
import json, unicodedata, re

# matchday, date, local HH:MM, utc_offset(h), venue, team1, team2, group
M = [
 # A
 (1,"2026-06-11","13:00",-6,"Estadio Azteca, Ciudad de Mexico","Mexico","Sudafrica","A"),
 (1,"2026-06-11","20:00",-6,"Estadio Akron, Guadalajara","Corea del Sur","Chequia","A"),
 (2,"2026-06-18","12:00",-4,"Mercedes-Benz Stadium, Atlanta","Chequia","Sudafrica","A"),
 (2,"2026-06-18","20:00",-6,"Estadio Akron, Guadalajara","Mexico","Corea del Sur","A"),
 (3,"2026-06-24","19:00",-6,"Estadio Azteca, Ciudad de Mexico","Chequia","Mexico","A"),
 (3,"2026-06-24","19:00",-6,"Estadio BBVA, Monterrey","Sudafrica","Corea del Sur","A"),
 # B
 (1,"2026-06-12","15:00",-4,"BMO Field, Toronto","Canada","Bosnia y Herzegovina","B"),
 (1,"2026-06-13","12:00",-7,"Levi's Stadium, Santa Clara","Qatar","Suiza","B"),
 (2,"2026-06-18","12:00",-7,"SoFi Stadium, Inglewood","Suiza","Bosnia y Herzegovina","B"),
 (2,"2026-06-18","15:00",-7,"BC Place, Vancouver","Canada","Qatar","B"),
 (3,"2026-06-24","12:00",-7,"BC Place, Vancouver","Suiza","Canada","B"),
 (3,"2026-06-24","12:00",-7,"Lumen Field, Seattle","Bosnia y Herzegovina","Qatar","B"),
 # C
 (1,"2026-06-13","18:00",-4,"MetLife Stadium, Nueva York/NJ","Brasil","Marruecos","C"),
 (1,"2026-06-13","21:00",-4,"Gillette Stadium, Boston","Haiti","Escocia","C"),
 (2,"2026-06-19","18:00",-4,"Gillette Stadium, Boston","Escocia","Marruecos","C"),
 (2,"2026-06-19","20:30",-4,"Lincoln Financial Field, Filadelfia","Brasil","Haiti","C"),
 (3,"2026-06-24","18:00",-4,"Hard Rock Stadium, Miami","Escocia","Brasil","C"),
 (3,"2026-06-24","18:00",-4,"Mercedes-Benz Stadium, Atlanta","Marruecos","Haiti","C"),
 # D
 (1,"2026-06-12","18:00",-7,"SoFi Stadium, Inglewood","Estados Unidos","Paraguay","D"),
 (1,"2026-06-13","21:00",-7,"BC Place, Vancouver","Australia","Turquia","D"),
 (2,"2026-06-19","12:00",-7,"Lumen Field, Seattle","Estados Unidos","Australia","D"),
 (2,"2026-06-19","20:00",-7,"Levi's Stadium, Santa Clara","Turquia","Paraguay","D"),
 (3,"2026-06-25","19:00",-7,"SoFi Stadium, Inglewood","Turquia","Estados Unidos","D"),
 (3,"2026-06-25","19:00",-7,"Levi's Stadium, Santa Clara","Paraguay","Australia","D"),
 # E
 (1,"2026-06-14","12:00",-5,"NRG Stadium, Houston","Alemania","Curazao","E"),
 (1,"2026-06-14","19:00",-4,"Lincoln Financial Field, Filadelfia","Costa de Marfil","Ecuador","E"),
 (2,"2026-06-20","16:00",-4,"BMO Field, Toronto","Alemania","Costa de Marfil","E"),
 (2,"2026-06-20","19:00",-5,"Arrowhead Stadium, Kansas City","Ecuador","Curazao","E"),
 (3,"2026-06-25","16:00",-4,"MetLife Stadium, Nueva York/NJ","Ecuador","Alemania","E"),
 (3,"2026-06-25","16:00",-4,"Lincoln Financial Field, Filadelfia","Curazao","Costa de Marfil","E"),
 # F
 (1,"2026-06-14","15:00",-5,"AT&T Stadium, Dallas","Paises Bajos","Japon","F"),
 (1,"2026-06-14","20:00",-6,"Estadio BBVA, Monterrey","Suecia","Tunez","F"),
 (2,"2026-06-20","12:00",-5,"NRG Stadium, Houston","Paises Bajos","Suecia","F"),
 (2,"2026-06-20","22:00",-6,"Estadio BBVA, Monterrey","Tunez","Japon","F"),
 (3,"2026-06-25","18:00",-5,"AT&T Stadium, Dallas","Japon","Suecia","F"),
 (3,"2026-06-25","18:00",-5,"Arrowhead Stadium, Kansas City","Tunez","Paises Bajos","F"),
 # G
 (1,"2026-06-15","12:00",-7,"Lumen Field, Seattle","Belgica","Egipto","G"),
 (1,"2026-06-15","18:00",-7,"SoFi Stadium, Inglewood","Iran","Nueva Zelanda","G"),
 (2,"2026-06-21","12:00",-7,"SoFi Stadium, Inglewood","Belgica","Iran","G"),
 (2,"2026-06-21","18:00",-7,"BC Place, Vancouver","Nueva Zelanda","Egipto","G"),
 (3,"2026-06-26","20:00",-7,"Lumen Field, Seattle","Egipto","Iran","G"),
 (3,"2026-06-26","20:00",-7,"BC Place, Vancouver","Nueva Zelanda","Belgica","G"),
 # H
 (1,"2026-06-15","12:00",-4,"Mercedes-Benz Stadium, Atlanta","Espana","Cabo Verde","H"),
 (1,"2026-06-15","18:00",-4,"Hard Rock Stadium, Miami","Arabia Saudita","Uruguay","H"),
 (2,"2026-06-21","12:00",-4,"Mercedes-Benz Stadium, Atlanta","Espana","Arabia Saudita","H"),
 (2,"2026-06-21","18:00",-4,"Hard Rock Stadium, Miami","Uruguay","Cabo Verde","H"),
 (3,"2026-06-26","19:00",-5,"NRG Stadium, Houston","Cabo Verde","Arabia Saudita","H"),
 (3,"2026-06-26","18:00",-6,"Estadio Akron, Guadalajara","Uruguay","Espana","H"),
 # I
 (1,"2026-06-16","15:00",-4,"MetLife Stadium, Nueva York/NJ","Francia","Senegal","I"),
 (1,"2026-06-16","18:00",-4,"Gillette Stadium, Boston","Irak","Noruega","I"),
 (2,"2026-06-22","17:00",-4,"Lincoln Financial Field, Filadelfia","Francia","Irak","I"),
 (2,"2026-06-22","20:00",-4,"MetLife Stadium, Nueva York/NJ","Noruega","Senegal","I"),
 (3,"2026-06-26","15:00",-4,"Gillette Stadium, Boston","Noruega","Francia","I"),
 (3,"2026-06-26","15:00",-4,"BMO Field, Toronto","Senegal","Irak","I"),
 # J
 (1,"2026-06-16","19:00",-5,"Arrowhead Stadium, Kansas City","Argentina","Argelia","J"),
 (1,"2026-06-16","21:00",-7,"Levi's Stadium, Santa Clara","Austria","Jordania","J"),
 (2,"2026-06-22","11:00",-5,"AT&T Stadium, Dallas","Argentina","Austria","J"),
 (2,"2026-06-22","20:00",-7,"Levi's Stadium, Santa Clara","Jordania","Argelia","J"),
 (3,"2026-06-27","20:00",-5,"Arrowhead Stadium, Kansas City","Argelia","Austria","J"),
 (3,"2026-06-27","20:00",-5,"AT&T Stadium, Dallas","Jordania","Argentina","J"),
 # K
 (1,"2026-06-17","12:00",-5,"NRG Stadium, Houston","Portugal","RD Congo","K"),
 (1,"2026-06-17","20:00",-6,"Estadio Azteca, Ciudad de Mexico","Uzbekistan","Colombia","K"),
 (2,"2026-06-23","12:00",-5,"NRG Stadium, Houston","Portugal","Uzbekistan","K"),
 (2,"2026-06-23","20:00",-6,"Estadio Akron, Guadalajara","Colombia","RD Congo","K"),
 (3,"2026-06-27","19:30",-4,"Hard Rock Stadium, Miami","Colombia","Portugal","K"),
 (3,"2026-06-27","19:30",-4,"Mercedes-Benz Stadium, Atlanta","RD Congo","Uzbekistan","K"),
 # L
 (1,"2026-06-17","15:00",-5,"AT&T Stadium, Dallas","Inglaterra","Croacia","L"),
 (1,"2026-06-17","19:00",-4,"BMO Field, Toronto","Ghana","Panama","L"),
 (2,"2026-06-23","16:00",-4,"Gillette Stadium, Boston","Inglaterra","Ghana","L"),
 (2,"2026-06-23","19:00",-4,"BMO Field, Toronto","Panama","Croacia","L"),
 (3,"2026-06-27","17:00",-4,"MetLife Stadium, Nueva York/NJ","Panama","Inglaterra","L"),
 (3,"2026-06-27","17:00",-4,"Lincoln Financial Field, Filadelfia","Croacia","Ghana","L"),
]

DIAS = ["lunes","martes","miercoles","jueves","viernes","sabado","domingo"]

def es_time(date, hhmm, off):
    dt = datetime.strptime(date+" "+hhmm, "%Y-%m-%d %H:%M")
    utc = dt - timedelta(hours=off)        # local -> UTC
    return utc + timedelta(hours=2)        # UTC -> Madrid CEST

def slug(t1,t2,g):
    s = f"{g}-{t1}-{t2}".lower()
    s = unicodedata.normalize("NFD",s).encode("ascii","ignore").decode()
    return re.sub(r"[^a-z0-9]+","-",s).strip("-")

rows = []
for md,date,hhmm,off,venue,t1,t2,g in M:
    es = es_time(date,hhmm,off)
    rows.append({"md":md,"date":date,"local":hhmm,"off":off,"venue":venue,
                 "t1":t1,"t2":t2,"g":g,"es":es,"slug":slug(t1,t2,g)})

rows.sort(key=lambda r: r["es"])

# ---- calendario cronologico ----
out = []
out.append("# Calendario — Fase de Grupos · Mundial 2026\n")
out.append("> 72 partidos · 11–27 junio 2026 · 16 sedes (USA/Canada/Mexico)\n")
out.append("> **Hora ES** = hora peninsular España (CEST, UTC+2). Orden cronologico por hora real.\n")
out.append("> `(+1)` = madrugada del dia siguiente en España.\n")

cur = None
for r in rows:
    esd = r["es"].strftime("%Y-%m-%d")
    plus = " (+1)" if esd != r["date"] else ""
    daykey = r["date"]
    if daykey != cur:
        cur = daykey
        d = datetime.strptime(daykey,"%Y-%m-%d")
        out.append(f"\n## {DIAS[d.weekday()].capitalize()} {d.day} jun — Jornada {r['md']}\n")
        out.append("| Hora ES | Hora local | Grupo | Partido | Sede |")
        out.append("|---|---|:---:|---|---|")
    out.append(f"| **{r['es'].strftime('%H:%M')}**{plus} | {r['local']} (UTC{r['off']}) | {r['g']} | "
               f"{r['t1']} – {r['t2']} | {r['venue']} |")

# ---- por grupo ----
out.append("\n---\n\n# Por grupo\n")
for g in "ABCDEFGHIJKL":
    gm = [r for r in rows if r["g"]==g]
    gm.sort(key=lambda r:(r["md"],r["es"]))
    out.append(f"\n## Grupo {g}\n")
    out.append("| J | Fecha | Hora ES | Partido | Sede |")
    out.append("|:-:|---|---|---|---|")
    for r in gm:
        esd = r["es"].strftime("%d/%m")
        out.append(f"| {r['md']} | {r['date'][8:]}/{r['date'][5:7]} | {r['es'].strftime('%H:%M')} | "
                   f"{r['t1']} – {r['t2']} | {r['venue']} |")

with open("/Users/erickhein/TechWorkspace/active_projects/misc/polla_mundial_2026/partidos/calendario_fase_grupos.md","w") as f:
    f.write("\n".join(out)+"\n")

# ---- indice de seguimiento ----
idx = []
idx.append("# Indice de Seguimiento — Analisis partido a partido\n")
idx.append("> Estado por partido. Marca ✅ cuando el analisis este escrito en `partidos/analisis/`.\n")
idx.append(f"> Total: {len(rows)} partidos.\n")
idx.append("\n| # | J | Fecha (ES) | Grupo | Partido | Archivo | Estado |")
idx.append("|--:|:-:|---|:-:|---|---|:-:|")
for i,r in enumerate(sorted(rows,key=lambda x:(x["es"])),1):
    idx.append(f"| {i} | {r['md']} | {r['es'].strftime('%d/%m %H:%M')} | {r['g']} | "
               f"{r['t1']} – {r['t2']} | `{r['slug']}.md` | ⬜ |")
with open("/Users/erickhein/TechWorkspace/active_projects/misc/polla_mundial_2026/partidos/seguimiento.md","w") as f:
    f.write("\n".join(idx)+"\n")

# json para automatizacion futura
data = [{k:(v.isoformat() if hasattr(v,'isoformat') else v) for k,v in r.items()} for r in rows]
with open("/Users/erickhein/TechWorkspace/active_projects/misc/polla_mundial_2026/partidos/fixtures.json","w") as f:
    json.dump(data,f,ensure_ascii=False,indent=1)

print(f"OK: {len(rows)} partidos -> calendario_fase_grupos.md, seguimiento.md, fixtures.json")
print("Primeros 3 (orden ES):")
for r in rows[:3]:
    print(f"  {r['es'].strftime('%d/%m %H:%M')} ES | {r['g']} {r['t1']}-{r['t2']}")
