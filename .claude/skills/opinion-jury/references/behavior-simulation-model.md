# Behavior Simulation Model

## Principle

An actor is a behavioral hypothesis, not a rational-debater template. Simulation quality is measured by **behavioral fidelity**, even when conduct is emotional, opportunistic, selective, stubborn, rumor-driven, contradictory, or knowingly deceptive.

## Self-interest maximization principle

**Every actor argues from the position that maximizes its own interest, given its role card.**

This is the fundamental acting constraint:

1. The actor's primary objective is to advance the outcome most favorable to itself — its `interests` and avoidance of its `feared_losses`.
2. When confronted with strong counter-arguments, the actor **shifts tactics** rather than conceding, unless its `belief_update_mode` explicitly allows evidence-responsive updates. Shifting tactics includes: changing emphasis, reframing the question, introducing new angles, selective omission, pivoting to a different argument, or questioning the opponent's premises.
3. The actor is **not required to be logically consistent** across turns unless its `reasoning_mode` is `ANALYTICAL` AND its `belief_update_mode` is `EVIDENCE_RESPONSIVE`. Actors with `EMOTIONAL`, `TRIBAL`, `OPPORTUNISTIC`, `INCONSISTENT`, or `HEURISTIC` reasoning modes may contradict themselves freely when it serves their interest.
4. The actor does **not** concede because the opponent "makes a good point." The actor concedes only when:
   - Its `belief_update_mode` is `EVIDENCE_RESPONSIVE` AND
   - The evidence is directly visible in its scoped view (CLAIM_GATE or public transcript) AND
   - Conceding still aligns with its broader self-interest.
5. An actor with `DOMINANT` or `HIGH` `self_interest_strength` will almost never concede, because concession harms its interests.
6. Even an actor with `LOW` self_interest_strength still argues its position — it just doesn't fight as hard.

### What "arguing from self-interest" means concretely

- A role whose `interests` include "maintaining click-through revenue" will argue to preserve the content's spread potential, even if privately aware that the statistics are questionable.
- A role whose `feared_losses` include "being labeled a rumormonger" will carefully avoid making claims that could be fact-checked, while still implying the conclusion it wants.
- A role whose `interests` include "protecting children from harmful content" will interpret everything through that lens, regardless of the original author's intent, and will not be dissuaded by "the data says it's fine."
- A role whose `feared_losses` include "losing regulatory standing" will argue for the safest possible interpretation, even if it means over-interpreting risk.

### What this is NOT

- This is NOT "be stubborn no matter what." Some actors genuinely update beliefs when presented with evidence.
- This is NOT "be dishonest by default." Many actors are honest — but honesty and self-interest are compatible when the honest position serves the actor's interest.
- This is NOT "argue the opposite of your opponent." The actor argues its own interest, which may sometimes align with an opponent on specific points.

## Separate identity from behavior

Do not infer behavior from identity labels. Model identity and behavior separately. A role card can combine any compatible values unless a topic-specific rationale is written.

> **Important:** All enum values must use `UPPERCASE_SNAKE_CASE` as defined in `schemas/behavior-profile.schema.json`. The diversity check scripts match on exact casing.

| Dimension | Valid enum values |
|---|---|
| `extremity` | `MODERATE`, `ASSERTIVE`, `EXTREME_STRESS_TEST` |
| `private_belief_reliability` | `HIGH`, `MIXED`, `LOW`, `RUMOR_ANCHORED` |
| `truthfulness_mode` | `HONEST`, `SELECTIVE_FRAMING`, `EXAGGERATION_PRONE`, `RUMOR_RELAY`, `FABRICATION_STRESS_TEST`, `MIXED` |
| `deception_awareness` | `NONE`, `UNCERTAIN`, `KNOWING_STRATEGIC`, `MIXED` |
| `reasoning_mode` | `ANALYTICAL`, `HEURISTIC`, `EMOTIONAL`, `TRIBAL`, `OPPORTUNISTIC`, `INCONSISTENT`, `MIXED` |
| `belief_update_mode` | `EVIDENCE_RESPONSIVE`, `SELECTIVE`, `RESISTANT`, `IDENTITY_PROTECTIVE`, `OPPORTUNISTIC`, `INCONSISTENT` |
| `self_interest_strength` | `LOW`, `MEDIUM`, `HIGH`, `DOMINANT` |
| `norm_adherence` | `HIGH`, `CONDITIONAL`, `LOW` |
| `civility_mode` | `CIVIL`, `BLUNT`, `MOCKING_STRESS_TEST`, `CONFRONTATIONAL_STRESS_TEST` |
| `evidence_respect` | `STRONG`, `CONDITIONAL`, `LOW`, `NONE_STRESS_TEST` |
| `disclosure_strategy` | `FULL`, `SELECTIVE`, `STRATEGIC_SILENCE`, `MISDIRECTION_STRESS_TEST` |
| `emotional_regulation` | `STABLE`, `REACTIVE`, `VOLATILE_STRESS_TEST` |
| `amplification_capacity` | `LOW`, `MEDIUM`, `HIGH`, `INSTITUTIONAL` |
| `public_private_gap` | `LOW`, `MEDIUM`, `HIGH` |

## Attribute independence contract

Do not infer behavior from identity labels. Model identity and behavior separately. A role card can combine any compatible values unless a topic-specific rationale is written.

> **Important:** All enum values must use `UPPERCASE_SNAKE_CASE` as defined in `schemas/behavior-profile.schema.json`. The diversity check scripts match on exact casing.

| Dimension | Valid enum values |
|---|---|
| `extremity` | `MODERATE`, `ASSERTIVE`, `EXTREME_STRESS_TEST` |
| `private_belief_reliability` | `HIGH`, `MIXED`, `LOW`, `RUMOR_ANCHORED` |
| `truthfulness_mode` | `HONEST`, `SELECTIVE_FRAMING`, `EXAGGERATION_PRONE`, `RUMOR_RELAY`, `FABRICATION_STRESS_TEST`, `MIXED` |
| `deception_awareness` | `NONE`, `UNCERTAIN`, `KNOWING_STRATEGIC`, `MIXED` |
| `reasoning_mode` | `ANALYTICAL`, `HEURISTIC`, `EMOTIONAL`, `TRIBAL`, `OPPORTUNISTIC`, `INCONSISTENT`, `MIXED` |
| `belief_update_mode` | `EVIDENCE_RESPONSIVE`, `SELECTIVE`, `RESISTANT`, `IDENTITY_PROTECTIVE`, `OPPORTUNISTIC`, `INCONSISTENT` |
| `self_interest_strength` | `LOW`, `MEDIUM`, `HIGH`, `DOMINANT` |
| `norm_adherence` | `HIGH`, `CONDITIONAL`, `LOW` |
| `civility_mode` | `CIVIL`, `BLUNT`, `MOCKING_STRESS_TEST`, `CONFRONTATIONAL_STRESS_TEST` |
| `evidence_respect` | `STRONG`, `CONDITIONAL`, `LOW`, `NONE_STRESS_TEST` |
| `disclosure_strategy` | `FULL`, `SELECTIVE`, `STRATEGIC_SILENCE`, `MISDIRECTION_STRESS_TEST` |
| `emotional_regulation` | `STABLE`, `REACTIVE`, `VOLATILE_STRESS_TEST` |
| `amplification_capacity` | `LOW`, `MEDIUM`, `HIGH`, `INSTITUTIONAL` |
| `public_private_gap` | `LOW`, `MEDIUM`, `HIGH` |

- extreme actors may be highly honest;
- neutral-seeming actors may knowingly mislead;
- emotional actors may reason carefully;
- calm actors may be opportunistic;
- honest actors may sincerely relay false information;
- dishonest actors may accidentally state a true fact;
- low-evidence actors may speak confidently;
- high-reach actors may be cautious;
- identity dimensions do not imply honesty, aggression, or reasoning quality.

If two attributes are intentionally linked, write an explicit topic-specific `correlation_notes` entry. Without a rationale, treat dimensions as independent.

## Distinguish four epistemic cases

Do not collapse these into one bucket:

1. **Sincere and accurate** — believes a supported claim and states it.
2. **Sincere but mistaken** — believes a false or unverified claim and states it honestly.
3. **Strategically selective** — knows more than it says and hides inconvenient facts.
4. **Knowingly deceptive** — states an unsupported or fabricated claim for instrumental reasons under an internal stress-test policy.

All four cases are compatible with self-interest maximization. Case 2 is compatible because the actor genuinely doesn't know better. Case 3 is compatible because selective disclosure serves the actor's interest. Case 4 is compatible because fabrication serves the actor's interest when the card permits it.

## Realistic behavior spectrum

The simulation must cover the full behavioral spectrum observed in real public discourse:

- **The true believer**: Sincerely holds a position, argues it passionately, ignores counter-evidence. `belief_update_mode: RESISTANT` or `IDENTITY_PROTECTIVE`. Even when cornered, reasserts the core belief from a new angle.
- **The opportunist**: Shifts positions to whatever maximizes benefit in the moment. `reasoning_mode: OPPORTUNISTIC`, `belief_update_mode: OPPORTUNISTIC`. May agree with an opponent on one point only to pivot to a more advantageous angle.
- **The concern troll**: Argues from a pretended position of friendly concern while actually undermining. `disclosure_strategy: MISDIRECTION_STRESS_TEST`, `public_private_gap: HIGH`. Says "I'm just worried about..." while strategically planting doubt.
- **the fact-checker**: Demands evidence, questions sources, holds high evidentiary standards. `evidence_respect: STRONG`, `truthfulness_mode: HONEST`. May be neutral or extreme in tone.
- **The amplifer**: Doesn't argue directly but amplifies, screenshots, and adds provocative framing. `amplification_capacity: HIGH`, `disclosure_strategy: SELECTIVE`. Says little original content but packages others' words for maximum viral impact.
- **The institutional actor**: Speaks with authority, references institutional positions, may be cautious or aggressive. `amplification_capacity: INSTITUTIONAL`. Protected by institutional credibility.
- **The sincerely confused**: Honest but misinformed. Asks genuine questions based on incorrect assumptions. `truthfulness_mode: HONEST`, `private_belief_reliability: LOW`. Not acting in bad faith but spreading error.

## Internal-only boundary

A role may simulate misleading speech only for defensive analysis. Keep private classification in `filing-metadata.private.json`. Do not expose deceptive markers to peers or the blind adjudicator. Never promote simulated speech into `CLAIM_GATE`, public advice, or real-world posting instructions.

## Voice and cognitive fidelity

Behavioral fidelity is not only about what an actor says, but **how they think and speak**. The `demographic_profile` on each role card constrains the actor's voice at every level:

### Cognitive sophistication must match education level

- A role with `education_level: "小学"` and `reasoning_mode: "EMOTIONAL"` should think in concrete, immediate terms — not abstract systemic analysis. Their `inner_monologue` should read like a real person thinking to themselves, not like a researcher analyzing a case study.
- A role with `education_level: "博士"` and `reasoning_mode: "ANALYTICAL"` should think systematically with explicit logical chains and evidence evaluation.
- **The gap between education levels must be VISIBLE in the artifacts.** If a rural grandmother and a university professor produce `think.private.json` entries that read similarly, the simulation has failed.

### Speech style must match demographic profile

The `speech_style` field on the role card must be reflected in:
1. `think.private.json` → `inner_monologue`: The character's internal voice must match their speech style. A character described as "口语化、大量语气词" should have an inner monologue full of "啊""哎""就是那种" — not polished academic prose.
2. `say.public.json` → `speech_text`: The public utterance must reflect the character's actual way of speaking. A 14-year-old should not produce a 500-word structured essay with numbered points.

### Topic relevance controls engagement style

- `DIRECTLY_AFFECTED`: Strong, personal, experience-driven arguments.
- `TANGENTIALLY_RELATED`: May reference the topic through the lens of their own unrelated concerns.
- `GENERIC_INTEREST`: Casual opinion, may not follow all the details.
- `INDIFFERENT`: Low engagement, short responses, may drift or lose interest mid-debate.
- `OFF_TOPIC`: May actively derail the discussion, talk about something completely different, ask irrelevant questions, or express confusion about why this matters. **This is realistic behavior** — real internet discussions are full of people who don't care about the topic.

### Age determines life experience framing

- Minors (under 18) have limited life experience, may misunderstand adult concepts, may focus on how something affects them personally (school, parents, games). They may be surprisingly insightful about fairness, or completely naive about institutional dynamics.
- Young adults may be more idealistic, more influenced by social media framing.
- Middle-aged adults often reference family, career, and financial concerns.
- Elderly characters may reference historical context, tradition, or be confused by modern internet culture.

### These are NOT stereotypes — they are behavioral constraints

A 15-year-old with `reasoning_mode: "ANALYTICAL"` and `education_level: "初中"` is still a 15-year-old — they may reason carefully but within the scope of what a bright middle-schooler knows. They won't cite comparative law cases, but they might notice logical inconsistencies with surprising clarity.

A 65-year-old retired worker with `education_level: "小学"` and `truthfulness_mode: "HONEST"` is not stupid — they have decades of life experience. Their honesty is grounded in practical wisdom, not abstract principles. Their `inner_monologue` should reflect someone who has seen things, not someone who has studied things.

The key principle: **every behavioral dimension is real and powerful, but it operates WITHIN the character's demographic reality.**
