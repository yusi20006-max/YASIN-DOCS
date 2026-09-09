# Yasin Ecosystem — Termux Installation Runbook

**Status:** Canonical installation companion to `docs/STARTUP_RUNBOOK.md`
**Platform:** Android / Termux / ARM64
**Verified:** 2026-09-08

## 1. Installation rule

The five runtime repositories below must be installed in **one bootstrap phase** on a fresh Termux device:

- `YasinHub`
- `Yasin-agent`
- `YasinRelay`
- `Yasin-AI`
- `YasinPress-Rewrite-`

Do not make YasinPress a separate recovery phase. The initial bootstrap must use **runtime dependencies only**; do not install `.[dev]` during the first installation.

Development/test tooling may be installed later when required.

## 2. Verified installation outcome — 2026-09-08

Fresh device: Redmi Note 12 4G / Android 15 / Termux / ARM64.

Verified:

- `YasinHub`: `.venv` created, editable install completed, pytest available.
- `Yasin-agent`: `.venv` created, editable install completed, pytest installed/verified.
- `YasinRelay`: editable runtime install completed as `yasin-relay==2.0.0`, pytest installed/verified.
- `Yasin-AI`: editable runtime install completed as `yasinai==1.1.4`, pytest/pytest-cov installed.
- `YasinPress-Rewrite-`: runtime dependencies installed and editable install completed as `yasinpress-rewrite==1.0.0`.

The first YasinPress attempt used `.[dev]` and was terminated with signal 9 while building development tooling. Runtime dependencies themselves were not the failure. The successful recovery installed runtime dependencies only, then used `pip install --no-deps -e .`.

Final YasinPress evidence:

```text
YasinPress IMPORT=OK
YasinPress RUNTIME INSTALL=OK
```

## 3. One-pass bootstrap command

For a fresh device, use this single installation phase. It deliberately avoids YasinPress development extras.

```bash
set -e

export YASIN_ECOSYSTEM_ROOT="$HOME/YasinEco"

cd "$YASIN_ECOSYSTEM_ROOT/YasinHub"
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e .
.venv/bin/python -m pip install pytest

cd "$YASIN_ECOSYSTEM_ROOT/Yasin-agent"
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e .
.venv/bin/python -m pip install pytest

cd "$YASIN_ECOSYSTEM_ROOT/YasinRelay"
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e .
.venv/bin/python -m pip install pytest

cd "$YASIN_ECOSYSTEM_ROOT/Yasin-AI"
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e .
.venv/bin/python -m pip install pytest pytest-cov

cd "$YASIN_ECOSYSTEM_ROOT/YasinPress-Rewrite-"
python -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install PyYAML>=6.0.2 httpx>=0.27.0 feedparser>=6.0.11 tzdata>=2026.3 jdatetime>=5.2.0
.venv/bin/python -m pip install --no-deps -e .

cd "$YASIN_ECOSYSTEM_ROOT"

printf '\n=== YASIN INSTALLATION CHECK ===\n'
for repo in YasinHub Yasin-agent YasinRelay Yasin-AI YasinPress-Rewrite-; do
    printf '%-24s ' "$repo"
    test -x "$repo/.venv/bin/python" && echo 'VENV=OK' || echo 'VENV=MISSING'
done

printf '\n=== IMPORT CHECK ===\n'
YasinHub/.venv/bin/python -c 'import yasinhub; print("YasinHub IMPORT=OK")'
Yasin-agent/.venv/bin/python -c 'import agent_platform; print("Yasin-agent IMPORT=OK")'
YasinRelay/.venv/bin/python -c 'import yasinrelay; print("YasinRelay IMPORT=OK")'
Yasin-AI/.venv/bin/python -c 'import yasinai; print("Yasin-AI IMPORT=OK")'
YasinPress-Rewrite-/.venv/bin/python -c 'import yasinpress; print("YasinPress IMPORT=OK")'

printf '\nYASIN RUNTIME INSTALL=OK\n'
```

## 4. Important constraint

Do not change the bootstrap back to `pip install -e ".[dev]"` or equivalent for YasinPress. On Android/Termux this can trigger unnecessary development-tool builds and memory/resource pressure. Runtime installation is the default bootstrap path.

Installation success does **not** mean service RUNNING, lifecycle acceptance, real publish PASS, or PWA visual PASS. Those remain separate runtime/browser acceptance gates.
