"""Defensive policy lab. Synthetic records; no network, shell or file tools."""
from dataclasses import dataclass
from html import escape


class DeniedAction(Exception):
    pass


@dataclass(frozen=True)
class Scope:
    # Created by the trusted application after authenticating the user.
    document_id: str
    max_calls: int = 3

    def __post_init__(self):
        if self.document_id not in {"report", "notes"}:
            raise ValueError("Unknown document")
        if type(self.max_calls) is not int or not 1 <= self.max_calls <= 100:
            raise ValueError("Invalid budget")


class GuardedSession:
    def __init__(self, scope: Scope):
        self.scope = scope
        self.attempts = 0
        self.completed = 0
        self._records = {"report": "Synthetic report: green", "notes": "Synthetic notes"}

    def read(self, proposal):
        # Count rejected attempts as well, preventing unlimited retries.
        if self.attempts >= self.scope.max_calls:
            raise DeniedAction("Budget exhausted")
        self.attempts += 1
        if type(proposal) is not dict or set(proposal) != {"tool", "document_id"}:
            raise DeniedAction("Invalid schema")
        if type(proposal["tool"]) is not str or proposal["tool"] != "read_document":
            raise DeniedAction("Tool not permitted")
        if type(proposal["document_id"]) is not str:
            raise DeniedAction("Invalid document ID")
        if proposal["document_id"] != self.scope.document_id:
            raise DeniedAction("Document outside scope")
        self.completed += 1
        return self._records[proposal["document_id"]]


def render_text(text):
    """Only for HTML text nodes, not JS, CSS, URLs or raw HTML attributes."""
    if type(text) is not str or len(text) > 4096:
        raise DeniedAction("Invalid output size or type")
    return "<pre>" + escape(text, quote=True) + "</pre>"


if __name__ == "__main__":
    session = GuardedSession(Scope("report", max_calls=2))
    print(session.read({"tool": "read_document", "document_id": "report"}))
    try:
        session.read({"tool": "read_document", "document_id": "notes"})
    except DeniedAction as error:
        print("DENIED:", error)
    print(render_text("Synthetic model output: <example>"))
