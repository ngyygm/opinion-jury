#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import argparse,json
from behavior_diversity import profile_errors, diversity_gaps

def main():
 ap=argparse.ArgumentParser();ap.add_argument('case_dir');ap.add_argument('--diversity-waiver',default='');a=ap.parse_args();case=Path(a.case_dir);role_paths=list((case/'03-role-pool/private/roles').glob('*/role-card.json'))
 if not role_paths: raise SystemExit('cannot commit empty role pool')
 cards=[json.loads(p.read_text(encoding='utf-8')) for p in role_paths]
 errs=profile_errors(cards)
 if errs: raise SystemExit('invalid role pool: '+'; '.join(errs))
 gaps=diversity_gaps(cards)
 if gaps and not a.diversity_waiver: raise SystemExit('behavior diversity barrier not satisfied: '+', '.join(gaps)+'; use --diversity-waiver with a written reason only when necessary')
 ts=datetime.now(timezone.utc).isoformat();commit={'committed_at':ts,'role_count':len(role_paths),'roles':[p.parent.name for p in role_paths],'behavior_diversity_gaps':gaps,'behavior_diversity_waiver':a.diversity_waiver or None}
 (case/'03-role-pool/pool-commit.json').write_text(json.dumps(commit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p=case/'manifest.json';m=json.loads(p.read_text(encoding='utf-8'));m['role_pool_status']='COMMITTED';m['status']='ROLE_POOL_COMMITTED';p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(p)
if __name__=='__main__': main()
