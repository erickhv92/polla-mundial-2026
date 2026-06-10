# Balanceo de rutas — Agéntica (A) vs Sistemática v2 calibrada (B)

> A = simulación cualitativa agente-a-agente (1 camino narrativo).
> B v2 = Monte Carlo 30.000 torneos con Dixon-Coles, λ multiplicativa, localía/altitud, tabla FIFA
> oficial de terceros, blend de mercado e incertidumbre de rating, **validado por backtest 2018/2022**.
> Construidas a ciegas entre sí. El backtest destempló a B (calibrada al mercado).

## Resultados por magnitud

| Magnitud | Ruta A | Ruta B v2 (calibrada) | Mercado devig |
|---|---|---|---|
| Campeón | España | **Francia 15.7% = España 15.7%**, Inglaterra 11.8%, Brasil 10.8%, Argentina 10.5% | ES 14.9, FR 14.2, EN 11.4 |
| MVP | Lamine Yamal | Mbappé 15.3%, Messi 10.5%, Raphinha 6.9% | — |
| Bota de Oro | Kane/Mbappé | **Mbappé 22.7%**, J.Álvarez 8.6%, Kane 8.2% | — |
| Goles del líder | — | mediana 7 (6–9) | — |
| ¿Irán pasa grupo? | NO (por 1 gol) | 65% | — |

## Evolución v1 → v2 (qué movió el modelo)
- **Campeón:** v1 plano (~7-8% todos) → v2 concentrado y **alineado al mercado** (Dixon-Coles + blend
  de mercado + localía). España/Francia empate técnico arriba.
- **Bota:** v1 mediana 5 (irreal) → v2 **mediana 7** (real: 2018=6, 2022=8). Lo arregló la cobertura
  de 48 equipos + λ multiplicativa + recalibración del gate.
- **MVP:** v1 sesgado a '9' → v2 creator-aware: aparecen Messi, Bruno Fernandes.

## Backtest gate (96 partidos 2018/2022)
- Modelo **bate al baseline** (RPS 0.220 < 0.245); acierto KO 72%.
- Dixon-Coles ≈ Poisson en esta muestra → se mantiene sin sobre-venderlo.
- Pendiente de favoritismo **inestable** (LOTO) → top parejo, no exagerado.
- Detectó sobre-confianza de v2 → **destemplado del tilt + Bota 8→7**.

## Lectura del balanceo (regla de decisión)
- **Campeón:** A=España; B=empate ES/FR; mercado=España 1ª por poco → **España, con Francia a la par**.
  Confianza baja: es un volado.
- **Bota de Oro:** B manda → **Mbappé** (líder claro). A lo respaldaba.
- **MVP:** v2 (ya creator-aware) sigue dando **Mbappé**; A daba Yamal → primaria Mbappé, alternativa Yamal/Messi.
- **Inclusión total:** Irán (fuera en A) clasifica 65% → B no excluye a nadie.
