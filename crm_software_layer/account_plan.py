from __future__ import annotations

from dataclasses import dataclass

from .cadence import ThreadSnapshot, evaluate_cadence


@dataclass(frozen=True)
class AccountSignal:
    fit_score: float
    urgency_score: float
    relationship_depth: int
    estimated_value: int
    thread: ThreadSnapshot


@dataclass(frozen=True)
class AccountPlan:
    priority: str
    next_action: str
    review_required: bool
    projected_value_band: str
    reason: str


def build_account_plan(signal: AccountSignal) -> AccountPlan:
    cadence = evaluate_cadence(signal.thread)
    fit = _bounded(signal.fit_score)
    urgency = _bounded(signal.urgency_score)
    value_band = _value_band(signal.estimated_value)

    if cadence.state in {"DO_NOT_CONTACT", "INVALID"}:
        return AccountPlan("blocked", "do_not_contact", False, value_band, cadence.reason)

    if cadence.state == "OPERATOR_REVIEW":
        return AccountPlan("high", "operator_review", True, value_band, cadence.reason)

    if fit >= 0.75 and urgency >= 0.65 and cadence.allowed_to_message:
        return AccountPlan("high", "send_personalized_followup", False, value_band, "high fit and urgency with healthy engagement")

    if fit >= 0.55 and signal.relationship_depth >= 2:
        return AccountPlan("medium", "nurture_with_value", False, value_band, "moderate fit with existing relationship depth")

    if cadence.next_delay_hours > 0:
        return AccountPlan("low", f"wait_{cadence.next_delay_hours}_hours", False, value_band, cadence.reason)

    return AccountPlan("low", "research_before_contact", False, value_band, "insufficient deterministic buying signal")


def _bounded(value: float) -> float:
    return min(1.0, max(0.0, value))


def _value_band(value: int) -> str:
    if value >= 50000:
        return "enterprise"
    if value >= 10000:
        return "growth"
    if value > 0:
        return "starter"
    return "unknown"
