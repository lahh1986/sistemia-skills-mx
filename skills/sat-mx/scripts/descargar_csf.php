<?php

declare(strict_types=1);

/**
 * descargar_csf.php — Descarga Constancia de Situación Fiscal del SAT México.
 *
 * Inputs (variables de ambiente, NO argumentos de línea de comandos):
 *   SAT_RFC               (requerido) — RFC del contribuyente
 *   SAT_CIEC              (requerido) — Contraseña CIEC del portal SAT
 *   SAT_OUTPUT            (requerido) — Ruta destino del PDF
 *   SAT_CAPTCHA_PROVIDER  (opcional)  — "console" (default) | "anticaptcha"
 *   SAT_CAPTCHA_KEY       (requerido si SAT_CAPTCHA_PROVIDER=anticaptcha)
 *
 * Las credenciales se leen de env por seguridad — los argumentos
 * de línea de comandos quedan visibles en `ps` para otros procesos.
 */

require_once __DIR__ . '/../vendor/autoload.php';

use GuzzleHttp\RequestOptions;
use PhpCfdi\CsfSatScraper\HttpClientFactory;
use PhpCfdi\CsfSatScraper\Scraper;
use PhpCfdi\ImageCaptchaResolver\Resolvers\AntiCaptchaResolver;
use PhpCfdi\ImageCaptchaResolver\Resolvers\ConsoleResolver;

function fail(string $message, int $code = 1): never {
    fwrite(STDERR, "ERROR: {$message}\n");
    exit($code);
}

function readEnv(string $name, bool $required = true): ?string {
    $value = getenv($name);
    if ($value === false || $value === '') {
        if ($required) {
            fail("Falta variable de ambiente: {$name}");
        }
        return null;
    }
    return $value;
}

$rfc    = readEnv('SAT_RFC');
$ciec   = readEnv('SAT_CIEC');
$output = readEnv('SAT_OUTPUT');

$provider = readEnv('SAT_CAPTCHA_PROVIDER', false) ?? 'console';

$outputDir = dirname($output);
if (! is_dir($outputDir)) {
    fail("El directorio destino no existe: {$outputDir}");
}
if (! is_writable($outputDir)) {
    fail("El directorio destino no tiene permisos de escritura: {$outputDir}");
}

$captchaSolver = match ($provider) {
    'console'     => new ConsoleResolver(),
    'anticaptcha' => (function (): AntiCaptchaResolver {
        $key = readEnv('SAT_CAPTCHA_KEY');
        return AntiCaptchaResolver::create($key);
    })(),
    default       => fail("SAT_CAPTCHA_PROVIDER no soportado: {$provider}. Usa 'console' o 'anticaptcha'."),
};

try {
    $client = HttpClientFactory::create([
        'curl' => [
            CURLOPT_SSL_CIPHER_LIST => 'DEFAULT@SECLEVEL=1',
        ],
        RequestOptions::VERIFY => false,
    ]);

    fwrite(STDERR, "→ Conectando al portal SAT…\n");

    $scraper = Scraper::create($client, $captchaSolver, $rfc, $ciec);

    fwrite(STDERR, "→ Resolviendo captcha y autenticando…\n");
    fwrite(STDERR, "  (si aparece el captcha, escribe lo que ves y presiona Enter)\n");

    $pdfContent = $scraper->download();
    $bytes = file_put_contents($output, (string) $pdfContent);

    if ($bytes === false || $bytes < 1000) {
        fail("La descarga falló o el PDF está incompleto (bytes={$bytes}).");
    }

    fwrite(STDERR, "✓ Constancia descargada: {$output} ({$bytes} bytes)\n");
    echo $output . PHP_EOL;
    exit(0);
} catch (Throwable $e) {
    fail($e->getMessage(), 2);
}
