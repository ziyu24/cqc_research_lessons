# Cross-Project Research Lessons

This repository stores concise, sanitized, reusable research pitfall cards. It is
not a scientific evidence store and must not contain full logs, tables, datasets,
credentials, connection details, unpublished manuscripts, or project-local
absolute paths.

The canonical index is `INDEX.yaml`. Cards are grouped under six categories:
`methodology`, `data`, `metrics`, `implementation`, `environment`, and `compute`.
The category directories intentionally contain only guidance until a real lesson
is separately reviewed and promoted.

Each card must satisfy the closed field set in `SCHEMA.yaml`. A short
`raw_evidence_summary` may preserve a bounded aggregate or representative
observation, and `error_excerpt` may preserve at most 20 short lines. Detailed
source evidence stays in its originating project.

Validate the repository locally with:

```text
python tools/validate.py .
python -m unittest -v tests.test_validate
```

`BLOCK` is reserved for active, deterministic, reproducible, uncontested
lessons. All other reusable guidance is `WARN`.
