# demografia-mx — Ejemplos

## Ejemplo 1: Cohorte simple — market sizing

**Usuario:** "¿Cuántas mujeres de 25-34 años viven en Jalisco hoy?"

```sql
SELECT SUM(poblacion) AS n
FROM poblacion
WHERE anio = 2026 AND entidad = 'Jalisco'
  AND sexo = 'Mujeres' AND edad BETWEEN 25 AND 34;
```

**Output al usuario:**
```
Mujeres 25-34 en Jalisco (2026): ~715,000

Como % de la entidad: 7.9%
Como % nacional del segmento: 8.4%

Comparativo nacional del segmento "mujeres 25-34":
  1. Estado de México   1,520,000
  2. Ciudad de México     820,000
  3. Jalisco              715,000
  4. Veracruz             630,000
  5. Puebla               530,000

Trayectoria Jalisco:
  2021: ~700K · 2026: ~715K · 2031: ~705K (crece hasta 2028, se contrae después)

Lectura: Tu TAM en este segmento llega a su pico entre 2028-2029.
Si dependes de adquisición de mujeres 25-34, tu ventana de crecimiento
orgánico es ~3 años. Después debes capturar más share o expandir cohorte.
```

---

## Ejemplo 2: Comparativo entre estados

**Usuario:** "¿En qué estado conviene lanzar mi app de citas? Quiero edades 18-30."

```sql
SELECT entidad,
       SUM(poblacion) FILTER (WHERE edad BETWEEN 18 AND 30) AS jovenes,
       SUM(poblacion) AS total,
       100.0 * SUM(poblacion) FILTER (WHERE edad BETWEEN 18 AND 30) / SUM(poblacion) AS pct_jovenes
FROM poblacion
WHERE anio = 2026 AND entidad != 'República Mexicana'
GROUP BY entidad
ORDER BY pct_jovenes DESC
LIMIT 10;
```

**Output esperado** (más jóvenes 18-30 por capita):
```
Top 10 estados por % de población 18-30:

  1. Quintana Roo    23.4%   (~470K personas 18-30)
  2. Baja California 22.1%
  3. Querétaro       21.8%
  4. Nuevo León      21.5%
  5. Aguascalientes  21.3%
  ...

Decisión: Quintana Roo + BCN + Querétaro son tu sweet spot por densidad.
Pero recuerda: market sizing NO es CAC. Para que sea viable, cruza con
ingreso (skill nse-mx) y penetración smartphone (skill habitos-digitales-mx).
```

---

## Ejemplo 3: Pirámide poblacional

**Usuario:** "Dame la pirámide de Nuevo León en 2026"

```sql
SELECT grupo_edad, sexo, poblacion
FROM poblacion_por_grupo
WHERE anio = 2026 AND entidad = 'Nuevo León'
ORDER BY grupo_edad, sexo;
```

**Output esperado:**
```
Pirámide poblacional — Nuevo León 2026

Grupo      Hombres    Mujeres    Total
0-4         265K       253K       518K
5-14        548K       527K     1,075K
15-17       162K       155K       317K
18-24       377K       367K       744K  ← bono demográfico
25-34       529K       540K     1,069K  ← bono demográfico
35-44       428K       452K       880K
45-54       350K       384K       734K
55-64       262K       298K       560K
65+         298K       370K       668K  ← envejecimiento

Total       3,219K     3,346K    6,565K  (51% mujeres)

Lectura: NL es relativamente joven y económicamente activo.
El grupo 18-44 es el 53% de la población = motor de consumo y trabajo.
65+ ya pesa 10%, va a duplicarse para 2050.
```

---

## Ejemplo 4: Proyección a 2050

**Usuario:** "¿Cuántos adultos mayores tendrá México en 2050?"

```sql
SELECT anio, SUM(poblacion) AS adultos_mayores
FROM poblacion
WHERE entidad = 'República Mexicana' AND edad >= 65
  AND anio IN (2025, 2030, 2040, 2050, 2060, 2070)
GROUP BY anio
ORDER BY anio;
```

**Output esperado:**
```
Adultos mayores (65+) — proyección nacional

2025  · 10.2 M  ·  7.8% de la población
2030  · 12.8 M  ·  9.5%
2040  · 19.4 M  · 13.4%
2050  · 26.3 M  · 17.5%
2060  · 32.1 M  · 21.0%
2070  · 36.0 M  · 23.6%

Lectura: en 25 años los 65+ pasan de 10M a 26M — multiplica por 2.6×.
Vertical de salud geriátrica, productos para adultos mayores, fintech
para pensiones, vivienda asistida, telemedicina = mercado en gestación.

Cuidado: este NO es bono demográfico — es transición al envejecimiento.
México tiene su pico de bono ~2025-2030 y empieza a perderlo en 2035.
```

---

## Ejemplo 5: Bono demográfico — cuándo termina

**Usuario:** "¿Cuándo se acaba el bono demográfico de México?"

```sql
SELECT anio,
       100.0 * SUM(poblacion) FILTER (WHERE edad < 15 OR edad >= 65)
         / SUM(poblacion) FILTER (WHERE edad BETWEEN 15 AND 64) AS razon_dependencia
FROM poblacion
WHERE entidad = 'República Mexicana'
  AND anio IN (2000, 2010, 2020, 2025, 2030, 2040, 2050, 2070)
GROUP BY anio
ORDER BY anio;
```

**Output esperado:**
```
Razón de dependencia — República Mexicana
(dependientes / población activa, %)

2000  ·  64.6  ← saliendo de alta dependencia infantil
2010  ·  55.7
2020  ·  51.0  ← cerca del fondo (mejor para bono)
2025  ·  51.4
2030  ·  53.2  ← empieza a subir por envejecimiento
2040  ·  58.6
2050  ·  66.4
2070  ·  82.0  ← peor que 2000, ahora por adultos mayores

Lectura: El bono demográfico de México vive su mejor año técnico
entre 2020-2030. Después, la población activa se contrae relativo
a dependientes. Cierre del bono: ~2030-2035.

Estrategia: si tu negocio depende de fuerza laboral joven y barata,
los próximos 5-10 años son los últimos con esa abundancia.
Después, encarecimiento estructural del costo laboral.
```
