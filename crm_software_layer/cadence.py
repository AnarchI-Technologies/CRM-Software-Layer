from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ThreadSnapshot:
    outbound_count: int
    inbound_count: int
    explicit_opt_out: bool = False
    high_value_context: bool = False


@dataclass(frozen=True)
class CadenceDecision:
    state: str
    next_delay_hours: int
    allowed_to_message: bool
    reason: str


def evaluate_cadence(snapshot: ThreadSnapshot) -> CadenceDecision:
    if snapshot.outbound_count < 0 or snapshot.inbound_count < 0:
        return CadenceDecision("INVALID", 0, False, "message counts cannot be negative")

    if snapshot.explicit_opt_out:
        return CadenceDecision("DO_NOT_CONTACT", 0, False, "explicit opt-out takes priority")

    if snapshot.inbound_count == 0 and snapshot.outbound_count >= 3:
        return CadenceDecision("COOLDOWN_LOW_PRESSURE", 72, False, "multiple outbound attempts without response")

    if snapshot.inbound_count == 0:
        return CadenceDecision("COOLDOWN_PASSIVE", 144, False, "no inbound signal yet")

    if snapshot.high_value_context:
        return CadenceDecision("OPERATOR_REVIEW", 24, False, "high-value context should be reviewed by a person")

    return CadenceDecision("ACTIVE_ENGAGEMENT", 6, True, "healthy two-way engagement")

