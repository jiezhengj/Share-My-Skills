[README](README.md) · [中文](README.zh.md)

# What Problem It Solves

A lot of people already use AI to talk through real-life problems: whether to change jobs, what sport to pick up, whether to move, or why a personal habit keeps falling apart.

Plain chat modes often run into familiar frustrations: ask a different AI and you get a conflicting conclusion; you know "context matters," but you have no idea which background facts actually drive the decision; after a while, the AI starts treating a single subjective remark as your permanent "personality profile"; and when you return later, you have to explain the whole backstory from scratch.

**Adaptive Life Consulting** is deliberately old-fashioned: no programs, code, scripts, or black-box scoring models, just a pure set of Prompt rules. It has one straightforward purpose—enabling your AI assistant to act like a grounded adviser: **to help you think through life's choices clearly and move forward into real-world action.**

# What It Is Not

- **No psychotherapy or mental health diagnosis**: It does not provide clinical assessments, personality typing, or therapy.
- **No fortune-telling or future prediction**: It does not engage in divination or pretend to know the future.
- **Not a blindly agreeable "AI best friend"**: It will not flatter you with hollow validation or sell you a comforting, one-size-fits-all answer.
- **Allowed to say "I don't know" and "Wrong question"**: When evidence is lacking, it will say so. When an assumption is flawed, it will point out that you might be asking the wrong question.

# How It Works: The Four Archetypes

If you want a simple way to picture the mechanism, imagine four distinct advisers working together:

> **Socrates asks. Sherlock Holmes investigates. Benjamin Franklin experiments. Zhang Liang decides when and how to act.**

- **Socrates (Questioning Premises)**: Questions the premise before rushing to answer, uncovering unverified assumptions.
- **Sherlock Holmes (Investigating Facts)**: Focuses on objective reality (prices, rules, locations) and looks at what you have actually done before, rather than relying on abstract self-evaluation.
- **Benjamin Franklin (Small Experiments)**: When thinking cannot resolve an unknown, designs a low-cost, reversible real-world trial.
- **Zhang Liang (Strategic Judgment)**: Judges which uncertainties truly matter, when enough evidence has been gathered, and when to stop deliberating and start acting.

In short: **Ask what matters, check what can be checked, test what is unknown, and focus on judgment and action.**

# How the Conversation Moves Forward

It does not subject you to a rigid, endless questionnaire. Every time new information comes in, it re-evaluates:

> *What is the most critical unknown right now? What information could actually change the next recommendation?*

Then it chooses the most effective action:

- **ASK**: Only ask what you alone can answer (critical constraints and preferences).
- **RESEARCH**: Look up external facts (prices, policies, venues, availability).
- **INSPECT**: Review past actual behavior and records rather than asking whether you are "a disciplined person."
- **INFER**: Form tentative, testable explanations without treating guesses as proven facts.
- **TEST**: When analysis reaches its limit, suggest a small real-world trial.

As the conversation progresses, questions should become fewer and the direction sharper.

# How to Use It

This skill can be used directly in mainstream Agent assistant tools like Codex, Claude, Workbuddy, Antigravity, and similar platforms.

## Setup

The skill is packaged under `.agents/skills/adaptive-life-consulting/`. You can:

- **Use as a project-level skill**: Open this repository in your Agent assistant (Antigravity, Claude Code, Codex, etc.). The assistant will automatically discover and load the skill.
- **Install globally**: Symlink or copy `.agents/skills/adaptive-life-consulting` to your global skills directory (e.g., `~/.agents/skills/` and `~/.gemini/config/skills/`).

## Starting Your First Conversation

No special prompts or commands are needed. Just start talking like you would with a trusted adviser:

- *"I'm debating whether to sign up for climbing classes this weekend, but I worry I won't stick with it."*
- *"I want to relocate to a new city in the next three months, but I'm not sure how to choose."*
- *"I want to improve my spoken English, but every study plan I make falls apart. Where am I going wrong?"*

# Keeping Progress and Moving to Action

## Continuing Without Starting Over, and Without Permanent Labels

It automatically helps you track long-term topics over time: tentative ideas, experiments you've tried, and interim conclusions are saved so you can pick up where you left off.

However, past records never turn into rigid personality labels. Facts expire, preferences depend on context, and earlier ideas can always be revised.

## Knowing When to Stop Analyzing and Start Acting

If asking more questions will no longer change the immediate recommendation, the AI stops asking.

Once verifiable facts are checked and remaining uncertainties can only be answered through firsthand experience, it encourages you to move beyond deliberation and test it directly in the real world.

# Architecture & Engineering

For developers and contributors looking to understand the underlying protocol design or run regression tests:

- **Design Invariants & Rationale**: [`DESIGN.md`](DESIGN.md)
- **Regression Evals & Test Cases**: [`EVALS.md`](EVALS.md)
