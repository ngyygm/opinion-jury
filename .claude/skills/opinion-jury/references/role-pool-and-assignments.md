# Role Pool and Court Assignments

## Build roles first

Create stable case-level role cards before any court opens:

```text
03-role-pool/private/roles/<role-card-id>/role-card.json
```

Commit with:

```bash
python scripts/commit_role_pool.py <case-dir>
```

## Factorize the card

Each role card separates:

- **demographic profile** (age_range, education_level, occupation, location_type, speech_style, topic_relevance) — constrains how the character thinks and speaks;
- stakeholder relation and interests;
- values and feared losses;
- information environment;
- amplification resources;
- private belief reliability;
- truthfulness mode;
- deception awareness;
- reasoning mode;
- belief-update mode;
- civility and emotional regulation;
- public/private gap;
- explicit correlation notes and stereotype guardrails.

Do not infer one dimension from another. The demographic profile constrains voice and cognition but does not determine honesty, rationality, or aggression.

## Reuse across courts

The same role may appear in multiple issue courts. Each appearance gets a new assignment folder:

```text
05-panels/panel-NNN-<slug>/private/actors/<assignment-id>/assignment.json
```

This supports cross-issue continuity analysis. The budget counts role appearances and enforces a lower unique-role diversity floor.

## Actor folder

Each assignment owns its own turn tree:

```text
private/actors/<assignment-id>/
├── assignment.json
├── continuity.private.jsonl
└── turns/
    └── round-NNN-<phase>/
        ├── input-scope.private.json
        ├── scoped-view/
        ├── think.private.json
        ├── say.public.json
        ├── say.public.md
        ├── filing-metadata.private.json
        └── behavior-fidelity.private.json
```
