# Persistence, Workspace, and Case Lifecycle

## Related Documents

Runtime entry: [`../SKILL.md`](../SKILL.md). Schemas: [`schemas.md`](schemas.md). Cross-case updates: [`truth-maintenance.md`](truth-maintenance.md). Design rationale: [`../DESIGN.md`](../DESIGN.md).


## 1. Scope

Read this reference when:

- discovering or initializing a workspace;
- creating, resuming, reopening, closing, splitting, linking, or merging cases;
- versioning conclusions;
- recovering after a lost chat session;
- migrating persistent schemas.

---

## 2. Consulting Root Discovery

Use logical variable:

```text
CONSULTING_ROOT
```

Discovery order:

1. If current directory or appropriate ancestor contains `.adaptive-life-consulting.yaml`, use that directory.
2. If the user explicitly states the current project is dedicated to this skill, use the current directory.
3. If the current directory already contains a clearly compatible `index.md`, `cases/`, and `memory/`, treat it as an existing root.
4. If the current project is shared with unrelated work and no consulting root exists, create `life-consulting/`.
5. Never create nested `life-consulting/life-consulting/`.

The marker records whether the workspace is `dedicated` or `shared`.

---

## 3. Recommended Workspace

```text
CONSULTING_ROOT/
├── .adaptive-life-consulting.yaml
├── index.md
├── cases/
│   └── YYYY-MM-DD_topic/
│       ├── case.md
│       ├── conclusion.md
│       ├── conclusions/
│       ├── evidence.md
│       ├── experiments.md
│       ├── decision-log.md
│       └── archive/
└── memory/
    ├── canonical.yaml
    ├── conflict-log.md
    └── archive/
```

Create only files justified by the case.

A simple case may need only:

```text
case.md
conclusion.md
```

---

## 4. Case Identity

Recommended human-readable ID:

```text
YYYY-MM-DD_<short-kebab-case-topic>
```

Examples:

```text
2026-08-19_choose-long-term-sport
2026-10-12_sleep-routine-breakdown
```

An internal UUID may coexist with the human-readable ID.

---

## 5. Case Relationship Classification

Before acting on a historically similar topic, classify:

### new-case

A genuinely new problem.

### resume

The same active or paused case continues without a material break in problem identity.

### reopen

A previously closed or awaiting-evidence case becomes active because new evidence or changed circumstances may alter the model.

### related-new-case

A new problem is related to old cases but should preserve its own identity.

Do not merge merely because titles or keywords are similar.

---

## 6. Case Status

Allowed default statuses:

```text
active
paused
awaiting-evidence
closed
reopened
superseded
```

### active

Currently under investigation.

### paused

Temporarily stopped; continuation does not require a specific external event.

### awaiting-evidence

Next useful progress depends on an experiment, external event, assessment, or future observation.

### closed

Current phase has a sufficiently actionable answer.

### reopened

A closed / paused case is active again due to material new evidence.

### superseded

The whole case framing has been replaced. Use sparingly.

---

## 7. Resume Protocol

When the user wants to continue old work:

1. Discover `CONSULTING_ROOT`.
2. Read `index.md`.
3. Resolve target case by explicit ID, topic, recent matching case, and status.
4. Read `case.md`.
5. Read current `conclusion.md`.
6. Read only supporting artifacts needed for the current frontier.
7. Reconstruct:
   - current problem;
   - success criteria;
   - current best action;
   - decisive factors;
   - pending unknowns;
   - pending experiments;
   - last conclusion;
   - last checkpoint.
8. Continue from the current frontier.
9. Do not re-ask known information unless it may be stale or disputed.

Raw transcript should be consulted only for targeted historical verification, not automatically.

---

## 8. Recovery Limits

If the workspace is deleted and no durable host memory or backup exists, recovery is impossible.

The skill must not imply otherwise.

For durable deployments, storage may be backed by:

- version control;
- synchronized storage;
- backups;
- another durable persistence layer.

---

## 9. When to Persist

Persist a case when any of these apply:

- many turns;
- likely cross-session continuation;
- substantial external research;
- multiple competing hypotheses;
- future real-world experiments;
- likely reopening;
- recommendation depends on accumulated reasoning.

Short, low-stakes, one-shot problems may remain ephemeral.

The user may explicitly request no persistence.

---

## 10. Case State Updates

Update `case.md` after meaningful state changes:

- new confirmed fact;
- new hard constraint;
- success criterion change;
- hypothesis creation / strengthening / downgrade / rejection;
- important external evidence;
- critical unknown resolution;
- question converted to experiment;
- current best action change;
- checkpoint;
- close / pause / reopen;
- material cross-case impact.

Do not rewrite it after every trivial utterance.

---

## 11. Current vs Historical Files

### Mutable

- `case.md`
- `conclusion.md`
- `index.md`
- canonical active memory

### Historical / append-only or superseded

- old evidence records;
- conclusion versions;
- decision-log entries;
- conflict-log entries.

Material history should not disappear.

---

## 12. Conclusion Versioning

For stable one-shot cases, `conclusion.md` may be sufficient.

For reopened or materially revised cases:

```text
conclusions/
├── 2026-08-19_v1.md
├── 2026-11-20_v2.md
└── ...
```

`conclusion.md` should represent the current synthesis or pointer.

Historical versions should remain intact except for non-destructive metadata such as `superseded_by`.

---

## 13. Decision Log

Use for evolving or high-value cases.

Record:

- date;
- decision / conclusion version;
- decisive evidence;
- what changed;
- why the model changed;
- which version superseded which.

The log should make retrospective reasoning reconstructable.

---

## 14. Split Child Case

Consider splitting when a subproblem develops:

- independent success criteria;
- distinct stakeholders;
- different time horizon;
- its own research;
- its own experiments;
- its own closure conditions.

Record parent relation.

Example metadata:

```yaml
parent_case: 2026-09-01_move-to-japan
relation: child
```

Do not copy the entire parent case. Reference relevant dependencies.

---

## 15. Merge / Link Cases

If two cases later prove to represent the same underlying problem:

- preserve both original IDs;
- choose or create a canonical case;
- record aliases / merged-from relations;
- preserve historical artifacts;
- update index.

Do not silently delete one case.

---

## 16. Closure

At closure or pause:

1. update case state;
2. set status;
3. update current conclusion;
4. create a conclusion version if materially important;
5. record decisive factors;
6. record remaining unknowns;
7. record reversal conditions;
8. record next action;
9. record reopening trigger;
10. update index.

---

## 17. Reopening

When reopening:

1. read latest state;
2. read current conclusion;
3. identify new evidence or changed constraint;
4. inspect only relevant history;
5. update affected model components;
6. run a checkpoint;
7. version a materially changed conclusion;
8. update decision log;
9. update index.

Do not restart the interview from zero.
