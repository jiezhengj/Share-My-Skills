# Adaptive Life Consulting — Design

## Related Documents

Runtime behavior is defined by [`SKILL.md`](SKILL.md) and mirrored in [`SKILL.zh.md`](SKILL.zh.md). Refactor acceptance scenarios live in [`EVALS.md`](EVALS.md). Operational detail is split across [`references/`](references/). Project overview: [`../../../README.md`](../../../README.md).


## 1. Why This Document Exists

`SKILL.md` defines runtime behavior.

This document preserves the reasoning behind that behavior so future maintainers do not accidentally reintroduce failure modes that were already discovered and rejected.

A future refactor may reorganize wording and file structure, but it should not violate the design invariants below without explicitly documenting a protocol change.

---

## 2. Design Objective

The skill is intended to help with life and everyday-life problems that are:

- personally contextual;
- uncertain;
- multi-factor;
- partly dependent on external reality;
- often not reducible to a fixed questionnaire;
- sometimes choices, but sometimes diagnosis, planning, behavior change, or problem discovery.

The system should improve the quality of **belief and action under uncertainty**.

It should not maximize psychological interpretation, conversation length, or user profiling.

---

## 3. Design Invariants

### INV-01 — Solve the Real Problem

Do not optimize the user's initial framing without first checking whether the framing, option set, assumptions, success criteria, or time horizon are themselves wrong.

### INV-02 — Deeply Deconstruct Lived Context and Execution Friction

Do not build an abstract, permanent personality inventory. Instead, deeply explore the user's real-world context, daily energy rhythms, procrastination mechanisms, drop-off triggers, and past experiential slices that directly affect how options are chosen, started, and sustained.

### INV-03 — Acquire Only Decision-Relevant Information

A question, research action, inspection, inference, or experiment should justify its expected information value.

Interesting information is not enough.

### INV-04 — Route Unknowns to the Best Evidence Source

Use ASK, RESEARCH, INSPECT, INFER, or TEST according to where reliable evidence actually exists.

### INV-05 — Do Not Force Introspection Where Reality Can Answer Better

If the user cannot reliably predict an unfamiliar experience, stop asking hypotheticals and design a real-world test.

### INV-06 — Preserve Epistemic Type

Facts, subjective experiences, values, preferences, behavior, inferences, hypotheses, and recommendations must not silently collapse into one another.

### INV-07 — Observed Behavior Usually Outweighs Abstract Self-Description

When behavior and trait labels disagree, investigate what actually happened.

### INV-08 — Hard Reality Can Dominate Psychological Fit

Health, safety, law, money, time, geography, eligibility, and opportunity structure may override a psychologically attractive option.

### INV-09 — Immediate-Action Confidence Is Not Long-Term-Conclusion Confidence

"This is the best thing to test next" is not equivalent to "this is definitely the best long-term choice."

### INV-10 — Chat Sessions Are Disposable; Cases Are Durable

When persistence is supported, the durable authority is the case state in the workspace, not a specific chat thread.

### INV-11 — Current State May Change; Material History Must Remain Traceable

Current case state is mutable. Historical evidence and conclusions that materially influenced reasoning must not be silently rewritten.

### INV-12 — Retrieval, Not Historical Preload

Past cases should be retrieved selectively when relevant, not injected wholesale as a global user profile.

### INV-13 — Hypotheses Never Silently Become Facts

A hypothesis may be strengthened, downgraded, rejected, or re-tested. It must not become a permanent user trait merely through repetition.

### INV-14 — Distinguish Time Change, Context Difference, and Contradiction

Different values across time or scope may both be true. Do not manufacture contradictions.

### INV-15 — Propagate Only Material Cross-Case Changes

Do not reopen every historical case after every new statement. Reopen only cases whose conclusions materially depended on changed evidence.

### INV-16 — Persistent Personalization Remains User-Inspectable and Correctable

The user should be able to inspect, correct, retire, delete, or prohibit reuse of persisted personal information where the host environment supports it.

### INV-17 — New Case Is Not the Same as Resume

Semantic similarity is insufficient to merge cases. Distinguish `new-case`, `resume`, `reopen`, and `related-new-case`.

### INV-18 — Split Cases Before Scope Drift Becomes Structural

If a subproblem develops its own goal, evidence, experiments, and lifecycle, it may deserve a child case.

### INV-19 — Consider Time Horizon Explicitly

Short-term and long-term optima may differ.

### INV-20 — Choice Problems Should Consider Status Quo and Delay

Do not assume the user must pick among the originally listed active options.

### INV-21 — Respect Stakeholder Perspective Boundaries

A user's belief about another person's thoughts is not automatically a fact about that person.

### INV-22 — Decision Quality and Outcome Quality Are Different

Retrospective review must distinguish whether the reasoning was sound at the time from whether the eventual outcome happened to be good or bad.

### INV-23 — Cognitive Value of Dialogue and Natural Convergence

Thoughtful dialogue, perspective reframing, and mutual understanding are first-class consulting values in themselves, not mere preliminary friction before action. Consultation should not be prematurely cut short under a rush to act, but should converge naturally when context is clear, working hypotheses are corroborated, and candidate paths genuinely resonate.

### INV-24 — Data Minimization Applies to Persistence Too

Do not preserve sensitive or irrelevant details merely because storage exists.

### INV-25 — Refactors Require Behavioral Regression, Not Visual Similarity

A shorter skill is not equivalent merely because it "sounds the same." Equivalence is judged through invariants and eval scenarios.

### INV-26 — Atomic Single-Question Cadence on Inquiry Turns

On any turn where the agent inquires or gathers information from the user, it must formulate strictly ONE atomic question with a single focus. Never combine multiple inquiries into compound questions using conjunctions ("meanwhile / also / additionally / besides / 同时 / 另外 / 顺便").

### INV-27 — Pure Professional Advisory Tone

The agent must maintain an objective, natural, and grounded consulting tone without roleplaying or referencing internal pedagogical character personas in user output.

### INV-28 — Interleaved Evidence Progression & Precondition Gates

After initial problem framing and dependency discovery, ASK / INSPECT and external RESEARCH may proceed in parallel and repeatedly update competing hypotheses. External reality exploration must not be deferred until user interviewing is complete. Actionable delivery still requires grounded dependencies, and an experiment must discriminate among explicit uncertainties or hypotheses rather than substitute for thinking.

### INV-30 — Hybrid Deterministic Tooling

Mechanical file system scaffolding, YAML schema validation, conclusion snapshotting, and cross-case dependency graph searches are delegated to zero-dependency deterministic Python scripts (`scripts/`). Cognitive intent analysis, epistemic typing, single-question gating, and experiment design remain 100% in the prompt reasoning domain.

### INV-29 — Anti-Premature Convergence by Action Cost

Low execution or trial cost is not an excuse to skip premise deconstruction and hypothesis discrimination. The agent must not collapse an adaptive consultation into a shallow recommendation simply because testing an option is cheap.

### INV-31 — Anchor Is Not Mechanism

When a user mentions a concrete past example, favorite, or dislike (e.g. a book, a past job, a sport), record it strictly as an unexamined factual anchor. The agent must never silently project the object's general attributes (genre tags, domain stereotypes) into confirmed user motivations without verifying the specific experiential slice that actually worked or failed.

### INV-32 — Tension-Driven Problem Formulation

Consultation requests are driven by latent tensions, dilemmas, or execution friction (e.g. desire vs fatigue, high taste baseline vs fear of disappointment, startup inertia). Before generating concrete options or recommendations, the agent must identify and clarify the underlying tension.

### INV-33 — Dual-Purpose Proactive Research

Research serves both fact verification and solution-space expansion. The agent must actively use external search to discover candidates beyond its static high-frequency memory (such as recent releases, niche options, and community-verified pitfalls), preventing memory echo chambers.

### INV-34 — Indirect Corroboration and Multi-Angle Triangulation

User choices or statements must not be treated as direct mechanical switches to immediate recommendations. The agent must formulate working hypotheses about underlying behavioral/psychological mechanisms, and test them through subsequent indirect inquiries, scenario comparisons, and cross-verifications.

### INV-35 — Upfront Depth and Budget Alignment

At the beginning of a consultation, the agent should calibrate the user's intended depth and time/round expectations (quick directional navigation vs deep multi-turn exploratory deconstruction) to pace the inquiry appropriately.

### INV-36 — Research as Cognitive Fuel for Hypothesis Refinement

External research is not merely for looking up prices or schedules; it is vital fuel for the agent to understand complex domain dynamics, challenge superficial stereotypes, and formulate richer, non-obvious hypotheses and indirect probes during consultation.

### INV-37 — Research Is Observable External Evidence

RESEARCH requires an actual external tool action, reading a traceable source, and preserving its provenance and supported scope. Model recall, unsourced domain exposition, and suggested searches are not research.

### INV-38 — Internal Prior Is Not External Reality

Model-internal knowledge may generate hypotheses, candidates, and search directions. It must not enter External Reality, masquerade as a research finding, or independently support a high-confidence or high-stakes conclusion.

### INV-39 — Model the User–Environment–Supply System

Substantive real-world advice must consider the interaction among the person, physical and institutional environment, actually available options and providers, domain mechanisms, and the path to execution. Understanding the person alone is insufficient.

### INV-40 — Discover Latent Decision Dependencies

The agent must identify unmentioned external dependencies that can change feasibility or ranking, including locality, time, supply, provider format, eligibility, safety, and current rules. It must not wait for the user to ask whether a real-world option exists.

### INV-41 — ASK and RESEARCH Interleave

Atomic single-question cadence limits only questions posed to the user. It does not prevent research, inspection, analysis, or reporting evidence in the same turn.

### INV-42 — External Reality Is Provenance-Bounded

Every claim admitted to External Reality must trace to a direct user report or an identified external source with retrieval time, evidence grade, supported scope, and material limitations.

### INV-43 — High-Stakes Claims Need Authority and Scope Control

Medical, legal, safety, and major financial claims require evidence appropriate to their risk. General guidance cannot silently become an individualized professional conclusion.

### INV-44 — Confidence Requires Dependency Completeness

A conclusion cannot receive high confidence when a decisive external dependency is missing, stale, weak, or narrower than the conclusion. Immediate-action confidence remains distinct from option-fit and external-feasibility confidence.

### INV-45 — Acquire Minimum Necessary Location

Request only the coarsest location or jurisdictional coordinate that can materially change the decision. Location is a dependency-sensitive input, not a universal intake question.

---

## 4. Non-Goals

This skill is not intended to:

- build a complete psychological profile;
- diagnose mental disorders;
- replace medical, legal, financial, or other domain professionals;
- maximize the number of interview questions;
- eliminate uncertainty before action;
- preserve every personal detail;
- make irreversible decisions on behalf of the user;
- make all historical cases consistent by forcing one permanent model of the user;
- treat generic population research as individualized truth;
- maintain a single eternal recommendation.

---

## 5. Core Architecture

The conceptual architecture is:

```text
Conversation / Event Stream
          |
          v
     Current Case State
          |
    +-----+------+----------------+
    |            |                |
    v            v                v
 Evidence     Experiments    Versioned Conclusions
    |
    v
Canonical Cross-Case Memory
    |
 selective retrieval / dependency impact
    v
Historical Cases
```

The important separation is:

- conversation = interaction;
- case state = active working model;
- artifacts = durable evidence and outputs;
- canonical memory = curated cross-case state;
- historical cases = selectively retrieved context.

---

## 6. Why Case State Exists

A long raw transcript contains:

- obsolete hypotheses;
- repeated statements;
- low-value side explorations;
- contradictory intermediate reasoning;
- stale external facts.

Even if the model context can technically hold the transcript, that does not make full-transcript preload the best working-memory design.

A compact case state should preserve the current frontier without pretending the historical transcript never existed.

---

## 7. Why Long-Term Memory Is Not Enough

Generic cross-session memory answers:

> What might be useful to remember about this user later?

Case state answers:

> Where has this specific investigation reached?

Those are different functions.

Case conclusions should not automatically become permanent user traits.

---

## 8. Why Real-World Experiments Are First-Class

Some variables are not reliably introspectable before experience.

Examples:

- whether a real commute becomes intolerable;
- whether a team culture feels acceptable;
- whether an activity's passive phases are boring;
- whether technical interest survives physical fatigue;
- whether a proposed routine is actually executable.

Repeated hypothetical questioning often produces false precision.

Experiments should be designed to discriminate among hypotheses rather than merely create "trial experiences."

---

## 9. Why Interaction Budgets Are Soft

Fixed question counts create two opposite errors:

- asking more after the decision frontier is already stable;
- stopping too early in genuinely complex cases.

Budgets therefore constrain exploration but do not create quotas.

Checkpoint logic is more important than exact question count.

---

## 10. Why Progressive Disclosure Is Preferred

The pre-refactor v3 accumulated many operational details in a single file.

That made the behavior explicit but created:

- duplicate rules;
- repeated stop logic;
- repeated persistence logic;
- repeated cross-case truth-maintenance logic;
- high runtime context load;
- greater risk that later patches would contradict earlier text.

The v4 bundle therefore keeps:

- runtime kernel in `SKILL.md`;
- rationale in `DESIGN.md`;
- behavioral regression in `EVALS.md`;
- detailed protocols in `references/`.

The goal is **runtime context slimming**, not deletion of important behavior.

---

## 11. Rejected Designs

### Rejected — Transcript-Only Memory

Reason:

Long-running consultation becomes dependent on one chat thread and accumulates stale reasoning.

### Rejected — Global User-Profile Preload

Reason:

Creates memory contamination, anchoring, and historical determinism.

### Rejected — Everything Goes Into Long-Term Memory

Reason:

Case-local conclusions and tentative hypotheses would become overgeneralized.

### Rejected — Every Turn Becomes a Markdown Transcript

Reason:

Duplicates host history and creates unnecessary storage and retrieval cost.

### Rejected — Fixed Questionnaire Length

Reason:

Question count is not a proxy for information gain.

### Rejected — Personality Matching as Primary Decision Method

Reason:

Traits often have weak discriminative power relative to constraints, behavior, and opportunity structure.

### Rejected — Research After Every User Answer

Reason:

Creates research decoration and false scientific precision without necessarily reducing uncertainty.

### Rejected — Silent Overwrite of Historical Evidence

Reason:

Destroys provenance and makes it impossible to understand why an earlier decision was made.

### Rejected — Reopen Every Historical Case After Every Memory Update

Reason:

Creates excessive propagation and over-association.

### Rejected — "Try Both and See"

Reason:

Underspecified experiments may test the wrong experience and produce low-value evidence.

### Rejected — Flat Declarative Rule Enumeration without Turn Progression

Reason:

Listing rules without an imperative state progression loop allows the LLM to skip critical premise deconstruction and hypothesis formulation steps under conversational pressure.

### Rejected — Low-Cost Trial as an Early Exit from Consultation

Reason:

Equating cheap trial cost with an immediate stop condition causes the agent to bypass deep context, attention curve, and historical dropout exploration for everyday decisions.

### Rejected — In-Band Negative Persona Constraints ("Pink Elephant" Prompting)

Reason:

Negative instructions like "do not roleplay Socrates" inadvertently increase token attention on those personas. Pedagogical metaphors must be purged entirely from the skill runtime and restricted to human documentation.

### Rejected — Silent Attribute Mapping from Examples

Reason:

Conflating an example's general attributes with the user's personal motivation causes false personalization, bypasses premise deconstruction, and triggers premature convergence.

### Rejected — Narrowing Research Exclusively to Static Fact-Checking

Reason:

Restricting external search solely to prices, regulations, and schedules prevents the agent from exploring modern, diverse, or counter-intuitive real-world solution spaces, trapping recommendations in repetitive LLM training artifacts.

### Rejected — Mechanistic Option-to-Result Mapping

Reason:

Treating a user's single answer or choice as an immediate recommendation trigger bypasses hypothesis formation, ignores deeper behavioral patterns, and fails to cross-verify assumptions through indirect probing.

### Rejected — Ideological Action Supremacy

Reason:

Treating conversation as mere overhead and enforcing aggressive early stopping destroys the cognitive reframing, emotional resonance, and deep deconstruction that constitute the core value of human-centered consultation.

### Rejected — Premature Round-Truncation

Reason:

Artificially capping interaction rounds to very small numbers forces the agent into shallow triage mode rather than allowing standard and deep inquiries to unfold with proper pacing.

---

## 12. Design Lessons From the Originating Case

The original development case involved a long adaptive consultation about choosing an adult sport.

Important lessons included:

1. Hidden variables can matter more than obvious option differences.
2. Some behavioral history is highly informative.
3. Local ecosystem research can dominate abstract preference.
4. Generic research citations can create false precision when discriminative value is low.
5. The agent can recognize declining information value yet still continue asking unless a formal stop rule exists.
6. Repeated "I don't know" often means the variable is not introspectable.
7. "Best next experiment" can be much more certain than "best long-term option."
8. Local-source quality must be graded rather than treated uniformly.
9. Long conversations can drift in context even when the final answer remains plausible.
10. Case persistence and structured state are necessary if the work is expected to survive session loss.

These lessons are captured as invariants and evals rather than preserved as domain-specific sport rules.

---

## 13. Change-Control Policy

Future maintainers should treat protocol changes in three categories.

### Refactor

Behavior should remain equivalent.

Requirements:

- preserve all applicable invariants;
- pass regression evals;
- preserve or migrate schemas;
- preserve historical provenance.

### Feature Addition

Adds behavior without intentionally breaking existing semantics.

Requirements:

- add new invariants if necessary;
- add evals;
- document interaction with existing references.

### Breaking Protocol Change

Intentionally changes behavior or storage semantics.

Requirements:

- increment protocol version;
- document migration;
- explicitly identify affected invariants and evals;
- preserve archived previous versions.


---

## 15. Final Design Principle

The system should become more useful over time without becoming more dogmatic about the user.

Accumulated history should improve evidence retrieval, not harden into an unquestioned identity model.
