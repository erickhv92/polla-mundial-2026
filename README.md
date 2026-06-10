# 🏆 Polla Mundial 2026 — Pronóstico con agentes + Monte Carlo

Dashboard interactivo de predicción del Mundial 2026, construido combinando
**trabajo agéntico** (análisis cualitativo partido a partido) y un **motor Monte Carlo**
en código (Dixon-Coles, 30.000 torneos), **validado con backtest 2018/2022**.

## Las 4 respuestas
- **Campeón:** España (empate técnico con Francia, 15.7%)
- **Mejor jugador:** Kylian Mbappé
- **Máximo goleador:** Kylian Mbappé
- **Goles del goleador:** 7 (rango 6–9)

## Cómo se hizo
- **Ruta A (agéntica):** 48 fichas de scouting + 103 análisis partido a partido (grupos → final).
- **Ruta B (sistemática):** ratings decorrelados (3 lentes) → motor Monte Carlo con Dixon-Coles,
  λ multiplicativa, localía/altitud, tabla FIFA oficial de terceros, blend de mercado e
  incertidumbre de rating.
- **Backtest gate (2018/2022):** validó el modelo (RPS 0.220 < baseline) y destempló la sobre-confianza.

## Ejecutar local
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

## Deploy (Streamlit Community Cloud)
1. Repo en GitHub.
2. share.streamlit.io → conectar repo → `app.py`.
3. Deploy → URL pública.

## Estructura
- `app.py` — dashboard Streamlit.
- `equipos/` — 48 fichas de scouting.
- `partidos/` — calendario, brackets, 103 análisis partido a partido.
- `ruta_b/` — motor Monte Carlo, datos, backtest, resultados.
- `RESPUESTAS_FINALES.md`, `COMPARACION_RUTAS.md` — síntesis.
- `gen_infografia.py`, `gen_proceso.py` — generadores de infografías.

> Pronóstico basado en simulación; no son resultados reales.
