import random
import unittest
from lab import DeniedAction, GuardedSession, Scope, render_text


class PolicyTests(unittest.TestCase):
    def test_selected_record_is_allowed(self):
        session = GuardedSession(Scope("report"))
        self.assertEqual(session.read({"tool": "read_document", "document_id": "report"}), "Synthetic report: green")
        self.assertEqual(session.completed, 1)

    def test_other_record_is_denied_without_completed_action(self):
        session = GuardedSession(Scope("report"))
        with self.assertRaises(DeniedAction):
            session.read({"tool": "read_document", "document_id": "notes"})
        self.assertEqual(session.completed, 0)

    def test_unknown_tool_is_denied(self):
        with self.assertRaises(DeniedAction):
            GuardedSession(Scope("report")).read({"tool": "unknown", "document_id": "report"})

    def test_extra_authority_field_is_denied(self):
        with self.assertRaises(DeniedAction):
            GuardedSession(Scope("report")).read({"tool": "read_document", "document_id": "report", "approved": True})

    def test_invalid_requests_consume_budget(self):
        session = GuardedSession(Scope("report", 1))
        with self.assertRaises(DeniedAction):
            session.read(None)
        with self.assertRaisesRegex(DeniedAction, "Budget"):
            session.read({"tool": "read_document", "document_id": "report"})
        self.assertEqual(session.completed, 0)

    def test_successful_requests_consume_budget(self):
        session = GuardedSession(Scope("report", 1))
        request = {"tool": "read_document", "document_id": "report"}
        session.read(request)
        with self.assertRaises(DeniedAction):
            session.read(request)

    def test_output_is_escaped(self):
        self.assertEqual(render_text('<example> & "quoted"'), '<pre>&lt;example&gt; &amp; &quot;quoted&quot;</pre>')

    def test_output_limits(self):
        for value in [None, {}, "a" * 4097]:
            with self.assertRaises(DeniedAction):
                render_text(value)
        self.assertEqual(len(render_text("a" * 4096)), 4107)

    def test_invalid_scope(self):
        for budget in [0, -1, True, 101, "3"]:
            with self.assertRaises(ValueError):
                Scope("report", budget)

    def test_seeded_policy_fuzz(self):
        # Fixed seed, fixed corpus and finite count: reproducible policy testing.
        rng = random.Random(20251001)
        values = [None, False, 0, [], {}, "", "notes", "report", "read_document", "unknown"]
        accepted = rejected = 0
        for index in range(2000):
            proposal = {"tool": rng.choice(values), "document_id": rng.choice(values)}
            if index % 7 == 0:
                proposal["extra"] = True
            if index % 11 == 0:
                proposal = rng.choice(values)
            expected = proposal == {"tool": "read_document", "document_id": "report"}
            session = GuardedSession(Scope("report"))
            try:
                result = session.read(proposal)
            except DeniedAction:
                self.assertFalse(expected)
                self.assertEqual(session.completed, 0)
                rejected += 1
            else:
                self.assertTrue(expected)
                self.assertEqual(result, "Synthetic report: green")
                accepted += 1
        self.assertGreater(accepted, 0)
        self.assertGreater(rejected, 0)


if __name__ == "__main__":
    unittest.main()
