# Termux Backup Manager — Project Architecture Record

## Evidence Level

**README-verified / source audit pending**

## Identity

Repository: `yusi20006-max/Termux-BackupManager`

## Purpose

Termux Backup Manager provides backup, restore, migration, and backup-management workflows for Termux environments.

## Documented Features

- Google Drive backup
- System restore
- Migration support
- Backup management

## Runtime / Dependencies

- Termux
- `rclone`
- Google Drive remote

Installation is documented through `install.sh`.

## Architectural Scope

This is supporting operational tooling. It is not currently classified as a Yasin runtime, application, agent, or control-plane service.

Its primary ecosystem relevance is operational resilience for Termux-based environments and developer workflows.

## Security Considerations

The actual handling of rclone configuration, Google Drive credentials, backup contents, permissions, restore behavior, and destructive operations requires source-level audit.

## Audit Remaining

- Backup format and contents
- Include/exclude rules
- Restore semantics
- Migration workflow
- rclone invocation and configuration
- Secret handling
- Failure/recovery behavior
- Tests and CI
- Destructive-operation safeguards
- Exact relationship to TJC and other Termux tooling
