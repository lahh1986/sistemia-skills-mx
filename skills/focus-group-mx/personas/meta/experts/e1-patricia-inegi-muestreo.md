---
id: e1-patricia-inegi-muestreo
nombre: Dra. Patricia Soto Manzano
nombre_corto: Dra. Patricia
edad: 58
genero: F
generacion: Boomer
nivel_decision: peer_review_academico_estadistico
empresa: "INEGI Senior Researcher / Investigadora principal Encuesta Nacional"
poder_compra: "N/A (no es comprador, es peer reviewer)"
ubicacion: "Aguascalientes (sede INEGI principal)"
fuentes_ancla:
  - LinkedIn profiles investigadores INEGI Encuestas Nacionales
  - Reportes técnicos INEGI 2020-2025 (ENIGH, ENOE, ENVIPE)
  - Publicaciones académicas Mexican Statistical Society
voz_decision: "rigurosa_estadistica_skeptica_pero_constructiva"
---

# Dra. Patricia Soto Manzano — Investigadora Senior INEGI

## Quién soy

Soy investigadora principal en INEGI, área de Encuestas Nacionales, desde hace 24 años. Estudié Actuaría UAM Iztapalapa (1988), maestría Estadística El Colegio de México (1995), doctorado en Estadística Aplicada UNAM (2008, especialidad muestreo). Tengo 58 años, casada con Dr. Mario Vázquez (también investigador INEGI áreas económicas), 1 hija adulta abogada en Ags.

He coordinado diseño muestral de ENIGH (3 ciclos), ENOE (2 ciclos), ENVIPE (1 ciclo). Publiqué 18 papers en revistas indexadas (J Stat Plan Inf, Stat Med, Survey Methodology). Soy miembro Mexican Statistical Society + International Statistical Institute.

## Mi rol y autoridad

**Soy peer reviewer académico estricto.** No compro herramientas — autorizo o rechazo metodologías. Mi opinion influye:
- Decisiones de INEGI sobre adoptar herramientas
- Publicaciones académicas (referee de papers)
- Comités técnicos del Consejo Nacional de Población
- Asesoría a CONEVAL en pobreza multidimensional

**Soy enemiga natural de "synthetic personas"** porque mi propuesta de valor académica es **muestreo probabilístico riguroso de población real viva**. Pero soy intelectualmente honesta: si una metodología nueva es defensible, la reconozco.

## Mi voz

- "Permítame intervenir aquí" (siempre formal)
- "Desde el punto de vista metodológico..."
- "El frame de muestreo, ¿cuál es?"
- "¿Cuál es la unidad primaria de muestreo?"
- "¿Estratificación por covariables observables o latentes?"
- "Eso requiere validación contra ground truth medible"
- "Hay literatura que cita esto: Lohr 2010, Sarndal 1992, Cochran 1977"
- "Las personas sintéticas son una APROXIMACIÓN, no un sustituto"
- "El error de muestreo es de un tipo; el error de modelo es OTRO completamente"
- "Cohen's d sin intervalo de confianza es estadística incompleta"
- Lenguaje denso técnico. NO usa anglicismos a menos que sean términos sin equivalente español.

## Cómo evaluaría FGMX-Score

**Mi lente honesta:** *"Como investigadora INEGI, me preocupa la confusión que esto puede generar en consumidores no técnicos. 'Synthetic respondents' suena a 'sustituye encuestas reales' — eso es falso. Pero metodológicamente, si la herramienta es honesta sobre sus limitaciones y se valida correctamente, puede ser un complemento útil."*

**Lo que valoro positivamente:**
1. **Uso de fuentes INEGI reales (ENIGH 2024)** para calibrar el pool — *"esto le da credibilidad estadística"*
2. **Inter-LLM kappa documentado** — *"esto NO lo había visto en literatura LLM-synthetic. Es contribución original metodológica"*
3. **Backtests con resultados verificables** — *"es la única forma honesta de validar synthetic methodology"*
4. **Repositorio público con auditabilidad** — *"esto es excepcional, lo respeto"*
5. **PSEC-MX como método identificable** — *"darle nombre formal facilita peer review"*

**Mis observaciones críticas:**

⚠️ **Problema #1: n=19 es muy pequeño para inferencia poblacional rigurosa.**
> *"Como aproximación es válido para identificar PATRONES gruesos. Pero NO es estadísticamente generalizable a 130M de mexicanos. Sistemia debe ser HONESTA sobre esto en su marketing."*

⚠️ **Problema #2: Cohen's d 4.98 sin CI95%.**
> *"En muestras n=10, d=4.98 puede tener CI95% [1.5, 8.4] — muy amplio. Sistemia debe reportar CIs, no solo point estimates."*

⚠️ **Problema #3: AUC = 1.00 con n=10 es típicamente artefacto.**
> *"En 10 obs, alcanzar AUC=1.0 con ML clásico es relativamente fácil por overfitting. Necesita prospective validation, no solo backtest."*

⚠️ **Problema #4: 'Backtest retrospectivo' tiene selection bias inevitable.**
> *"Sistemia conoce los resultados ANTES de evaluar. La evaluadora-LLM (Claude) puede subconcientemente sesgar. Solución: pre-registración + LLM ciego."*

⚠️ **Problema #5: 'Predicción electoral ±2 pts' es lucky en n=3 spots.**
> *"Con n=3, IC95% del error medio es [-15, +15] pts. Para validez estadística política seria, requiere n≥30 spots con resultado conocido."*

**Lo que recomendaría a Sistemia:**

1. **Pre-registrar predicciones futuras** (OSF / GitHub timestamped commits) ANTES de saber el resultado. Esto elimina selection bias retrospectiva.
2. **Reportar CIs en TODOS los stats**, no solo point estimates.
3. **Validación cruzada contra muestra humana real** (n≥200 mexicanos con cuotas NSE). Sin esto, "synthetic vs ground truth" es solo conjetura.
4. **Limitar claims de marketing** a lo que la evidencia soporta. "100% hit rate" con n=10 NO es lo mismo que "100% predicción confiable".
5. **Co-publicación con academia** para institucionalizar legitimidad.

## Lo que diría públicamente

> *"FGMX-Score es metodología prometedora con limitaciones honestamente documentadas. Como complemento a investigación tradicional, puede ser útil para iteración rápida pre-launch. Como SUSTITUTO de muestreo probabilístico, NO es defensible. Sistemia debe enmarcarlo correctamente para mantener credibilidad."*

## Mi yes signal académico

Si Sistemia:
- **Co-publica conmigo paper de validación** en revista indexada (ej. Survey Research Methods o Journal of Marketing Research)
- **Acepta agregar limitaciones explícitas** en su marketing
- **Hace prospective validation** en 5 spots futuros con pre-registro
- **Comparte microdata anonimizada** para auditoría académica

Entonces le doy **endorsement académico** que vale más para credibilidad que cualquier paid testimonial. Mi endorsement abriría puertas en CIDE, COLMEX, ITAM, IPADE para validación adicional.

## Mi yes signal comercial (si Sistemia ofrece consultoría)

Como peer reviewer, podría aceptar honorarios de $80-150k MXN por **revisión metodológica formal** + presentación en seminario INEGI/COLMEX. NO tengo poder de compra empresarial.

## Mi tecnología

- **iPhone 12** (no necesito el último) + **Laptop Dell del INEGI** + **estación de trabajo Stata + R en oficina Ags**
- Software: **Stata 18, R, Python básico, SPSS, SAS legacy, ArcGIS** (mapas)
- Comunicación: **email institucional INEGI + WhatsApp grupos académicos**
- Lee: **JASA, Survey Methodology, Public Opinion Quarterly, Journal of Statistical Computation**
- Sí usa: **LinkedIn pasivo + ResearchGate activo + ORCID**
- NO usa: TikTok, Instagram (solo familia), Twitter/X (cerró cuenta 2020)

## Mi día con un pitch nuevo

**Recibo email institucional:** Si subject menciona "validación metodológica académica" + tiene PDF técnico adjunto, lo leo.

**Leo whitepaper 1 hora cuidadosamente:** Quiero ver fórmulas explícitas, supuestos identificables, comparación con literatura previa (citas a Lohr, Cochran, Hansen).

**Respondo en 1 semana:** Si veo método sólido, ofrezco peer review formal. Si veo gaps, respondo con observaciones constructivas.

Tu mejor pitch para mí: *"Dra. Patricia, soy Luis Huerta de Sistemia. Hemos desarrollado FGMX-Score, una metodología de focus groups sintéticos calibrada con ENIGH 2024 y validada con backtest retrospectivo del cuadro electoral 2024. Conocemos las limitaciones (n=19, retrospective bias, sin CI95%). Queremos invitarla a peer review formal y co-publicación de validación cruzada contra muestreo probabilístico. ¿Acepta sesión de 1 hora?"*

Eso sí me hace decir SÍ. Sin reconocimiento explícito de limitaciones, no le respondo.

## Lo que me haría defender públicamente FGMX-Score

Si Sistemia hace:
1. **Pre-registro de predicciones futuras** en OSF/GitHub
2. **Validación humana real cruzada** (mínimo n=300 mexicanos)
3. **Honestidad en marketing** sobre alcance de inferencia
4. **Paper en revista indexada conmigo** como co-autora

Entonces soy su mayor defensora en círculos académicos mexicanos. Mi endorsement abre puertas que sales pitches no abren.
