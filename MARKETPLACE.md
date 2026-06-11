# Sistemia Skills MX — Marketplace

> Catálogo de skills de Claude Code para mercado mexicano. Cada skill resuelve
> una pregunta concreta de negocio, queda anclada en data pública oficial MX
> y se distribuye con metodología transparente.

## Filosofía

1. **100% México.** No es traducción de skills gringos. Cada decisión asume
   contexto, idioma y cultura mexicana.
2. **Data pública oficial.** INEGI, AMAI, PROFECO, CONAPO, IFT, AMVO, BBVA,
   World Bank. Nada de números inventados o "vibes". 4 GB de research catalogado
   (ver [`research/INDEX.md`](research/INDEX.md)).
3. **Sin caja negra.** Si el skill toma una decisión, puedes ver el dato detrás.
   Implementaciones abiertas, queries auditables, validaciones documentadas.
4. **Composables.** Cada skill resuelve algo discreto. Skills compuestos
   (`mercado-local-mx`) orquestan a los atómicos.
5. **Distribuidos como Markdown.** Sin runtime extra. Si tienes Claude Code,
   el skill funciona.

## Catálogo — v1.0

### Skills atómicos (resuelven una pregunta cada uno)

#### 1. `focus-group-mx` 🎯 — Validación de copy
- **Pregunta:** ¿Mi anuncio/landing/copy va a funcionar en México antes de gastar en ads?
- **Cómo:** 14 personas mexicanas (NSE × género × generación × región × voto 2024) evalúan el material con FGMX-Score de 7 dimensiones.
- **Output:** Score numérico + 3 variantes mejoradas + tabla de decisiones.
- **Data:** ENIGH 2024 microdatos (91,414 hogares) + AMAI 2024 + PROFECO + INE 2024.
- **Status:** ✅ MVP funcional (1 persona validada, 13 en cola para v1.1).

#### 2. `precios-mx` 💰 — Precios reales por geografía
- **Pregunta:** ¿Cuánto cuesta X en Y colonia/ciudad/estado/cadena? ¿Es justo $Z?
- **Cómo:** Wrapper de DuckDB sobre 10.5 M de capturas PROFECO QQP 2024-2026.
- **Output:** Mediana, distribución, top 3 más barato/caro, lectura accionable.
- **Data:** PROFECO "Quién es Quién en los Precios" consolidado.
- **Status:** ✅ Funcional end-to-end.

#### 3. `nse-mx` 🪪 — Clasificador NSE AMAI 2024
- **Pregunta:** ¿Qué NSE (A/B → E) es este hogar/cliente/lead?
- **Cómo:** Implementación abierta de la Regla AMAI 2024 (6 variables, regresión calibrada con ENIGH 2022).
- **Output:** Nivel + puntos + percentil + perfil de gasto + brand affinity.
- **Data:** AMAI Nota Metodológica oct-2023 + distribuciones ENIGH 2022 nacional y por entidad.
- **Status:** ✅ Funcional con script Python.

#### 4. `demografia-mx` 👥 — Market sizing demográfico
- **Pregunta:** ¿Cuántas personas {edad/sexo} viven en {entidad} en {año}?
- **Cómo:** DuckDB sobre Conciliación CONAPO 1950-2019 + Proyecciones 2020-2070 (737K renglones, edad simple).
- **Output:** Cohorte + comparativo entre estados + trayectoria + implicación.
- **Data:** CONAPO oficial DOF.
- **Status:** ✅ Funcional. v1.1: agregar Censo INEGI 2020 (sub-municipal).

#### 5. `habitos-digitales-mx` 📲 — Canal y plataforma por target
- **Pregunta:** ¿En qué red/plataforma/dispositivo está mi target y cuánto puedo alcanzar?
- **Cómo:** Snapshot 2024-2025 de ENDUTIH + DataReportal + AMVO + ENIF con tablas listas para query.
- **Output:** Mix de canales recomendado + presupuesto sugerido por plataforma + gaps offline.
- **Data:** ENDUTIH 2024 INEGI (n=65,000 viviendas), DataReportal Digital 2025 MX, AMVO 2024-25, ENIF 2024.
- **Status:** ✅ Snapshot listo.

#### 6. `payments-mx` 💳 — Gateway y métodos de pago en México
- **Pregunta:** ¿Qué gateway/PSP uso? ¿Qué métodos acepto? ¿Cuánto me cuesta realmente? ¿Cómo armo split de marketplace?
- **Cómo:** Comisiones reales 2026 verificadas (Conekta, Mercado Pago, Stripe MX, Openpay, Clip) + adopción real de métodos (AMVO, Banxico, INEGI) + árbol de decisión por vertical (B2C, SaaS, marketplace, B2B, retail alto ticket) + patrones de marketplace (split, escrow, KYC seller).
- **Output:** Gateway recomendado + métodos a aceptar + fee efectivo estimado + gotchas operativos + próximos pasos concretos.
- **Data:** Páginas oficiales de pricing (cada gateway), AMVO Estudio Venta Online 2025, Banxico SPEI/CoDi, INEGI ENIF 2024, GlobeNewswire BNPL Report 2026, marco regulatorio CNBV/Ley Fintech.
- **Status:** ✅ MVP funcional — 5 gateways + 11 métodos + caso end-to-end de marketplace (eltianguis).

#### 7. `mexicanismos-mx` 🗣️ — Español MX por región, edad, clase y registro
- **Pregunta:** ¿Este copy MX suena natural para mi target (regio/chilango/yucateco/costeño)? ¿Tiene clasismo accidental? ¿El slang Gen Z va a caducar?
- **Cómo:** 7 zonas dialectales (Lope Blanch adaptado + Yucatán separado) + 110 mexicanismos curados con scoring por región/registro/generación/NSE + 50 falsos amigos intra-MX y cross-Latam + guía editorial de carga clasista/racial + 25 entries Gen Z 2026 con `decay_risk` y `last_validated` para advertir caducidad.
- **Output:** Veredicto + análisis línea por línea + 3 versiones alternativas (más natural / segura cross-MX / saturada de marca regional) + flags de falsos amigos y carga clasista + links a DEM como oracle.
- **Data:** Curaduría propia Sistemia (NO copia DEM, que es CC BY-NC-ND). Anclas: DEM/Colmex, Diccionario de Mexicanismos AML 2022, Federico Navarrete "Alfabeto del racismo mexicano" (2017), corpus regionales (CHM Monterrey, CHBC Baja California, CSCM CDMX), prensa MX para slang juvenil.
- **Frontera con `locale-mx`:** locale-mx = reglas duras (tú/ustedes, "computadora"). mexicanismos-mx = qué palabra MX según target. Complementarios.
- **Status:** ✅ MVP funcional — 7 regiones + 110 mexicanismos + 50 falsos amigos + caso end-to-end (landing dental regio vs CDMX).

#### 8. `payments-ar` 🇦🇷 — Gateway y métodos de pago en Argentina
- **Pregunta:** ¿Qué gateway uso en AR? ¿Cómo modelo cuotas post-Ahora 12 derogado? ¿Cómo cobro USD con cepo cambiario? ¿MP a inmediato 6.29% o 35d 1.49%?
- **Cómo:** Comisiones reales 2026 verificadas (Mercado Pago AR, Decidir/Prisma, dLocal, MODO, PayU, Ualá Bis, Naranja X) + adopción real de métodos (BCRA Informe Pagos Minoristas, Infobae) + árbol de decisión específico AR (vertical + cuotas + bancarización + geografía + cepo) + patrones de marketplace MP API + estrategia de cuotas post-derogación.
- **Output:** Gateway recomendado + estrategia de cuotas (absorber merchant vs trasladar cliente vs híbrido) + fee efectivo estimado + gotchas operativos AR (hold MP 7-21d, categoría BCRA cambiante, surcharge tarjeta internacional +3%, cepo) + próximos pasos.
- **Data:** Páginas oficiales + secundarias verificadas (MP bloquea WebFetch), BCRA Com 'A' 8432/2026, Infobae jun-2026 derogación Ahora 12, GlobeNewswire AR BNPL Report 2026.
- **Status:** ✅ MVP funcional — 7 gateways + 14 métodos + caso end-to-end e-commerce electro con cuotas.

### Skills compuestos (orquestan a los atómicos)

#### 9. `mercado-local-mx` 📍 — Viabilidad de negocio físico
- **Pregunta:** ¿Vale la pena abrir mi negocio en X ciudad / colonia?
- **Cómo:** Combina `demografia-mx` + `nse-mx` + `precios-mx` + (opcional) `habitos-digitales-mx` para calcular TAM/SAM/SOM, semáforo de viabilidad, ingreso estimado y riesgos.
- **Output:** Dossier de viabilidad con 3 ubicaciones alternativas si la primera no convence.
- **Status:** ✅ Workflow documentado.

#### 10. `legal-pyme-mx` ⚖️ — Cumplimiento legal federal PyME
- **Pregunta:** ¿Esta PyME cumple con sus obligaciones legales federales más caras?
- **Cómo:** Validadores RFC + CURP + chequeo contra 11 listas SAT (69-B/69 CFF, 14,436 RFCs), generador de Aviso de Privacidad LFPDPPP 2025 (corto/simplificado/integral por giro), tabla ISN por estado, árbol de decisión para obligaciones por giro.
- **Output:** Veredicto + costo del riesgo si se ignora + ruta de cumplimiento.
- **Data:** 30 archivos oficiales (~119 MB) descargados: SAT (CFDI XSDs, RMF 2026, listas 69-B/CFF), Diputados (CFF/LFPDPPP/LFPC/LSS/LIFNVT/LFT/LFPPI/LFPIORPI), STPS (NOM-035), INAI (Manual Aviso Privacidad), RENAPO (reglas CURP).
- **Status:** ✅ MVP funcional. RFC + 69-B + Aviso Privacidad + CURP + ISN listos. Pendiente v1.1: COFEPRIS, CONDUSEF, IFT, marco NOM-STPS completo.

#### 11. `contador-pyme-mx` 🧾 — Validador CFDI + skills para contadores PyME
- **Pregunta:** ¿Este CFDI 4.0 está bien armado? ¿Voy a deducir sin problemas? ¿Mi proveedor es facturera?
- **Cómo:** Validador estructural contra XSDs SAT + catálogos vigentes 2026 + detección de complementos (Pagos 2.0, Nómina 1.2, Carta Porte 3.1, Retenciones v2.0) + reglas de negocio (RESICO PF→PM 1.25%, honorarios 10%+10.67%, arrendamiento, PUE fin de mes, motivos cancelación 01-04) + cruce automático contra 11 listas SAT (delega a `legal-pyme-mx`).
- **Output:** Veredicto + lista de hallazgos con severidad + recomendación accionable + costo de NO atender el riesgo.
- **Data:** 40 archivos descargados (~26 MB) — 11 XSDs CFDI + 6 XSDs Contabilidad Electrónica + Anexo 8 RMF (tarifas ISR) + Anexo 24 RMF (contabilidad) + 6 leyes federales (CFF, LISR, LIVA, LIEPS, LFT, LSS) + INPC histórico INEGI. Más 21 servicios con auth (Banxico SIE, descarga masiva CFDI, 32-D, etc.) documentados.
- **Módulos v1.0 (9):** CFDI [`validate_cfdi.py` · `check_pue_ppd.py` · `check_cancellation.py`] · Nómina [`calc_nomina.py` · `calc_finiquito.py`] · Declaraciones [`calc_pago_provisional_isr.py` (PM + PF + RESICO + arrend) · `calc_iva_mensual.py` · `gen_diot_txt.py` (plataforma nueva 2025) · `calc_declaracion_anual_pf.py` (Art. 152 con deducciones personales topadas)]
- **Data oficial cargada:** Tarifas ISR 2026 5 periodos (Anexo 8 RMF DOF 28-12-2025) + tarifa anual 2025/2026 + subsidio empleo 2026 ($536.22 / 15.02% UMA) + tarifas RESICO PF 1-2.5% + cuotas IMSS 8 seguros (CEAV con tabla por rango SBC) + UMA $117.31 + SM $315.04/$440.87 + calendario fiscal 2026 + layout DIOT 17 campos + 32 ISN estatales
- **Próximos v1.1:** `descarga-masiva-cfdi-mx`, `valores-vigentes-mx` (Banxico SIE + INEGI INPC live), `opinion-32d-mx`, `calc_declaracion_anual_pm.py`
- **Status:** ✅ MVP funcional — 9 módulos probados con casos reales (CFDI RESICO sin retención, PUE fin mes, cancelación 01, finiquito 4 años, despido 6 años $233K, nómina Michoacán $15K, RESICO PF $45K, IVA mensual, DIOT 3 proveedores, anual PF saldo a favor).

## Próximos en backlog (v1.1+)

| Skill candidato | Qué resolvería | Data adicional necesaria |
|---|---|---|
| `naming-mx` | Generar nombres de marca con check NIC.mx + IMPI + redes + fit cultural regional | API NIC.mx + IMPI registro |
| `whatsapp-mx` | Templates + flows de WA Business que convierten en MX | metodología, no data |
| `copy-mx` | Generador/revisor de español MX real (sin anglicismos, ritmo regional) | reglas + corpus locale-mx |
| `reseñas-mx` | Análisis de Google + Doctoralia + FB de un negocio local | reusar pipeline Trust |
| `calendario-mx` | Cuándo lanzar qué (Buen Fin, Día de Madres 10 mayo, quincenas, etc.) | ~50 fechas curadas |

## Cómo usar este repo

### Instalación rápida (un skill)

```bash
git clone https://github.com/lahh1986/sistemia-skills-mx.git
cp -r sistemia-skills-mx/skills/precios-mx ~/.claude/skills/
# habilitar en Claude Code config si no está auto-detectado
```

### Instalación completa (todos los skills + research)

```bash
git clone https://github.com/lahh1986/sistemia-skills-mx.git
cd sistemia-skills-mx

# Bajar research bruto (~4 GB)
# (instrucciones por institución en research/FUENTES.md)

# Construir DBs derivadas
python3 skills/demografia-mx/scripts/build_db.py
# (precios.duckdb se distribuye ya construido; ver research/)
```

### Estructura del repo

```
sistemia-skills-mx/
├── README.md
├── MARKETPLACE.md             ← este archivo (catálogo)
├── METODOLOGIA.md             ← método PSEC-MX para personas sintéticas
├── research/                  ← 4 GB de data MX pública catalogada
│   ├── INDEX.md               ← mapa temático
│   ├── catalog.json           ← 67 fuentes machine-readable
│   ├── FUENTES.md             ← auditoría completa
│   ├── precios.duckdb         ← 10.5M registros PROFECO
│   ├── demografia.duckdb      ← 737K renglones CONAPO
│   └── {institucion}/         ← una carpeta por institución
└── skills/
    ├── focus-group-mx/
    ├── precios-mx/
    ├── nse-mx/
    ├── demografia-mx/
    ├── mercado-local-mx/
    └── habitos-digitales-mx/
```

## Licencia y atribución

- **Skills (código y docs):** MIT — ver [`LICENSE`](LICENSE).
- **Datos de terceros:** cada institución mantiene su licencia. Ver
  [`research/FUENTES.md`](research/FUENTES.md) para atribuciones por archivo.
- **AMAI:** la regla NSE AMAI 2024 es metodología pública; la implementación
  en `nse-mx` es una reconstrucción abierta basada en la nota metodológica de
  octubre 2023. Para entregables formales en investigación de mercado,
  recomendamos usar el algoritmo licenciado directamente con AMAI.

## Contribuir

Issues y PRs bienvenidos. Reglas:

1. Cada skill debe tener `SKILL.md` con `name`, `description` (con triggers),
   y workflow documentado.
2. Anclar afirmaciones a fuentes en `research/` o agregar nuevas con script
   de descarga reproducible.
3. Español de México en docs orientadas a usuario (sin "vale", "ordenador",
   "tío", "vos"). Inglés en código (variables, funciones).
4. Si un skill compite con `focus-group-mx` por cobertura, justificar la
   diferenciación.

— Curado por Luis Huerta (chombi) · Sistemia.mx · 2026
