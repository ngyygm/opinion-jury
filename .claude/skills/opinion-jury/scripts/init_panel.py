#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,re

def main():
 ap=argparse.ArgumentParser();ap.add_argument('case_dir');ap.add_argument('panel_id');ap.add_argument('issue_id');ap.add_argument('slug');ap.add_argument('--title',default='');a=ap.parse_args();case=Path(a.case_dir)
 m=json.loads((case/'manifest.json').read_text(encoding='utf-8'));
 if m.get('role_pool_status')!='COMMITTED': raise SystemExit('ROLE_POOL_COMMITTED barrier not satisfied')
 folder=a.panel_id.lower()+'-'+re.sub(r'[^a-z0-9]+','-',a.slug.lower()).strip('-');panel=case/'05-panels'/folder
 for d in ['private/actors','session/public-snapshots','session/blind-adjudicator','verdict']: (panel/d).mkdir(parents=True,exist_ok=True)
 for f in ['transcript.public.jsonl','public-disclosures.jsonl','assignment-index.jsonl']: (panel/f).touch()
 pm={'panel_id':a.panel_id,'issue_id':a.issue_id,'title':a.title or a.slug,'created_at':datetime.now(timezone.utc).isoformat(),'status':'INITIALIZED','assignments_status':'DRAFT'}
 (panel/'panel-manifest.json').write_text(json.dumps(pm,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');(panel/'public-question.md').write_text('# Court question\n\n'+pm['title']+'\n',encoding='utf-8')
 with (case/'05-panels/panel-index.jsonl').open('a',encoding='utf-8') as h:h.write(json.dumps({'panel_id':a.panel_id,'panel_dir':panel.relative_to(case).as_posix()},ensure_ascii=False)+'\n')
 print(panel)
if __name__=='__main__': main()
