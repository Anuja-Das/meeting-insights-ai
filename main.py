from src.agents.coordinator_agent import coordinator
from src.agents.synthesizer_agent import synthesizer


def generate_insights(notes: str) -> str:
    """Run the existing pipeline and return (final_output_str)."""

    hub_output = coordinator(notes)
    final_output = synthesizer(hub_output)
    return final_output


def read_notes_from_user() -> str:
    """Read multi-line notes from stdin until an empty line (or EOF)."""
    print("Enter meeting notes (finish by submitting an empty line):")
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "":
            break
        lines.append(line)
    return "\n".join(lines).strip()


if __name__ == "__main__":
    notes = read_notes_from_user()
    if not notes:
        raise SystemExit("No notes provided. Please enter at least one line of notes.")

    _hub_output, _final_output = generate_insights(notes)
    print(_final_output)
