# CRM Software Layer

Consent-aware CRM cadence primitives for AnarchI Technologies.

Hardcoding freedom into the systems of tomorrow.

## Purpose

CRM Software Layer provides deterministic relationship cadence controls. It helps decide when to engage, wait, stop, or route to operator review without exposing private contact data or encouraging noisy automation.

## What Changed

- Replaced the thin fatigue heartbeat file with a tested CRM cadence package.
- Added explicit opt-out handling.
- Added conservative cooldown behavior for unanswered outbound messages.
- Added human review routing for high-value context.

## Structure

```text
.
|-- crm_software_layer/
|   |-- __init__.py
|   `-- cadence.py
|-- tests/
|   `-- test_cadence.py
`-- README.md
```

## Verify

```bash
python -m unittest discover -s tests -q
```

## Public Safety

Do not commit contact lists, private messages, customer records, credentials, live CRM exports, or automated outreach flows that bypass consent and review.
