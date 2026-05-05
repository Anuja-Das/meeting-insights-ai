import json

from src.agents.risk_detector_agent import risk_detector
from src.agents.action_extractor_agent import action_extractor


def coordinator(notes):
    actions_raw = action_extractor(notes)
    risks_raw = risk_detector(notes)

    actions = json.loads(actions_raw)
    risks = json.loads(risks_raw)

    return {
        "notes": notes,
        "actions": actions.get("actions", []),
        "risks": risks.get("risks", [])
    }