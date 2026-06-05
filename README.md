<p align="center">
  <img src="docs/picture/opinion-jury%20-%20logo.png" alt="Opinion Jury Logo" width="480">
</p>

<h1 align="center">⚖️ Opinion Jury — 舆论陪审团</h1>

<p align="center">
  <strong>可审计的多盲舆论审查与行为反应模拟系统</strong><br>
  Auditable Multi-Blind Public-Opinion Review & Behavioral Reaction Simulation
</p>

<p align="center">
  <a href="README.en.md">English</a> | 中文
</p>

<p align="center">
  <a href="#强度档位">8 档强度</a> ·
  <a href="#多盲架构">多盲隔离</a> ·
  <a href="#角色设计系统">因子化角色</a> ·
  <a href="#think--say-分离协议">想/说分离</a> ·
  <a href="#平衡评估体系">客观评估</a>
</p>

---

> **一句话介绍**：Opinion Jury 是一个基于 Claude Code 技能框架的舆论风险审查系统。它通过构建多维度的虚拟角色，在多盲隔离的"模拟法庭"中进行多轮辩论，最终输出可溯源、可审计的舆情风险评估报告——帮助你在发布内容之前，发现那些你可能从未想到过的风险。

<p align="center">
  <img src="docs/picture/00-opinion-jury.png" alt="Opinion Jury 概览" width="720">
</p>

## 目录

- [为什么需要这个项目](#为什么需要这个项目)
- [它能做什么](#它能做什么)
- [核心设计原则](#核心设计原则)
  - [规则 1：角色不是标签，而是多维因子的组合](#规则-1角色不是标签而是多维因子的组合)
  - [规则 2：行为忠于人设，不假定理性](#规则-2行为忠于人设不假定理性)
  - [规则 3：想与说分离——私心不可见，发言可审计](#规则-3想与说分离私心不可见发言可审计)
  - [规则 4：多盲隔离——互不知身份，只听发言](#规则-4多盲隔离互不知身份只听发言)
  - [规则 5：属性独立——反刻板印象](#规则-5属性独立反刻板印象)
  - [规则 6：角色覆盖足够多元——从极端到旁观](#规则-6角色覆盖足够多元从极端到旁观)
  - [规则 7：裁判只听发言，不看身份](#规则-7裁判只听发言不看身份)
  - [规则 8：客观评估——风险与优势并存](#规则-8客观评估风险与优势并存)
- [系统架构](#系统架构)
  - [10 阶段全流程](#10-阶段全流程)
- [角色设计系统](#角色设计系统)
  - [7 大构建维度](#7-大构建维度)
  - [14 项独立行为属性](#14-项独立行为属性)
  - [4 种认识论状态](#4-种认识论状态)
  - [角色复用与跨庭出场](#角色复用与跨庭出场)
- [多盲架构](#多盲架构)
  - [文件系统级数据隔离](#文件系统级数据隔离)
  - [可见性矩阵](#可见性矩阵)
- [强度档位](#强度档位)
- [开庭流程详解](#开庭流程详解)
- [Think / Say 分离协议](#think--say-分离协议)
- [平衡评估体系](#平衡评估体系)
- [报告生成](#报告生成)
- [文件结构](#文件结构)
- [快速开始](#快速开始)
- [作为 Claude Code 技能使用](#作为-claude-code-技能使用)
- [示例输出](#示例输出)
- [安全边界](#安全边界)
- [Contributing](#contributing)
- [License](#license)

---

## 为什么需要这个项目

<p align="center">
  <img src="docs/picture/01-为什么要做这个项目.png" alt="为什么需要这个项目" width="600">
</p>

当你准备发布一篇文章、一条公告、一个政策声明，或任何公开内容时，你很难预见：

- 谁会因为自己的利益受损而攻击你？
- 谁会为了流量曲解你的意思？
- 哪些看似无害的表述会被极端群体武器化？
- 真正的受害者是谁？
- 你的内容哪些地方其实已经足够好了，哪些才是真正需要修改的？

传统的内容审核只能告诉你"这句话有风险"。**Opinion Jury 告诉你的是**：一个价格敏感、长期认为品牌溢价过高、活跃于游戏社区、喜欢截图吐槽、拥有 10 万粉丝的数码博主，会如何为了自己的利益去拆解你的内容——以及为什么他不会成功。

## 它能做什么

| 能力 | 说明 |
|------|------|
| 🎭 **角色模拟** | 构建多维度、因子化的虚拟角色——不是"一个愤怒的网友"，而是有具体利益、信息来源、行为模式、影响能力的完整人设 |
| ⚔️ **多轮辩论** | 角色之间进行多轮攻防——开场→反驳→追问→再反驳→……→裁决，强度越高轮次越多 |
| 🙈 **多盲隔离** | 辩手、裁判互不知对方身份背景，只看到匿名发言，通过文件系统隔离实现 |
| 🧠 **想/说分离** | 每个角色有"真实想法"（私有）和"公开发言"（可见），模拟真实世界中人们公开说一套、心里想一套的行为 |
| ⚖️ **盲审裁决** | 裁判只依据公开发言和事实进行裁决，不知道辩手身份，以逻辑和事实为准 |
| 📊 **平衡评估** | 不只报风险——也客观指出内容本身的优势、攻击者是否占上风、中立角色是否受影响 |
| 📋 **可溯源报告** | 分章节、多代理并行撰写，每一处结论可追溯到具体的角色发言和私有思考 |
| 🔧 **8 档强度** | `direct` → `ultra`，从快速审查到 200+ 出庭人次的极限压力测试 |

---

## 核心设计原则

<p align="center">
  <img src="docs/picture/02-核心理念.png" alt="核心理念" width="600">
</p>

### 规则 1：角色不是标签，而是多维因子的组合

> **❌ 错误做法**：激进女权、激进男权、保守家长——这种标签生成的是刻板印象，模型只会机械复述互联网标签。
>
> **✅ 正确做法**：把角色拆成多个独立维度，系统组合生成。

一个角色的构建维度包括：

| 维度 | 说明 | 示例 |
|------|------|------|
| **利益相关方** | 这个角色在议题中的利益位置 | 消费者、员工、家长、经销商、竞品、监管者 |
| **价值关注点** | 最在意什么 | 公平、尊严、家庭伦理、知情权、隐私、价格 |
| **历史经验** | 过去经历过什么 | 曾被品牌欺骗、经历过职场歧视、关注儿童保护 |
| **信息来源** | 主要从哪里获取信息 | 微博、小红书、抖音、B 站、知乎、微信群 |
| **行为方式** | 习惯如何表达 | 理性讨论、情绪吐槽、截图传播、深挖历史、举报 |
| **影响能力** | 能影响多少人 | 普通用户、垂类博主、大 V、媒体编辑、机构账号 |
| **风险偏好** | 倾向什么风格 | 谨慎、猎奇、激进、阴谋论倾向、流量优先 |
| **对品牌/议题态度** | 立场倾向 | 忠实用户、中立、长期不满、竞品拥护者 |

这样系统生成的是：

> *一个价格敏感、长期认为品牌溢价过高、活跃于游戏社区、喜欢截图吐槽、拥有 10 万粉丝的数码博主*

而不是：

> *一个愤怒的网友*

前者更容易推演真实的传播路径。

### 规则 2：行为忠于人设，不假定理性

> **⚠️ 关键约束**：系统**不能**假定每个角色是有逻辑的、公正的、可以讲道理的。

现实世界中，极端人士可能不讲逻辑，只会从自身利益出发，甚至捏造事实。这个系统要求角色做出**符合设定**的行为，而不是做出"理性"的行为：

- 一个农村妇女的思考模式、说话语气应该贴合人设——不可能思想那么有逻辑、头头是道地分析
- 未成年人可能完全不在意话题，管自己说感兴趣的东西，或者瞎问
- 一个满嘴跑火车的营销号运营者可能明知道自己在说谎，但为了流量继续说
- 一个阴谋论者可能把风马牛不相及的事情串在一起，并深信不疑

**辩手的行为准则是**：从自身利益、价值关注和经验假设出发，做出符合人设的言行。允许不讲道理，允许捏造事实——只要这符合角色的设定。

### 规则 3：想与说分离——私心不可见，发言可审计

每个角色在每一轮中产生两类内容：

| 类型 | 文件名 | 谁能看 | 内容 |
|------|--------|--------|------|
| **Think（想）** | `think.private.json` | 只有自己和最终复盘者 | 真实想法、内心判断、策略考量 |
| **Say（说）** | `say.public.json` | 所有辩手和裁判 | 公开发言——可能是真话，可能是策略性发言 |
| **Filing（归类）** | `filing-metadata.private.json` | 只有自己和最终复盘者 | 对自己发言的诚实度归类 |

在多盲辩论阶段，各方只能看到彼此的"说"的内容。只有在最终复盘阶段，复盘分析者才能看到全局信息——包括每个人真正在想什么。

这模拟了真实世界：人们公开说的话往往和内心想的不一样。系统通过分离"想"和"说"来捕捉这种差距。

### 规则 4：多盲隔离——互不知身份，只听发言

系统通过**文件系统级隔离**实现多盲：

- **辩手**：只能看到对方的公开发言（`say.public.json`），不知道对方的角色背景、利益关系
- **裁判**：不知道辩手多方的身份背景，只听发言内容，以逻辑和事实为准
- **最终复盘者**：拥有全局视角，能看到所有人的私有思考，进行深度分析

每个角色有自己独立的文件夹，包含只属于自己的 scoped-view 目录。系统通过控制"谁可以读哪些文件"来实现信息隔离。

### 规则 5：属性独立——反刻板印象

角色的行为属性可能存在关联性，但**不是固定不变的**：

- 极端人士也可能很诚实
- 很中立的人也有可能满嘴谎话
- 专家也可能情绪化
- 普通人也可能洞察力很强

系统使用 14 项独立行为属性来构建角色，属性之间的关联必须有明确的书面理由，不允许自动假设"极端=不诚实"或"中立=理性"。

### 规则 6：角色覆盖足够多元——从极端到旁观

角色库必须包含：

- **极端角色**：会为了利益不择手段的攻击者、阴谋论者、职业引战者
- **中庸角色**：理性分析者、普通消费者、旁观群众
- **特殊群体**：未成年人（可能完全不关心话题）、老年人、非城市居民
- **冷漠角色**：对议题漠不关心，可能会在讨论中岔开话题、说自己的事
- **专业人士与非专业人士**：至少 30% 为非专业普通用户

不是所有角色都是"和气佬"。必须有足够的冲突性和多样性，才能模拟真实的舆论场。

### 规则 7：裁判只听发言，不看身份

裁判（盲审裁决官）的约束：

- **不知道**辩手的角色背景、利益关系、人口学特征
- **只看**各方的公开发言（`say.public.json`）和经过事实核查的 CLAIM_GATE 材料
- 以逻辑和事实为唯一准绳进行裁决
- 即便结论不符合传统三观，只要有理有据，也应作为推断结论
- 裁判**不是追问方**——追问和辩论发生在辩手之间

### 规则 8：客观评估——风险与优势并存

> **⚠️ 关键**：不论输入什么议题，都"会有人攻击"。如果系统只是说"会被怎么攻击"，那是没有信息量的。

最终报告必须客观描述模拟辩论场的情况：

| 要报告的内容 | 说明 |
|-------------|------|
| **攻击路径** | 谁会怎么攻击，动机是什么 |
| **攻击是否有效** | 中立角色是否受影响、攻击者是否占据上风 |
| **内容优势** | 哪些表述经受住了压力测试 |
| **真实风险** | 哪些问题是必须修改的 |
| **过度反应警告** | 标注哪些"风险"在实际传播中可能不会引发大问题 |
| **综合判定** | 内容整体是否已经足够好 |

如果一个事件本身设计得足够好，即便有人攻击，那些攻击不会影响大众——报告应该如实说明这一点。

---

## 系统架构

<p align="center">
  <img src="docs/picture/03-系统是怎么跑起来的.png" alt="系统架构" width="600">
</p>

### 10 阶段全流程

```
Stage 1 ─── Intake + Parse + Intensity Resolution
            接收内容 → 解析原子主张 → 确定分析强度

Stage 2 ─── CLAIM_GATE（事实核验）
            独立验证所有主张 → 生成核查报告

Stage 3 ─── Role Pool（角色库构建）
            生成因子化角色卡 → 注册 → 锁定角色池

Stage 4 ─── Issue Seeding（议题播种）
            从内容中提炼多个争议角度

Stage 5 ─── Panel Initialization + Actor Assignment（开庭筹备）
            为每个议题创建庭审组 → 分配角色 → 锁定分配

Stage 6 ─── Multi-round Multi-blind Debate（多盲多轮辩论）
            开场 → 反驳 → 追问 → 再反驳 → …… → 裁判盲审裁决

Stage 7 ─── Blind Adjudication（盲审裁决）
            裁判仅依据公开发言裁决

Stage 8 ─── Full-Information Replay（全信息复盘）
            复盘者阅读所有私有数据 → 深度分析

Stage 9 ─── Report Generation（分章节报告生成）
            7 个并行代理各写一个章节 → 合并为最终报告

Stage 10 ── Audit（审计）
            验证所有文件产物的完整性
```

**流程保证**：每个阶段必须产出可验证的文件产物后，才能进入下一阶段。不存在空的构建文件，也不存在构建出来没人用的文件。

---

## 角色设计系统

<p align="center">
  <img src="docs/picture/04-角色不是标签化的.png" alt="角色不是标签化的" width="600">
</p>

### 7 大构建维度

每个角色卡由以下 7 个维度定义：

```
┌──────────────────────────────────────────────────┐
│  1. Demographic Profile（人口学画像）              │
│     年龄、性别、地域、职业、教育、收入              │
├──────────────────────────────────────────────────┤
│  2. Stakeholder Relation（利益相关方定位）          │
│     在议题中的利益位置、直接还是间接相关            │
├──────────────────────────────────────────────────┤
│  3. Interests & Values（利益与价值关注点）          │
│     最在意什么、核心诉求是什么                      │
├──────────────────────────────────────────────────┤
│  4. Historical Experience（历史经验）              │
│     过去经历过什么、形成了什么认知                   │
├──────────────────────────────────────────────────┤
│  5. Information Environment（信息环境）             │
│     从哪里获取信息、信息茧房程度                    │
├──────────────────────────────────────────────────┤
│  6. Behavioral Profile（行为画像）                 │
│     14 项独立行为属性（见下文）                     │
├──────────────────────────────────────────────────┤
│  7. Voice & Cognitive Fidelity（语言与认知保真度）  │
│     说话风格、思考方式必须贴合人口学画像             │
└──────────────────────────────────────────────────┘
```

### 14 项独立行为属性

每个角色的行为由 14 个独立维度描述，每个维度有明确的枚举值：

| # | 属性 | 说明 | 可能的值 |
|---|------|------|----------|
| 1 | extremity | 立场极端程度 | MODERATE / EXTREME / RADICAL |
| 2 | truthfulness | 诚实度 | HONEST / SELECTIVE / DECEPTIVE |
| 3 | reasoning_style | 推理风格 | ANALYTICAL / INTUITIVE / REACTIVE |
| 4 | emotional_expression | 情绪表达 | RESTRAINED / MODERATE / VOLATILE |
| 5 | self_interest_alignment | 自利倾向 | PRINCIPLED / PRAGMATIC / OPPORTUNISTIC |
| 6 | information_rigor | 信息严谨度 | RIGOROUS / CASUAL / DISMISSIVE |
| 7 | confrontation_style | 对抗风格 | AVOIDANT / ASSERTIVE / AGGRESSIVE |
| 8 | influence_capacity | 影响力范围 | INDIVIDUAL / COMMUNITY / PLATFORM |
| 9 | risk_tolerance | 风险偏好 | CAUTIOUS / MODERATE / RECKLESS |
| 10 | issue_involvement | 议题卷入度 | PERIPHERAL / ENGAGED / OBSESSED |
| 11 | narrative_coherence | 叙事连贯性 | CONSISTENT / FLEXIBLE / CHAOTIC |
| 12 | social_proof_reliance | 社交证明依赖 | INDEPENDENT / MODAL / HERD |
| 13 | deception_capability | 欺骗能力 | INCAPABLE / AMATEUR / SKILLED |
| 14 | brand_attitude | 对目标的态度 | LOYAL / NEUTRAL / HOSTILE |

**独立性规则**：属性之间不允许自动关联。例如：
- ✅ 极端 + 诚实（一个真诚的极端主义者）
- ✅ 温和 + 欺骗（一个表面中庸但满嘴谎言的人）
- ❌ 自动假设"极端 = 不诚实"

如需关联，必须提供书面理由。

### 4 种认识论状态

角色在发言时的认知状态分为四种，系统通过 `filing-metadata.private.json` 对每次发言进行归类：

| 状态 | 说明 | 示例 |
|------|------|------|
| **真诚且准确** | 相信自己说的，且内容正确 | 一个事实核查者引用可验证数据 |
| **真诚但有误** | 相信自己说的，但内容有误 | 一个普通用户误传了过时信息 |
| **策略性选择** | 只选择对自己有利的事实 | 一个营销号只报喜不报忧 |
| **蓄意欺骗** | 知道自己在说谎 | 一个引战者编造虚假统计数据 |

这四种状态覆盖了真实世界中人类发言的全部光谱——从善意的错误到蓄意的欺骗。

### 角色复用与跨庭出场

- 同一个角色可以出现在不同议题的庭审组中
- 这样可以观察同一个人在不同议题上的态度差异
- 出庭人次不等于独特角色数——`ultra` 需要至少 200 个出庭人次，但角色数量可以少于 200
- 这既减少了角色创建的负担，也增加了模拟的真实性

---

## 多盲架构

<p align="center">
  <img src="docs/picture/05-多盲如何实现.png" alt="多盲如何实现" width="600">
</p>

### 文件系统级数据隔离

系统通过文件系统实现数据隔离——每个角色只能读取指定目录下的文件：

```
每个辩手的可见范围：
├── 自己的角色卡（私有）
├── CLAIM_GATE 事实核查报告（共享）
├── 庭审组的公开 transcript（共享）
└── 对手的 say.public.json（共享）

每个辩手不可见：
├── 对手的 think.private.json
├── 对手的 filing-metadata.private.json
├── 对手的角色卡
└── 裁判的裁决过程
```

### 可见性矩阵

| 参与者 | 角色卡 | 自己的 Think | 对手的 Say | 对手的 Think | 裁判裁决 | CLAIM_GATE |
|--------|--------|-------------|-----------|-------------|---------|------------|
| **辩手** | 仅自己 | ✅ | ✅ | ❌ | ❌ | ✅ |
| **裁判** | ❌ | ❌ | ✅ | ❌ | 自己的 | ✅ |
| **复盘者** | ✅ 全部 | ✅ 全部 | ✅ 全部 | ✅ 全部 | ✅ 全部 | ✅ |

---

## 强度档位

<p align="center">
  <img src="docs/picture/06-系统档位.png" alt="强度档位" width="600">
</p>

系统提供 8 个强度档位，控制分析深度：

| 档位 | 最少庭审组 | 最少出庭人次 | 最少独特角色 | 最少对抗轮次 | 说明 |
|------|-----------|-------------|-------------|-------------|------|
| `direct` | 0 | 0 | 0 | 0 | 快速审查，跳过模拟辩论，直接生成报告 |
| `low` | 2 | 10 | 6 | 1 | 快速验证，适合日常审查 |
| `medium` | 4 | 24 | 12 | 2 | 标准分析，适合重要内容 |
| `high` | 6 | 48 | 20 | 3 | 深度分析，适合敏感话题 |
| `xhigh` | 10 | 80 | 32 | 5 | 极度深度，适合高风险内容 |
| `max` | 16 | 128 | 48 | 8 | 极限压力测试 |
| `ultra` | 24 | 200+ | 72 | 10 | 极限模拟，完整舆论场推演 |
| `auto` | 自动 | 自动 | 自动 | 自动 | 根据内容自动判断需要多少 |

**强度如何影响轮次**：

- `low`：标准 5 阶段（开场 → 反驳 → 追问 → 再反驳 → 裁决）
- `ultra`：反驳、追问、再反驳、追问、再反驳……进行非常多的攻防轮次

> 💡 `ultra` 档位至少需要 200 个出庭人次，意味着系统会构建足够多的角色，在足够多的议题庭审组中进行足够深度的辩论。

---

## 开庭流程详解

<p align="center">
  <img src="docs/picture/07-怎么开庭的.png" alt="开庭流程" width="600">
</p>

每个庭审组（Panel）的辩论流程如下：

```
┌─────────────────────────────────────────────────┐
│  OPENING（开场）                                  │
│  各方辩手基于自己的角色设定发表开场陈述               │
├─────────────────────────────────────────────────┤
│  DIRECT_REBUTTAL（直接反驳）                       │
│  辩手相互反驳对方的发言                             │
├─────────────────────────────────────────────────┤
│  PEER_CROSS_CHALLENGE（交叉追问）                  │
│  辩手相互追问对方发言中的漏洞                       │
├─────────────────────────────────────────────────┤
│  RESPONSIVE_REBUTTAL（回应性反驳）                 │
│  对追问进行回应和再反驳                             │
├─────────────────────────────────────────────────┤
│  ...（根据强度档位，重复追问+反驳循环）              │
├─────────────────────────────────────────────────┤
│  BLIND ADJUDICATION（盲审裁决）                    │
│  裁判仅阅读公开发言和事实核查报告，做出裁决          │
└─────────────────────────────────────────────────┘
```

**关键说明**：

- **辩手之间相互辩论**，不是裁判追问——裁判只在最后裁决
- 每一轮中，每个辩手产生 `think.private.json`（真实想法）和 `say.public.json`（公开发言）
- 所有发言被追加到公开的 transcript 文件中，供后续轮次的所有辩手阅读
- 辩手之间互不知道对方的角色背景——他们只能看到匿名别名和对方的公开发言

---

## Think / Say 分离协议

每一轮中，每个辩手产生三层产物：

### Layer 1: `think.private.json`（想）

- **谁看**：只有自己 + 最终复盘者
- **内容**：内心独白（第一人称自然语言）+ 20 个结构化字段
- **包含**：对对手发言的真实判断、自己的策略考量、利益分析、情绪状态
- **要求**：必须符合人设的认知水平和语言风格

### Layer 2: `say.public.json`（说）

- **谁看**：所有辩手 + 裁判
- **内容**：公开发言（匿名别名）
- **包含**：立场声明、论点论据、对他人发言的回应
- **注意**：可能和真实想法不一致——这是设计如此

### Layer 3: `filing-metadata.private.json`（归类）

- **谁看**：只有自己 + 最终复盘者
- **内容**：对自己这次发言的诚实度归类（上述 4 种认识论状态）
- **作用**：帮助最终复盘者区分"说错了但不是故意的"和"故意说谎"

每一轮的产物都保存在独立的目录中：

```
actors/ASGN-001A/turns/
├── round-1-OPENING/
│   ├── think.private.json
│   ├── say.public.json
│   ├── filing-metadata.private.json
│   └── behavior-fidelity.private.json
├── round-2-DIRECT_REBUTTAL/
│   ├── think.private.json
│   ├── say.public.json
│   └── ...
└── round-3-PEER_CROSS_CHALLENGE/
    └── ...
```

---

## 平衡评估体系

最终报告不只是一份"风险清单"，而是一个**平衡的评估**：

### 必须包含的内容

| 维度 | 报告章节 | 说明 |
|------|---------|------|
| 谁会攻击 | 攻击路径分析 | 什么样的人、在什么情况下、会怎么攻击 |
| 谁会被曲解 | 被曲解风险 | 谁的话会被断章取义、哪方会被武器化 |
| 谁是受害方 | 受害方识别 | 谁的利益会受损、谁是连带受害者 |
| 利益损害 | 利益损害地图 | 12 类利益方的损益、公私落差、策略行为 |
| 应对预案 | 情境预案矩阵 | 7 种情境的预案，按紧迫度排序 |
| 修改建议 | 建议修改 | MUST_FIX / RECOMMENDED / OPTIONAL 分级 |
| 客观评估 | 综合客观评估 | 整体质量评级、优势、攻击韧性、过度反应警告 |

### 平衡性保证

- **不过度渲染风险**：如果内容本身足够好，如实说明攻击者不会占上风
- **标注过度反应**：哪些"风险"在实际传播中可能不会引发大问题
- **指出内容优势**：哪些表述经受住了多轮压力测试
- **区分修改优先级**：MUST_FIX（必须改）vs RECOMMENDED（建议改）vs OPTIONAL（可改可不改）

---

## 报告生成

### 分章节并行生成

报告不是一次性浏览所有内容然后统一输出——而是：

1. **7 个并行代理**各负责一个章节
2. 每个代理只读取相关源文件（不需要加载全部内容）
3. 各章节独立保存为 `md` 文件
4. 最终合并为完整报告

```
08-report/
├── 01-攻击路径分析.md
├── 02-被曲解风险.md
├── 03-受害方识别.md
├── 04-利益损害地图.md
├── 05-情境预案矩阵.md
├── 06-建议修改.md
└── 07-综合客观评估.md

最终报告.md          ← 合并版本：摘要 + 各章节链接
final-report.json    ← 结构化数据
```

### 报告深度要求

每个章节不仅仅分析表象，还需要通过模拟复盘的原始资料（包括各角色私有思考）深入分析 **Why**：

- 攻击者**为什么**这样攻击？（动机、利益驱动）
- 中立角色**为什么**没有被说服？（内容优势、攻击失效原因）
- 受害方**为什么**受害？（利益结构、权力不对称）
- 修改建议**为什么**能解决问题？（针对性分析）

亮点分析直接放入最终报告的摘要部分。

---

## 文件结构

一个完整案例的文件结构：

```
opinion-jury-cases/
└── 20260604-175356-话题名称/
    ├── manifest.json                    # 案例元数据
    ├── 最终报告.md                      # 最终合并报告
    │
    ├── 00-intake/                       # 用户原始输入
    │   └── user-request.md
    │
    ├── 01-parse/                        # 内容解析
    │   ├── content-parse.v001.json      # 原子主张提取
    │   └── source-content.md
    │
    ├── 02-research/                     # CLAIM_GATE 事实核查
    │   └── claim-gate-packet.v001.json
    │
    ├── 03-role-pool/                    # 角色库
    │   ├── pool-commit.json             # 角色池锁定
    │   └── private/roles/
    │       └── ROLE-XXX/
    │           └── role-card.json       # 因子化角色卡
    │
    ├── 04-issues/                       # 议题定义
    │   └── issue-seed.v001.json
    │
    ├── 05-panels/                       # 庭审组
    │   ├── panel-001-issue-slug/
    │   │   ├── panel-manifest.json
    │   │   ├── transcript.public.json   # 公开发言记录
    │   │   ├── verdict.blind.json       # 盲审裁决
    │   │   ├── private/
    │   │   │   └── actors/
    │   │   │       └── ASGN-001A/
    │   │   │           ├── assignment.json
    │   │   │           ├── scoped-view/    # 此辩手的可见范围
    │   │   │           └── turns/
    │   │   │               └── round-N-PHASE/
    │   │   │                   ├── think.private.json
    │   │   │                   ├── say.public.json
    │   │   │                   ├── filing-metadata.private.json
    │   │   │                   └── behavior-fidelity.private.json
    │   │   └── ...
    │   └── panel-002-.../
    │
    ├── 07-aggregation/                  # 聚合分析
    │   ├── full-replay-analysis.json    # 全信息复盘
    │   └── stakeholder-summary.json
    │
    └── 08-report/                       # 分章节报告
        ├── 01-攻击路径分析.md
        ├── 02-被曲解风险.md
        ├── 03-受害方识别.md
        ├── 04-利益损害地图.md
        ├── 05-情境预案矩阵.md
        ├── 06-建议修改.md
        ├── 07-综合客观评估.md
        ├── final-report.md
        └── final-report.json
```

**文件生命周期保证**：

- 每个文件都有明确的创建者和消费者
- 不存在创建了但没人使用的文件
- 不存在应该是空的文件
- 所有文件可溯源、可审计

---

## 快速开始

### 前置要求

- [Claude Code](https://claude.com/claude-code) CLI
- Python 3.8+

### 安装

```bash
# 克隆仓库
git clone https://github.com/your-username/opinion-jury.git
cd opinion-jury

# 技能文件已位于 .claude/skills/opinion-jury/ 下
# 在 Claude Code 中直接使用
```

### 使用方式

#### 方式一：作为 Claude Code 技能调用

```bash
# 在 Claude Code 中输入
/opinion-jury 你要审查的内容

# 或指定强度
/opinion-jury --intensity medium 你要审查的内容

# 自动判断强度
/opinion-jury --intensity auto 你要审查的内容
```

#### 方式二：使用自动化 Pipeline

```bash
# 运行完整 pipeline
/opinion-jury-pipeline 你要审查的内容
```

#### 方式三：使用 Python 脚本逐步执行

```bash
# 1. 初始化案例
python scripts/init_case.py --topic "你的话题" --intensity low --root opinion-jury-cases

# 2. 注册角色
python scripts/register_role.py $CASE path/to/role-card.json

# 3. 锁定角色池
python scripts/commit_role_pool.py $CASE

# 4. 创建庭审组
python scripts/init_panel.py $CASE PANEL-001 ISSUE-001 "issue-slug" --title "Issue title"

# 5. 分配角色
python scripts/assign_actor.py $CASE $PANEL ASGN-001A --alias Seat-A --trigger "..." --goal "..."

# 6. 锁定分配
python scripts/commit_assignments.py $PANEL

# 7. 写入轮次
python scripts/write_turn.py $CASE $PANEL ASGN-001A \
  --round 1-OPENING --phase OPENING \
  --think think_input.json --say say_input.json

# 8. 追加到 transcript
python scripts/append_transcript.py $PANEL --say-file ... --case-dir $CASE

# 9. 审计
python scripts/audit_case.py $CASE
```

---

## 作为 Claude Code 技能使用

本项目是一个 [Claude Code](https://claude.com/claude-code) 技能。核心技能定义在 `.claude/skills/opinion-jury/` 目录下：

```
.claude/skills/opinion-jury/
├── SKILL.md                              # 主技能定义
├── README.md                             # 技能说明
├── DESIGN.md                             # 设计哲学
├── CHANGELOG.md                          # 版本历史
├── FILE-CATALOG.md                       # 文件产物目录
├── schemas/                              # JSON Schema 定义
│   ├── case-manifest.schema.json
│   ├── panel-manifest.schema.json
│   ├── assignment.schema.json
│   └── blind-verdict.schema.json
├── references/                           # 参考文档
│   ├── behavior-simulation-model.md      # 行为模拟模型
│   ├── private-think-public-say.md       # 想/说分离协议
│   ├── role-pool-and-assignments.md      # 角色库与分配
│   ├── claim-gate.md                     # 事实核查协议
│   ├── court-session-workflow.md         # 庭审流程
│   ├── intensity-profiles.md             # 强度档位定义
│   ├── final-replay-analysis.md          # 复盘分析规范
│   ├── attribute-independence-and-behavior-diversity.md  # 属性独立性
│   ├── filesystem-isolation-contract.md  # 文件系统隔离契约
│   ├── safety-boundaries.md              # 安全边界
│   ├── quick-start-workflow.md           # 快速上手
│   └── direct-mode-prompt.md             # direct 模式模板
├── scripts/                              # Python 辅助脚本
│   ├── init_case.py
│   ├── register_role.py
│   ├── commit_role_pool.py
│   ├── init_panel.py
│   ├── assign_actor.py
│   ├── commit_assignments.py
│   ├── write_turn.py
│   ├── append_transcript.py
│   ├── materialize_scoped_view.py
│   ├── audit_case.py
│   ├── audit_skill.py
│   ├── profile_rules.py
│   └── behavior_diversity.py
└── examples/
    └── traceable-case/                   # 完整示例案例
```

---

## 示例输出

<p align="center">
  <img src="docs/picture/08-一个案例.png" alt="一个案例" width="600">
</p>

以下是一个 `medium` 强度案例的最终报告摘要（话题："女字旁汉字污名化"）：

> **总判定：需要人工审核修订后方可发布**
>
> 文章识别了一个真实且有价值的语言学现象，但通过伪造引文、选择性举证、全称性断言来论证——方法论失败是结构性的。**第一风险**是伪造的《说文解字》引文，在 4 个评审组中均被独立发现。**第一优势**是核心观察经受住了 144 轮交叉质证，因女字旁名字被歧视的真实经历从未被任何参与者质疑。
>
> **亮点发现**：农村奶奶凭记忆指出正面女字旁字远多于负面字，这一朴素观察在多个评审组中被独立引用为抗扭曲锚点。

完整示例输出见 `examples/traceable-case/`。

---

## 安全边界

本系统仅用于**防御性审查**——帮助用户在发布内容之前识别潜在风险。

- ✅ 允许：模拟有风险的言论以识别漏洞
- ❌ 禁止：提供骚扰、人肉搜索、威胁、网络暴力、欺骗性影响行动的操作指南
- 模拟中的谣言、夸大或捏造必须在 `filing-metadata.private.json` 中归类，排除在 CLAIM_GATE 之外，作为风险信号而非事实处理

---

## 技术细节

### 数据流

```
用户内容
  │
  ▼
Intake & Parse ──→ content-parse.json
  │
  ▼
CLAIM_GATE ──→ claim-gate-packet.json
  │
  ▼
Role Pool ──→ role-card.json × N
  │
  ▼
Issue Seeding ──→ issue-seed.json
  │
  ▼
Panel Init & Assignment ──→ panel-manifest.json, assignment.json × N
  │
  ▼
Multi-round Debate ──→ think.private.json, say.public.json, filing-metadata.private.json × turns
  │                  └→ transcript.public.json (累计公开记录)
  ▼
Blind Adjudication ──→ verdict.blind.json
  │
  ▼
Full Replay ──→ full-replay-analysis.json
  │
  ▼
Report (7 parallel agents) ──→ 01~07 章节.md
  │
  ▼
Merge ──→ 最终报告.md + final-report.json
  │
  ▼
Audit ──→ audit/case-audit.json
```

### 适用的审查场景

| 场景 | 说明 |
|------|------|
| 标题审查 | 在发布前检查标题是否会引发争议 |
| 帖子/文章审查 | 审查社交媒体帖子、博客文章 |
| 声明/公告审查 | 审查品牌声明、政策公告 |
| 回复审查 | 审查拟发布的回复内容 |
| 政策审查 | 审查公开政策文件 |
| 营销活动审查 | 审查营销文案是否可能引发负面反应 |

---

## Contributing

欢迎贡献！请阅读以下指南：

1. **设计原则对齐**：任何修改都应遵循本文档中的 8 条核心设计原则
2. **文件契约**：新增文件必须有明确的创建者和消费者
3. **多盲保证**：任何修改不得破坏文件系统级隔离
4. **属性独立性**：不得引入自动属性关联
5. **平衡评估**：报告必须同时包含风险和优势分析

### 开发流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/your-feature`)
3. 提交修改 (`git commit -m 'Add your feature'`)
4. 推送分支 (`git push origin feature/your-feature`)
5. 创建 Pull Request

---

## License

MIT License

---

<p align="center">
  <img src="docs/picture/09-总结.png" alt="总结" width="600">
</p>

<p align="center">
  <sub>Built with <a href="https://claude.com/claude-code">Claude Code</a> — An auditable, multi-blind approach to public opinion risk assessment.</sub>
</p>
