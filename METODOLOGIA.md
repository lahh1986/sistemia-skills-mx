# Metodología PSEC-MX

> **Personas Sintéticas Empíricamente Calibradas para México**
>
> Método de 6 pasos para construir y validar personas mexicanas para evaluación
> de copy publicitario, narrativas de marca, y mensajes políticos.

---

## Por qué PSEC-MX

Los "synthetic users" / "AI personas" gringos típicamente son:

- **No anclados:** descripciones genéricas sin verificación empírica
- **Translation de gringo:** Soccer mom de Iowa traducida a "ama de casa de Toluca"
- **Caja negra:** sin metodología pública
- **Sin validación predictiva:** no se prueba contra resultados reales

Para el mercado mexicano necesitamos personas con:

- **Anclas estadísticas verificables** (ENIGH, AMAI, PROFECO, etc.)
- **Cultura auténtica MX** (vocabulario, modismos, marcas, voto)
- **Validación documentada y reproducible**
- **Backtest contra eventos conocidos** (resultados electorales 2024)

PSEC-MX es la respuesta.

---

## Los 6 pasos

### Paso 1 — Estratificación a priori

Definir el marco muestral conceptual y las celdas a poblar.

**Variables del estrato:**
- NSE AMAI: A/B, C+, C, C-, D+, D, E (7 niveles)
- Género: F/M
- Generación: Gen Z (18-27), Millennial (28-43), Gen X (44-59), Boomer (60+)
- Región: Norte, Centro, Bajío, Sur
- Tipo de localidad: urbana premium / clase media / periferia / ciudad media / rural

**Justificación:** muestreo estratificado multietápico es estándar en estadística
demográfica oficial (INEGI usa el mismo método para ENIGH).

**Output:** matriz de celdas teóricas (224 posibles si cruzamos las 4 variables
principales). Las 14 personas v1 cubren 14 celdas representativas.

### Paso 2 — Centroide empírico

Cada persona debe coincidir con el **centroide del universo similar real**.

**Procedimiento:**
1. Filtrar ENIGH 2024 microdatos al universo de la persona
   (entidad + tam_loc + edad_jefe + educa_jefe + tot_integ)
2. Calcular mediana de ingreso, gasto, composición del hogar
3. La persona debe matchear ≥85% con la mediana del universo similar

**Ejemplo — María Fernanda (C- Ecatepec):**
- Universo similar Ecatepec: 203 hogares en muestra
- Ingreso mediana del universo: $19,535/mes
- María Fer declarado: $18,500/mes
- **Match: 95%** ✓

Si una persona NO matchea ≥85%, se documenta la divergencia explícitamente
(ej: Doña Rosa está en bottom 11% nacional, está sub-mediana de Apatzingán
pero coherente con realidad económica de Tierra Caliente).

### Paso 3 — Triangulación MTMM (Multi-Trait Multi-Method)

Cada característica de la persona debe estar respaldada por **3+ fuentes independientes**.

**Ejemplo — NSE C- de María Fer triangulado:**

| Fuente 1 | Fuente 2 | Fuente 3 |
|---|---|---|
| ENIGH 2024 est_socio=2 (Medio bajo) | AMAI NSE 2024 regla C- por equipamiento | ENSAFI 2023 estrés financiero alto (37%) |

Score MTMM = dimensiones con 3+ fuentes / dimensiones totales evaluadas.

**Target:** ≥5/7 dimensiones (NSE, ingreso, hábitos digitales, financiero,
educación, hogar, política).

### Paso 4 — Backtest predictivo

¿Si esta persona hubiera votado en 2024, qué hubiera votado? ¿Coincide con
el resultado real de su estrato?

**Procedimiento:**
1. Persona declara voto 2024 (Sheinbaum / Xóchitl / Máynez / abstención)
2. Comparar contra resultado oficial INE de su sección/municipio
3. Comparar contra tracking de Mitofsky/EF/Demoscopia para su estrato

**Ejemplo — María Fer voto Sheinbaum:**
- Edomex 2024 resultado: Sheinbaum 60.65%
- Mujeres C- Edomex (estimado Mitofsky): Sheinbaum ~65%
- María Fer voto declarado: Sheinbaum ✓ coincide con mayoría

**Si la persona NO predice correctamente, recalibrar o documentar como minoría
disidente (ej: Karla Aguascalientes votó Sheinbaum siendo de bastión PAN —
representa 33% de mujeres C disidentes, válido pero atípico).**

### Paso 5 — Reliability tests (v1.3 — pendiente)

Tres pruebas de consistencia:

**5a. Test-retest:**
Mismo prompt × 5 veces sobre la misma persona → variance <15% en métricas clave.

**5b. Inter-LLM kappa:**
Mismo dossier evaluado en Claude + GPT + Gemini + Grok → Cohen's κ > 0.7.

**5c. Cross-persona consistency:**
Misma persona evaluando 10 ads similares → respuestas correlacionadas.

### Paso 6 — Face validity (v1.4 — pendiente)

Validación cualitativa con expertos.

**Procedimiento:**
1. 5 expertos mexicanos (sociólogo COLMEX, antropólogo consumidor Lexia,
   consultor político, encuestador profesional, copywriter MX senior)
2. Cada uno evalúa los 14 dossiers en escala 1-7
   ("¿suena auténticamente mexicana?")
3. **Target:** media ≥5.5 por dossier

---

## Comparación con métodos existentes

| Método | Estratificación | Centroide empírico | MTMM | Backtest | Reliability | Face validity | Reproducible |
|---|---|---|---|---|---|---|---|
| Justin Brooke (synthetic focus group) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Synthetic Users startups gringas | ⚠️ Marginal | ⚠️ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Argyle et al. 2022 (Stanford) | ✅ | ✅ | ⚠️ | ✅ (ANES US) | ✅ | ❌ | ✅ |
| Aher et al. 2023 (multi-human) | ✅ | ✅ | ⚠️ | ⚠️ | ✅ | ❌ | ✅ |
| **PSEC-MX (este método)** | ✅ | ✅ | ✅ | ✅ ENIGH+INE | ⏳ v1.3 | ⏳ v1.4 | ✅ |

---

## Fuentes de datos utilizadas

Todas públicas, gratuitas, citables:

### Tier 1 — Estructural
- **INEGI ENIGH 2024** microdatos (n=91,414 hogares)
- **AMAI NSE 2024** metodología
- **INEGI Censo 2020** + Inventario Viviendas
- **CONAPO** Proyecciones población 1950-2070

### Tier 2 — Comportamiento
- **INEGI ENDUTIH 2024** hábitos digitales
- **INEGI ENIF 2024** inclusión financiera
- **INEGI ENSAFI 2023** salud financiera
- **INSP ENSANUT** salud/nutrición
- **INEGI ENADID 2023** demografía
- **INEGI ENUT 2024** uso del tiempo

### Tier 3 — Consumo
- **PROFECO QQP 2024-2026** precios reales (10.5M registros)
- **AMVO** Estudio Venta Online 2024-2025
- **AIMX** Hábitos Internet 2024
- **DataReportal Mexico 2025**

### Tier 4 — Regional
- **BBVA Research** Situación Sectorial Regional
- **Banxico** Reportes Economías Regionales

### Tier 5 — Político
- **INE** PREP y Cómputos 2024
- **INEGI ENVIPE 2024** seguridad
- **INEGI ENCIG 2023** calidad gubernamental
- **INEGI ENCUCI 2020** cultura cívica
- **Latinobarómetro 2024**
- **LAPOP/AmericasBarometer 2023**
- **Mitofsky / El Financiero** tracking presidencial
- **CELAG** Radiografía Votante MORENA 2024
- **Data Cívica** Votar entre Balas
- **Integralia + Laboratorio Electoral** violencia política

---

## Limitaciones del método (honestidad académica)

1. **No es encuesta real.** PSEC-MX produce simulación, no medición primaria.
   Para decisiones de campaña de >$5M MXN, validar con encuesta presencial.

2. **N=14 personas para v1.** Para nichos específicos puede no cubrirse —
   el skill avisa al usuario si el target es estrecho.

3. **Sesgo de creador.** Yo (Luis Huerta) construí las personas, así que mi
   sesgo intelectual está presente. Mitigado con anclas empíricas pero no
   eliminado.

4. **Datos ENIGH 2024 son del último año disponible.** Para 2026-2027
   habrá ENIGH 2026 que requerirá recalibrar.

5. **Reliability tests pendientes (v1.3).** Actualmente confianza en outputs
   se basa en validación cuantitativa (pasos 1-4), no en consistencia
   inter-LLM medida formalmente.

6. **Face validity pendiente (v1.4).** Los dossiers no han sido validados por
   panel de expertos mexicanos remunerados.

---

## Cómo citar

```bibtex
@misc{huerta_psec_mx_2026,
  author = {Huerta, Luis A.},
  title = {{PSEC-MX: Personas Sintéticas Empíricamente Calibradas para México}},
  year = {2026},
  url = {https://github.com/lahh1986/sistemia-skills-mx},
  note = {v1.1}
}
```

---

## Roadmap metodológico

- **v1.1** (presente): Pasos 1-4 implementados. 14 personas validadas.
- **v1.2** (Q3 2026): Personas adicionales para corregir gaps (Máynez, A/B
  patrimonial, C medio CDMX, etc.).
- **v1.3** (Q3 2026): Reliability tests (paso 5).
- **v1.4** (Q4 2026): Face validity con expertos (paso 6).
- **v2.0** (2027): Capa 2 con personas regionales para gubernaturas 2027
  (fork privado, no público).
- **v3.0** (2028+): Recalibrar con ENIGH 2026, expandir pool a 28-40 personas.

---

## Contacto / Colaboración

Para contribuir personas siguiendo PSEC-MX, abrir Pull Request con:

1. Dossier completo siguiendo [PLANTILLA_DOSSIER.md](skills/focus-group-mx/PLANTILLA_DOSSIER.md)
2. Archivo de validación en `skills/focus-group-mx/validation/`
3. Anclas explícitas en frontmatter (`fuentes_ancla` + `validacion_psec_mx`)

Mantenedor: [@lahh1986](https://github.com/lahh1986)
