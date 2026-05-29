---
name: mercado-local-mx (preview)
description: |
  Versión preview pública. Documenta el método del bundle, pero depende de
  precios-mx + demografia-mx + nse-mx + habitos-digitales-mx (algunos solo
  funcionan con datos comerciales de Sistemia). Versión completa por
  WhatsApp.
---

# mercado-local-mx — preview

> ¿Vale la pena abrir tu negocio físico en X ciudad/colonia mexicana?
> Análisis de viabilidad micro-mercado.
>
> **Esta es la versión preview.** Explica el método del bundle. Como orquesta
> 4 skills (`demografia-mx`, `nse-mx`, `precios-mx`, `habitos-digitales-mx`),
> requiere que los 4 estén instalados — y `precios-mx` + `demografia-mx`
> necesitan sus DBs comerciales para funcionar full.
> [**Acceso completo + análisis a la medida vía WhatsApp**](https://wa.me/525529477307?text=Hola%2C%20me%20interesa%20acceso%20completo%20a%20mercado-local-mx).

---

## Qué hace este skill

Tú le dices: "Quiero abrir una clínica dental cosmética en Mérida, ticket promedio $4,500 MXN, capacidad 200 pacientes/mes". El skill orquesta los datasets:

1. **Demografía local** — ¿cuántas personas viven en el catchment y son target?
2. **Distribución NSE** — ¿cuántas están en el rango de poder pagar?
3. **Nivel de precios y competencia** — ¿qué retail/competencia está cerca? ¿cuánto cobran?
4. **Hábitos digitales** — ¿cómo prospectas? ¿WhatsApp? ¿Instagram? ¿anuncios físicos?

Devuelve:
- **TAM / SAM / SOM** numerados con fuentes
- **Semáforo de viabilidad** (verde / amarillo / rojo) con razones
- **Sugerencia de ticket promedio** ajustado a la zona
- **Pricing tentativo** con base en precios.duckdb local
- **Canales de adquisición recomendados** con base en hábitos digitales del segmento

---

## Workflow (8 pasos resumidos)

| Paso | Qué hace |
|---|---|
| 1. Define target demográfico | Edad × sexo × NSE objetivo del giro |
| 2. TAM/SAM | Población del catchment ajustado por NSE |
| 3. Sanity check de precios | Competencia retail + capacidad de pago local |
| 4. Estima SOM | % alcanzable con tu propuesta |
| 5. Hábitos del segmento | Plataforma de adquisición primaria |
| 6. Ticket promedio realista | Mediana del precio en zona × ajustes |
| 7. Modelo unitario simple | Revenue × margen × volumen |
| 8. Semáforo + recomendación | Verde / Amarillo / Rojo con razones |

---

## Versión preview vs completa

| Característica | Preview (este repo) | Completo (Sistemia) |
|---|---|---|
| Documentación del método | ✅ Sí | ✅ Sí |
| Tabla giros × target típico | ✅ Sí | ✅ Sí |
| Ajustes por zona metro | ✅ Sí | ✅ Sí |
| Requiere `precios-mx` con DB | ⚠️ No funciona sin acceso comercial | ✅ Incluido |
| Requiere `demografia-mx` con DB | ⚠️ No funciona sin acceso comercial | ✅ Incluido |
| `nse-mx` data (público) | ✅ Sí | ✅ Sí |
| `habitos-digitales-mx` data (público) | ✅ Sí | ✅ Sí |
| Análisis llave en mano | ❌ No | ✅ Sí (servicio) |

---

## Cómo conseguir la versión completa

3 opciones, según tu caso:

1. **Bundle completo** — los 4 skills + DBs + soporte para que corras los análisis tú mismo
2. **Análisis a la medida** — tú nos das (giro, ubicación, target), nosotros te entregamos el dossier de viabilidad listo
3. **Suscripción de consultas** — quincenal / mensual, ideal para chains o quien evalúa muchas zonas

→ [Cuéntanos por WhatsApp](https://wa.me/525529477307?text=Hola%2C%20me%20interesa%20acceso%20completo%20a%20mercado-local-mx).

---

## Instalación (preview)

```bash
git clone https://github.com/lahh1986/sistemia-skills-mx.git
cp -r sistemia-skills-mx/skills/mercado-local-mx ~/.claude/skills/mercado-local-mx-preview
```

Con `nse-mx` + `habitos-digitales-mx` (públicos) ya puedes correr los pasos 1, 3 (parcial), 5 y 6 (parcial). Pasos 2, 4 y 7 requieren las DBs comerciales.

---

*Preview liberado bajo MIT. La orquestación full + análisis a la medida son producto comercial de Sistemia.*
