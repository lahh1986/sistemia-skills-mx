---
name: habitos-digitales-mx
description: |
  Usar cuando el usuario quiera saber qué CANAL/PLATAFORMA/DISPOSITIVO usa
  su target mexicano antes de gastar en ads o construir un funnel digital.
  Cubre penetración de internet, smartphone, redes sociales (Facebook,
  TikTok, YouTube, Instagram, LinkedIn, X, Pinterest, Snapchat), e-commerce
  y métodos de pago, segmentado por edad, sexo, urbano/rural y entidad.
  Fuentes: ENDUTIH 2024 INEGI + DataReportal Digital 2025 MX + AMVO 2025
  + ENIF 2024.

  Triggers: "qué red social usa mi target", "TikTok vs Instagram MX",
  "penetración smartphone en", "horas internet por edad MX", "audiencia
  Facebook México", "ENDUTIH", "DataReportal MX", "e-commerce México",
  "AMVO", "cómo paga online la gente", "compras online MX", "hábitos
  digitales", "elegir canal de ads MX".
---

# habitos-digitales-mx — Penetración digital y consumo de medios MX

> Wrapper sobre los datasets oficiales más recientes de comportamiento digital
> mexicano: **ENDUTIH 2024 INEGI** (100.2 M usuarios, n=65,000 viviendas),
> **DataReportal Digital 2025 Mexico** (audiencias por plataforma), **AMVO
> Estudio Venta Online 2024-2025** (e-commerce), **ENIF 2024 INEGI** (métodos
> de pago, bancarización).

## Cuándo activarte

- El usuario pregunta qué plataforma usar para llegar a su target
- El usuario quiere saber penetración smartphone/internet/redes en MX por segmento
- El usuario está armando un media plan y necesita audiencias reales
- El usuario quiere validar si su funnel funciona en zona rural (NO asumas online en D/E rural)
- El usuario menciona ENDUTIH, DataReportal, AMVO, hábitos digitales

## Snapshot México digital 2024-2025

### Población base
- **Total nacional:** 131 millones (DataReportal 2025)
- **Población 6+ (universo ENDUTIH):** 120.6 millones
- **Hogares:** 39.1 M total · 31.5 M urbano · 7.6 M rural

### Penetración internet (ENDUTIH 2024)
- **100.2 millones** usuarios = 83.1% de población 6+
- Urbano: **86.9%** · Rural: **68.5%** (brecha 18 pp persiste)
- Hombres: **84.1%** · Mujeres: **82.3%** (brecha 1.8 pp, históricamente cerrándose)
- Promedio uso: **4.4 horas/día**

### Penetración por edad (% usuarios internet · horas/día)
| Edad | % usuarios | Horas/día |
|---|---|---|
| 6-11 | 79.7% | 2.6 |
| 12-17 | 95.1% | 4.5 |
| **18-24** | **97.0%** | **5.7** |
| **25-34** | **95.1%** | **5.6** |
| 35-44 | 92.3% | 4.7 |
| 45-54 | 83.8% | 3.9 |
| 55-64 | 71.0% | 3.2 |
| 65+ | 42.1% | 3.0 |

### Dispositivos para conectarse (% de usuarios internet)
| Equipo | % |
|---|---|
| Celular inteligente | **97.2%** |
| Smart TV | 43.6% (↑5.8 pp vs 2023) |
| Computadora | 35.9% (↓8.1 pp vs 2023) |
| Consola videojuegos | 8.1% |

**Implicación:** mobile-first es ley. Email + landings deben ser mobile-perfect. Smart TV en alza para CTV ads. Desktop sigue cayendo.

### Lugar de acceso
- Hogar: 95.1% · Conexión móvil cualquier lugar: 56.8% · Casa de otra persona: 44.1% · Trabajo: 41.2% · Sitio público: 19.8% · Escuela: 16.5%

## Plataformas sociales (DataReportal Digital 2025 MX, ene 2025)

| Plataforma | Usuarios MX | % Población | F/M | Skew |
|---|---|---|---|---|
| **Facebook** | 93.0M | 70.7% | 51.8 / 48.2 | Balanceado, omnipresente |
| **TikTok** (18+) | 85.4M | 91.7% de 18+ | 43.6 / 56.4 | Slight male skew |
| **YouTube** | 83.6M | 63.6% | 51.2 / 48.8 | Balanceado |
| **Messenger** | 57.0M | 43.3% | 52.2 / 47.8 | Levemente femenino |
| **Instagram** | 48.8M | 37.1% | 53.5 / 46.5 | Femenino moderado |
| **Pinterest** | 26.7M | 20.3% | 67.2 / 26.2 | **Fuerte femenino** |
| **LinkedIn** | 26.0M | 19.8% | 44.0 / 56.0 | Profesional, slight male |
| **X (Twitter)** | 16.9M | 12.8% | 33.6 / 66.4 | **Fuerte masculino** |
| **Snapchat** | 15.1M | 11.5% | 73.9 / 25.0 | **Muy femenino joven** |

### Crecimiento ene 2024 → ene 2025
- TikTok: +11.2M (+15.1%) ← más rápido
- LinkedIn: +4.0M (+18.2%)
- Instagram: +3.9M (+8.7%)
- Pinterest: +2.64M (+11.0%)
- WhatsApp y Facebook ya saturados, crecen marginal

## Workflow

### Paso 1: Identifica target y canales candidatos

Pregunta al usuario:
1. **Quién es tu target** (edad, sexo, NSE si lo sabe, urbano/rural)
2. **Qué busca lograr** (awareness, lead-gen, venta directa, app installs, contenido orgánico)
3. **Geografía** (nacional, estatal, ciudad específica)

Si el usuario no sabe, usa el skill `focus-group-mx` para validar perfil primero.

### Paso 2: Calcula audiencia alcanzable

Usa la tabla de plataformas × la composición demográfica. Combina con `demografia-mx` para ajustar por estado.

Ejemplo:
- **Target: Mujeres 25-34 NSE C+ en CDMX**
- Audiencia base demografia-mx: ~800K mujeres 25-34 en CDMX
- Penetración internet 25-34: 95.1% → 760K
- NSE C+: 16% del estado → **~120K alcanzables online**
- TikTok en este segmento: ~75% de internautas = ~90K
- Instagram: ~60% = ~72K

### Paso 3: Recomienda mix de canales por objetivo

| Objetivo | Mix recomendado MX |
|---|---|
| **Awareness mass** | Facebook + YouTube + TikTok (alcance combinado >90% adultos urbanos) |
| **B2C joven 18-30** | TikTok (#1) + Instagram + YouTube Shorts |
| **B2C mujer 30-50** | Facebook + Instagram + Pinterest (compras hogar/moda) |
| **B2C hombre 18-45** | TikTok + YouTube + X (gaming/tech/deportes) |
| **B2B / contratación** | LinkedIn + Facebook (siguen funcionando en MX para empleo) |
| **Lead-gen WhatsApp** | Meta Ads (FB+IG) con Click-to-WhatsApp + landing simple |
| **Venta directa e-commerce** | Meta Ads + Google Shopping + TikTok Shop (creciendo) |
| **Audiencia 50+** | Facebook + WhatsApp + YouTube TV (NO TikTok) |
| **Audiencia rural** | Facebook + WhatsApp + radio AM/FM tradicional. NO asumas Instagram/TikTok obvio |

### Paso 4: Avisa los gaps

Siempre cierra con:
- **21.9 M mexicanos están offline** (16.7% de la población). NO son tu target digital. Para ellos: TV abierta, radio, OOH, volantes.
- En **rural, brecha digital del 31.5%** (vs 13.1% urbano). Para producto rural-relevant, mezcla canales offline.
- Para **65+, solo 42% usa internet** y muchos solo WhatsApp. NO asumas Instagram/TikTok funcional.

### Paso 5: Output al usuario

```markdown
## Plan de canales digitales — {{target}}

### Audiencia alcanzable
- Total target demográfico: {{N}}
- Penetrados online: {{N}} ({{%}})
- En tu plataforma top recomendada: {{N}}

### Mix recomendado
| Plataforma | Por qué | % de presupuesto sugerido |
| TikTok | Tu target es 25-34 mujer, plataforma #2 en penetración y la que más crece | 35-45% |
| ... |

### Consideraciones
- {{Sesgo género de la plataforma vs tu target}}
- {{Horas de uso = ventana de exposición posible}}
- {{Crecimiento de la plataforma vs estancamiento}}

### Lo que NO funciona para tu caso
- {{Plataforma X — razón}}
```

## E-commerce y pagos (AMVO 2025 + ENIF 2024)

Para casos de venta online directa, consulta estos datos rápidos:

### Compras online MX (AMVO 2025)
- **77% de mexicanos urbanos** compraron online al menos 1× en 2024
- Top categorías: **moda · electrónica · hogar · belleza · viajes**
- Frecuencia: ~5 compras/trimestre en compradores activos
- Ticket promedio: $850-1,200 MXN
- Buen Fin (noviembre) concentra ~22% del año en muchas verticales

### Métodos de pago online
- **Tarjeta de crédito:** 41%
- **Tarjeta de débito:** 35%
- **Efectivo en tiendas (OXXO Pay, 7-Eleven):** 22% ← exclusivamente MX
- **Transferencia SPEI:** 18% (creciendo fuerte con CoDi)
- **Apple/Google Pay:** 9%
- **MSI (meses sin intereses):** 32% en compras > $2,000 MXN

**Implicación:** SIEMPRE incluye OXXO Pay como opción si vendes a NSE D+/C-. SIEMPRE MSI si ticket > $2K MXN. SPEI/CoDi suben de share rápido.

### Bancarización (ENIF 2024)
- **49.1% de adultos** tienen cuenta bancaria
- Tarjeta crédito: **31.8%**
- Tarjeta débito: **45.6%**
- Las **mujeres están 4 pp abajo** que hombres en cuenta bancaria
- Estados con menor bancarización: Chiapas, Oaxaca, Tlaxcala, Guerrero
- Estados con mayor: NL, BCS, CDMX, Querétaro

## Cheat sheet — "¿en qué plataforma están?"

| Si tu target es… | Plataforma #1 | Por qué |
|---|---|---|
| Adolescentes 12-17 | TikTok | 95% penetración 12-17 + ola TikTok |
| Universitarios 18-24 | TikTok / Instagram | 97% online, 5.7h/día, alta concentración |
| Mujeres 25-34 NSE C+ | Instagram + TikTok | sesgo femenino + alto poder adquisitivo |
| Madres 30-50 | Facebook + Pinterest | grupos de madres + recetas/hogar |
| Profesionistas 25-50 | LinkedIn + Instagram | networking + lifestyle |
| Hombres 25-45 deportes/gaming | YouTube + X + TikTok | YouTube por contenido largo, X para deporte en vivo |
| Adultos 45+ | Facebook + WhatsApp | siguen siendo dominantes en este grupo |
| 65+ | WhatsApp (familia) + TV abierta | internet solo 42%, foco en lo que ya usan |
| Rural | Facebook + WhatsApp | infraestructura limitada, plataformas más establecidas |

## Lo que NO hace este skill

- **No reemplaza un estudio de mercado primario.** Es síntesis de fuentes públicas.
- **No tiene audiencias hyperlocal** (colonia, AGEB). Va a estado máximo.
- **No conoce tu CPM/CPL real.** Para eso necesitas estimaciones de Meta/Google Ads Manager.
- **No incluye comportamientos B2B granulares.** LinkedIn data es general MX.

## Fuentes

- **ENDUTIH 2024** INEGI (mayo 2025) · `research/inegi/endutih/endutih2024_boletin_resultados.pdf` + microdatos
- **DataReportal Digital 2025 Mexico** · `research/datareportal/datareportal_digital_2025_mexico_resumen.md`
- **AMVO Estudio Venta Online 2024 + 2025** · `research/amvo/`
- **ENIF 2024** INEGI · `research/inegi/enif/enif2024_reporte_completo.pdf`
- **AIMX 20 Hábitos Internet 2024** · `research/aimx/`
- **IFT Primera/Segunda Encuesta 2024** · `research/ift/` (brechas digitales, accesibilidad)
