"""Second process for T-RESTART. Starts a wait, then exits. This is not an OS kill."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "context-lake") not in sys.path:
    sys.path.insert(0, str(ROOT / "context-lake"))

os.environ["MODEL_MODE"] = "replay"
os.environ["APP_A_CHECKPOINT_PATH"] = sys.argv[1]
os.environ["APP_A_AUDIT_PATH"] = sys.argv[2]

from apps.app_a.agent.checkpointer import new_saver  # noqa: E402
from apps.app_a.agent.graph import is_waiting, run_agent  # noqa: E402
from apps.app_a.store import reset_runtime  # noqa: E402

corr = sys.argv[3]
case_id = sys.argv[4]
reset_runtime()
conn, saver = new_saver(Path(sys.argv[1]))
result = run_agent(
    {
        "correlation_id": corr,
        "thread_id": corr,
        "case_id": case_id,
        "actor_id": "demo-rt01-1",
        "actor_role": "RT-01",
        "scenario": "SP-08",
        "proposed_action": "",
        "step_count": 0,
        "tool_call_count": 0,
        "gather_visits": 0,
        "budget_exhausted": False,
        "citations": [],
        "untrusted_quotes": [],
        "lake_item_ids": [],
        "draft_plan": "",
        "sentence": "",
        "verdict": "",
        "opa_verdict": "",
        "block": False,
        "record_change": False,
        "waiting_role": "",
        "proposed_by": "model_draft",
        "human_decision": "",
        "human_action_type": "",
        "human_actor_id": "",
        "human_actor_role": "",
        "error_class": "",
    },
    checkpointer=saver,
)
from apps.app_a.agent.graph import get_graph  # noqa: E402

graph = get_graph(saver)
waiting = is_waiting(graph, corr)
print(json.dumps({"waiting": waiting, "opa_verdict": (result.get("state") or {}).get("opa_verdict")}))
conn.close()
sys.exit(0 if waiting else 2)
