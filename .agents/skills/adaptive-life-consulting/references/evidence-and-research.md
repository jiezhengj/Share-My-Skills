# Evidence and Research Protocol

## Related Documents

Runtime entry: [`../SKILL.md`](../SKILL.md). Interview and experiment routing: [`interviewing-and-experiments.md`](interviewing-and-experiments.md). Schemas: [`schemas.md`](schemas.md). Cross-case evidence updates: [`truth-maintenance.md`](truth-maintenance.md).


## 1. Evidence Routing

For every important unknown choose among:

```text
ASK
RESEARCH
INSPECT
INFER
TEST
```

The source should be selected by reliability and decision relevance, not habit.

Before selecting a route, discover latent dependencies. Ask what location, time, market, provider, eligibility, professional-standard, or safety fact must be true for the eventual action to work, even if the user has not mentioned it.

---

## 2. ASK

Ask the user when:

- the information is private, experiential, or value-based;
- the user can likely answer;
- different answers matter;
- the question does not ask for unreliable prediction.

Before asking, verify that RESEARCH, INSPECT, or TEST would not produce more reliable evidence. The user should not have to identify an externally checkable dependency before the Agent investigates it.

Good examples:

- What time can you realistically protect every week?
- What happened the last time you tried something similar?
- Would the project still matter if competition were impossible?

Poor examples:

- Guess the current local price.
- Predict whether you will enjoy a type of experience you have never had.

---

## 3. RESEARCH

RESEARCH is an observable external action, not an internal reasoning style. It requires all of the following:

1. Invoke an available external search, browser, database, map, or authoritative-document tool.
2. Read the returned source rather than relying only on a generated recollection or an unopened search snippet.
3. Preserve a traceable source identifier and retrieval date.
4. Record the claim the source supports, its grade, its scope, and important limitations.
5. Integrate the result into the decision model.

Model recall, unsourced domain knowledge, invented citations, suggested queries, or a phrase such as "research shows" do not satisfy this definition. Classify them as `internal_prior` or `agent-inference`; use them only to generate hypotheses, candidates, and searches.

Research when the answer exists externally, when current reality may change feasibility, when exploring solutions beyond internal memory biases, or when developing deeper hypotheses about domain mechanisms. The user does not need to request search explicitly.

Four operational tracks:

### A. Fact Verification Track
- current local resources;
- current prices and operational schedules;
- laws, regulations, and institutional eligibility;
- provider status and transit constraints;
- medical or professional standards.

### B. Solution Exploration & Reality Calibration Track
- discovering candidates beyond the Agent's default static memory (e.g. recent releases, modern translations, niche or cross-domain options);
- verifying real-world community feedback, friction points, and common drop-out / failure modes for candidate options;
- uncovering alternative perspectives and counter-intuitive paths.

For open search, diversify the initial pool across materially different participation or delivery mechanisms rather than merely collecting the highest-ranked or most familiar categories. Stop broad scanning once additional mechanisms no longer change the questions or candidate structure.

### C. Cognitive Fuel & Mechanism Discovery Track
- searching domain reports, sociological analyses, or community retrospectives to understand why certain setups, group formats, or structures succeed or fail for specific behavioral habits;
- breaking superficial stereotypes to enrich the Agent's conceptual depth, formulate non-obvious hypotheses, and design insightful indirect probing inquiries.

### D. Action Verification Track

- confirm that a candidate currently exists and is accessible;
- distinguish category-level appeal from provider-level delivery;
- verify current schedule, price, eligibility, enrollment path, and operating status where decision-sensitive;
- identify what must still be confirmed directly with a provider or qualified professional.

### Proactive Research Triggers

Default to external research before making a substantive recommendation when any of these could change the option set, ranking, risk, or execution:

- locality, travel radius, or current availability;
- provider quality or delivery format;
- prices, schedules, laws, rules, or professional standards;
- health, safety, legal, or major financial exposure;
- recent developments, niche candidates, or common real-world failure modes;
- a recommendation that would consume meaningful time, money, or bodily risk.

If a required coordinate is private, ask for the minimum useful granularity. While waiting, continue coordinate-independent research when it can reduce uncertainty.

### Tool Failure and Unavailable Research

When external tools are unavailable, blocked, or fail:

- do not claim that research occurred;
- preserve relevant content as `internal_prior` or an unverified hypothesis;
- lower confidence and expose the unresolved dependency when material;
- route to a later verification action rather than silently substituting model recall.

---

## 4. INSPECT

Prefer actual records or behavior when they provide stronger evidence.

Possible sources:

- prior case artifacts;
- calendars;
- files;
- logs;
- historical actions;
- records of attendance;
- budgets;
- application history;
- purchase history;
- other user-provided evidence.

Use the least intrusive source sufficient for the question.

---

## 5. INFER

Inference is appropriate when:

- existing evidence already supports a useful working model;
- another question has low marginal value;
- the inference can remain explicitly tentative.

Do not write inference as a confirmed user fact.

---

## 6. TEST

Use reality when prediction is unreliable and a safe, reversible experiment is available.

Experiment design details are in `interviewing-and-experiments.md`.

---

## 7. Evidence Hierarchy

Default weighting:

### Tier 1 — Hard Constraints and Direct Reality

- safety;
- health;
- law;
- money;
- time;
- geography;
- eligibility;
- deadlines.

### Tier 2 — Observed Behavior

- sustained behavior;
- repeated failures;
- voluntary return;
- behavior under comparable conditions.

### Tier 3 — Environment and Opportunity Structure

- local resources;
- provider quality;
- cost;
- schedule;
- transport;
- institutional structure;
- market conditions.

### Tier 4 — Repeated Preferences and Motivational Patterns

Useful but contextual.

### Tier 5 — Analogies and Interpretive Clues

Games, fiction, aesthetics, identity cues.

Primarily hypothesis generators.

### Tier 6 — Generic Population Research

Useful for plausibility, broad risk, and known mechanisms.

Do not let Tier 6 create false individual precision.

---

## 8. Source Grades

### Grade A

Current authoritative or first-party evidence.

Examples:

- regulation;
- official current schedule;
- official event registration;
- authoritative medical guideline.

### Grade B

Recent, independently corroborated evidence.

Examples:

- active official social page plus independent listing;
- recent local journalism plus first-party confirmation.

### Grade C

Aggregators, generic estimates, stale operating pages.

Use cautiously and label uncertainty.

### Grade D

Unverified comments, isolated anecdotes, obsolete claims.

Use only as leads unless the task specifically concerns subjective community experience.

---

## 9. Local Reality

For local services or institutions, where practical combine:

- official site;
- current maps / business listing;
- active social media;
- recent event records;
- reviews;
- community discussions;
- local journalism;
- regulatory or institutional source.

Do not equate "search result exists" with "provider is suitable."

Separate:

- existence;
- current operation;
- actual price;
- schedule;
- quality;
- fit;
- progression pathway.

Acquire only the minimum location precision required by decision sensitivity. Depending on the problem this may be a country, city, district, transit stop, travel-time radius, or no location at all. Never turn location into a universal intake field.

Location unlocks supply discovery; it does not by itself prove feasibility. Until decision-sensitive schedule, travel tolerance, budget, eligibility, and delivery-format constraints are known, local results remain a pool for further investigation rather than a ranked sustainable recommendation.

Where practical, verify local supply across distinct questions:

- existence;
- current operation;
- current offering;
- beginner eligibility;
- delivery format;
- price and schedule;
- access and transport;
- quality signals;
- fit with the user's decisive constraints.

---

## 10. Provenance

Important evidence should preserve where practical:

- record ID;
- source;
- date observed;
- valid time;
- source type;
- confidence;
- scope;
- whether direct or inferred;
- freshness / review date;
- case(s) using it.

A decision-relevant external record should minimally identify:

```yaml
id: X-...
claim: ...
research_action: external_tool_call
source_title: ...
source_locator: ...
publisher: ...
source_type: first-party | authoritative | independent | community | aggregator
grade: A | B | C | D
retrieved_at: YYYY-MM-DD
supports: [...]
does_not_support: [...]
scope: [...]
confidence: low | medium | high
review_after: YYYY-MM-DD | null
```

"Source: external search" without a traceable locator, date, and supported claim is not provenance.

---

## 11. Freshness

Recheck facts that naturally become stale.

Examples:

- prices;
- schedules;
- operating status;
- job status;
- relationship status;
- health status;
- laws;
- service availability;
- commute conditions.

A previously true fact may become historical rather than "wrong."

---

## 12. High-Stakes Evidence

When health, safety, law, finance, or other high-stakes constraints may dominate:

- identify them early;
- prefer authoritative sources;
- separate general standards from individualized professional evaluation;
- do not overstate unverified rules;
- distinguish:
  - an organization may allow something;
  - it is professionally or medically appropriate.

Professional evaluation may itself be an information-gathering action.

Do not infer individualized medical safety, legal classification, personal financial suitability, or real-world self-defense effectiveness solely from a general source or internal prior. General authoritative guidance may identify risks and useful questions; individualized conclusions require evidence appropriate to that individual and jurisdiction.

---

## 13. Generic Research Guard

A research paper saying a variable matters in a population does not prove that the variable explains this user.

Use research to say:

> This mechanism is plausible and worth considering.

Not:

> This is definitely why you behave this way.

---

## 14. Research Stop Rule

Stop research when:

- the candidate pool is sufficiently diverse, recent, and grounded;
- decisive external constraints and common failure modes have been checked;
- remaining uncertainty is private to the user or better tested in reality;
- additional sources only repeat the same high-frequency consensus.

More sources do not automatically mean more confidence.


## 15. Research Integration Check

After each meaningful research pass, identify at least one concrete update:

- add, remove, or reorder a candidate;
- strengthen, weaken, or reject a hypothesis;
- expose a constraint or unresolved dependency;
- revise a confidence level;
- improve the next atomic question;
- route an uncertainty to INSPECT, ASK, professional evaluation, or TEST.

If the research changes nothing and new sources repeat the same evidence, stop. Citations added after an unchanged answer are decoration, not integrated research.


## 16. External Reality Admission Gate

Admit a claim to `External Reality` only when it is:

- a traceable external observation with adequate provenance; or
- a clearly labeled direct user report about the user's world.

Do not admit internal priors, agent inferences, hypotheses, recommendations, source extrapolations, or provider marketing claims beyond what they directly establish. A decisive dependency cannot support high confidence while its source is missing, stale, weak, or narrower than the conclusion.
