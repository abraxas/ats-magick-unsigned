#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-ats-magick-unsigned}"
export PYTHONUNBUFFERED=1

LABEL="ats-magick-unsigned"
WITNESS="ATS-MAGICK-UNSIGNED-WITNESS"
IMAGE="${ATS_LAB_IMAGE:-ats-10.2.0-lab:local}"
LOCK="${ATS_LAB_LOCK:-/tmp/ats-10.2.0-lab.lock}"
SRC_CONTEXT="../../client-reviews/trafficserver/src"

down() {
  echo "== docker compose down -v =="
  docker compose -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans || true
}

fail_setup() {
  echo "FAIL ${LABEL} $* ${WITNESS}" | tee poc-last-run.txt
  docker compose -p "${COMPOSE_PROJECT_NAME}" logs --no-color --tail=80 || true
  down
  exit 1
}

ensure_image() {
  echo "== flock ${LOCK} for ${IMAGE} =="
  python3 - "${LOCK}" "${IMAGE}" "${SRC_CONTEXT}" <<'PY'
import fcntl
import os
import subprocess
import sys

lock_path, image, src_context = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(os.path.dirname(lock_path) or ".", exist_ok=True)
fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o644)
fcntl.flock(fd, fcntl.LOCK_EX)


def has_magick() -> bool:
    inspect = subprocess.run(
        ["docker", "image", "inspect", image],
        capture_output=True,
        check=False,
    )
    if inspect.returncode != 0:
        return False
    probe = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "ls",
            image,
            "/opt/ats/libexec/trafficserver/magick.so",
        ],
        capture_output=True,
        check=False,
    )
    return probe.returncode == 0


if has_magick():
    print(f"IOC image-ready {image} magick.so=yes", flush=True)
    sys.exit(0)

print(f"== docker build -t {image} ==", flush=True)
build = subprocess.run(
    ["docker", "build", "-t", image, "-f", "Dockerfile", src_context],
    check=False,
)
if build.returncode != 0:
    sys.exit(build.returncode)
if not has_magick():
    print("FAIL image-missing-magick.so", flush=True)
    sys.exit(2)
print(f"IOC image-built {image} magick.so=yes", flush=True)
sys.exit(0)
PY
}

echo "== prepare oracle dirs =="
rm -rf oracle-unsigned oracle-signed
mkdir -p oracle-unsigned oracle-signed
chmod 1777 oracle-unsigned oracle-signed

echo "== docker compose down (clean) =="
down

if ! ensure_image; then
  fail_setup "image-build-failed"
fi

echo "== docker compose up =="
up_ok=0
for attempt in $(seq 1 8); do
  if docker compose -p "${COMPOSE_PROJECT_NAME}" up -d; then
    up_ok=1
    break
  fi
  echo "IOC compose-up-retry attempt=${attempt}"
  sleep 20
  down
done
if [[ "${up_ok}" != 1 ]]; then
  fail_setup "compose-up-failed"
fi

echo "== wait origin 127.0.0.1:18801 and ATS 18800/18802 =="
ready=0
for i in $(seq 1 60); do
  if python3 - <<'PY'
import socket
for port in (18800, 18801, 18802):
    s = socket.create_connection(("127.0.0.1", port), 2)
    s.close()
PY
  then
    ready=1
    echo "IOC tcp-ready attempt=${i}"
    break
  fi
  echo "IOC tcp-wait attempt=${i}"
  sleep 2
done
if [[ "${ready}" != 1 ]]; then
  fail_setup "ports-not-ready"
fi

echo "== poc.py =="
set +e
python3 ./poc.py | tee poc-last-run.txt
rc=${PIPESTATUS[0]}
set -e

if ! tail -n1 poc-last-run.txt 2>/dev/null | grep -qE '^(SUCCESS|FAIL) '; then
  echo "FAIL ${LABEL} poc-exit=${rc} ${WITNESS}" >> poc-last-run.txt
  rc=1
fi

down
exit "${rc}"
