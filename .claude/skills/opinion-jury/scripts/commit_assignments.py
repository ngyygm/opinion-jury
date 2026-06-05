#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import argparse,json

def main():
 ap=argparse.ArgumentParser();ap.add_argument('panel_dir');a=ap.parse_args();panel=Path(a.panel_dir);rows=[json.loads(x) for x in (panel/'assignment-index.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
 if len(rows)<2: raise SystemExit('need at least two actor assignments')
 ts=datetime.now(timezone.utc).isoformat();(panel/'assignment-commit.json').write_text(json.dumps({'committed_at':ts,'assignment_count':len(rows)},indent=2)+'\n',encoding='utf-8')
 p=panel/'panel-manifest.json';m=json.loads(p.read_text(encoding='utf-8'));m['assignments_status']='COMMITTED';m['status']='ASSIGNMENTS_COMMITTED';p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(p)
if __name__=='__main__': main()
