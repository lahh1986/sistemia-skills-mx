# mexicanismos-mx

> Skill de Claude Code para escribir, revisar y adaptar **español mexicano por región, generación, clase social y registro** sin caer en caricatura, clasismo accidental ni el chilango por default.

Parte de [El Tianguis](https://eltianguis.sistemia.mx) — catálogo abierto de skills de Claude Code para México y Latinoamérica.

---

## Qué hace

Le dices a Claude:

> "Tengo este copy de landing para una clínica dental en Monterrey, ¿suena natural para regios o lo siento muy CDMX?"

Y te responde con:

- **Veredicto**: qué frases suenan chilangas, dónde se nota el "copy genérico LATAM" y qué hay que cambiar
- **Versiones alternativas**: una más natural para tu target, una segura cross-MX, una saturada de marca regional (con su tradeoff)
- **Flags**: falsos amigos peligrosos (chichí, chaqueta, popote, coger), carga clasista accidental (naco, fresa, godín mal usado), slang Gen Z con fecha de caducidad
- **Anclas**: link al Diccionario del Español de México (DEM) de Colmex cuando aplica

Cubre 7 zonas dialectales: Centro/CDMX, Noreste/Regio, Noroeste/Frontera, Norte-Bajío, Occidente/Tapatío, Sur-Sureste costa, Yucatán (zona separada, no agrupada con sureste — tiene justificación académica).

110 mexicanismos curados + 50 falsos amigos internos + guía editorial de clasismo + 25 entries de slang Gen Z 2026 (con `decay_risk` para advertir caducidad).

---

## Por qué este skill existe

**`locale-mx` ya cubre las reglas duras** (tú/ustedes, "computadora" no "ordenador", nada de "vale/tío"). Pero un copy que cumple esas reglas todavía puede sonar:

- Chilango pegado para una audiencia regia (que detecta el "está padre" en 3 segundos)
- Inconsistente entre registro corporativo y callejero
- Cargado de clasismo accidental (eufemismos racializados que parecen "cariñosos")
- Lleno de slang Gen Z que va a sonar pasado en 8 meses
- Caricaturesco saturando 10 mexicanismos en una sola línea

Este skill va **un nivel más profundo**: dada la regla "es español MX", elige QUÉ palabras MX según target. Para Sistemia y sus proyectos (Trust, Estudio, Academia, Otis cliente bilingüe), esto es la diferencia entre copy que convierte y copy que aliena.

---

## Instalación

```bash
# Copia el skill donde tu Claude Code lo lea
cp -r mexicanismos-mx/ ~/.claude/skills/mexicanismos-mx/
```

No hay setup. Es un skill de conocimiento — no ejecuta nada en tu máquina.

---

## Uso

Activa el skill con cualquier de estos triggers:

- "Adapta este copy para Monterrey, suena muy CDMX"
- "¿Esto suena regio o tapatío?"
- "Modismos por región México"
- "Falsos amigos del español mexicano"
- "Slang Gen Z mexicano 2026"
- "Evitar clasismo en mi anuncio"
- "¿Qué significa 'jale' en Monterrey?"
- "Versión yucateca de este texto sin caricatura"

Claude te preguntará por target (región + generación + NSE + registro) y devolverá análisis + versiones alternativas + flags de riesgo.

---

## Estructura

```
mexicanismos-mx/
├── SKILL.md                    # Workflow + decisión multi-zona + frontera con locale-mx + licencia DEM
├── README.md                   # Esto que estás leyendo
├── data/
│   ├── regiones.json           # 7 zonas dialectales + casos multi-zona
│   ├── mexicanismos.json       # 110 palabras curadas con scoring por región/registro
│   ├── falsos_amigos.json      # Palabras que cambian significado intra-MX y cross-Latam
│   ├── registro_clasismo.json  # Guía editorial sobre palabras con carga social
│   └── genz_2026.json          # Slang juvenil con decay_risk + last_validated
└── examples/
    └── landing-dental-regio-vs-cdmx.md  # Caso end-to-end de adaptación regional
```

---

## Frescura

Datos al `2026-06-10`. El bloque `genz_2026.json` necesita revalidación cada 12 meses — el slang Gen Z decae rápido. Los otros archivos son más estables (modismos clásicos, falsos amigos, carga clasista cambian en escala de años).

---

## Frontera con otros skills

| Skill | Cuándo usar |
|---|---|
| **`locale-mx`** | Reglas BÁSICAS de español MX (tú/ustedes, "computadora") |
| **`mexicanismos-mx`** (este) | Decisión QUÉ palabra MX según región/edad/clase/registro |
| **`focus-group-mx`** | Validar copy con 14 personas mexicanas sintéticas — sube un nivel |

Los tres son complementarios. Para un landing crítico: `locale-mx` corrige base → `mexicanismos-mx` adapta por región → `focus-group-mx` valida.

---

## Sobre licencias de fuentes

El Diccionario del Español de México (DEM) de El Colegio de México es CC BY-NC-ND. **Las definiciones en `mexicanismos.json` son CURADAS POR SISTEMIA**, NO copia del DEM. Cada entrada apunta a DEM con link de referencia como oracle académico cuando aplica.

El Diccionario de Mexicanismos de la AML (2da ed. 2022) es paywall — citamos cuando una entrada está confirmada ahí, sin copiar contenido.

Para citas académicas formales, manda a DEM/AML directo.

---

## Lo que NO hace

- No reemplaza a `locale-mx` (reglas básicas)
- No reemplaza a `focus-group-mx` (validar con personas sintéticas)
- No emite glosas verbatim del DEM (licencia)
- No predice qué slang Gen Z va a quedar
- No certifica que tu copy sea 100% inofensivo (la lectura cultural sigue siendo humana)
- No habla otros españoles (España, Argentina, Colombia, etc.)

---

## Cómo aportar

Issues y PRs bienvenidos:

- https://github.com/lahh1986/sistemia-skills-mx/issues

Especialmente valioso aportar: marcadores regionales que estamos perdiendo, slang Gen Z nuevo, casos de carga clasista emergente.

---

## Licencia

MIT. Skill mantenido por [Sistemia](https://sistemia.mx).
