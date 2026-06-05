# Filesystem Isolation Contract

## Principle

Filesystem scoping is the multi-blind boundary. Prompt-only instructions are insufficient.

## Debater view

For each actor invocation, materialize a read-only `scoped-view/`. It may contain only:

- source content;
- approved observable evidence subset;
- current public court question;
- actor's own role card;
- actor's own assignment;
- actor's own previous private memo and own previous private filing metadata when needed;
- frozen public transcript snapshot from prior rounds;
- public disclosures.

It must not contain:

- another actor's role card, assignment, private memo, filing metadata, or draft;
- identity mappings;
- blind verdict packet;
- final replay output;
- full case root.

## Public transcript rule

Only `say.public.json` files are eligible for transcript append. Never append `think.private.json`, `filing-metadata.private.json`, behavior profiles, or internal risk markers.

## Blind adjudicator view

The terminal blind adjudicator gets only:

- court question;
- final anonymous transcript;
- registered public evidence;
- neutral `CLAIM_GATE`;
- public disclosures.

It must not receive role cards, assignments, private memos, filing metadata, behavior profiles, identity maps, or stress-test labels.

## Final replay view

The post-verdict private replay analyst may receive the complete private archive. Its output is private by default. Only a redacted stakeholder summary may enter the final report.
