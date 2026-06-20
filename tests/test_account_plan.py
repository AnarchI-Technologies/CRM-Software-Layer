import unittest

from crm_software_layer import AccountSignal, ThreadSnapshot, build_account_plan


class AccountPlanTests(unittest.TestCase):
    def test_blocks_opted_out_account(self):
        plan = build_account_plan(
            AccountSignal(0.9, 0.9, 5, 100000, ThreadSnapshot(1, 1, explicit_opt_out=True))
        )

        self.assertEqual(plan.priority, "blocked")
        self.assertEqual(plan.next_action, "do_not_contact")

    def test_high_fit_healthy_thread_gets_personalized_followup(self):
        plan = build_account_plan(AccountSignal(0.9, 0.8, 3, 60000, ThreadSnapshot(1, 2)))

        self.assertEqual(plan.priority, "high")
        self.assertEqual(plan.next_action, "send_personalized_followup")
        self.assertEqual(plan.projected_value_band, "enterprise")

    def test_relationship_depth_creates_medium_nurture_path(self):
        plan = build_account_plan(AccountSignal(0.6, 0.2, 2, 12000, ThreadSnapshot(0, 1)))

        self.assertEqual(plan.priority, "medium")
        self.assertEqual(plan.next_action, "nurture_with_value")
        self.assertEqual(plan.projected_value_band, "growth")

    def test_unanswered_thread_respects_wait_state(self):
        plan = build_account_plan(AccountSignal(0.8, 0.8, 1, 2500, ThreadSnapshot(2, 0)))

        self.assertEqual(plan.priority, "low")
        self.assertEqual(plan.next_action, "wait_144_hours")


if __name__ == "__main__":
    unittest.main()
