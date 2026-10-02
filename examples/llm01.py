"""LLM01: untrusted report.txt must stay data, not become a command."""
from pathlib import Path


def tool(action: str) -> None:
    """Harmless teaching stub: this only prints and does not do real work."""
    print("TOOL WOULD RUN:", action)


report_path = Path(__file__).with_name("data") / "report.txt"
report = report_path.read_text(encoding="utf-8")

print("1. Vulnerable version")
if "TOOL:" in report:
    tool(report.split("TOOL:", 1)[1].strip())

print("\n2. Protected version")
user_task = "summarize"
if user_task == "summarize":
    print("REPORT AS TEXT:", report)
else:
    print("STOP: task is not permitted")

print("\nThe report cannot choose a tool. The application checks user_task.")
