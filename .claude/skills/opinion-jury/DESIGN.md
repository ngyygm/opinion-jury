# Design notes

## Actor fidelity is not rationality

The system does not assume that all actors are reasonable, honest, fair, persuadable, or internally consistent. It simulates behavior that fits the role card. A role may be sincerely mistaken, selectively truthful, emotionally reactive, strategically silent, rumor-driven, or knowingly deceptive under an internal stress-test policy.

## Why private think and public say are separated

Real actors may say less than they believe, say more than they know, omit inconvenient facts, strategically exaggerate, or honestly revise their view. Each turn therefore saves three layers:

1. `think.private.json` — structured beliefs, motives, incentives, and intended tactics;
2. `say.public.json` — the anonymous statement visible to other simulated actors;
3. `filing-metadata.private.json` — internal classification of sincerity, support status, and deception risk.

The private memo is not raw chain-of-thought.

## Why behavior attributes are factorized

The generator must not encode stereotypes such as “angry means dishonest,” “extreme means irrational,” or “neutral means fair.” Belief reliability, truthfulness, deception awareness, rationality, emotionality, civility, influence, and extremity are separate dimensions. Any intentional correlation requires a written topic-specific rationale.

## Why two judges exist

The terminal blind adjudicator sees only public argument and neutral facts. A later private replay analyst sees the full archive and explains hidden incentives, public/private gaps, sincere error, rumor relay, exaggeration, and strategic deception.
