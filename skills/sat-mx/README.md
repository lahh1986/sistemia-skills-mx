# sat-mx

> Skill de Claude Code para descargar la **Constancia de Situación Fiscal** y la **Opinión de Cumplimiento** del SAT México, sin entrar al portal.

Parte de [El Tianguis](https://eltianguis.sistemia.mx) — catálogo abierto de skills de Claude Code para México y Latinoamérica.

---

## Qué hace

Le dices a Claude:

> "Bájame mi Constancia de Situación Fiscal."

Y te entrega:

- El **PDF** descargado directo del SAT
- Los datos **parseados a JSON** (RFC, régimen fiscal, domicilio, código postal, obligaciones, fecha de emisión)

Lo mismo para tu **Opinión de Cumplimiento** (32-D):

- PDF descargado
- JSON con RFC, **sentido** (POSITIVA / NEGATIVA / SIN_OPINION), folio, fecha

Todo corre en tu computadora. **Tus credenciales (RFC + CIEC) nunca salen de ahí.**

---

## Instalación

```bash
# 1. Clona o copia este directorio donde tu Claude Code lo lea
cp -r sat-mx/ ~/.claude/skills/sat-mx/

# 2. Corre el setup una sola vez (verifica PHP, Composer, pdftotext, e instala las libs)
cd ~/.claude/skills/sat-mx
bash scripts/setup.sh
```

El setup te dice exactamente qué te falta instalar (PHP 8.2+, Composer, `poppler-utils`).

---

## Uso

Una vez instalado, basta con pedírselo a Claude en lenguaje natural:

- "Bájame mi Constancia"
- "Necesito mi Opinión de Cumplimiento positiva"
- "Saca mi 32-D del día"

Claude te pedirá tu **RFC + CIEC**, te mostrará el captcha para que lo resuelvas, y te entregará el PDF + el resumen.

---

## Seguridad

| Cosa | Cómo se maneja |
|---|---|
| Tu CIEC | Se pasa como variable de ambiente al script PHP, nunca como argumento de CLI (no aparece en `ps`) |
| Persistencia | Cero. La CIEC no se guarda en ningún archivo. |
| Tránsito | Todo corre local. Tus credenciales nunca llegan a Anthropic ni a Sistemia. |
| Captcha | Por default lo resuelves tú en consola. Opcional: integrar 2captcha o anti-captcha. |

Si quieres revisar el código antes de correrlo: son ~250 líneas en `scripts/`, todas abiertas.

---

## Lo que NO hace

- No reemplaza a tu contador
- No funciona con e.firma (.cer/.key) — solo con CIEC
- No declara impuestos ni hace ningún trámite escritural
- No descarga acuses, declaraciones ni facturas
- No guarda tu CIEC en ningún lado

---

## Créditos

Este skill se apoya **completamente** en el trabajo de [**phpcfdi**](https://www.phpcfdi.com) y sus mantenedores (autor original: Cesar Aguilera).

- [`phpcfdi/csf-sat-scraper`](https://github.com/phpcfdi/csf-sat-scraper) — el scraper de Constancia
- [`phpcfdi/opinion-cumplimiento-sat-scraper`](https://github.com/phpcfdi/opinion-cumplimiento-sat-scraper) — el scraper de Opinión
- [`phpcfdi/image-captcha-resolver`](https://github.com/phpcfdi/image-captcha-resolver) — los resolvedores de captcha

Si este skill te ahorra tiempo, **dales una star** en sus repos. Ellos llevan años manteniendo esto al día cada vez que el SAT modifica su portal.

---

## Cómo aportar

Issues y PRs bienvenidos:

- Bugs / sugerencias del skill: https://github.com/lahh1986/sistemia-skills-mx/issues
- Bugs de los scrapers en sí: report directo a phpcfdi (links arriba)

---

## Licencia

MIT (heredada de phpcfdi). Skill mantenido por [Sistemia](https://sistemia.mx).
