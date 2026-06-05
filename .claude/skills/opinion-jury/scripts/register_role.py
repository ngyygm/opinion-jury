#!/usr/bin/env python3
from pathlib import Path
import argparse,json,shutil
from behavior_diversity import profile_errors

def main():
 ap=argparse.ArgumentParser();ap.add_argument('case_dir');ap.add_argument('role_card');a=ap.parse_args();case=Path(a.case_dir);src=Path(a.role_card)
 m=json.loads((case/'manifest.json').read_text(encoding='utf-8'));
 if m.get('role_pool_status')=='COMMITTED': raise SystemExit('role pool already committed')
 role=json.loads(src.read_text(encoding='utf-8'));errs=profile_errors([role])
 if errs: raise SystemExit('invalid role card: '+'; '.join(errs))
 rid=role['role_card_id'];dest=case/'03-role-pool/private/roles'/rid/'role-card.json';dest.parent.mkdir(parents=True,exist_ok=False);shutil.copy2(src,dest)
 with (case/'03-role-pool/role-index.jsonl').open('a',encoding='utf-8') as h:h.write(json.dumps({'role_card_id':rid,'path':dest.relative_to(case).as_posix()},ensure_ascii=False)+'\n')
 print(dest)
if __name__=='__main__': main()
