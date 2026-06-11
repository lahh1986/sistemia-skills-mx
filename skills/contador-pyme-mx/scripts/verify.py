#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify.py — Verifica el catálogo de fuentes de contador-pyme-mx.

Lee sources.json, hace HEAD (con fallback a GET) contra cada URL y escribe
sources.verified.json rellenando: estado_verificacion, http_status, final_url,
content_type, size_bytes_esperado, redirected, checked_at, error.

Solo usa la librería estándar de Python 3.8+. SIN dependencias (no requests).

Ejecuta esto desde la terminal del contador (red abierta). El sandbox donde se
generó el catálogo NO puede alcanzar dominios .gob.mx, por eso los estados
llegan como "pendiente": esta utilidad los resuelve.

Uso:
  python3 verify.py                      # verifica todo (omite los requires_auth)
  python3 verify.py --check-auth         # intenta también los de auth (suelen dar 401/403)
  python3 verify.py --only SAT           # filtra por institution / id / topic (substring)
  python3 verify.py --workers 8 --timeout 30
  python3 verify.py --insecure           # ignora errores de certificado TLS
  python3 verify.py --inplace            # sobrescribe sources.json en vez de crear .verified
  python3 verify.py --download DIR       # además descarga a DIR/<local_path> los OK descargables

Códigos de estado posibles en estado_verificacion:
  200_OK | 3xx_REDIRECT_OK | 401_AUTH | 403_FORBIDDEN | 404_NOT_FOUND |
  4xx | 5xx | ERROR:<motivo> | omitido_requiere_auth
"""
import argparse, json, os, ssl, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36 contador-pyme-mx/verify")
DESCARGABLES = {"pdf", "xsd", "csv", "zip", "xml"}


def _ctx(insecure):
    if insecure:
        c = ssl.create_default_context()
        c.check_hostname = False
        c.verify_mode = ssl.CERT_NONE
        return c
    return ssl.create_default_context()


def _open(url, method, timeout, ctx, read_bytes=0):
    """Devuelve (status, final_url, headers, body_bytes). Lanza en fallo de red."""
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": UA,
        "Accept": "*/*",
        "Accept-Language": "es-MX,es;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        body = r.read(read_bytes) if read_bytes else b""
        return r.status, r.geturl(), dict(r.headers), body


def check_one(item, timeout, ctx, want_size=True):
    url = item.get("url")
    res = {
        "estado_verificacion": "pendiente",
        "http_status": None,
        "final_url": None,
        "content_type": None,
        "size_bytes_esperado": None,
        "redirected": False,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "error": None,
    }
    if not url:
        res["estado_verificacion"] = "ERROR:sin_url"
        return res

    status = final = headers = None
    try:
        status, final, headers, _ = _open(url, "HEAD", timeout, ctx)
    except urllib.error.HTTPError as e:
        status, final, headers = e.code, getattr(e, "url", url), dict(e.headers or {})
    except Exception as e:
        # HEAD falló a nivel red: reintenta con GET
        try:
            status, final, headers, _ = _open(url, "GET", timeout, ctx, read_bytes=2048)
        except urllib.error.HTTPError as e2:
            status, final, headers = e2.code, getattr(e2, "url", url), dict(e2.headers or {})
        except Exception as e2:
            res["estado_verificacion"] = f"ERROR:{type(e2).__name__}"
            res["error"] = str(e2)[:200]
            return res

    # Algunos hosts rechazan HEAD (405/400/403/501) pero responden GET.
    if status in (400, 403, 405, 406, 501):
        try:
            status, final, headers, _ = _open(url, "GET", timeout, ctx, read_bytes=2048)
        except urllib.error.HTTPError as e:
            status, final, headers = e.code, getattr(e, "url", url), dict(e.headers or {})
        except Exception:
            pass

    res["http_status"] = status
    res["final_url"] = final
    res["redirected"] = bool(final and final.rstrip("/") != url.rstrip("/"))
    headers = headers or {}
    res["content_type"] = headers.get("Content-Type") or headers.get("content-type")

    # tamaño
    cl = headers.get("Content-Length") or headers.get("content-length")
    if cl and cl.isdigit():
        res["size_bytes_esperado"] = int(cl)
    elif want_size and 200 <= (status or 0) < 300 and (item.get("format") in DESCARGABLES):
        # sin Content-Length: descarga para medir
        try:
            _, _, _, body = _open(url, "GET", timeout, ctx, read_bytes=20_000_000)
            res["size_bytes_esperado"] = len(body)
        except Exception:
            pass

    if status and 200 <= status < 300:
        res["estado_verificacion"] = "200_OK"
    elif status and 300 <= status < 400:
        res["estado_verificacion"] = "3xx_REDIRECT_OK"
    elif status == 401:
        res["estado_verificacion"] = "401_AUTH"
    elif status == 403:
        res["estado_verificacion"] = "403_FORBIDDEN"
    elif status == 404:
        res["estado_verificacion"] = "404_NOT_FOUND"
    elif status and 400 <= status < 500:
        res["estado_verificacion"] = f"{status}"
    elif status and status >= 500:
        res["estado_verificacion"] = f"{status}"
    else:
        res["estado_verificacion"] = "ERROR:sin_status"
    return res


def maybe_download(item, dst_root, timeout, ctx):
    lp, url = item.get("local_path"), item.get("url")
    if not (lp and url) or item.get("format") not in DESCARGABLES:
        return None
    path = os.path.join(dst_root, lp)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        _, _, _, body = _open(url, "GET", timeout, ctx, read_bytes=200_000_000)
        with open(path, "wb") as f:
            f.write(body)
        return len(body)
    except Exception as e:
        return f"ERR:{e}"


def main():
    ap = argparse.ArgumentParser(description="Verifica sources.json de contador-pyme-mx")
    ap.add_argument("--input", default="sources.json")
    ap.add_argument("--output", default="sources.verified.json")
    ap.add_argument("--inplace", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=25)
    ap.add_argument("--only", default=None, help="substring en institution/id/topic")
    ap.add_argument("--check-auth", action="store_true", help="también prueba requires_auth")
    ap.add_argument("--insecure", action="store_true")
    ap.add_argument("--no-size", action="store_true", help="no descargar para medir tamaño")
    ap.add_argument("--download", default=None, metavar="DIR",
                    help="descarga los OK descargables al árbol local_path bajo DIR")
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    ctx = _ctx(args.insecure)

    def selected(it):
        if not args.only:
            return True
        s = args.only.lower()
        return (s in it.get("institution", "").lower()
                or s in it.get("id", "").lower()
                or any(s in t.lower() for t in it.get("topics", [])))

    todo, skipped_auth = [], 0
    for it in data:
        if not selected(it):
            continue
        if it.get("requires_auth") and not args.check_auth:
            it["estado_verificacion"] = "omitido_requiere_auth"
            it["checked_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            skipped_auth += 1
        else:
            todo.append(it)

    print(f"Verificando {len(todo)} fuentes "
          f"(omitidas por auth: {skipped_auth}; workers={args.workers}; timeout={args.timeout}s)\n")

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(check_one, it, args.timeout, ctx, not args.no_size): it for it in todo}
        done = 0
        for fut in as_completed(futs):
            it = futs[fut]
            it.update(fut.result())
            done += 1
            mark = "OK " if it["estado_verificacion"] == "200_OK" else "!! "
            sz = it.get("size_bytes_esperado")
            print(f"[{done:>3}/{len(todo)}] {mark}{it['estado_verificacion']:<18} "
                  f"{(str(sz)+'B') if sz else '':>10}  {it['id']}")

    if args.download:
        print(f"\nDescargando OK descargables a {args.download} ...")
        for it in data:
            if it.get("estado_verificacion") == "200_OK":
                r = maybe_download(it, args.download, args.timeout, ctx)
                if isinstance(r, int):
                    print(f"  saved {r:>9}B  {it['local_path']}")
                elif r:
                    print(f"  {r}  {it.get('local_path')}")

    out = args.input if args.inplace else args.output
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # resumen
    from collections import Counter
    c = Counter(it["estado_verificacion"] for it in data)
    print("\n===== RESUMEN =====")
    for k, v in sorted(c.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {v:>3}  {k}")
    bad = [it for it in data if it["estado_verificacion"] not in
           ("200_OK", "omitido_requiere_auth", "3xx_REDIRECT_OK")]
    if bad:
        print("\n----- REVISAR (no-OK) -----")
        for it in bad:
            print(f"  {it['estado_verificacion']:<18} {it['id']}")
            print(f"      {it['url']}")
            if it.get("final_url") and it["final_url"] != it["url"]:
                print(f"      -> {it['final_url']}")
    print(f"\nEscrito: {out}")


if __name__ == "__main__":
    main()
