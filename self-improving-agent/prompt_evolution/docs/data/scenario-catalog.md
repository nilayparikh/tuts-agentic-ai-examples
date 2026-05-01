# Scenario Catalog

Scenarios live in `.data/scenarios/`. Each file defines one support-desk case
that can run without typing a long problem statement by hand.

Each scenario contains:

| Field                   | Purpose                                                     |
| ----------------------- | ----------------------------------------------------------- |
| `slug`                  | Stable CLI id for `--scenario`                              |
| `context_slug`          | Context pack used for policy and voice                      |
| `customer_problem`      | Default customer issue for the run                          |
| `default_preferences`   | Tone, structure, initiative, evidence, and closing defaults |
| `customer_facts`        | Facts added to the generation prompt                        |
| `risk_flags`            | Promises the reply must avoid                               |
| `expected_policy_slugs` | Policy points the case should exercise                      |
| `success_criteria`      | Human-readable demo target                                  |
| `operator_notes`        | Teaching notes for the scenario                             |

## Shipped Cases

| Scenario                     | Context                   | Best For                                        |
| ---------------------------- | ------------------------- | ----------------------------------------------- |
| `makerspace_missing_booking` | Makerspace front desk     | Policy-first access and certification gates     |
| `coworking_guest_refund`     | Coworking membership desk | Refund restraint and access reissue wording     |
| `hotel_late_credit`          | Boutique hotel guest desk | Polite refusal and staff handoff                |
| `pet_medication_update`      | Pet boarding guest desk   | Checklist structure and safety-sensitive review |

Run a scenario:

```bash
python util.py -e prompt_evolution loop --scenario makerspace_missing_booking
```

Override one preference while keeping the rest of the scenario defaults:

```bash
python util.py -e prompt_evolution loop --scenario makerspace_missing_booking \
  --preference tone=warm
```

The override is useful in demos. You can show the same problem with a different
tone or closing behavior while keeping the policy facts stable.
