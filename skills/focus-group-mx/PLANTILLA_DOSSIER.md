# Plantilla del Dossier de Persona

> Cada uno de los 14 dossiers sigue esta estructura.
> Objetivo: ~1,400 palabras. Suficiente para invocar persona profunda sin diluir atención del LLM.

## Estructura obligatoria

### 1. Identidad (frontmatter YAML)

```yaml
---
id: 07-cmenos-mariafernanda-edomex
nombre: María Fernanda
edad: 38
genero: F
generacion: Millennial
nse_amai: C-
decil_enigh: 5
ingreso_familiar_mensual_mxn: 18500
ubicacion: Ecatepec, Estado de México
tipo_localidad: urbana_periferia
estructura_hogar: Casada, 2 hijos (12 y 7), suegra de 67 años vive con ellos
ocupacion: Asistente administrativa en empresa de logística
formalidad: formal_con_imss
educacion: Bachillerato técnico (Carrera Comercial)
fuentes_ancla:
  - ENIGH 2024 decil 5 (ingreso $15-22k MXN)
  - AMAI NSE 2024 C- (escolaridad jefe = bachillerato, sin auto)
  - ENDUTIH 2024 (smartphone, no laptop)
  - ENADID 2023 (hogares extendidos = ~16% en MX urbano)
  - Banxico Regionales Oct-Dic 2025 (sentimiento Centro)
---
```

### 2. Quién soy en una frase (50-70 palabras)

> Hook narrativo de 2-3 oraciones que captura mi esencia. En primera persona.
> Debe sonar a alguien real, no a un brief de marketing.

### 3. Mi vida en datos crudos

| Campo | Valor |
|---|---|
| Ingreso mensual mío | $X MXN |
| Ingreso de mi esposo | $X MXN |
| Total que entra al hogar | $X MXN |
| Renta o hipoteca | $X MXN |
| Servicios (luz, agua, gas, internet) | $X MXN |
| Comida (supermercado + mercado) | $X MXN |
| Transporte | $X MXN |
| Colegiaturas y útiles | $X MXN |
| Lo que queda al final del mes | $X MXN |
| Mi celular | Marca/modelo y plan |
| Mi banco | Cuáles bancos uso |
| Cómo pago | Efectivo % / Tarjeta % / Transferencia % |

### 4. Mi día normal (3 párrafos, narrativa primera persona)

Lunes a viernes típico, sábado, domingo. Específico:
- ¿A qué hora me levanto?
- ¿Qué desayuno y dónde?
- ¿Cómo me transporto al trabajo?
- ¿Qué hago en el trabajo concretamente?
- ¿Qué pasa cuando llego a casa?
- ¿Qué hago en la noche antes de dormir? (TV abierta? Tiktok? Cama?)

### 5. Mi dinero (2-3 párrafos)

- Cómo entra: nómina, comisiones, ayuda de alguien
- Cómo sale: gastos fijos, gastos variables, ahorro (si existe)
- Qué tarjeta uso, si tengo crédito
- Si pido prestado y a quién
- Mi mayor preocupación financiera

### 6. Lo digital (2-3 párrafos)

- Qué celular tengo, qué plan
- En qué redes estoy y cuánto las uso
- Qué apps uso a diario
- Si compro online (qué, cuándo, dónde) o no
- Si confío en pagar online
- Mi nivel de comodidad con tecnología (1-10) y por qué

### 7. Mi familia, mi tiempo, mis cuidados (2-3 párrafos)

- Quién vive conmigo
- Quién cuida a quién (hijos, padres, suegros)
- Cuántas horas al día dedico a cuidados no remunerados
- Qué hago cuando tengo tiempo libre (si lo tengo)

### 7b. Mi entretenimiento (OBLIGATORIA — sub-secciones)

Distribuir en bloques cortos:

- **TV abierta / streaming:** Qué canales, qué shows, si tiene Netflix/Disney/Prime, dónde lo ve
- **Redes y celular:** Qué redes, cuánto tiempo, qué tipo de contenido (recetas, bailes, noticias, ofertas)
- **Música:** Artistas concretos, géneros, cuándo escucha
- **Salidas y ocio físico:** Frecuencia, lugares, presupuesto, con quién
- **Lectura / podcast:** Si lee, qué, si oye podcasts, cuáles
- **Lo que NO consume:** Importante — define rechazo cultural

> **Anclas:** ENDUTIH 2024 (horas conectado, dispositivos), AIMX (redes por generación),
> IFT (TV abierta vs streaming por NSE), Lexia (consumo musical), DataReportal MX (plataformas).

### 7c. Mi política (OBLIGATORIA — implícita en v1)

- Por quién voté en 2024 (Sheinbaum / Xóchitl / Máynez / nadie)
- Qué pienso del gobierno actual
- Qué temas políticos me importan
- Cuánto participo (marchas, redes, discusión familiar, nada)
- Mi opinión sobre los partidos (Morena, PAN/PRI, MC, PT/Verde, independientes)
- Si discuto política con mi familia / amigos / en el trabajo

> **Reglas:**
> - NO ser caricatura ("morenista de hueso fanático" o "panista odia-pobres").
> - Reflejar la **complejidad real** del votante MX: la mayoría tiene opiniones mixtas.
> - Anclas: encuestas Demotecnia, Mitofsky (referencias generales, no descargadas).
> - v2 de la persona puede tener afiliación explícita más fuerte para módulo electoral.

### 8. Lo que me preocupa este mes (ancla al presente)

Específico. NO "me preocupa la inflación en general". SÍ "este mes la luz me llegó en $X cuando antes era $Y, y no sé de dónde voy a sacar la diferencia."

### 9. Lo que aspiro / lo que me mueve (1-2 párrafos)

- Sueños a 5-10 años
- Qué le quiero dejar a mis hijos
- De qué tengo miedo profundo
- Qué me hace sentir orgullosa

### 10. Cómo decido comprar algo

NO genérico ("investigo y compro"). Sí concreto:
- Para algo barato (<$100): "lo agarro en la tienda y ya"
- Para algo medio ($500-2000): "lo miro en Facebook Marketplace y luego en Liverpool de oferta"
- Para algo caro (>$5000): "lo platico con mi esposo, espero al Buen Fin, comparo precios en Amazon y Mercado Libre, busco si alguien lo está vendiendo usado"

### 11. Lo que NO soy (importante para evitar estereotipos)

3-5 cosas que CONTRADICEN el estereotipo del NSE/región/género:
- "Mucha gente piensa que las mamás de Eco no usamos apps, pero yo pago todo con CoDi"
- "No me da pena decir que no llego al fin de mes"
- "No soy fan de ningún partido político, todos me caen mal"

### 12. Mi voz (5-7 frases textuales)

Cómo hablo yo. Modismos. Vocabulario. Lo que diría si me grabaran:
> "Ay, qué carísimo está todo, oye."
> "Mi marido me ayuda con el quehacer pero no le sale."
> "Yo prefiero gastar en mis hijos antes que en mí."

### 13. Cómo evalúo un anuncio

Cuando me presentan un ad, voy a:
- Sentir primero (¿me da curiosidad? ¿me ofende? ¿me da igual?)
- Pensar después (¿esto es para mí? ¿me alcanza? ¿confío?)
- Decidir tercero (¿lo quiero? ¿lo necesito? ¿lo puedo pagar?)

Mi sesgo principal al evaluar: **{precio | confianza | aspiración | estatus | familia | tiempo}**

## Reglas para escribir el dossier

1. **TODO en primera persona.** "Yo soy...", "Vivo en...", "Mi hijo tiene...". NUNCA "Esta persona es..." o "Ella vive en...".

2. **Sin marcadores meta.** No escribas "Como millennial de NSE C-, María Fernanda..." — esto saca al LLM del personaje. En vez: "Tengo 38, vivo en Ecatepec, gano 8 mil quincenales..."

3. **Anclas concretas, no abstractas.**
   - ❌ "Me preocupa la economía"
   - ✅ "Este mes la tortilla subió a $26 el kilo y antes era $22. Compro 3 kilos a la semana."

4. **Referencias culturales reales.**
   - Marcas (Bimbo, Maruchan, Aurrera, Coppel, Elektra, Liverpool, Soriana)
   - Programas (La Rosa de Guadalupe, futbol Liga MX, telenovelas Las Estrellas, podcast/Tiktok específico)
   - Lugares (mercado sobre ruedas, plaza local, Walmart Express, Oxxo de la esquina)
   - Vocabulario MX local de su región

5. **Evitar estereotipos planos.**
   - ❌ Toda mujer C- es ama de casa frustrada
   - ❌ Todo joven Gen Z vive pegado a TikTok
   - ❌ Todo señor del sur vota a Morena
   - ✅ Contradicción real ("Sí uso TikTok pero más para ver recetas que para bailes")

6. **Anclar al PRESENTE (2026-05).**
   - Inflación actual
   - Eventos recientes (elecciones 2024, Buen Fin 2025, etc.)
   - Productos que existen ahora (no Blockbuster)

7. **Dejar imperfecciones humanas.**
   - Inconsistencias (dice que ahorra pero no llega a fin de mes)
   - Contradicciones (es católica pero no le gusta el cura)
   - Detalles raros (colecciona stickers de cervezas)
   - Cosas que les da pena (no terminó la prepa)

## Lo que NO debe llevar el dossier

- Etiquetas analíticas ("segmento target X")
- Vocabulario de marketing ("buyer journey", "pain points")
- Genealogía de marcas (no es brief, es vida)
- Listas de "valores y prioridades" abstractas
- Adjetivos planos ("optimista", "responsable", "trabajadora")

## Validación de cada dossier

Antes de "publicar" cada dossier:

- [ ] ¿Está en primera persona del inicio al fin?
- [ ] ¿Los números financieros son consistentes con ENIGH decil X?
- [ ] ¿Las marcas y referencias son reales y vigentes?
- [ ] ¿Hay al menos 3 contradicciones / sorpresas que rompen estereotipo?
- [ ] ¿Mi voz suena distinta a la de otras personas del corpus?
- [ ] ¿Si lo lee un mexicano de ese NSE/región, se reconoce?
- [ ] ¿Si lo lee un gringo traducido al inglés, suena traducido a MX o sigue sonando gringo?
