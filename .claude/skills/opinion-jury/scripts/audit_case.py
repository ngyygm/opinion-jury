#!/usr/bin/env python3
from pathlib import Path
import sys,json,re
from profile_rules import PROFILES
from behavior_diversity import REQ_BEHAVIOR, diversity_gaps
REQ_THINK={'inner_monologue','assignment_id','round','phase','private_goal','perceived_stakes','private_belief_state','epistemic_state','confidence','uncertainties','intended_emphasis','intended_omissions','private_message_strategy','planned_public_claims','rhetorical_tactics','truth_handling_this_turn','private_action_intent','likely_next_action','emotional_state','continuity_notes','raw_chain_of_thought_saved'}
REQ_SAY={'turn_id','panel_id','anonymous_alias','round','phase','speech_text','target_turn_refs','public_question_refs','public_evidence_refs','public_action_signals'}
REQ_META={'assignment_id','turn_id','speech_origin','speaker_private_belief_alignment','support_status','contains_known_falsehood','contains_unverified_assertion','contains_selective_omission','claim_gate_ingestion_prohibited','peer_visible','blind_adjudicator_visible','private_notes'}
PRIVATE_TOKENS={'private_goal','perceived_stakes','intended_omissions','truth_handling_this_turn','role_card_id','display_name_private','behavior_profile','assignment_id','speech_origin','speaker_private_belief_alignment','support_status','contains_known_falsehood','contains_unverified_assertion','contains_selective_omission','simulated_internal_only'}
ACCEPT_FIDELITY={'ROLE_FIDEL_HONEST','ROLE_FIDEL_SINCERE_BUT_MISTAKEN','ROLE_FIDEL_SELECTIVE','ROLE_FIDEL_STRATEGIC_DECEPTION','ROLE_FIDEL_EMOTIONAL_INCONSISTENCY','ROLE_FIDEL_WITH_EVIDENCE_UPDATE'}
REQUIRED_PHASES={'OPENING','DIRECT_REBUTTAL','PEER_CROSS_CHALLENGE','RESPONSIVE_REBUTTAL'}
SILENCE_MARKER_PATTERN=re.compile(r'^\(SEAT-\S+ 未发言\)$')

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def lines(p): return [json.loads(x) for x in p.read_text(encoding='utf-8').splitlines() if x.strip()] if p.exists() else []
def check_view(turn_dir,errors):
 scope=turn_dir/'input-scope.private.json';view=turn_dir/'scoped-view';manifest=view/'view-manifest.json'
 if not scope.exists(): errors.append(f'missing input scope: {scope}')
 if not manifest.exists(): errors.append(f'missing materialized scoped view: {manifest}')
 if scope.exists() and manifest.exists():
  s=load(scope);m=load(manifest);allow=s.get('allowlist',[]);files=m.get('files',[])
  if len(allow)!=len(files): errors.append(f'scoped view file count mismatch: {turn_dir}')
  sources=[x.get('source') for x in files]
  if sources!=allow: errors.append(f'scoped view allowlist mismatch: {turn_dir}')
  for rel in allow:
   if '/private/actors/' in rel and not rel.endswith('/assignment.json') and '/turns/' not in rel: errors.append(f'scoped view may expose actor-private tree: {turn_dir}: {rel}')

def main():
 if len(sys.argv)!=2: print('Usage: python scripts/audit_case.py <case-dir>',file=sys.stderr);return 2
 case=Path(sys.argv[1]);errors=[];warnings=[]
 if not (case/'manifest.json').exists(): errors.append('missing manifest.json'); print(json.dumps({'status':'FAIL','errors':errors})); return 1
 m=load(case/'manifest.json')
 # Direct-mode fast-path audit: only validate intake, parse, claim-gate, report
 if m.get('resolved_intensity')=='direct':
  for f in ['00-intake/user-request.md','01-parse/source-content.md','01-parse/content-parse.v001.json','02-research/claim-gate-packet.v001.json','07-report/final-report.md','07-report/final-report.json']:
   if not (case/f).exists(): errors.append(f'missing {f}')
  if not (case/'audit').exists(): errors.append('missing audit directory')
  result={'status':'PASS' if not errors else 'FAIL','errors':errors,'warnings':warnings,'role_count':0,'appearance_count':0,'panel_count':0,'public_turn_count':0}
  (case/'audit/case-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if not errors else 1
 for d in ['03-role-pool/private/roles','05-panels','06-aggregation/private','06-aggregation/public','audit']:
  if not (case/d).exists(): errors.append('missing '+d)
 roles=list((case/'03-role-pool/private/roles').glob('*/role-card.json'))
 role_ids={p.parent.name for p in roles}
 if m.get('role_pool_status')!='COMMITTED': errors.append('role pool not committed')
 if not (case/'03-role-pool/pool-commit.json').exists(): errors.append('missing role pool commit artifact')
 if not roles: errors.append('no persisted role cards')
 cards=[]
 # Build role_id -> response_policy map for silence policy checks
 role_policies={}
 for p in roles:
  card=load(p);cards.append(card);bp=card.get('behavior_profile',{})
  if not REQ_BEHAVIOR.issubset(bp): errors.append(f'role {p.parent.name}: incomplete factorized behavior profile')
  role_policies[p.parent.name]=bp.get('response_policy','ALWAYS_RESPOND')
 commit=load(case/'03-role-pool/pool-commit.json') if (case/'03-role-pool/pool-commit.json').exists() else {}
 gaps=diversity_gaps(cards)
 if gaps:
  msg='behavior diversity gaps: '+', '.join(gaps)
  if m.get('demo_underfilled_allowed') or commit.get('behavior_diversity_waiver'): warnings.append(msg)
  else: errors.append(msg)
 idx_roles={x.get('role_card_id') for x in lines(case/'03-role-pool/role-index.jsonl')}
 if idx_roles!=role_ids: errors.append(f'role-index.jsonl {idx_roles} != filesystem roles {role_ids}')
 brand_stances={card.get('brand_stance') for card in cards if card.get('brand_stance')}
 if len(brand_stances)<2: warnings.append(f'brand_stance coverage too narrow: only {len(brand_stances)} distinct stance(s) across all roles {brand_stances}')
 # Demographic profile completeness check
 demo_missing=[card.get('role_card_id','') for card in cards if not card.get('demographic_profile')]
 if demo_missing: errors.append(f'roles missing demographic_profile: {", ".join(demo_missing)}')
 topic_rels={str(card.get('demographic_profile',{}).get('topic_relevance','')) for card in cards}
 if len(topic_rels)<3: warnings.append(f'topic_relevance coverage narrow: only {topic_rels} — consider INDIFFERENT or OFF_TOPIC roles')
 appearances=lines(case/'03-role-pool/appearance-ledger.jsonl');panel_count=0;turn_count=0;all_assignment_ids=[];actual_panel_dirs=[]
 # Build assignment_id -> role_card_id map for policy checks
 asgn_to_role={}
 for panel in sorted((case/'05-panels').glob('panel-*')):
  if not panel.is_dir(): continue
  panel_count+=1;actual_panel_dirs.append(panel.name);pm=load(panel/'panel-manifest.json')
  if pm.get('assignments_status')!='COMMITTED': errors.append(f'{panel.name}: assignments not committed')
  if not (panel/'assignment-commit.json').exists(): errors.append(f'{panel.name}: missing assignment commit')
  assignments=lines(panel/'assignment-index.jsonl');all_assignment_ids += [x.get('assignment_id') for x in assignments]
  for a in assignments:
   asgn_to_role[a.get('assignment_id','')]=a.get('role_card_id','')
  if len(assignments)<2: errors.append(f'{panel.name}: fewer than two assignments')
  aliases={x['anonymous_alias'] for x in assignments}
  for a in assignments:
   if a.get('role_card_id') not in role_ids: errors.append(f'{panel.name}: assignment references missing case-level role {a.get("role_card_id")}')
  transcript=lines(panel/'transcript.public.jsonl')
  fallback=lines(panel/'public/transcript.public.jsonl')
  if not transcript and fallback: transcript=fallback
  elif transcript and fallback and len(fallback)>len(transcript): transcript=fallback
  turn_count+=len(transcript);phases={x.get('phase') for x in transcript}
  if pm.get('status')=='CLOSED' and not REQUIRED_PHASES.issubset(phases): errors.append(f'{panel.name}: closed court lacks required peer debate phases')
  cycles=sum(1 for x in transcript if x.get('phase')=='RESPONSIVE_REBUTTAL')//max(1,len(assignments))
  level=m.get('resolved_intensity');profile=PROFILES.get(level)
  if pm.get('status')=='CLOSED' and profile and cycles<profile['min_peer_cycles']: errors.append(f'{panel.name}: peer cycles {cycles} < {profile["min_peer_cycles"]}')
  # ── Silence-specific transcript validation ──
  for row in transcript:
   if PRIVATE_TOKENS.intersection(row): errors.append(f'{panel.name}: public transcript leaks private fields')
   if not REQ_SAY.issubset(row): errors.append(f'{panel.name}: malformed public say {row.get("turn_id")}')
   if row.get('anonymous_alias') not in aliases: errors.append(f'{panel.name}: unknown alias in transcript')
   entry_type=row.get('entry_type','SPEECH')
   if entry_type=='SILENCE':
    # Validate silence marker format
    if not SILENCE_MARKER_PATTERN.match(row.get('speech_text','')):
     errors.append(f'{panel.name}: SILENCE entry speech_text must match "(SEAT-X 未发言)", got: {row.get("speech_text","")}')
    if row.get('target_turn_refs',[]): errors.append(f'{panel.name}: SILENCE entry target_turn_refs must be empty')
    if row.get('public_evidence_refs',[]): errors.append(f'{panel.name}: SILENCE entry public_evidence_refs must be empty')
    # OPENING phase must never have silence
    if row.get('phase')=='OPENING':
     errors.append(f'{panel.name}: OPENING phase must not have silence entries (mandatory response) — {row.get("turn_id")}')
  for a in assignments:
   actor=panel/'private/actors'/a['assignment_id']
   if not (actor/'assignment.json').exists(): errors.append(f'{panel.name}: missing actor assignment folder {a["assignment_id"]}')
   turns=list((actor/'turns').glob('round-*')) if (actor/'turns').exists() else []
   if not turns: warnings.append(f'{panel.name}: actor {a["assignment_id"]} has no turn artifacts yet')
   # Get this actor's response_policy
   rc_id=asgn_to_role.get(a['assignment_id'],'')
   policy=role_policies.get(rc_id,'ALWAYS_RESPOND')
   silence_count=0
   for t in turns:
    if not (t/'say.public.json').exists(): errors.append(f'{panel.name}: missing say.public.json in {t.relative_to(panel)}')
    has_new=(t/'turn.private.json').exists()
    has_old=(t/'think.private.json').exists()
    if not has_new and not has_old: errors.append(f'{panel.name}: missing turn artifacts in {t.relative_to(panel)}')
    check_view(t,errors)
    # Check if this is a silence turn
    is_silent=False
    if (t/'say.public.json').exists():
     say_obj=load(t/'say.public.json')
     is_silent=say_obj.get('entry_type','')=='SILENCE'
    if is_silent:
     silence_count+=1
     # Verify response-decision.private.json exists
     if not (t/'response-decision.private.json').exists(): errors.append(f'{panel.name}: silent turn missing response-decision.private.json in {t.relative_to(case)}')
     # Verify inner_monologue still present in think (mandatory every round)
    # New format: turn.private.json (think+filing+fidelity merged)
    if has_new:
     tp=load(t/'turn.private.json')
     think=tp.get('think',{})
     missing_think=sorted(REQ_THINK-set(think))
     if missing_think: errors.append(f'{panel.name}: think {t.relative_to(case)} missing: {", ".join(missing_think)}')
     if think.get('raw_chain_of_thought_saved') is not False: errors.append(f'{panel.name}: raw chain of thought must not be saved')
     mono=think.get('inner_monologue','')
     if not mono or len(mono)<100: warnings.append(f'{panel.name}: inner_monologue too short ({len(mono)} chars) in {t.relative_to(case)}')
     filing=tp.get('filing_metadata',{})
     if filing.get('claim_gate_ingestion_prohibited') is not True: errors.append(f'{panel.name}: actor speech must not enter claim gate directly {t}')
     if filing.get('peer_visible') is not False or filing.get('blind_adjudicator_visible') is not False: errors.append(f'{panel.name}: private filing metadata visibility violation {t}')
     # For silence turns, speech_origin should be STRATEGIC_SILENCE
     if is_silent and filing.get('speech_origin')!='STRATEGIC_SILENCE': errors.append(f'{panel.name}: silent turn speech_origin must be STRATEGIC_SILENCE, got {filing.get("speech_origin")}')
     bf=tp.get('behavior_fidelity',{})
     if not bf.get('admit_to_public_record') or bf.get('classification') not in ACCEPT_FIDELITY: errors.append(f'{panel.name}: public say admitted without behavior fidelity pass {t}')
    # Old format backward compat
    elif has_old:
     obj=load(t/'think.private.json')
     missing_think=sorted(REQ_THINK-set(obj))
     if missing_think: errors.append(f'{panel.name}: think memo {t.relative_to(case)} missing: {", ".join(missing_think)}')
     if obj.get('raw_chain_of_thought_saved') is not False: errors.append(f'{panel.name}: raw chain of thought must not be saved')
     mono=obj.get('inner_monologue','')
     if not mono or len(mono)<100: warnings.append(f'{panel.name}: think inner_monologue too short ({len(mono)} chars) in {t.relative_to(case)}')
     if (t/'filing-metadata.private.json').exists():
      meta=load(t/'filing-metadata.private.json')
      if meta.get('claim_gate_ingestion_prohibited') is not True: errors.append(f'{panel.name}: actor speech must not enter claim gate directly {t}')
      if meta.get('peer_visible') is not False or meta.get('blind_adjudicator_visible') is not False: errors.append(f'{panel.name}: private filing metadata visibility violation {t}')
     if (t/'behavior-fidelity.private.json').exists():
      g=load(t/'behavior-fidelity.private.json')
      if not g.get('admit_to_public_record') or g.get('classification') not in ACCEPT_FIDELITY: errors.append(f'{panel.name}: public say admitted without behavior fidelity pass {t}')
    if (t/'say.public.json').exists():
     obj=load(t/'say.public.json')
     missing_say=sorted(REQ_SAY-set(obj))
     if missing_say: errors.append(f'{panel.name}: say file {t.relative_to(case)} missing: {", ".join(missing_say)}')
     if PRIVATE_TOKENS.intersection(obj): errors.append(f'{panel.name}: public say leaks private fields {t}')
   # Check: ALWAYS_RESPOND / FULLY_ENGAGED actors must have zero silence
   if policy in ('ALWAYS_RESPOND','FULLY_ENGAGED') and silence_count>0:
    errors.append(f'{panel.name}: actor {a["assignment_id"]} has response_policy={policy} but has {silence_count} silence turn(s)')
  judge=panel/'session/blind-adjudicator/verdict-packet.json'
  if pm.get('status')=='CLOSED' and not judge.exists(): errors.append(f'{panel.name}: closed court missing blind verdict packet')
  if judge.exists():
   txt=judge.read_text(encoding='utf-8')
   for token in PRIVATE_TOKENS:
    if token in txt: errors.append(f'{panel.name}: blind packet leaks {token}')
   if not (panel/'verdict/verdict.json').exists(): errors.append(f'{panel.name}: missing blind verdict')
   elif not (panel/'verdict/verdict.md').exists(): warnings.append(f'{panel.name}: verdict.json exists but verdict.md is missing')
 idx_panel_dirs={x.get('panel_dir','').rsplit('/',1)[-1] for x in lines(case/'05-panels/panel-index.jsonl')}
 if idx_panel_dirs!=set(actual_panel_dirs): errors.append(f'panel-index.jsonl {idx_panel_dirs} != filesystem panels {set(actual_panel_dirs)}')
 app_ids=[x.get('assignment_id') for x in appearances]
 if sorted(app_ids)!=sorted(all_assignment_ids): errors.append('appearance ledger does not match panel assignments')
 level=m.get('resolved_intensity');profile=PROFILES.get(level);demo=bool(m.get('demo_underfilled_allowed'))
 if profile:
  deficits=[]
  if panel_count<profile['min_panels']: deficits.append(f'panels {panel_count} < {profile["min_panels"]}')
  if len(appearances)<profile['min_appearances']: deficits.append(f'appearances {len(appearances)} < {profile["min_appearances"]}')
  if len(role_ids)<profile['min_unique_roles']: deficits.append(f'unique roles {len(role_ids)} < {profile["min_unique_roles"]}')
  if deficits:
   msg='intensity underfilled: '+', '.join(deficits)
   (warnings if demo else errors).append(msg)
 replay=case/'06-aggregation/private/full-replay-analysis.json'
 if m.get('status')=='COMPLETE':
  if not replay.exists(): errors.append('complete case missing full private replay')
  else:
   r=load(replay)
   for key in ['stakeholder_reactions','private_public_gap_findings','epistemic_behavior_findings','cross_issue_continuity','deception_and_distortion_signals','balanced_assessment','limitations']:
    if key not in r: errors.append(f'full replay missing {key}')
   ba=r.get('balanced_assessment',{})
   if ba:
    for bak in ['attack_resilience','content_strengths','net_verdict','overreaction_warning','modification_priority']:
     if bak not in ba: warnings.append(f'balanced_assessment missing recommended field {bak}')
 result={'status':'PASS' if not errors else 'FAIL','errors':errors,'warnings':warnings,'role_count':len(roles),'appearance_count':len(appearances),'panel_count':panel_count,'public_turn_count':turn_count}
 (case/'audit/case-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2));return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
