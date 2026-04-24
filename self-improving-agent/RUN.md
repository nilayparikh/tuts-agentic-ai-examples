# RUN.md — Self-Improving Agent Quick Reference

All commands go through `util.py`. Route to a demo with `--example` or `-e`.

## First Time Setup

```bash
python util.py setup
python util.py verify
```

## CleanLoop

CleanLoop is now finance-only. You do not choose a dataset. The loop always
works on the five finance invoice files in `cleanloop/.input/`.

Run the loop:

```bash
python util.py -e cleanloop loop
python util.py -e cleanloop loop --max-iterations 10
python util.py -e cleanloop loop --rerank
python util.py -e cleanloop loop --rerank --candidates 5
```

Evaluate and monitor:

```bash
python util.py -e cleanloop evaluate
python util.py -e cleanloop dashboard
python util.py status
```

Advanced commands:

```bash
python util.py -e cleanloop challenge --levels 1 2 3
python util.py -e cleanloop sandbox --timeout 10
python util.py -e cleanloop autonomy --rounds 20
python util.py -e cleanloop reset
```

## Prompt Evolution

Prompt Evolution mutates an instruction prompt instead of code. You pick a
predefined context pack, choose multiple preferences, and enter a live support
issue.

List the available contexts and preference axes:

```bash
python util.py -e prompt_evolution catalog
```

Run the loop:

```bash
python util.py -e prompt_evolution loop --context coworking_membership \
  --preference tone=warm \
  --preference structure=bullets \
  --preference initiative=next_step \
  --problem "A member says their guest booking vanished before tonight's workshop."
python util.py -e prompt_evolution dashboard
python util.py -e prompt_evolution reset
```

Prompt Evolution now ships a broader support mix, including coworking,
makerspace, hotel, pet boarding, community garden, and language school desks.

In a normal terminal session, Prompt Evolution now shows the best intermediate
reply and asks for more input until you accept it:

```text
Are you happy with this output? [Y/n]
What should change next?
```

Good Prompt Evolution feedback:

- "Make it warmer and shorter." Expected effect: softer tone and less setup.
- "Mention tool certification earlier." Expected effect: policy grounding moves higher.
- "End with one clear question." Expected effect: tighter closing action.
- "Offer two options instead of one." Expected effect: the next step becomes branching.

Verbose trace additions:

- per-round LLM request lines are printed while the loop runs
- the saved session now includes `logs` and `llm` metadata per round
- `prompt_evolution/.output/latest_mutation.diff` shows the latest instruction diff
- `python util.py -e prompt_evolution dashboard` opens a Streamlit view of the trace

## Skill Mastery

Skill Mastery learns reusable habits from shipped demonstration traces and then
recombines those habits on a new issue.

List the available contexts and habit seeds:

```bash
python util.py -e skill_mastery catalog
```

Run the loop:

```bash
python util.py -e skill_mastery loop --context makerspace_frontdesk \
  --problem "A member's laser cutter booking disappeared before open lab tonight."
python util.py -e skill_mastery dashboard
python util.py -e skill_mastery reset
```

In a normal terminal session, Skill Mastery also shows the best intermediate
reply and asks for more input until you accept it:

```text
Are you happy with this output? [Y/n]
What should change next?
```

Good Skill Mastery feedback:

- "Lead with the missing booking." Expected effect: the mirror habit appears earlier.
- "Mention certification before the reassurance." Expected effect: the policy gate moves up.
- "End with one confirmation question." Expected effect: a clearer checkpoint.
- "Keep it direct, but sound more human." Expected effect: less formal wording without losing the habit structure.

Verbose trace additions:

- per-round LLM request lines are printed while the loop runs
- the saved session now includes `logs` and `llm` metadata per round
- `skill_mastery/.output/latest_mutation.diff` shows the latest reply diff
- `python util.py -e skill_mastery dashboard` opens a Streamlit view of the trace

What reset does:

- Deletes `cleanloop/.output/`
- Restores `clean_data.py` from `clean_data_starter.py`
- Clears stale finance artifacts before the next run

Key CleanLoop artifacts:

```text
cleanloop/.output/
  finance_master.csv
  finance_eval_history.json
  finance_strategy.json

cleanloop/.gold/
  finance_expected.csv
```

The strategy file is the lightweight metacognition layer. It records the
current repair focus, such as value normalization or row reconciliation.

## Shared Commands

```bash
python util.py setup
python util.py verify
python util.py status
```

## Finance Arena Files

| File                               | Why It Exists                                          |
| ---------------------------------- | ------------------------------------------------------ |
| `finance_invoices.csv`             | Base ledger                                            |
| `finance_invoices_flags.csv`       | Flags, placeholders, and review codes                  |
| `finance_invoices_regional.csv`    | Mixed currencies and mixed date formats                |
| `finance_invoices_collections.csv` | Collections metadata and disputed values               |
| `finance_invoices_adjustments.csv` | Reversals, adjustments, approval markers, and outliers |

Target schema:

```text
date, entity, value, category
```

## Typical Workflows

CleanLoop:

```text
python util.py setup
python util.py verify
python util.py -e cleanloop loop
python util.py -e cleanloop dashboard
python util.py -e cleanloop challenge
python util.py -e cleanloop loop
python util.py -e cleanloop reset
```
