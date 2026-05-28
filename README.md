# Sistemia Skills MX

> Skills de Claude Code para el mercado mexicano. Hand-crafted, ancladas en datos públicos,
> con metodología científica documentada.

[![Validation: PSEC-MX](https://img.shields.io/badge/Validation-PSEC--MX-blue)](METODOLOGIA.md)
[![Coverage: 14 personas](https://img.shields.io/badge/Personas-14-green)](skills/focus-group-mx/personas/)
[![Sources: ENIGH 2024](https://img.shields.io/badge/Sources-ENIGH%202024%2BAMAI%2BPROFECO-orange)](#fuentes-de-datos)

## Skills disponibles

### 🎯 `focus-group-mx` (flagship)

**14 personas mexicanas evalúan tu copy/ad/landing antes de gastar en ads.**

Cubrimos NSE A/B → E × género × generación × región usando microdatos ENIGH 2024
(n=91,414 hogares). Cada persona pasa validación cuantitativa documentada.

[Ver skill →](skills/focus-group-mx/)

## ¿Qué tiene de distinto?

| | Personas genéricas / Synthetic Users gringos | **Sistemia Skills MX** |
|---|---|---|
| Anclaje en datos | Marginal o ausente | **ENIGH 2024 microdatos + AMAI NSE 2024 + PROFECO + INEGI ENVIPE/ENCIG/etc.** |
| Validación científica | Generalmente ausente | **Método PSEC-MX documentado** ([METODOLOGIA.md](METODOLOGIA.md)) |
| Cultura mexicana | Translation de gringo | **Hand-crafted con voz, modismos, política, entretenimiento auténticos MX** |
| Backtest electoral | No aplica | **Predicción 2024 vs resultado real validado** |
| Cobertura NSE | Plana | **A/B → E cubriendo del percentil 99.5 al 5** |
| Reproducibilidad | Caja negra | **Validaciones individuales públicas** ([validation/](skills/focus-group-mx/validation/)) |

## Casos de uso

- **Validar copy de ads** antes de gastar en Meta/Google/TikTok
- **Probar slogans, taglines, naming** para mercado MX
- **Detectar tono no-mexicano** en copy traducido del inglés
- **Auditar landing pages** desde múltiples NSE
- **Evaluar spots de TV/radio** desde voto/edad/región específicos
- **Estudios de marca** sin contratar focus group real

## Quick start

### Instalación

Este repo es una colección de skills. Para usar en Claude Code:

1. Clona el repo: `git clone https://github.com/lahh1986/sistemia-skills-mx.git`
2. Mueve el skill que quieras a tu directorio de skills de Claude Code
3. Activa la skill en tu config

### Uso básico

Una vez activado el skill `focus-group-mx`:

```
"Evalúa este copy: 'Compra ahora tu seguro de auto a $299/mes con cobertura amplia'"
```

El skill automáticamente:

1. **Identifica el target** del producto (NSE, edad, género, región)
2. **Selecciona** las personas relevantes del pool (modelo C híbrido)
3. **Invoca a cada persona en primera persona** ("Eres María Fer...")
4. **Cada una evalúa** desde su perspectiva real
5. **Sintetiza** con tabla de decisiones + score + 3 variantes mejoradas

## Las 14 personas

| # | Persona | NSE | Región | Voto 2024 |
|---|---|---|---|---|
| 01 | Andrea Garza | A/B | San Pedro NL | Xóchitl |
| 02 | Rodrigo Mendoza | A/B | Lomas CDMX | Xóchitl |
| 03 | Mariana Vázquez | C+ | Zapopan JAL | Sheinbaum |
| 04 | Daniel Hernández | C+ | Querétaro | Xóchitl |
| 05 | Karla Esparza | C | Aguascalientes | Sheinbaum |
| 06 | Jorge Pacheco | C | Coyoacán CDMX | Sheinbaum |
| 07 | María Fernanda Ramírez | C- | Ecatepec Edomex | Sheinbaum |
| 08 | Hugo Cárdenas | C- | Tijuana BC | Sheinbaum |
| 09 | Lupita Reyes | D+ | Iztapalapa CDMX | Sheinbaum |
| 10 | Ramón Solís | D+ | Tlaquepaque JAL | Sheinbaum |
| 11 | Doña Rosa Pérez | D | Apatzingán MICH | Sheinbaum |
| 12 | Brayan Núñez | D | Chimalhuacán Edomex | Sheinbaum |
| 13 | Sofía Bautista | E | Chilpancingo GRO | Sheinbaum |
| 14 | Don Tomás López | E | Chiapas tsotsil rural | Sheinbaum |

[Detalles de cada persona →](skills/focus-group-mx/personas/)

## Metodología: PSEC-MX

**Personas Sintéticas Empíricamente Calibradas para México.** 6 pasos:

1. **Estratificación a priori** — celdas NSE × género × generación × región
2. **Centroide empírico** — match con mediana del universo similar en ENIGH 2024
3. **Triangulación MTMM** — cada característica validada con 3+ fuentes
4. **Backtest predictivo** — predicción voto 2024 vs resultado real
5. **Reliability tests** — inter-LLM kappa + test-retest (pendiente v1.3)
6. **Face validity** — 5 expertos mexicanos (pendiente v1.4)

[Metodología completa →](METODOLOGIA.md)

## Fuentes de datos

Todas las personas están ancladas en fuentes públicas y gratuitas:

- **INEGI ENIGH 2024** — microdatos (n=91,414 hogares) ingreso/gasto
- **AMAI NSE 2024** — metodología niveles socioeconómicos
- **PROFECO QQP** — precios reales por producto/cadena/municipio (10.5M registros)
- **INEGI ENDUTIH 2024** — hábitos digitales
- **INEGI ENIF 2024** — inclusión financiera
- **INEGI ENVIPE 2024** — seguridad y victimización
- **INEGI ENCIG 2023** — calidad gubernamental
- **BBVA Research** — consumo regional + remesas
- **Latinobarómetro 2024** — opinión pública LATAM
- **LAPOP/AmericasBarometer** — política comparada

## Estado actual

- ✅ **Capa 1 v1.1** — 14 personas hand-crafted validadas PSEC-MX (presente)
- ⏳ **v1.2** — 5 personas adicionales para corregir gaps (Q3 2026)
- ⏳ **v1.3** — Reliability tests (inter-LLM kappa) (Q3 2026)
- ⏳ **v1.4** — Face validity con expertos pagados (Q4 2026)
- 🔒 **Capa 2 política** — Fork privado para campañas 2027 (no público)

## Licencia

Apache 2.0 — ver [LICENSE](LICENSE).

Los dossiers y metodología son libres para uso académico, periodístico, comercial.
La atribución a "Sistemia Skills MX" es apreciada pero no requerida.

## Contribuir

Si encuentras inconsistencias en los datos o quieres proponer una persona adicional,
abre un issue. Las contribuciones siguen el método PSEC-MX (con anclaje empírico).

## Sobre

Construido por [Luis "Chombi" Huerta](https://github.com/lahh1986) como parte del
ecosistema **Sistemia.mx** — plataforma de herramientas para el mercado mexicano.

- Sistemia Estudio: estudio.sistemia.mx
- Trust: trust.sistemia.mx
- Podcast Agentes Sucios: dev tools en español

## Roadmap público

Próximos skills planeados:

- `locale-mx` — Validador de copy mexicano vs gringo traducido
- `chombi-message` — Mensajes en español MX familiar para WhatsApp
- `deploy-sistemia` — Deploy a Cloudflare Pages con flujo estándar

Si te interesa colaborar o contratar un skill custom para tu marca/agencia,
contacto en sistemia.mx.
