# contador-pyme-mx · catálogo de fuentes oficiales

Tres archivos:

| Archivo | Qué es |
|---|---|
| `sources.json` | Array JSON con 61 fuentes oficiales (SAT, Diputados, Banxico, INEGI, IMSS, INFONAVIT, STPS, DOF/CONASAMI). Es el catálogo maestro del skill. |
| `verify.py` | Verificador HTTP standalone (solo stdlib). Rellena `estado_verificacion`, `http_status`, `size_bytes_esperado`, etc. |
| `gen_sources.py` | Generador del catálogo (para extender/regenerar). |

## Estado de verificación — léelo

El catálogo se generó en un sandbox cuya red está restringida a registros de
paquetes (pypi/npm/github). **No puede alcanzar dominios `.gob.mx` ni `banxico.org.mx`**
(el proxy responde `403 host_not_allowed`). Por eso:

- **5 fuentes** llegan ya como `200_OK`: los 5 XSD núcleo del CFDI, verificados en
  vivo vía un fetcher que sí alcanza esos hosts (devolvieron `text/xml`):
  `cfdv40`, `nomina12`, `Pagos20`, `retencionpagov2`, `CatalogoCuentas_1_1`.
- Las **56 restantes** llegan como `pendiente`. No están sin comprobar a ciegas:
  cada una trae `confianza: alta|media` según la evidencia. **Corre `verify.py`
  en tu terminal** (red abierta) para convertir `pendiente` → estado real + tamaño.

## Correr el verificador

```bash
python3 verify.py                 # verifica todo (omite los requires_auth)
python3 verify.py --check-auth    # también prueba los de auth (darán 401/403, es normal)
python3 verify.py --only SAT      # filtra por institution / id / topic (substring)
python3 verify.py --insecure      # si algún certificado TLS .gob.mx da problemas
python3 verify.py --inplace       # sobrescribe sources.json en vez de crear .verified
python3 verify.py --download ./corpus   # descarga los OK descargables al árbol local_path
```

Salida: `sources.verified.json` + un resumen por estado + lista de los no-OK con su
`final_url` (útil cuando Diputados redirige `/pdf/X.pdf` → `portalhcd...`).

## Vocabulario de `estado_verificacion`

`200_OK` · `3xx_REDIRECT_OK` · `401_AUTH` · `403_FORBIDDEN` · `404_NOT_FOUND` ·
`4xx`/`5xx` (código literal) · `ERROR:<motivo>` · `omitido_requiere_auth`

## Campos de cada entrada

`id`, `institution`, `name`, `year`, `topics[]`, `geography`, `granularity`
(`esquema|norma|ley|dataset|api|servicio|portal`), `format`
(`xsd|pdf|csv|api_json|soap|web`), `url`, `url_alt`, `local_path`,
`estado_verificacion`, `verificado_en_sesion`, `metodo_verificacion`,
`confianza` (`alta|media`), `size_bytes_esperado`, `requires_auth`, `auth_tipo`,
`vigencia_dof`, `notas`.

## `confianza: media` — qué confirmar a mano

13 entradas. Las que más vale revisar con `verify.py`:

- `sat_cfdi_xsd_tfd11`, `sat_cartaporte_31_xsd`, `sat_retencionpago_catalogos_xsd`:
  versión/nombre de archivo del XSD.
- `sat_conta_auxctas_11`, `sat_conta_auxfolios_12`, `sat_conta_catparaesq`: rutas
  de auxiliares de contabilidad.
- `sat_consulta_cfdi_svc` y los 4 `sat_dm_*_svc`: endpoints SOAP (el de
  *Verificación* está confirmado en la doc del servicio; los demás, valídalos).
- `dip_linfonavit`, `dip_reglamentos`: nombre exacto del PDF en el índice de Diputados.

## `requires_auth: true` (13) — se omiten por defecto

Banxico SIE (token), descarga masiva CFDI / DIOT / 32-D / IDSE / REPSE (e.firma o
contraseña), INEGI API de indicadores (token). `verify.py` los marca
`omitido_requiere_auth`; con `--check-auth` los toca (esperar 401/403).

## Árbol `local_path` sugerido

```
corpus/
  esquemas-cfdi/        esquemas-contabilidad/
  sat-rmf-2026/         sat-guias/   sat-padrones/   sat-servicios/
  banxico/   inegi/   dof/   imss/   infonavit/   stps/
  leyes-federales/   datos-abiertos/
```

> Recordatorio del catálogo: **te faltan LISR, LIVA, LIEPS y reglamentos**
> (Diputados, `dip_lisr`/`dip_liva`/`dip_lieps`/`dip_reglamentos`). Sin ellos,
> los temas de cálculo de impuestos y deducciones quedan incompletos.
