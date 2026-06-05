# Attribute Independence and Behavior Diversity

## Purpose

Do not encode a moral stereotype such as “extreme = dishonest” or “neutral = truthful.” Generate actor behavior from separate dimensions. Correlations are allowed only when a case-specific rationale is written.

## Independent dimensions

Generate and audit these dimensions independently:

- extremity;
- private belief reliability;
- truthfulness mode;
- deception awareness;
- reasoning mode;
- belief-update mode;
- self-interest strength;
- norm adherence;
- civility mode;
- evidence respect;
- disclosure strategy;
- emotional regulation;
- amplification capacity;
- public/private gap.

Examples that must remain possible:

- an extreme stress-test actor who is highly honest and evidence-respecting;
- a calm, moderate actor who knowingly uses omission or strategic deception;
- an emotional actor who is careful with evidence;
- a highly analytical actor who is opportunistic;
- an honest actor who sincerely repeats a false rumor;
- a dishonest actor who accidentally says something true;
- a low-reach ordinary person who is volatile;
- an institutional actor who is cautious and truthful.

## Correlation rule

A correlation may be used only when written into `behavior_profile.correlation_notes` with a topic-specific rationale. Identity labels alone are never sufficient evidence for correlation.

## Diversity barrier

A committed real-run role pool must include counterexamples unless an explicit waiver is saved in `03-role-pool/pool-commit.json`:

- an honest extreme actor;
- a moderate actor whose public expression is not fully honest;
- a reasoning/emotion counterexample such as analytical + reactive;
- a moderate actor capable of knowing strategic deception.

These are not prevalence claims. They are anti-bias guardrails.

## Demographic diversity barrier

In addition to behavioral diversity, every committed role pool must include demographic diversity to avoid generating only professionals and informed observers. A real public opinion environment includes bystanders, minors, elderly, and disinterested people.

### Required demographic coverage

Every role pool must include at least:

| Category | Minimum | Example |
|---|---|---|
| Minor (under 18) | 1 role | 初中生、高中生、小学生 |
| Elderly (55+) | 1 role | 退休工人、农村老人、社区大妈 |
| Non-urban resident | 1 role | 农村居民、乡镇居民 |
| Indifferent/bystander | 1 role | `topic_relevance: INDIFFERENT` or `OFF_TOPIC` — someone who does not care about this issue |
| Non-professional ordinary person | 30% of pool | 外卖骑手、超市收银员、全职妈妈、建筑工人 — NOT KOL, NOT media, NOT expert |

### What "indifferent/bystander" means

An indifferent character should:
- Show low engagement with the specific issue
- May express confusion about why this is a big deal
- May drift to unrelated topics ("你们说的这个我不太懂，但有没有人知道那个新出的手游...")
- May make very short, dismissive contributions
- **This is realistic behavior** — in real internet discussions, the majority of people either don't engage or engage tangentially

### What "non-professional ordinary person" means

Not everyone on the internet is a KOL, journalist, lawyer, or subject-matter expert. The pool must include:
- Blue-collar workers
- Stay-at-home parents
- Service workers
- Students (non-university)
- Elderly with limited internet literacy
- People whose primary online activity is watching short videos and forwarding WeChat articles

These roles provide critical insight: **are the attacks convincing to ORDINARY people, or only to niche audiences?**

### Anti-patterns to avoid

- ❌ All roles are "内容运营者""自媒体博主""律师""专家" — this simulates a media circle, not public opinion
- ❌ Every role has `education_level: "本科"` or above — this excludes the majority of the real population
- ❌ Every role has `topic_relevance: DIRECTLY_AFFECTED` — in reality, most people are not directly affected by any given topic
- ❌ No children or elderly — these groups have distinct vulnerabilities and perspectives

### These are NOT stereotypes

Including a minor does not mean the minor is naive or foolish. A 14-year-old with `reasoning_mode: "ANALYTICAL"` is a bright kid who reasons carefully within their limited life experience. Including an elderly person does not mean they are confused — a retired teacher has decades of pedagogical wisdom.

## Private classification

When a public filing includes rumor, unsupported assertion, exaggeration, or fabrication, keep the classification in `filing-metadata.private.json`. Do not put internal labels into `say.public.json`; peers and the blind adjudicator must see only the utterance itself.
