#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,shutil

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('case_dir');ap.add_argument('scope_json');a=ap.parse_args();case=Path(a.case_dir).resolve();scope=Path(a.scope_json).resolve();obj=json.loads(scope.read_text(encoding='utf-8'));view=scope.parent/'scoped-view'
 if view.exists(): shutil.rmtree(view)
 view.mkdir();manifest=[]
 for i,rel in enumerate(obj['allowlist'],1):
  src=case/rel
  if not src.is_file(): raise SystemExit('missing allowed file '+rel)
  dest=view/f'{i:03d}-{src.name}';shutil.copy2(src,dest);manifest.append({'source':rel,'view_file':dest.name,'sha256':sha(dest),'size':dest.stat().st_size})
 scope_id=obj.get('scope_id',f'{obj.get("assignment_id","unknown")}-{obj.get("round","?")}-{obj.get("phase","?")}')
 (view/'view-manifest.json').write_text(json.dumps({'scope_id':scope_id,'files':manifest},ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(view)
if __name__=='__main__': main()
