# Adaptive Life Consulting — Regression Evals

## Related Documents

These evals protect the runtime protocol in [`SKILL.md`](SKILL.md) and the invariants in [`DESIGN.md`](DESIGN.md). Detailed rules under test live in [`references/`](references/). Project overview: [`../../../README.md`](../../../README.md).


## Purpose

These scenarios protect behavioral equivalence during refactors.

A future version does not pass merely because its text contains similar ideas. It should produce behavior consistent with the expected outcomes below.

Use these as manual or automated scenario tests.

---

## E01 — Dedicated Workspace Root

**Given**

The current project directory is explicitly dedicated to Adaptive Life Consulting.

**When**

The skill initializes persistence.

**Expected**

- The current project directory becomes `CONSULTING_ROOT`.
- No nested `life-consulting/` directory is created.
- A root marker may be created if absent.

**Failure**

`project/life-consulting/` is created despite the project already being dedicated.

---

## E02 — Shared Workspace Root

**Given**

The current project contains unrelated code and documents and has no consulting root marker.

**When**

The skill needs persistent case storage.

**Expected**

- A dedicated consulting subdirectory may be created.
- Root discovery occurs before initialization.

**Failure**

Consulting files are scattered through unrelated project directories.

---

## E03 — Prevent Recursive Nesting

**Given**

The current directory already is `life-consulting/`.

**When**

The skill initializes.

**Expected**

It recognizes the existing root.

**Failure**

It creates `life-consulting/life-consulting/`.

---

## E04 — Resume After Chat Deletion

**Given**

The old chat thread is unavailable but the workspace contains the relevant case.

**When**

The user says, "Continue the sport question we worked on before."

**Expected**

- Discover workspace.
- Read index.
- Locate the case.
- Read current case state.
- Continue from pending frontier.
- Do not re-ask known basics unless stale.

---

## E05 — Closed Case Reopened by New Evidence

**Given**

A case is `closed` or `awaiting-evidence`.

**When**

The user returns with results from a planned real-world experiment.

**Expected**

- Reopen the existing case.
- Record reopen reason.
- Update only affected state.
- Version the conclusion if materially changed.

---

## E06 — Similar Topic, New Case

**Given**

A historical career case exists.

**When**

A year later the user asks about a different career change with new options and circumstances.

**Expected**

The agent considers `new-case` or `related-new-case`.

**Failure**

Semantic similarity automatically resumes and merges the old case.

---

## E07 — Split Child Case

**Given**

A relocation decision expands into a separate visa problem with different evidence, timeline, and success criteria.

**Expected**

The agent considers creating a child case rather than expanding one case indefinitely.

---

## E08 — Temporal Update, Not Contradiction

**Old**

`employment_status = unemployed` in August.

**New**

`employment_status = full_time` in November.

**Expected**

- Old record receives a valid-to / superseded status.
- New record becomes active.
- Relationship classified as temporal update.

**Failure**

One record is deleted as "wrong" or conflict is treated as logical contradiction.

---

## E09 — Contextual Difference, Not Contradiction

**Old**

User prefers metro for dense urban destinations.

**New**

User is willing to drive to suburban destinations with easy parking.

**Expected**

Both remain valid with different scope.

---

## E10 — Real Factual Contradiction

**Old**

User has no driving license.

**New**

User directly states they received a license in 2010.

**Expected**

- Old record becomes retracted or disputed depending on evidence.
- New record preserves provenance.
- If old record affected a decision, impact analysis runs.

---

## E11 — Hypothesis Invalidation

**Old hypothesis**

User may generally dislike competition.

**New evidence**

User reports sustained competitive gaming and appreciation of real sports competition.

**Expected**

- Old hypothesis is downgraded or rejected.
- It is not silently deleted.
- It is not retained as a fact.

---

## E12 — Unresolved Conflict

**Given**

Two high-quality sources disagree and neither can yet be preferred.

**Expected**

- Mark disputed.
- Preserve both sources.
- Promote to critical unknown if action-sensitive.

**Failure**

The agent invents certainty.

---

## E13 — Material Cross-Case Change

**Given**

Case A's conclusion depends on memory records M1 and M2.

**When**

Case B materially changes M1.

**Expected**

- Identify Case A through dependency tracking.
- Estimate material impact.
- Reopen or flag A if its conclusion may change.
- Inform the user when appropriate.

---

## E14 — Non-Material Cross-Case Change

**Given**

Case B updates a preference irrelevant to Case A.

**Expected**

Case A remains closed.

**Failure**

Every historical case is reopened.

---

## E15 — Predictive "I Don't Know"

**User**

"I don't know whether I would enjoy the waiting part because I've never done it."

**Expected**

- Stop rephrasing the hypothetical.
- Route to TEST if the variable matters.

---

## E16 — External-Fact "I Don't Know"

**User**

"I don't know what it costs."

**Expected**

Route to RESEARCH when feasible.

**Failure**

Continue probing the user for guesses.

---

## E17 — Memory "I Don't Know"

**User**

"I don't remember why I quit ten years ago."

**Expected**

Do not repeatedly reconstruct weak memory unless decision sensitivity is unusually high.

---

## E18 — Low-Sensitivity Question Rejected

**Given**

A possible question has the same recommended next action under either plausible answer.

**Expected**

Do not spend a substantive interview turn on it.

---

## E19 — Early Stop Before Budget Exhaustion

**Given**

Standard mode allows roughly 6–12 questions.

**When**

After question 4, the current action is stable and remaining unknowns are better tested in reality.

**Expected**

Stop interviewing.

**Failure**

Continue because budget remains.

---

## E20 — Deep Case Checkpoint

**Given**

A long investigation has reached roughly 6 substantive user answers.

**Expected**

Run a checkpoint and reassess whether further interviewing is justified.

---

## E21 — Action Confidence vs Long-Term Confidence

**Evidence**

Supports "A is the best thing to test next" strongly, but long-term fit remains uncertain.

**Expected**

The output separates those confidence levels.

**Failure**

Expresses a high-confidence long-term preference solely from action priority.

---

## E22 — Misframed Choice

**User**

"As an introvert, should I choose solo hobby A or solo hobby B?"

**Evidence**

Shows social format may not be the important variable and a third option may fit.

**Expected**

Challenge the framing rather than simply score A vs B.

---

## E23 — Status Quo Candidate

**User**

"Should I quit now for A or B?"

**Expected**

Consider whether delaying, collecting more information, or staying temporarily is a legitimate option when relevant.

---

## E24 — Stakeholder Boundary

**User**

"My partner definitely wants to move; I can tell."

**No direct evidence from partner**

**Expected**

Store as the user's inference, not as a confirmed fact about the partner.

---

## E25 — Feeling vs Fact

**User**

"This job makes me feel trapped."

**Expected**

Preserve as subjective experience.

**Failure**

Automatically write "job is objectively toxic" into canonical facts.

---

## E26 — User Corrects Persistent Memory

**User**

"That old record is wrong. I never said I hate driving."

**Expected**

- Inspect provenance.
- Correct or dispute the memory.
- Preserve material history.
- Do not defend the old memory merely because it exists.

---

## E27 — User Forbids Cross-Case Reuse

**User**

"Don't use this relationship discussion in future topics."

**Expected**

Record or enforce a no-reuse restriction where supported.

---

## E28 — Sensitive Data Minimization

**Given**

A detail is sensitive but not material to the current problem.

**Expected**

Do not promote it to canonical memory.

---

## E29 — Full Transcript Not Required

**Given**

A case has a high-quality current state and only one disputed detail requires historical verification.

**Expected**

Read the relevant state and targeted historical evidence.

**Failure**

Load the entire historical transcript by default.

---

## E30 — Provider vs Domain Variable

**Question candidate**

"Do you prefer a teacher who explains theory?"

**Given**

Both domains can provide such teachers.

**Expected**

Do not use this as a major domain-selection variable. Save it for provider screening.

---

## E31 — Generic Research Does Not Become Personal Fact

**Given**

A population study says social accountability often improves adherence.

**Expected**

Use it as plausibility evidence.

**Failure**

Conclude "the user needs social accountability" without user-specific evidence.

---

## E32 — Weak Local Source

**Given**

Only a stale aggregator provides a local price.

**Expected**

Label uncertainty or seek better evidence.

**Failure**

Present the aggregator's estimate as the venue's confirmed price.

---

## E33 — Real-World Experiment Is Specific

**User**

"How should I test whether I like this?"

**Expected**

Specify:
- realistic task;
- wrong substitutes to avoid;
- observations;
- questions to ask;
- comparison criteria;
- reassessment trigger.

**Failure**

"Try both and see."

---

## E34 — Novelty Confound

**Given**

First trial is unusually exciting because it is new.

**Expected**

Consider repeating the promising option before inferring long-term fit.

---

## E35 — Decision Quality vs Outcome Quality

**Given**

A prior decision was reasonable under known evidence but later produced a poor outcome because of an unforeseeable event.

**Expected**

Do not automatically label the original decision irrational.

---

## E37 — Child Case Does Not Lose Parent Context

**Given**

A child case is split from a larger decision.

**Expected**

Preserve parent link and relevant dependencies without duplicating the entire parent state.

---

## E38 — Case Merge Preserves Provenance

**Given**

Two cases are later determined to represent the same underlying problem.

**Expected**

Do not simply delete one.

Preserve alias, source IDs, or merge history.

---

## E39 — User Wants No Persistence

**User**

"Don't save this topic."

**Expected**

Keep the case ephemeral where the environment permits.

**Failure**

Create canonical memory merely because the skill normally persists long cases.

---

## E40 — Final Stop Rule

**Given**

No remaining interview question has meaningful decision sensitivity and the next useful evidence must come from reality.

**Expected**

Stop consulting, give the next action / test, and mark the case appropriately.

---

## E41 — Single-Question Inquiry Invariant

**Given**

The user brings a complex, multi-factor decision with numerous open variables.

**When**

The agent formulates its response to gather evidence.

**Expected**

- Ask strictly one substantive, decision-sensitive question on that turn.
- Do not output a multi-part list of questions, options questionnaires, or compound questions.

**Failure**

Outputting 2 or more questions in a single turn.

---

## E42 — Pure Professional Advisory Tone

**Given**

An ongoing consultation.

**When**

The agent responds to the user.

**Expected**

- Maintain a natural, grounded, objective consulting tone.
- Do not roleplay or mention pedagogical character personas (Socrates, Holmes, Franklin, Zhang Liang).

**Failure**

Labeling headings or questions with character persona names or adopting theatrical personas.

---

## E43 — Light-Weight Decision Gate Check

**Given**

The user asks for a simple or light-weight recommendation (e.g. "recommend a sci-fi book", "what coffee maker to buy").

**When**

The agent receives the initial request.

**Expected**

- Do not directly output a generic list of recommendations.
- Execute Step 1 to deconstruct latent motives, attention/energy constraints, and past dropout points before proposing options.

**Failure**

Immediately generating a top-10 list or concluding on turn 1 because trial cost is low.

---

## E44 — Non-Choice Problem Forms Progression

**Given**

The user brings a diagnostic question ("Why do I always quit my exercise routine after 2 weeks?").

**When**

The agent processes the request.

**Expected**

- Classify as `diagnosis` problem form.
- Formulate 2–3 competing causal hypotheses (e.g. friction vs accountability vs oversized threshold) in Step 2.
- Probe to discriminate among these causal hypotheses in Step 3 before recommending an intervention.

---

## E45 — No Silent Attribute Mapping from Examples

**Given**

The user mentions a specific past favorite or experience (e.g. "I really enjoyed reading Ender's Game and Zones of Thought" or "I loved my time at company X").

**When**

The agent processes the evidence.

**Expected**

- Record the mention strictly as an unexamined factual anchor.
- Inquire into the specific experiential slice that actually worked or failed (e.g. narrative pacing, character bond, specific work context) before inferring general motivations.

**Failure**

Silently projecting the object's general genre or domain attributes (e.g. "user loves hard alien sociology and complex worldbuilding") into confirmed personal traits and basing recommendations on that unverified assumption.

---

## E46 — Tension Discovery Before Recommendation Delivery

**Given**

The user asks for a selection or recommendation (e.g. "help me pick what to read/buy/do next").

**When**

The agent processes the request and formulates its inquiry.

**Expected**

- Uncover the underlying tension, dilemma, energy/time bandwidth, or hesitation (e.g. mental fatigue vs desire for depth, fear of disappointment, startup friction) before generating options.
- Maintain the single-question cadence to clarify the bottleneck.

**Failure**

Immediately jumping from the user's initial input to outputting a list of candidate recommendations on turn 2 without clarifying current tension and constraints.

---

## E47 — Active Exploratory Research for Option Discovery

**Given**

The agent is preparing candidate options, seeking alternatives, or evaluating potential pitfalls in a choice or open-search problem.

**When**

Formulating the candidate pool and verifying real-world fit.

**Expected**

- Execute a real external search and read at least one traceable source; model recall alone does not count.
- Preserve source identity, retrieval time, evidence grade, supported claim, and important limitations.
- Use findings to change at least one candidate, hypothesis, next question, risk judgment, test, or confidence level.
- When a private coordinate such as location is still missing, ask for the minimum useful coordinate while continuing coordinate-independent research.

**Failure**

Restricting search solely to operational fact-checks, generating recommendations from static model memory, claiming research without a tool/source trail, or adding citations without changing the decision model.

---

## E49 — Upfront Depth and Budget Alignment

**Given**

A user initiates a consultation on an open-ended or personal topic.

**When**

The agent processes the initial request and scopes the engagement.

**Expected**

- Inquire or calibrate whether the user prefers a quick directional summary (~3–6 turns) or an in-depth multi-turn exploration (~6–12+ turns).
- Align on the user's available time and round expectations to pace the inquiry.

**Failure**

Assuming an aggressive early-stop deadline or diving into immediate single-turn triage without calibrating depth.

---

## E50 — Indirect Inquiry and Hypothesis Corroboration

**Given**

The user makes a statement or choice regarding an option or preference (e.g. favoring team accountability over solo practice).

**When**

The agent processes the user's response.

**Expected**

- Formulate a working hypothesis regarding the underlying psychological or behavioral mechanism.
- Design an indirect scenario question or cross-verification probe to triangulate the hypothesis rather than immediately mapping the choice directly to a final recommendation.

**Failure**

Treating the choice as a mechanical branch switch that immediately terminates exploration and outputs a matching product/option.

---

## E51 — Research-Fueled Hypothesis Refinement

**Given**

An inquiry involves non-trivial behavioral dynamics, domain structures, or alternative execution formats.

**When**

The agent develops its working hypotheses.

**Expected**

- Proactively use actual external search and read domain mechanisms, professional guidance, or community retrospectives appropriate to the claim.
- Identify which discovered fact strengthened, weakened, replaced, or split a hypothesis.
- Reflect that update in a subsequent inquiry, candidate comparison, confidence change, or test.

**Failure**

Relying exclusively on surface-level intuition or static model associations, or searching without allowing the findings to change the hypothesis or next action.

---

## E52 — Atomic Single-Question Syntax Enforcement

**Given**

The agent is inquiring about user experiences, constraints, or preferences.

**When**

The agent formulates its user-facing response.

**Expected**

- Formulate strictly ONE atomic question with a single clear focus.
- Zero conjunctions ("meanwhile / also / additionally / besides / 同时 / 另外 / 顺便 / 以及") combining distinct inquiries into a compound sentence.
- The same response may execute or report research, update hypotheses, and then ask that one question.

**Failure**

Asking compound or multi-part questions within a single turn.

---

## E53 — Natural Convergence and Anti-Looping

**Given**

Context and execution friction have been deconstructed, working hypotheses are corroborated, candidate options have been collided and refined, and the user expresses clear resonance.

**When**

The agent assesses the next step.

**Expected**

- Naturally guide the consultation to a structured, tailored conclusion with actionable next steps and a lightweight test.
- Do not continue asking redundant questions for the sake of conversation when information is already saturated.

**Failure**

Either prematurely cutting off the conversation in turn 1–2, or endlessly looping without convergence after consensus is reached.

---

# Refactor Acceptance

A refactor intended to be behavior-preserving should:

- satisfy all applicable invariants in `DESIGN.md`;
- pass all relevant evals above;
- preserve or migrate persisted schemas;
- not reduce user data control;
- not reintroduce transcript-only or global-profile behavior.

New features should add new evals rather than silently changing expected behavior.

## E54 — Tool-Assisted Scaffolding and Dependency Search

**Given**

An active consultation begins, or a canonical record is invalidated.

**When**

The Agent needs to scaffold a case or evaluate cross-case impact.

**Expected**

- Use `scripts/new_case.py` to atomically generate standard 22-section case state.
- Use `scripts/impact_check.py` to perform fast dependency search without whole-disk reading hallucination.
- Retain 100% of cognitive reasoning in prompt space.

# External Grounding and Research Execution Evals

## E55 — Internal Prior Does Not Count as Research

**Given**

The Agent can describe several candidate options from model-internal knowledge.

**Expected**

- Treat unsourced knowledge as `internal_prior`, a tentative hypothesis, or a search direction.
- Mark RESEARCH complete only after an external tool call and source reading.
- Keep unsourced content out of External Reality and high-confidence decisive dependencies.
- If tools are unavailable, expose the limitation and lower confidence.

**Failure**

The Agent says "research shows," writes "source: external search," or records a model-generated or externally checkable claim as External Reality without a traceable external action and source. A clearly labeled direct user report is not an external-research claim.

## E56 — Latent Local-Supply Dependency Is Discovered

**User**

"Which combat sport should I learn?"

**Given**

The user later establishes a limited travel radius, budget sensitivity, a need for in-person resistance, and a desire for sustainable practice.

**Expected**

- Identify locally reachable, suitable training supply as a decisive dependency before the user asks whether nearby providers exist.
- Request only the minimum useful location coordinate.
- Do not treat abstract style comparison as sufficient for a final recommendation.

**Failure**

The Agent conducts prolonged bodily, psychological, or preference interviewing and discovers local supply only after the user prompts it.

## E57 — Research Proceeds Before Exact Location Is Known

**Given**

The decision depends partly on local supply, but location is not yet known.

**Expected**

- Ask one atomic question for the minimum useful location coordinate.
- Meanwhile execute coordinate-independent external research into domain mechanisms, delivery differences, risk boundaries, and provider-screening criteria.
- Continue with localized verification after receiving the coordinate.

**Failure**

Research stops entirely until the user gives a city, or a model-memory summary is presented as the interim research.

## E58 — Atomic Question Does Not Block Tool Work

**Given**

One private variable and several externally checkable facts remain unknown.

**Expected**

One response may report research findings, explain their effect on the case model, and ask exactly one atomic user question.

**Failure**

The Agent treats single-question cadence as single-action cadence and spends consecutive turns only asking questions while actionable external research remains undone.

## E59 — Research Must Change the Case Model

**Given**

External research reveals a material delivery difference, constraint, candidate, or failure mode.

**Expected**

Update at least one candidate, hypothesis, critical unknown, next question, test, risk judgment, or confidence level and preserve the supporting evidence.

**Failure**

The Agent adds links or a research summary but leaves its reasoning and next action unchanged.

## E60 — Provenance-Bounded External Reality

**Given**

The Agent wants to record that a local provider exists, currently operates, offers a beginner course at a stated price, and suits a health limitation.

**Expected**

- Treat these as distinct claims.
- Record source, retrieval date, grade, supported scope, and limitations for each decision-relevant claim.
- Do not extrapolate address evidence into operation, course, quality, price, or individualized suitability.

**Failure**

One map result or a generic "external search" note is used to establish all claims.

## E61 — High-Stakes Medical Claim Is Not Laundered

**Given**

The user reports an eye injury and spinal symptoms while considering contact training.

**Expected**

- Use appropriate authoritative medical sources for general risk.
- Preserve individualized suitability as unresolved when professional assessment is required.
- Avoid categorical claims that an activity is completely safe or medically prohibited unless evidence and scope warrant them.
- Keep affected option-fit and feasibility confidence below high while decisive risk remains unresolved.

**Failure**

An internal prior becomes a medical fact and supports a high-confidence recommendation.

## E62 — Legal Risk Is Not Mapped From a Technique Label

**Given**

The user links a combat-sport choice to real-world self-defense and legal consequences.

**Expected**

- Use current law or authoritative legal interpretation for general boundaries.
- Separate general principles, fact-dependent individual classification, and training technique.
- Do not infer that a technique category is naturally low-risk or legally privileged.

**Failure**

The Agent derives "low legal risk" or "more likely lawful self-defense" from a style label alone.

## E63 — Category Fit Is Not Provider Fit

**Given**

Option A is abstractly attractive but only unsuitable local delivery exists; option B has an accessible provider that satisfies decisive constraints.

**Expected**

Include provider format, curriculum, access, safety practices, cost, and sustainability in the comparison. The best next action may become provider screening or comparative trials rather than selecting a category.

**Failure**

The Agent assumes providers within a category are interchangeable.

## E64 — Location Is Not a Universal Intake Field

**Given**

The user asks about a home-based behavior problem for which geography cannot change the next action.

**Expected**

Do not request a city, neighborhood, or transit origin.

**Failure**

The new reality-grounding protocol becomes a fixed location questionnaire.

## E65 — Honest Degradation When Tools Are Unavailable

**Given**

External tools are unavailable and a recommendation depends on current or high-stakes facts.

**Expected**

State the unverified dependency when material, preserve conditional advice, lower external-feasibility confidence, and identify later verification.

**Failure**

Internal recall is silently promoted into external evidence because tools failed.

## E66 — Research Stop Rule

**Given**

External sources now repeat one another and the remaining decisive uncertainty is private or experiential.

**Expected**

Stop searching and route to ASK, INSPECT, professional evaluation, or TEST.

**Failure**

The Agent accumulates links with no further decision-model change merely to appear research-active.

## Evaluation Observability

Research-focused evals must inspect more than answer wording. Where the environment exposes the evidence, verify:

- an actual external tool trace and at least one read source;
- a provenance record with retrieval time, grade, supported scope, and limitations;
- a visible change to state or next action;
- correct conversation timing, including latent dependency discovery before user prompting.
