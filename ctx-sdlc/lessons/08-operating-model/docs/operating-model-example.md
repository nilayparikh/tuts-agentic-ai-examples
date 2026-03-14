# Lesson 08 — Operating Model Example

This document defines the concrete example used in Lesson 08.

## Objective

Show that a read-only operating-model analysis can explain how the lesson detects context drift and why the clean versus drifted examples matter.

## Expected Output Shape

The preferred output for this lesson is a structured analysis with:

1. Summary
2. Drift types the lesson is designed to catch
3. Most dangerous differences between the clean and drifted examples
4. One false positive
5. One hard negative
6. Maintenance cadence recommendation
7. Prioritized fixes

## Required Constraints

1. The workflow must remain read-only.
2. The analysis must inspect both maintenance scripts, both example instruction files, and the maintenance schedule together.
3. The analysis must explicitly call out copy-paste drift, stale references, contradictory rules, over-specification, and under-specification.
4. The analysis must explain why the clean example is healthier than the drifted example.
5. The analysis must include at least one false positive and one hard negative from the operating-model perspective.
6. The analysis must map each major drift risk or dangerous difference to the exact artifact or artifact pair that demonstrates it.
7. The assessment run must not use SQL, task/todo write tools, or other write-capable tools.

## Concrete Scenario

Use the lesson's current maintenance scripts and example instruction files to explain what kinds of context rot the operating model is trying to prevent.

## What Good Output Looks Like

Good output will usually:

- explain what `audit_context.py` checks versus what `detect_stale_refs.py` checks
- identify stale technology references and contradictory rules in the drifted example
- explain why overly detailed global instructions are dangerous
- call out one false positive where a difference looks suspicious but is actually acceptable
- call out one hard negative where stale or contradictory context would directly mislead an assistant
