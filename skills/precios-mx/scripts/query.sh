#!/usr/bin/env bash
# Wrapper de DuckDB para queries del corpus precios-mx
# Uso:
#   ./query.sh "<SQL>"
#   ./query.sh -f archivo.sql
#   ./query.sh -i  (modo interactivo)

set -euo pipefail

DB_PATH="${PRECIOS_MX_DB:-/Volumes/Storage/sistemia-skills-mx/research/precios.duckdb}"

if [ ! -f "$DB_PATH" ]; then
  echo "ERROR: no se encuentra precios.duckdb en $DB_PATH" >&2
  echo "Set PRECIOS_MX_DB env var to override." >&2
  exit 1
fi

if [ "$#" -eq 0 ]; then
  cat <<'USAGE'
precios-mx query helper

Uso:
  query.sh "SQL"                Ejecuta un query inline
  query.sh -f archivo.sql       Ejecuta queries desde archivo
  query.sh -i                   Modo interactivo (DuckDB CLI)

Tabla: precios
Columns: producto, presentacion, marca, categoria, catalogo, precio,
         fecha_registro, cadena_comercial, giro, nombre_comercial,
         direccion, estado, municipio, latitud, longitud, filename

Ejemplos:
  query.sh "SELECT MEDIAN(precio) FROM precios WHERE producto ILIKE '%tortilla%' AND fecha_registro >= CURRENT_DATE - INTERVAL '90 days'"

  query.sh "SELECT estado, MEDIAN(precio) p FROM precios
            WHERE producto ILIKE '%refresco%' AND marca ILIKE '%coca%'
              AND fecha_registro >= CURRENT_DATE - INTERVAL '180 days'
            GROUP BY estado ORDER BY p"
USAGE
  exit 0
fi

case "$1" in
  -i)
    exec duckdb "$DB_PATH"
    ;;
  -f)
    [ -z "${2:-}" ] && { echo "ERROR: -f requires archivo.sql" >&2; exit 1; }
    exec duckdb "$DB_PATH" < "$2"
    ;;
  *)
    exec duckdb "$DB_PATH" "$1"
    ;;
esac
