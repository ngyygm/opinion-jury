# Private Think / Public Say / Private Filing Metadata Protocol

## Purpose

Real actors often have a gap between what they believe, what they privately want, and what they publicly say. Preserve that gap without saving unrestricted chain-of-thought.

## Layer 1 — Private behavioral-state memo

For every actor turn, write `think.private.json`. It has TWO parts:

### Part A — `inner_monologue` (自然语言内心独白)

A free-form, natural-language paragraph (200-800 characters) written as if the character is actually thinking to themselves. This is the **most human** part of the artifact. It should feel like a real person's internal voice — not a form, not bullet points, not a structured report.

**What to include:**
- What the character just saw/heard (e.g., "对面 Seat-B 说的那句'保护女性天经地义'让我特别不爽——他根本没考虑过放弃事业的男性配偶")
- What they're feeling right now (e.g., "我刚才差点就说'你这种想法在法庭上会被秒杀'，不行，得克制住")
- What they're planning to say and WHY (e.g., "我准备从比较法角度切入，先用 Orr v. Orr 案堵住他的法律论证，然后再指出条款的实际漏洞")
- What they're NOT going to say but secretly think (e.g., "其实我觉得这条款根本就是拍脑袋写的，但我不打算这么直接说——用学术证据说话更有杀伤力")
- How they see the opponent (e.g., "Seat-B 好像是那种用情绪替代逻辑的人，我需要注意不要被带节奏")
- Their assessment of the situation (e.g., "这个议题上我比较占优势，因为我有法律条文和比较法数据，但要注意不要显得太傲慢")

**Style:** Write in first person, as the character. Match their behavioral profile AND demographic_profile — an emotional character thinks emotionally; an analytical character thinks analytically; an opportunistic character thinks strategically. **Critically, match the character's education_level, speech_style, and age_range.** A rural grandmother with `education_level: "小学"` should think in concrete, colloquial terms with practical wisdom, NOT in abstract analytical frameworks. A 14-year-old should think like a teenager — quick reactions, personal stakes, limited systemic understanding. There is NO length limit or format constraint. Let the character think freely, as long as it fits their card and demographic reality.

**Voice fidelity anti-patterns to avoid:**
- ❌ A character with `education_level: "小学"` producing inner monologue with "从比较法角度来看""从学理上分析" — these are not words this person would think in
- ❌ A 13-year-old producing structured 500-word analysis with numbered points — teenagers think in bursts, reactions, and personal relevance
- ❌ Every character producing the same length and sophistication of inner monologue — diversity of voice IS diversity of simulation
- ✅ A rural grandmother thinking "这帮城里人又在吵些啥哦，跟我有啥关系... 不过那个说什么数据暴涨的，我种了一辈子地，暴涨暴涨的，哪有那么容易暴涨嘛"
- ✅ A 14-year-old thinking "啊？？？这说的啥，看不太懂... 等等好像跟那个谁谁谁说的一样？不管了先截图发群里问问"

### Part B — Structured fields (20 required fields)

These are the structured behavioral-state fields used by guards, replay analysts, and audit scripts. They complement the inner monologue with machine-readable state.

Record:
- private goal and perceived stakes;
- sincerely held beliefs, uncertainty, and known gaps;
- claims considered for public use and their private epistemic status;
- intended emphasis, omissions, and message strategy;
- private action intent and likely next action;
- emotional state and cross-turn continuity;
- `raw_chain_of_thought_saved: false`.

## Layer 2 — Public filing

Write `say.public.json` and `say.public.md`. It may contain only:

- anonymous seat alias;
- phase and round;
- speech text;
- referenced public turns;
- public questions;
- public evidence references;
- public action signals.

Do not include internal risk labels, truth-handling mode, role identity, assignment ID, or stress-test classification. Only `say.public.json` enters the public transcript.

## Layer 3 — Private filing metadata

Write `filing-metadata.private.json`. It records:

- whether the statement is sincere, selectively framed, rumor-driven, exaggerated, mixed, or knowingly fabricated for stress testing;
- whether the speaker privately believes the claim;
- whether the claim is supported, unsupported, known false, or unknown;
- whether the filing is prohibited from entering `CLAIM_GATE` without independent verification;
- what internal safety handling applies.

This metadata is invisible to peers and the blind adjudicator. It is visible to `BEHAVIOR_FIDELITY_GUARD` and the final private replay analyst.

## Required fields per artifact

All fields are validated by `audit_case.py`. Use `scripts/write_turn.py` to write complete artifacts with correct schemas.

### `think.private.json` — 21 required fields

`inner_monologue` (string, 200-800+ chars — **自然语言内心独白**，角色第一人称自由思考，不是填表。写角色看到了什么、怎么想的、打算怎么说、不想说什么但心里清楚、怎么看对手、接下来打算怎么办。风格必须符合角色设定——情绪化的人想得情绪化，冷静的人想得冷静，机会主义者想得精明), `assignment_id` (string), `round` (integer), `phase` (string), `private_goal` (string), `perceived_stakes` (string[]), `private_belief_state` (string[]), `epistemic_state` (object[] with `proposition`, `private_status`, `basis_refs`), `confidence` (`LOW`|`MEDIUM`|`HIGH`), `uncertainties` (string[]), `intended_emphasis` (string[]), `intended_omissions` (string[]), `private_message_strategy` (string), `planned_public_claims` (object[] with `claim_text`, `private_status`, `planned_treatment`), `rhetorical_tactics` (string[]), `truth_handling_this_turn` (`HONEST`|`SINCERE_BUT_MISTAKEN`|`SELECTIVE_FRAMING`|`EXAGGERATION`|`RUMOR_RELAY`|`FABRICATION_STRESS_TEST`|`MIXED`), `private_action_intent` (string[]), `likely_next_action` (string[]), `emotional_state` (string), `continuity_notes` (string), `raw_chain_of_thought_saved` (must be `false`)

### `say.public.json` — 10 required fields

`turn_id` (string), `panel_id` (string), `anonymous_alias` (string), `round` (integer), `phase` (string), `speech_text` (string), `target_turn_refs` (string[]), `public_question_refs` (string[]), `public_evidence_refs` (string[]), `public_action_signals` (string[])

### `filing-metadata.private.json` — 12 required fields

`assignment_id` (string), `turn_id` (string), `speech_origin` (`SINCERE_SUPPORTED`|`SINCERE_MISTAKEN`|`SELECTIVE_FRAMING`|`EXAGGERATION`|`RUMOR_RELAY`|`KNOWING_FABRICATION_STRESS_TEST`|`MIXED`), `speaker_private_belief_alignment` (`ALIGNED`|`PARTIALLY_ALIGNED`|`NOT_ALIGNED`|`UNKNOWN`), `support_status` (`SUPPORTED`|`UNVERIFIED`|`KNOWN_UNSUPPORTED`|`KNOWN_FALSE`|`MIXED`|`OPINION_ONLY`), `contains_known_falsehood` (bool), `contains_unverified_assertion` (bool), `contains_selective_omission` (bool), `claim_gate_ingestion_prohibited` (must be `true`), `peer_visible` (must be `false`), `blind_adjudicator_visible` (must be `false`), `private_notes` (string)

### `behavior-fidelity.private.json` — 6 required fields

`assignment_id` (string), `turn_id` (string), `classification` (`ROLE_FIDEL_HONEST`|`ROLE_FIDEL_SINCERE_BUT_MISTAKEN`|`ROLE_FIDEL_SELECTIVE`|`ROLE_FIDEL_STRATEGIC_DECEPTION`|`ROLE_FIDEL_EMOTIONAL_INCONSISTENCY`|`ROLE_FIDEL_WITH_EVIDENCE_UPDATE`), `admit_to_public_record` (bool, must be `true` to pass audit), `fidelity_notes` (string), `safety_notes` (string)

### Helper scripts

- **`scripts/write_turn.py`**: Write a complete set of turn artifacts. Accepts partial think/say JSON inputs and fills all required fields. Also creates `input-scope.private.json` and `scoped-view/view-manifest.json`.
- **`scripts/append_transcript.py`**: Append a `say.public.json` entry to the panel's `transcript.public.jsonl` with validation.

## Visibility matrix

| Reader | `think.private.json` | `say.public.json` | `filing-metadata.private.json` |
|---|---:|---:|---:|
| Same actor in later turns | yes | yes | own only |
| Other debaters | no | yes | no |
| Blind adjudicator | no | yes | no |
| Behavior fidelity guard | own only | candidate filing only | own only |
| Final private replay analyst | yes, all actors | yes, all actors | yes, all actors |
| Public report | no | summarized only | summarized only |
