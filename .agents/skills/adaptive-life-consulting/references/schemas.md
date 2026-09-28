# Normative Schemas

## Related Documents

Runtime entry: [`../SKILL.md`](../SKILL.md). Persistence semantics: [`persistence.md`](persistence.md). Truth-maintenance semantics: [`truth-maintenance.md`](truth-maintenance.md). Evidence provenance: [`evidence-and-research.md`](evidence-and-research.md).


These are recommended default schemas. Host environments may implement equivalent structured state without literal Markdown/YAML files.

---

## 1. Workspace Marker

`.adaptive-life-consulting.yaml`

```yaml
schema_version: 1
protocol_version: 5
workspace_type: dedicated  # dedicated | shared
skill_name: adaptive-life-consulting
created_at: 2026-08-19
```

---

## 2. Case Index

`index.md`

```markdown
# Case Index

| Case ID | Status | Updated | Topic | Current State |
|---|---|---|---|---|
| 2026-08-19_choose-long-term-sport | awaiting-evidence | 2026-08-19 | Long-term adult sport | Awaiting real-world trials |
```

---

## 3. Case State

`case.md`

```markdown
# Case State

## Case Metadata
- Case ID:
- Internal ID:
- Created:
- Last Updated:
- Status:
- Primary Language:
- Parent Case:
- Related Cases:
- Reopened From:
- Reopen Reason:

## Current Problem

## Problem Form
- choice | open-search | diagnosis | behavior-change | planning | tradeoff | undefined

## Current Success Criteria

## Time Horizon
- Short-term:
- Long-term:
- Primary decision horizon:

## Stakeholders
- Stakeholder:
  - role:
  - directly stated preferences:
  - user inference:
  - decision rights:

## Current Best Action

## Hard Constraints

## Soft Preferences

## Confirmed Facts

## Subjective Experiences

## Goals / Values

## Behavioral Evidence

## External Reality

## Working Hypotheses

## Downgraded / Rejected Hypotheses

## Critical Unknowns

## Non-Introspectable Unknowns

## Provider-Level Questions

## Execution-Level Questions

## Experiments Pending

## Evidence Gaps

## Decisive Dependencies

## Persistence Restrictions

## Confidence
- Facts:
- Explanatory model:
- Strategic conclusion:
- Immediate next action:

## Next Information-Gathering Action

## Last Checkpoint
```

---

## 4. Conclusion

`conclusion.md` or a versioned conclusion file

```markdown
# Conclusion

## Current Problem

## Current Answer / Strategy

## Confidence
- Facts:
- Explanatory model:
- Strategic / long-term conclusion:
- Immediate next action:

## Decisive Factors

## Hard Constraints

## Supporting Behavioral Evidence

## External Reality

## Important Working Hypotheses

## Main Risks

## Remaining Critical Unknowns

## What Would Change the Conclusion

## Recommended Next Action

## Validation / Experiment Plan

## Reassessment Trigger

## Dependencies

## Decision Quality Notes

## Date
```

---

## 5. Canonical Memory Record

`memory/canonical.yaml`

```yaml
id: schedule-0042

type: fact
# fact | experience | goal | preference | behavior | hypothesis

value: "User can reliably allocate one weekend session per week."

source_cases:
  - 2026-08-19_choose-long-term-sport

source_records: []

observed_at: 2026-08-19

valid_from: 2026-08-19
valid_to: null

confidence: high
# high | medium | low

scope:
  - recurring-activities
  - sports
  - hobbies

conditions: []

stability: contextual
# stable | contextual | temporary

status: active
# active | superseded | retracted | disputed | expired | restricted

supersedes: []
conflicts_with: []

reuse_scope:
  - cross-case
# or current-case-only / restricted scopes

review_after: 2027-02-19
```

---

## 6. Evidence Record

Suggested structure inside `evidence.md`:

```markdown
### E-014

Type:
user-reported-fact

Claim:
User can only reliably protect one formal weekend session.

Source:
Direct user statement.

Observed:
2026-08-19

Scope:
recurring formal activities

Confidence:
high

Status:
active

Dependencies:
- used_by: conclusion-v1
```

Possible evidence types:

```text
user-reported-fact
subjective-experience
observed-behavior
documentary-record
external-authoritative
external-corroborated
external-weak
agent-inference
internal_prior
```

`internal_prior` is not verified evidence. It may seed hypotheses or research queries, but it must not be referenced as an external decisive dependency.

For decision-relevant external evidence, use a provenance-complete record:

```yaml
id: X-2026-09-04-001
type: external-authoritative
claim: "..."
research_action: external_tool_call
source_title: "..."
source_locator: "https://... or stable database/document identifier"
publisher: "..."
source_type: authoritative
grade: A
retrieved_at: 2026-09-04
valid_from: null
valid_to: null
supports:
  - candidate-or-hypothesis-id
does_not_support:
  - individualized-suitability
scope:
  - jurisdiction-or-market
confidence: high
review_after: 2026-10-04
status: active
```

An external evidence record is incomplete when it says only "external search" or omits the traceable source, retrieval time, supported claim, or scope.

Critical unknowns and evidence gaps may use:

```yaml
id: U-001
question: "Which locally available provider can meet the decisive constraints?"
decision_sensitivity: high
best_route: RESEARCH
status: blocked
blocked_by:
  - minimum-location-coordinate
```

---

## 7. Hypothesis Record

```markdown
### H-014

Hypothesis:
User may persist better when absence creates real responsibility toward others.

Status:
active
# active | strengthened | downgraded | rejected | superseded

Supporting Evidence:
- E-020
- E-021

Contrary Evidence:
- E-033

Confidence:
medium

Scope:
recurring group commitments
```

---

## 8. Experiment Record

`experiments.md`

```markdown
### EXP-003

Question:
Will the user remain engaged during the passive phases of a full team session?

Hypotheses:
- H-011
- H-017

Procedure:
Attend one complete realistic team session.

Do Not Substitute:
Short batting-cage session.

Observe:
- pre-departure reluctance
- attention during waiting
- desire to retry after failure
- spontaneous research afterward
- 24–48 hour physical cost

Ask Provider:
- beginner progression
- schedule expectations
- real competition path

Update Rule:
If attention remains high and voluntary curiosity appears afterward, strengthen H-011.
If passive phases produce disengagement and avoidance, strengthen H-017.

Status:
pending
```

---

## 9. Decision Log

`decision-log.md`

```markdown
# Decision Log

## 2026-08-19

Event:
Created conclusion v1.

Decisive dependencies:
- M:schedule-0042
- E:competition-goal-002

Reasoning summary:
...

## 2026-11-20

Event:
Case reopened.

Trigger:
M:schedule-0042 materially changed.

Impact:
Previous strategic conclusion may no longer hold.

Result:
Created conclusion v2.
```

---

## 10. Case Relationship Metadata

```yaml
case_id: 2026-09-15_visa-path
parent_case: 2026-09-01_move-to-japan
relation: child
related_cases:
  - 2026-09-03_job-offer
```

For merge history:

```yaml
canonical_case: 2026-09-01_move-to-japan
merged_from:
  - 2026-08-28_japan-relocation
aliases:
  - japan-move
```

---

## 11. Persistence Restriction

Example:

```yaml
record_id: relationship-0017
status: restricted
reuse_scope:
  - current-case-only
reason: user_requested_no_cross_case_reuse
```

---

## 12. Confidence Vocabulary

Recommended qualitative vocabulary:

```text
high
medium
low
unknown
```

For factual status:

```text
confirmed
probable
tentative
unknown
```

Avoid fake numerical precision unless the problem genuinely supports it.

For substantive real-world recommendations, separate at least:

```yaml
problem_understanding_confidence: high | medium | low | unknown
option_fit_confidence: high | medium | low | unknown
external_feasibility_confidence: high | medium | low | unknown
immediate_action_confidence: high | medium | low | unknown
```

`external_feasibility_confidence` cannot be high when a decisive external dependency is missing, stale, weak, or unsupported. `immediate_action_confidence` may be high for an information-rich test even while long-term option fit remains uncertain.
