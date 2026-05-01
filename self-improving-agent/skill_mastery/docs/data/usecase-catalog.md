# Skill Mastery Use Case Catalog

Use cases live in `skill_mastery/.data/usecases/`. Each file gives the loop a
repeatable service case with the same shape every time.

## File Shape

```json
{
  "slug": "makerspace_access_checkpoint",
  "label": "Makerspace Access Checkpoint",
  "context_slug": "makerspace_frontdesk",
  "customer_problem": "A member says their laser cutter booking vanished...",
  "customer_facts": ["The booking is missing before open lab tonight."],
  "risk_flags": ["Do not bypass active tool certification."],
  "expected_habit_slugs": ["mirror_issue", "cite_policy_gate"],
  "expected_policy_slugs": ["booking_window", "certification_gate"],
  "success_criteria": ["Mirror the missing booking in the first sentence."],
  "source_demonstration_ids": ["makerspace-booking-restore"],
  "operator_notes": ["Best demo for booking and access language."]
}
```

## Shipped Use Cases

| Use case                       | Context                | Best for                                                      |
| ------------------------------ | ---------------------- | ------------------------------------------------------------- |
| `makerspace_access_checkpoint` | `makerspace_frontdesk` | Booking recovery, certification gates, and access boundaries  |
| `language_transfer_recovery`   | `language_school`      | Transfer review, section changes, and policy timing           |
| `pet_medication_boundary`      | `pet_boarding`         | Safety-sensitive medication updates and escalation boundaries |

## How Selection Uses Them

The use case sets the default context and problem. It also records expected
habit slugs for trace review and dashboard comparison. The selector still scores
habits from the actual profile text and context terms, so a use case remains an
input fixture, not a hard-coded answer key.

Run the catalog view with:

```bash
python util.py -e skill_mastery usecases
```
