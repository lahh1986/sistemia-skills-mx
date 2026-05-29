---
name: precios-mx
description: |
  Usar cuando el usuario quiera consultar PRECIOS REALES de productos en México
  por colonia, ciudad, estado, cadena comercial o periodo. Cubre 10.5 millones
  de registros PROFECO 2024-2026 (911 productos × 231 cadenas × 31 estados)
  con lat/lon, dirección y fecha. Ideal para: benchmarks regionales, detectar
  arbitraje, validar pricing, encontrar la cadena más barata para un SKU,
  monitorear inflación local, fact-check de "está carísimo".

  Triggers: "cuánto cuesta X en Y", "precio de X en [colonia/ciudad/estado]",
  "dónde es más barato", "compara precio entre cadenas", "Walmart vs Soriana",
  "precio histórico", "inflación de [producto]", "arbitraje", "cuál es el
  precio justo de", "PROFECO", "Quién es Quién en los Precios", "QQP",
  "benchmark de precios", "precios reales México".
---

# precios-mx — Consulta de precios reales MX (PROFECO QQP)

> Wrapper de Claude Code sobre `precios.duckdb` — base consolidada del programa
> **Quién es Quién en los Precios** de PROFECO, con 10.5 M de capturas
> entre 2024-01-02 y 2026-02-28.

## Cuándo activarte

- El usuario pregunta cuánto cuesta un producto específico en una zona específica
- El usuario quiere comparar precios entre cadenas (Walmart, Soriana, Bodega Aurrera, Chedraui, La Comer, Costco, Sam's, HEB, Oxxo, etc.)
- El usuario pregunta dónde es más barato comprar X
- El usuario quiere ver la variación de precio de un producto a lo largo del tiempo
- El usuario quiere validar si un precio que vio "está caro" o "está bien"
- El usuario está construyendo pricing para un producto y necesita benchmark
- El usuario quiere mapear arbitraje entre estados (comprar en X, vender en Y)
- El usuario menciona PROFECO, QQP, Quién es Quién en los Precios

**NO actives si:** el usuario quiere precios de servicios (consultas médicas, plomería, etc.) — PROFECO solo cubre productos de consumo masivo, electrónicos, muebles, juguetes y similares en retail físico.

## Cobertura del dataset

| Dimensión | Cobertura |
|---|---|
| Periodo | 2024-01-02 → 2026-02-28 (~2 años, refresco semanal/quincenal) |
| Registros | 10,543,471 |
| Productos únicos | 911 (Refresco, Jamón, Leche, Toalla Femenina, Detergente, etc.) |
| Cadenas | 231 (Walmart, Soriana, Chedraui, Bodega Aurrera, Costco, HEB, Sam's, La Comer, Fresko, Casa Ley, Sumesa, Calimax, Smart, Merza, Waldo's, etc.) |
| Estados | 31 (todos excepto algún boletín faltante) |
| Geolocalización | lat/lon + dirección física por sucursal |

**Schema (tabla `precios`):**
```
producto         VARCHAR  -- ej "Refresco", "Leche Ultrapasteurizada", "Carne Res"
presentacion     VARCHAR  -- ej "Lata 355 ml", "1 lt", "kg"
marca            VARCHAR  -- ej "Coca-Cola", "Lala", "Bachoco"
categoria        VARCHAR  -- ej "Botanas y Bebidas", "Derivados de Leche"
catalogo         VARCHAR
precio           DOUBLE   -- en MXN
fecha_registro   DATE
cadena_comercial VARCHAR  -- ej "Walmart", "Soriana Híper"
giro             VARCHAR
nombre_comercial VARCHAR  -- nombre específico de la sucursal
direccion        VARCHAR
estado           VARCHAR
municipio        VARCHAR
latitud          DOUBLE
longitud         DOUBLE
filename         VARCHAR  -- archivo PROFECO origen
```

## Workflow

### Paso 1: Identifica intent del usuario

Determina cuál de estos casos aplica:

| Caso | Pregunta del usuario | Query base |
|---|---|---|
| A. **Precio puntual** | "¿Cuánto cuesta una Coca 600 ml en Iztapalapa?" | Filtra por producto + marca + presentación + municipio. Devuelve mediana + min/max + cadenas |
| B. **Comparación geográfica** | "¿Dónde es más barato comprar tortilla?" | Group by estado/municipio, AVG(precio) últimos 90 días |
| C. **Comparación cadenas** | "¿Walmart vs Soriana para huevo?" | Group by cadena_comercial, mediana + min últimos 90 días |
| D. **Histórico** | "¿Cuánto ha subido el aceite el último año?" | Time series por mes, MIN/AVG por periodo |
| E. **Arbitraje** | "¿Dónde compro barato cigarros para vender en frontera?" | Top 3 estados más baratos vs más caros, mismo SKU |
| F. **Benchmark de pricing** | "Voy a vender X a $Y, ¿es justo?" | Distribución del producto + percentil donde cae $Y |

### Paso 2: Construye la query DuckDB

**Path al DB:** `/Volumes/Storage/sistemia-skills-mx/research/precios.duckdb` (o symlink `~/sistemia-skills-mx/research/precios.duckdb`).

**Usa el helper:**
```bash
~/sistemia-skills-mx/skills/precios-mx/scripts/query.sh "<SQL>"
```

**Convenciones:**
- Siempre filtra `fecha_registro >= CURRENT_DATE - INTERVAL '180 days'` salvo que pidan histórico (mantiene relevancia).
- Para texto de producto usa `producto ILIKE '%X%'` (case-insensitive).
- Para cadenas reporta `MEDIAN(precio)` no `AVG` — más robusto a outliers.
- Para mostrar al usuario incluye SIEMPRE: producto, presentación, marca, precio, cadena, sucursal/municipio, fecha.
- Si el dataset tiene < 10 capturas para la query, advierte "muestra pequeña — interprétalo con cautela".

### Paso 3: Devuelve el output

Estructura del output al usuario:

```markdown
## Precio de {{producto}} en {{ubicación}}

**Mediana actual** (últimos {{N}} días): **${{precio}} MXN** por {{presentación}}
**Rango observado:** ${{min}} – ${{max}}
**Muestra:** {{n}} capturas en {{n_sucursales}} sucursales

### Top 3 más barato
| Cadena | Sucursal | Precio | Fecha |
| ... |

### Top 3 más caro
| ... |

### Notas
- {{insight sobre estacionalidad / cadena outlier / brecha regional}}
- Fuente: PROFECO "Quién es Quién en los Precios" via precios-mx.
```

Si el usuario pidió comparación geográfica:
```markdown
## {{producto}} por estado

| Estado | Mediana | Min | Max | Capturas |
| Nuevo León | $14.50 | $11.90 | $19.50 | 1,243 |
| CDMX | $15.20 | ... |
...

Más barato: **{{estado}}** (${{precio}})
Más caro: **{{estado}}** (${{precio}})
Brecha: **{{X%}}**
```

### Paso 4: Recomendación accionable

Cierra siempre con 1-2 líneas accionables, NO solo data:
- "Para tu negocio en {{municipio}}, considera que la cadena más barata es {{cadena}} a ${{precio}} — ahorras {{X%}} vs comprar en {{cadena_promedio}}."
- "Si tu pricing target es ${{X}}, caes en el percentil {{P}} — {{lectura}}."
- "Cuidado: este SKU sube {{X%}} cada {{periodo}} históricamente."

## Lo que NO hace este skill

- **No predice precios futuros.** Es un wrapper de datos históricos.
- **No cubre productos fuera del catálogo PROFECO.** Servicios, software, B2B, productos artesanales NO están.
- **No tiene precios de e-commerce.** Solo retail físico capturado por PROFECO.
- **No actualiza en tiempo real.** Última captura disponible: 2026-02-28. Si el usuario pide "precio HOY", aclara que es la última observación.

## Ejemplos

Ver `examples/` para queries reales con outputs ejemplificados.

## Fuentes

- **PROFECO Quién es Quién en los Precios** (programa público desde 2002, datos abiertos en datos.gob.mx).
- Consolidado en `precios.duckdb` por el proyecto Sistemia Skills MX (2026-05).
- Diccionario de campos: `research/profeco/profeco_qqp_2026_diccionario.csv`.
