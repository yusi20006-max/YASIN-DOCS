# Termux Canonical Project Layout

## Status

**Confirmed operational rule — canonical ecosystem local layout.**

All Yasin Ecosystem repositories used together on Termux MUST be installed directly under:

```text
~/yasineco/
```

Each repository uses its canonical GitHub repository name as its directory name. Do not use legacy paths such as `~/yasin-ecosystem/`, `*-main`, or nested clone directories unless a repository explicitly documents a different runtime requirement.

## Canonical layout

```text
~/yasineco/
├── Yasin-Core/
├── Yasin-Agent/
├── Yasin-AI/
├── YasinHub/
├── YasinCLI/
├── YasinRelay/
├── YasinFeed/
├── YasinPress/
└── YASIN-DOCS/
```

## Canonical GitHub owner

```text
https://github.com/yusi20006-max
```

## Standard clean clone command

When a repository must be replaced from GitHub, remove the old local directory first and clone directly into its canonical path:

```bash
mkdir -p "$HOME/yasineco"
rm -rf "$HOME/yasineco/<REPO>"
git clone "https://github.com/yusi20006-max/<REPO>.git" "$HOME/yasineco/<REPO>"
```

Example:

```bash
mkdir -p "$HOME/yasineco"
rm -rf "$HOME/yasineco/Yasin-Agent"
git clone https://github.com/yusi20006-max/Yasin-agent.git "$HOME/yasineco/Yasin-Agent"
```

## Bootstrap / reinstall all canonical repositories

Use this only when intentionally rebuilding the complete local ecosystem. It deletes the existing local clones listed below before cloning fresh copies from `main`:

```bash
set -e
mkdir -p "$HOME/yasineco"

for repo in \
  Yasin-Core \
  Yasin-Agent \
  Yasin-AI \
  YasinHub \
  YasinCLI \
  YasinRelay \
  YasinFeed \
  YasinPress \
  YASIN-DOCS
 do
  rm -rf "$HOME/yasineco/$repo"
  git clone --branch main "https://github.com/yusi20006-max/$repo.git" "$HOME/yasineco/$repo"
done
```

## Runtime path rule

Configuration, registries, service definitions, runit scripts, CLI commands, documentation, and automation MUST resolve repositories from the canonical `$HOME/yasineco/<REPO>` layout.

In particular:

- `Yasin-Agent` → `$HOME/yasineco/Yasin-Agent`
- `YasinHub` → `$HOME/yasineco/YasinHub`
- `Yasin-AI` → `$HOME/yasineco/Yasin-AI`
- `YasinRelay` → `$HOME/yasineco/YasinRelay`
- `YasinFeed` → `$HOME/yasineco/YasinFeed`
- `YasinPress` → `$HOME/yasineco/YasinPress`

Legacy locations such as `$HOME/yasin-ecosystem/` and directory names ending in `-main` are not canonical and MUST NOT be written into active runtime configuration.

## AI coding-agent rule

Before cloning, reinstalling, moving, or configuring a Yasin project on Termux, the agent MUST apply this document's canonical layout. If an existing configuration points to a legacy path, repair the configuration to the canonical `$HOME/yasineco/<REPO>` path rather than creating another clone at the legacy location.

## Important distinction

This document defines the **local filesystem convention**. Individual repositories remain the source of truth for their own dependency installation, virtual environments, environment variables, and runtime commands.

Do not commit secrets or service tokens. Tokens must come from the established local environment/configuration mechanism.
