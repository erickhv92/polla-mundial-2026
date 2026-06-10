# 🏆 Respuestas finales v2 — Polla Mundial 2026 (modelo calibrado)

> Síntesis de dos rutas independientes + calibración por backtest:
> **A** = simulación agéntica cualitativa (1 camino). **B v2** = Monte Carlo 30.000 torneos
> con Dixon-Coles, λ multiplicativa, localía/altitud, tabla FIFA oficial de terceros, blend de
> mercado e **incertidumbre de rating**, **validado contra Mundiales 2018/2022** (backtest gate).
> El backtest destempló el exceso de confianza: el modelo ahora **calca el orden del mercado**.

---

## 1️⃣ Equipo ganador → **ESPAÑA** 🇪🇸 (empate técnico con Francia 🇫🇷)

- **Ruta A:** España campeón.
- **Ruta B v2:** **Francia 15.7% = España 15.7%** (IC95 idénticos [15.3-16.1]), luego Inglaterra
  11.8%, Brasil 10.8%, Argentina 10.5%. Calibrado al mercado (devig: ES 14.9, FR 14.2).
- **Veredicto:** **España** por desempate (la elige Ruta A y el mercado la pone 1ª por un pelo),
  pero es un **volado con Francia**. Confianza **baja-media** — campo abierto.
- *Valor polla:* si la liga premia diferenciarse, **Francia** paga casi lo mismo con igual probabilidad.

## 2️⃣ Mejor jugador (MVP) → **KYLIAN MBAPPÉ** 🇫🇷 (alt. Yamal/Messi)

- **Ruta A:** Lamine Yamal (figura del campeón España).
- **Ruta B v2 (creator-aware):** Mbappé 15.3%, **Messi 10.5%**, Raphinha 6.9%, Kane, Bruno Fernandes.
- **Veredicto:** **Mbappé** — lo respaldan modelo + ser máximo goleador + Francia co-favorita.
  Cambió respecto a v1: el MVP ahora valora creadores y aún así Mbappé lidera.
- *Alternativas fuertes:* **Lamine Yamal** (si gana España), **Messi** (despedida).

## 3️⃣ Jugador con más goles (Bota de Oro) → **KYLIAN MBAPPÉ** 🇫🇷

- **Ruta B v2:** Mbappé **22.7%**, muy por delante (Julián Álvarez 8.6%, Kane 8.2%, Oyarzabal 6.4%).
- **Veredicto:** **Mbappé**. Confianza **media-alta** (líder claro, casi 3× el 2º).
- *Alternativas:* Julián Álvarez, Harry Kane.

## 4️⃣ ¿Cuántos goles tendrá el goleador? → **7 goles** (rango 6–9)

- **Ruta B v2 (calibrada):** mediana **7**, p25 **6**, p90 **9**.
- **Validación backtest:** Botas reales recientes 2018=6, 2022=8 → mediana 7 es coherente. El
  formato 2026 (campeón juega 8 partidos) sube ligeramente el techo.
- **Veredicto:** **7 goles** (apuesta segura 6–8).

---

## Resumen para la polla

| Pregunta | Respuesta | Confianza | Alternativa real |
|---|---|:--:|---|
| **Equipo ganador** | España | Baja-media (volado con Francia) | **Francia** (≈igual prob.) |
| **Mejor jugador** | Kylian Mbappé | Media | Lamine Yamal / Messi |
| **Máximo goleador** | Kylian Mbappé | Media-alta | Julián Álvarez |
| **Goles del goleador** | 7 (6–9) | Media | — |

---

## Cómo se llegó aquí (trazabilidad del modelo)
- **Datos:** 48 fichas + 189 goleadores (48/48 equipos) + cuotas devig + tabla FIFA terceros + sedes/altitud.
- **Modelo B v2:** Dixon-Coles (ρ=−0.13), λ multiplicativa, localía/altitud anfitriones, blend de
  mercado 30%, incertidumbre de rating (IC Wilson), penales 0.40–0.60, atribución por
  minutos/asistencias/penaltis, MVP creator-aware.
- **Backtest gate (2018/2022, 96 partidos):** el modelo **bate al baseline** (RPS 0.220 vs 0.245)
  y acierta el 72% de avances de eliminatoria. Detectó **sobre-confianza** → se destempló el tilt
  y se recalibró la Bota (mediana 8→7). Dixon-Coles ≈ Poisson en esta muestra (se mantiene, sin
  sobre-vender). Pendiente de favoritismo **inestable** en LOTO → por eso el top sale parejo y
  alineado al mercado, no exagerado.
- **Honestidad:** cada respuesta lleva IC/confianza. El top del torneo es un volado; el modelo no
  finge certeza que los datos no dan.

*Detalle: `ruta_b/mc_results_v2.json`, `ruta_b/backtest_calibration.py` (salida en gate),
`COMPARACION_RUTAS.md`, plan en `docs/plans/`.*
