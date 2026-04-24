# Self-Improving Agents — Example Project

This repo now ships three runnable demos for the
<a href="https://tuts.localm.dev/self-improving-agents" target="_blank" rel="noopener noreferrer">Self-Improving Agents</a>
course.

| Example              | Domain                    | What It Teaches                                                          | Video                                                |
| -------------------- | ------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------- |
| **CleanLoop**        | Data engineering          | The core Karpathy loop on one finance invoice arena                      | [Watch](https://www.youtube.com/watch?v=loYCwyRU_tM) |
| **Prompt Evolution** | Customer support strategy | Prompt mutation with contexts, preferences, and Hermes                   | Not yet published                                    |
| **Skill Mastery**    | Service operations        | MaestroMotif-style reusable habits, selection, and zero-shot composition | Not yet published                                    |

CleanLoop is the teaching path. It uses one finance-only arena, one gold
reference, one output file, and one reset path. Every fresh run copies
`clean_data_starter.py` over `clean_data.py`, clears stale finance artifacts,
and starts the loop from the same weak baseline.

Prompt Evolution is the follow-on example. It mutates an instruction prompt
instead of source code. The user picks a context pack, selects multiple style
preferences, enters a live support problem, and lets Hermes refine the prompt
between rounds. In a normal terminal session, it now shows the intermediate
best draft and asks for follow-up feedback until the user is happy. It now also
prints verbose round logs, records LLM request metadata, and ships a dashboard
for inspecting mutation diffs.

Skill Mastery is the reusable-habit example. It learns compact behavior cards
from shipped demonstration traces, selects the habits that fit a new issue, and
uses Hermes to compose a fresh reply with those habits. In a normal terminal
session, it also shows the intermediate best reply and keeps collecting user
feedback until the user accepts the output. It now also prints verbose round
logs, records LLM request metadata, and ships a dashboard for inspecting reply
diffs.

## Videos

| Lesson | Thumbnail                                                                                                                                                                   | Watch                                                                                                   | Example                 |
| ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ----------------------- |
| 01     | [![Watch: AI That Improves Itself: The "Bounded Recipe" for Agents](https://img.youtube.com/vi/loYCwyRU_tM/maxresdefault.jpg)](https://www.youtube.com/watch?v=loYCwyRU_tM) | [AI That Improves Itself: The "Bounded Recipe" for Agents](https://www.youtube.com/watch?v=loYCwyRU_tM) | [cleanloop](cleanloop/) |

## Quick Start

```bash
cd _examples/self-improving-agent
python util.py setup
python util.py verify

python util.py -e cleanloop loop
python util.py -e cleanloop dashboard

python util.py -e prompt_evolution catalog
python util.py -e prompt_evolution loop --context coworking_membership \
  --preference tone=warm \
  --preference structure=bullets \
  --preference initiative=next_step \
  --problem "A member says their guest booking vanished before tonight's workshop."
python util.py -e prompt_evolution dashboard

python util.py -e skill_mastery catalog
python util.py -e skill_mastery loop --context makerspace_frontdesk \
  --problem "A member's laser cutter booking disappeared before open lab tonight."
python util.py -e skill_mastery dashboard

python util.py -e cleanloop reset
python util.py -e prompt_evolution reset
python util.py -e skill_mastery reset
```

See [RUN.md](RUN.md) for the full command reference.

For both Prompt Evolution and Skill Mastery, the live demo pattern is now:

1. Start with the baseline context, preferences, and problem.
2. Let the loop show the intermediate best output.
3. Use the terminal follow-up prompt to ask for one targeted change.
4. Keep iterating until the visible draft demonstrates the adaptation you want.

## Project Structure

```text
self-improving-agent/
  util.py
  .env.example
  pyproject.toml

  cleanloop/
    .input/                 ← Five finance invoice files only
    .gold/                  ← finance_expected.csv
    .output/                ← finance_master.csv, finance_eval_history.json, finance_strategy.json
    clean_data.py           ← Mutable genome
    clean_data_starter.py   ← Starter-copy reset source
    prepare.py              ← Immutable referee
    loop.py                 ← Orchestrator + metacognition snapshot
    dashboard.py            ← Streamlit dashboard
    challenger.py           ← Harder finance fixtures
    reranker.py             ← Best-of-N candidate selection
    sandbox.py              ← Subprocess isolation wrapper
    autonomy.py             ← Graduated trust ladder
    README.md               ← Human-readable agenda

  prompt_evolution/
    README.md               ← Mutable instruction agenda + Mermaid architecture
    .data/
      contexts/             ← Predefined service context packs
      preferences/          ← Preference axes and options
    .output/                ← latest_session.json, best_response.md, best_instructions.md, latest_mutation.diff
    config.py               ← Catalog and selection-profile loader
    dashboard.py            ← Streamlit trace dashboard
    evaluator.py            ← Deterministic scoring rules
    hermes_client.py        ← Hermes AIAgent adapter
    loop.py                 ← Prompt mutation loop

  skill_mastery/
    README.md               ← MaestroMotif-style habit-learning walkthrough
    .data/
      contexts/             ← Shared service contexts
      habits.json           ← Reusable habit seeds
      demonstrations.json   ← Successful and weak example traces
    .output/                ← latest_session.json, learned_habits.json, selected_habits.md, best_response.md, latest_mutation.diff
    config.py               ← Context, habit, and trace loader
    dashboard.py            ← Streamlit trace dashboard
    learner.py              ← Reusable habit promotion logic
    selector.py             ← Habit-selection policy for new issues
    evaluator.py            ← Deterministic skill-application scoring
    loop.py                 ← Habit composition loop

```

## CleanLoop Arena

CleanLoop now uses one progressive finance arena. The five files increase in
messiness while keeping the same target schema: `date`, `entity`, `value`,
`category`.

| File                               | Purpose                                                |
| ---------------------------------- | ------------------------------------------------------ |
| `finance_invoices.csv`             | Base ledger with blanks, refunds, and text amounts     |
| `finance_invoices_flags.csv`       | Risk flags, review codes, and placeholders             |
| `finance_invoices_regional.csv`    | Mixed currencies, regions, and mixed date formats      |
| `finance_invoices_collections.csv` | Collections metadata, escalations, and disputed values |
| `finance_invoices_adjustments.csv` | Reversals, adjustments, approval markers, and outliers |

The loop writes three core artifacts:

| Artifact                    | Purpose                                                  |
| --------------------------- | -------------------------------------------------------- |
| `finance_master.csv`        | Current genome output                                    |
| `finance_eval_history.json` | Round-by-round history for the dashboard                 |
| `finance_strategy.json`     | Lightweight metacognition snapshot for the current focus |

## The Arena Pattern

CleanLoop uses the core three-role contract:

| Role         | File            | Mutable? |
| ------------ | --------------- | -------- |
| Referee      | `prepare.py`    | No       |
| Genome       | `clean_data.py` | Yes      |
| Orchestrator | `loop.py`       | No       |

CleanLoop is the reference implementation.

- The judge compares output rows against `cleanloop/.gold/finance_expected.csv`.
- The starter genome is deliberately weak, so the loop has to earn progress.
- The loop records a small metacognition snapshot to make the current repair
  focus visible.

The course roadmap now uses two runnable extensions after CleanLoop, followed
by one conceptual next step:

- Prompt Evolution: mutate prompts and repair strategies as explicit artifacts.
- Skill Mastery: learn reusable habits, then compose them zero-shot on a new issue.
- Self-Play or RL hypothesis: show how proposer-vs-critic loops could create a reward signal without implementing RL.

## Commands

Shared commands:

- `python util.py setup`
- `python util.py verify`
- `python util.py status`

CleanLoop commands:

- `python util.py -e cleanloop evaluate`
- `python util.py -e cleanloop loop`
- `python util.py -e cleanloop dashboard`
- `python util.py -e cleanloop challenge`
- `python util.py -e cleanloop sandbox`
- `python util.py -e cleanloop autonomy`
- `python util.py -e cleanloop reset`

Prompt Evolution commands:

- `python util.py -e prompt_evolution catalog`
- `python util.py -e prompt_evolution loop`
- `python util.py -e prompt_evolution dashboard`
- `python util.py -e prompt_evolution reset`

Skill Mastery commands:

- `python util.py -e skill_mastery catalog`
- `python util.py -e skill_mastery loop`
- `python util.py -e skill_mastery dashboard`
- `python util.py -e skill_mastery reset`

| Provider         | Endpoint                          | Model           |
| ---------------- | --------------------------------- | --------------- |
| Azure AI Foundry | `https://<name>.openai.azure.com` | `Kimi-K2`       |
| Foundry Local    | `http://localhost:5272/v1`        | `qwen2.5-coder` |
| OpenAI Direct    | `https://api.openai.com/v1`       | `gpt-4o`        |

## Lesson → Code Map

Each lesson's EXAMPLE.md points to specific files and line ranges in this project.
See the per-lesson folders in `content/ai/self-improving-agents/course/` for details.
