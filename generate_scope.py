#!/usr/bin/env python3
"""Generate/fix input-scope.private.json and scoped-view/view-manifest.json files.
Overwrites existing manifests that have the wrong schema."""
import json, hashlib, shutil
from pathlib import Path

CASE = Path(r"D:\exa\opinion-jury\opinion-jury-cases\20260605-193330-胖猫跳江通报")

ROUNDS = [
    ("round-01-opening", "001"),
    ("round-02-direct-rebuttal", "002"),
    ("round-03-peer-cross-challenge", "003"),
    ("round-04-responsive-rebuttal", "004"),
    ("round-05-peer-cross-challenge", "005"),
    ("round-06-responsive-rebuttal", "006"),
]

def sha256_file(p):
    if p.exists():
        return hashlib.sha256(p.read_bytes()).hexdigest()
    return "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

def file_size(p):
    if p.exists():
        return p.stat().st_size
    return 0

def needs_fix(scope_path, manifest_path):
    """Check if the manifest matches the scope correctly."""
    if not scope_path.exists() or not manifest_path.exists():
        return True
    try:
        s = json.loads(scope_path.read_text(encoding='utf-8'))
        m = json.loads(manifest_path.read_text(encoding='utf-8'))
        allow = s.get('allowlist', [])
        files = m.get('files', [])
        sources = [x.get('source') for x in files]
        if len(allow) != len(files):
            return True
        if sources != allow:
            return True
        return False
    except Exception:
        return True

def main():
    panel_dir = CASE / "05-panels"
    fixed = 0
    for panel in sorted(panel_dir.glob("panel-*")):
        if not panel.is_dir():
            continue
        panel_name = panel.name
        assign_path = panel / "assignment-index.jsonl"
        assignments = []
        if assign_path.exists():
            for line in assign_path.read_text(encoding='utf-8').splitlines():
                if line.strip():
                    assignments.append(json.loads(line))

        for assign in assignments:
            aid = assign["assignment_id"]
            role_card_id = assign["role_card_id"]
            actor_dir = panel / "private" / "actors" / aid
            turns_dir = actor_dir / "turns"

            for round_dir_name, round_num in ROUNDS:
                turn_dir = turns_dir / round_dir_name
                if not turn_dir.exists():
                    continue

                scope_file = turn_dir / "input-scope.private.json"
                view_dir = turn_dir / "scoped-view"
                manifest_file = view_dir / "view-manifest.json"

                # Build allowlist
                allowlist = [
                    "01-parse/source-content.md",
                    "02-research/claim-gate-packet.v001.json",
                    f"05-panels/{panel_name}/public-question.md",
                    f"03-role-pool/private/roles/{role_card_id}/role-card.json",
                    f"05-panels/{panel_name}/private/actors/{aid}/assignment.json",
                    f"05-panels/{panel_name}/session/public-snapshots/transcript.before-round-{round_num}.jsonl",
                ]

                scope_id = f"{panel_name.split('-')[0].upper()}-{aid}-R{round_num}"

                # Always write scope file with correct format
                scope_data = {
                    "scope_id": scope_id,
                    "allowlist": allowlist,
                }
                scope_file.write_text(json.dumps(scope_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

                # Check if manifest needs fixing
                if not needs_fix(scope_file, manifest_file):
                    continue

                # Create scoped-view directory
                if not view_dir.exists():
                    view_dir.mkdir(parents=True, exist_ok=True)

                # Build file manifest
                file_map = [
                    ("01-parse/source-content.md", "001-source-content.md"),
                    ("02-research/claim-gate-packet.v001.json", "002-claim-gate-packet.v001.json"),
                    (f"05-panels/{panel_name}/public-question.md", "003-public-question.md"),
                    (f"03-role-pool/private/roles/{role_card_id}/role-card.json", "004-role-card.json"),
                    (f"05-panels/{panel_name}/private/actors/{aid}/assignment.json", "005-assignment.json"),
                    (f"05-panels/{panel_name}/session/public-snapshots/transcript.before-round-{round_num}.jsonl", "006-transcript.before-round-{round_num}.jsonl"),
                ]

                view_files = []
                for source, view_file_name in file_map:
                    source_path = CASE / source
                    entry = {
                        "source": source,
                        "view_file": view_file_name,
                        "sha256": sha256_file(source_path),
                        "size": file_size(source_path),
                    }
                    view_files.append(entry)
                    # Copy actual file into scoped view
                    dest = view_dir / view_file_name
                    if source_path.exists():
                        shutil.copy2(str(source_path), str(dest))
                    else:
                        # Create empty file for missing sources
                        dest.write_text("", encoding="utf-8")

                manifest_data = {
                    "scope_id": scope_id,
                    "files": view_files,
                }
                manifest_file.write_text(json.dumps(manifest_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                fixed += 1

    print(f"Fixed {fixed} scoped views.")

if __name__ == "__main__":
    main()
