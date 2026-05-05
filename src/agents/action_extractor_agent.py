from src.util.llm_adapter import call_llm
from src.util.prompts import action_extractor_prompt

def action_extractor(notes):
    return call_llm(
        [
            {
                "role": "user",
                "content": action_extractor_prompt.format(notes=notes)
            }
        ]
    )