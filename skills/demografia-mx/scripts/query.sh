#!/usr/bin/env bash
# Wrapper de DuckDB para queries del corpus demografia-mx
set -euo pipefail

DB_PATH="${DEMOGRAFIA_MX_DB:-/Volumes/Storage/sistemia-skills-mx/research/demografia.duckdb}"

if [ ! -f "$DB_PATH" ]; then
  echo "ERROR: no se encuentra demografia.duckdb en $DB_PATH" >&2
  echo "Corre primero: python3 $(dirname "$0")/build_db.py" >&2
  exit 1
fi

if [ "$#" -eq 0 ]; then
  cat <<'USAGE'
demografia-mx query helper

Uso:
  query.sh "SQL"                Ejecuta un query inline
  query.sh -f archivo.sql       Ejecuta desde archivo
  query.sh -i                   Modo interactivo DuckDB

Tablas:
  poblacion           anio | entidad | cve_geo | edad | sexo | poblacion
  esperanza_vida      anio | entidad | sexo | esperanza
  poblacion_total     (vista: agregado anio × entidad)
  poblacion_por_grupo (vista: grupos de edad 0-4, 5-14, 15-17, 18-24, 25-34, 35-44, 45-54, 55-64, 65+)

Ejemplos:
  query.sh "SELECT SUM(poblacion) FROM poblacion WHERE anio=2026 AND entidad='Jalisco' AND sexo='Mujeres' AND edad BETWEEN 25 AND 34"
USAGE
  exit 0
fi

case "$1" in
  -i) exec duckdb "$DB_PATH" ;;
  -f) exec duckdb "$DB_PATH" < "$2" ;;
  *)  exec duckdb "$DB_PATH" "$1" ;;
esac
