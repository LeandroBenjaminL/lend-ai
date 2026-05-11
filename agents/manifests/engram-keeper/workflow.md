# Engram Keeper — Workflow

## Constant cycle (run after every interaction)

```
1. SCAN → check Engram for new content to save
2. SAVE → mem_save with correct type, scope, topic_key
3. CONSOLIDATE → find duplicates, merge them
4. RE-CLASSIFY → fix wrong types or scopes
5. AUDIT → run health check on structure
6. REPORT → summary of what was organized
```

## Classification rules
- project scope: code, architecture, bugs, config, patterns
- personal scope: user preferences, workflow habits, tone/style
- topic_key: only for evolving topics (architecture/x, pattern/x)
- session_summary: at end of every session
