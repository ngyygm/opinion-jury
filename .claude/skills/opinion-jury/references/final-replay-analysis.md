# Final Full-Information Replay

## Purpose

Blind adjudication evaluates the public record without persona bias. The later private replay analyst explains behavioral risk using the complete private archive.

## Inputs

After verdicts exist, the replay analyst may read:

- all case-level role cards;
- all court assignments;
- all private `think` memos;
- all private `filing-metadata` files;
- all public `say` filings and transcripts;
- `CLAIM_GATE`;
- blind verdicts;
- continuity logs for reused roles.

## Required outputs

Private output:

```text
06-aggregation/private/full-replay-analysis.json
```

Redacted public summary:

```text
06-aggregation/public/stakeholder-reaction-summary.json
```

Explain:

- likely stakeholder reactions and private incentives;
- public/private gaps;
- sincere but mistaken reactions;
- strategic omission, exaggeration, rumor relay, and fabrication-stress-test signals;
- how the same actor changes across courts;
- which statements affected blind adjudication despite being unsupported;
- which risks deserve edits, fact checks, or human review.

### attacker_profiles

For each actor whose `filing-metadata` shows selective framing, rumor relay, exaggeration, or fabrication, produce a structured profile:

- **Real-world archetype** — what type of person this actor represents (e.g., partisan op-ed writer, viral social-media aggregator, opposition researcher, concern-trolling ally, bad-faith fact-checker).
- **Likely attack vector** — the channel they would use (mainstream op-ed, Twitter/X thread, TikTok clip, congressional hearing, regulatory complaint, open letter) and the specific talking points they would lead with.
- **Reach estimate** — how far the distortion could plausibly spread (niche audience, medium-viral, mainstream pickup, policy-level escalation) and the amplification path.
- **Credibility assessment** — whether the intended audience would find this actor persuasive on this topic, and why (institutional authority, perceived neutrality, demographic alignment, novelty of the framing).

### misrepresentation_targets

For each claim in `CLAIM_GATE` flagged as UNVERIFIED or CATEGORY_MISMATCH, map the distortion surface:

- **Vulnerable portion** — which specific part of the original content is most susceptible to misrepresentation.
- **Distortion mechanism** — how the claim would be twisted (out-of-context quote, selective statistic, false equivalence, guilt-by-association, motte-and-bailey).
- **Likely distorter** — which actor profile (from `attacker_profiles`) would deploy this distortion and to which audience.
- **Distorted artifact** — a concrete sketch of what the distorted version looks like as a meme, screenshot, pull-quote, or headline — the form it would take when it circulates.

### collateral_victims

Identify every party harmed beyond the content's intended target:

- **Institutions cited or referenced** — organizations, agencies, journals, or companies named in the content whose credibility could be collateral damage.
- **Demographic groups mentioned or implied** — populations who could be stereotyped, endangered, or politicized by the content's reception.
- **Third parties whose data or statements are used** — individuals or organizations whose prior work is quoted, cited, or re-contextualized.
- For each: why they are vulnerable (pre-existing narrative, ongoing litigation, regulatory scrutiny, public sensitivity) and what the impact looks like (harassment, funding cuts, legal exposure, reputational harm).

### interest_damage_map

Map whose material interests are at stake:

- **Revenue, reputation, regulatory standing, legal exposure** — for each stakeholder, catalog the concrete interest dimension.
- **Side alignment** — whether the stakeholder is on the pro-publication side or anti-publication side (or has a split incentive where different parts of their interest pull in opposite directions).
- **What they stand to gain or lose** — specific, tangible outcomes (market share, election outcome, grant renewal, lawsuit viability, platform policy change) tied to whether the content is published, amplified, or suppressed.

### contingency_matrix

Build a structured response matrix by attacker-type x scenario x severity:

- **Specific response options per cell** — for each combination of attacker archetype, attack scenario, and severity level, list concrete response actions (prebunking, rapid rebuttal, legal threat, platform takedown request, proactive disclosure, ally amplification).
- **"Do nothing" as an explicit option** — for each cell, include "do nothing" alongside its trade-off analysis (what happens if no response is mounted, how the damage curve evolves).
- **Time-sensitivity** — label each cell with its escalation speed (hours, days, weeks) and note which scenarios escalate fastest, so the publisher knows where to allocate immediate attention.

### self_interest_vs_stated_position

The core risk signal. For each actor category:

- **Gap between private incentive and public claim** — where the actor's material self-interest diverges from the position they articulate publicly. This gap is the highest-risk predictor of strategic behavior.
- **Gap magnitude ranking** — which gaps are largest, meaning which actors have the most to lose and are simultaneously making the most contrary public claims. These are the actors most likely to act unpredictably or aggressively.
- **Publisher implication** — what the gap means for the content publisher: which actors to monitor most closely, which public statements to discount, and which private incentives to prepare countermeasures against.

Mark all actor outputs as simulation hypotheses, not empirical predictions.

### balanced_assessment (REQUIRED)

The replay analyst MUST include a balanced assessment section. This is critical — the simulation is run at extreme settings, and not every risk identified translates to real-world danger.

```json
{
  "balanced_assessment": {
    "attack_resilience": [
      {
        "attack_description": "description of a simulated attack",
        "neutral_actor_response": "how neutral/moderate actors in the simulation responded",
        "gained_traction": true/false,
        "evidence_refs": ["turn refs showing neutral actors' responses"]
      }
    ],
    "content_strengths": [
      {
        "strength": "specific aspect of the content that resists distortion",
        "why_strong": "explanation of why this aspect is resilient",
        "simulated_test_refs": ["turn refs where actors tried and failed to distort this"]
      }
    ],
    "net_verdict": "An honest summary: is this content likely to cause a real PR crisis? Or are the simulated risks largely theoretical given the content's actual design quality? Be specific.",
    "overreaction_warning": "Flag cases where the simulation's extreme setting (EXTREME_STRESS_TEST actors, FABRICATION_STRESS_TEST) may overstate real-world risk. Identify which attacks would not occur in practice or would not gain traction with real audiences.",
    "modification_priority": [
      {
        "item": "specific change needed",
        "priority": "MUST_FIX | RECOMMENDED | OPTIONAL",
        "reasoning": "why this priority level"
      }
    ]
  }
}
```

#### How to produce the balanced assessment

1. **Review neutral actors' actual responses** — Read what MODERATE or NEUTRAL-extremity actors actually said during debate. Did they side with attackers? Did they remain unconvinced? Did they defend the content? This is the strongest signal of real-world risk.

2. **Check if attacks gained traction** — During PEER_CROSS_CHALLENGE rounds, did other actors adopt or amplify the attack? Or was the attack isolated to the attacker alone? Attacks that failed to convince anyone in the simulation are lower real-world risk.

3. **Identify content strengths** — Which parts of the content did even hostile actors fail to distort? Which arguments survived cross-examination? These are the content's defensive strengths.

4. **Distinguish simulation artifacts from real risk** — The simulation includes EXTREME_STRESS_TEST actors and FABRICATION_STRESS_TEST actors by design. These represent worst-case scenarios. If only stress-test actors attacked and no moderate actors were swayed, the real-world risk is lower than the raw attack count suggests.

5. **Assign modification priorities honestly** — Not everything flagged needs fixing. Some risks are acceptable. Some attacks would happen regardless of content quality. Be honest about what actually needs to change versus what is just noise.
