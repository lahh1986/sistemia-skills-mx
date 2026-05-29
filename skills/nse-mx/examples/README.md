# nse-mx — Ejemplos

## Ejemplo 1: Hogar conocido

**Usuario:** "Mi cliente es contador, casa con 2 baños, 1 carro, tiene fibra de Telmex, él y su esposa trabajan, 3 recámaras. ¿Qué NSE es?"

```bash
./scripts/classify.py \
  --educ profesional_completa \
  --banos 2 --autos 1 --internet si --ocupados 2 --dormitorios 3
```

**Output:**
- **Nivel C+** · 192/300 puntos · percentil ~84
- 12% de los hogares mexicanos están en este nivel.

**Lectura para el usuario:**
> Tu cliente está en el top 16% de México. Buen poder adquisitivo pero no
> patrimonial-rico. Le entran MSI fácil, cuida marca, compra Liverpool/Sears,
> manda hijos a privada cuota media. Copy: aspiracional accesible, no lujo
> exclusivo. WhatsApp Business funciona perfecto, email también lo lee.

---

## Ejemplo 2: Hogar D / lead de Coppel

**Usuario:** "Persona que vive en Apatzingán, su jefa (mamá) terminó primaria, no tienen auto, sí celular con datos pero no internet en casa, baño con regadera pero sin agua caliente (cuenta como 0 baño completo), ella es la única que aporta. Recámaras: 1 que comparten todos."

```bash
./scripts/classify.py \
  --educ primaria_completa --banos 0 --autos 0 \
  --internet no --ocupados 1 --dormitorios 1
```

**Output:**
- **Nivel E** · 34/300 · percentil ~5
- 8.7% de hogares MX.

**Lectura:**
> Hogar en pobreza. Programas sociales son ingreso significativo. Compra en
> tianguis y tiendita de la esquina. Crédito SOLO con prendaria (Monte de
> Piedad) o Coppel/Famsa con aval. Cuidado: si vendes ad de servicio digital
> de subscripción mensual, este hogar NO es tu target.
>
> Apatzingán (Michoacán) está en un estado donde 38% son D + 10% E = 48% de
> los hogares están en estas categorías, así que este perfil es MUY común
> ahí. Distinto de un D en Polanco (sería outlier).

---

## Ejemplo 3: Solo conoce la colonia

**Usuario:** "Solo sé que viven en Polanco. ¿Qué NSE asumir?"

**Respuesta del skill:**
> Sin las 6 variables no se puede clasificar exacto. Pero usando los priors
> nacionales:
>
> Polanco está en CDMX (donde A/B es 11% nacional) y es una zona top urbana
> (donde A/B sube a ~50-70% solo para esa colonia específica). La prior
> bayesiana razonable es **A/B con probabilidad 50-70%, C+ 25-35%, C 5-15%**.
>
> Para precisión real, pide al usuario las 6 preguntas AMAI o ancla a un dato
> externo (predial pagado, valor de inmueble, escuela donde estudian hijos).

---

## Ejemplo 4: Segmentación de base de leads

**Usuario:** "Tengo CSV con 5,000 leads, columnas: `nivel_estudios, baños, autos, internet, ingresos_personas, recamaras`. Segméntame por NSE."

**Respuesta sugerida:**

```python
import pandas as pd
import json
import subprocess

df = pd.read_csv("leads.csv")
results = []
for _, row in df.iterrows():
    h = {
        "educacion_jefe": row["nivel_estudios"],
        "banos_completos": row["baños"],
        "autos": row["autos"],
        "internet": "si" if row["internet"] else "no",
        "ocupados": row["ingresos_personas"],
        "dormitorios": row["recamaras"],
    }
    r = subprocess.run(
        ["python3", "scripts/classify.py", "--json", json.dumps(h)],
        capture_output=True, text=True
    )
    results.append(json.loads(r.stdout)["nivel"])
df["nse"] = results
print(df.groupby("nse").size())
```

---

## Ejemplo 5: Cross-check con AMAI oficial

Si el usuario te dice "ya AMAI me dijo que este hogar es C", úsalo como ancla y advierte si tu clasificación difiere:

> "Mi cálculo abierto te da {{X}} con {{P}} puntos. AMAI oficial te dijo C.
> Diferencia probable: ±1 nivel en casos frontera por los puntos exactos de
> AMAI (cerrados). Para entregables formales a clientes en MR usa AMAI oficial;
> para segmentación interna y marketing decisional, mi clasificación es
> robusta a ±1 nivel."
