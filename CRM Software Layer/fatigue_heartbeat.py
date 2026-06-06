class LeadFatigueController:
    """Manages chat thread heartbeat signals to prevent system lead bombardment."""
    def evaluate_thread(self, bot_msg_count: int, user_msg_count: int) -> str:
        if bot_msg_count >= 3 and user_msg_count == 0:
            return "COOLDOWN_LOW_PRESSURE"
        if user_msg_count == 0:
            return "COOLDOWN_PASSIVE"
        return "ACTIVE_ENGAGEMENT"

    def calculate_backoff_interval(self, state: str) -> int:
        intervals = {"ACTIVE_ENGAGEMENT": 6, "COOLDOWN_LOW_PRESSURE": 72, "COOLDOWN_PASSIVE": 144}
        return intervals.get(state, 24)
