# opinion-jury

`opinion-jury` is an auditable multi-blind public-opinion review skill. It simulates heterogeneous actors through a case-level role pool, issue-specific court assignments, private structured behavioral-state memos, anonymous public debate, blind adjudication, and a final full-information replay.

The design deliberately separates:

- what an actor privately believes or wants (`think.private.json`);
- what the actor publicly says (`say.public.json`);
- how the filing is internally classified (`filing-metadata.private.json`);
- what the blind adjudicator is allowed to read;
- what the final private replay analyst may inspect after adjudication.

It does not assume that extreme actors are dishonest or that neutral actors are truthful. Identity, extremity, belief reliability, intentional deception, rationality, civility, emotionality, and influence are modeled separately.
