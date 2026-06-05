#!/usr/bin/env python3
"""Write a complete set of turn artifacts with correct schema fields.

Simplified from 7 files to 3 files per turn:
  - say.public.json     (public, others can read)
  - turn.private.json   (private: think + filing + fidelity merged)
  - scoped-view/        (multi-blind isolation copies)

Usage:
  python write_turn.py <case_dir> <panel_dir> <assignment_id> \
    --round 01-opening --phase OPENING \
    --think think_input.json --say say_input.json \
    --filing-classification SINCERE_SUPPORTED \
    --fidelity-classification ROLE_FIDEL_HONEST \
    --truth-handling HONEST
"""
from pathlib import Path
import argparse,json,sys

REQ_THINK={'inner_monologue','assignment_id','round','phase','private_goal','perceived_stakes','private_belief_state','epistemic_state','confidence','uncertainties','intended_emphasis','intended_omissions','private_message_strategy','planned_public_claims','rhetorical_tactics','truth_handling_this_turn','private_action_intent','likely_next_action','emotional_state','continuity_notes','raw_chain_of_thought_saved'}
REQ_SAY={'turn_id','panel_id','anonymous_alias','round','phase','speech_text','target_turn_refs','public_question_refs','public_evidence_refs','public_action_signals'}
SPEECH_ORIGINS={'SINCERE_SUPPORTED','SINCERE_MISTAKEN','SELECTIVE_FRAMING','EXAGGERATION','RUMOR_RELAY','KNOWING_FABRICATION_STRESS_TEST','MIXED'}
FIDELITY_CLASSES={'ROLE_FIDEL_HONEST','ROLE_FIDEL_SINCERE_BUT_MISTAKEN','ROLE_FIDEL_SELECTIVE','ROLE_FIDEL_STRATEGIC_DECEPTION','ROLE_FIDEL_EMOTIONAL_INCONSISTENCY','ROLE_FIDEL_WITH_EVIDENCE_UPDATE'}
TRUTH_HANDLINGS={'HONEST','SINCERE_BUT_MISTAKEN','SELECTIVE_FRAMING','EXAGGERATION','RUMOR_RELAY','FABRICATION_STRESS_TEST','MIXED'}

def main():
 ap=argparse.ArgumentParser(description='Write a complete set of turn artifacts')
 ap.add_argument('case_dir');ap.add_argument('panel_dir');ap.add_argument('assignment_id')
 ap.add_argument('--round',required=True,help='e.g. 01-opening')
 ap.add_argument('--phase',required=True,help='e.g. OPENING')
 ap.add_argument('--think',required=True,help='Path to think input JSON (may be partial)')
 ap.add_argument('--say',required=True,help='Path to say input JSON or plain text')
 ap.add_argument('--filing-classification',required=True,choices=sorted(SPEECH_ORIGINS))
 ap.add_argument('--fidelity-classification',required=True,choices=sorted(FIDELITY_CLASSES))
 ap.add_argument('--truth-handling',required=True,choices=sorted(TRUTH_HANDLINGS))
 a=ap.parse_args()
 case=Path(a.case_dir);panel=Path(a.panel_dir)
 if not panel.is_absolute(): panel=case/panel

 # Load assignment for alias and panel_id
 asgn_path=panel/'private/actors'/a.assignment_id/'assignment.json'
 if not asgn_path.exists(): raise SystemExit(f'assignment not found: {asgn_path}')
 asgn=json.loads(asgn_path.read_text(encoding='utf-8'))
 alias=asgn.get('anonymous_alias','')
 panel_id=asgn.get('panel_id',panel.name)

 turn_dir=panel/'private/actors'/a.assignment_id/'turns'/f'round-{a.round}'
 turn_dir.mkdir(parents=True,exist_ok=True)

 # ── Load think input ──────────────────────────────────────────
 think_path=Path(a.think)
 think_in=json.loads(think_path.read_text(encoding='utf-8'))

 round_num=a.round.split('-')[0] if '-' in a.round else a.round
 try: round_int=int(round_num)
 except ValueError: round_int=round_num

 think={
  'inner_monologue': think_in.get('inner_monologue',think_in.get('monologue','')),
  'assignment_id': a.assignment_id,
  'round': round_int,
  'phase': a.phase,
  'private_goal': think_in.get('private_goal',''),
  'perceived_stakes': think_in.get('perceived_stakes',[]),
  'private_belief_state': think_in.get('private_belief_state',think_in.get('sincerely_held_beliefs',[])),
  'epistemic_state': think_in.get('epistemic_state',[]),
  'confidence': think_in.get('confidence','MEDIUM'),
  'uncertainties': think_in.get('uncertainties',[]),
  'intended_emphasis': think_in.get('intended_emphasis',[]),
  'intended_omissions': think_in.get('intended_omissions',[]),
  'private_message_strategy': think_in.get('private_message_strategy',''),
  'planned_public_claims': think_in.get('planned_public_claims',[]),
  'rhetorical_tactics': think_in.get('rhetorical_tactics',[]),
  'truth_handling_this_turn': a.truth_handling,
  'private_action_intent': think_in.get('private_action_intent',[]),
  'likely_next_action': think_in.get('likely_next_action',[]),
  'emotional_state': think_in.get('emotional_state',''),
  'continuity_notes': think_in.get('continuity_notes',''),
  'raw_chain_of_thought_saved': False,
 }
 # Ensure array fields are arrays
 for k in ('perceived_stakes','private_belief_state','epistemic_state','uncertainties','intended_emphasis','intended_omissions','planned_public_claims','rhetorical_tactics','private_action_intent','likely_next_action'):
  if isinstance(think[k],str): think[k]=[think[k]]

 # ── Build filing-metadata ─────────────────────────────────────
 fc=a.filing_classification
 filing={
  'assignment_id': a.assignment_id,
  'turn_id': f'{a.assignment_id}-round-{a.round}',
  'speech_origin': fc,
  'speaker_private_belief_alignment': 'ALIGNED' if fc in ('SINCERE_SUPPORTED','SINCERE_MISTAKEN') else 'PARTIALLY_ALIGNED' if fc in ('SELECTIVE_FRAMING','MIXED') else 'NOT_ALIGNED',
  'support_status': 'SUPPORTED' if fc=='SINCERE_SUPPORTED' else 'UNVERIFIED' if fc in ('SINCERE_MISTAKEN','RUMOR_RELAY') else 'KNOWN_UNSUPPORTED' if fc=='KNOWING_FABRICATION_STRESS_TEST' else 'MIXED',
  'contains_known_falsehood': fc in ('KNOWING_FABRICATION_STRESS_TEST',),
  'contains_unverified_assertion': fc in ('EXAGGERATION','RUMOR_RELAY','SINCERE_MISTAKEN'),
  'contains_selective_omission': fc in ('SELECTIVE_FRAMING','MIXED'),
  'claim_gate_ingestion_prohibited': True,
  'peer_visible': False,
  'blind_adjudicator_visible': False,
  'private_notes': f'Auto-classified as {fc}',
 }

 # ── Build behavior-fidelity ───────────────────────────────────
 fidelity={
  'assignment_id': a.assignment_id,
  'turn_id': f'{a.assignment_id}-round-{a.round}',
  'classification': a.fidelity_classification,
  'admit_to_public_record': True,
  'fidelity_notes': 'Auto-admitted with classification',
  'safety_notes': 'Within safety boundaries',
 }

 # ── Write turn.private.json (merged: think + filing + fidelity) ──
 turn_private={
  '_structure': 'think + filing_metadata + behavior_fidelity merged into single file',
  '_visibility': 'private — only replay analyst may read',
  'think': think,
  'filing_metadata': filing,
  'behavior_fidelity': fidelity,
 }
 (turn_dir/'turn.private.json').write_text(json.dumps(turn_private,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

 # ── Load say input and write say.public.json ──────────────────
 say_path=Path(a.say)
 try:
  say_in=json.loads(say_path.read_text(encoding='utf-8'))
 except (json.JSONDecodeError,UnicodeDecodeError):
  say_in={'speech_text':say_path.read_text(encoding='utf-8')}

 say={
  'turn_id': f'{a.assignment_id}-round-{a.round}',
  'panel_id': panel_id,
  'anonymous_alias': say_in.get('alias',alias),
  'round': round_int,
  'phase': say_in.get('phase',a.phase),
  'speech_text': say_in.get('speech_text',say_in.get('text','')),
  'target_turn_refs': say_in.get('target_turn_refs',say_in.get('references',[])),
  'public_question_refs': say_in.get('public_question_refs',[]),
  'public_evidence_refs': say_in.get('public_evidence_refs',[]),
  'public_action_signals': say_in.get('public_action_signals',[]),
 }
 (turn_dir/'say.public.json').write_text(json.dumps(say,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

 # ── Build scoped-view (multi-blind isolation) ─────────────────
 sv=turn_dir/'scoped-view';sv.mkdir(exist_ok=True)
 try: panel_rel=panel.relative_to(case).as_posix()
 except ValueError: panel_rel=panel.name
 scope={
  'scope_type':'actor_turn_input',
  'allowlist':[
   '01-parse/source-content.md',
   f'{panel_rel}/transcript.public.jsonl',
  ],
  'includes':['source_content','prior_public_transcript'],
  'excludes':['other_actor_cards','other_private_memos','filing_metadata','identity_maps','blind_verdict'],
 }
 (sv/'view-manifest.json').write_text(json.dumps(scope,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

 # ── Clean up tmp/ artifacts left by the agent ─────────────────
 import shutil
 for tmp in [turn_dir.parent/'tmp', turn_dir/'tmp']:
  if tmp.exists(): shutil.rmtree(tmp,ignore_errors=True)

 print(turn_dir)

if __name__=='__main__': main()
