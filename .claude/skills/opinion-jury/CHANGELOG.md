# Changelog

## 2.2.0

- Added `direct` intensity level: single-prompt fast path that skips Stages 3–9 (role pool, panels, debate, blind adjudication, replay). Goes directly from intake + CLAIM_GATE to final report via a structured prompt template.
- Moved auto intensity resolution from Stage 4 to new Stage 1.5 (immediately after parse, before CLAIM_GATE). `auto` can now resolve to `direct` for simple content. Resolution criteria cover content volume, claim count, institutional attribution, statistical claims, affected groups, domain sensitivity, and emotional hooks.
- Updated `audit_case.py` to validate only the reduced file set when intensity is `direct`.
- Added `references/direct-mode-prompt.md` with the direct-mode prompt template.
- Updated `FILE-CATALOG.md`, `intensity-profiles.md`, `quick-start-workflow.md` with `direct` level.

## 2.1.0

- Split every actor filing into private `think`, public `say`, and private filing metadata.
- Removed internal-only and deception markers from peer-visible public speech.
- Added separate dimensions for private belief reliability, deception awareness, belief-update mode, and norm adherence.
- Distinguished sincere error, strategic omission, rumor relay, exaggeration, and knowing fabrication.
- Strengthened multi-blind filesystem isolation and audit checks.
- Updated final replay to analyze public/private gaps and epistemic behavior.

## 2.0.0

- Replaced rational-advocate assumption with behavior-fidelity simulation.
- Added factorized behavior attributes and explicit anti-correlation bias rules.
- Added case-level role pool and cross-court role reuse.
- Added per-assignment actor folders.
- Added structured private `think` memos and public `say` filings.
- Added `BEHAVIOR_FIDELITY_GUARD`.
- Added terminal blind adjudication and post-verdict full-information replay separation.
- Added audit checks for private/public leakage and missing actor artifacts.
