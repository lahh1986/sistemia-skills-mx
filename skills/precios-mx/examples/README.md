# precios-mx — Ejemplos

Cada ejemplo muestra: pregunta del usuario → query DuckDB → output recomendado.

## Ejemplo 1: Precio puntual en municipio

**Usuario:** "¿Cuánto cuesta una Coca-Cola 600 ml en Iztapalapa hoy?"

**Query:**
```sql
SELECT cadena_comercial, nombre_comercial, presentacion, precio, fecha_registro
FROM precios
WHERE producto ILIKE '%refresco%'
  AND marca ILIKE '%coca%'
  AND presentacion ILIKE '%600%'
  AND municipio ILIKE '%iztapalapa%'
  AND fecha_registro >= CURRENT_DATE - INTERVAL '90 days'
ORDER BY precio;
```

**Output al usuario:**

```
Precio de Coca-Cola 600 ml en Iztapalapa (últimos 90 días)

Mediana: $16.50 MXN
Rango: $13.00 (Bodega Aurrera) – $19.50 (Súper City)
Muestra: 47 capturas en 22 sucursales

Más barato: Bodega Aurrera Av. Tláhuac — $13.00 (2026-02-12)
Más caro:   Súper City Eje 8 — $19.50 (2026-01-28)

→ Diferencia 50% entre la cadena más barata y la más cara. Si compras semanal,
  cambiar de Súper City a Bodega Aurrera te ahorra ~$338/año por familia (1 refresco/día).
```

---

## Ejemplo 2: Comparación geográfica

**Usuario:** "¿Dónde es más barata la tortilla en México?"

**Query:**
```sql
SELECT estado,
       MEDIAN(precio) AS mediana,
       MIN(precio) AS minimo,
       MAX(precio) AS maximo,
       COUNT(*) AS n
FROM precios
WHERE producto ILIKE '%tortilla%'
  AND fecha_registro >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY estado
HAVING COUNT(*) >= 30
ORDER BY mediana;
```

**Output:**

```
Tortilla por estado (mediana últimos 90 días, n≥30)

Más barata:  Tlaxcala       $19.00/kg
             Hidalgo        $19.50/kg
             Estado de Méx. $20.00/kg

Más cara:    Baja California Sur  $32.00/kg
             Quintana Roo         $30.00/kg
             Baja California      $28.00/kg

Brecha nacional: 68% entre el más barato y el más caro.

→ Si vendes producto que usa tortilla en BCS, tu COGS de tortilla es ~70% más
  alto que un competidor en Tlaxcala. Considéralo en pricing.
```

---

## Ejemplo 3: Comparación entre cadenas

**Usuario:** "¿Walmart o Soriana para hacer mi despensa en Guadalajara?"

**Query:**
```sql
WITH canasta AS (
  SELECT 'Leche' AS item, '%leche ultrapasteurizada%' AS p UNION
  SELECT 'Huevo', '%huevo%' UNION
  SELECT 'Aceite', '%aceite%' UNION
  SELECT 'Frijol', '%frijol%' UNION
  SELECT 'Pasta', '%pasta para sopa%' UNION
  SELECT 'Atún', '%atún%'
)
SELECT c.item,
       p.cadena_comercial,
       MEDIAN(p.precio) AS mediana
FROM precios p
JOIN canasta c ON p.producto ILIKE c.p
WHERE p.cadena_comercial IN ('Walmart', 'Soriana Híper', 'Soriana Súper')
  AND p.municipio ILIKE '%guadalajara%'
  AND p.fecha_registro >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY c.item, p.cadena_comercial
ORDER BY c.item, p.cadena_comercial;
```

**Output:**

```
Canasta 6 ítems en Guadalajara — Walmart vs Soriana

Item    Walmart   Soriana   Δ
Leche   $26.50    $28.00    Walmart +$1.50
Huevo   $42.00    $39.50    Soriana +$2.50
Aceite  $48.00    $51.00    Walmart +$3.00
Frijol  $38.00    $40.00    Walmart +$2.00
Pasta   $14.50    $14.00    Soriana +$0.50
Atún    $21.00    $22.50    Walmart +$1.50

Total canasta: Walmart $190.00 · Soriana $195.00
→ Walmart sale 2.6% más barato en esta canasta de 6 SKUs.
   Pero Soriana gana en huevo y pasta. Si tu volumen es huevo-pesado, Soriana.
```

---

## Ejemplo 4: Histórico de inflación

**Usuario:** "¿Cuánto ha subido el aceite el último año?"

**Query:**
```sql
SELECT DATE_TRUNC('month', fecha_registro) AS mes,
       MEDIAN(precio) AS mediana
FROM precios
WHERE producto ILIKE '%aceite%'
  AND fecha_registro >= '2025-01-01'
GROUP BY mes
ORDER BY mes;
```

**Output:**

```
Aceite — mediana nacional por mes

2025-01  $42.00
2025-04  $44.00
2025-07  $46.50
2025-10  $48.00
2026-01  $49.50
2026-02  $50.00

→ Subió 19% en 13 meses (vs INPC general ~4-5%). Aceite es uno de los SKU
  más inflacionarios. Si vendes producto que usa aceite (frituras, restaurantes,
  panadería), tu COGS está subiendo ~3x más rápido que la inflación general.
```

---

## Ejemplo 5: Benchmark de pricing

**Usuario:** "Voy a vender mi salsa picante artesanal a $65 los 250 ml en supermercados de CDMX. ¿Es justo?"

**Query:**
```sql
SELECT presentacion, marca, MEDIAN(precio) AS mediana, MIN(precio) AS minimo, MAX(precio) AS maximo
FROM precios
WHERE producto ILIKE '%salsa%'
  AND estado ILIKE '%ciudad de méxico%'
  AND fecha_registro >= CURRENT_DATE - INTERVAL '180 days'
GROUP BY presentacion, marca
HAVING COUNT(*) >= 5
ORDER BY mediana DESC;
```

**Output:**

```
Salsas en CDMX — distribución de precios

Tabasco 60 ml          $48.00  (premium internacional)
Cholula 150 ml         $52.00  (premium mexicano)
Valentina 1 lt         $35.00  (mass-market)
Búfalo 150 ml          $22.00  (value)
La Costeña 250 ml      $28.00  (mass-market)

Tu propuesta: $65 / 250 ml = $260/lt

Lectura: caes 2-3x por encima de las marcas mass-market y arriba de las premium.
Probablemente solo viable en (a) anaqueles gourmet (City Market, La Comer Sumesa,
Costco premium) o (b) con storytelling artesanal fuerte. En anaquel mass, el shopper
NO va a alcanzar $65 cuando hay Valentina a $35.

Sugerencia: bajar a $45-50 para abrir canal mass, o subir a $75-85 con presentación
gourmet (botella vidrio, etiqueta artesanal) y meterlo solo en canal premium.
```
