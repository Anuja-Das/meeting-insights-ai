from src.util.llm_adapter import call_llm
from src.util.prompts import risk_detector_prompt

def risk_detector(notes):
    return call_llm(
        [
            {
                "role": "user",
                "content": risk_detector_prompt.format(notes=notes)
            }
        ]
    )