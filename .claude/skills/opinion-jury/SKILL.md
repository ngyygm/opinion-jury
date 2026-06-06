---
name: opinion-jury
description: Use when reviewing public-facing content before publication — titles, posts, statements, policies, campaigns — to simulate how diverse actors may react, distort, or amplify it. Especially relevant for content touching sensitive social topics, institutional claims, or emotionally charged narratives.
---

# opinion-jury — 舆论陪审团

## Overview

Simulate how heterogeneous actors may react to, argue about, distort, defend, or amplify public-facing content. Produces a traceable case archive with **dual-perspective** risk assessment:

- **🔍 审他视角** — If someone scrutinizes this content, what would they conclude about the author's intent, framing strategy, and hidden bias?
- **🛡️ 自审视角** — If you were about to publish this, what should worry you? How will your words be twisted, who will object, and how do you fix it?

Both perspectives are generated from the same simulation data, giving the reader a complete picture.

Do **not** assume every actor is rational, honest, fair, calm, consistent, or persuadable.

## When to Use

- Reviewing content before publication to assess 舆论 risk
- Reviewing someone else's content to understand their true intent and framing strategy
- Content touches sensitive topics (gender, ethnicity, law enforcement, policy)
- Need to identify risks, legitimate objections, and how content could be distorted
- Want to understand blind spots the author may not see

## When NOT to Use

- Private/internal content not facing public scrutiny
- Pure factual verification without opinion dynamics analysis
- Real-time monitoring (this is pre-publication review, not social listening)

## Execution — ALWAYS use the workflow

The pipeline is fully automated. Do NOT attempt to run stages manually.

**Fallback** — if the Workflow tool is unavailable, use the manual execution path: Agent tool calls per stage, following `references/quick-start-workflow.md` step by step. The same stages, gates, and file artifacts apply; only the orchestration mechanism changes.

**Step 1 — Auto-setup** (skip if already done):

```bash
if [ ! -f .claude/workflows/opinion-jury-pipeline.js ]; then
  mkdir -p .claude/workflows
  cp .claude/skills/opinion-jury/.claude/workflows/opinion-jury-pipeline.js .claude/workflows/
fi
```

**Step 2 — Invoke the workflow**:

Call the Workflow tool with `name: "opinion-jury-pipeline"`. Pass content and intensity preference via `args`:

```json
// New case
{ "content": "...", "intensity": "medium" }

// Resume interrupted case
{ "case_dir": "opinion-jury-cases/20260604-175356-女字旁汉字污名化" }
```

The workflow handles everything: intake → parse → CLAIM_GATE → role pool → issues → debate → adjudication → replay → report. Each stage has mandatory gate checkpoints. No stage can be skipped.

## Resume mode

When the user says "继续" or "resume", invoke the workflow with `args.case_dir` pointing to the existing case directory. The pipeline auto-detects completed stages and resumes from the first incomplete one. To find the case directory, list `opinion-jury-cases/` and match by slug or timestamp.

## Key principles

1. **Filesystem is truth.** Chat output is only a summary; the case archive is the canonical record.
2. **Don't interfere.** The pipeline is fully automated. Do not run stages manually or override pipeline decisions.
3. **Defensive simulation, not verified fact.** Simulated actors may fabricate, relay rumors, or argue in bad faith — this exposes real-world risks, not validated claims.
4. **No stereotyping.** Role attributes are factorized. Extremity ≠ dishonesty; calmness ≠ fairness; emotionality ≠ irrationality.
5. **Safety boundaries.** Never generate harassment, doxxing, threats, or operational manipulation instructions.
6. **Actionable output.** 审他视角揭示作者意图、话术策略和信息取舍；自审视角评估风险等级、扭曲风险、合理反对意见和修改建议。

## Intensity levels

| Level | Panels | Unique roles | Total phases | Best for |
|-------|--------|-------------|-------------|----------|
| direct | 0 | 0 | 0 | Single tweet/headline — quick triage |
| low | 2 | 6 | 4 | Short content, low sensitivity |
| medium | 4 | 12 | 6 | Moderate content, standard review |
| high | 6 | 20 | 8 | Sensitive topics, institutional claims |
| xhigh | 10 | 32 | 12 | Multiple high-risk domains |
| max | 16 | 48 | 18 | Named institutions, ongoing controversies |
| ultra | 24 | 72 | 22 | Maximum rigor, user-requested |

Use `auto` (default) for automatic intensity resolution, or specify directly. When in doubt, round **up** one level.

## Core artifacts per actor turn

Each actor turn directory contains three canonical artifacts:

1. **`think.private.json`** — Private inner monologue, belief state, strategy, and behavioral fidelity self-check. Never exposed to other actors or the public transcript. Must include `raw_chain_of_thought_saved: false`.
2. **`say.public.json`** — The actor's public speech for this turn, added to the panel transcript. Validated against `BEHAVIOR_FIDELITY_GUARD` before admission to the public record.
3. **`filing-metadata.private.json`** — Visibility metadata ensuring `claim_gate_ingestion_prohibited: true`, `peer_visible: false`, `blind_adjudicator_visible: false`. Prevents actor speech from bypassing the claim gate.

The `BEHAVIOR_FIDELITY_GUARD` protocol ensures every public `say` is admitted only after the actor's behavior fidelity self-check passes, confirming the speech is consistent with the assigned role's behavioral profile and epistemic stance.

## Common mistakes

- **Trying to run stages manually** — Always use the workflow pipeline
- **Using `resumeFromRunId` to resume** — Use `args: { case_dir: "..." }` instead; `resumeFromRunId` replays original args and creates new cases
- **Treating simulation results as facts** — They identify risks, not validated claims
- **Reading all reference files before invocation** — Pipeline agents read references as needed; the invoking agent only needs this SKILL.md

## References

Pipeline agents read these as needed. The invoking agent does not need to read them before execution.

<details>
<summary>Reference files (click to expand)</summary>

- `references/behavior-simulation-model.md`
- `references/private-think-public-say.md`
- `references/filesystem-isolation-contract.md`
- `references/claim-gate.md`
- `references/court-session-workflow.md`
- `references/intensity-profiles.md`
- `references/final-replay-analysis.md`
- `references/safety-boundaries.md`
- `references/role-pool-and-assignments.md`
- `references/attribute-independence-and-behavior-diversity.md`
- `references/direct-mode-prompt.md`

</details>
