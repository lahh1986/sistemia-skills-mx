# Caso: landing dental — variante Monterrey vs CDMX

> Sistemia Estudio recibe un cliente dental en Monterrey. La agencia (CDMX)
> manda copy default. Aquí mostramos cómo `mexicanismos-mx` adapta para que
> suene regio sin caricatura, y cómo se vería el mismo copy para CDMX.

## Input — copy default (suena chilango, sirve solo para CDMX)

```
¡Hola! En Clínica Sonrisa creemos que tu sonrisa es lo máximo.
Por eso hicimos un consultorio bien padre con todo el equipo moderno,
para que vengas a chambear con tu dentista de confianza.

Agenda en 2 minutos, te checamos sin compromiso, y si todo sale chido
seguimos con tu tratamiento. Estamos en Polanco, fácil llegar.
```

## Diagnóstico del target

| Variable | Valor cliente regio | Valor cliente CDMX |
|---|---|---|
| Región | noreste_regio | centro_altiplano |
| Generación | mixto, weight millennial+X | mixto, weight millennial |
| NSE | B/C+ urbano | B/C urbano |
| Registro | semi-formal coloquial | semi-formal coloquial |

## Análisis del copy default contra `mexicanismos-mx`

### Para audiencia regio (Monterrey)
| Texto | Problema | Severidad |
|---|---|---|
| "es lo máximo" | OK nacional. No es problema, pero no aporta sabor regio. | Bajo |
| "bien padre" | Marcador chilango. Para regio suena distante o ñoño. | Medio-alto |
| "chambear" | Nacional, pero "jalar" suena más auténtico regio. | Bajo-medio |
| "te checamos" | OK nacional. Funciona. | OK |
| "todo sale chido" | OK nacional. Funciona regio. | OK |
| "Polanco, fácil llegar" | Geografía CDMX. Hay que cambiar a colonia regia. | CRÍTICO |

**Lectura general regio:** copy claramente chilango pegado mecánicamente. Un regio detecta el "padre" en 3 segundos y desconecta. La referencia a Polanco es error de copy genérico.

### Para audiencia CDMX
| Texto | Problema | Severidad |
|---|---|---|
| Todo el copy | Funciona. Polanco es CDMX. | OK |

**Lectura general CDMX:** copy correcto para CDMX. Cero ajustes.

---

## Output — copy adaptado regio

```
Qué onda. En Clínica Sonrisa pensamos que una buena sonrisa está con madre.
Por eso armamos un consultorio con equipo moderno y dentistas que sí saben
lo que hacen, para que le entres a tu tratamiento sin volverte loco.

Agenda en 2 minutos, te checamos sin compromiso, y si jalas con nosotros
seguimos. Estamos en San Pedro, a un lado del Tec, fácil llegar.
```

### Cambios aplicados
| Cambio | Razón |
|---|---|
| "Hola" → "Qué onda" | Cierre informal regio más natural |
| "bien padre" → "está con madre" | Marcador regio fuerte sin caricatura |
| "vengas a chambear con tu dentista" → "le entres a tu tratamiento" | "Chambear con dentista" sonaba raro (chambear=trabajar); "le entres" es marca regio aceptable |
| "todo sale chido" → "jalas con nosotros" | "Jalar" como verbo regio = entablar relación. Marca regional sin saturar |
| "Polanco" → "San Pedro, a un lado del Tec" | Geografía correcta. San Pedro es la zona premium de MTY |
| Mantenemos "te checamos", "fácil llegar" | Funcionan nacional, no necesitan cambio |

### Cosas que NO incluí (con razón)
- "bofo", "chopo" → marcadores fuertes que podrían sonar caricatura
- "wey" → registro callejero, inapropiado para landing dental
- "agüevo" → vulgar para B2C salud
- "raite", "troca" → no aplican al contexto dental

### Cosas que evité conscientemente
- Saturar el copy con marcadores regios (sería caricatura)
- Mencionar carne asada o cerveza (estereotipo)
- Usar inglés ("nice", "aesthetic") — regio working/middle class no se identifica con eso

---

## Output — copy para CDMX (mismo cliente, ciudad distinta)

```
¡Hola! En Clínica Sonrisa creemos que tu sonrisa es lo máximo. Por eso
armamos un consultorio padrísimo con todo el equipo moderno, para que
vengas con confianza a tu próximo tratamiento.

Agenda en 2 minutos, te checamos sin compromiso, y si todo sale chido
seguimos con tu plan. Estamos en Polanco, a 3 cuadras del metro
Auditorio.
```

### Cambios desde el default
| Cambio | Razón |
|---|---|
| "hicimos un consultorio bien padre" → "armamos un consultorio padrísimo" | "Armamos" es marcador centro positivo; "padrísimo" intensifica naturalmente |
| "a chambear con tu dentista de confianza" → "con confianza a tu próximo tratamiento" | "Chambear" en contexto de paciente sonaba raro; reescritura natural CDMX |
| "Polanco, fácil llegar" → "Polanco, a 3 cuadras del metro Auditorio" | Geografía específica chilanga (referencia al metro = chilango clásico) |

---

## Variante muy regional regio (con riesgo de caricatura — usar con criterio)

Si el brand quiere apostar más fuerte a la identidad regia (riesgo: aliena no-regios pero refuerza local), una versión más cargada:

```
Qué onda mi compa. En Clínica Sonrisa sabemos que jalar tu sonrisa
hasta el siguiente nivel no debe ser pedo.

Armamos un consultorio con madre — equipo moderno, dentistas que la saben,
y precios sin pedos para que no andes contando los billetes.

Échate la agenda en 2 minutos, te checamos gratis, y si jalamos seguimos.
San Pedro, a un lado del Tec, fácil llegar.
```

**Cuándo SÍ usar esta versión:** dental que es marca con identidad regia explícita, busca diferenciarse del chilanguismo aspiracional.
**Cuándo NO usar:** dental premium para audiencia mixta (incluye regios chilangueados o no-regios viviendo en MTY).

---

## Notas editoriales del caso

1. **Falso amigo evitado:** No usé "chichi" / "chichí" en ningún lado. Aunque la palabra apropiada en Yucatán es "abuela", el riesgo cross-MX es alto.

2. **Carga clasista evitada:** No usé "naco", "fresa", "godín", ni eufemismos racializados. Salud dental cruza clases — copy debe ser inclusivo.

3. **Slang Gen Z evitado:** No usé "delulu", "aesthetic", "POV", "x", "gpi". Una landing dental es brand de 1-3 años de uso; meter slang juvenil con `decay_risk: alto` caduca rápido.

4. **Yucatán-ready si fuera Mérida:** Si el cliente fuera de Mérida, cambiaría "qué onda" por "mare", "está con madre" por "está bomba", y "San Pedro" por "Norte de Mérida" o referencia local concreta. Pero NO satures préstamos mayas: 1-2 marcadores yucatecos es máxima dosis.

---

## Próximo skill complementario

Cuando el flujo escale, considerar:
- **`mexicanismos-mx-detector`**: dado un texto cualquiera, devuelve probabilidad de cada zona ("este texto suena 70% chilango, 20% regio, 10% norteño").
- **`mexicanismos-mx-anonimizador`**: dado un texto regional, lo neutraliza a MX nacional para contenido cross-regional.

Para v1, el flujo manual con `mexicanismos-mx` + revisión humana es suficiente.
