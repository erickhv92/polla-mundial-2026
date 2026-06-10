# Proceso de Análisis Partido a Partido — Polla Mundial 2026

Proceso sistemático y repetible para evaluar cada uno de los 72 partidos de fase de grupos
y convertir el análisis en un **pronóstico accionable** para la polla.

## Inputs (ya disponibles)
- `equipos/<pais>.md` — scouting de cada selección (plantel, estrellas, forma, fortalezas/debilidades, bajas).
- `partidos/calendario_fase_grupos.md` — calendario cronológico (hora España) + por grupo.
- `partidos/fixtures.json` — datos estructurados de los 72 partidos.
- `partidos/seguimiento.md` — índice de estado (⬜ pendiente / ✅ hecho).

## Flujo por partido
1. Leer fichas de los **dos equipos** (`equipos/`) → forma, bajas, estrellas.
2. Buscar info **fresca del enfrentamiento** (web): últimas alineaciones, lesiones de última hora,
   historial directo (H2H), contexto (¿se juegan clasificar?), cuotas 1X2 del partido.
3. Rellenar la **plantilla** (abajo) → escribir en `partidos/analisis/<slug>.md`.
4. Emitir **pronóstico**: resultado 1X2, marcador probable, goleador, over/under 2.5, confianza (1–5).
5. Marcar ✅ en `seguimiento.md`.

## Orden recomendado
- Por **jornada** (J1 completa → J2 → J3): en J2/J3 ya hay resultados reales que actualizan el contexto.
- Dentro de la jornada, **orden cronológico** (como en el calendario).
- Prioriza grupos con tus equipos de la polla o los de favoritos disputados.

## Criterios de evaluación (peso sugerido)
| Factor | Qué mirar | Peso |
|---|---|:--:|
| Calidad plantel | FIFA rank, estrellas, profundidad | 25% |
| Forma reciente | últimos ~5 partidos, racha | 20% |
| Bajas/lesiones | ausencias clave (def/medio/del) | 15% |
| Estilo/táctica | choque de sistemas, quién domina balón | 15% |
| Contexto del partido | qué se juega cada uno (J3 sobre todo) | 10% |
| H2H + historial Mundial | precedentes directos | 8% |
| Factores externos | sede/altitud/calor, viaje, descanso | 7% |

## Plantilla de análisis (copiar a `analisis/<slug>.md`)

```markdown
# [Grupo X · Jornada N] Equipo1 – Equipo2
**Fecha:** DD/MM HH:MM (ES) · **Sede:** Estadio, Ciudad · **Cuotas 1X2:** x / x / x

## Contexto
- Qué se juega cada equipo (clasificación, primero de grupo, etc.)
- Estado tras jornadas previas (solo J2/J3)

## Equipo1
- Forma reciente: 
- XI probable / sistema: 
- Bajas/dudas: 
- Clave: 

## Equipo2
- Forma reciente: 
- XI probable / sistema: 
- Bajas/dudas: 
- Clave: 

## Duelo táctico
- Dónde se decide (mediocampo, bandas, balón parado, transiciones)
- Jugador-llave del partido

## H2H
- Precedentes directos relevantes

## Pronóstico
- **1X2:** [1 / X / 2] — confianza ☆☆☆☆☆ (1–5)
- **Marcador probable:** x–x
- **Goleador probable:** 
- **Over/Under 2.5:** 
- **Apuesta de valor (polla):** 
```

## Salida agregada
Tras cada jornada, actualizar en `analisis/`:
- `_jornada1_resumen.md`, `_jornada2_resumen.md`, `_jornada3_resumen.md` — pronósticos consolidados + aciertos.
- Al cerrar J3 → proyección de **clasificados** (1º/2º + mejores terceros) que alimenta el bracket y los picks de la polla.

## Cómo ejecutarlo
- **Manual / guiado:** "analiza el partido N" o "analiza la jornada 1 del grupo H".
- **Por lote (workflow):** lanzar un workflow que recorra `fixtures.json`, una etapa de investigación + una de pronóstico por partido, escribiendo cada `analisis/<slug>.md`. Pídelo con la palabra "workflow".
