#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import argparse,json

def main():
 ap=argparse.ArgumentParser();ap.add_argument('case_dir');ap.add_argument('panel_dir');ap.add_argument('assignment_id');ap.add_argument('role_card_id');ap.add_argument('--alias',required=True);ap.add_argument('--trigger',required=True);ap.add_argument('--goal',required=True);a=ap.parse_args();case=Path(a.case_dir);panel=Path(a.panel_dir)
 if not panel.is_absolute(): panel=case/panel
 role=case/'03-role-pool/private/roles'/a.role_card_id/'role-card.json'
 if not role.exists(): raise SystemExit('role card not found in committed role pool')
 pm=json.loads((panel/'panel-manifest.json').read_text(encoding='utf-8'));
 if pm.get('assignments_status')=='COMMITTED': raise SystemExit('assignments already committed')
 actor=panel/'private/actors'/a.assignment_id;actor.mkdir(parents=True,exist_ok=False);(actor/'turns').mkdir()
 row={'assignment_id':a.assignment_id,'panel_id':pm['panel_id'],'role_card_id':a.role_card_id,'anonymous_alias':a.alias,'issue_trigger':a.trigger,'court_specific_goal':a.goal,'observable_evidence_refs':[],'created_at':datetime.now(timezone.utc).isoformat()}
 (actor/'assignment.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
 with (panel/'assignment-index.jsonl').open('a',encoding='utf-8') as h:h.write(json.dumps(row,ensure_ascii=False)+'\n')
 with (case/'03-role-pool/appearance-ledger.jsonl').open('a',encoding='utf-8') as h:h.write(json.dumps({'assignment_id':a.assignment_id,'panel_id':pm['panel_id'],'role_card_id':a.role_card_id},ensure_ascii=False)+'\n')
 print(actor)
if __name__=='__main__': main()
