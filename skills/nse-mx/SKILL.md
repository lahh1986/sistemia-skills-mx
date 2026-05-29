---
name: nse-mx
description: |
  Usar cuando el usuario quiera CLASIFICAR un hogar, cliente, lead o persona
  mexicana en NSE AMAI (A/B, C+, C, C-, D+, D, E) usando la regla AMAI 2024
  vigente (6 variables: educación jefe del hogar, baños completos, autos,
  internet, ocupados, dormitorios). Devuelve el nivel + percentil nacional
  + perfil de gasto + brand affinity esperado + comparativos por estado.
  También útil para inferir NSE desde colonia/CP/datos parciales y para
  segmentar bases de datos.

  Triggers: "qué NSE es", "clasifica este hogar", "AMAI", "nivel socioeconómico",
  "segmenta mi base", "qué clase social es", "es A/B o C", "C+ vs C-",
  "Niveles AMAI", "regla AMAI 2024", "perfil socioeconómico", "qué porcentaje
  de mexicanos son", "distribución por estado", "rural vs urbano NSE".
---

# nse-mx — Clasificador NSE AMAI 2024 para México

> Implementación abierta de la **Regla NSE AMAI 2024** (Comité Técnico AMAI,
> octubre 2023), basada en los coeficientes de regresión publicados en la nota
> metodológica oficial y calibrada contra la distribución nacional ENIGH 2022.

## Cuándo activarte

- El usuario te pasa info de un hogar/cliente y pregunta el NSE
- El usuario quiere segmentar una base de leads/clientes por NSE
- El usuario quiere saber qué % de México es A/B, C, D, etc.
- El usuario quiere distribución NSE por estado o tamaño de localidad
- El usuario menciona "AMAI", "regla AMAI", "NSE 8x7", "NSE 6", "Niveles AMAI"
- El usuario quiere inferir NSE desde una colonia, CP o municipio (no exacto, aproximado)
- El usuario está construyendo personas y necesita anclarlas en un NSE

**NO actives si:** el usuario pregunta por NSE de OTRO país (Brasil ABEP, Argentina, Chile ESOMAR). AMAI es específica de México.

## Las 6 variables AMAI 2024

| # | Variable | Categorías |
|---|---|---|
| 1 | **Educación del jefe del hogar** | Sin instrucción · Primaria incompleta · Primaria completa · Secundaria incompleta · Secundaria completa · Preparatoria incompleta · Preparatoria completa · Profesional incompleta · Profesional completa · Posgrado |
| 2 | **Número de baños completos** (con regadera + WC) | 0 · 1 · 2 · 3+ |
| 3 | **Número de autos** propios (excluye motos, taxis, uber) | 0 · 1 · 2 · 3+ |
| 4 | **Internet en el hogar** | Sí · No |
| 5 | **Personas que aportan ingresos** | 0 · 1 · 2 · 3+ |
| 6 | **Número de dormitorios** (cuartos para dormir) | 0 · 1 · 2 · 3+ |

## Algoritmo de clasificación

### Paso 1: Asigna puntos por cada variable

Puntos derivados de los coeficientes de regresión publicados en la nota
metodológica AMAI 2024 (Comité Técnico, octubre 2023, Figura 4), escalados a
una escala 0-300 con suma máxima ~300.

**Tabla de puntos** (ver `data/puntos_amai_2024.json` para versión machine-readable):

```
Educación jefe del hogar
  Sin instrucción / preescolar       0
  Primaria incompleta                5
  Primaria completa                 12
  Secundaria incompleta             17
  Secundaria completa               18
  Preparatoria incompleta           21
  Preparatoria completa             26
  Profesional incompleta            37
  Profesional completa              52
  Posgrado                          79

Baños completos
  0                                  0
  1                                 21
  2                                 43
  3+                                64

Autos propios
  0                                  0
  1                                 19
  2                                 38
  3+                                57

Internet en hogar
  No                                 0
  Sí                                28

Ocupados (personas que aportan ingreso)
  0                                  0
  1                                 16
  2                                 33
  3+                                49

Dormitorios
  0                                  0
  1                                  6
  2                                 12
  3                                 17
  4+                                23
```

### Paso 2: Suma puntos → Nivel NSE

| Puntos | Nivel | % Hogares MX | Nombre coloquial |
|---|---|---|---|
| 221+ | **A/B** | 7.3% | "ricos" — patrimonial / alto profesionista |
| 181-220 | **C+** | 12.0% | "clase media alta" |
| 156-180 | **C** | 15.3% | "clase media típica" |
| 131-155 | **C-** | 16.4% | "clase media baja emergente" |
| 101-130 | **D+** | 14.9% | "clase media en construcción / clase trabajadora alta" |
| 61-100 | **D** | 25.4% | "clase baja" (el bloque más grande de México) |
| 0-60 | **E** | 8.7% | "pobreza" |

**Fuente:** Distribución nacional ENIGH 2022 publicada en Figura 1 de la nota metodológica AMAI 2024.

### Paso 3: Cross-check con estado y tamaño de localidad

Si tienes el estado, ajusta tu lectura. Distribuciones de referencia (ENIGH 2022):

**Top 5 estados con más A/B:**
Aguascalientes (13%) · Nuevo León (12%) · BCS (12%) · Querétaro (11%) · CDMX (11%)

**Bottom 5 estados con menos A/B:**
Oaxaca (3%) · Veracruz (3%) · Chiapas (3%) · Guerrero (4%) · Puebla (5%)

**Por tamaño de localidad:**
| Tamaño | E | D | D+ | C- | C | C+ | A/B |
|---|---|---|---|---|---|---|---|
| <2,500 hab (rural) | 17.7% | 39.0% | 15.0% | 12.4% | 9.0% | 5.5% | 1.4% |
| 2,500-15K | 12.3% | 30.7% | 16.1% | 15.2% | 13.2% | 8.5% | 4.0% |
| 15K-100K | 6.8% | 24.6% | 15.3% | 17.6% | 16.6% | 12.0% | 7.0% |
| 100K+ (urbano) | 4.1% | 18.0% | 14.5% | 18.2% | 18.4% | 16.2% | 10.7% |

Si el usuario dice "soy de Polanco, CDMX" la prior bayesiana sube a A/B ~30-50%. Si dice "soy de Apatzingán Michoacán" la prior va más hacia D/E.

### Paso 4: Output al usuario

```markdown
## Clasificación NSE AMAI 2024

**Nivel: {{NSE}}**
**Puntos: {{X}} de 300**
**Percentil nacional: ~{{P}}** (top {{100-P}}% de México)

### Desglose
| Variable | Respuesta | Puntos |
| Educación jefe | Profesional completa | 52 |
| Baños | 2 | 43 |
| Autos | 1 | 19 |
| Internet | Sí | 28 |
| Ocupados | 2 | 33 |
| Dormitorios | 3 | 17 |
| **Total** | | **192** |

### Perfil de gasto esperado (ENIGH 2022 × NSE)
- {{Alimentos %}} · {{Transporte %}} · {{Vivienda %}} · {{Educación %}}

### Lectura accionable
{{1-2 líneas sobre qué producto/canal/copy le entra}}

### Caveats
- Implementación abierta basada en la metodología AMAI 2024 pública (no es el
  scoring oficial cerrado de AMAI). Los puntos están derivados de los coeficientes
  de regresión publicados en la nota metodológica de octubre 2023.
- Diferencia esperada vs. AMAI oficial: ±1 nivel en casos frontera.
```

## Perfiles por NSE (atajos para personas, copy, marketing)

### A/B (7.3%)
- Patrimonial heredado o profesionista top. Vacaciones internacionales, escuela privada bilingüe, autos premium (Audi, BMW, Mercedes), shop en Liverpool/Palacio/El Palacio de Hierro, City Market, Costco premium. Lee Reforma o El Financiero, ve Netflix sin pestañear en cargo. Gasta ~26% en alimentos, ~24% en transporte, ~25% en educación + servicios. **Copy:** sofisticado, en inglés ok, valor por calidad no por precio.
- Hubs: Polanco, Lomas, Bosques (CDMX) · San Pedro Garza García (NL) · Zapopan norte · Valle Real (JAL) · Cumbres (Querétaro)

### C+ (12.0%)
- Clase media alta con auto propio, internet de fibra, hijos en escuela privada (cuota media), vacaciones nacionales + 1 internacional cada 2 años. Compra Liverpool, Sears, Soriana Híper, La Comer. Mantiene Netflix + Disney+ + Spotify. **Copy:** aspiracional pero accesible, "tu mereces", calidad-precio.

### C (15.3%)
- Clase media típica de México. Casa propia (vía Infonavit), uno o dos autos, internet, hijos en pública o privada barata. Compra Walmart, Soriana Súper, Chedraui. Netflix sí, los demás esporádicos. **Copy:** valor por dinero, garantía, "para tu familia", "rinde".

### C- (16.4%)
- Clase media baja emergente. Casa propia (a veces sin escrituras), tal vez un auto, internet, secundaria-prepa completa, smartphone Xiaomi o Samsung gama media. Compra Bodega Aurrera, Soriana Mercado, mercado sobre ruedas. Netflix compartido. **Copy:** practical, MSI (meses sin intereses) es clave, oferta.

### D+ (14.9%)
- Clase trabajadora alta / clase media en construcción. Renta o casa con título irregular, sin auto o uno viejo, internet de prepago, secundaria, smartphone $3-5K. Compra en mercados, Bodega Aurrera, tianguis, tienda de la esquina. **Copy:** "más por menos", precio sin filtro, garantía explícita.

### D (25.4%)
- El bloque MÁS grande de México. Sin auto, sin internet fijo (sí celular con datos limitados), primaria-secundaria, vivienda autoproducida. Compra en mercado, tienda de barrio, tianguis. Crédito vía Coppel, Elektra, fonacot. **Copy:** súper directo, español llano, precios al frente, financiamiento.

### E (8.7%)
- Pobreza extrema o vulnerable. Vivienda precaria, sin servicios completos, primaria incompleta. Programas sociales son ingreso principal. Compra en tianguis, mercado, tiendas locales muy pequeñas. **Copy:** no aspiracional — funcional, comunitario, sin jerga.

## Workflow recomendado

### Caso 1: Usuario pide clasificar un hogar específico

1. Pregunta las 6 variables (educación, baños, autos, internet, ocupados, dormitorios).
2. Calcula puntos usando la tabla.
3. Identifica nivel.
4. Devuelve el output estructurado de arriba.
5. Si el usuario solo te dio 4-5 variables, asume valor mediano (mediana nacional) y advierte que es estimación.

### Caso 2: Usuario solo te da la colonia/CP

1. NO puedes clasificar exacto sin las 6 variables. Avisa esto.
2. Devuelve **distribución probable** basada en estado + tamaño de localidad.
3. Sugiere qué preguntas haría AMAI si quisiera precisión.

### Caso 3: Usuario quiere segmentar una base de datos

1. Pide que comparta columnas disponibles.
2. Mapea sus columnas a las 6 variables AMAI.
3. Genera SQL/pandas snippet que aplique la regla.

## Lo que NO hace este skill

- **No reemplaza la regla AMAI oficial** para investigación de mercado certificada. Para entregables formales a clientes en MR, usen el algoritmo licenciado AMAI.
- **No predice ingreso** en pesos. AMAI mide estilo de vida y comodidades, no salario líquido. Un trabajador petrolero puede ganar mucho y vivir en D+ por elección.
- **No es CONEVAL.** AMAI ≠ pobreza multidimensional. CONEVAL mide carencias sociales para política pública, AMAI mide nivel para marketing.
- **No clasifica empresas.** Solo hogares / personas.

## Fuentes

- **Nota Metodológica NSE AMAI 2024** (Comité Técnico AMAI, octubre 2023) — distribuciones, coeficientes de regresión, validaciones. Path: `research/amai/amai_nse_2024_nota_metodologica.pdf`.
- **Cuestionario AMAI** (vigente 2024 desde versión 2022) — Path: `research/amai/amai_cuestionario_2022.pdf`.
- **ENIGH 2022 microdatos** — base sobre la cual AMAI 2024 fue validada. Path: `research/inegi/enigh-2022/microdatos_enigh_ns_2022_csv.zip`.
- **ENIGH 2024 microdatos** — para revalidar la regla en datos más recientes. Path: `research/inegi/enigh-2024/microdatos_enigh2024_ns_csv.zip`.
