# mercado-local-mx — Ejemplos

## Ejemplo 1: Dentista cosmético en Mérida

**Usuario:** "Quiero abrir una clínica dental cosmética (blanqueamiento, ortodoncia estética, implantes). Estoy viendo Mérida. Ticket promedio $8,000. Capacidad: 80 pacientes/mes."

### Paso 1: Target
- 25-55 años, ambos géneros, NSE C/C+/A/B (los que pagan tratamiento cosmético $5K+)

### Paso 2: TAM Mérida
```bash
demografia-mx: SELECT SUM(poblacion) FROM poblacion
  WHERE anio=2026 AND entidad='Yucatán' AND edad BETWEEN 25 AND 55
```
→ Yucatán 25-55 = 1,120,000
→ Mérida ZM ~52% = **582,000**

### Paso 3: SAM (con NSE)
- Yucatán: C 15% + C+ 12% + A/B 8% = **35%**
- SAM = 582,000 × 35% = **204,000 personas**

### Paso 4: Competencia
```bash
precios-mx no aplica para dentistas (no es retail PROFECO).
→ Recomendación: scrape Google Maps "dentista Mérida" para conteo.
```

### Paso 5: SOM razonable
- Dentista cosmético = nicho diferenciado. Share 0.5-2%.
- SOM = 204,000 × 1% = **2,040 personas/año** = ~170 personas/mes que potencialmente buscan tu servicio.
- Pero conversión típica = 20-30%. Pacientes reales/mes = 35-50.

### Paso 6: Cruza con capacidad
- Capacidad: 80/mes. SOM: 35-50/mes. **Bottleneck = demanda.**
- Subutilización esperada en primer año: ~40%.

### Paso 7: Ingreso estimado
- 45 pacientes × $8,000 = **$360,000/mes** (estimación conservadora año 1)

### Output:
```
Análisis de viabilidad: clínica dental cosmética en Mérida

Semáforo: 🟡 Marginal pero viable

TAM Mérida 25-55: 582,000
SAM (NSE C/C+/A/B): 204,000
SOM mensual: 35-50 pacientes (~0.02-0.025% de SAM convertidos)
Ingreso estimado mes: $280K-$400K MXN

Riesgos:
- Mérida tiene Yucatán A/B en 8% (bajo nacional). Mercado premium ajustado.
- Capacidad subutilizada los primeros 12 meses → ojo con costos fijos.
- Necesitas Google Ads + Instagram + referidos profesionistas para llenar.

Recomendación:
1. Sí es viable pero NO te endeudes con renta premium ($60K+/mes).
   Busca local <$30K renta.
2. Invierte en marketing digital + alianzas con clínicas estéticas
   y dermatólogos para referidos.
3. Considera Mérida Norte (Cabo Norte / Altabrisa / Temozón) donde se
   concentra NSE A/B/C+.

Alternativas: Querétaro y Aguascalientes tienen mejor combo NSE A/B (11-13%)
+ tamaño + crecimiento.
```

---

## Ejemplo 2: Café especialidad en Tlaquepaque

**Usuario:** "Café de especialidad, ticket promedio $90 pesos, capacidad 4,000 transacciones/mes (sentados + para llevar). ¿Viable en Tlaquepaque?"

### Resumen:
- Tlaquepaque es parte ZMG (~62% Jalisco)
- Target 22-40, NSE C/C+/A/B (los que pagan $90 por café)
- Jalisco 22-40 = ~3.1M · ZMG ~62% = 1.9M
- NSE C+C++A/B en Jalisco = 19+16+8 = 43%
- SAM ZMG = 1.9M × 43% = ~820,000 personas

Pero atención: ZMG ≠ Tlaquepaque. Tlaquepaque es solo ~17% de ZMG → SAM micro = 140,000.
De esos, los que toman café especialidad regularmente: ~15-20%. → ~25,000 clientes potenciales.

Share alcanzable para café local: 1-3% de cliente potencial = 250-750/mes activos.
Frecuencia café especialidad = 2-4 visitas/mes promedio = 750-3,000 transacciones/mes.

Ingreso estimado: 1,500 × $90 = **$135K/mes** (escenario realista año 1).

**Semáforo: 🟡 Viable con ejecución impecable.** Capacidad supera demanda (4,000 vs 1,500) → no satures inversión en mobiliario.

---

## Ejemplo 3: Comparativo "¿en qué ciudad lanzo?"

**Usuario:** "Tengo presupuesto para 1 sucursal de mi marca de muebles de gama media (ticket $25K, NSE objetivo C/C+). ¿En qué ciudad de Bajío me conviene?"

```sql
-- demografia-mx: target 30-55 (jefes de hogar comprando muebles)
SELECT entidad, SUM(poblacion) AS adultos
FROM poblacion
WHERE anio = 2026
  AND entidad IN ('Guanajuato', 'Querétaro', 'Aguascalientes', 'San Luis Potosí')
  AND edad BETWEEN 30 AND 55
GROUP BY entidad;
```

Resultado:
- Guanajuato: 1.55M
- Querétaro: 0.78M
- Aguascalientes: 0.45M
- SLP: 0.79M

```python
# nse-mx: % C+C+ por estado
gto = 18+11 = 29%   → SAM 30-55 GTO = 1.55M × 29% × ~25% (León ZM share) ≈ 113K
qro = 19+15 = 34%   → SAM 30-55 QRO ZM = 0.78M × 34% × 55% ≈ 146K
ags = 20+15 = 35%   → SAM 30-55 AGS capital = 0.45M × 35% × 70% ≈ 110K
slp = 14+12 = 26%   → SAM 30-55 SLP capital = 0.79M × 26% × 40% ≈ 82K
```

**Output:**
```
Ranking para abrir tu sucursal de muebles gama media:

1. Querétaro ZM   ·  SAM 146K  ·  NSE C/C+ 34%  ·  crecimiento alto
2. Guanajuato (León)  ·  SAM 113K  ·  NSE 29%  ·  competencia alta
3. Aguascalientes  ·  SAM 110K  ·  NSE 35% (mejor mix)  ·  ciudad chica
4. San Luis Potosí  ·  SAM 82K  ·  NSE 26%  ·  menos competencia

Recomendación: Querétaro o Aguascalientes.
- Querétaro = más TAM + NSE alto + dinámica industrial.
- Aguascalientes = mejor mix NSE + menos competencia + costos bajos.

Si tu marca es premium → Querétaro (Juriquilla, El Refugio).
Si tu marca es value premium → Aguascalientes (cerca Plaza Vía).
```
