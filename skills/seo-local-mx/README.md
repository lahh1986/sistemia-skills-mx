# seo-local-mx

> Skill de Claude Code para subir un negocio físico mexicano en Google Maps, Local Pack y AI Overviews — sin gastar la tarde leyendo guías gringas que asumen Yelp, Yellowpages.com y "fontanero".

Parte de [El Tianguis](https://eltianguis.sistemia.mx) — catálogo abierto de skills de Claude Code para México y Latinoamérica.

---

## Qué hace

Le dices a Claude:

> "Soy dentista en Roma Norte, CDMX. Ya tengo Google Business Profile con 38 reseñas y 4.6 estrellas. No estoy en el Local Pack para 'dentista cerca de mí'. ¿Qué hago?"

Y te responde con:

- **Diagnóstico** del gap real (cuántas reseñas/mes te faltan según benchmark CDMX)
- **Schema LocalBusiness/Dentist JSON-LD** listo para pegar con tus datos
- **5-10 keywords prioritarias** con regionalismos MX (muelas del juicio, blanqueamiento, endodoncia, ortodoncia precio)
- **3-5 directorios prioritarios** del vertical (Doctoralia es #1 absoluto)
- **Plan de reseñas** con velocidad real para tu vertical+ciudad
- **FAQ schema** con preguntas en lenguaje natural de pacientes mexicanos
- **Próximos pasos en orden de impacto** (no lista neutral)

Cubre las decisiones que más rompen PyME y servicios mexicanos:

- **Google Business Profile** completo (categorías MX, atributos disponibles, posts, productos, servicios, Q&A, reservaciones via partners)
- **Schema LocalBusiness JSON-LD** completo (palanca #1 para AI Overviews en español MX)
- **AI Overviews / GEO** en es-MX — qué cambió, cómo aparecer citado
- **Reseñas** — benchmarks reales por vertical × tamaño de ciudad (metrópoli/media/pueblo)
- **Keywords con regionalismos**: tlapalería vs ferretería, refaccionaria vs autopartes, plomero vs fontanero, regularización vs tutoring, estética vs salón
- **Voice search es-MX**: cómo pregunta la gente en MX a Google Assistant/Siri/Alexa
- **Directorios MX que pesan en 2026**: Doctoralia, Sección Amarilla, Cylex, Waze, Inmuebles24, Bodas.com.mx, OpenTable, TripAdvisor — y los que ya no (OLX MX cerró clasificados)
- **Updates de algoritmo 2026** con impacto en local pack

---

## Por qué este skill existe

Las guías de SEO local en español traducen patrones gringos que en MX no aplican:

- "Yelp es obligatorio" → en MX, Yelp tiene tráfico directo bajo (importa solo porque alimenta Apple Maps)
- "Sigue la lista de Yext / Moz Local" → mitad son directorios sin tráfico real en MX
- "Optimiza para 'fontanero'" → en MX se busca "plomero" 10:1
- "Usa 'tutoring' o 'beauty salon'" → en MX se busca "regularización" o "estética"
- "Apunta a Yellowpages.com" → ni siquiera está en MX

Y a las particularidades de 2026:

- **Vivanuncios** fue absorbido por **Inmuebles24** (Navent)
- **OLX MX** cerró operaciones de clasificados y autos
- **Reserve with Google MX** solo via partners (TheFork, OpenTable, Doctoralia)
- **AI Overviews activo en es-MX** desde 2024-08, pleno en 2026
- **Updates 2026** castigan directorios genéricos, premian entidades reales con GBP completo
- **GEO** (Generative Engine Optimization) ya es término establecido en la comunidad SEO mexicana

Este skill consolida:

- Investigación al **2026-06-18** triangulada entre Gemini (long-context + Google docs), Grok (real-time + comunidad X), ChatGPT Deep Research (multi-fuente con citas)
- Patrones MX reales con regionalismos validados contra RAE/DEM/Asale
- Benchmarks de reseñas extrapolados de Local Falcon (50.4M resultados US Q4 2025) con multiplicadores por tamaño de ciudad MX
- Reglas operativas que distinguen Local Pack #1 vs Orgánico #1 debajo del pack vs Orgánico #1 sin pack (CTRs muy distintos)

---

## Instalación

```bash
# Copia el skill donde tu Claude Code lo lea
cp -r seo-local-mx/ ~/.claude/skills/seo-local-mx/
```

No hay setup. Es un skill de conocimiento — no ejecuta nada en tu máquina.

---

## Uso

Activa el skill mencionando cualquiera de estos triggers:

- "¿Cómo subo mi [vertical] en Google Maps en [ciudad]?"
- "¿Qué schema LocalBusiness uso para mi [vertical]?"
- "¿Cuántas reseñas necesito para Local Pack en [ciudad]?"
- "¿Cómo aparezco en AI Overviews para 'plomero cerca de mí'?"
- "¿Qué keywords reales busca la gente para [vertical] en MX?"
- "¿Doctoralia vs Sección Amarilla, cuál me da más?"
- "¿Cómo optimizo mi GBP de tlapalería?"
- "¿Qué FAQ debería poner en mi landing de mecánico?"

Claude te preguntará por tu vertical, ciudad/tamaño, GBP actual y problema concreto, y devolverá un plan accionable ordenado por palanca.

---

## Verticales cubiertos en v1.0

| Vertical | Categoría GBP principal | Schema type |
|---|---|---|
| Dentista / clínica dental | `dentist` | `Dentist` |
| Restaurante / taquería / comida a domicilio | `restaurant`, `taco_restaurant` | `Restaurant` |
| Plomero | `plumber` | `Plumber` |
| Estética / barbería | `beauty_salon` | `BeautySalon`, `HairSalon` |
| Taller mecánico | `mechanic` | `AutoRepair` |
| Clases particulares / regularización | `tutoring_service` | `EducationalOrganization` |
| Asesor inmobiliario / casa en venta | `real_estate_agency` | `RealEstateAgent` |
| Ferretería / tlapalería | `hardware_store` | `HardwareStore` |

Otros verticales se pueden cubrir extendiendo `data/keywords-mx.json` y `data/reviews-velocity-mx.json`.

---

## Estructura

```
seo-local-mx/
├── SKILL.md                       # Cuándo activarse + workflow paso-a-paso + reglas
├── README.md                      # Esto que estás leyendo
├── data/
│   ├── gbp-categorias-mx.json     # Categorías GBP por vertical + atributos MX
│   ├── gbp-features-mx.json       # 11 features GBP con límites
│   ├── directorios-mx.json        # 20 directorios MX con DA, NAP, reseñas
│   ├── ai-overviews-mx.json       # Comportamiento AIO es-MX + patrones citación
│   ├── algo-updates-mx.json       # Updates 2026 con impacto local MX
│   ├── comunidad-seo-mx.json      # 5 cuentas X + tools con tracción MX
│   ├── keywords-mx.json           # 8 verticales × keywords + regionalismos
│   ├── ctr-por-posicion-es.json   # Curvas CTR por superficie SERP
│   ├── reviews-velocity-mx.json   # 8 verticales × 3 tamaños de ciudad
│   └── voice-search-mx.json       # Patrones voice search por vertical
├── examples/
│   └── dentista-cdmx.md           # Caso end-to-end (dentista Roma Norte CDMX)
└── research/                       # Prompts originales + respuestas Gemini/Grok/ChatGPT
```

---

## Frescura

Datos verificados al `2026-06-18`. **Importante:**

- **AI Overviews y Local Pack** cambian seguido — revisa `algo-updates-mx.json` cada 90 días.
- **Categorías GBP** y atributos disponibles en MX se actualizan sin aviso — valida en https://support.google.com/business si dudas.
- **Volúmenes mensuales de keywords** NO están hardcodeados — conecta GKP/GSC/Ahrefs/Semrush con la taxonomía del skill como semilla.
- **Benchmarks de reseñas** están extrapolados de Local Falcon US (Q4 2025) con multiplicadores MX. Para reglas finas, exporta tu data de Local Falcon o BrightLocal por ciudad.

Si detectas un cambio, edita el JSON correspondiente y actualiza `_meta.captured_at`.

---

## Lo que NO hace

- No reemplaza a una agencia SEO ni a un consultor in-house
- No predice qué keyword va a "explotar" — usa GKP/Trends para eso
- No genera código de producción para deploy — da plantillas; los JSON-LD viven en respuestas del skill
- No cubre **Google Ads / Performance Max** — eso es paid, no orgánico
- No cubre **SEO técnico puro** (Core Web Vitals avanzado, JS rendering, hreflang inter-país) — para eso se construirá `seo-tecnico-mx`
- No cubre otros países LATAM (cada uno tendrá su skill: `seo-local-co`, `seo-local-pe`, etc.)
- No enseña black hat (PBN, link farms, comprar reseñas, scraping, GPT spam) — el skill explícitamente lo desincentiva
- No es asesor legal para LFPDPPP / datos personales — eso es scope de un futuro `legal-pyme-mx`

---

## Limitaciones de los datos

| Dato | Estado | Cómo cerrar el gap |
|---|---|---|
| Categorías GBP MX | v0.1 (10/40 verticales) | Ronda 2 con Gemini |
| Directorios MX | v0.1 (20/80) | Ronda 2 con Gemini con foco educación/automotriz/comercio/hiperlocal |
| Volúmenes mensuales keywords MX | No hardcodeado | Conectar GKP/Ahrefs/Semrush |
| CTR por posición es-MX | Extrapolado de global | Conectar GSC del usuario |
| Reviews velocity MX | Extrapolado de US (Local Falcon) | Exportar data Local Falcon/BrightLocal MX |
| Voice search corpus MX | No existe público | INEGI ENDUTIH 2024 + reglas globales como proxy |

Todos los gaps están marcados explícitamente en los JSON con `_meta` y flags como `extrapolado_de_us`, `no_encontré_data_pública_confiable`.

---

## Cómo aportar

Issues y PRs bienvenidos:

- https://github.com/lahh1986/sistemia-skills-mx/issues

Si trabajas un vertical no cubierto, o ves un benchmark que ya no cuadra, abre PR con un objeto siguiendo el shape de `data/reviews-velocity-mx.json` o `data/keywords-mx.json`.

---

## Licencia

MIT. Skill mantenido por [Sistemia](https://sistemia.mx).
