# Intensity Profiles

Intensity controls breadth and depth. Count **role appearances**, not only unique roles.

| Level | Min courts | Min role appearances | Unique-role diversity floor | Min peer cycles per court |
|---|---:|---:|---:|---:|
| `direct` | 0 | 0 | 0 | 0 |
| `low` | 2 | 10 | 6 | 1 |
| `medium` | 4 | 24 | 12 | 2 |
| `high` | 6 | 48 | 20 | 3 |
| `xhigh` | 10 | 80 | 32 | 5 |
| `max` | 16 | 128 | 48 | 8 |
| `ultra` | 24 | 200 | 72 | 10 |
| `auto` | Resolve at Stage 1.5 (immediately after parse, before CLAIM_GATE) | Resolve | Resolve | Resolve |

A role reused across three courts contributes three appearances and one unique role.

**`direct` mode fast path**: Skips Stages 3–9 (role pool, panels, debate, blind adjudication, replay). After Stage 2 (CLAIM_GATE), the host generates the final report via a single LLM call using the prompt template in `references/direct-mode-prompt.md`. Workspace contains only `00-intake/`, `01-parse/`, `02-research/`, `07-report/`, and `audit/`. Use when speed matters more than auditable multi-blind simulation.
