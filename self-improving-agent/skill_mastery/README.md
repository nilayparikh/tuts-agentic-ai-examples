# Skill Mastery Studio

This example learns reusable support habits from successful traces, then
recombines those habits for a new issue. It is a lightweight adaptation of the
MaestroMotif idea: learn small skills, decide when they apply, and compose them
zero-shot for a fresh task.

```mermaid
flowchart LR
    A[Demonstration traces] --> B[Habit learner]
    C[Habit seeds] --> B
    D[New problem] --> E[Context pack]
    E --> F[Habit selector]
    B --> F
    F --> G[Selected habit cards]
    G --> H[Hermes drafting agent]
    H --> I[Candidate reply]
    I --> J[Deterministic evaluator]
    J --> K[Revision feedback]
    K --> H
```

## Scenario

Skill Mastery Studio models a shared service desk across several real-world
operations contexts. Instead of mutating one large instruction prompt, it learns
small reusable habits that appear again and again in strong responses.

## MaestroMotif Mapping

This example keeps the surface intentionally small, but it mirrors the four
phase logic from MaestroMotif:

1. Score evidence from prior traces.
2. Distill reusable habit cards.
3. Select the habits that fit the new problem.
4. Compose a reply with those habits zero-shot.

## Output Artifacts

The loop writes these files to `.output/`:

- `latest_session.json` — round history, scores, selected habits, and context
- `learned_habits.json` — the reusable habits promoted from the shipped traces
- `selected_habits.md` — the small habit set used for the current issue
- `best_response.md` — the highest-scoring customer reply
- `latest_mutation.diff` — unified diff showing how the reply artifact changed

If you keep iterating in the terminal review flow, later rounds also record the
exact `user_feedback` string that triggered the revision.

Each saved round now also records verbose `logs`, `llm` request metadata, and
the mutation diff for the changed reply artifact when a revision lands.

## Verbose Execution Trace

The CLI now prints a CleanLoop-style trace while the loop runs. You see:

- round start markers
- explicit LLM request lines for draft and revision calls
- per-round scores
- unified text diff output when the reply changes

That makes it obvious when the example is actually calling the LLM and how the
customer-facing reply changed after each revision.

## Dashboard

Launch the dashboard with:

```bash
python util.py -e skill_mastery dashboard
```

The dashboard shows:

- per-round scores and user feedback
- raw reply text for each round
- logged LLM request metadata
- the latest unified diff for the reply mutation

## Interactive Review

In a normal terminal session, the loop now shows the current best reply first,
then asks for more feedback until you accept the result.

The CLI asks two follow-up questions after the intermediate output:

```text
Are you happy with this output? [Y/n]
What should change next?
```

Use the second prompt to steer the habit composition. Good feedback usually
targets one of these moves:

- Problem mirroring: lead with the customer issue faster
- Policy grounding: cite the rule earlier or more directly
- Checkpoint design: ask one clear question or name one next step
- Tone: more direct, more human, less formal, shorter

Examples:

- If you ask "lead with the missing booking," expect the mirror habit to appear earlier.
- If you ask "mention certification before the reassurance," expect the gate or policy to move higher in the reply.
- If you ask "end with one confirmation question," expect a sharper checkpoint.
- If you ask "sound more human but keep the policy," expect less formal phrasing without dropping the rule.

You can also provide feedback on this line: "Keep the same structure, but make the first sentence more direct and end by asking for the badge number."

## Command Flow

```bash
python util.py -e skill_mastery catalog
python util.py -e skill_mastery loop --context makerspace_frontdesk \
  --problem "A member's laser cutter booking disappeared before open lab tonight."
python util.py -e skill_mastery dashboard
python util.py -e skill_mastery reset
```

Suggested demo path:

1. Let the first reply show which habits were selected for the baseline issue.
2. Ask for one concrete revision in the review prompt.
3. Show how the next reply changes while the learned habit set stays stable.
4. Stop when the user-facing draft demonstrates the adaptation you want.
