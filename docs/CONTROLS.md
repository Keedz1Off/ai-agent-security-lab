# Control walkthroughs

Each example pairs a failure mode with a defensive code location and an observable test. Inputs are local synthetic proposals; they do not exploit a model or service.

## 1. Untrusted content and excessive tool authority

**Failure mode:** an application treats a model's proposed action as permission. External text can influence model output; therefore a fluent explanation or a claimed approval inside that output must not expand access.

**Invariant:** only the exact read tool is available for this task, with exactly two fields. Authority comes from the application's Scope, never from proposal metadata.

**Control:** `GuardedSession.read` rejects unknown tools and unexpected fields before completing an action.

```python
session = GuardedSession(Scope("report"))
result = session.read({"tool": "read_document", "document_id": "report"})
```

**Evidence:** `test_unknown_tool_is_denied`, `test_extra_authority_field_is_denied`. Denial raises `DeniedAction`. This is downstream containment, not prompt-injection detection or a stronger system prompt.

## 2. Access to data outside the selected scope

**Failure mode:** the model chooses which record it may read. Valid record names alone do not establish authorization.

**Invariant:** the requested document ID equals the trusted user's selection. A second valid record is still unauthorized for this session.

**Control:** equality against `Scope.document_id`; opaque IDs avoid accepting arbitrary file paths.

**Evidence:** `test_selected_record_is_allowed` and `test_other_record_is_denied_without_completed_action` verify both useful access and rejection. The completed-action counter remains zero on rejection. Production retrieval needs the same authorization before fetching chunks or building a model context; this demo does not implement a vector database.

## 3. Model output entering an HTML page

**Failure mode:** treating generated text as trusted markup can change how a page is rendered.

**Invariant:** text is displayed as text, with a fixed wrapper and no executable interpretation.

**Control:** `render_text` uses Python's HTML escaping after enforcing a type and length limit.

```python
render_text("Example: <label> & details")
# <pre>Example: &lt;label&gt; &amp; details</pre>
```

**Evidence:** `test_output_is_escaped`, `test_output_limits`. Do not reuse this encoder for JavaScript, CSS or URL contexts. Real frontends should prefer textContent or framework autoescaping.

## 4. Repeated tool proposals and resource budgets

**Failure mode:** a retry loop keeps trying after a rejected proposal, consuming resources indefinitely.

**Invariant:** attempts never exceed the trusted session budget; rejections consume that budget too.

**Control:** budget check and increment happen before proposal validation.

**Evidence:** tests exercise exhaustion after both valid and invalid calls. This single-process session counter needs atomic shared storage in a concurrent deployment. It does not limit model token usage, wall-clock time or provider charges.
