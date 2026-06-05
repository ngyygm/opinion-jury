# Quick-Start Workflow Guide

This is the recommended execution sequence for the opinion-jury skill. Run these scripts in order.

## 1. Initialize case

```bash
python scripts/init_case.py --topic "your topic" --intensity low --root opinion-jury-cases
```

This prints the case directory path. Save it as `$CASE`.

## 2. Register roles

For each role card JSON file:

```bash
python scripts/register_role.py $CASE path/to/role-card.json
```

Role cards must have factorized behavioral dimensions. See `schemas/role-card.schema.json`.

## 3. Commit role pool

```bash
python scripts/commit_role_pool.py $CASE
```

If diversity barriers fail, either add counterexample roles or use `--diversity-waiver "reason"`.

## 4. Initialize panels

For each issue (check intensity profile for minimum panel count):

```bash
python scripts/init_panel.py $CASE PANEL-001 ISSUE-001 "issue-slug" --title "Issue title"
```

This prints the panel directory path. Save it as `$PANEL`.

## 5. Assign actors

For each actor in each panel:

```bash
python scripts/assign_actor.py $CASE $PANEL ASGN-001A --alias Seat-A --trigger "issue description" --goal "court goal"
```

## 6. Commit assignments

```bash
python scripts/commit_assignments.py $PANEL
```

## 7. Write turns

For each actor turn (one invocation per round per actor):

```bash
python scripts/write_turn.py $CASE $PANEL ASGN-001A \
  --round 1-OPENING --phase OPENING \
  --think think_input.json --say say_input.json \
  --filing-classification SINCERE_SUPPORTED \
  --fidelity-classification ROLE_FIDEL_HONEST \
  --truth-handling HONEST
```

## 8. Append to transcript

After each turn is admitted:

```bash
python scripts/append_transcript.py $PANEL --say-file $PANEL/private/actors/ASGN-001A/turns/round-1-OPENING/say.public.json --case-dir $CASE
```

## 9. Audit

```bash
python scripts/audit_case.py $CASE
```

Must show `"status": "PASS"` before proceeding to report generation.

## Intensity profiles

| Level | Min panels | Min appearances | Min unique roles | Min peer cycles |
|-------|-----------|----------------|-----------------|----------------|
| direct| 0         | 0              | 0               | 0              |
| low   | 2         | 10             | 6               | 1              |
| medium| 4         | 24             | 12              | 2              |
| high  | 6         | 48             | 20              | 3              |
| xhigh | 10        | 80             | 32              | 5              |
| max   | 16        | 128            | 48              | 8              |
| ultra | 24        | 200            | 72              | 10             |

## Common pitfalls

1. **Windows encoding**: All scripts now use `encoding='utf-8'`. Chinese content works on Windows.
2. **Role pool must be committed** before `init_panel.py` will run.
3. **Assignments must be committed** before writing turns.
4. **`write_turn.py` does NOT append to transcript** — you must run `append_transcript.py` separately.
5. **Diversity barriers** require counterexample roles (extreme+honest, moderate+strategic, etc.).
