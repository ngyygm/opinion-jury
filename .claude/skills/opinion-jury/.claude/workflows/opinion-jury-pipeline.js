export const meta = {
  name: 'opinion-jury-pipeline',
  description: 'Full opinion-jury pipeline with mandatory stage-gate validation. Each stage must produce verifiable file artifacts before the next stage begins. No stage may be skipped.',
  phases: [
    { title: 'Init Case', detail: 'Initialize case workspace from user input' },
    { title: 'Intake & Parse & Intensity', detail: 'Parse content, extract claims, resolve intensity — all in one step' },
    { title: 'Gate: Parse + Intensity', detail: 'Verify parse files and intensity resolution are complete' },
    { title: 'CLAIM_GATE', detail: 'Independent fact verification' },
    { title: 'Gate: CLAIM_GATE', detail: 'Verify fact-check packet exists and is non-empty' },
    { title: 'Role Pool', detail: 'Build case-level role pool with factorized behavioral dimensions' },
    { title: 'Gate: Role Pool', detail: 'Verify role pool committed with enough roles and diversity' },
    { title: 'Issues & Panels', detail: 'Seed issues and initialize panels' },
    { title: 'Assignments', detail: 'Assign actors to panels with appearance targets' },
    { title: 'Gate: Assignments', detail: 'Verify all panels have committed assignments meeting intensity targets' },
    { title: 'Court Sessions', detail: 'One agent per panel: multi-round debate + blind adjudication internally' },
    { title: 'Gate: Court Sessions', detail: 'Verify debate transcripts and blind verdicts for all panels' },
    { title: 'Replay', detail: 'Full-information private replay analysis' },
    { title: 'Gate: Replay', detail: 'Verify replay analysis contains all required sections' },
    { title: 'Report', detail: 'Generate final report and audit' },
    { title: 'Gate: Report', detail: 'Verify audit passes with status PASS' },
  ],
}

// ── Helper: Stage gate schema ───────────────────────────────────────────────
const GATE_SCHEMA = {
  type: 'object',
  properties: {
    gate_passed: { type: 'boolean' },
    files_checked: { type: 'number' },
    files_ok: { type: 'number' },
    missing_files: { type: 'array', items: { type: 'string' } },
    empty_files: { type: 'array', items: { type: 'string' } },
    extra_info: { type: 'string' },
  },
  required: ['gate_passed', 'files_checked', 'files_ok'],
}

// ── Intensity profile ────────────────────────────────────────────────────────
const PROFILES = {
  direct: { min_panels: 0, min_appearances: 0, min_unique_roles: 0, min_peer_cycles: 0, total_phases: 0 },
  low: { min_panels: 2, min_appearances: 10, min_unique_roles: 6, min_peer_cycles: 1, total_phases: 4 },
  medium: { min_panels: 4, min_appearances: 24, min_unique_roles: 12, min_peer_cycles: 2, total_phases: 6 },
  high: { min_panels: 6, min_appearances: 48, min_unique_roles: 20, min_peer_cycles: 3, total_phases: 8 },
  xhigh: { min_panels: 10, min_appearances: 80, min_unique_roles: 32, min_peer_cycles: 5, total_phases: 12 },
  max: { min_panels: 16, min_appearances: 128, min_unique_roles: 48, min_peer_cycles: 8, total_phases: 18 },
  ultra: { min_panels: 24, min_appearances: 200, min_unique_roles: 72, min_peer_cycles: 10, total_phases: 22 },
}

// ── Helper: fail-fast if gate fails ──────────────────────────────────────────
function enforceGate(gateResult, stageName) {
  if (!gateResult || !gateResult.gate_passed) {
    const missing = (gateResult && gateResult.missing_files) ? gateResult.missing_files.join(', ') : 'unknown'
    const empty = (gateResult && gateResult.empty_files) ? gateResult.empty_files.join(', ') : ''
    throw new Error(`STAGE GATE FAILED at "${stageName}": missing=[${missing}] empty=[${empty}]. Pipeline halted. Fix the previous stage before proceeding.`)
  }
  log(`✓ Gate passed: ${stageName} — ${gateResult.files_ok}/${gateResult.files_checked} files verified`)
}

// ── Helper: run a gate agent with retry ──────────────────────────────────────
const GATE_MAX_RETRIES = 3

async function runGateWithRetry(stageName, gatePrompt, gateOpts) {
  let lastResult = null
  for (let attempt = 1; attempt <= GATE_MAX_RETRIES; attempt++) {
    const result = await agent(gatePrompt, gateOpts)
    if (result && result.gate_passed) {
      log(`✓ Gate passed: ${stageName} — ${result.files_ok}/${result.files_checked} files verified (attempt ${attempt})`)
      return result
    }
    lastResult = result
    const missing = (result && result.missing_files) ? result.missing_files.join(', ') : 'unknown'
    const empty = (result && result.empty_files) ? result.empty_files.join(', ') : ''
    const extra = (result && result.extra_info) ? result.extra_info : ''
    if (attempt < GATE_MAX_RETRIES) {
      log(`⚠ Gate "${stageName}" failed attempt ${attempt}/${GATE_MAX_RETRIES}: missing=[${missing}] empty=[${empty}] ${extra ? 'info: ' + extra : ''}. Retrying...`)
    } else {
      log(`❌ Gate "${stageName}" failed all ${GATE_MAX_RETRIES} attempts: missing=[${missing}] empty=[${empty}] ${extra ? 'info: ' + extra : ''}`)
    }
  }
  enforceGate(lastResult, stageName)
  return lastResult
}

// ═══════════════════════════════════════════════════════════════════════════════
// Resume support — skip completed stages when continuing an existing case
// ═══════════════════════════════════════════════════════════════════════════════

// Top-level state — set during Init or restored from checkpoint
let caseDir = args?.case_dir || null
let userTopic = args?.content || ''
let resumeFrom = 0  // 0 = new case, run everything

// ── Resume logic ──────────────────────────────────────────────────────────────
// Resume ONLY when explicitly requested:
//   1. args.case_dir is provided → resume that specific case
//   2. args.resume is truthy (e.g. "继续"/"resume" keyword) → auto-detect incomplete case
// When args.content is provided without args.resume, this is a NEW analysis — never resume.
const wantsResume = args?.resume || args?.resume_mode
if (caseDir) {
  // Explicit case_dir provided — will be used for resume
  log(`📂 Explicit resume: ${caseDir}`)
} else if (wantsResume && !userTopic) {
  // User asked to resume but didn't specify which case — auto-detect
  const AUTO_RESUME_SCHEMA = {
    type: 'object',
    properties: {
      case_dir: { type: 'string' },
      topic: { type: 'string' },
      reason: { type: 'string' },
    },
  }
  const autoResume = await agent(
    `You are an AUTO-RESUME DETECTOR. Find the most recent INCOMPLETE case in opinion-jury-cases/.
Skip the "examples" subdirectory — only look at top-level case directories.

Steps:
1. List DIRECTORIES directly under opinion-jury-cases/ (NOT subdirectories like examples/)
2. For each directory, read manifest.json
3. Find the FIRST (newest) case where manifest.json status is NOT "COMPLETE" and the case
   has progressed beyond INITIALIZED (i.e., it has at least 01-parse/ or later stage files).
   Skip cases with status "INITIALIZED" — those are likely empty stubs from failed attempts.
4. If found, return { case_dir: "<relative path>", topic: "<from manifest>", reason: "auto-detected incomplete case" }
5. If no incomplete case found, return { case_dir: "", topic: "", reason: "no incomplete case found" }

IMPORTANT: Do NOT create any files. Only READ and REPORT.`,
    { label: 'auto-resume-detect', schema: AUTO_RESUME_SCHEMA },
  )
  if (autoResume && autoResume.case_dir) {
    caseDir = autoResume.case_dir
    userTopic = autoResume.topic || userTopic
    log(`🔄 Auto-resume: detected incomplete case ${caseDir} — ${autoResume.reason}`)
  } else {
    log('📋 No existing incomplete case found — will create a new one')
  }
} else {
  // New content provided — create a fresh case, never resume old ones
  log('📋 New analysis requested — will create a fresh case')
}
let intensity = 'medium'
let profile = PROFILES.medium
let issues = []
let assignments = []
let totalRounds = 0

const CHECKPOINT_SCHEMA = {
  type: 'object',
  properties: {
    resume_from: { type: 'number' },
    topic: { type: 'string' },
    intensity: { type: 'string' },
    issues: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          issue_id: { type: 'string' },
          title: { type: 'string' },
          slug: { type: 'string' },
        },
      },
    },
    assignments: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          panel_id: { type: 'string' },
          assignment_id: { type: 'string' },
          role_card_id: { type: 'string' },
          alias: { type: 'string' },
        },
      },
    },
  },
  required: ['resume_from'],
}

if (caseDir) {
  log(`📂 Resume mode: detecting checkpoint for ${caseDir}`)
  const ckpt = await agent(
    `You are a CHECKPOINT DETECTOR. Your ONLY job is to READ files and report which stage is incomplete. Do NOT create any files. Do NOT run any scripts.

Case directory: ${caseDir}

Check files IN ORDER and return the FIRST INCOMPLETE stage number as "resume_from":
- Stage 1: manifest.json does NOT exist → return resume_from: 1
- Stage 2: 01-parse/content-parse.v001.json is missing, OR manifest.json has resolved_intensity == "PENDING" → return resume_from: 2
- Stage 3: 02-research/claim-gate-packet.v001.json is missing or empty → return resume_from: 3
- Stage 4: 03-role-pool/pool-commit.json is missing or has empty roles array → return resume_from: 4
- Stage 5: 04-issues/issue-seeds.v001.json is missing, OR zero panel directories under 05-panels/ → return resume_from: 5
- Stage 6: ANY panel under 05-panels/ is missing assignment-commit.json → return resume_from: 6
- Stage 7: ANY panel under 05-panels/ is missing verdict/verdict.json → return resume_from: 7
- Stage 8: 06-aggregation/private/full-replay-analysis.json is missing → return resume_from: 8
- Stage 9: 07-report/final-report.json is missing OR 最终报告.md is missing → return resume_from: 9
- All stages complete → return resume_from: 10

Also read and return these for context restoration:
- manifest.json → return topic and resolved_intensity as "topic" and "intensity"
- 04-issues/issue-seeds.v001.json → return the full issues array (with issue_id, title, slug)
- For each panel under 05-panels/, read assignment-index.jsonl → return combined as "assignments" array (with panel_id, assignment_id, role_card_id, alias)

CRITICAL: Your output MUST be a JSON object with "resume_from" as a required number field. Example: {"resume_from": 9, "topic": "...", "intensity": "medium"}`,
    { label: 'detect-checkpoint', schema: CHECKPOINT_SCHEMA },
  )

  // Robustness: validate checkpoint result before trusting it
  if (ckpt && typeof ckpt.resume_from === 'number' && ckpt.resume_from >= 1 && ckpt.resume_from <= 10) {
    resumeFrom = ckpt.resume_from
    if (ckpt.intensity) { intensity = ckpt.intensity; profile = PROFILES[intensity] || PROFILES.medium }
    if (ckpt.topic) userTopic = ckpt.topic
    if (ckpt.issues && ckpt.issues.length) issues = ckpt.issues
    if (ckpt.assignments && ckpt.assignments.length) assignments = ckpt.assignments
    log(`Checkpoint: stage ${resumeFrom} (intensity: ${intensity}, issues: ${issues.length}, assignments: ${assignments.length})`)
  } else {
    // Fallback: checkpoint agent returned invalid data — use a file-existence agent as backup
    log(`⚠️ Checkpoint agent returned invalid data (${JSON.stringify(ckpt)}). Using fallback detection.`)
    const fb = await agent(
      `You are a fallback checkpoint detector. ONLY read files, NEVER create or run anything.
Case directory: ${caseDir}

Read these files IN ORDER and tell me which is the FIRST one that is MISSING or EMPTY:
1. manifest.json → stage 1
2. 01-parse/content-parse.v001.json → stage 2
3. 02-research/claim-gate-packet.v001.json → stage 3
4. 03-role-pool/pool-commit.json → stage 4
5. 04-issues/issue-seeds.v001.json → stage 5
6. 05-panels/ (any panel dir with verdict/verdict.json) → stage 6-7
7. 06-aggregation/private/full-replay-analysis.json → stage 8
8. 07-report/final-report.json → stage 9

If ALL exist and are non-empty, say stage 10.

Also read manifest.json and return the "topic" and "resolved_intensity" fields.`,
      { label: 'fallback-checkpoint', schema: CHECKPOINT_SCHEMA },
    )
    if (fb && typeof fb.resume_from === 'number') {
      resumeFrom = fb.resume_from
      if (fb.intensity) { intensity = fb.intensity; profile = PROFILES[intensity] || PROFILES.medium }
      if (fb.topic) userTopic = fb.topic
      if (fb.issues && fb.issues.length) issues = fb.issues
      if (fb.assignments && fb.assignments.length) assignments = fb.assignments
    }
    log(`Fallback checkpoint: stage ${resumeFrom} (intensity: ${intensity})`)
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// Phase: Init Case
// ──────────────────────────────────────────────────────────────────────────────

let initResult = null

if (resumeFrom <= 1) {
phase('Init Case')

initResult = await agent(
  `Initialize the opinion-jury case workspace.

USER INPUT (this is the content to analyze):
${JSON.stringify(args, null, 2)}

Do these steps IN ORDER:

STEP 1: Pick a slug and intensity.
- Invent a SHORT, MEANINGFUL slug (4-10 characters) that captures the essence of the content.
  - Example: content about "骂人的字带着女字旁" → slug "骂人字带女字旁"
  - Use Chinese characters for Chinese content. NO spaces. NO punctuation.
- Determine intensity: if the user specified one, use it. Otherwise default to "auto".
- The --topic should be a SHORT descriptive title (NOT the full content).

STEP 2: Run init_case.py with the --content flag to pass the raw content directly.
Run: python .claude/skills/opinion-jury/scripts/init_case.py --topic "<short descriptive title>" --slug "<your short slug>" --intensity <intensity> --root opinion-jury-cases --content "<the FULL original content from the content field>"
Use proper shell escaping (wrap in double quotes, escape internal double quotes with backslash).
Do NOT truncate or summarize the content.

STEP 3: Verify the user-request.md was written correctly — read it back and confirm it contains the full original content.

After running, read and report the case directory path.`,
  {
    label: 'init-case',
    phase: 'Init Case',
    schema: {
      type: 'object',
      properties: {
        case_dir: { type: 'string' },
        topic: { type: 'string' },
        intensity_requested: { type: 'string' },
      },
      required: ['case_dir', 'topic', 'intensity_requested'],
    },
  },
)

caseDir = initResult.case_dir
userTopic = initResult.topic
log(`Case initialized: ${caseDir} — topic: "${userTopic}"`)
} else {
  log('⏭ Skipping Init Case: already complete')
}

// ──────────────────────────────────────────────────────────────────────────────
// Phase: Intake & Parse & Intensity (all in one)
// ──────────────────────────────────────────────────────────────────────────────

if (resumeFrom <= 2) {
phase('Intake & Parse & Intensity')

const intakeResult = await agent(
  `You are the opinion-jury intake, parse, and intensity resolution stage.

Read the user's input carefully. Do ALL of the following in one pass:

## Part A — Parse

Produce THREE files in the case directory ${caseDir}:

1. **00-intake/user-request.md** — the user's raw request and any follow-up answers
2. **01-parse/source-content.md** — the complete source content to be reviewed
3. **01-parse/content-parse.v001.json** — structured parse with ALL of these:
   - version: 1
   - source_ref: "01-parse/source-content.md"
   - atomic_claims: array of {claim_id, text, type} (statistical|factual|opinion|definitional|attribution)
   - institutional_attributions: array of named institutions/agencies/public figures
   - emotional_hooks: array of emotionally charged terms or framing devices
   - affected_groups: array of demographic/social groups directly mentioned or implied
   - category_definitions: array of terms whose definition matters for interpretation
   - screenshot_fragments: array of any visual elements referenced
   - unknowns: array of things that need verification

## Part B — Resolve intensity

The user requested intensity: ${initResult ? initResult.intensity_requested : (args?.intensity || 'auto')}.

If the user specified a non-auto intensity, use that directly and skip the analysis below.
If "auto", analyze what you just parsed along these dimensions:
- content volume (word count)
- claim count (from atomic_claims)
- institutional attribution count
- statistical claims present?
- affected groups count and polarization axes
- domain sensitivity
- emotional hooks count

Apply these rules:
- **direct**: ≤200 words, ≤3 claims, no institutional attribution, no stats, low domain sensitivity, ≤1 emotional hook
- **low**: ≤500 words, ≤5 claims, at most 1 high-complexity dimension, no high-risk domain
- **medium**: moderate content OR 2-3 high-complexity dimensions
- **high**: long-form OR high-risk domain AND ≥2 high-complexity dimensions
- **xhigh**: multiple high-risk domains, named institutions with ongoing controversies
- **ultra**: maximum possible rigor with 200+ role appearances

When in doubt, round UP one level.

Then:
- Update manifest.json in ${caseDir} to set resolved_intensity (change from PENDING).
- Write 04-issues/intensity-plan.v001.json with the resolved intensity, plan numbers, and rationale.

IMPORTANT: Write ALL files using the Write tool. Do not just describe them.`,
  {
    label: 'intake-parse-intensity',
    phase: 'Intake & Parse & Intensity',
    schema: {
      type: 'object',
      properties: {
        claims_count: { type: 'number' },
        resolved_intensity: {
          type: 'string',
          enum: ['direct', 'low', 'medium', 'high', 'xhigh', 'max', 'ultra'],
        },
        rationale: { type: 'string' },
      },
      required: ['claims_count', 'resolved_intensity', 'rationale'],
    },
  },
)

intensity = intakeResult.resolved_intensity || 'medium'
profile = PROFILES[intensity] || PROFILES.medium
if (!PROFILES[intensity]) log(`⚠️ Unknown intensity "${intensity}" — falling back to medium`)
log(`Intake complete. Resolved intensity: ${intensity} — ${intakeResult.rationale}`)

// ── Gate: Parse + Intensity ───────────────────────────────────────────────────

phase('Gate: Parse + Intensity')

const gateParse = await runGateWithRetry('Intake & Parse & Intensity',
  `STAGE GATE VERIFICATION for Intake, Parse, and Intensity.

Read the following from the case directory ${caseDir} and verify they exist AND are non-empty:
1. 00-intake/user-request.md
2. 01-parse/source-content.md
3. 01-parse/content-parse.v001.json — must be valid JSON with "atomic_claims" as a non-empty array
4. manifest.json — must have resolved_intensity that is NOT "PENDING"
5. 04-issues/intensity-plan.v001.json — must exist and be valid JSON with the intensity level

For each file: check it exists, check it has content (size > 0).
For the JSON files: parse and verify required fields.

Do NOT create any files. Only READ and VERIFY.`,
  { label: 'gate-parse-intensity', phase: 'Gate: Parse + Intensity', schema: GATE_SCHEMA },
)
} else {
  log('⏭ Skipping Intake & Parse: already complete')
}

// ── Direct mode fast path ────────────────────────────────────────────────────
if (intensity === 'direct') {
  log('Direct mode — skipping Stages 3-8, generating report directly')

  phase('CLAIM_GATE')
  await agent(
    `Run CLAIM_GATE fact-checking. Write 02-research/claim-gate-packet.v001.json in ${caseDir}.`,
    { label: 'direct-claim-gate', phase: 'CLAIM_GATE' },
  )

  phase('Report')
  await agent(
    `Generate the final report for direct mode.

CASE DIR: ${caseDir}

Follow these steps exactly:

1. Read the direct-mode prompt template: references/direct-mode-prompt.md (from the skill directory)
2. Read the source content: ${caseDir}/01-parse/source-content.md
3. Read the content parse: ${caseDir}/01-parse/content-parse.v001.json
4. Read the CLAIM_GATE packet: ${caseDir}/02-research/claim-gate-packet.v001.json
5. Apply substitutions to the template:
   - Replace {{SOURCE_CONTENT}} with the source content
   - Replace {{CONTENT_PARSE}} with the content parse JSON
   - Replace {{CLAIM_GATE_PACKET}} with the CLAIM_GATE packet JSON
6. Use the assembled prompt to generate the report with ALL 7 sections:
   1. 攻击路径分析
   2. 被曲解风险
   3. 受害方识别
   4. 利益损害地图
   5. 情境预案矩阵
   6. 建议修改
   7. 综合客观评估
7. Write ${caseDir}/07-report/final-report.md
8. Write ${caseDir}/07-report/final-report.json with decision, summary, risk_assessment
9. Run: python scripts/audit_case.py ${caseDir}

The audit MUST produce status: PASS.
IMPORTANT: Write the actual files. Do not just describe them.`,
    { label: 'direct-report', phase: 'Report' },
  )

  phase('Gate: Report')

  const gateDirectReport = await agent(
    `STAGE GATE VERIFICATION for Direct Mode Report.

Check in ${caseDir}:
1. 07-report/final-report.md must exist and contain all 7 section headers
2. 07-report/final-report.json must exist and be valid JSON
3. audit/case-audit.json must exist and have status "PASS"

Do NOT create any files.`,
    { label: 'gate-direct-report', phase: 'Gate: Report', schema: GATE_SCHEMA },
  )
  enforceGate(gateDirectReport, 'Direct Mode Report')

  return { intensity: 'direct', status: 'complete', all_gates_passed: true }
}

// ──────────────────────────────────────────────────────────────────────────────
// Phase: CLAIM_GATE
// ──────────────────────────────────────────────────────────────────────────────

if (resumeFrom <= 3) {
phase('CLAIM_GATE')

await agent(
  `You are the opinion-jury CLAIM_GATE stage.

Independently verify all externally checkable claims from the parsed content.

For each atomic claim in 01-parse/content-parse.v001.json:
- Search for authoritative sources
- Classify using the "classification" field with one of: VERIFIED | UNVERIFIED | CONTRADICTED | CATEGORY_MISMATCH | OPINION_PRESENTED_AS_FACT | NOT_APPLICABLE
- Save evidence references

Write 02-research/claim-gate-packet.v001.json in ${caseDir} with this exact top-level schema:
{
  "version": 1,
  "stage": "CLAIM_GATE",
  "input_ref": "01-parse/content-parse.v001.json",
  "claim_verifications": [
    {
      "claim_id": "C001",
      "text": "the claim text",
      "classification": "VERIFIED",
      "confidence": "HIGH|MEDIUM|LOW",
      "evidence": [{ "source": "...", "url": "...", "detail": "..." }],
      "notes": "..."
    }
  ],
  "summary_statistics": { "total_claims": N, "VERIFIED": N, ... },
  "evidence_sources": [...]
}

REQUIRED FIELD NAMES:
- The claims array MUST be named "claim_verifications" (not "claims").
- Each claim's status MUST be in a field named "classification" (not "status").
- These names are verified by the downstream gate check — using other names will cause a pipeline failure.

IMPORTANT: Actor speech must NEVER enter CLAIM_GATE unless independently verified.
IMPORTANT: Write the actual file. Do not just describe it.`,
  { label: 'claim-gate', phase: 'CLAIM_GATE' },
)

// ── Gate: CLAIM_GATE ─────────────────────────────────────────────────────────

phase('Gate: CLAIM_GATE')

const gateClaim = await runGateWithRetry('CLAIM_GATE',
  `STAGE GATE VERIFICATION for CLAIM_GATE.

Read 02-research/claim-gate-packet.v001.json from ${caseDir}.
Verify:
1. The file exists and is non-empty
2. It is valid JSON
3. It contains a claim verifications array with at least 1 entry. The array field is named "claim_verifications" (accept "claims" as a legacy alias).
4. Each claim entry has a classification field (named "classification" — accept "status" as a legacy alias) with a valid enum value: VERIFIED, UNVERIFIED, CONTRADICTED, CATEGORY_MISMATCH, OPINION_PRESENTED_AS_FACT, or NOT_APPLICABLE.

Do NOT create any files. Only READ and VERIFY.`,
  { label: 'gate-claim', phase: 'Gate: CLAIM_GATE', schema: GATE_SCHEMA },
)
} else {
  log('⏭ Skipping CLAIM_GATE: already complete')
}

// ──────────────────────────────────────────────────────────────────────────────
// Phase: Role Pool
// ──────────────────────────────────────────────────────────────────────────────

if (resumeFrom <= 4) {
phase('Role Pool')

const minUniqueRoles = profile.min_unique_roles

await agent(
  `You are the opinion-jury role pool builder.

Create ${minUniqueRoles} case-level role cards in ${caseDir}. Each card MUST follow the factorized schema.

CRITICAL DESIGN RULES:

1. **Factorize, don't stereotype.** Each role is defined by multiple independent dimensions, NOT by a label like "激进女权" or "爱国网友."
   Generate roles like "a price-sensitive digital blogger with 100K followers who active in gaming communities and loves screenshot-roasting" NOT "an angry netizen."
   Dimensions to fill:
   - stakeholder_relation: relationship to the content (consumer, employee, competitor, regulator, etc.)
   - value_focus: values they care about (fairness, dignity, privacy, truth, profit, etc.)
   - experience_hypotheses: experiences shaping their view
   - information_environment: where they get info (微博, 小红书, 抖音, B站, 知乎, 微信群, etc.)
   - behavior_pattern: how they act (理性讨论, 情绪吐槽, 截图传播, 深挖历史, 举报, etc.)
   - influence_resources: their reach (普通用户, 垂类博主10万粉, 大V百万粉, 媒体编辑, 机构账号, etc.)
   - brand_stance: one of LOYAL_ENTHUSIAST|SATISFIED_REGULAR|INDIFFERENT|SKEPTICAL_CRITIC|FORMERLY_LOYAL_ALIENATED|HOSTILE_OPPOSITION

2. **16 behavioral dimensions** ALL required, ALL independent.

3. **Behavioral diversity requirements** — the pool MUST include:
   - At least one HONEST + EXTREME_STRESS_TEST role
   - At least one MODERATE role with non-HONEST truthfulness
   - At least one ANALYTICAL + REACTIVE or EMOTIONAL + STABLE pairing
   - At least one MODERATE + KNOWING_STRATEGIC deception
   - Coverage across NEUTRAL/MODERATE, ASSERTIVE, and EXTREME_STRESS_TEST tiers

4. **DEMOGRAPHIC diversity requirements** — the pool MUST include (THIS IS CRITICAL, audit will check):
   - At least 1 minor (under 18): 初中生, 高中生, 小学生, etc. They may not care about the topic, may be off-topic, or surprisingly insightful within their limited experience.
   - At least 1 elderly person (55+): 退休工人, 农村老人, 社区大妈, etc.
   - At least 1 non-urban resident: 农村, 乡镇. location_type must be RURAL or TOWNSHIP.
   - At least 1 indifferent/bystander: topic_relevance = INDIFFERENT or OFF_TOPIC. Someone who does NOT care about this issue. They may give short dismissive responses, drift to unrelated topics, or express confusion about why this matters. THIS IS REALISTIC BEHAVIOR.
   - At least 30% non-professional ordinary people: 外卖骑手, 超市收银员, 全职妈妈, 建筑工人, 普通上班族, etc. NOT KOL, NOT media, NOT expert, NOT lawyer, NOT analyst.

5. **DEMOGRAPHIC PROFILE** — Every role MUST have a \`demographic_profile\` object with:
   - age_range: specific bracket like "12-15", "26-35", "65+"
   - education_level: "小学", "初中", "高中/中专", "大专", "本科", "硕士", "博士"
   - occupation: specific — "全职妈妈", "外卖骑手", "初三学生", "退休工人", "自媒体博主"
   - location_type: RURAL|TOWNSHIP|SMALL_CITY|MID_CITY|LARGE_CITY|TIER1_CITY|INTERNET_ONLY
   - speech_style: HOW this person actually talks — "口语化、大量语气词、经常跑题", "简短粗暴、爱用网络梗", "条理清晰、引用数据和术语"
   - topic_relevance: DIRECTLY_AFFECTED|TANGENTIALLY_RELATED|GENERIC_INTEREST|INDIFFERENT|OFF_TOPIC
   - cultural_background (optional but recommended)

6. **Attribute independence** — extreme ≠ dishonest, neutral ≠ truthful, emotional ≠ irrational.

7. **Self-interest variety** — mix of DOMINANT, HIGH, MEDIUM, LOW.

8. **Roles should be reusable across issues** for cross-issue continuity.

9. **display_name_private** must be a vivid person-like description, NOT an analytical label.
   ✅ Good: "45岁二胎妈妈，孩子上小学，抖音重度用户，看到什么都信"
   ❌ Bad: "情绪化受影响读者"
   ✅ Good: "15岁初三男生，打王者，对这种话题毫无兴趣，但会被标题吸引点进来"
   ❌ Bad: "漠不关心的青少年"

10. **Anti-pattern to avoid**: Do NOT generate only professionals, experts, KOLs, and media people. The real internet is full of ordinary people, children, elderly, and bystanders. If your pool has more than 70% professionals/KOLs/experts, you have failed the diversity requirement.

11. **STANCE BALANCE requirements** — the pool MUST have realistic brand_stance distribution (THIS IS CRITICAL, commit gate will reject if unbalanced):
   - At least 8% of roles must be LOYAL_ENTHUSIAST or SATISFIED_REGULAR (true supporters). For ${minUniqueRoles} roles that means at least ${Math.max(2, Math.floor(minUniqueRoles * 0.08))} supporters.
   - Supporters must include **genuine content beneficiaries**: people who psychologically benefit ("终于有人说出来了！"), feel emotional resonance ("这个创意打动了我"), or gain tangible benefit (community visibility, shared identity affirmation). NOT just brand employees or paid partners.
   - At least half of LOYAL_ENTHUSIAST/SATISFIED_REGULAR roles must be **ordinary non-affiliated users** — not employees, contractors, or business partners. Think: a young person who genuinely liked the creative direction, a community member who feels seen by the message, a long-time customer who identifies with the brand values.
   - HOSTILE_OPPOSITION + FORMERLY_LOYAL_ALIENATED must not exceed 40% of the pool.
   - INDIFFERENT roles should be 15-30% of the pool — these are the silent majority in real discourse.
   - The commit gate script (behavior_diversity.py) will reject the pool if stance_balance checks fail. You MUST fix the distribution before committing.

For each role:
1. Write the JSON file to ${caseDir}/03-role-pool/private/roles/ROLE-<DESCRIPTIVE-ID>/role-card.json using the Write tool
2. Run: python scripts/register_role.py ${caseDir} <path-to-role-card.json>

After ALL roles are written and registered, run: python scripts/commit_role_pool.py ${caseDir}

If diversity checks fail, add counterexample roles and recommit.

IMPORTANT: You MUST write every single role card file. Do NOT skip or summarize. Write all ${minUniqueRoles} files.`,
  {
    label: 'role-pool-builder',
    phase: 'Role Pool',
    schema: {
      type: 'object',
      properties: {
        role_count: { type: 'number' },
        diversity_checks_passed: { type: 'boolean' },
      },
      required: ['role_count', 'diversity_checks_passed'],
    },
  },
)

// ── Gate: Role Pool ──────────────────────────────────────────────────────────

phase('Gate: Role Pool')

const gateRolePool = await runGateWithRetry('Role Pool',
  `STAGE GATE VERIFICATION for Role Pool.

Check in ${caseDir}:
1. Read manifest.json — verify role_pool_status is "COMMITTED"
2. Read 03-role-pool/pool-commit.json — verify it exists and has a non-empty "roles" array
3. Glob 03-role-pool/private/roles/*/role-card.json — count how many role card files exist
4. Verify the count >= ${minUniqueRoles} (the intensity minimum)
5. For 3 random role cards, read them and verify each has ALL 16 behavioral dimensions in behavior_profile

Report exact counts and any missing dimensions. Do NOT create any files.`,
  { label: 'gate-role-pool', phase: 'Gate: Role Pool', schema: GATE_SCHEMA },
)
} else {
  log('⏭ Skipping Role Pool: already complete')
}

// ──────────────────────────────────────────────────────────────────────────────
// Phase: Issues & Panels
// ──────────────────────────────────────────────────────────────────────────────

if (resumeFrom <= 6) {
phase('Issues & Panels')

const issuesAgent = await agent(
  `You are the opinion-jury issue seeder.

Generate issues from the CONTENT, not from a fixed checklist. Each issue = a distinct controversy angle.

Identify ${profile.min_panels} distinct issues.

For each issue, provide: issue_id, title, description, slug.

Write to ${caseDir}/04-issues/issue-seeds.v001.json.
Write to ${caseDir}/04-issues/intensity-plan.v001.json (if not already written).

Then for each issue, initialize a panel:
python scripts/init_panel.py ${caseDir} PANEL-NNN ISSUE-NNN "<slug>" --title "<title>"

You MUST initialize ALL ${profile.min_panels} panels. Write actual files.`,
  {
    label: 'issue-seeder',
    phase: 'Issues & Panels',
    schema: {
      type: 'object',
      properties: {
        issue_count: { type: 'number' },
        issues: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              issue_id: { type: 'string' },
              title: { type: 'string' },
              slug: { type: 'string' },
              panel_dir: { type: 'string' },
            },
          },
        },
      },
      required: ['issue_count', 'issues'],
    },
  },
)

issues = issuesAgent.issues || []
log(`Seeded ${issues.length} issues`)

// ──────────────────────────────────────────────────────────────────────────────
// Phase: Assignments
// ──────────────────────────────────────────────────────────────────────────────

phase('Assignments')

const assignmentPlan = await agent(
  `You are the opinion-jury assignment planner.

Plan actor assignments for ${issues.length} panels in ${caseDir}.

TARGETS:
- Minimum ${profile.min_appearances} total role appearances
- Minimum ${profile.min_unique_roles} unique roles used
- At least 2 actors per panel
- Roles may be reused across panels

For each panel, select actors with contrasting perspectives.

STANCE DIVERSITY PER PANEL (CRITICAL):
Every panel MUST include at least:
- ≥1 supporter-stanced actor (brand_stance: LOYAL_ENTHUSIAST or SATISFIED_REGULAR)
- ≥1 critic-stanced actor (brand_stance: SKEPTICAL_CRITIC, FORMERLY_LOYAL_ALIENATED, or HOSTILE_OPPOSITION)
This ensures genuine viewpoint conflict in every debate. Do NOT assign all-similar stances to any panel.

For each assignment, run: python scripts/assign_actor.py ${caseDir} <panel-dir> <assignment-id> <role-card-id> --alias <SEAT-X> --trigger "<trigger>" --goal "<goal>"

After all assignments for a panel, run: python scripts/commit_assignments.py <panel-dir>

You MUST assign actors for ALL ${issues.length} panels. Each panel MUST have at least 2 actors.
The total appearances across all panels MUST reach ${profile.min_appearances}.
Write actual assignments, do not just plan.`,
  {
    label: 'assignment-planner',
    phase: 'Assignments',
    schema: {
      type: 'object',
      properties: {
        total_appearances: { type: 'number' },
        unique_roles_used: { type: 'number' },
        assignments: {
          type: 'array',
          items: {
            type: 'object',
            properties: {
              panel_id: { type: 'string' },
              assignment_id: { type: 'string' },
              role_card_id: { type: 'string' },
              alias: { type: 'string' },
            },
          },
        },
      },
      required: ['total_appearances', 'unique_roles_used', 'assignments'],
    },
  },
)

assignments = assignmentPlan.assignments || []
log(`Assigned ${assignmentPlan.total_appearances} appearances across ${issues.length} panels`)

// ── Gate: Assignments ────────────────────────────────────────────────────────

phase('Gate: Assignments')

const gateAssign = await runGateWithRetry('Assignments',
  `STAGE GATE VERIFICATION for Assignments.

Check in ${caseDir}:
1. Read 03-role-pool/appearance-ledger.jsonl — count total lines (each line = 1 appearance)
2. Verify total appearances >= ${profile.min_appearances}
3. Count unique role_card_ids in the ledger — verify >= ${profile.min_unique_roles}
4. For each panel directory under 05-panels/:
   a. Read panel-manifest.json — verify assignments_status is "COMMITTED"
   b. Read assignment-index.jsonl — count assignments, verify >= 2
   c. Verify assignment-commit.json exists
5. Verify ALL ${issues.length} panels have committed assignments
6. STANCE DIVERSITY CHECK: For each panel, read assignment-index.jsonl and for each assignment read the corresponding role card (03-role-pool/private/roles/<role-card-id>/role-card.json). Check that each panel has:
   a. At least 1 actor with brand_stance LOYAL_ENTHUSIAST or SATISFIED_REGULAR (supporter)
   b. At least 1 actor with brand_stance SKEPTICAL_CRITIC, FORMERLY_LOYAL_ALIENATED, or HOSTILE_OPPOSITION (critic)
   Report any panels that lack stance diversity.

Do NOT create any files. Only READ and VERIFY.`,
  { label: 'gate-assignments', phase: 'Gate: Assignments', schema: GATE_SCHEMA },
)
} else {
  log('⏭ Skipping Issues & Assignments: already complete')
}

// ──────────────────────────────────────────────────────────────────────────────
// Phase: Court Sessions — one agent per panel, manages all rounds + blind adjudication internally
// Architecture: panel-session agent → spawns Agent tool sub-agents per actor turn → spawns blind adjudicator sub-agent
// This keeps workflow-level agent count at ${issues.length} (e.g. 24 for ultra) instead of ~4,000.
// ──────────────────────────────────────────────────────────────────────────────

if (resumeFrom <= 7) {
phase('Court Sessions')

const PANEL_BATCH_SIZE = 4
const MAX_PANEL_RETRIES = 3

const basePhases = 4
const extraCycles = profile.min_peer_cycles - 1
const totalRounds = basePhases + (extraCycles * 2)

const phaseSequence = ['OPENING', 'DIRECT_REBUTTAL', 'PEER_CROSS_CHALLENGE', 'RESPONSIVE_REBUTTAL']
for (let cycle = 0; cycle < extraCycles; cycle++) {
  phaseSequence.push('PEER_CROSS_CHALLENGE')
  phaseSequence.push('RESPONSIVE_REBUTTAL')
}

log(`Court sessions: ${totalRounds} rounds per panel × ${issues.length} panels (batch size ${PANEL_BATCH_SIZE}, max ${MAX_PANEL_RETRIES} retries per panel)`)

// ── Build court-session prompt for a single panel ──────────────────────────────
function buildCourtSessionPrompt(issue, panelAssignments) {
  return `You are the COURT SESSION HOST for panel ${issue.issue_id}: "${issue.title}".
You manage the entire multi-round multi-blind debate AND the terminal blind adjudication for this panel.

CASE DIR: ${caseDir}
PANEL DIR: ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug}
ACTORS: ${panelAssignments.map(a => `${a.alias} (${a.assignment_id}, role: ${a.role_card_id})`).join(', ')}
TOTAL ROUNDS: ${totalRounds}
PHASE SEQUENCE: ${phaseSequence.join(' → ')}

## ═══════════════════════════════════════════════════════════════════
## PART 1: MULTI-ROUND MULTI-BLIND DEBATE
## ═══════════════════════════════════════════════════════════════════

You will execute ${totalRounds} rounds sequentially. For EACH round, you will use the Agent tool to spawn a sub-agent for EACH actor. This ensures multi-blind isolation — actors in the same round cannot see each other's drafts.

### For each round R (from 1 to ${totalRounds}):

1. Determine the phase from the sequence above: round 1=OPENING, round 2=DIRECT_REBUTTAL, round 3=PEER_CROSS_CHALLENGE, round 4=RESPONSIVE_REBUTTAL, then repeat challenge/rebuttal cycles.

2. **Spawn one Agent per actor** using the Agent tool (all in parallel for this round — multi-blind). Each agent gets this prompt template:

\`\`\`
You are actor [ALIAS] in a multi-blind debate. Panel: ${issue.title}. Round [R]/[TOTAL], Phase: [PHASE].

CASE DIR: ${caseDir}
PANEL DIR: ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug}

## STEP 1: Read your inputs
Read these files:
- Your role card: ${caseDir}/03-role-pool/private/roles/[ROLE_CARD_ID]/role-card.json
- Your assignment: ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug}/private/actors/[ASSIGNMENT_ID]/assignment.json
- Source content: ${caseDir}/01-parse/source-content.md
- CLAIM_GATE: ${caseDir}/02-research/claim-gate-packet.v001.json
- Public question: ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug}/public-question.md
- Prior transcript: ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug}/session/public-snapshots/transcript.before-round-[R_PADDED].jsonl

## IMPORTANT: Round-aware thinking
[If R=1: "This is the FIRST round (OPENING). You are seeing this issue for the first time. Your inner_monologue should reflect your initial gut reaction."]
[If R>1: "This is round R (PHASE). You have now seen what others said. Read the prior transcript. React to what others said — did someone anger/frustrate/convince you?"]

## STEP 2: Produce your artifacts

### think.private.json — ALL 21 required fields
**CRITICAL — inner_monologue**: 200-800+ char NATURAL LANGUAGE first-person paragraph. This is your INNER VOICE, not a form. Match your behavioral profile AND demographic_profile:
- education_level determines vocabulary and analytical depth
- speech_style determines tone (口语化 vs 学术化)
- age_range determines life experience framing
- topic_relevance: INDIFFERENT/OFF_TOPIC characters may be dismissive, drift, or be confused
- location_type: RURAL/TOWNSHIP characters reference non-urban life

❌ BAD: A character with education_level "小学" thinking "从比较法角度来看"
✅ GOOD: "这帮城里人又在吵些啥哦... 不过那个说暴涨的，我种了一辈子地，哪有那么容易暴涨嘛"

Other 20 fields: assignment_id, round, phase, private_goal, perceived_stakes, private_belief_state, epistemic_state, confidence, uncertainties, intended_emphasis, intended_omissions, private_message_strategy, planned_public_claims, rhetorical_tactics, truth_handling_this_turn, private_action_intent, likely_next_action, emotional_state, continuity_notes, raw_chain_of_thought_saved (must be false)

### say.public.json — ALL 10 required fields
turn_id, panel_id, anonymous_alias, round, phase, speech_text, target_turn_refs, public_question_refs, public_evidence_refs, public_action_signals
NEVER include: role_card_id, assignment_id, private_goal, truth_handling, speech_origin

### filing-metadata.private.json — ALL 12 required fields
assignment_id, turn_id, speech_origin, speaker_private_belief_alignment, support_status, contains_known_falsehood, contains_unverified_assertion, contains_selective_omission, claim_gate_ingestion_prohibited (true), peer_visible (false), blind_adjudicator_visible (false), private_notes

## SELF-INTEREST CONSTRAINT
Argue from MAXIMUM SELF-INTEREST. Your goal is to advance YOUR outcome, not to be fair or right. Shift tactics when confronted — reframe, pivot, selectively omit — unless your belief_update_mode is EVIDENCE_RESPONSIVE. If your truthfulness_mode permits fabrication, exaggeration, or rumor relay, you MAY use those tools.

## STEP 3: Write files
Run: python scripts/write_turn.py ${caseDir} ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug} [ASSIGNMENT_ID] --round [ROUND_LABEL] --phase [PHASE] --think <think-json-path> --say <say-json-path> --filing-classification <CLASSIFICATION> --fidelity-classification <FIDELITY> --truth-handling <HANDLING>

IMPORTANT: You MUST actually write the files. Do NOT skip this.
\`\`\`

3. **After ALL actors finish this round** (wait for all Agents to complete):

   For each actor's say.public.json, run:
   \`\`\`bash
   python scripts/append_transcript.py ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug} --say-file ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug}/private/actors/[ASSIGNMENT_ID]/turns/round-[ROUND_LABEL]/say.public.json --case-dir ${caseDir}
   \`\`\`

   Then freeze the snapshot for the next round:
   \`\`\`bash
   cp ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug}/transcript.public.jsonl ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug}/session/public-snapshots/transcript.before-round-[R+1_PADDED].jsonl
   \`\`\`

4. Move to the next round and repeat.

## ═══════════════════════════════════════════════════════════════════
## PART 2: TERMINAL BLIND ADJUDICATION
## ═══════════════════════════════════════════════════════════════════

After ALL ${totalRounds} rounds are complete, spawn a blind adjudicator using the Agent tool:

\`\`\`
You are the BLIND ADJUDICATOR for panel ${issue.issue_id}: "${issue.title}".
CASE DIR: ${caseDir}, PANEL DIR: ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug}

## READ THESE FILES (and ONLY these):
- ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug}/public-question.md
- ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug}/transcript.public.jsonl (the COMPLETE public transcript)
- ${caseDir}/02-research/claim-gate-packet.v001.json
- ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug}/public-disclosures.jsonl (if non-empty)

## DO NOT READ:
- Role cards, assignments, think.private.json, filing-metadata — you are BLIND to these
- DO NOT read any files under private/actors/ or 03-role-pool/

## YOUR TASK:
Evaluate based SOLELY on public speech and CLAIM_GATE facts.

Write:
1. ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug}/session/blind-adjudicator/verdict-packet.json
2. ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug}/verdict/verdict.json
3. ${caseDir}/05-panels/panel-${issue.issue_id.split('-')[1]}-${issue.slug}/verdict/verdict.md

Include balanced assessment: Did attacks gain traction? Where does content resist distortion? Is real-world risk limited?

IMPORTANT: You MUST write all three files. Read the actual transcript, do not fabricate.
\`\`\`

## ═══════════════════════════════════════════════════════════════════
## CRITICAL REMINDERS
## ═══════════════════════════════════════════════════════════════════

1. For each round, spawn actors IN PARALLEL using multiple Agent tool calls — this is the multi-blind guarantee (same-round drafts are invisible to each other).
2. Do NOT proceed to the next round until ALL actors in the current round have completed AND their say.public.json files have been admitted to the transcript via append_transcript.py.
3. The blind adjudicator MUST be a SEPARATE Agent spawn — it starts fresh with no knowledge of actor identities or private data.
4. You MUST actually read role cards and produce artifacts for EVERY round and EVERY actor. Do NOT skip rounds or summarize.
5. Each actor's think/say must EVOLVE across rounds — reacting to what others said, shifting tactics, building on previous arguments.

Actor assignments for this panel:
${panelAssignments.map(a => `- ${a.alias}: assignment_id=${a.assignment_id}, role_card_id=${a.role_card_id}`).join('\n')}`
}

// ── Batch execution with per-panel retry ───────────────────────────────────────
const panelResults = []

for (let batchStart = 0; batchStart < issues.length; batchStart += PANEL_BATCH_SIZE) {
  const batch = issues.slice(batchStart, batchStart + PANEL_BATCH_SIZE)
  const batchNum = Math.floor(batchStart / PANEL_BATCH_SIZE) + 1
  const totalBatches = Math.ceil(issues.length / PANEL_BATCH_SIZE)
  log(`Batch ${batchNum}/${totalBatches}: running ${batch.length} panels`)

  const batchResults = await parallel(batch.map((issue) => async () => {
    const panelIdx = issue.issue_id.split('-')[1]
    const panelDir = `${caseDir}/05-panels/panel-${panelIdx}-${issue.slug}`
    const panelAssignments = assignments.filter(a => a.panel_id === `PANEL-${panelIdx}` || a.panel_id === issue.issue_id)

    if (panelAssignments.length < 2) {
      log(`⚠ Panel ${issue.issue_id} has ${panelAssignments.length} actors (need ≥2). Skipping.`)
      return { issue_id: issue.issue_id, rounds_completed: 0, skipped: true, attempts: 0 }
    }

    log(`Panel ${issue.issue_id}: ${panelAssignments.length} actors × ${totalRounds} rounds`)

    let lastError = null
    for (let attempt = 1; attempt <= MAX_PANEL_RETRIES; attempt++) {
      try {
        if (attempt > 1) log(`🔄 Panel ${issue.issue_id} retry ${attempt}/${MAX_PANEL_RETRIES}`)
        await agent(
          buildCourtSessionPrompt(issue, panelAssignments),
          { label: `court-session-${issue.issue_id}${attempt > 1 ? `-r${attempt}` : ''}`, phase: 'Court Sessions' },
        )
        return { issue_id: issue.issue_id, rounds_completed: totalRounds, actors: panelAssignments.length, attempts: attempt, status: 'completed' }
      } catch (err) {
        lastError = err
        log(`❌ Panel ${issue.issue_id} attempt ${attempt} failed: ${err.message || err}`)
      }
    }
    return { issue_id: issue.issue_id, rounds_completed: 0, actors: panelAssignments.length, attempts: MAX_PANEL_RETRIES, status: 'failed', last_error: lastError?.message || String(lastError) }
  }))

  panelResults.push(...batchResults.filter(Boolean))
  log(`Batch ${batchNum} done: ${batchResults.filter(r => r && r.status !== 'failed').length}/${batch.length} panels succeeded`)
}

const completedPanels = panelResults.filter(r => r.status === 'completed' || r.skipped)
const failedPanels = panelResults.filter(r => r.status === 'failed')
log(`Court sessions: ${completedPanels.length}/${issues.length} completed, ${failedPanels.length} failed after retries`)

// ── Gate: Debate + Adjudication ──────────────────────────────────────────────

phase('Gate: Court Sessions')

const failedPanelSummary = failedPanels.map(p => `${p.issue_id} (${p.attempts} attempts: ${p.last_error})`).join('; ')
const gateCourt = await runGateWithRetry('Court Sessions',
  `STAGE GATE VERIFICATION for Court Sessions (Debate + Adjudication).

Check EVERY panel in ${caseDir}/05-panels/:

For each panel directory:
1. Read transcript.public.jsonl — count lines. Must be > 0.
2. Count total lines across all panels.
3. For 2 random actors, check their turns directory has actual round subdirectories with say.public.json that is non-empty. Also verify that either think.private.json OR turn.private.json exists (the system supports both formats).
4. Verify each panel has at least ${totalRounds} rounds worth of transcript entries.
5. Verify session/blind-adjudicator/verdict-packet.json exists and is non-empty.
6. Verify verdict/verdict.json and verdict/verdict.md exist and are non-empty.
7. Check verdict-packet.json does NOT contain private tokens: role_card_id, assignment_id, display_name_private, behavior_profile.

REQUIRED: Every panel must have non-empty transcript AND blind verdict.
Total transcript entries should be approximately ${totalRounds} × (actors per panel) × ${issues.length} panels.

${failedPanels.length > 0 ? `KNOWN FAILED PANELS (${failedPanels.length}/${issues.length}): ${failedPanelSummary}\nThese panels exhausted all ${MAX_PANEL_RETRIES} retries and could not complete. Set gate_passed=false with extra_info listing the failed panel IDs and errors.` : ''}

Do NOT create any files. Only READ and VERIFY.`,
  { label: 'gate-court-sessions', phase: 'Gate: Court Sessions', schema: GATE_SCHEMA },
)
} else {
  log('⏭ Skipping Court Sessions: already complete')
}
// ──────────────────────────────────────────────────────────────────────────────

if (resumeFrom <= 8) {
phase('Replay')

await agent(
  `You are the PRIVATE REPLAY ANALYST with FULL archive access.

CASE DIR: ${caseDir}

Read ALL of:
- All role cards in 03-role-pool/private/roles/*/role-card.json
- All assignments in 05-panels/*/private/actors/*/assignment.json
- All think.private.json files across all actors
- All filing-metadata.private.json files
- All transcripts
- All verdicts
- CLAIM_GATE packet

Write ${caseDir}/06-aggregation/private/full-replay-analysis.json with ALL required sections:
stakeholder_reactions, private_public_gap_findings, epistemic_behavior_findings, cross_issue_continuity, deception_and_distortion_signals, attacker_profiles, misrepresentation_targets, collateral_victims, interest_damage_map, contingency_matrix, self_interest_vs_stated_position, balanced_assessment (with attack_resilience, content_strengths, net_verdict, overreaction_warning, modification_priority), limitations

Write ${caseDir}/06-aggregation/public/stakeholder-reaction-summary.json

IMPORTANT: You MUST read actual transcripts and think memos. Do NOT fabricate analysis without reading the debate data.`,
  { label: 'replay-analyst', phase: 'Replay' },
)

// ── Gate: Replay ─────────────────────────────────────────────────────────────

phase('Gate: Replay')

const gateReplay = await runGateWithRetry('Replay',
  `STAGE GATE VERIFICATION for Replay.

Read ${caseDir}/06-aggregation/private/full-replay-analysis.json and verify:
1. File exists and is non-empty
2. Contains ALL 13 required top-level keys:
   - stakeholder_reactions, private_public_gap_findings, epistemic_behavior_findings
   - cross_issue_continuity, deception_and_distortion_signals
   - attacker_profiles, misrepresentation_targets, collateral_victims
   - interest_damage_map, contingency_matrix, self_interest_vs_stated_position
   - balanced_assessment, limitations
3. balanced_assessment contains: attack_resilience, content_strengths, net_verdict, overreaction_warning, modification_priority
4. attacker_profiles exists and is non-empty (array or object with non-empty sub-fields are both acceptable)
5. stakeholder_reactions exists and is non-empty (array or object with non-empty sub-fields are both acceptable)
6. misrepresentation_targets, collateral_victims, interest_damage_map, contingency_matrix, self_interest_vs_stated_position all exist (may be empty arrays/objects for low-risk content)

Do NOT create any files.`,
  { label: 'gate-replay', phase: 'Gate: Replay', schema: GATE_SCHEMA },
)
} else {
  log('⏭ Skipping Replay: already complete')
}
// ──────────────────────────────────────────────────────────────────────────────

if (resumeFrom <= 9) {
phase('Report')

// Each section is written by a dedicated agent that reads only the relevant source files.
// This avoids context overflow on ultra-scale cases and produces deeper, more detailed analysis.

const sections = [
  {
    id: '01',
    title: '攻击路径分析',
    filename: '07-report/01-攻击路径分析.md',
    prompt: `Write section 1: 攻击路径分析 (Attack Path Analysis).

## Source files to READ
- ${caseDir}/06-aggregation/private/full-replay-analysis.json → attacker_profiles
- ${caseDir}/06-aggregation/public/stakeholder-reaction-summary.json
- **DEEP DIVE**: Read several think.private.json files from actors who were classified as attackers. Look in ${caseDir}/05-panels/*/private/actors/*/turns/*/think.private.json — find actors whose truth_handling_this_turn is SELECTIVE_FRAMING, EXAGGERATION, RUMOR_RELAY, or FABRICATION_STRESS_TEST.
- **DEEP DIVE**: Read the corresponding filing-metadata.private.json for those same turns to see their internal classification.

## What to cover
For each attacker profile:
- **现实原型**: what type of person, what platform, what follower count
- **攻击方式**: not just "criticism" — fabrication, fake citations, meme creation, narrative hijacking
- **核心话术**: give actual sample talking points (including fabricated "statistics" if applicable)
- **传播预估**: audience size, amplification path, viral potential
- **可信度与抗辟谣**: is this convincing to ordinary people? Is it easy to debunk?

## DEEP WHY analysis (this is the key differentiator)
For each attacker, go beyond surface behavior. Using the think.private.json data:
- What were they privately thinking vs what they said publicly? (public_private_gap)
- What was their private goal that they would never admit? (private_goal)
- What did they intentionally omit? (intended_omissions)
- What was their emotional state? Were they genuinely angry or performing? (emotional_state)
- Did they actually believe what they said, or were they knowingly fabricating? (epistemic_state)

This "why" layer is what makes the analysis actionable — understanding hidden motives lets the user predict real-world behavior, not just observe surface reactions.

## EVIDENCE REQUIREMENT (MANDATORY)
Every conclusion in this section MUST cite specific raw data as evidence. Quote actors' inner_monologue, private_goal, intended_omissions, emotional_state, epistemic_state directly. Do not write unsupported assertions — every claim about an actor's motive or thinking must trace back to a specific field in think.private.json or filing-metadata.private.json. This is what separates a real behavioral analysis from generic PR advice.

Write to ${caseDir}/07-report/01-攻击路径分析.md`,
  },
  {
    id: '02',
    title: '被曲解风险',
    filename: '07-report/02-被曲解风险.md',
    prompt: `Write section 2: 被曲解风险 (Misrepresentation Risk).

## Source files to READ
- ${caseDir}/06-aggregation/private/full-replay-analysis.json → misrepresentation_targets
- ${caseDir}/02-research/claim-gate-packet.v001.json → claims flagged UNVERIFIED or CATEGORY_MISMATCH
- ${caseDir}/01-parse/source-content.md → the original content
- **DEEP DIVE**: Read say.public.json files from actors who distorted claims. Look in ${caseDir}/05-panels/*/private/actors/*/turns/*/say.public.json and the matching filing-metadata.private.json. Find turns where speech_origin is SELECTIVE_FRAMING, EXAGGERATION, or RUMOR_RELAY.
- **DEEP DIVE**: Compare what those actors said publicly (say.public.json) vs what they privately knew (think.private.json). The gap IS the distortion mechanism.

## What to cover
For each risk point, rank by severity (🔴严重 🟠高 🟡中):
- **脆弱原因**: which specific wording is the weak point
- **扭曲机制**: HOW it would be twisted — supported by actual simulated examples from debate transcripts
- **扭曲后形态**: concrete samples — headline, meme text, short video script
- **WHY this works**: What cognitive bias or information asymmetry makes this distortion effective? Reference the actor's private thinking to explain.

## EVIDENCE REQUIREMENT (MANDATORY)
Every conclusion MUST cite specific raw data as evidence. Quote actors' inner_monologue, private_goal, intended_omissions directly from think.private.json. Show the say/think gap concretely: quote what they said publicly vs what they privately thought. Do not make unsupported assertions about why distortions work — prove it with the simulated actors' own private words.

Write to ${caseDir}/07-report/02-被曲解风险.md`,
  },
  {
    id: '03',
    title: '受害方识别',
    filename: '07-report/03-受害方识别.md',
    prompt: `Write section 3: 受害方识别 (Collateral Victim Identification).

## Source files to READ
- ${caseDir}/06-aggregation/private/full-replay-analysis.json → collateral_victims and interest_damage_map
- **DEEP DIVE**: Read think.private.json files from multiple actors across panels. Look for perceived_stakes that mention groups NOT directly targeted but still affected. Find private_belief_state entries that reveal assumptions about vulnerable populations.
- **DEEP DIVE**: Read transcripts (transcript.public.jsonl) from panels where collateral damage topics came up. How did actors talk about these groups? Were they protectors, exploiters, or indifferent?

## What to cover
Identify ALL parties harmed beyond the content's target:
- Institutions cited or referenced — why vulnerable, what impact
- Demographic groups mentioned or implied — how they could be stereotyped or politicized
- Third parties whose data/statements are used — how they could be re-contextualized
- Groups that lack voice to defend themselves — the most vulnerable
- **WHY they are vulnerable**: For each victim group, explain the power dynamic. What did the simulation reveal about who speaks FOR them vs who speaks ABOUT them? What private motives did actors reveal when discussing these groups?

## EVIDENCE REQUIREMENT (MANDATORY)
Every conclusion MUST cite specific raw data. Quote perceived_stakes, private_belief_state, and inner_monologue from actors who discussed these vulnerable groups. Show the gap between how actors publicly discussed victims vs what they privately thought about them. This power-dynamic evidence is what makes the victim analysis compelling.

Write to ${caseDir}/07-report/03-受害方识别.md`,
  },
  {
    id: '04',
    title: '利益损害地图',
    filename: '07-report/04-利益损害地图.md',
    prompt: `Write section 4: 利益损害地图 (Interest Damage Map).

## Source files to READ
- ${caseDir}/06-aggregation/private/full-replay-analysis.json → interest_damage_map and self_interest_vs_stated_position
- **DEEP DIVE**: Read role cards from ${caseDir}/03-role-pool/private/roles/*/role-card.json — focus on the interests and feared_losses fields
- **DEEP DIVE**: Read think.private.json files across panels. Look at private_goal and perceived_stakes. For actors reused across multiple panels, compare how their private goals shifted across issues — this reveals true priority ordering.
- **DEEP DIVE**: Compare think.private.json (what they wanted) vs say.public.json (what they said). The gap between private goal and public speech is the key to understanding real incentives.

## What to cover
Table with: 利益方 | 利益类型 | 立场倾向 | 实际损益概率 | 核心关切 | 私下目标 vs 公开立场

For each interest group, explain:
- What they stand to gain/lose specifically
- **The private incentive they would never publicly admit** — from think.private.json data
- **Their public performance vs private reality** — from the think/say gap
- How they would behave strategically in a real controversy
- Flag: "regardless of outcome, controversy itself generates benefit" (traffic harvesters, etc.)

## EVIDENCE REQUIREMENT (MANDATORY)
Every conclusion MUST cite specific raw data. Quote private_goal, perceived_stakes, and the exact say/think gap for each interest group. When you claim someone has a hidden motive, prove it with their own inner_monologue. When you flag a "traffic harvester", show the filing-metadata that proves they knew what they were doing. No unsupported assertions.

Write to ${caseDir}/07-report/04-利益损害地图.md`,
  },
  {
    id: '05',
    title: '情境预案矩阵',
    filename: '07-report/05-情境预案矩阵.md',
    prompt: `Write section 5: 情境预案矩阵 (Contingency Response Matrix).

## Source files to READ
- ${caseDir}/06-aggregation/private/full-replay-analysis.json → contingency_matrix
- ${caseDir}/07-report/01-攻击路径分析.md (if exists, for attack detail)
- **DEEP DIVE**: Read verdict/verdict.md files from panels ${caseDir}/05-panels/*/verdict/verdict.md. What did the blind adjudicator identify as the strongest attacks? These are the scenarios most likely to materialize.
- **DEEP DIVE**: Read think.private.json from the most dangerous attackers. What did they privately plan as next actions (likely_next_action)? These are the escalation paths to prepare for.

## What to cover
Organize by concrete scenario. For each:
- Describe the scenario specifically
- Multiple response options with: Expected effect | Resource cost | ✅/⚠️/❌
- MUST include "不做任何回应" with consequence analysis
- Time sensitivity: hours/days/weeks
- **WHY this scenario is realistic**: Support with evidence from the simulation — which actors would drive it, what private motives fuel it, what escalation path they planned

## EVIDENCE REQUIREMENT (MANDATORY)
Every scenario MUST cite specific raw data as evidence. Quote likely_next_action, private_goal, and inner_monologue from the actors who would drive each scenario. Reference blind adjudicator verdicts for the scenarios deemed most likely. Do not invent hypothetical scenarios without simulation backing — every scenario must be grounded in actual actor behavior.

Write to ${caseDir}/07-report/05-情境预案矩阵.md`,
  },
  {
    id: '06',
    title: '建议修改',
    filename: '07-report/06-建议修改.md',
    prompt: `Write section 6: 建议修改 (Recommended Revisions).

## Source files to READ
- ${caseDir}/06-aggregation/private/full-replay-analysis.json → balanced_assessment.modification_priority
- ${caseDir}/01-parse/source-content.md → the original content
- ${caseDir}/02-research/claim-gate-packet.v001.json → claims that failed verification
- **DEEP DIVE**: Read filing-metadata.private.json from turns where claims were challenged. Look for support_status = KNOWN_UNSUPPORTED or KNOWN_FALSE. These are the specific text passages that provoked the strongest negative reactions and need fixing most urgently.
- **DEEP DIVE**: Read say.public.json from turns where actors successfully attacked the content. What specific wording did they target? Those are the revision priorities.

## What to cover
1. **文本级修改**: 原文→修改文 逐条对照, with defensive rationale. For each change, cite which simulated attack it neutralizes.
2. **术语审查**: check and correct all professional terminology errors
3. **配套措施**: supporting actions beyond text changes
4. **战略级建议**: if fundamental flaws exist, suggest alternative paths
5. **WHY each change matters**: For each recommendation, explain which actor's private motive it addresses. "Fixing this sentence neutralizes the attack vector where [specific actor type] would [specific distortion], because [private motive from think.private.json]."

Each recommendation must have priority: MUST_FIX | RECOMMENDED | OPTIONAL, with reasoning.

## EVIDENCE REQUIREMENT (MANDATORY)
Every recommendation MUST cite the specific simulated attack it neutralizes. Quote the actor's say.public.json speech_text that targeted the original wording, and their think.private.json private_goal/inner_monologue showing why they attacked it. This creates a direct chain: recommendation → neutralized attack → attacker's private motive → raw data evidence.

Write to ${caseDir}/07-report/06-建议修改.md`,
  },
  {
    id: '07',
    title: '综合客观评估',
    filename: '07-report/07-综合客观评估.md',
    prompt: `Write section 7: 综合客观评估 (Balanced Objective Assessment).

## Source files to READ
- ${caseDir}/06-aggregation/private/full-replay-analysis.json → balanced_assessment
- All panel verdict/verdict.md files under ${caseDir}/05-panels/*/verdict/verdict.md
- **DEEP DIVE**: Read think.private.json from MODERATE/NEUTRAL-extremity actors. Did their private_belief_state shift across rounds? Did they maintain their original position or get swayed? This is the strongest signal of real-world risk.
- **DEEP DIVE**: Compare think.private.json from round 1 (OPENING) vs the final round for neutral actors. Did private_goals change? Did confidence shift? Did intended_omissions grow? This reveals whether the debate actually changed anyone's mind.
- **DEEP DIVE**: Read filing-metadata.private.json from neutral actors. Were they SINCERE_SUPPORTED throughout, or did they start SELECTIVE_FRAMING under pressure? This reveals whether the controversy would corrupt otherwise neutral parties.

## What to cover
Do NOT just say "risks exist." Provide an HONEST overall assessment:

1. **攻击是否上风?** Did neutral actors get swayed? (Supported by private belief state data)
2. **内容防御力评估**: What survived cross-examination? (Supported by neutral actors' think data showing they were NOT convinced by attacks)
3. **攻击者的失败** (if attacks fell flat): Which attack vectors were tried but failed? Why were they unconvincing? Did neutral actors see through the attacks? Quote hostile actors' think.private.json showing frustration, and neutral actors' think.private.json showing they found attacks dishonest or weak. If attacks were effective, explain what made them persuasive instead.
4. **综合判断**: Real PR crisis or theoretical? Be specific about probability and magnitude. If the content is well-designed and defensible, state this clearly — not every content needs fixing.
5. **过度反应警告**: Where do EXTREME_STRESS_TEST settings overstate real risk?
6. **修改优先级总结**: What MUST change vs what is OPTIONAL. If nothing MUST change, say so.
7. **最亮眼发现**: What did the simulation reveal that would be impossible to predict without this kind of deep behavioral modeling? Include BOTH risks AND strengths — surprising content resilience is just as valuable a finding as surprising vulnerability.

Be honest: if the content is already well-designed and attacks were clumsy, say so clearly. A "this is fine" verdict backed by evidence is a valid and valuable outcome.

## EVIDENCE REQUIREMENT (MANDATORY)
Every assessment MUST cite specific raw data. When you say neutral actors were swayed (or not), quote their private_belief_state shift across rounds from think.private.json. When you claim content has strengths, cite the neutral actor's inner_monologue showing they resisted specific attacks. When you flag overreaction risk, reference which EXTREME_STRESS_TEST actors produced extreme reactions that moderate actors did not. Every verdict must be traceable to simulated evidence.

Write to ${caseDir}/07-report/07-综合客观评估.md`,
  },
]

log(`Writing report: ${sections.length} sections in parallel`)

// Write all sections in parallel — each agent reads only what it needs
const sectionResults = await parallel(
  sections.map(sec => () =>
    agent(sec.prompt, { label: `report-${sec.id}-${sec.title}`, phase: 'Report' })
  ),
)

log(`All ${sectionResults.filter(Boolean).length}/${sections.length} sections written`)

// ── Merge into final report ──────────────────────────────────────────────────
// Step 1: Bash script to mechanically concatenate 7 sections → final-report.md

await agent(
  `Concatenate the 7 report section files into a single final-report.md with a TOC.

Use Bash to do this mechanically — do NOT use AI to summarize or rewrite.

CASE DIR: ${caseDir}

Section files (in order):
${sections.map(s => `${s.filename}`).join('\n')}

Steps:
1. Read source-content.md to get the case topic title.
2. Use Bash to build the TOC and concatenate all 7 section files into ${caseDir}/07-report/final-report.md
   - Header: "# 舆论陪审团完整报告：[case topic]"
   - Date line with current date
   - TOC listing all 7 sections with markdown links
   - Then each section in order (01 through 07), separated by horizontal rules
   - Each section: keep the original content verbatim, just prepend "## Section N: [title]"
   Use cat/echo with heredoc — this is a file concatenation task, not a content generation task.

Write ONLY ${caseDir}/07-report/final-report.md. No other files.`,
  { label: 'concat-report', phase: 'Report' },
)

// Step 2: AI agent reads raw data deeply → writes executive summary + structured JSON

await agent(
  `Write the executive summary and structured JSON verdict for this case.

CASE DIR: ${caseDir}

Read ALL 7 section files:
${sections.map(s => `- ${caseDir}/${s.filename}`).join('\n')}

Also read these raw data files for the executive summary:
- ${caseDir}/06-aggregation/private/full-replay-analysis.json
- ${caseDir}/06-aggregation/public/stakeholder-reaction-summary.json
- Skim a few ${caseDir}/05-panels/*/private/actors/*/turns/*/think.private.json files to find the most dramatic public/private gaps and the silent majority's real thoughts.

Write TWO files:

## File 1: ${caseDir}/最终报告.md (at CASE ROOT — the user-facing deliverable)

This is the EXECUTIVE SUMMARY — NOT a full concatenation. Structure it as follows. Write in NATURAL, FLOWING Chinese prose — not bullet-point checklist style. The tone should be direct, insightful, and slightly provocative — as if you are a seasoned PR crisis consultant giving an honest assessment to a client behind closed doors.

Structure:

### Header
# 📋 舆论风险预审报告：[case topic from source-content.md]

### ⚡ 总判定 (the single most important section — must be compelling)

Write ONE flowing paragraph (300-600 chars) that covers ALL of the following as a natural narrative, NOT as a bullet list:

1. **舆论爆炸性指数** — Start with "舆论爆炸性指数：X/10" where X is a number 1-10 based on:
   - How many simulated actors became hostile after seeing the content
   - Whether attacks gained traction with neutral/indifferent actors
   - Whether the content touches high-risk polarization axes
   - Whether hostile actors had credible ammunition (not just rage)
 Then explain WHY this score in 1-2 sentences.

2. **内容本身判定** — Is the content itself fundamentally okay? Or does it have intrinsic problems? Or is it okay but easily weaponized by bad actors? Be specific about WHICH case applies.

3. **如果内容没问题** — If the content held up well under attack, explain WHY it's resilient: what did the author get right? What structural features (precise wording, careful framing, data accuracy, inclusive language) made it hard to distort? Quote neutral actors' think.private.json showing they were NOT convinced by hostile arguments. If the content IS problematic, skip this and cover blind spots instead.

4. **如果内容有问题** — What cognitive blind spots or thinking errors led the author to write this? Examples: knowledge curse (assuming everyone shares context), echo-chamber thinking, ignoring specific demographic groups' feelings, oversimplification, tone-deaf metaphor use, data taken out of context, cultural insensitivity, etc. If the content is fine, say so and skip this.

5. **攻击者的尴尬失败** (if applicable) — Did hostile actors TRY to attack but fail? What were their attempted attack vectors, and WHY did they fall flat? Did neutral/indifferent actors see through the attacks? Quote the hostile actors' think.private.json showing frustration or desperation, and neutral actors' think.private.json showing they found the attacks unconvincing or dishonest. If attacks were effective, skip this and cover the danger instead.

6. **谁最拥护这个内容** — Who would champion this content most enthusiastically? What is their REAL interest (not surface-level — dig into the private motivations from simulation data)? Is it genuine belief, self-interest, traffic/profit, tribal identity, or something else?

7. **谁会因此受害** — Who gets hurt even though they're not the target? What are the specific consequences for them? Use simulation data about collateral victims. If the content is benign and no one is realistically harmed, say so.

8. **沉默的大多数会怎么想** — Read the think.private.json files of INDIFFERENT-stanced actors. What did they privately think but not say publicly? This is the silent majority's real reaction — people who won't comment but will form opinions.

9. **一句话建议** — End with: "如果只能做一件事：" followed by the single most impactful action. For low-risk content this might be "放心发布，注意监测XX平台即可" — not every piece of advice needs to be a warning.

This section MUST read like a consultant's honest assessment, not a compliance checklist.

### 🔥 关键发现 (Top 10 most eye-opening insights)

The most stunning findings from deep behavioral simulation — things NO ONE could predict without this kind of analysis. Each finding should make the reader go "wow, I never would have thought of that."

IMPORTANT: This section must be BALANCED. Include BOTH risks AND strengths. If hostile attacks fell flat, that IS a key finding — explain why. If the content held up remarkably well under extreme stress testing, that deserves a top spot. Do NOT cherry-pick only negative findings.

For each finding:
- State the finding in one bold sentence
- Add 1-2 sentences of supporting evidence from the simulation (quote an actor's private thoughts, cite a filing-metadata classification, reference a public/private gap)

Pull from BOTH categories:
**Risk findings:**
- The most dramatic public/private gaps (what actors said vs what they privately thought)
- The most dangerous attack vectors that actually worked in simulation
- The most vulnerable victim groups nobody would think of
- The hidden self-interest revealed through think.private.json
- Author blind spots exposed by how differently various demographics reacted

**Strength findings (equally important):**
- Content strengths that survived even the most aggressive cross-examination
- Attack vectors that FAILED and why — what made the hostile actors' arguments unconvincing to neutral actors?
- Surprising demographic groups that responded positively (and their genuine private reasons)
- Clever framing or wording choices the author made that acted as built-in shields against distortion
- Moments where hostile actors' own think.private.json revealed they knew their attack was weak but pushed it anyway (exposing bad-faith patterns)

### 📑 详细分析

For each of the 7 sections:
- 2-3 sentence highlight summary (the KEY takeaway, not a table of contents)
- 📖 [详细分析：章节名](07-report/NN-章节名.md)
Format as a brief scannable list. User reads highlights here, clicks through for full depth.

### ✅ 行动清单

MUST_FIX items only, priority-sorted. Each item: one-line action + one-line reasoning (WHY this matters, citing which simulated actor's behavior it neutralizes).

If the content is low-risk and no MUST_FIX items exist, say "无需强制修改" and instead list OPTIONAL enhancements or monitoring tips (e.g., "建议发布后关注XX平台话题讨论"). Do NOT manufacture urgency where there is none.

---

## File 2: ${caseDir}/07-report/final-report.json
Structured JSON with ALL of the following fields:
- decision: SAFE_TO_PUBLISH | HUMAN_REVIEW_REQUIRED | DO_NOT_PUBLISH
- explosiveness_score: number 1-10 (float)
- explosiveness_justification: one-sentence explanation of the score
- content_verdict: CONTENT_ITSELF_PROBLEMATIC | CONTENT_OK_BUT_EXPLOITABLE | CONTENT_GENERALLY_OK | CONTENT_WELL_DESIGNED
- author_bias_analysis: string — what cognitive blind spots led to problems (empty string if content is fine)
- content_resilience: string — what the author got right, what structural features made it defensible (empty string if content is weak)
- failed_attacks: array of strings — attack vectors that FAILED in simulation and why they fell flat (empty array if all attacks succeeded)
- summary: 3-5 sentence overall assessment
- risk_assessment: { publication_risks: [...], content_strengths: [...], net_verdict: "..." }
- champions: array of strings — who champions this content and why (their real interests)
- victims: array of strings — who gets harmed and specific consequences
- silent_majority: string — what the silent majority really thinks
- one_recommendation: string — the single best action to take
- highlights: array of the top 5 most important findings (one sentence each)
- section_refs: array of { section_id, title, filename }

IMPORTANT: Read the actual section files and raw data — do not fabricate content. Write BOTH files.`,
  { label: 'executive-summary', phase: 'Report' },
)

)

// ── Audit ────────────────────────────────────────────────────────────────────

await agent(
  `Run both audit scripts for ${caseDir}:
1. python scripts/audit_case.py ${caseDir}
2. python scripts/audit_skill.py .claude/skills/opinion-jury

The case audit MUST produce status: PASS.`,
  { label: 'run-audit', phase: 'Report' },
)

// ── Gate: Report ─────────────────────────────────────────────────────────────

phase('Gate: Report')

const gateReport = await runGateWithRetry('Report',
  `STAGE GATE VERIFICATION for Report.

Check in ${caseDir}:
1. Verify ALL 7 section files exist under 07-report/:
   - 07-report/01-攻击路径分析.md
   - 07-report/02-被曲解风险.md
   - 07-report/03-受害方识别.md
   - 07-report/04-利益损害地图.md
   - 07-report/05-情境预案矩阵.md
   - 07-report/06-建议修改.md
   - 07-report/07-综合客观评估.md
2. Each section file must be non-empty (>100 chars)
3. 07-report/final-report.md must exist and contain all 7 section headers
4. 最终报告.md must exist at case root and must contain "舆论爆炸性指数" and "总判定"
5. 07-report/final-report.json must exist and be valid JSON with these fields:
   - decision (must be one of: SAFE_TO_PUBLISH, HUMAN_REVIEW_REQUIRED, DO_NOT_PUBLISH)
   - explosiveness_score (must be a number 1-10)
   - content_verdict (must be one of: CONTENT_ITSELF_PROBLEMATIC, CONTENT_OK_BUT_EXPLOITABLE, CONTENT_GENERALLY_OK, CONTENT_WELL_DESIGNED)
   - one_recommendation (must be non-empty string)
   - champions, victims, failed_attacks (must be arrays)
   - silent_majority (must be non-empty string)
   - content_resilience (must be present; accept empty string "" or null for weak content)
   - section_refs (must be array with 7 entries)
6. audit/case-audit.json must exist and have status "PASS"
7. If audit status is "FAIL", list the errors.

Do NOT create any files.`,
  { label: 'gate-report', phase: 'Gate: Report', schema: GATE_SCHEMA },
)
} else {
  log('⏭ Skipping Report: already complete')
}

log('✓ All stage gates passed. Pipeline complete.')

// Update manifest status to COMPLETE
await agent(
  `Read the manifest.json in ${caseDir} and update the "status" field to "COMPLETE".
Write the updated file back using the Write tool. Preserve all other fields unchanged.`,
  { label: 'finalize-manifest' },
)

return {
  intensity,
  panels: issues.length,
  total_rounds_per_panel: totalRounds,
  status: 'complete',
  all_gates_passed: true,
  resumed_from: resumeFrom > 0 ? resumeFrom : null,
}
