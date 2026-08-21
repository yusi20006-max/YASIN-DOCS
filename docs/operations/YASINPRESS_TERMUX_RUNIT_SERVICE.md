# YasinPress-Rewrite — Termux / runit Persistent Service

## Status

**Confirmed — implemented and validated on Termux.**

Date: 2026-08-21

Repository:

`yusi20006-max/YasinPress-Rewrite-`

## Goal

Keep `YasinPress-Rewrite-` running continuously under Termux using `runit`, so the application is supervised by the Termux service manager and automatically restarted if its process exits.

## Final Architecture

```text
runsvdir
  └── runsv yasinpress
        └── ~/.venv/bin/yasinpress run
```

The service is registered under:

`$PREFIX/var/service/yasinpress`

The service is therefore discovered and supervised by the existing Termux `runsvdir` instance:

`$PREFIX/var/service`

## Final Service Definition

The final working service contains only the main `run` script:

```sh
#!/data/data/com.termux/files/usr/bin/sh

cd "$HOME/YasinPress-Rewrite-" || exit 1

exec "$HOME/YasinPress-Rewrite-/.venv/bin/yasinpress" run
```

The script is executable.

## Installation / Reconstruction

The working service was created with:

```sh
SERVICE="$PREFIX/var/service/yasinpress"

sv down "$SERVICE" 2>/dev/null || true
sleep 2
rm -rf "$SERVICE/log"

cat > "$SERVICE/run" <<'EOF'
#!/data/data/com.termux/files/usr/bin/sh

cd "$HOME/YasinPress-Rewrite-" || exit 1

exec "$HOME/YasinPress-Rewrite-/.venv/bin/yasinpress" run
EOF

chmod +x "$SERVICE/run"
sv up "$SERVICE"
```

## Why the `~/service/yasinpress` Version Was Removed

An initial service was created under:

`$HOME/service/yasinpress`

This location was not being supervised by the active Termux `runsvdir`, whose service directory was confirmed as:

`$PREFIX/var/service`

The Home service definition was therefore removed. The canonical Termux service location is:

`$PREFIX/var/service/yasinpress`

## Logger Investigation

An initial attempt used the conventional runit nested logger layout:

```text
$PREFIX/var/service/yasinpress/
├── run
└── log/
    └── run
```

The logger script was:

```sh
#!/data/data/com.termux/files/usr/bin/sh

mkdir -p "$HOME/.local/share/yasinpress/log"

exec svlogd "$HOME/.local/share/yasinpress/log"
```

However, the running `runsv yasinpress` repeatedly reported:

```text
warning: .../yasinpress/log: unable to open supervise/ok: file does not exist
```

The expected `log/supervise/ok` was never created, and no `current` log file appeared in:

`~/.local/share/yasinpress/log`

`svlogd` itself was confirmed to exist at:

`$PREFIX/bin/svlogd`

The main service supervisor was healthy, but the nested logger was not being initialized correctly in this Termux setup.

## Resolution

The logger subservice was removed from the final configuration rather than continuing to modify a working application supervisor.

The final service intentionally contains only the main `run` script. Persistent file logging is **not currently part of the confirmed service configuration** and can be added later as a separate operational improvement.

## Existing Process Cleanup

During troubleshooting, stale YasinPress processes from earlier manual/service attempts were found. They included old `yasinpress run` processes and a stopped (`T`) `python3 -m yasinpress.cli.main run` process.

The final validation confirmed that the active process is the one spawned by the current `runsv yasinpress` supervisor.

## Validation

### 1. runsvdir discovery

Confirmed active:

```text
/data/data/com.termux/files/usr/bin/runsvdir /data/data/com.termux/files/usr/var/service
```

### 2. Service status

Confirmed:

```text
run: .../var/service/yasinpress: (pid 5331) ...
```

After the restart test, the service was running as a new process:

```text
run: .../var/service/yasinpress: (pid 6253) 5s
```

### 3. CLI health

The YasinPress CLI responded successfully:

```text
exit=0
```

### 4. Automatic restart validation

The active application process was deliberately terminated:

```sh
OLD_PID="$(pgrep -f "$HOME/YasinPress-Rewrite-/.venv/bin/yasinpress run" | head -1)"
kill "$OLD_PID"
```

Before termination the process was:

```text
PID 5331
```

Five seconds later `runit` had automatically started a replacement process:

```text
PID 6253
```

This confirms that the service is supervised and self-restarting.

## Operational Result

YasinPress-Rewrite is now considered **permanently supervised under runit** on the configured Termux environment.

Expected lifecycle:

```text
Termux runsvdir
       ↓
   runsv yasinpress
       ↓
 yasinpress run
       ↓
 process exits
       ↓
 runsv detects exit
       ↓
 yasinpress run starts again
```

## Current Limitations

- Persistent `svlogd` file logging is not enabled in the final configuration.
- The service depends on the existing Termux `runsvdir` being active.
- The application continues to use the project's existing virtual environment at `.venv`.
- This document records the confirmed Termux deployment state; it does not change YasinPress application code.

## Future Work

Do not destabilize the current service configuration merely to add logging.

When YasinPress is revisited, logging can be implemented as a separate operational task and validated independently.

The current priority is to keep the stable YasinPress deployment unchanged while the broader Yasin ecosystem work continues, including Yasin MCP and Yasin Operations.

## Evidence Classification

- **Confirmed:** `runit` supervises the YasinPress process.
- **Confirmed:** YasinPress automatically restarts after its process is killed.
- **Confirmed:** the final service location is `$PREFIX/var/service/yasinpress`.
- **Confirmed:** the main service `run` script is executable and launches the project's `.venv/bin/yasinpress run`.
- **Unresolved / Future:** persistent `svlogd` file logging.
