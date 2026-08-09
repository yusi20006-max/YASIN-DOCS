# Yasin Project Status Matrix

This matrix is intentionally conservative. `Partial` means the repository and a high-level role are known, not that the full architecture has been verified.

| Project | Repository Found | Architecture Record | Source/Manifest Evidence | Cross-Project Contract | API Audit | CI/Test Audit |
|---|---:|---:|---:|---:|---:|---:|
| Yasin-Core | Yes | Yes | Strong | Strong | Partial | Strong |
| Yasin-Agent | Yes | Yes | Strong | Strong | Partial | Strong |
| Yasin-AI | Yes | Yes | Strong | Partial | Partial | Strong |
| YasinHub | Yes | Yes | Strong | Strong | Partial | Strong |
| YasinRelay | Yes | Yes | Strong | Strong | Partial | Partial |
| YasinFeed | Yes | Yes | Partial | Strong | Partial | Partial |
| YasinPress | Yes | Yes | Partial | Partial | Partial | Partial |
| YasinCLI | Yes | Yes | Strong | Strong | Partial | Strong |
| YASIN-DOCS | Yes | Yes | Complete | N/A | N/A | Partial |
| OpenFeed | Yes | Yes | Partial | Partial | Partial | Partial |
| FeedBridge | Yes | Yes | Strong | Strong | Partial | Partial |
| TJC | Yes | Yes | Partial | Partial | Partial | Partial |
| Termux Backup Manager | Yes | Yes | Partial | Partial | Partial | Partial |
| YasinCoder | Yes | Scope candidate | Not audited | Unknown | Unknown | Unknown |
| YasinJules | Yes | Scope candidate | Not audited | Unknown | Unknown | Unknown |
| Telegram-Mirror | Yes | Scope candidate | Not audited | Unknown | Unknown | Unknown |
| YasinPress-Rewrite- | Yes | Scope candidate | Not audited | Unknown | Unknown | Unknown |

## Evidence Notes

- **Strong** means direct implementation/package/PR evidence exists for the specific category.
- **Partial** means some repository evidence exists but the complete contract is not verified.
- **Unknown** means no sufficient evidence was collected yet.
- `Scope candidate` means the repository was discovered in the owner's GitHub inventory but has not been proven to be an active architectural component.

## Key Verified Contracts

`docs/projects/VERIFIED_CONTRACTS.md` and `docs/projects/SOURCE_VERIFIED_ARCHITECTURE.md` record the strongest cross-project evidence discovered during Phase 5.

## Completion Criteria

Architecture documentation is considered complete only when every discovered repository is either:

1. included as an audited Yasin component; or
2. explicitly classified as related/supporting/out-of-scope with the reason recorded.

Low-level unknowns must remain explicitly marked rather than replaced with assumptions.
