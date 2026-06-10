#!/usr/bin/env python3
"""Reporte visual — Polla Mundial 2026 (Ruta A agéntica + Ruta B Monte Carlo).
Ejecutar:  streamlit run app.py
"""
import json, glob, os, re, urllib.request
import pandas as pd
import streamlit as st

BASE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(BASE, "partidos")
A = os.path.join(P, "analisis")
RB = os.path.join(BASE, "ruta_b")

st.set_page_config(page_title="Polla Mundial 2026", page_icon="🏆", layout="wide")

# ---------- helpers ----------
@st.cache_data
def rd(path):
    try:
        with open(path, encoding="utf-8") as f: return f.read()
    except Exception: return None

@st.cache_data
def jload(path):
    try:
        with open(path, encoding="utf-8") as f: return json.load(f)
    except Exception: return None

NAME = {"mexico":"México","south_africa":"Sudáfrica","south_korea":"Corea del Sur","czechia":"Chequia",
"canada":"Canadá","bosnia_and_herzegovina":"Bosnia","qatar":"Qatar","switzerland":"Suiza","brazil":"Brasil",
"morocco":"Marruecos","haiti":"Haití","scotland":"Escocia","united_states":"EEUU","paraguay":"Paraguay",
"australia":"Australia","turkiye":"Turquía","germany":"Alemania","curacao":"Curazao","ivory_coast":"Costa de Marfil",
"ecuador":"Ecuador","netherlands":"Países Bajos","japan":"Japón","sweden":"Suecia","tunisia":"Túnez",
"belgium":"Bélgica","egypt":"Egipto","iran":"Irán","new_zealand":"Nueva Zelanda","spain":"España",
"cape_verde":"Cabo Verde","saudi_arabia":"Arabia Saudita","uruguay":"Uruguay","france":"Francia","senegal":"Senegal",
"iraq":"Irak","norway":"Noruega","argentina":"Argentina","algeria":"Argelia","austria":"Austria","jordan":"Jordania",
"portugal":"Portugal","dr_congo":"RD Congo","uzbekistan":"Uzbekistán","colombia":"Colombia","england":"Inglaterra",
"croatia":"Croacia","ghana":"Ghana","panama":"Panamá"}
def nm(s): return NAME.get(s, s)

def bar(pairs, xlab="%", n=12):
    df = pd.DataFrame([(nm(t), v) for t, v in pairs[:n]], columns=["Equipo", xlab]).set_index("Equipo")
    st.bar_chart(df, horizontal=True)

def ko_files(sub):
    d = {}
    for f in glob.glob(os.path.join(A, sub, "m*.md")):
        m = re.match(r"m(\d+)-", os.path.basename(f))
        if m: d[int(m.group(1))] = f
    return d

MC = jload(os.path.join(RB, "mc_results_v2.json")) or {}

# ---------- sidebar ----------
st.sidebar.title("🏆 Polla Mundial 2026")
st.sidebar.caption("Ruta A (agéntica) + Ruta B (Monte Carlo 30k, calibrada por backtest)")
page = st.sidebar.radio("Secciones", ["🏆 Resumen y respuestas","🧭 Método","⚽ Simulación paso a paso",
    "📊 Monte Carlo","👤 Equipos","⚖️ Rutas A vs B"])
st.sidebar.divider()
if MC:
    st.sidebar.metric("Campeón (pick)", "España", "≈ Francia · empate 15.7%")
    st.sidebar.caption("MC: España=Francia 15.7% (volado). Pick por desempate: mercado + Ruta A.")
    st.sidebar.metric("Bota de Oro", MC["golden_boot"][0][0], f"{MC['golden_boot'][0][1]}%")

# ---------- contador de visitas (counterapi.dev, +1 por sesión) ----------
def _bump_views():
    try:
        req = urllib.request.Request(
            "https://api.counterapi.dev/v1/erickhv92/polla-mundial-2026/up",
            headers={"User-Agent": "Mozilla/5.0 (polla-app)"})
        with urllib.request.urlopen(req, timeout=4) as r:
            return json.load(r).get("count")
    except Exception:
        return None
if "views" not in st.session_state:
    st.session_state["views"] = _bump_views()
st.sidebar.divider()
_v = st.session_state.get("views")
st.sidebar.metric("👁️ Visitas", f"{_v:,}".replace(",", ".") if isinstance(_v, int) else "—")

# ====================================================== RESUMEN
if page == "🏆 Resumen y respuestas":
    st.title("🏆 Respuestas finales")
    c = st.columns(4)
    c[0].metric("Equipo ganador", "España", "≈ Francia (volado)")
    c[1].metric("Mejor jugador", "Mbappé", "alt. Yamal/Messi")
    c[2].metric("Máximo goleador", "Mbappé", f"{MC['golden_boot'][0][1]}%" if MC else "")
    c[3].metric("Goles del goleador", "7", "rango 6–9")
    st.divider()
    L, R = st.columns([3,2])
    with L:
        st.markdown(rd(os.path.join(BASE,"RESPUESTAS_FINALES.md")) or "_falta RESPUESTAS_FINALES.md_")
    with R:
        if MC:
            st.subheader("P(campeón) — top 12")
            bar([(t,v) for t,v,_ in MC["champion"]], "P(campeón) %")
            st.caption("IC95 en mc_results_v2.json. España y Francia empate técnico.")
    st.divider()
    img = os.path.join(BASE, "infografia_polla.png")
    if os.path.exists(img):
        st.subheader("📲 Infografía para compartir (WhatsApp)")
        ci = st.columns([2,3])
        ci[0].image(img, width="stretch")
        with open(img, "rb") as f:
            ci[1].download_button("⬇️ Descargar PNG", f, file_name="polla_mundial_2026.png",
                                  mime="image/png", width="stretch")
        ci[1].caption("Imagen lista para mandar. Se regenera con `python gen_infografia.py`.")

# ====================================================== METODO
elif page == "🧭 Método":
    st.title("🧭 Método — paso a paso")
    st.markdown("""
**Dos rutas independientes + validación:**

| Fase | Qué entregó |
|---|---|
| **Ruta A — agéntica** | 48 fichas de scouting + 103 análisis partido a partido (grupos→final) |
| **F1 datos** | 189 goleadores (48/48), cuotas devig, tabla FIFA terceros (495 filas), sedes/altitud, backtest 2018/22 |
| **F2 modelo gol** | Dixon-Coles + λ multiplicativa + localía/altitud + terceros oficiales |
| **F3 jugadores** | Atribución por minutos/asistencias/penaltis; MVP creator-aware |
| **F4 incertidumbre** | Blend de mercado + IC Wilson + probabilidad por ronda |
| **F6 backtest (gate)** | Validó vs 2018/22: bate baseline (RPS 0.220<0.245), acierto KO 72%; detectó sobre-confianza |
| **F7 cierre** | Destempló el tilt + recalibró la Bota (8→7) → respuestas con IC |

**Principio:** la Ruta B se construyó *a ciegas* de la A (estimadores decorrelados).
El backtest **frenó el exceso de confianza con datos**: el modelo final calca el orden del mercado.
""")
    img = os.path.join(BASE, "proceso_infografia.png")
    if os.path.exists(img):
        st.divider()
        st.subheader("🛠️ Cómo se hizo — proceso, recursos y coste")
        ci = st.columns([3,2])
        ci[0].image(img, width="stretch")
        with open(img, "rb") as f:
            ci[1].download_button("⬇️ Descargar PNG (proceso)", f, file_name="polla_proceso.png",
                                  mime="image/png", width="stretch")
        ci[1].caption("~185 subagentes · ~6M tokens · 30.000 torneos en código. Se regenera con `python gen_proceso.py`.")
    with st.expander("📄 Plan completo de ajustes (docs/plans)"):
        pl = sorted(glob.glob(os.path.join(BASE,"docs","plans","*ajustes*.md")))
        st.markdown(rd(pl[0]) if pl else "_sin plan_")

# ====================================================== SIMULACION
elif page == "⚽ Simulación paso a paso":
    st.title("⚽ Simulación — avanza de grupos a la final")
    fases = ["Fase de grupos","32avos","Octavos","Cuartos","Semifinales","Final"]
    st.session_state.setdefault("fase", fases[0])
    def _step(d):
        i = fases.index(st.session_state.fase)
        st.session_state.fase = fases[max(0, min(len(fases)-1, i+d))]
    i_now = fases.index(st.session_state.fase)
    nav = st.columns([1.3, 6, 1.3])
    nav[0].button("◀ Anterior", on_click=_step, args=(-1,), disabled=i_now==0, width="stretch")
    nav[2].button("Siguiente ▶", on_click=_step, args=(1,), disabled=i_now==len(fases)-1, width="stretch")
    fase = st.radio("Ronda", fases, key="fase", horizontal=True, label_visibility="collapsed")
    i_now = fases.index(fase)
    st.progress((i_now+1)/len(fases), text=f"Fase {i_now+1} de {len(fases)}  ·  {fase}")
    st.divider()

    if fase == "Fase de grupos":
        fx = jload(os.path.join(P,"fixtures.json")) or []
        groups = sorted(set(m["g"] for m in fx))
        gsel = st.selectbox("Grupo", groups, format_func=lambda g: f"Grupo {g}")
        st.caption("Haz clic en cada partido para ver el análisis completo (zoom).")
        for m in [x for x in fx if x["g"]==gsel]:
            slug = m.get("slug")
            title = f"J{m['md']} · {m['t1']} – {m['t2']}  ·  {m.get('es','')[:16].replace('T',' ')}  ·  {m.get('venue','')}"
            with st.expander(title):
                txt = rd(os.path.join(A, f"{slug}.md")) if slug else None
                st.markdown(txt or "_análisis no encontrado_")
        st.divider()
        st.subheader("Clasificación final proyectada")
        st.markdown(rd(os.path.join(A,"_clasificacion_final_proyectada.md")) or "")
    else:
        ROUND = {"32avos":("r32","r32_bracket.json"),"Octavos":("r16","r16_bracket.json"),
                 "Cuartos":("qf","qf_bracket.json"),"Semifinales":("sf","sf_bracket.json"),
                 "Final":("final","sf_bracket.json")}
        sub, bj = ROUND[fase]
        bracket = jload(os.path.join(P, bj)) or {}
        files = ko_files(sub)
        if fase == "Final":
            matches = []
            if bracket.get("third_place"): matches.append({**bracket["third_place"],"label":"🥉 3er puesto"})
            if bracket.get("final"): matches.append({**bracket["final"],"label":"🏆 FINAL"})
        else:
            matches = bracket.get("matches") or bracket.get("sf") or []
        st.subheader(f"{fase} — {len(matches)} partidos")
        rows = []
        for mt in matches:
            w = mt.get("winner"); via = mt.get("via","")
            rows.append({"Partido":f"{nm(mt['home'])} vs {nm(mt['away'])}","Pasa":nm(w) if w else "—","Vía":via,"Sede":mt.get("venue","")})
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
        st.caption("Zoom: abre cada cruce para el análisis de la simulación.")
        for mt in matches:
            num = mt.get("match")
            lab = mt.get("label","")
            t = f"{lab+'  ·  ' if lab else ''}{nm(mt['home'])} – {nm(mt['away'])}  →  PASA: {nm(mt.get('winner',''))} ({mt.get('via','')})"
            with st.expander(t):
                fp = files.get(num)
                st.markdown(rd(fp) if fp else "_análisis no encontrado_")

# ====================================================== MONTE CARLO
elif page == "📊 Monte Carlo":
    st.title("📊 Distribuciones Monte Carlo (Ruta B v2, 30k torneos)")
    if not MC: st.warning("Falta mc_results_v2.json"); st.stop()
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🏆 P(campeón)")
        bar([(t,v) for t,v,_ in MC["champion"]], "%")
        st.subheader("🎯 Bota de Oro — P(líder)")
        bar(MC["golden_boot"], "%", 8)
        st.metric("Goles del goleador (mediana)", MC["gb_goals_median"], f"p25 {MC['gb_goals_p25']} – p90 {MC['gb_goals_p90']}")
    with c2:
        st.subheader("🥇 Llega a semifinales")
        bar(MC["reach_sf"], "%", 8)
        st.subheader("⭐ MVP")
        bar(MC["mvp"], "%", 8)
        st.metric("Irán pasa de grupo", f"{MC['qualify_iran']}%", "nadie excluido a priori")
    st.divider()
    st.subheader("Tabla campeón con IC95")
    st.dataframe(pd.DataFrame([(nm(t),f"{v}%",f"[{lo}-{hi}]") for t,v,(lo,hi) in MC["champion"]],
                 columns=["Equipo","P(campeón)","IC95"]), width="stretch", hide_index=True)

# ====================================================== EQUIPOS
elif page == "👤 Equipos":
    st.title("👤 Fichas de scouting (48 selecciones)")
    fichas = sorted(glob.glob(os.path.join(BASE,"equipos","*.md")))
    slugs = [os.path.splitext(os.path.basename(f))[0] for f in fichas]
    sel = st.selectbox("Selección", slugs, format_func=nm)
    st.markdown(rd(os.path.join(BASE,"equipos",f"{sel}.md")) or "")

# ====================================================== RUTAS
elif page == "⚖️ Rutas A vs B":
    st.title("⚖️ Balanceo — Agéntica vs Monte Carlo")
    st.markdown(rd(os.path.join(BASE,"COMPARACION_RUTAS.md")) or "")
    with st.expander("📄 Picks definitivos (Ruta A)"):
        st.markdown(rd(os.path.join(BASE,"POLLA_PICKS_DEFINITIVOS.md")) or "")
