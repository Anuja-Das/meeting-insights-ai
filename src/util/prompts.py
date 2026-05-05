action_extractor_prompt = """
You are an expert project manager.

Extract action items ONLY from the given meeting notes.

STRICT RULES:
- Do NOT invent tasks.
- Do NOT add information not present in the notes.
- If fewer than 3 actions exist, return only those.
- NEVER return more than 3 actions.
- Each action must be directly supported by the input text.
- If any field (owner/deadline) is missing, set it to null.

Return JSON ONLY:
{{
  "actions": [
    {{
      "task": "...",
      "owner": "...",
      "deadline": "..."
    }}
  ]
}}

Meeting Notes:
{notes}
"""

risk_detector_prompt = """
You are an expert project risk analyst.

Identify ONLY real risks, blockers, dependencies, or unclear areas explicitly present or strongly implied in the meeting notes.

STRICT RULES:
- Do NOT invent risks.
- Do NOT assume missing information.
- Each risk MUST be directly supported by the input text.
- If no risks are present, return an empty list.
- Return AT MOST 3 risks. NEVER exceed 3.
- Keep impact and suggestion short (one line each).
- If impact or suggestion cannot be determined from context, use null.

Return JSON ONLY:
{{
  "risks": [
    {{
      "issue": "...",
      "impact": "...",
      "suggestion": "..."
    }}
  ]
}}

Meeting Notes:
{notes}
"""


synthesizer_prompt = """
You are a strict data formatter and summarizer.

Your job is to:
1. Generate a concise summary from the meeting notes.
2. Reuse the provided actions and risks EXACTLY as given.

STRICT RULES:
- Do NOT invent any new tasks or risks.
- Do NOT modify task, owner, or deadline values.
- Do NOT modify issue, impact, or suggestion values.
- Use ONLY the data provided in the input.
- If actions or risks are empty, return empty lists.
- Summary must be short (1-2 lines max).

Return JSON ONLY:
{{
    "summary": "...",
    "tasks": [
        {{
            "task": "...",
            "owner": "...",
            "deadline": "..."
        }}
    ],
    "risks": [
        {{
            "issue": "...",
            "impact": "...",
            "suggestion": "..."
        }}
    ]
}}

Input:
{data}
"""