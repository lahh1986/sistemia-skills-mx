#!/usr/bin/env bash
# setup.sh — verifica dependencias y prepara el skill sat-mx
# Corre una vez antes del primer uso.

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SKILL_DIR"

red()    { printf '\033[31m%s\033[0m\n' "$*"; }
green()  { printf '\033[32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[33m%s\033[0m\n' "$*"; }
bold()   { printf '\033[1m%s\033[0m\n' "$*"; }

bold "sat-mx — setup"
echo

detect_os() {
  case "$(uname -s)" in
    Darwin) echo "mac" ;;
    Linux)  echo "linux" ;;
    *)      echo "other" ;;
  esac
}

OS="$(detect_os)"

# 1. PHP 8.2+
check_php() {
  if ! command -v php >/dev/null 2>&1; then
    red "✗ PHP no está instalado."
    case "$OS" in
      mac)   yellow "  Instálalo con: brew install php" ;;
      linux) yellow "  Instálalo con: sudo apt install php-cli php-curl php-xml php-mbstring" ;;
      *)     yellow "  Instala PHP 8.2+ para tu sistema operativo." ;;
    esac
    return 1
  fi

  PHP_VERSION="$(php -r 'echo PHP_VERSION;')"
  PHP_MAJOR="$(php -r 'echo PHP_MAJOR_VERSION;')"
  PHP_MINOR="$(php -r 'echo PHP_MINOR_VERSION;')"

  if (( PHP_MAJOR < 8 )) || (( PHP_MAJOR == 8 && PHP_MINOR < 2 )); then
    red "✗ PHP $PHP_VERSION es muy viejo. Necesitas PHP 8.2 o superior."
    return 1
  fi

  green "✓ PHP $PHP_VERSION"
  return 0
}

# 2. Composer
check_composer() {
  if ! command -v composer >/dev/null 2>&1; then
    yellow "→ Composer no está instalado. Intentando instalar..."
    case "$OS" in
      mac)
        if command -v brew >/dev/null 2>&1; then
          brew install composer
        else
          red "✗ No se encontró Homebrew. Instala Composer manualmente: https://getcomposer.org/download/"
          return 1
        fi
        ;;
      linux)
        local installer="/tmp/composer-setup.php"
        php -r "copy('https://getcomposer.org/installer', '$installer');"
        sudo php "$installer" --install-dir=/usr/local/bin --filename=composer
        rm "$installer"
        ;;
      *)
        red "✗ Instala Composer manualmente: https://getcomposer.org/download/"
        return 1
        ;;
    esac
  fi

  green "✓ Composer $(composer --version --no-ansi 2>/dev/null | head -1)"
  return 0
}

# 3. pdftotext (de poppler, para parsear PDFs)
check_pdftotext() {
  if ! command -v pdftotext >/dev/null 2>&1; then
    yellow "⚠ pdftotext no está instalado. El skill funciona sin él pero NO podrá parsear los PDFs a JSON."
    case "$OS" in
      mac)   yellow "  Recomendado: brew install poppler" ;;
      linux) yellow "  Recomendado: sudo apt install poppler-utils" ;;
    esac
    return 0
  fi
  green "✓ pdftotext (poppler)"
  return 0
}

# 4. python3 (para parse_pdf.py)
check_python() {
  if ! command -v python3 >/dev/null 2>&1; then
    yellow "⚠ python3 no está instalado. Necesario para parsear PDFs."
    return 0
  fi
  green "✓ python3 $(python3 --version 2>&1 | awk '{print $2}')"
  return 0
}

# 5. composer install
install_deps() {
  bold "Instalando librerías de phpcfdi (composer)..."
  if [ -d vendor ]; then
    yellow "  vendor/ ya existe, corriendo composer update..."
    composer update --no-interaction --no-progress
  else
    composer install --no-interaction --no-progress
  fi
  green "✓ Librerías instaladas en vendor/"
}

# Ejecución
bold "1. Verificando PHP..."
check_php || exit 1
echo

bold "2. Verificando Composer..."
check_composer || exit 1
echo

bold "3. Verificando pdftotext..."
check_pdftotext
echo

bold "4. Verificando python3..."
check_python
echo

bold "5. Instalando dependencias..."
install_deps
echo

green "✓ Setup completo. Ya puedes usar sat-mx."
echo
yellow "Siguiente paso: pídele a Claude que descargue tu Constancia o tu Opinión de Cumplimiento."
