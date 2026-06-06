#!/usr/bin/env python3
"""Append a say.public.json entry to the panel's transcript.public.jsonl.

Usage:
  python append_transcript.py <panel_dir> --say-file path/to/say.public.json

Validates that the say entry has all required fields and contains no private tokens.
Supports both SPEECH and SILENCE entry types.
"""
from pathlib import Path
import argparse,json,sys,re

REQ_SAY={'turn_id','panel_id','anonymous_alias','round','phase','speech_text','target_turn_refs','public_question_refs','public_evidence_refs','public_action_signals'}
PRIVATE_TOKENS={'private_goal','perceived_stakes','intended_omissions','truth_handling_this_turn','role_card_id','display_name_private','behavior_profile','assignment_id','speech_origin','speaker_private_belief_alignment','support_status','contains_known_falsehood','contains_unverified_assertion','contains_selective_omission','simulated_internal_only'}
SILENCE_MARKER_PATTERN=re.compile(r'^\(SEAT-\S+ 未发言\)$')

def main():
 ap=argparse.ArgumentParser(description='Append say entry to panel transcript')
 ap.add_argument('panel_dir');ap.add_argument('--say-file',required=True);ap.add_argument('--case-dir',default='',help='Resolve panel_dir relative to case_dir if provided')
 a=ap.parse_args();panel=Path(a.panel_dir)
 if not panel.is_absolute():
  if a.case_dir: panel=Path(a.case_dir)/panel
  else: panel=Path.cwd()/panel

 say_path=Path(a.say_file)
 say=json.loads(say_path.read_text(encoding='utf-8'))

 # Validate required fields
 missing=sorted(REQ_SAY-set(say.keys()))
 if missing: raise SystemExit(f'say.public.json missing required fields: {", ".join(missing)}')

 # Check for private token leaks
 leaked=PRIVATE_TOKENS.intersection(say.keys())
 if leaked: raise SystemExit(f'say.public.json contains private tokens: {", ".join(sorted(leaked))}')

 # Validate silence markers
 entry_type=say.get('entry_type','SPEECH')
 if entry_type=='SILENCE':
  # Verify speech_text matches silence marker pattern
  if not SILENCE_MARKER_PATTERN.match(say['speech_text']):
   raise SystemExit(f'SILENCE entry speech_text must match pattern "(SEAT-X 未发言)", got: {say["speech_text"]}')
  # Verify refs are empty
  if say.get('target_turn_refs',[]):
   raise SystemExit(f'SILENCE entry target_turn_refs must be empty, got: {say["target_turn_refs"]}')
  if say.get('public_question_refs',[]):
   raise SystemExit(f'SILENCE entry public_question_refs must be empty, got: {say["public_question_refs"]}')
  if say.get('public_evidence_refs',[]):
   raise SystemExit(f'SILENCE entry public_evidence_refs must be empty, got: {say["public_evidence_refs"]}')
  # public_action_signals may contain silence-appropriate signals or be empty
  valid_silence_signals={'WITHDREW_FROM_ROUND'}
  invalid=[s for s in say.get('public_action_signals',[]) if s not in valid_silence_signals]
  if invalid:
   raise SystemExit(f'SILENCE entry public_action_signals contains invalid signals: {invalid}')

 # Append to transcript.public.jsonl (created by init_panel.py in panel root)
 jsonl_path=panel/'transcript.public.jsonl'
 jsonl_path.parent.mkdir(parents=True,exist_ok=True)
 with jsonl_path.open('a',encoding='utf-8') as f:
  f.write(json.dumps(say,ensure_ascii=False)+'\n')

 # Also update the JSON array version in public/ if it exists
 json_path=panel/'public'/'transcript.public.json'
 if json_path.exists():
  try:
   arr=json.loads(json_path.read_text(encoding='utf-8'))
   if isinstance(arr,list):
    arr.append(say)
    json_path.write_text(json.dumps(arr,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  except (json.JSONDecodeError,ValueError):
   pass  # skip if malformed

 entry_type_display=f' [{entry_type}]' if entry_type!='SPEECH' else ''
 print(f'Appended {say.get("turn_id","entry")}{entry_type_display} to {jsonl_path}')

if __name__=='__main__': main()
