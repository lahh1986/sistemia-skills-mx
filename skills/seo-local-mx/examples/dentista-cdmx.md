# Ejemplo end-to-end: Dentista en Roma Norte, CDMX

> Caso: Dra. Ana Solís, clínica dental en Roma Norte, CDMX. 38 reseñas Google con rating 4.6. No aparece en el Local Pack para "dentista cerca de mí" buscando desde el barrio. Quiere llegar al top 3 del pack en 6-9 meses sin pagar Ads.

---

## Paso 1 — Diagnóstico

| Variable | Valor del caso |
|---|---|
| Vertical | Dentista (clínica con 2 odontólogas) |
| Ciudad / tamaño | CDMX → **metrópoli** (multiplicador reviews 1.35x) |
| Colonia | Roma Norte, Cuauhtémoc |
| GBP actual | Verificado, 38 reseñas, 4.6, categoría "Dentista" ✓ |
| Sitio web | WordPress 2022, sin schema, CWV en rojo (LCP 4.2s) |
| Competencia top3 Local Pack | 420, 287, 195 reseñas |
| Problema concreto | No aparece en Local Pack ni con búsqueda desde Roma Norte |

## Paso 2 — Carga de datos

```
keywords-mx.json     → vertical "dentista"
reviews-velocity-mx.json → vertical "dentista", ciudad_size "metropoli"
directorios-mx.json  → filtrar vertical=salud
ai-overviews-mx.json → patrones citación
voice-search-mx.json → vertical "dentista"
gbp-categorias-mx.json → confirmar categoría + atributos
```

## Paso 3 — Gap de reseñas (benchmark CDMX metrópoli)

De `reviews-velocity-mx.json` vertical "dentista" / ciudad_size "metropoli":

```json
{
  "reseñas_promedio_top3_local_pack": 467,
  "reseñas_minimas_competir": 70,
  "velocidad_recomendada": "12-18 nuevas/mes",
  "rating_promedio_top3": 4.8
}
```

**Posicionamiento de Ana:**

- **Actual:** 38 reseñas, 4.6 rating
- **Para competir (P10):** 70 reseñas, 4.5+ → faltan **32 reseñas**
- **Para dominar (P50):** ~467 reseñas, 4.8 → faltan ~430 reseñas

**Plan:**
- Pedir **12-15 reseñas/mes** a pacientes (no incentivar, momento natural post-cita)
- En 3 meses: 38 → 80 (cruza umbral de competir)
- En 12 meses: 38 → 200 (entra a zona de contender por top 3)
- Subir rating a 4.7 promedio (responder TODAS, incluyendo negativas con plan de mejora)

## Paso 4 — Schema LocalBusiness JSON-LD listo para pegar

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Dentist",
  "@id": "https://clinicaanasolisroma.mx/#dentist",
  "name": "Clínica Dental Ana Solís — Roma Norte",
  "image": [
    "https://clinicaanasolisroma.mx/img/fachada.jpg",
    "https://clinicaanasolisroma.mx/img/consultorio.jpg"
  ],
  "logo": "https://clinicaanasolisroma.mx/img/logo.svg",
  "url": "https://clinicaanasolisroma.mx",
  "telephone": "+525512345678",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Calle Tonalá 123, Int. 2",
    "addressLocality": "Roma Norte",
    "addressRegion": "Cuauhtémoc, CDMX",
    "postalCode": "06700",
    "addressCountry": "MX"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 19.4154,
    "longitude": -99.1665
  },
  "openingHoursSpecification": [
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "20:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "14:00"}
  ],
  "areaServed": [
    {"@type": "City", "name": "Roma Norte"},
    {"@type": "City", "name": "Roma Sur"},
    {"@type": "City", "name": "Condesa"},
    {"@type": "City", "name": "Juárez"},
    {"@type": "City", "name": "Cuauhtémoc"}
  ],
  "sameAs": [
    "https://www.facebook.com/clinicaanasolisroma",
    "https://www.instagram.com/clinicaanasolisroma",
    "https://www.doctoralia.com.mx/ana-solis-roma",
    "https://www.google.com/maps/place/..."
  ],
  "hasMap": "https://www.google.com/maps/place/...",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.6",
    "reviewCount": "38"
  },
  "medicalSpecialty": ["Dentistry", "Orthodontics", "Endodontics"],
  "availableService": [
    {"@type": "MedicalProcedure", "name": "Limpieza dental"},
    {"@type": "MedicalProcedure", "name": "Blanqueamiento dental"},
    {"@type": "MedicalProcedure", "name": "Extracción de muelas del juicio"},
    {"@type": "MedicalProcedure", "name": "Endodoncia"},
    {"@type": "MedicalProcedure", "name": "Ortodoncia / Brackets"},
    {"@type": "MedicalProcedure", "name": "Implantes dentales"}
  ]
}
</script>
```

**Por qué importa:** de `ai-overviews-mx.json`, el patrón #1 para ser citado en AI Overviews es Schema completo. Sin esto, ni Google Maps ni AIO te eligen como entidad confiable.

## Paso 5 — Keywords prioritarias (de `keywords-mx.json` vertical "dentista")

**Head terms** (usar en title, H1, meta description):
- dentista (no "odontólogo" como primario — es preferencia léxica MX)
- clínica dental
- odontólogo (secundario formal, para landing institucional)

**Modificadores calientes** (combinar con head + ciudad/colonia):
- `cerca de mí` (local-now) → "dentista cerca de mí Roma Norte"
- `precio` (price) → "blanqueamiento dental precio CDMX"
- `24 horas / urgencias` (urgency) → "dentista urgencias CDMX"
- `sin dolor` (fear) → "dentista sin dolor Roma Norte"
- `domingo / abierto ahora` (schedule) → "dentista abierto sábado Roma Norte"

**Long-tail alta intención** (landings de servicio):
- extracción muela del juicio precio CDMX
- blanqueamiento dental costo
- endodoncia precio cerca de mí
- brackets precio mensualidad

**Regionalismos a respetar:**
- "muelas del juicio" en páginas comerciales, "terceros molares" en FAQ clínico
- "dentista" como head (no "odontólogo")

## Paso 6 — FAQPage schema (de `voice-search-mx.json`)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "¿Atienden urgencias dentales hoy en Roma Norte?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Sí, atendemos urgencias dentales en horario regular (L-V 9-20h, S 9-14h) en Calle Tonalá 123, Roma Norte. Si tienes dolor agudo, fractura o sangrado, llámanos al +52 55 1234 5678 y te damos hueco el mismo día."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cuánto cuesta una extracción de muela del juicio en CDMX?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "El costo varía según complejidad (incluida vs incluida en hueso). En nuestra clínica de Roma Norte, una extracción simple desde $2,500 MXN y una compleja con cirugía desde $5,500 MXN. Incluye consulta previa, radiografía y revisión post-operatoria."
      }
    },
    {
      "@type": "Question",
      "name": "¿Atienden dentista los domingos?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No abrimos domingos. Nuestro horario es lunes a viernes 9:00-20:00 y sábado 9:00-14:00. Para urgencias fuera de horario contamos con línea WhatsApp +52 55 1234 5678."
      }
    },
    {
      "@type": "Question",
      "name": "¿Cuánto cuesta el blanqueamiento dental?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "El blanqueamiento dental profesional en consultorio en nuestra clínica de Roma Norte va desde $3,500 MXN (sesión única) hasta $6,500 MXN (paquete completo con férulas para casa). Resultado visible desde la primera sesión."
      }
    }
  ]
}
</script>
```

**Reglas aplicadas:** respuestas de 40-60 palabras, con servicio + zona + horario/precio + siguiente acción. Lenguaje natural es-MX ("muelas del juicio" no "terceros molares").

## Paso 7 — Directorios prioritarios (de `directorios-mx.json`)

| Prioridad | Directorio | Por qué |
|---|---|---|
| 1 | **Google Business Profile** | Ya verificado — siguiente: posts semanales + Q&A sembradas + 8 fotos nuevas/mes |
| 2 | **Doctoralia** | Dominante absoluto en salud MX. Alimenta Reserve with Google. Configurar agenda online. |
| 3 | **Apple Maps Connect** | iPhone share MX creciente. Alimentar perfil mínimo + verificar Yelp para reseñas. |
| 4 | **Waze for Business** | CDMX = Waze city. Perfil con horario + categoría. |
| 5 | **Facebook Pages + Instagram Business** | Buscador local complementario MX. Etiquetas de ubicación. |
| 6 | **Sección Amarilla** | Citación NAP histórica MX. Free tier para verificación NAP. |
| 7 | **Bing Places** | Bajo tráfico B2C, alto valor NAP. Auto-sync con GBP. |

**No spammear** Cylex, Páginas Amarillas o GuiaMexico hasta que los 7 anteriores estén 100%.

## Paso 8 — Próximos pasos en orden de impacto

| Semana | Acción | Impacto esperado |
|---|---|---|
| 1 | Pegar Schema LocalBusiness/Dentist + FAQPage en home y landings de servicio | AIO citation eligibility |
| 1 | Auditar NAP en GBP, sitio, Doctoralia, Sección Amarilla → corregir variantes | Confianza de entidad |
| 1-2 | Setup Doctoralia con agenda (Reserve with Google) | Citas online + reseñas verificadas |
| 1-4 | Plan de reseñas: pedir post-cita via WhatsApp link a 12-15 pacientes/mes | Llegar a 70 reseñas en 90 días |
| 2 | Arreglar Core Web Vitals (LCP 4.2s → meta <2.5s). Lazy load, optimizar imágenes, defer JS no crítico | Ranking orgánico + Local Pack |
| 2-4 | Landing por servicio: blanqueamiento, ortodoncia, endodoncia, extracción muela del juicio. Cada una con FAQ schema. | Long-tail capture |
| 4 | Setup GBP Posts semanales (Oferta + Novedad alternados) | Engagement signal |
| 4 | Subir 8 fotos nuevas: consultorio, equipo, antes/después (con consentimiento) | CTR + retención |
| 8 | Apple Maps Connect, Waze, Sección Amarilla con NAP idéntico | Citaciones consistentes |
| 12 | Review métricas en GBP Insights + GSC. Ajustar curso. | Loop de mejora |

## Paso 9 — Métricas de éxito

- **Mes 3:** 70+ reseñas, rating 4.7+, aparece en Local Pack para 1-2 queries de marca + barrio
- **Mes 6:** 130+ reseñas, top 3 Local Pack para "dentista Roma Norte"
- **Mes 9:** 180+ reseñas, top 3 para "dentista cerca de mí" desde el barrio
- **Mes 12:** 220+ reseñas, citado en AI Overview para queries de procedimiento ("¿cuánto cuesta blanqueamiento dental CDMX?")

---

## Lo que NO hacemos

- ❌ Stuffing de colonias en title: "Dentista Roma, Condesa, Juárez, Cuauhtémoc, Polanco, Anzures..."
- ❌ Páginas idénticas por colonia con city swap. Cada landing tiene contenido único (testimonios del barrio, fotos, info local).
- ❌ Pedir reseñas a cambio de descuento (alto riesgo de eliminación por Google).
- ❌ Schema con datos placeholder (`+52 555 000 0000`) — Google los detecta como spam.
- ❌ Esperar a tener "el sitio perfecto" antes de empezar — GBP completo + reseñas + schema valen más que un rediseño.
