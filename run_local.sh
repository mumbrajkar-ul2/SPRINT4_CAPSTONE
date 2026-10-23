#!/usr/bin/env bash
# Native Force Fab stack. This script starts processes. It does not copy a database onto a live process.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
RUN="$ROOT/.run"
mkdir -p "$RUN"
PORTS=(8095 8080 8090 8091 8092 8100 8110)

port_busy() {
  local port="$1"
  if command -v ss >/dev/null 2>&1; then
    ss -ltn | grep -q ":${port} "
    return
  fi
  python - "$port" <<'PY'
import socket, sys
sock = socket.socket()
sock.settimeout(0.2)
busy = sock.connect_ex(("127.0.0.1", int(sys.argv[1]))) == 0
sock.close()
sys.exit(0 if busy else 1)
PY
}

any_busy() {
  local port
  for port in "${PORTS[@]}"; do
    if port_busy "$port"; then
      return 0
    fi
  done
  return 1
}

stop_all() {
  if [[ -d "$RUN" ]]; then
    local pidfile
    for pidfile in "$RUN"/*.pid; do
      [[ -f "$pidfile" ]] || continue
      local pid
      pid="$(cat "$pidfile" || true)"
      if [[ -n "${pid}" ]]; then
        kill "$pid" 2>/dev/null || true
      fi
      rm -f "$pidfile"
    done
  fi
}

start_one() {
  local name="$1"
  local port="$2"
  shift 2
  if port_busy "$port"; then
    echo "Port ${port} is already in use. Stop the stack before starting ${name}."
    exit 1
  fi
  setsid nohup "$@" >"$RUN/${name}.log" 2>&1 &
  echo $! >"$RUN/${name}.pid"
  local tries=0
  while (( tries < 30 )); do
    if port_busy "$port"; then
      return 0
    fi
    sleep 0.4
    tries=$((tries + 1))
  done
  echo "${name} did not open port ${port}."
  exit 1
}

sync_source() {
  local dest="${1:-}"
  if [[ -z "$dest" ]]; then
    echo "sync-source needs a destination directory."
    exit 1
  fi
  if any_busy; then
    echo "A Force Fab port is still open. Stop the stack before copying source."
    exit 1
  fi
  mkdir -p "$dest"
  tar -C "$ROOT" \
    --exclude='*.sqlite3' \
    --exclude='*.sqlite3-wal' \
    --exclude='*.sqlite3-shm' \
    --exclude='*-wal' \
    --exclude='*-shm' \
    --exclude='*-journal' \
    --exclude='.run' \
    --exclude='operations/model-replay' \
    --exclude='node_modules' \
    -cf - . | tar -C "$dest" -xf -
  echo "Copied source to ${dest}. Database files and replay files stayed where they were."
}

cmd="${1:-status}"
case "$cmd" in
  stop)
    stop_all
    echo "Stopped."
    ;;
  status)
    for port in "${PORTS[@]}"; do
      if port_busy "$port"; then
        echo "port ${port} open"
      else
        echo "port ${port} closed"
      fi
    done
    ;;
  sync-source)
    sync_source "${2:-}"
    ;;
  start|restart)
    if [[ "$cmd" == "restart" ]]; then
      stop_all
      sleep 1
    fi
    if [[ ! -f "$RUN/cookie_secret" ]]; then
      python -c "import secrets; print(secrets.token_hex(32))" >"$RUN/cookie_secret"
    fi
    export FF_COOKIE_SECRET="$(cat "$RUN/cookie_secret")"
    export FF_IDP_PUBLIC_URL="${FF_IDP_PUBLIC_URL:-http://127.0.0.1:8095}"
    export FF_IDP_URL="$FF_IDP_PUBLIC_URL"
    export FF_STATE_DIR="$RUN/identity"
    export FF_DEMO_HINTS=1
    export FF_ENV=local
    export FABPULSE_API_KEY="${FABPULSE_API_KEY:-local-demo-only}"
    export MODEL_MODE="${MODEL_MODE:-replay}"
    export PYTHONPATH="$ROOT:$ROOT/context-lake"
    cd "$ROOT"
    start_one identity 8095 python -m uvicorn apps.identity.server:app --host 127.0.0.1 --port 8095
    start_one lake-rest 8091 python -m uvicorn rest_server:app --host 127.0.0.1 --port 8091
    start_one lake-mcp 8092 python -m uvicorn mcp_server:app --host 127.0.0.1 --port 8092
    PYTHONPATH="$ROOT:$ROOT/context-lake:$ROOT/fabpulse-legacy-workshop-v8-Semiconductor/fabpulse-legacy" \
      start_one app-a 8100 python -m uvicorn apps.app_a.server:app --host 127.0.0.1 --port 8100
    PYTHONPATH="$ROOT:$ROOT/context-lake" \
      start_one app-b 8110 python -m uvicorn apps.app_b.server:app --host 127.0.0.1 --port 8110
    echo "Force Fab is up."
    echo "Application A http://127.0.0.1:8100"
    echo "Application B http://127.0.0.1:8110"
    echo "Identity      http://127.0.0.1:8095"
    ;;
  *)
    echo "Use start, stop, status, restart, or sync-source."
    exit 1
    ;;
esac
