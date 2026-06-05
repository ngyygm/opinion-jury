#!/usr/bin/env python3
"""Append a say.public.json entry to the panel's transcript.public.jsonl.

Usage:
  python append_transcript.py <panel_dir> --say-file path/to/say.public.json

Validates that the say entry has all required fields and contains no private tokens.
"""
from pathlib import Path
import argparse,json,sys

REQ_SAY={'turn_id','panel_id','anonymous_alias','round','phase','speech_text','target_turn_refs','public_question_refs','public_evidence_refs','public_action_signals'}
PRIVATE_TOKENS={'private_goal','perceived_stakes','intended_omissions','truth_handling_this_turn','role_card_id','display_name_private','behavior_profile','assignment_id','speech_origin','speaker_private_belief_alignment','support_status','contains_known_falsehood','contains_unverified_assertion','contains_selective_omission','simulated_internal_only'}

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
    json_path.write_text(json.dumps(arr,ensure_ascii=False,indent=2)+'\n')
  except (json.JSONDecodeError,ValueError):
   pass  # skip if malformed

 print(f'Appended {say.get("turn_id","entry")} to {jsonl_path}')

if __name__=='__main__': main()
