---
name: seo-local-mx
description: |
  Usar cuando el usuario quiera mejorar el SEO local de un negocio físico en
  México: clínica dental, restaurante, plomero, taller mecánico, estética,
  asesor inmobiliario, ferretería/tlapalería, clases particulares. Cubre los
  patrones reales de cómo busca la gente en México (regionalismos validados:
  tlapalería, refaccionaria, regularización, plomero vs fontanero), las
  categorías y features de Google Business Profile disponibles en MX, los 20+
  directorios que mueven aguja (Doctoralia, Sección Amarilla, Inmuebles24,
  Waze, Apple Maps, etc.), benchmarks de reseñas por vertical + tamaño de
  ciudad, comportamiento de AI Overviews en español MX y patrones de Schema
  LocalBusiness JSON-LD para ser citado en AIO. Devuelve un plan accionable
  ordenado por palanca, no una lista neutral.

  Triggers: "cómo rankear en Google Maps", "SEO local México", "Google Business
  Profile dentista/plomero/restaurante", "schema LocalBusiness", "Local Pack
  México", "AI Overviews SEO", "GEO en español", "reseñas Google velocidad",
  "directorios citaciones MX", "NAP consistencia", "tlapalería keyword",
  "ferretería SEO", "cerca de mí mexicano", "Doctoralia ranking", "Sección
  Amarilla SEO", "Waze para negocios", "Apple Maps México", "Reserve with
  Google MX", "Inmuebles24 vs Properati", "Bodas.com.mx".
---

# seo-local-mx — SEO local para negocios mexicanos (GBP, AIO, schema, reseñas)

> Wrapper de Claude Code que conoce las palancas reales del SEO local en
> México 2026: cómo se comporta el Local Pack vs AI Overviews en español MX,
> qué directorios pesan, cuántas reseñas/mes necesita cada vertical en cada
> tamaño de ciudad, y cómo aprovechar regionalismos (tlapalería, refaccionaria,
> regularización) que los tools gringos pierden.

**Fuente de verdad** (todo en `data/`):

| Archivo | Qué contiene |
|---|---|
| `gbp-categorias-mx.json` | Categorías GBP por vertical + atributos disponibles en MX |
| `gbp-features-mx.json` | 11 features GBP con límites, frecuencia y impacto SEO |
| `directorios-mx.json` | 20 directorios MX (general + vertical) con DA, NAP, reseñas |
| `ai-overviews-mx.json` | Comportamiento AIO en es-MX + 6 patrones para ser citado |
| `algo-updates-mx.json` | 4 updates 2026 con impacto en local pack MX |
| `comunidad-seo-mx.json` | 5 cuentas X + temas calientes + tools con tracción MX |
| `keywords-mx.json` | 8 verticales × head terms, modificadores, long tail, regionalismos |
| `ctr-por-posicion-es.json` | 3 curvas operativas (mobile/desktop, con/sin pack) |
| `reviews-velocity-mx.json` | 8 verticales × 3 tamaños de ciudad |
| `voice-search-mx.json` | 8 verticales × patrón voice vs text + FAQ |

**Frescura:** datos verificados al `2026-06-18`. Los updates de Google y AIO
cambian rápido — revalida contra `algo-updates-mx.json` cada 90 días.

---

## Cuándo activarte

- El usuario tiene un **negocio físico en México** y quiere aparecer en Maps / Local Pack / AI Overview
- El usuario pregunta cómo optimizar **Google Business Profile** (categorías, atributos, posts, productos, servicios, reseñas)
- El usuario pregunta por **Schema LocalBusiness JSON-LD** o subtipos (Dentist, Plumber, AutoRepair, RealEstateAgent, etc.)
- El usuario pregunta por **AI Overviews / SGE / GEO en español MX** o cómo ser citado
- El usuario quiere armar estrategia de **reseñas Google** (volumen, velocidad, respuestas)
- El usuario pregunta por **directorios y citaciones** mexicanos (Doctoralia, Sección Amarilla, Cylex, Waze, Apple Maps, Bodas.com.mx, etc.)
- El usuario quiere **keywords reales** por vertical en MX con regionalismos
- El usuario quiere armar **landing local por ciudad/colonia** para servicios
- El usuario menciona **NAP, hreflang es-MX, Core Web Vitals** en contexto local

**NO actives si:**

- El usuario es 100% **e-commerce sin tienda física** — eso es SEO general/producto, no local
- El usuario pregunta por **SEO técnico puro** sin componente local (eso es scope de un futuro skill `seo-tecnico-mx`)
- El usuario pregunta por **Google Ads / Performance Max** — no es SEO local
- El usuario está en **otro país LATAM** — referir al skill `seo-local-{cc}` correspondiente (todavía no existe; advertirlo)
- El usuario pregunta por **link building agresivo / PBN / link farms** — el skill no enseña black hat

---

## Workflow

### Paso 1 — Diagnóstico del caso

Antes de recomendar, pregunta y registra:

| Variable | Pregunta | Por qué importa |
|---|---|---|
| **Vertical** | ¿Qué tipo de negocio? ¿Dentista, plomero, restaurante, taller, estética, asesor inmobiliario, ferretería, clases particulares? | Define categoría GBP, schema type, benchmarks de reseñas y keywords |
| **Tamaño de ciudad** | ¿Metrópoli (CDMX/GDL/MTY), ciudad media (300k-1M) o pueblo (<300k)? | Cambia el benchmark de reseñas ~2x entre metro y pueblo |
| **Ciudad/colonia** | ¿Dónde físicamente? | Permite armar landing por colonia + recomendar directorios hiperlocales |
| **GBP actual** | ¿Ya tienes Google Business Profile? ¿Verificado? ¿Cuántas reseñas y rating? | Define si arrancamos de cero o auditamos lo que hay |
| **Sitio web** | ¿Tiene? ¿Schema LocalBusiness ya implementado? ¿Core Web Vitals? | Define qué se puede mover en sitio vs solo GBP |
| **Competencia local** | ¿Conoces tus 3 competidores top en Maps? ¿Cuántas reseñas tienen? | Define gap a cerrar — competir (P10) vs dominar (P50) |
| **Problema concreto** | ¿No aparece en Maps? ¿Aparece pero no recibe llamadas? ¿Cae en Local Pack? | Cambia el orden del workflow |

Si el usuario no aporta esta info, **pregúntale antes de recomendar**. Una recomendación sin estos datos es ruido (un dentista en CDMX necesita 12-18 reseñas/mes; en pueblo, 3-6).

### Paso 2 — Carga los datos relevantes

Lee solo los archivos JSON que aplican al caso:

- Siempre: `gbp-categorias-mx.json`, `gbp-features-mx.json`, `keywords-mx.json`
- Si pregunta por AIO/GEO: `ai-overviews-mx.json`
- Si planea reseñas: `reviews-velocity-mx.json`
- Si pregunta por directorios: `directorios-mx.json`
- Si pregunta por voice/FAQ: `voice-search-mx.json`
- Si pregunta por updates recientes: `algo-updates-mx.json`
- Si pregunta por tools/comunidad: `comunidad-seo-mx.json`
- Si pregunta por CTR/proyecciones de tráfico: `ctr-por-posicion-es.json`

### Paso 3 — Diagnostica el GBP (palanca #1)

Audita en orden:

1. **Categoría principal** correcta del `gbp-categorias-mx.json`. La categoría primaria pesa más que las secundarias.
2. **NAP consistente** entre GBP, sitio web, y los directorios principales (Doctoralia, Sección Amarilla, Apple Maps, Waze). Tolerancia: cero variantes.
3. **Atributos disponibles MX** marcados (acepta pacientes nuevos, cita previa, accesible, etc.). Los atributos US no existen en MX — no los esperes.
4. **Servicios** descritos con palabras clave reales (cargados del `keywords-mx.json` del vertical).
5. **Fotos**: logo, portada, interior, exterior, equipo. Mensual nuevo.
6. **Posts** semanales (Oferta/Evento/Novedad).
7. **Q&A sembradas** por el dueño respondiendo preguntas reales de clientes.
8. **Reseñas**: rating ≥ 4.5, velocidad por vertical+ciudad de `reviews-velocity-mx.json`, respuesta a todas en <48 horas.
9. **Productos/Servicios** con descripciones largas (las palabras clave aquí indexan en Local Pack como justificaciones "Ofrece: X").
10. **Reservaciones**: si aplica (restaurante, salud, belleza), enlazar partner: TheFork, OpenTable, Doctoralia.

### Paso 4 — Schema LocalBusiness JSON-LD (palanca #1 para AIO)

De `ai-overviews-mx.json`, el patrón #1 para ser citado en AI Overviews es Schema completo. Implementa **todas** estas propiedades en el sitio:

- `@type`: subtipo específico (`Dentist`, `Restaurant`, `Plumber`, `AutoRepair`, `RealEstateAgent`, `BeautySalon`, `HardwareStore`, `EducationalOrganization`)
- `name`, `image`, `url`, `telephone` (formato E.164: `+52...`)
- `address` (PostalAddress completo: streetAddress, addressLocality, addressRegion, postalCode, addressCountry: "MX")
- `geo` (GeoCoordinates: latitude, longitude)
- `openingHoursSpecification` (array por día)
- `areaServed` (ciudades/colonias atendidas)
- `sameAs` (perfiles sociales + GBP + directorios principales)
- `priceRange` (`$`, `$$`, `$$$`)
- `aggregateRating` + `review` (importar de GBP via integración)
- `hasMap` (link a Google Maps)

### Paso 5 — Estrategia de keywords con regionalismos

Carga el vertical de `keywords-mx.json`. Tres reglas:

1. **Head term MX, no traducción de inglés**: "plomero" (no "fontanero"), "estética" (no "salón de belleza" como primario), "dentista" (no "odontólogo" como primario).
2. **Regionalismos como aliases semánticos**, no traducciones: si el negocio está en centro de MX, usa **tlapalería** además de ferretería. Si vende refacciones, **refaccionaria**. Si da clases de regularización, no traduzcas a "tutoring".
3. **Modificadores calientes** por vertical: `cerca de mí`, `precio`, `24 horas`, `a domicilio`, `abierto ahora`, `domingo`, modificador problem-specific (fuga de agua, cambio de aceite, sin dolor).

**Nunca hardcodees volumen mensual.** El skill marca todos los volúmenes como `no_encontré_data_pública_confiable`. Conecta GKP/GSC/Ahrefs/Semrush con la taxonomía como semilla.

### Paso 6 — Plan de contenido / FAQPage (voice + AIO)

De `voice-search-mx.json` y `ai-overviews-mx.json`:

- **FAQPage schema** en página principal y landings de servicio. Preguntas en lenguaje natural es-MX: "¿Atienden urgencias dentales hoy?", "¿Cuánto tarda un cambio de aceite?", "¿Cómo comprar casa con crédito Infonavit?"
- **Respuestas en 40-60 palabras**, con servicio + zona + horario + siguiente acción.
- **Landing por colonia/zona** si el negocio sirve varias áreas. No spam de páginas idénticas con city swap — cada landing debe tener contenido único (testimonios locales, fotos del lugar, info del barrio).
- **HowTo schema** para procedimientos comunes ("Cómo agendar cita de blanqueamiento", "Cómo preparar tu auto para afinación").

### Paso 7 — Plan de reseñas (velocidad real, no spam)

De `reviews-velocity-mx.json`, identifica el bucket (vertical × tamaño de ciudad) y aplica:

| Métrica | Cómo usar |
|---|---|
| `reseñas_promedio_top3_local_pack` | Meta de largo plazo para dominar |
| `reseñas_minimas_competir` | Umbral mínimo para que Google considere al perfil |
| `velocidad_recomendada` | Reseñas nuevas/mes — **no excedas**, los picos artificiales son riesgo |
| `rating_promedio_top3` | Rating mínimo a mantener (típicamente 4.5-4.8) |

**Reglas:**
- **No incentives reseñas** (Google las elimina y puede suspender GBP).
- **Pide en momentos naturales** del servicio (post-cita, post-entrega).
- **Responde TODAS** en <48 horas, incluso las de 5 estrellas.
- **Sin reseñas negativas no respondidas** — eso pesa más que tres positivas adicionales.

### Paso 8 — Citaciones / directorios

De `directorios-mx.json`, prioriza en este orden:

1. **Obligatorios (DA ≥ 90)**: GBP, Apple Maps Connect, Bing Places, Waze, Facebook Pages, Instagram Business
2. **Vertical fuerte**: el directorio dominante del vertical (Doctoralia para salud, TripAdvisor/OpenTable para restaurantes, Inmuebles24 para inmuebles, Bodas.com.mx para eventos/belleza)
3. **Tradicionales MX**: Sección Amarilla, Páginas Amarillas, Cylex MX, GuiaMexico
4. **Agregadores que alimentan otros**: Yelp MX (alimenta Apple Maps), Foursquare (alimenta Uber, Twitter)

**No hagas list-building masivo en directorios débiles.** Los updates 2026 (`algo-updates-mx.json`) castigan directorios genéricos. Mejor 15 citaciones consistentes que 80 incompletas.

### Paso 9 — Monitoreo

- **GBP Insights** (mensual): búsquedas que llegaron al perfil, llamadas, mensajes, clics a web/direcciones
- **GSC**: queries con impresiones + posición. Filtra por queries con intención local ("cerca de mí", ciudad, colonia)
- **Local Falcon / Whitespark / BrightLocal**: ranking en Local Pack por grid de ubicación (no solo "posición 1" — la posición varía por punto del mapa)
- **AIO citations**: monitorear manualmente queries clave (no hay tool sólido aún) para ver si el negocio es citado

---

## Reglas operativas (resumen)

### Triada de superficie SERP — el skill SIEMPRE distingue

Nunca digas "posición 1" sin especificar:

- **Local Pack #1** (el primero de los 3 negocios en el mapa)
- **Orgánico #1 debajo del pack** (CTR muy distinto: ~14% mobile vs ~30% sin pack)
- **Orgánico #1 sin pack** (CTR alto, ~30% mobile)

De `ctr-por-posicion-es.json` curvas:
- Mobile sin pack: pos 1 = 30%, pos 3 = 9%, pos 10 = 1.4%
- Mobile con pack: Local Pack 1 = 18%, orgánico 1 debajo = 14%, orgánico 3 debajo = 6%

### Competir vs dominar

- **Competir** = alcanzar **P10** del benchmark de reseñas + rating ≥ 4.5
- **Dominar** = acercarse a **P50** (mediana) del Local 3-Pack + reseñas nuevas todos los meses

### Lo que cambió en 2026 (de `algo-updates-mx.json`)

- AIO activo en MX desde 2024-08, pleno en 2026
- Updates 2026 castigan directorios genéricos, premian entidades reales
- GBP con AI summary propio aparece (jun 2026)
- "GEO" (Generative Engine Optimization) ya es término establecido

### Anti-patterns que el skill NO recomienda

- ❌ Stuffing de ciudades en title tags ("Dentista CDMX, Polanco, Roma, Condesa, Anzures...")
- ❌ Páginas idénticas con city swap (Google penaliza thin content)
- ❌ Comprar reseñas o incentivarlas (alto riesgo de suspensión GBP)
- ❌ List-building en 80 directorios débiles (post-updates 2026 ya no funciona)
- ❌ Schema LocalBusiness incompleto (sin geo, sin openingHoursSpecification) — no se cita en AIO
- ❌ Decir "fontanero" en sitio MX (es España; usa "plomero")
- ❌ Traducir regionalismos: si la gente busca "tlapalería" o "regularización", no escribas "hardware store" ni "tutoring"
- ❌ Recomendar Twilio Reviews API o herramientas que ya no operan en MX

---

## Output esperado del skill

Cuando alguien pregunta "cómo rankeo mi dentista en CDMX", el skill devuelve:

1. **Diagnóstico** (3-5 preguntas concretas si faltan datos)
2. **Plan accionable ordenado por palanca** (GBP → schema → keywords → reseñas → contenido → directorios → monitoreo)
3. **Benchmarks específicos** del vertical+ciudad ("Necesitas 12-18 reseñas/mes con rating ≥ 4.7 para competir en Local Pack en CDMX")
4. **Schema JSON-LD listo para pegar** con datos del usuario
5. **5-10 keywords prioritarias** con regionalismos del vertical
6. **3-5 directorios prioritarios** del vertical
7. **Próximos pasos en orden de impacto**

Ver `examples/dentista-cdmx.md` para un caso end-to-end.
