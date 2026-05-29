---
name: mercado-local-mx
description: |
  Usar cuando el usuario quiera VALIDAR LA VIABILIDAD DE ABRIR (o expandir) un
  negocio físico en una ciudad/colonia/estado de México. Genera un análisis
  micro-mercado que combina: tamaño poblacional del target (demografia-mx),
  distribución NSE local (nse-mx), nivel de precios y competencia retail
  (precios-mx), penetración digital (habitos-digitales-mx) e infraestructura
  financiera (CNBV). Devuelve TAM/SAM/SOM, semáforo de viabilidad, sugerencias
  de ticket promedio y pricing tentativo.

  Triggers: "vale la pena abrir X en Y", "viabilidad de negocio en",
  "análisis micro-mercado", "TAM SAM SOM", "estudio de mercado para",
  "voy a abrir una sucursal en", "expandir mi marca a", "qué ciudad
  conviene para lanzar", "feasibility study MX".
---

# mercado-local-mx — Análisis de viabilidad micro-mercado

> Skill **compuesto** que orquesta `demografia-mx`, `nse-mx`, `precios-mx` y
> (cuando aplica) `habitos-digitales-mx`. Te entrega un dossier de viabilidad
> para abrir o expandir un negocio físico en una ciudad/estado mexicano.

## Cuándo activarte

- El usuario está evaluando abrir una sucursal/negocio físico en una ciudad MX específica
- El usuario quiere expandir su marca a un estado nuevo
- El usuario pregunta "¿en qué ciudad conviene lanzar X?"
- El usuario tiene presupuesto y quiere saber dónde rinde más
- El usuario está buscando ubicación de un anchor store, café, salón, clínica, etc.

**NO actives si:**
- El usuario quiere análisis de mercado nacional/multipaís → usa `demografia-mx` solo.
- El usuario quiere validar copy/ad antes de gastar → usa `focus-group-mx`.
- El usuario quiere análisis de e-commerce sin ubicación física → este skill es para retail/servicio físico.

## Inputs requeridos

Antes de empezar, pregunta o infiere:

1. **Tipo de negocio** (dentista, barbería, café, clínica de belleza, restaurante, tienda de electrónicos, etc.)
2. **Ubicación tentativa** (ciudad y/o colonia/CP)
3. **Ticket promedio esperado** (en MXN) o rango
4. **Capacidad mensual** (clientes/transacciones por mes que puede atender)
5. **Target de cliente** (edad, género, NSE) — si el usuario no sabe, propón inferencia desde el negocio

Si el usuario no tiene 3-4 listos, propón valores típicos del giro y avisa.

## Workflow (8 pasos)

### 1. Define el target demográfico

Identifica el segmento que paga este negocio. Plantillas comunes:

| Giro | Target típico | NSE relevante |
|---|---|---|
| Dentista cosmético | 25-55 años, urbano | C / C+ / A/B |
| Dentista general / clínica social | 5-60, todas las edades, familias | D+ / C- / C |
| Barbería premium | hombres 18-45 | C / C+ |
| Café especialidad | 22-40, urbano | C / C+ / A/B |
| Restaurante familiar | 25-55 familias con hijos | C- / C / C+ |
| Tienda electrodomésticos crédito | 25-55, jefe de hogar | D+ / C- / C |
| Salón belleza alta gama | mujeres 30-55 | C+ / A/B |
| Plomería / electricista | jefes de hogar | D+ a A/B (todos) |
| Bar / cantina barrio | 25-55, alcohol | D / D+ / C- |

### 2. Tamaño del mercado addressable (TAM/SAM)

Consulta `demografia-mx`:

```bash
~/sistemia-skills-mx/skills/demografia-mx/scripts/query.sh "
SELECT SUM(poblacion) AS personas_target
FROM poblacion
WHERE anio = 2026
  AND entidad = '<ESTADO>'
  AND edad BETWEEN <MIN> AND <MAX>
  AND sexo IN (<H/M/AMBOS>)
"
```

Si tu ubicación es una **ciudad/municipio** (no estado entero), aplica un factor de ajuste:

| Ciudad/Zona Metro | % del estado |
|---|---|
| ZMVM (CDMX + EdoMex conurbado) | ~95% de CDMX + ~50% de EdoMex |
| ZMG (Zapopan + GDL + Tlajomulco + Tlaquepaque + Tonalá) | ~62% de Jalisco |
| Monterrey ZM | ~80% de Nuevo León |
| Puebla ZM | ~30% de Puebla |
| Tijuana | ~50% de BC |
| León | ~25% de Guanajuato |
| Querétaro ZM | ~55% de Querétaro |
| Mérida | ~52% de Yucatán |
| Cancún | ~45% de QRoo |
| Aguascalientes capital | ~70% de Ags |

Para colonias específicas, el aproximado es: una colonia residencial media en zona urbana = 5,000 – 25,000 habitantes. Pide al usuario radio de catchment (típico para retail físico: 2-5 km o 10-20 min en auto).

### 3. Ajusta por NSE relevante

Consulta `nse-mx` para sacar % del estado en cada NSE objetivo:

```bash
python3 -c "
import json
data = json.load(open('/Volumes/Storage/sistemia-skills-mx/skills/nse-mx/data/puntos_amai_2024.json'))
dist = data['distribucion_por_estado_pct']['<ESTADO>']
print(dist)
"
```

Multiplica: `TAM × pct_NSE_target = SAM`.

Ejemplo: Dentista cosmético en Mérida (Yucatán). Target = 25-55 NSE C/C+/A/B.
- Población Yucatán 25-55: ~1.1M
- Mérida ~52% = 572,000
- NSE C+C++A/B en Yucatán: 15% + 12% + 8% = 35%
- SAM = 572,000 × 35% = **200,000 personas**

### 4. Sanity check con nivel de precios local

Consulta `precios-mx` para benchmark de poder adquisitivo y competencia:

```bash
~/sistemia-skills-mx/skills/precios-mx/scripts/query.sh "
SELECT cadena_comercial, COUNT(DISTINCT nombre_comercial) AS sucursales
FROM precios
WHERE municipio ILIKE '%<CIUDAD>%'
  AND fecha_registro >= CURRENT_DATE - INTERVAL '180 days'
GROUP BY cadena_comercial
ORDER BY sucursales DESC LIMIT 15
"
```

Esto te dice qué retail ya está ahí. Walmart Express + 7-Eleven + Oxxo presentes = zona consolidada urbana. City Market + Costco premium + La Comer Sumesa = zona NSE alto. Solo Bodega Aurrera + tianguis = zona popular.

### 5. Estima penetración / share alcanzable (SOM)

Reglas de pulgar conservadoras por giro:

| Tipo de negocio | % SAM que captura un negocio individual razonable |
|---|---|
| Negocio nicho diferenciado en colonia chica | 0.5% – 2% del SAM |
| Negocio mainstream en zona urbana media | 0.1% – 0.5% del SAM |
| Tienda en zona NSE alto con poca competencia | 1% – 3% del SAM |
| Restaurante / café con anchor (1 año operando) | 1% – 5% del SAM (de los que comen fuera 1x/mes) |
| Negocio en colonia D/D+ con buen precio | 2% – 8% del SAM |

Multiplica frecuencia: si tu cliente típico viene 1×/mes, el cálculo es:
```
SOM_anual = SAM × share × 12 visitas/año
SOM_mensual = SAM × share
```

### 6. Cruza con capacidad

Si la capacidad mensual del negocio es **menor** que el SOM mensual, **bottleneck es operación**, no demanda. Si la capacidad es **mayor** que el SOM, **bottleneck es demanda** — riesgo de subutilización.

### 7. Proyecta ingreso mensual y valida vs costos

```
Ingreso mensual estimado = min(SOM_mensual, capacidad_mensual) × ticket_promedio
```

Pide al usuario costos fijos (renta, nómina, servicios) y costos variables (materia prima, comisión). Calcula margen y meses para recuperar inversión.

### 8. Output al usuario

```markdown
## Análisis de viabilidad: {{negocio}} en {{ciudad}}

### Semáforo
- **TAM:** {{N}} personas en target demográfico (edad/género/sexo)
- **SAM:** {{N}} con NSE relevante ({{niveles}})
- **SOM mensual razonable:** {{N}} clientes/mes
- **Ingreso bruto estimado:** ${{MXN}} / mes
- **Veredicto:** 🟢 viable / 🟡 marginal / 🔴 no viable

### Desglose
| Métrica | Valor | Notas |
| Población {{edad}} en {{ciudad}} | {{N}} | CONAPO 2026 |
| Distribución NSE local | C+ {{X%}}, C {{Y%}}, ... | AMAI 2024 × entidad |
| Competencia retail visible | {{N}} sucursales de {{cadenas}} | PROFECO últimos 180d |
| Ticket promedio esperado | ${{X}} | input usuario |
| Share alcanzable conservador | {{X%}} | rule of thumb por giro |

### Riesgos identificados
- {{ej. NSE objetivo es <20% de la población local → mercado pequeño}}
- {{ej. Ya hay 4 cadenas grandes del mismo giro → competencia consolidada}}
- {{ej. Ticket alto para nivel de precios local → resistencia}}

### Recomendación
{{2-3 líneas accionables}}

### Tres ubicaciones alternativas si no te convence esta
{{Usa demografia-mx para encontrar 3 ciudades con mejor combo NSE + tamaño + menos competencia}}
```

## Decisión rápida — heurísticas

- **Si el NSE objetivo es <10% del estado**, probablemente esa ciudad no es buena. Busca otra.
- **Si el TAM <100,000 y tu negocio necesita 1% share**, te quedan ~1,000 clientes posibles. Para B2C con frecuencia mensual, eso es marginal.
- **Si la ciudad tiene 4+ cadenas grandes del mismo giro ya operando**, asume competencia roja — pivota a propuesta de valor diferenciada antes de invertir.
- **Si el municipio tiene <500 capturas PROFECO los últimos 180 días**, es zona rural/semi-urbana — ajusta SAM y NSE a la baja.

## Lo que NO hace este skill

- **No es estudio de feasibility financiero.** No hace P&L, no estima CAC, no proyecta payback. Solo dimensiona mercado.
- **No considera tráfico peatonal/vehicular real.** Para eso necesitas data privada (Mapas Google Heatmap, Waze, Carto, etc.).
- **No conoce el ambiente competitivo de tu giro específico** más allá de retail PROFECO. Para spa, dentista, clínica veterinaria necesitas Google Maps / scrape.
- **No reemplaza visita en campo.** Es un primer filtro cuantitativo.

## Skills que usa internamente

| Skill | Para qué |
|---|---|
| `demografia-mx` | TAM por edad/género/entidad |
| `nse-mx` | Distribución NSE por entidad |
| `precios-mx` | Competencia retail visible + nivel de precios local |
| `habitos-digitales-mx` | (opcional) Penetración digital si el negocio requiere reservas online |
| `focus-group-mx` | (siguiente paso) Validar copy/branding del negocio una vez decidida la ubicación |
