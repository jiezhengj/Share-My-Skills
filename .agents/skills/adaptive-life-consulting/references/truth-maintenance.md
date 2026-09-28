# Cross-Case Truth Maintenance

## Related Documents

Runtime entry: [`../SKILL.md`](../SKILL.md). Persistence and reopening: [`persistence.md`](persistence.md). Record schemas: [`schemas.md`](schemas.md). Evidence provenance: [`evidence-and-research.md`](evidence-and-research.md). Design rationale: [`../DESIGN.md`](../DESIGN.md).


## 1. Purpose

This protocol prevents historical memory from becoming either:

- an immutable, stale user profile;
- or a silently rewritten history.

Read this file when creating or updating cross-case memory, resolving inconsistencies, or determining whether a historical case must be reopened.

---

## 2. Canonical Cross-Case Memory

Use canonical memory only for information reasonably reusable across cases.

Recommended types:

```text
fact
experience
goal
preference
behavior
hypothesis
```

Recommendations normally remain case-local.

Possible statuses:

```text
active
superseded
retracted
disputed
expired
restricted
```

---

## 3. Core Rule

> Current canonical state may change.
> Historical material must remain traceable when it materially influenced reasoning.

Do not silently rewrite the past to make the current model appear cleaner.

---

## 4. Relationship Classification

When new evidence relates to an old record, classify before changing anything.

### confirm

New evidence supports the old record.

### refine

New evidence adds precision without changing the basic claim.

### contextualize

Both claims may be true under different scopes or conditions.

### temporal-update

The value changed over time.

### supersede

A newer record replaces the old one as the current canonical state.

### contradict

Two claims cannot both be true in the same relevant time and scope.

### invalidate

The basis for an old inference or conclusion no longer holds.

### retract

A prior record is judged erroneous and is withdrawn from active use.

---

## 5. Temporal Updates

Example:

Old:

```yaml
value: unemployed
valid_to: 2026-11-19
status: superseded
```

New:

```yaml
value: employed_full_time
valid_from: 2026-11-20
status: active
supersedes:
  - employment-status-001
```

Do not call this a contradiction.

---

## 6. Contextual Reconciliation

Example:

```yaml
type: preference
value: prefers_metro
scope:
  - dense_urban_travel
```

and:

```yaml
type: preference
value: willing_to_drive
scope:
  - suburban_travel
conditions:
  - easy_parking
```

Do not force a false binary.

---

## 7. Real Contradiction

When two claims cannot both be true in the same time and scope:

1. inspect provenance;
2. compare source reliability;
3. consider whether one is a user correction;
4. retract or dispute the weaker record;
5. preserve the history if it affected prior reasoning.

Example:

```yaml
id: driving-license-001
value: no_license
status: retracted
reason: contradicted_by_later_direct_user_statement
```

---

## 8. Hypothesis Revision

Hypotheses should carry explicit IDs where practical.

When evidence undermines one:

- `strengthened`
- `downgraded`
- `rejected`
- `superseded`

Preserve the reason.

Example:

```markdown
### H-014

Original hypothesis:
User may generally dislike competition.

Status:
rejected

Reason:
Later direct behavioral evidence contradicts the generalization.

Superseded by:
H-021 — User appears selective about forms of competition.
```

This history prevents repeated inference failure.

---

## 9. Unresolved Conflict

If available evidence cannot resolve the conflict:

```yaml
status: disputed
conflicts_with:
  - other-record-id
```

Do not manufacture certainty.

If action-sensitive, promote the conflict to `Critical Unknown`.

Possible resolution methods:

- ASK;
- RESEARCH;
- INSPECT;
- time-qualified interpretation;
- later evidence.

---

## 10. Cross-Case Retrieval

Use:

> retrieval, not preload

Historical cases are retrieved only when relevant.

Default transfer rules:

- old facts -> reusable if relevant, fresh, and uncontested;
- old experiences -> useful as historical evidence;
- old goals -> revalidate if life stage may have changed;
- old preferences -> contextual priors, not permanent laws;
- old behavior -> evidence, not destiny;
- old hypotheses -> hypothesis generators only;
- old recommendations -> do not transfer across domains.

---

## 11. Dependency Tracking

Important conclusions should reference decisive dependencies when practical.

Example:

```markdown
## Decisive Dependencies

- M:schedule-0042
- M:vision-0017
- E:competition-goal-002
- X:rule-source-008
```

Suggested prefixes:

```text
M: canonical memory
E: case evidence
H: hypothesis
X: external evidence
```

The purpose is impact analysis, not perfect database normalization.

---

## 12. Impact Analysis

Trigger when:

- important cross-case fact changes;
- high-confidence behavior record is revised;
- decisive hypothesis is invalidated;
- hard constraint changes;
- old record is retracted;
- user corrects persistent memory.

Pipeline:

```text
new evidence
    |
    v
classify relationship
    |
    v
update canonical state
    |
    v
identify dependent cases
    |
    v
estimate material impact
    |
    +--> no material effect -> annotate only
    |
    +--> material effect -> flag or reopen case
```

Do not scan and reopen every historical case after trivial changes.

---

## 13. User Notification

If new evidence materially invalidates a prior important conclusion, inform the user when appropriate.

Example:

> This new information changes a premise that the earlier career case depended on, so that case should be reconsidered rather than silently left as settled.

Do not overwhelm the user with non-material background consistency updates.

---

## 14. User Correction and Data Agency

If the user disputes a stored record:

1. inspect source and provenance;
2. distinguish correction from preference change or time change;
3. update canonical status;
4. preserve material historical provenance;
5. propagate material impact;
6. respect delete / no-reuse requests where supported.

User corrections are evidence, not merely "feedback on style."

---

## 15. Restricted / No-Reuse Records

If the user asks that information not be reused across cases, represent that restriction where supported.

Example:

```yaml
status: restricted
reuse_scope:
  - current_case_only
```

Do not retrieve restricted material into unrelated cases.

---

## 16. Historical Determinism Guard

Never reason:

> The user behaved this way once, therefore they are this kind of person forever.

Historical behavior may raise or lower hypotheses. Current evidence can always overturn it.

---

## 17. No Silent Promotion

The following transitions require explicit evidence:

```text
experience -> fact
preference -> trait
behavior -> trait
inference -> fact
hypothesis -> fact
recommendation -> goal
```

Do not perform them automatically.
