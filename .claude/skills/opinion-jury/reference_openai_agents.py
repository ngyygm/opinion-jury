"""Reference orchestration skeleton for opinion-jury.

Host-controlled persistence is mandatory. Do not collapse role generation,
debate, adjudication, and replay into one prompt. Expose only the scoped view.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json

@dataclass
class ActorRun:
    assignment_id: str
    round_no: int
    phase: str
    scoped_view: Path

def call_agent(agent_name: str, scoped_view: Path) -> dict:
    raise NotImplementedError("Bind to your runtime. Expose scoped_view only.")

def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def run_actor_turn(run: ActorRun, turn_dir: Path) -> dict:
    """Persist structured private state, public speech, and private metadata separately."""
    result = call_agent("behavioral_actor", run.scoped_view)
    think = result["think_private_structured"]   # concise state, not raw chain-of-thought
    say = result["say_public"]                   # peer-visible only
    metadata = result["filing_metadata_private"] # never peer-visible
    write_json(turn_dir / "think.private.json", think)
    write_json(turn_dir / "say.public.json", say)
    (turn_dir / "say.public.md").write_text(say["speech_text"] + "\n", encoding="utf-8")
    write_json(turn_dir / "filing-metadata.private.json", metadata)
    fidelity = call_agent("behavior_fidelity_guard", run.scoped_view)
    write_json(turn_dir / "behavior-fidelity.private.json", fidelity)
    if not fidelity.get("admit_to_public_record"):
        raise RuntimeError("candidate public filing rejected by behavior fidelity guard")
    return say

def append_public_transcript(transcript_path: Path, say: dict) -> None:
    """Append only the public filing. Never append private metadata."""
    with transcript_path.open("a", encoding="utf-8") as h:
        h.write(json.dumps(say, ensure_ascii=False) + "\n")

def run_terminal_blind_adjudication(scoped_view: Path, verdict_path: Path) -> None:
    verdict = call_agent("terminal_blind_adjudicator", scoped_view)
    write_json(verdict_path, verdict)

def run_private_full_replay(scoped_view: Path, output_path: Path) -> None:
    replay = call_agent("private_full_replay_analyst", scoped_view)
    write_json(output_path, replay)
