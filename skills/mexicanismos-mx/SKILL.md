---
name: mexicanismos-mx
description: |
  Usar cuando el usuario quiera REVISAR, GENERAR o ADAPTAR texto en español
  mexicano por región (Centro/CDMX, Norte/Regio, Frontera/Noroeste, Bajío,
  Occidente/Tapatío, Sur-Sureste costa, Yucatán), por generación (Boomer/X/
  Millennial/Z), por nivel socioeconómico (NSE A/B/C/D/E) y por registro
  (formal corporativo, semi-formal, coloquial, familiar, callejero, redes).
  Detecta modismos, falsos amigos internos (palabras que cambian de significado
  por región), riesgos de carga clasista/racial, y slang Gen Z 2026 con vida
  útil corta. Va más profundo que `locale-mx`: no es solo "tú/ustedes",
  es decidir si tu copy regio "está con madre" o "padrísimo" para tu target.

  Triggers: "este copy suena gringo traducido", "adapta este texto para
  Monterrey", "no quiero que suene fresa", "modismos por región", "qué dicen
  los regios", "yucateco real sin caricatura", "slang Gen Z mexicano",
  "evitar clasismo en mi anuncio", "español de México auténtico", "palabras
  que cambian significado en México", "falsos amigos mexicanos", "chamba vs
  jale", "padre vs chido vs con madre", "diccionario mexicanismos",
  "regionalismos México", "expresiones típicas mexicanas".
---

# mexicanismos-mx — Español de México por región, edad, clase y registro

> Wrapper editorial sobre 110 mexicanismos curados + 7 zonas dialectales + 50
> falsos amigos internos + guía de carga clasista/racial + 25 entries de slang
> Gen Z 2026. Sirve para decidir QUÉ palabras usar para QUÉ audiencia mexicana
> sin que tu copy suene chilango por default, gringo traducido o caricatura.

**Fuente de verdad:**
- `data/regiones.json` — 7 zonas dialectales (Lope Blanch adaptado + Yucatán separado) con carácter léxico y casos multi-zona
- `data/mexicanismos.json` — 110 palabras con scoring por región/registro/generación + link a DEM cuando aplica
- `data/falsos_amigos.json` — palabras que cambian significado intra-MX y entre MX/Latam (chichí, chaqueta, popote, concha, coger, etc.)
- `data/registro_clasismo.json` — guía editorial sobre palabras con carga social (clase, raza, género, regional, ideológica)
- `data/genz_2026.json` — slang juvenil 2025-2026 con `decay_risk` y `last_validated` — REVISAR cada 12 meses

**Frescura:** datos al `2026-06-10`. El slang Gen Z decae rápido — el bloque `genz_2026.json` necesita revalidación anual.

---

## Frontera con `locale-mx` (importante)

`locale-mx` ya existe y cubre **reglas duras** de español MX:
- Tú/ustedes (no vosotros, no vos)
- "Computadora" no "ordenador", "carro" no "coche", "checar" no "comprobar"
- Nada de "vale", "tío", "ordenador", "follar", "joder"

**`mexicanismos-mx` opera UN NIVEL MÁS PROFUNDO**: dada la regla "es español MX", elige QUÉ palabra MX según target. No reemplaza `locale-mx`, lo complementa.

**Heurística:** si el usuario pregunta "esto suena gringo o español de España", es `locale-mx`. Si pregunta "esto suena chilango pero mi cliente es regio", es `mexicanismos-mx`.

---

## Cuándo activarte

- El usuario quiere REVISAR copy MX y saber si suena natural para una audiencia específica
- El usuario quiere GENERAR copy MX con flavor regional (regio, tapatío, yucateco, costeño)
- El usuario teme caer en clasismo accidental o caricatura regional
- El usuario pregunta el significado de un mexicanismo o si suena igual en otra zona
- El usuario pregunta por slang Gen Z mexicano actual
- El usuario tiene un texto que "suena gringo traducido" y quiere arreglar
- El usuario tiene texto que "suena chilango" y necesita adaptar a provincia o frontera
- El usuario menciona "español mexicano", "modismos", "regionalismos", "jerga", "slang MX"

**NO actives si:**
- El usuario pide reglas BÁSICAS de español MX (tú/ustedes) → eso es `locale-mx`
- El usuario pide validar copy con personas sintéticas → eso es `focus-group-mx`
- El usuario quiere escribir en otro español (España, Argentina, Colombia) → no es este skill
- El usuario quiere asesoría lingüística académica formal → ni este ni ningún skill — ir a DEM/Colmex directo

---

## Workflow

### Paso 1 — Diagnóstico del target

Antes de recomendar palabras, identificá:

| Variable | Pregunta a hacer | Por qué importa |
|---|---|---|
| **Región del target** | ¿CDMX/centro? ¿Monterrey/regio? ¿GDL/tapatío? ¿Yucatán? ¿Frontera (TJ/Mexicali/CDJ)? ¿Sur-sureste (Veracruz, Oaxaca, Chiapas)? ¿Bajío? | "Está chido" funciona nacional. "Está con madre" suena regio. "Está padre" suena chilango. Para regio decir "padre" puede sonar distante o ñoño. |
| **Generación** | ¿Boomer (60+)? ¿X (45-59)? ¿Millennial (30-44)? ¿Z (15-29)? ¿Alfa (<15)? | "Fierro pariente" suena retro. "Estoy delulu" suena Gen Z. "Godín" suena millennial. Slang juvenil decae cada 12-18 meses. |
| **NSE** | ¿A/B+ urbano? ¿C urbano? ¿D/E periferia/rural? | "Aesthetic" suena A/B Polanco. "Está con madre" cruza clases. "Mande" puede leerse sumiso en NSE A/B Gen Z urbana. |
| **Registro** | ¿Formal corporativo? ¿Semi-formal B2B? ¿Coloquial brand? ¿Familiar/redes sociales? | Lo que suena "auténtico" en redes puede sonar grosero en B2B. "Wey" en hero de landing = error. |
| **Geografía multi-zona** | ¿Tu target es bicultural (regio en CDMX, chilango con padres yucatecos)? | `regiones.json.casos_multi_zona` tiene patrones. Léxico mixto, NO una sola etiqueta. |

Si el usuario no da esta info, **preguntale antes de recomendar**. Por defecto, un copy "MX" sin target = chilango neutral, lo cual aliena al 60% del país sin que el creador se dé cuenta.

### Paso 2 — Cargá los datos relevantes

Leé sólo lo que aplica al target. NO pegues archivos completos al usuario.

- Para revisar copy: cargá `mexicanismos.json` filtrado por las regiones del target + `falsos_amigos.json` para flag de errores intra-MX + `registro_clasismo.json` si el copy toca temas sensibles.
- Para generar copy: cargá `regiones.json` (zona del target) + `mexicanismos.json` filtrado.
- Para slang Gen Z: cargá `genz_2026.json` con flag de `last_validated` — si más de 12 meses, advertir.

### Paso 3 — Aplicá el árbol de decisión

```
¿El input es texto a REVISAR o tarea para GENERAR?
├── REVISAR copy existente
│   ├── ¿Suena gringo traducido?
│   │   └── Identificá calcos del inglés y proponé MX-natural (ej: "agarrar" no "tomar la oportunidad")
│   ├── ¿Suena chilango pero target es no-CDMX?
│   │   └── Sustituí marcadores chilangos por marcadores del target (ej: padre → con madre para regio)
│   ├── ¿Contiene palabras con carga clasista/racial?
│   │   └── Flag con `registro_clasismo.json` y proponé alternativa
│   ├── ¿Contiene falsos amigos peligrosos?
│   │   └── Flag `chaqueta` para CDMX, `chichí` cross-MX, `coger` cross-Latam
│   └── ¿Slang Gen Z presente?
│       └── Verificá last_validated; si >12 meses, advertir caducidad
│
├── GENERAR copy nuevo
│   ├── Identificá zona + edad + NSE + registro
│   ├── Cargá mexicanismos.json filtrado
│   ├── Elegí 2-3 marcadores regionales SIN saturar (saturar = caricatura)
│   ├── Mantené registro consistente (no mezclar formal con callejero)
│   ├── Validá contra falsos_amigos.json y registro_clasismo.json
│   └── Sugerí 2-3 variantes para que el usuario pruebe
│
└── EXPLICAR un mexicanismo
    ├── Buscá en mexicanismos.json
    ├── Si falla, sugerí buscar en DEM (link)
    └── Marcá si es nacional, regional, o cargado socialmente
```

### Paso 4 — Output recomendado

Estructura del output al usuario:

```markdown
## Análisis para audiencia {{región}} · {{generación}} · {{NSE}} · {{registro}}

### Veredicto rápido
{{Funciona / Funciona parcialmente / No funciona / Riesgo}}

### Hallazgos línea por línea
| Texto original | Problema | Sugerencia |
| "..." | Suena chilango (target regio) | "..." |
| "..." | Falso amigo riesgoso | "..." |
| "..." | Carga clasista accidental | "..." |
| "..." | Slang Gen Z caducado | "..." |

### Versiones alternativas (top 3)
1. **Más natural para {{región}}**: "..."
2. **Más segura cross-MX**: "..."
3. **Si querés saturar marca regional** (con riesgo de caricatura): "..."

### Cosas a NO usar para este target
- "{{palabra}}" — {{razón}}
- "{{palabra}}" — {{razón}}

### Anclas
- {{término relevante}}: ver DEM https://dem.colmex.mx/Ver/{{término}}
- (Cuando aplica) Diccionario de Mexicanismos AML (2da ed. 2022) tiene entrada.
```

### Paso 5 — Citá DEM/AML como ORACLE, no como fuente

**Crítico de licencia**: el Diccionario del Español de México (DEM) de El Colegio de México es CC BY-NC-ND. **NO podemos shipear sus glosas en este skill** — las definiciones en `mexicanismos.json` son CURADAS POR SISTEMIA. Si el usuario pide la definición "oficial":

> "La definición que doy es curaduría editorial nuestra. Para la entrada autorizada, ver DEM: https://dem.colmex.mx/Ver/{{término}}. El Diccionario de Mexicanismos de la AML (2da ed. 2022) también tiene una entrada — disponible en libro físico/ebook."

Esto NO es disclaimer legal — es transparencia editorial. La calidad académica de DEM > la nuestra. Si el usuario necesita citation académica, mandamos a DEM.

### Paso 6 — Advertí caducidad del slang Gen Z

Cualquier entrada de `genz_2026.json` con `decay_risk: alto` y/o `last_validated > 12 meses` tiene vida útil corta. **Siempre incluir disclaimer**:

> "El slang Gen Z 2025-2026 que mencioné tiene vida útil ~12 meses. Validar antes de imprimir o lanzar campaña. Si tu copy es brand de largo plazo (>1 año), preferí registros más estables (coloquial nacional sin slang juvenil saturado)."

---

## Errores comunes a evitar (modo agente)

1. **Saturar marcadores regionales** — meter 10 mexicanismos regio en un párrafo de 50 palabras es caricatura, no autenticidad. 2-3 marcadores bien colocados es lo correcto.

2. **Asumir "MX = CDMX"** — el centro produce la mayoría del contenido nacional, lo cual genera ceguera regional. Sin target específico, "MX" no es "chilango".

3. **Confundir generación con NSE** — un boomer regio working-class habla DISTINTO a un Gen Z chilango fresa. Cada eje es independiente.

4. **Caer en clasismo accidental** — usar "no manches" en formal corporativo, decir "elote desgranado" como si fuera vulgar (es regio), aplicar "godín" a alguien que no se auto-define así.

5. **Decir "es lo mismo" cuando no lo es** — bolillo ≠ birote en GDL. Esquites ≠ elote desgranado en MTY. Esos detalles los detecta cualquier local.

6. **Trotar slang Gen Z como si fuera estable** — "estoy en mi era de X" caduca rápido. "Padre/chido" es estable. Distinguir.

7. **Tratar Yucatán como folklor** — "mare", "bomba", "chichí" son léxico cotidiano no exotismo turístico. Tratar como tal es ofensivo.

8. **Mezclar registros** — "Estimado cliente, qué pedo, agradecemos su atención" es absurdo. Decidir UN registro y mantenerlo.

---

## Lo que SÍ y NO hace este skill

**SÍ:**
- Revisa copy MX por región + generación + NSE + registro
- Genera variantes regionales (regio, chilango, tapatío, yucateco, costeño) con marcadores apropiados
- Detecta falsos amigos intra-MX (chichí, chaqueta, jale) y cross-Latam (concha, coger)
- Flag de clasismo, racismo lingüístico, regionalismo burlón
- Lista slang Gen Z 2025-2026 con vida útil
- Linkea a DEM y AML como anclas académicas

**NO:**
- No emite glosas verbatim del DEM (licencia)
- No reemplaza a `locale-mx` (reglas básicas)
- No reemplaza a `focus-group-mx` (validar con personas sintéticas)
- No predice qué slang Gen Z va a quedar — solo dice cuándo se validó
- No certifica que un copy sea 100% inofensivo — la lectura cultural sigue siendo humana
- No habla otros españoles (AR/ES/CO) — solo MX

---

## Cómo refrescar los datos

Cada 12 meses, revisar:
1. `genz_2026.json` — slang juvenil decae rápido. Borrar entradas con `last_validated > 18 meses` salvo que se valide vigencia.
2. `mexicanismos.json` — agregar marcas regionales nuevas si surgen, marcar como `decay_risk: alto` las que están perdiendo uso.
3. `falsos_amigos.json` — agregar nuevos descubrimientos.
4. `registro_clasismo.json` — la conversación sobre clasismo MX evoluciona; añadir referencias actualizadas.

Cuando refresques, actualiza el campo `_meta.as_of` y agregá un changelog.

---

## Fuentes

- **Diccionario del Español de México (DEM)** — El Colegio de México · https://dem.colmex.mx (oracle, no fuente)
- **Diccionario de Mexicanismos (DM)** — Academia Mexicana de la Lengua, 2da ed. 2022 (oracle, paywall)
- **Federico Navarrete — Alfabeto del racismo mexicano** (Malpaso, 2017) — ancla del bloque clasismo/racismo
- **Lope Blanch (1971)** — modelo de 6+ zonas dialectales adaptado a 7 (Yucatán separado)
- **Corpus regionales** Colmex/UANL — CHM (Monterrey), CHBC (Baja California), CSCM (CDMX) — validación de marcadores
- Prensa MX para regionalismos (MasdeMx, El Universal, Milenio) — citados en `genz_2026.json`
- Investigación curada por Sistemia Skills MX al `2026-06-10`.
