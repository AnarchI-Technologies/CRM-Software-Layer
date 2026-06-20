import unittest

from crm_software_layer import ThreadSnapshot, evaluate_cadence


class CadenceTests(unittest.TestCase):
    def test_blocks_explicit_opt_out(self):
        decision = evaluate_cadence(ThreadSnapshot(1, 1, explicit_opt_out=True))

        self.assertEqual(decision.state, "DO_NOT_CONTACT")
        self.assertFalse(decision.allowed_to_message)

    def test_cools_down_after_unanswered_outbound_messages(self):
        decision = evaluate_cadence(ThreadSnapshot(3, 0))

        self.assertEqual(decision.state, "COOLDOWN_LOW_PRESSURE")
        self.assertEqual(decision.next_delay_hours, 72)

    def test_allows_healthy_two_way_engagement(self):
        decision = evaluate_cadence(ThreadSnapshot(1, 2))

        self.assertEqual(decision.state, "ACTIVE_ENGAGEMENT")
        self.assertTrue(decision.allowed_to_message)


if __name__ == "__main__":
    unittest.main()

