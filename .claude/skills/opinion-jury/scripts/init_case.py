#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,re,shutil

def now(): return datetime.now().isoformat()

def sanitize_slug(s):
 """Sanitize an agent-provided slug. Remove unsafe chars, keep CJK/Latin/digits/-_."""
 s=s.strip()
 out=[]
 for ch in s:
  if ch in '-_':
   if out and out[-1] not in '-_': out.append(ch)
  elif 'a' <= ch <= 'z' or 'A' <= ch <= 'Z' or '0' <= ch <= '9':
   out.append(ch)
  elif '一' <= ch <= '鿿' or '぀' <= ch <= 'ヿ' or '가' <= ch <= '힯':
   out.append(ch)
 while out and out[-1] in '-_': out.pop()
 return ''.join(out)[:64] if out else 'untitled'

def touch(p): p.parent.mkdir(parents=True,exist_ok=True);p.touch()

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--topic',required=True,help='Full topic text (stored in manifest)')
 ap.add_argument('--slug',required=True,help='Short meaningful slug for directory name, provided by the calling agent. Example: 骂人字带女字旁')
 ap.add_argument('--root',default='opinion-jury-cases')
 ap.add_argument('--intensity',default='auto')
 ap.add_argument('--content-file',default=None,help='Path to a file containing the full raw user input to preserve verbatim')
 ap.add_argument('--content',default=None,help='Raw content string (alternative to --content-file, avoids temp files)')
 a=ap.parse_args()

 slug_str=sanitize_slug(a.slug)
 root=Path(a.root).resolve()

 # ── Idempotency: check if a case with the same slug already exists ──────────
 existing=list(root.glob(f"*-{slug_str}"))
 valid_case=None
 for ex in existing:
  if (ex/'manifest.json').exists():
   valid_case=ex
  else:
   # Orphan directory (no manifest) — clean it up
   shutil.rmtree(ex,ignore_errors=True)
 if valid_case:
  print(valid_case)
  return

 ts=now()
 cid=datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+slug_str
 case=root/cid

 for d in ['00-intake','01-parse','02-research','03-role-pool/private/roles','04-issues','05-panels','06-aggregation/private','06-aggregation/public','07-report','audit']:
  (case/d).mkdir(parents=True,exist_ok=True)

 for f in ['03-role-pool/role-index.jsonl','03-role-pool/appearance-ledger.jsonl','05-panels/panel-index.jsonl']:
  touch(case/f)

 # Write user-request.md: prefer --content string, then --content-file, then placeholder
 if a.content:
  (case/'00-intake/user-request.md').write_text(a.content,encoding='utf-8')
 elif a.content_file:
  try:
   raw=Path(a.content_file).read_text(encoding='utf-8')
  except FileNotFoundError:
   raw=f'# User request\n\nContent file not found: {a.content_file}\n'
  (case/'00-intake/user-request.md').write_text(raw,encoding='utf-8')
 else:
  (case/'00-intake/user-request.md').write_text('# User request\n\nPending capture.\n',encoding='utf-8')

 m={
  'case_id':cid,
  'topic':a.topic,
  'slug':slug_str,
  'created_at':ts,
  'status':'INITIALIZED',
  'requested_intensity':a.intensity,
  'resolved_intensity':'PENDING' if a.intensity=='auto' else a.intensity,
  'role_pool_status':'DRAFT'
 }
 (case/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(case)

if __name__=='__main__': main()
