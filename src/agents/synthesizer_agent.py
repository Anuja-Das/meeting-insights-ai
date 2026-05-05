from src.util.llm_adapter import call_llm
from src.util.prompts import synthesizer_prompt

def synthesizer(data):
    return call_llm(
        [
            {
                "role": "user",
                "content": synthesizer_prompt.format(data=data)
            }
        ]
    )