---
name: focus-group-mx (preview)
description: |
  Versión preview pública. Da un panel sintético reducido para que pruebes la mecánica.
  Para el panel completo de 19 personas + FGMX-Score validado + backtest histórico + soporte,
  ve a marketing.sistemia.mx.
---

# Focus Group MX — preview

> Antes de pagar pauta, deja que mexicanos sintéticos lean tu copy.
>
> **Esta es la versión preview.** Da un panel reducido para que entiendas cómo funciona
> el método. La versión completa con **19 personas validadas + FGMX-Score con backtest
> hit-rate 100%** vive en [**marketing.sistemia.mx**](https://marketing.sistemia.mx).

---

## Qué hace este skill

Cuando le pasas un anuncio, copy de WhatsApp, landing page o headline, este skill
activa un focus group sintético de personas mexicanas que lo leen y te dicen sin filtros:

- Qué entendieron (o no)
- Si les late o se sienten ofendidos
- Qué tan cara/barata les suena la propuesta
- Si lo comprarían y por qué sí o no
- Qué cambiarían

Hablan en su voz real (no "como diría una persona X"), con su NSE, generación, región y
contexto cultural. No es lluvia de ideas: es una simulación validada con datos públicos
de México.

---

## Cuándo activarlo

- Antes de gastar en Meta Ads, Google Ads o TikTok Ads
- Para probar un naming, slogan, tagline antes de imprimir/grabar
- Para validar copy de WhatsApp Business
- Para detectar si tu landing suena "gringa traducida" o tiene problemas culturales

---

## Cómo funciona (resumen del método)

El preview incluye **3 personas de ejemplo** del panel completo:

| Persona | NSE | Región | Cuándo usarla |
|---|---|---|---|
| **Andrea** | A/B | Monterrey | Premium, lujo, B2B alto |
| **Mariana** | C+ | Guadalajara | Mid-market, aspiracional |
| **María Fer** | C- | Edomex | Masivo barato, FMCG |

Cada persona responde con una reacción inicial corta + 3 razones + 1 sugerencia
concreta. La versión completa agrega 16 personas más y calcula **FGMX-Score** (7
dimensiones ponderadas por categoría de producto).

---

## Ejemplo de uso (preview)

> **Tú:** "Evalúa este copy para venta de seguro de auto:
> *Protege lo que más quieres por solo $399 al mes. Cobertura amplia, sin enganche.*"

> **Andrea (A/B Monterrey):**
> "¿$399 al mes? Suena raro barato. ¿Qué incluye? Yo busco confianza, no precio.
> No me convence sin marca conocida atrás."

> **Mariana (C+ Guadalajara):**
> "$399 sí me cuadra. Pero 'cobertura amplia' no me dice nada concreto. ¿Cubre robo total?
> ¿Cristales? Falta especificar."

> **María Fer (C- Edomex):**
> "$399 sigue siendo mucho para mí cada mes. Si me dieran opción semestral lo pensaría.
> Y necesito ver que sí pagan cuando choco, no nomás promesas."

> **Recomendación preview:** Especificar coberturas concretas (no "amplia"), agregar
> social proof de pagos reales, y considerar pricing semestral o anual para NSE C-.

---

## Versión completa vs preview

| | Preview (este repo) | Completo (marketing.sistemia.mx) |
|---|---|---|
| Personas | 3 ejemplos | **19 personas validadas** |
| Cobertura NSE | A/B → C- | **A/B → E (todo el espectro)** |
| Cobertura voto 2024 | — | **Sheinbaum/Xóchitl/Máynez balanced** |
| Métrica | Cualitativa | **FGMX-Score (7 dimensiones)** |
| Categorías producto | Genérico | **14 categorías con pesos calibrados** |
| Modos | Evaluación básica | **+A/B test, Competitivo, Diagnóstico, Brief→Copy** |
| Variantes mejoradas | — | **3 variantes con Buyability proyectado** |
| Canales recomendados | — | **Por NSE + persona** |
| Backtest histórico | — | **n=10 cases, hit-rate 100%, AUC 1.00** |
| Soporte + updates | Comunidad | **Direct + nuevas personas cada Q** |
| Precios PROFECO | — | **DB de 10.5M registros para validar pricing** |

---

## Instalación (preview)

```bash
# Clona el repo
git clone https://github.com/lahh1986/sistemia-skills-mx.git
cd sistemia-skills-mx

# Copia el preview a tu Claude Code skills
cp -r skills/focus-group-mx ~/.claude/skills/focus-group-mx-preview
```

Después, en Claude Code, escribe algo como:
> "Usa focus-group-mx para evaluar este copy: [tu copy aquí]"

---

## ¿Quieres la versión completa?

→ **[marketing.sistemia.mx](https://marketing.sistemia.mx)**

Suma **19 personas validadas con PSEC-MX** (ENIGH 2024 + AMAI + PROFECO + INE 2024),
**FGMX-Score con backtest hit-rate 100%**, modos avanzados, y soporte directo.

---

*Preview liberado bajo MIT. El método PSEC-MX, los dossiers completos de las 19 personas,
los pesos del FGMX-Score y la base de precios PROFECO son producto comercial de Sistemia.*
