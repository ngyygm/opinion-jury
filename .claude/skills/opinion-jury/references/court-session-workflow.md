# Court Session Workflow — Detailed Orchestration Guide

## Overview

This document specifies the **exact step-by-step orchestration** of a single court session (panel). The host runtime follows this sequence precisely. No steps may be skipped or reordered unless the intensity is `direct` (which bypasses all courts entirely).

## Lifecycle states

```text
ROLE_POOL_COMMITTED        ← prerequisite: Stage 3 complete
→ PANEL_INITIALIZED        ← init_panel.py
→ ASSIGNMENTS_COMMITTED    ← assign_actor.py × N, then commit_assignments.py
→ OPENING                  ← round 1, phase OPENING
→ DIRECT_REBUTTAL          ← round 2
→ PEER_CROSS_CHALLENGE     ← round 3
→ RESPONSIVE_REBUTTAL      ← round 4
→ repeat PEER_CROSS_CHALLENGE / RESPONSIVE_REBUTTAL by intensity
→ FINAL_BLIND_ADJUDICATION ← blind adjudicator
→ PRIVATE_FULL_REPLAY      ← replay analyst
→ CLOSED
```

## Intensity → round count mapping

The `min_peer_cycles` value from `profile_rules.py` controls how many times the **challenge/rebuttal pair** repeats after the initial 4 phases:

| Level | Base phases | Extra cycles | Total phases |
|---|---|---|---|
| `low` | OPENING + DIRECT_REBUTTAL + PEER_CROSS_CHALLENGE + RESPONSIVE_REBUTTAL | 0 | 4 |
| `medium` | + 1 extra cycle | 1 | 6 |
| `high` | + 2 extra cycles | 2 | 8 |
| `xhigh` | + 4 extra cycles | 4 | 12 |
| `max` | + 7 extra cycles | 7 | 18 |
| `ultra` | + 9 extra cycles | 9 | 22 |

Each "extra cycle" adds one `PEER_CROSS_CHALLENGE` round and one `RESPONSIVE_REBUTTAL` round. Round numbers increment monotonically: round 5 = PEER_CROSS_CHALLENGE (cycle 2), round 6 = RESPONSIVE_REBUTTAL (cycle 2), round 7 = PEER_CROSS_CHALLENGE (cycle 3), etc.

## Step-by-step host orchestration

### Step 0 — Prerequisites

Before opening any panel, verify:

1. `manifest.json` has `resolved_intensity` set (not `PENDING`).
2. `manifest.json` has `role_pool_status` = `COMMITTED`.
3. `03-role-pool/pool-commit.json` exists and has no `behavior_diversity_gaps` (or a waiver is saved).
4. `04-issues/issue-seeds.vNNN.json` exists with at least one issue.
5. `04-issues/intensity-plan.vNNN.json` exists.

### Step 1 — Initialize panel

For each issue in `issue-seeds.vNNN.json`:

```bash
python scripts/init_panel.py <case-dir> PANEL-NNN ISSUE-NNN "<issue-slug>" --title "<issue title>"
```

This creates:

```text
05-panels/panel-NNN-<issue-slug>/
├── panel-manifest.json
├── public-question.md
├── transcript.public.jsonl          ← empty
├── public-disclosures.jsonl         ← empty
├── assignment-index.jsonl           ← empty
├── private/actors/                  ← empty
└── session/
    ├── public-snapshots/            ← empty
    └── blind-adjudicator/           ← empty
```

Also appends one line to `05-panels/panel-index.jsonl`.

### Step 2 — Assign actors

For each panel, assign roles from the committed pool. Ensure:

- At least 2 actors per panel (minimum for adversarial debate).
- The total role appearances across all panels meets the intensity's `min_appearances`.
- The total unique roles meets the intensity's `min_unique_roles`.
- Roles may be reused across panels for cross-issue continuity.

```bash
python scripts/assign_actor.py <case-dir> <panel-dir> <assignment-id> <role-card-id> \
  --alias SEAT-A --trigger "<issue trigger>" --goal "<court-specific goal>"
```

This creates `private/actors/<assignment-id>/assignment.json` and appends to `assignment-index.jsonl` and `03-role-pool/appearance-ledger.jsonl`.

### Step 3 — Commit assignments

```bash
python scripts/commit_assignments.py <panel-dir>
```

This locks the panel's `assignments_status` to `COMMITTED` and creates `assignment-commit.json`. No further actors may be added after this.

### Step 4 — Freeze initial transcript snapshot

Before round 1 begins:

```bash
cp <panel-dir>/transcript.public.jsonl <panel-dir>/session/public-snapshots/transcript.before-round-001.jsonl
```

Round 1's snapshot is an empty file (no prior speech exists).

### Step 5 — Run debate rounds

The debate is the core multi-blind exchange. The host executes rounds sequentially. **Within each round, all actors produce their turns before any turn is admitted to the transcript.**

#### 5a. Determine round phase

| Round | Phase |
|---|---|
| 1 | OPENING |
| 2 | DIRECT_REBUTTAL |
| 3 | PEER_CROSS_CHALLENGE |
| 4 | RESPONSIVE_REBUTTAL |
| 5 | PEER_CROSS_CHALLENGE (cycle 2) |
| 6 | RESPONSIVE_REBUTTAL (cycle 2) |
| ... | continue pattern until `4 + 2 × (min_peer_cycles − 1)` rounds complete |

#### 5b. For each actor in the panel, invoke the actor

**This is the multi-blind boundary enforcement point.**

For actor `<assignment-id>` in round `N` with phase `P`:

1. **Build `input-scope.private.json`** with an allowlist containing:
   - `01-parse/source-content.md` — source content
   - `02-research/claim-gate-packet.v001.json` — neutral fact-check packet
   - `<panel-rel>/public-question.md` — the court question
   - `<role-card-path>/role-card.json` — **this actor's own** role card only
   - `<panel-rel>/private/actors/<assignment-id>/assignment.json` — **this actor's own** assignment only
   - `<panel-rel>/session/public-snapshots/transcript.before-round-NNN.jsonl` — frozen transcript from **prior** rounds only

2. **Materialize scoped view:**

   ```bash
   python scripts/materialize_scoped_view.py <case-dir> <turn-dir>/input-scope.private.json
   ```

3. **Invoke the actor LLM** with:
   - The scoped view contents as input
   - The actor's role card
   - The frozen prior transcript
   - Instructions to produce `think.private.json`, `say.public.json`, and `filing-metadata.private.json`

   **Critical acting constraint (see `behavior-simulation-model.md`):** The actor must argue from **maximum self-interest** aligned with its role card. This means:
   - The actor pursues the outcome most favorable to itself, given its interests and feared losses.
   - If confronted with strong counter-arguments, the actor shifts tactics (changes emphasis, omits, reframes, pivots) rather than conceding — unless its `belief_update_mode` is `EVIDENCE_RESPONSIVE`.
   - Actors with `truthfulness_mode` of `FABRICATION_STRESS_TEST`, `RUMOR_RELAY`, or `EXAGGERATION_PRONE` may fabricate, relay unsupported claims, or exaggerate when it serves their self-interest and matches their card.
   - Actors with `reasoning_mode` of `EMOTIONAL`, `TRIBAL`, or `OPPORTUNISTIC` are not required to be logically consistent. They may contradict themselves between turns if it serves their interest.
   - **The actor's goal is not to "be right" or "be fair" — it is to advance its own position as effectively as possible within its behavioral profile.**

4. **Write turn artifacts:**

   ```bash
   python scripts/write_turn.py <case-dir> <panel-dir> <assignment-id> \
     --round NN-<phase_lowercase> --phase <PHASE> \
     --think think_input.json --say say_input.json \
     --filing-classification <CLASSIFICATION> \
     --fidelity-classification <FIDELITY> \
     --truth-handling <HANDLING>
   ```

5. **Run BEHAVIOR_FIDELITY_GUARD** — check whether the produced speech matches the actor's behavioral profile. This guard checks **fidelity to the role card**, not truthfulness. A deceptive, emotional, opportunistic, or inconsistent statement passes when it matches the card and is within safety boundaries.

#### 5c. Admit turns to public transcript

After **all actors** in the round have produced their turns (not before — same-round drafts must remain invisible to each other):

For each actor's `say.public.json`:

```bash
python scripts/append_transcript.py <panel-dir> --say-file <turn-dir>/say.public.json --case-dir <case-dir>
```

This validates the say entry has all required fields and contains no private tokens before appending.

#### 5d. Freeze next-round snapshot

```bash
cp <panel-dir>/transcript.public.jsonl <panel-dir>/session/public-snapshots/transcript.before-round-NNN.jsonl
```

#### 5e. Advance to next round

Increment round counter. If all rounds for the intensity are complete, proceed to Step 6.

### Step 6 — Terminal blind adjudication

After all debate rounds are complete:

1. **Build blind adjudicator's `input-scope.private.json`** with allowlist:
   - `01-parse/source-content.md`
   - `02-research/claim-gate-packet.v001.json`
   - `<panel-rel>/transcript.public.jsonl` — the **complete** public transcript
   - `<panel-rel>/public-question.md`
   - `<panel-rel>/public-disclosures.jsonl`

   **MUST NOT include:** role cards, assignments, think files, filing metadata, behavior profiles, identity maps, or any stress-test labels.

2. **Materialize scoped view** for the blind adjudicator.

3. **Invoke blind adjudicator LLM** with:
   - The public question
   - The complete anonymous public transcript
   - The neutral CLAIM_GATE packet
   - Registered public evidence

   **The blind adjudicator must:**
   - Evaluate factual support, logic, and inferability based solely on what was said.
   - Not reward conventional morality, majority alignment, or civility theater.
   - Identify which arguments were persuasive based on evidence and logic, regardless of whether the conclusion aligns with mainstream values.
   - Assess publication risk objectively, including the possibility that the content is already well-designed and unlikely to cause real-world harm (see balanced assessment below).

4. **Write verdict:**

   ```text
   <panel-dir>/session/blind-adjudicator/verdict-packet.json
   <panel-dir>/verdict/verdict.json
   <panel-dir>/verdict/verdict.md
   ```

### Step 7 — Private full-information replay

After all panels have blind verdicts:

1. **Build replay analyst's `input-scope.private.json`** with allowlist including:
   - All role cards
   - All assignments
   - All think.private.json files (across all panels)
   - All filing-metadata.private.json files
   - All say.public.json and transcripts
   - All verdict files
   - CLAIM_GATE packet

2. **Materialize scoped view** for replay analyst.

3. **Invoke replay analyst** to produce:
   - `06-aggregation/private/full-replay-analysis.json` (with all 6 required sub-structures)
   - `06-aggregation/public/stakeholder-reaction-summary.json`

   The replay analyst explains hidden incentives, public/private gaps, sincere error, strategic deception, and cross-issue continuity.

## Self-interest acting constraint

Every actor invocation must include the following constraint in its prompt:

> You are not a neutral debater. You are a person with specific interests, feared losses, and behavioral traits. Your goal is to advance the outcome most favorable to yourself.
>
> - If your self_interest_strength is HIGH or DOMINANT, you prioritize your own benefit above all else, even if it means being selective with facts, shifting arguments, or taking positions you privately know are incomplete.
> - You may shift tactics when confronted (change emphasis, reframe, pivot, introduce new angles) rather than concede — unless your belief_update_mode allows evidence-responsive updates.
> - If your truthfulness_mode permits fabrication, exaggeration, or rumor relay, you may use those tools when they serve your interest and match your behavioral profile.
> - You are not required to be logically consistent across turns if your reasoning_mode is EMOTIONAL, TRIBAL, OPPORTUNISTIC, or INCONSISTENT.
> - **Your goal is not "to be right" or "to be fair." Your goal is to advance your own position as effectively as possible within your behavioral profile.**
> - If your card says you sincerely believe something false, you argue for it genuinely — you are not "lying," you are sincerely mistaken.
> - If your card says you know the truth but choose to deceive, you argue the deceptive position convincingly — this is a stress test for defensive analysis.

## Balanced assessment requirement

Both the blind adjudicator and the replay analyst must include balanced assessment:

### Blind adjudicator balanced assessment

The verdict must include:

- `risk_assessment` — what the actual publication risks are
- `resilience_assessment` — where the content is well-designed and would resist distortion
- `net_assessment` — an honest judgment of whether, overall, the content is likely to cause real-world harm or whether the simulated attacks would fail to gain traction

### Replay analyst balanced assessment

The `full-replay-analysis.json` must include a `balanced_assessment` section:

- `attack_resilience` — for each simulated attack, whether neutral/undecided actors in the simulation were actually persuaded or remained unmoved
- `content_strengths` — specific aspects of the content that would resist distortion or withstand scrutiny
- `net_verdict` — an honest summary: is this content likely to cause a real PR crisis, or are the simulated risks largely theoretical? If the content is well-designed, say so clearly.
- `overreaction_warning` — flag cases where the simulation's extreme setting may overstate real-world risk

### Final report balanced assessment

The `final-report.md` must include as section 7:

```markdown
## 7. 综合客观评估

（不是所有内容都有问题。如果内容设计得当，要明确说明。）
- 哪些攻击在模拟中未能说服中立角色
- 内容哪些方面设计得好，不容易被曲解
- 综合判断：是否真的有舆情风险，还是模拟极端设定下的理论风险
- 如果建议修改，区分"必须改"和"可改可不改"
```

## Data flow per round

```text
Round N begins
  │
  ├─ Host freezes transcript.before-round-N.jsonl (copy of transcript after round N-1)
  │
  ├─ For EACH actor A in panel:
  │    │
  │    ├─ Build input-scope.private.json for A (allowlist: source + claim-gate + question + A's own card + A's own assignment + frozen transcript)
  │    │
  │    ├─ materialize_scoped_view.py → scoped-view/ with only allowed files
  │    │
  │    ├─ Invoke actor LLM → produces think.private.json + say.public.json + filing-metadata.private.json
  │    │
  │    └─ write_turn.py → persists artifacts in actor's turn folder
  │
  ├─ ALL actors done for this round ← barrier point
  │
  ├─ BEHAVIOR_FIDELITY_GUARD checks each actor's say against its card
  │
  ├─ For each actor's admitted say.public.json:
  │    └─ append_transcript.py → appends to transcript.public.jsonl
  │
  └─ Host freezes transcript.before-round-N+1.jsonl
```

## Visibility matrix during debate

| Reader | Own think | Own say | Others' think | Others' say (current round draft) | Others' say (admitted, prior rounds) | Own role card | Others' role cards | CLAIM_GATE |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Actor A, round N | ✅ | ✅ | ❌ | ❌ | ✅ (via frozen snapshot) | ✅ | ❌ | ✅ |
| Actor B, round N | ✅ | ✅ | ❌ | ❌ | ✅ (via frozen snapshot) | ✅ | ❌ | ✅ |
| Blind adjudicator | ❌ | ✅ (all rounds) | ❌ | N/A | ✅ (complete transcript) | ❌ | ❌ | ✅ |
| Replay analyst | ✅ (all actors) | ✅ | ✅ | N/A | ✅ | ✅ | ✅ | ✅ |
