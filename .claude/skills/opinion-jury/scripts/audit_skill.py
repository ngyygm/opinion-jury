#!/usr/bin/env python3
from pathlib import Path
import json,sys

def main():
 root=Path(sys.argv[1] if len(sys.argv)>1 else '.');errors=[]
 for f in ['SKILL.md','README.md','config/defaults.yaml','references/behavior-simulation-model.md','references/private-think-public-say.md','references/filesystem-isolation-contract.md','scripts/audit_case.py','schemas/filing-metadata.schema.json']:
  if not (root/f).exists(): errors.append('missing '+f)
 for p in (root/'schemas').glob('*.json'):
  try: json.loads(p.read_text(encoding='utf-8'))
  except Exception as e: errors.append(f'invalid schema {p}: {e}')
 skill=(root/'SKILL.md').read_text(encoding='utf-8') if (root/'SKILL.md').exists() else ''
 for token in ['name: opinion-jury','BEHAVIOR_FIDELITY_GUARD','filing-metadata.private.json','think.private.json','say.public.json']:
  if token not in skill: errors.append('missing skill contract token '+token)
 print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors,'schema_count':len(list((root/'schemas').glob('*.json')))},ensure_ascii=False,indent=2));return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
