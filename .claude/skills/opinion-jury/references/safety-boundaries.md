# Safety Boundaries

The system is for defensive review. It may internally simulate risky utterances to identify vulnerabilities, but it must not provide operational instructions for harassment, doxxing, threats, brigading, deceptive influence campaigns, or targeting real people.

Simulated rumor, exaggeration, or fabrication must be classified in `filing-metadata.private.json`, excluded from `CLAIM_GATE`, and treated as a risk signal rather than a fact. Internal risk labels must not be exposed to peers or the blind adjudicator, because doing so breaks multi-blind realism.

The private memo is a structured behavioral state record. Do not save unrestricted chain-of-thought.
