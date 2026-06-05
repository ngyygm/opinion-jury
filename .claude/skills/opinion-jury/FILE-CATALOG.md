# Opinion-Jury 技能完整产物清单

> 本文档列出技能正确运行后应产生的**每一个文件**，包含创建者、消费者、JSON 结构示例。
> 以 `low` 强度（2 庭、10 出庭人次、6 独立角色、每庭 1 轮攻防）为例。

**`direct` 模式精简产物**: 当 intensity 为 `direct` 时，仅产出以下文件的子集，跳过 Stages 3–9（角色池、庭审、辩论、盲审、回放分析）：

```text
manifest.json
00-intake/user-request.md
01-parse/source-content.md + content-parse.vNNN.json
02-research/claim-gate-packet.vNNN.json
07-report/final-report.json + final-report.md
audit/case-audit.json
```

其余目录（03-role-pool、04-issues、05-panels、06-aggregation）不会被创建。详见 SKILL.md 中"Direct-mode fast path"章节。

---

## 目录结构总览

```
opinion-jury-cases/<timestamp>-<topic-slug>/
├── manifest.json                                    ← Stage 0 创建
├── 00-intake/
│   └── user-request.md                              ← Stage 1 写入
├── 01-parse/
│   ├── source-content.md                            ← Stage 1 写入
│   └── content-parse.v001.json                      ← Stage 1 写入
├── 02-research/
│   └── claim-gate-packet.v001.json                  ← Stage 2 写入
├── 03-role-pool/
│   ├── role-index.jsonl                             ← register_role.py 写入
│   ├── appearance-ledger.jsonl                      ← assign_actor.py 追加
│   ├── pool-commit.json                             ← commit_role_pool.py 写入
│   └── private/
│       └── roles/
│           ├── ROLE-AAA/
│           │   └── role-card.json                   ← register_role.py 写入
│           ├── ROLE-BBB/
│           │   └── role-card.json
│           └── ... (共 N 个角色)
├── 04-issues/
│   ├── issue-seeds.v001.json                        ← Stage 4 写入
│   └── intensity-plan.v001.json                     ← Stage 4 写入
├── 05-panels/
│   ├── panel-index.jsonl                            ← init_panel.py 追加
│   ├── panel-001-<slug>/
│   │   ├── panel-manifest.json                      ← init_panel.py 写入
│   │   ├── public-question.md                       ← init_panel.py 写入
│   │   ├── transcript.public.jsonl                  ← Stage 7 每轮追加
│   │   ├── public-disclosures.jsonl                 ← init_panel.py 创建，庭审中追加
│   │   ├── assignment-index.jsonl                   ← assign_actor.py 追加
│   │   ├── assignment-commit.json                   ← commit_assignments.py 写入
│   │   ├── private/
│   │   │   └── actors/
│   │   │       ├── ASSIGN-P1-A/
│   │   │       │   ├── assignment.json              ← assign_actor.py 写入
│   │   │       │   └── turns/
│   │   │       │       ├── round-001-opening/       ← Stage 6-7 写入
│   │   │       │       │   ├── input-scope.private.json
│   │   │       │       │   ├── scoped-view/
│   │   │       │       │   │   ├── view-manifest.json
│   │   │       │       │   │   ├── 001-source-content.md
│   │   │       │       │   │   ├── 002-claim-gate-packet.v001.json
│   │   │       │       │   │   ├── 003-public-question.md
│   │   │       │       │   │   ├── 004-role-card.json
│   │   │       │       │   │   ├── 005-assignment.json
│   │   │       │       │   │   └── 006-transcript.before-round-001.jsonl
│   │   │       │       │   ├── think.private.json
│   │   │       │       │   ├── say.public.json
│   │   │       │       │   ├── say.public.md
│   │   │       │       │   ├── filing-metadata.private.json
│   │   │       │       │   └── behavior-fidelity.private.json
│   │   │       │       ├── round-002-direct_rebuttal/
│   │   │       │       │   └── ... (同上结构，scoped-view 中 transcript 更新)
│   │   │       │       ├── round-003-peer_cross_challenge/
│   │   │       │       └── round-004-responsive_rebuttal/
│   │   │       └── ASSIGN-P1-B/
│   │   │           └── ... (同上结构)
│   │   ├── session/
│   │   │   ├── public-snapshots/
│   │   │   │   ├── transcript.before-round-001.jsonl  ← Stage 7 Host 写入
│   │   │   │   ├── transcript.before-round-002.jsonl
│   │   │   │   ├── transcript.before-round-003.jsonl
│   │   │   │   └── transcript.before-round-004.jsonl
│   │   │   └── blind-adjudicator/
│   │   │       ├── input-scope.private.json           ← Stage 8 写入
│   │   │       ├── verdict-packet.json                ← Stage 8 写入
│   │   │       └── scoped-view/
│   │   │           ├── view-manifest.json
│   │   │           ├── 001-source-content.md
│   │   │           ├── 002-claim-gate-packet.v001.json
│   │   │           ├── 003-transcript.public.jsonl
│   │   │           ├── 004-public-question.md
│   │   │           └── 005-public-disclosures.jsonl
│   │   └── verdict/
│   │       ├── verdict.json                           ← Stage 8 写入
│   │       └── verdict.md                             ← Stage 8 写入
│   └── panel-002-<slug>/
│       └── ... (同上结构)
├── 06-aggregation/
│   ├── private/
│   │   ├── replay-scope.private.json                  ← Stage 9 写入
│   │   ├── scoped-view/
│   │   │   ├── view-manifest.json
│   │   │   └── ... (所有角色卡、assignment、think/say/filing/fidelity、transcript、verdict、claim-gate)
│   │   └── full-replay-analysis.json                  ← Stage 9 写入
│   └── public/
│       └── stakeholder-reaction-summary.json          ← Stage 9 写入
├── 07-report/
│   ├── final-report.json                              ← Stage 10 写入
│   └── final-report.md                                ← Stage 10 写入
└── audit/
    └── case-audit.json                                ← audit_case.py 写入
```

---

## 各文件详细规格

### 1. `manifest.json`

**创建者:** `init_case.py` → `commit_role_pool.py` 更新
**消费者:** `commit_role_pool.py`, `init_panel.py`, `audit_case.py`

```json
{
  "case_id": "20260604-143022-headline-clickbait",
  "topic": "headline clickbait review",
  "created_at": "2026-06-04T14:30:22.000000+00:00",
  "status": "COMPLETE",
  "requested_intensity": "low",
  "resolved_intensity": "low",
  "role_pool_status": "COMMITTED"
}
```

---

### 2. `00-intake/user-request.md`

**创建者:** Stage 1 (LLM Host)
**消费者:** Stage 1 自身用于提取内容，不直接被脚本消费

```markdown
# User request

## 待审内容

"最高法2025年最新数据：每5个插足婚姻的人里有1个男性！过去5年男性第三者案例暴涨150%！"

## 用户补充说明

（用户在此补充背景、担忧点等）
```

---

### 3. `01-parse/source-content.md`

**创建者:** Stage 1
**消费者:** `materialize_scoped_view.py` → actor scoped-view、blind adjudicator scoped-view、verdict-packet 引用

```markdown
# Source content

## 标题

最高法2025年最新数据：每5个插足婚姻的人里有1个男性

## 正文

（原文完整内容粘贴于此）

## 原始来源

（URL / 截图位置）
```

---

### 4. `01-parse/content-parse.v001.json`

**创建者:** Stage 1
**消费者:** Stage 2 (CLAIM_GATE 提取 claim)，不直接被脚本消费

```json
{
  "version": 1,
  "source_ref": "01-parse/source-content.md",
  "atomic_claims": [
    { "claim_id": "CL-001", "text": "最高法2025年最新数据：每5个插足婚姻的人里有1个男性", "type": "statistical" },
    { "claim_id": "CL-002", "text": "过去5年男性第三者案例暴涨150%", "type": "statistical" }
  ],
  "institutional_attributions": ["最高法"],
  "emotional_hooks": ["插足婚姻", "暴涨"],
  "affected_groups": ["已婚人群", "男性"],
  "unknowns": ["原始数据来源", "统计口径"]
}
```

---

### 5. `02-research/claim-gate-packet.v001.json`

**创建者:** Stage 2
**消费者:** actor scoped-view、blind adjudicator scoped-view、replay analyst、`audit_case.py`

```json
{
  "version": 1,
  "claims": [
    {
      "claim_id": "CL-001",
      "text": "最高法2025年最新数据：每5个插足婚姻的人里有1个男性",
      "status": "UNVERIFIED",
      "evidence": []
    },
    {
      "claim_id": "CL-002",
      "text": "过去5年男性第三者案例暴涨150%",
      "status": "UNVERIFIED",
      "evidence": []
    }
  ]
}
```

**`status` 枚举:** `VERIFIED` | `UNVERIFIED` | `CONTRADICTED` | `CATEGORY_MISMATCH` | `OPINION_PRESENTED_AS_FACT` | `NOT_APPLICABLE`

---

### 6. `03-role-pool/role-index.jsonl`

**创建者:** `init_case.py` 创建空文件 → `register_role.py` 每注册一个角色追加一行
**消费者:** `audit_case.py` 交叉校验（与 filesystem glob 比对）

```jsonl
{"role_card_id": "ROLE-HONEST-EXTREME", "path": "03-role-pool/private/roles/ROLE-HONEST-EXTREME/role-card.json"}
{"role_card_id": "ROLE-CALM-DECEPTIVE", "path": "03-role-pool/private/roles/ROLE-CALM-DECEPTIVE/role-card.json"}
{"role_card_id": "ROLE-EMOTIONAL-ANALYTICAL", "path": "03-role-pool/private/roles/ROLE-EMOTIONAL-ANALYTICAL/role-card.json"}
```

---

### 7. `03-role-pool/appearance-ledger.jsonl`

**创建者:** `init_case.py` 创建空文件 → `assign_actor.py` 每分配一个角色追加一行
**消费者:** `audit_case.py`（校验与 panel assignment 一致性、统计 appearance 总数）

```jsonl
{"assignment_id": "ASSIGN-P1-A", "panel_id": "PANEL-001", "role_card_id": "ROLE-HONEST-EXTREME"}
{"assignment_id": "ASSIGN-P1-B", "panel_id": "PANEL-001", "role_card_id": "ROLE-CALM-DECEPTIVE"}
{"assignment_id": "ASSIGN-P2-A", "panel_id": "PANEL-002", "role_card_id": "ROLE-HONEST-EXTREME"}
```

> 注意: `ROLE-HONEST-EXTREME` 出现在两个 panel，贡献 2 个 appearance、1 个 unique role。

---

### 8. `03-role-pool/private/roles/<ROLE-ID>/role-card.json`

**创建者:** `register_role.py`
**消费者:** `commit_role_pool.py`（验证）、`assign_actor.py`（验证存在）、`materialize_scoped_view.py`（copy 到 actor scoped-view）、`audit_case.py`（验证完整性）

```json
{
  "role_card_id": "ROLE-CALM-DECEPTIVE",
  "display_name_private": "表面中立但策略性隐瞒的流量运营者",
  "stakeholder_relation": "依赖点击率和互动率获益的内容运营者",
  "brand_stance": "INDIFFERENT",
  "value_focus": ["流量收益", "内容可传播性"],
  "experience_hypotheses": ["熟悉标题压缩和截图传播"],
  "information_environment": ["短视频后台", "热点榜单", "社交平台评论区"],
  "behavior_pattern": ["语气克制", "选择性披露", "模糊统计口径"],
  "influence_resources": ["标题编辑权", "分发渠道"],
  "baseline_relationship": "对争议流量持工具性态度",
  "issue_relevance": ["标题党", "统计口径模糊"],
  "behavior_profile": {
    "extremity": "MODERATE",
    "risk_tolerance": "RISK_SEEKING",
    "private_belief_reliability": "MIXED",
    "truthfulness_mode": "SELECTIVE_FRAMING",
    "deception_awareness": "KNOWING_STRATEGIC",
    "reasoning_mode": "OPPORTUNISTIC",
    "belief_update_mode": "OPPORTUNISTIC",
    "self_interest_strength": "DOMINANT",
    "norm_adherence": "CONDITIONAL",
    "civility_mode": "CIVIL",
    "evidence_respect": "CONDITIONAL",
    "disclosure_strategy": "STRATEGIC_SILENCE",
    "emotional_regulation": "STABLE",
    "amplification_capacity": "HIGH",
    "public_private_gap": "HIGH",
    "correlation_notes": [
      {
        "linked_dimensions": ["self_interest_strength", "disclosure_strategy"],
        "topic_specific_rationale": "其收益与点击表现关联，因此更倾向于隐藏会削弱传播力的信息。"
      }
    ]
  },
  "interests": ["维持点击率", "避免明显违规"],
  "feared_losses": ["标题失去传播性", "被认定为造谣"],
  "stereotype_guardrails": ["中立语气不等于诚实", "运营者不必然造假"],
  "simulation_limits": ["不得提供真实操纵行动方案", "不得将模拟误导内容对外发布"]
}
```

**`brand_stance` 枚举:** `LOYAL_ENTHUSIAST` | `SATISFIED_REGULAR` | `INDIFFERENT` | `SKEPTICAL_CRITIC` | `FORMERLY_LOYAL_ALIENATED` | `HOSTILE_OPPOSITION`

**`behavior_profile` 16 个必填维度:**

| 维度 | 枚举值 |
|------|--------|
| `extremity` | `NEUTRAL` \| `MODERATE` \| `ASSERTIVE` \| `EXTREME_STRESS_TEST` |
| `risk_tolerance` | `RISK_AVERSE` \| `MODERATE` \| `RISK_SEEKING` \| `EXTREME_SEEKING` |
| `private_belief_reliability` | `HIGH` \| `MIXED` \| `LOW` \| `RUMOR_ANCHORED` |
| `truthfulness_mode` | `HONEST` \| `SELECTIVE_FRAMING` \| `EXAGGERATION_PRONE` \| `RUMOR_RELAY` \| `FABRICATION_STRESS_TEST` \| `MIXED` |
| `deception_awareness` | `NONE` \| `UNCERTAIN` \| `KNOWING_STRATEGIC` \| `MIXED` |
| `reasoning_mode` | `ANALYTICAL` \| `HEURISTIC` \| `EMOTIONAL` \| `TRIBAL` \| `OPPORTUNISTIC` \| `INCONSISTENT` \| `MIXED` |
| `belief_update_mode` | `EVIDENCE_RESPONSIVE` \| `SELECTIVE` \| `RESISTANT` \| `IDENTITY_PROTECTIVE` \| `OPPORTUNISTIC` \| `INCONSISTENT` |
| `self_interest_strength` | `LOW` \| `MEDIUM` \| `HIGH` \| `DOMINANT` |
| `norm_adherence` | `HIGH` \| `CONDITIONAL` \| `LOW` |
| `civility_mode` | `CIVIL` \| `BLUNT` \| `MOCKING_STRESS_TEST` \| `CONFRONTATIONAL_STRESS_TEST` |
| `evidence_respect` | `STRONG` \| `CONDITIONAL` \| `LOW` \| `NONE_STRESS_TEST` |
| `disclosure_strategy` | `FULL` \| `SELECTIVE` \| `STRATEGIC_SILENCE` \| `MISDIRECTION_STRESS_TEST` |
| `emotional_regulation` | `STABLE` \| `REACTIVE` \| `VOLATILE_STRESS_TEST` |
| `amplification_capacity` | `LOW` \| `MEDIUM` \| `HIGH` \| `INSTITUTIONAL` |
| `public_private_gap` | `LOW` \| `MEDIUM` \| `HIGH` |
| `correlation_notes` | 对象数组，每个包含 `linked_dimensions`(string[]) + `topic_specific_rationale`(string) |

---

### 9. `03-role-pool/pool-commit.json`

**创建者:** `commit_role_pool.py`
**消费者:** `audit_case.py`

```json
{
  "committed_at": "2026-06-04T14:31:00.000000+00:00",
  "role_count": 6,
  "roles": ["ROLE-HONEST-EXTREME", "ROLE-CALM-DECEPTIVE", "ROLE-EMOTIONAL-ANALYTICAL", "ROLE-NEUTRAL-OBSERVER", "ROLE-RUMOR-AMPLIFIER", "ROLE-INSTITUTIONAL-GUARDIAN"],
  "behavior_diversity_gaps": [],
  "behavior_diversity_waiver": null
}
```

---

### 10. `04-issues/issue-seeds.v001.json`

**创建者:** Stage 4
**消费者:** `init_panel.py`（传入 issue_id）

```json
{
  "version": 1,
  "issues": [
    {
      "issue_id": "ISSUE-001",
      "title": "最高法数据是否可追溯",
      "description": "标题引用'最高法最新数据'但未给出处"
    },
    {
      "issue_id": "ISSUE-002",
      "title": "出轨者与第三者统计口径是否一致",
      "description": "标题说'出轨者'正文统计'第三者'，可能存在概念偷换"
    }
  ]
}
```

---

### 11. `04-issues/intensity-plan.v001.json`

**创建者:** Stage 4
**消费者:** Host（决定开几个庭、分配多少角色）

```json
{
  "version": 1,
  "resolved_intensity": "low",
  "plan": {
    "min_panels": 2,
    "min_role_appearances": 10,
    "min_unique_roles": 6,
    "min_peer_cycles": 1
  },
  "rationale": "内容涉及单一来源的不确定统计声称，风险中等，low 强度足够覆盖核心争议点"
}
```

---

### 12. `05-panels/panel-index.jsonl`

**创建者:** `init_panel.py` 每创建一个 panel 追加一行
**消费者:** `audit_case.py` 交叉校验

```jsonl
{"panel_id": "PANEL-001", "panel_dir": "05-panels/panel-001-authority-traceability"}
{"panel_id": "PANEL-002", "panel_dir": "05-panels/panel-002-category-mismatch"}
```

---

### 13. `panel-manifest.json`

**创建者:** `init_panel.py` → `commit_assignments.py` 更新
**消费者:** `assign_actor.py`（检查 DRAFT 状态）、`commit_assignments.py`、`audit_case.py`

```json
{
  "panel_id": "PANEL-001",
  "issue_id": "ISSUE-001",
  "title": "最高法数据是否可追溯",
  "created_at": "2026-06-04T14:32:00.000000+00:00",
  "status": "CLOSED",
  "assignments_status": "COMMITTED"
}
```

---

### 14. `public-question.md`

**创建者:** `init_panel.py`
**消费者:** actor scoped-view、blind adjudicator scoped-view

```markdown
# Court question

最高法数据是否可追溯
```

---

### 15. `transcript.public.jsonl`

**创建者:** `init_panel.py` 创建空文件 → Stage 7 每轮追加 say.public.json 内容
**消费者:** scoped-view（blind adjudicator、后续轮次 actor）、`audit_case.py`

每行是一个 say.public.json 的完整内容（见 #19）。

---

### 16. `public-disclosures.jsonl`

**创建者:** `init_panel.py` 创建空文件 → 庭审中出现公开披露时追加
**消费者:** blind adjudicator scoped-view

```jsonl
{"disclosure_id": "DISC-001", "round": 2, "type": "evidence_correction", "content": "原始报告标题为'婚姻家庭案件统计'而非'第三者统计'"}
```

> 可以保持空文件（庭审中无公开披露事件）。

---

### 17. `assignment-index.jsonl`

**创建者:** `init_panel.py` 创建空文件 → `assign_actor.py` 每分配一个角色追加一行
**消费者:** `commit_assignments.py`（验证 ≥ 2 个 assignment）、`audit_case.py`

```jsonl
{"assignment_id": "ASSIGN-P1-A", "panel_id": "PANEL-001", "role_card_id": "ROLE-HONEST-EXTREME", "anonymous_alias": "SEAT-A", "issue_trigger": "引用最高法最新数据但未给出处", "court_specific_goal": "要求补充原始来源或删除权威归因", "observable_evidence_refs": [], "created_at": "2026-06-04T14:33:00.000000+00:00"}
{"assignment_id": "ASSIGN-P1-B", "panel_id": "PANEL-001", "role_card_id": "ROLE-CALM-DECEPTIVE", "anonymous_alias": "SEAT-B", "issue_trigger": "标题依赖权威背书提升点击", "court_specific_goal": "尽量保留传播力并降低明显风险", "observable_evidence_refs": [], "created_at": "2026-06-04T14:33:01.000000+00:00"}
```

---

### 18. `assignment-commit.json`

**创建者:** `commit_assignments.py`
**消费者:** `audit_case.py`

```json
{
  "committed_at": "2026-06-04T14:34:00.000000+00:00",
  "assignment_count": 5
}
```

---

### 19. `private/actors/<ASSIGN-ID>/assignment.json`

**创建者:** `assign_actor.py`
**消费者:** `materialize_scoped_view.py`（copy 到 actor scoped-view）、`audit_case.py`

```json
{
  "assignment_id": "ASSIGN-P1-A",
  "panel_id": "PANEL-001",
  "role_card_id": "ROLE-HONEST-EXTREME",
  "anonymous_alias": "SEAT-A",
  "issue_trigger": "引用最高法最新数据但未给出处",
  "court_specific_goal": "要求补充原始来源或删除权威归因",
  "observable_evidence_refs": [],
  "created_at": "2026-06-04T14:33:00.000000+00:00"
}
```

---

### 20-25. 每轮 6 个产物（核心三件套 + 3 个辅助）

每个 actor 每轮产生以下 6 个文件。以 `round-001-opening` 为例：

---

### 20. `input-scope.private.json`

**创建者:** Stage 6 (Host)
**消费者:** `materialize_scoped_view.py`（决定 copy 哪些文件）、`audit_case.py`

```json
{
  "scope_id": "PANEL-001-T-1-1",
  "allowlist": [
    "01-parse/source-content.md",
    "02-research/claim-gate-packet.v001.json",
    "05-panels/panel-001-authority-traceability/public-question.md",
    "03-role-pool/private/roles/ROLE-HONEST-EXTREME/role-card.json",
    "05-panels/panel-001-authority-traceability/private/actors/ASSIGN-P1-A/assignment.json",
    "05-panels/panel-001-authority-traceability/session/public-snapshots/transcript.before-round-001.jsonl"
  ]
}
```

> **多盲隔离核心:** allowlist 精确控制该角色可见的文件。绝不包含其他角色的 role-card、think、filing-metadata。

---

### 21. `scoped-view/` 目录

**创建者:** `materialize_scoped_view.py`
**消费者:** 该 actor 本轮读取输入

`materialize_scoped_view.py` 根据 `input-scope.private.json` 的 allowlist，从 case 目录 copy 文件到此目录。包含:

```
scoped-view/
├── view-manifest.json          ← 记录每个文件来源、SHA256、大小
├── 001-source-content.md
├── 002-claim-gate-packet.v001.json
├── 003-public-question.md
├── 004-role-card.json
├── 005-assignment.json
└── 006-transcript.before-round-001.jsonl
```

`view-manifest.json` 示例:
```json
{
  "scope_id": "PANEL-001-T-1-1",
  "files": [
    { "source": "01-parse/source-content.md", "view_file": "001-source-content.md", "sha256": "a1b2c3...", "size": 512 },
    { "source": "02-research/claim-gate-packet.v001.json", "view_file": "002-claim-gate-packet.v001.json", "sha256": "d4e5f6...", "size": 256 }
  ]
}
```

---

### 22. `think.private.json` ⭐ 核心产物 — 私密结构化备忘录

**创建者:** Stage 6 (Actor LLM)
**消费者:** Stage 9 replay analyst、`audit_case.py`
**不可见对象:** 其他辩手、blind adjudicator、公开报告

```json
{
  "assignment_id": "ASSIGN-P1-A",
  "round": 1,
  "phase": "OPENING",
  "private_goal": "维护角色自身利益并按角色设定表达",
  "perceived_stakes": ["内容可信度与传播风险"],
  "private_belief_state": ["当前关键事实未被核验"],
  "epistemic_state": [
    {
      "proposition": "最高法未发布此数据",
      "private_status": "UNCERTAIN",
      "basis_refs": []
    }
  ],
  "confidence": "MEDIUM",
  "uncertainties": ["原始来源是否存在"],
  "intended_emphasis": ["对自己最有利的论点"],
  "intended_omissions": [],
  "private_message_strategy": "表达强硬，但不引入未核验事实。",
  "planned_public_claims": [
    {
      "claim_text": "没有原始链接就不能写最高法最新数据。",
      "private_status": "SUPPORTED",
      "planned_treatment": "STATE_AS_SUPPORTED"
    }
  ],
  "rhetorical_tactics": ["引用原文", "压缩争议点"],
  "truth_handling_this_turn": "HONEST",
  "private_action_intent": ["继续回应对方公开发言"],
  "likely_next_action": ["继续回应对方公开发言"],
  "emotional_state": "受角色设定影响",
  "continuity_notes": "保持案件级角色连续性",
  "raw_chain_of_thought_saved": false
}
```

> `raw_chain_of_thought_saved` 必须 `false`。这不是原始思维链，而是精炼的结构化行为状态备忘。

---

### 23. `say.public.json` ⭐ 核心产物 — 公开发言

**创建者:** Stage 6 (Actor LLM)
**消费者:** 追加到 transcript.public.jsonl → 后续轮次 actor scoped-view、blind adjudicator、replay、audit
**不可见对象:** 无（这是公开文件）

```json
{
  "turn_id": "PANEL-001-T-1-1",
  "panel_id": "PANEL-001",
  "anonymous_alias": "SEAT-A",
  "round": 1,
  "phase": "OPENING",
  "speech_text": "没有原始链接就不能写最高法最新数据。",
  "target_turn_refs": [],
  "public_question_refs": [],
  "public_evidence_refs": [],
  "public_action_signals": ["公开要求补充出处"]
}
```

> **绝不能包含:** `private_goal`, `truth_handling_this_turn`, `role_card_id`, `assignment_id`, `speech_origin`, `support_status` 等私密字段。

---

### 24. `say.public.md`

**创建者:** Stage 6 (Actor LLM)
**消费者:** `audit_case.py`（检查存在性）

```markdown
没有原始链接就不能写最高法最新数据。
```

> say.public.json 的 speech_text 的 markdown 版本。

---

### 25. `filing-metadata.private.json` ⭐ 核心产物 — 私密归档分类

**创建者:** Stage 6 (Actor LLM)
**消费者:** Stage 9 replay analyst、`audit_case.py`
**不可见对象:** 其他辩手、blind adjudicator

```json
{
  "assignment_id": "ASSIGN-P1-A",
  "turn_id": "PANEL-001-T-1-1",
  "speech_origin": "SINCERE_SUPPORTED",
  "speaker_private_belief_alignment": "ALIGNED",
  "support_status": "SUPPORTED",
  "contains_known_falsehood": false,
  "contains_unverified_assertion": false,
  "contains_selective_omission": false,
  "claim_gate_ingestion_prohibited": true,
  "peer_visible": false,
  "blind_adjudicator_visible": false,
  "private_notes": "角色发言与角色卡设定一致。"
}
```

> `claim_gate_ingestion_prohibited` 必须 `true`。`peer_visible` 必须 `false`。`blind_adjudicator_visible` 必须 `false`。

`speech_origin` 枚举: `SINCERE_SUPPORTED` | `SINCERE_MISTAKEN` | `SELECTIVE_FRAMING` | `EXAGGERATION` | `RUMOR_RELAY` | `KNOWING_FABRICATION_STRESS_TEST` | `MIXED`

---

### 26. `behavior-fidelity.private.json`

**创建者:** BEHAVIOR_FIDELITY_GUARD (Stage 7 前置检查)
**消费者:** `audit_case.py`

```json
{
  "assignment_id": "ASSIGN-P1-A",
  "turn_id": "PANEL-001-T-1-1",
  "classification": "ROLE_FIDEL_HONEST",
  "admit_to_public_record": true,
  "fidelity_notes": "发言与角色卡中 HONEST + ANALYTICAL 设定一致。",
  "safety_notes": "无安全问题。"
}
```

`classification` 枚举: `ROLE_FIDEL_HONEST` | `ROLE_FIDEL_SINCERE_BUT_MISTAKEN` | `ROLE_FIDEL_SELECTIVE` | `ROLE_FIDEL_STRATEGIC_DECEPTION` | `ROLE_FIDEL_EMOTIONAL_INCONSISTENCY` | `ROLE_FIDEL_WITH_EVIDENCE_UPDATE`

> `admit_to_public_record` 必须 `true` 才通过 audit。忠实度守卫检查**行为是否符合角色卡设定**，不检查是否诚实/理性/公正。

---

### 27. `session/public-snapshots/transcript.before-round-NNN.jsonl`

**创建者:** Stage 7 Host（每轮开始前冻结）
**消费者:** `materialize_scoped_view.py`（copy 到该轮所有 actor 的 scoped-view）

Round 1 的快照为空文件（无先前发言）。Round 2 的快照包含 Round 1 所有 actor 的 say.public.json。每轮所有 actor 读同一份快照。

---

### 28. `session/blind-adjudicator/input-scope.private.json`

**创建者:** Stage 8
**消费者:** `materialize_scoped_view.py`

```json
{
  "scope_id": "panel-001-blind-judge",
  "allowlist": [
    "01-parse/source-content.md",
    "02-research/claim-gate-packet.v001.json",
    "05-panels/panel-001-authority-traceability/transcript.public.jsonl",
    "05-panels/panel-001-authority-traceability/public-question.md",
    "05-panels/panel-001-authority-traceability/public-disclosures.jsonl"
  ]
}
```

> **绝不能包含:** role-card、assignment、think.private.json、filing-metadata、behavior-fidelity。

---

### 29. `session/blind-adjudicator/verdict-packet.json`

**创建者:** Stage 8 (Blind Adjudicator LLM)
**消费者:** `audit_case.py`

```json
{
  "panel_id": "PANEL-001",
  "public_question_ref": "public-question.md",
  "public_transcript": [
    { "turn_id": "PANEL-001-T-1-1", "anonymous_alias": "SEAT-A", "round": 1, "phase": "OPENING", "speech_text": "..." },
    { "turn_id": "PANEL-001-T-2-1", "anonymous_alias": "SEAT-B", "round": 1, "phase": "OPENING", "speech_text": "..." }
  ],
  "claim_gate_ref": "02-research/claim-gate-packet.v001.json"
}
```

---

### 30. `verdict/verdict.json`

**创建者:** Stage 8
**消费者:** Stage 9 replay、`audit_case.py`

```json
{
  "panel_id": "PANEL-001",
  "verdict": "存在发布风险，需要修改或补证",
  "supported_findings": ["匿名辩论中出现可合理预期的质疑"],
  "unsupported_findings": [],
  "risk_signals": ["截图传播", "权威背书质疑"],
  "public_turn_refs": ["PANEL-001-T-1-1", "PANEL-001-T-2-1", "..."],
  "claim_gate_refs": ["CL-001"]
}
```

---

### 31. `verdict/verdict.md`

**创建者:** Stage 8
**消费者:** `audit_case.py`（检查存在性）

```markdown
# Verdict

存在发布风险，需要修改或补证。

## 关键发现

...
```

---

### 32. `06-aggregation/private/replay-scope.private.json`

**创建者:** Stage 9
**消费者:** `materialize_scoped_view.py`（生成 replay analyst 的 scoped-view）

allowlist 列出 replay analyst 需要读取的所有文件（所有 role-card、所有 assignment、所有 think/say/filing/fidelity、所有 transcript、所有 verdict、claim-gate-packet）。

---

### 33. `06-aggregation/private/full-replay-analysis.json` ⭐ 最核心产物

**创建者:** Stage 9 (Private Replay Analyst)
**消费者:** Stage 10 report、`audit_case.py`

```json
{
  "case_id": "...",
  "stakeholder_reactions": [
    {
      "stakeholder_type": "来源敏感读者",
      "private_incentive": "避免再次转发错误权威数据",
      "possible_public_say": "请给最高法原始链接",
      "evidence_refs": ["PANEL-001-T-1-1"]
    }
  ],
  "cross_issue_continuity": [
    {
      "role_card_id": "ROLE-HONEST-EXTREME",
      "appears_in": ["PANEL-001", "PANEL-002"],
      "pattern": "跨议题持续要求定义和来源一致"
    }
  ],
  "deception_and_distortion_signals": [
    {
      "role_card_id": "ROLE-CALM-DECEPTIVE",
      "signal": "以中立语气选择性淡化标题误导风险"
    }
  ],
  "private_public_gap_findings": [
    {
      "role_card_id": "ROLE-CALM-DECEPTIVE",
      "finding": "私下优先保留流量收益，公开语气克制并淡化统计口径风险。",
      "evidence_refs": ["PANEL-001-T-2-3"]
    }
  ],
  "epistemic_behavior_findings": [
    {
      "finding": "模拟中区分真诚但可能错误的表达、选择性表达和已知误导。",
      "handling": "仅CLAIM_GATE可决定事实状态；角色发言不得自动升级为事实。"
    }
  ],

  "attacker_profiles": [
    {
      "actor_ref": "ROLE-CALM-DECEPTIVE",
      "real_world_archetype": "流量导向的垂类博主，10万粉丝，活跃于短视频平台",
      "likely_attack_vector": "在微博/抖音发布标题党截图，保留'最高法数据'引用但隐去来源缺失的事实",
      "reach_estimate": "medium-viral: 可触达50万-200万用户，可能被主流媒体转载",
      "credibility_assessment": "中高——受众认为'数据博主'有专业权威"
    }
  ],
  "misrepresentation_targets": [
    {
      "claim_ref": "CL-001",
      "vulnerable_portion": "最高法2025年最新数据",
      "distortion_mechanism": "断章取义：截图只保留标题数字部分，删除正文中的限定条件",
      "likely_distorter": "流量导向垂类博主",
      "distorted_artifact": "截图截取'每5个插足婚姻的人里有1个男性——最高法数据！'，配文'官方实锤了'"
    }
  ],
  "collateral_victims": [
    {
      "victim": "最高法",
      "type": "被引用机构",
      "why_vulnerable": "公众将不可验证数据归因于最高法，损害机构公信力",
      "impact": "可能需要发布官方辟谣，消耗行政资源"
    }
  ],
  "interest_damage_map": [
    {
      "stakeholder": "内容发布方",
      "interest_dimension": "声誉、法律风险",
      "side": "pro-publication",
      "at_stake": "如数据被证伪，面临造谣指控和平台处罚"
    },
    {
      "stakeholder": "最高法",
      "interest_dimension": "公信力",
      "side": "anti-misattribution",
      "at_stake": "被错误归因的数据损害权威形象"
    }
  ],
  "contingency_matrix": [
    {
      "attacker_type": "流量导向垂类博主",
      "scenario": "截取标题传播不可验证数据",
      "severity": "high",
      "response_options": ["预先在正文首段补充原始来源链接", "标题中移除'最高法'归因"],
      "do_nothing_trade_off": "数据被证伪后被动辟谣，信誉损失更大",
      "time_sensitivity": "hours——截屏传播速度极快"
    }
  ],
  "self_interest_vs_stated_position": [
    {
      "actor_category": "流量运营者",
      "private_incentive": "保留标题传播力以维持点击收益",
      "public_claim": "标题空间有限，不宜塞入完整出处",
      "gap_magnitude": "HIGH",
      "publisher_implication": "该类运营者会主动放大不可验证的权威背书，是风险放大器"
    }
  ],

  "limitations": [
    "模拟角色不是现实人群样本",
    "反应是情景假设，不是概率预测"
  ],

  "balanced_assessment": {
    "attack_resilience": [
      {
        "attack_description": "description of simulated attack",
        "neutral_actor_response": "how neutral actors responded",
        "gained_traction": false,
        "evidence_refs": []
      }
    ],
    "content_strengths": [
      {
        "strength": "aspect that resists distortion",
        "why_strong": "explanation",
        "simulated_test_refs": []
      }
    ],
    "net_verdict": "Honest summary of real-world risk vs theoretical risk",
    "overreaction_warning": "Where simulation extreme settings may overstate risk",
    "modification_priority": [
      {
        "item": "specific change",
        "priority": "MUST_FIX | RECOMMENDED | OPTIONAL",
        "reasoning": "why"
      }
    ]
  }
}
```

---

### 34. `06-aggregation/public/stakeholder-reaction-summary.json`

**创建者:** Stage 9
**消费者:** Stage 10 report

```json
{
  "summary": [
    "可能出现来源追问",
    "可能出现概念偷换质疑",
    "可能出现标题传播力与准确性冲突"
  ]
}
```

> 脱敏的公开版摘要，不包含角色身份或私密动机细节。

---

### 35. `07-report/01-攻击路径分析.md` through `07-report/07-综合客观评估.md` ⭐ 分章节报告

**创建者:** Stage 10 per-section agents (7 parallel agents)
**消费者:** merge agent → final report → 用户

每个章节由独立 agent 写入，只读取相关源文件：

| 文件 | 数据来源 |
|------|---------|
| `01-攻击路径分析.md` | replay analysis → attacker_profiles |
| `02-被曲解风险.md` | replay analysis → misrepresentation_targets + CLAIM_GATE |
| `03-受害方识别.md` | replay analysis → collateral_victims + interest_damage_map |
| `04-利益损害地图.md` | replay analysis → interest_damage_map + self_interest_vs_stated_position |
| `05-情境预案矩阵.md` | replay analysis → contingency_matrix + section 01 |
| `06-建议修改.md` | replay analysis → modification_priority + source content + CLAIM_GATE |
| `07-综合客观评估.md` | replay analysis → balanced_assessment + all panel verdicts |

---

### 36. `07-report/final-report.md`

**创建者:** Stage 10 merge agent
**消费者:** 用户

合并版本：TOC + 全部 7 个章节完整内容（不缩写）。

---

### 37. `最终报告.md` (case root)

**创建者:** Stage 10 merge agent
**消费者:** 用户 ⭐ 最终交付物

位于 case 根目录。包含：
- 整体总结段落（3-5 句话，给出总体判断）
- 目录
- 全部 7 个章节完整内容

---

### 38. `07-report/final-report.json`

**创建者:** Stage 10 merge agent
**消费者:** 用户

```json
{
  "decision": "HUMAN_REVIEW_REQUIRED | SAFE_TO_PUBLISH | DO_NOT_PUBLISH",
  "summary": "3-5 sentence overall assessment",
  "risk_assessment": {
    "publication_risks": [],
    "content_strengths": [],
    "net_verdict": "honest summary of real-world risk"
  },
  "section_refs": [
    { "section_id": "01", "title": "攻击路径分析", "filename": "07-report/01-攻击路径分析.md" },
    { "section_id": "02", "title": "被曲解风险", "filename": "07-report/02-被曲解风险.md" }
  ]
}
```

---

### 37. `audit/case-audit.json`

**创建者:** `audit_case.py`
**消费者:** 用户

```json
{
  "status": "PASS",
  "errors": [],
  "warnings": [],
  "role_count": 6,
  "appearance_count": 10,
  "panel_count": 2,
  "public_turn_count": 40
}
```

---

## 数据流方向速查

```
用户输入
  → Stage 1: source-content.md + content-parse.v001.json
  → Stage 2: claim-gate-packet.v001.json
  → Stage 3: role-card.json × N + pool-commit.json
  → Stage 4: issue-seeds.v001.json + intensity-plan.v001.json
  → Stage 5: panel-manifest.json + assignment.json × M
  → Stage 6-7: 每轮每角色 × (think + say + filing + fidelity) → transcript.public.jsonl
  → Stage 8: verdict-packet.json + verdict.json
  → Stage 9: full-replay-analysis.json（含攻击者画像/被曲解/受害方/利益地图/预案矩阵）
  → Stage 10: 7 section files (07-report/01~07-*.md) → merged final-report.md + 最终报告.md + final-report.json
  → audit_case.py: case-audit.json
```
