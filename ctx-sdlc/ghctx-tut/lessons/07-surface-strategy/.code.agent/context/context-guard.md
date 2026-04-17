{
"hookName": "loan-workbench-context-guard",
"description": "Validates that generated context files are not hand-edited. Edit .code.agent/context/ sources and rerun transform.py.",
"appliesTo": [
"AGENTS.md",
"CLAUDE.md",
".github/copilot-instructions.md",
".github/instructions/**/*.md",
".github/agents/**/*.md",
".github/skills/**/SKILL.md",
".github/prompts/**/*.prompt.md",
".github/hooks/*.json",
".claude/rules/**/*.md"
],
"checks": [
{
"id": "no-manual-edit",
"message": "Do not hand-edit generated context files. Edit .code.agent/context/ and rerun python transform.py --write.",
"severity": "error"
},
{
"id": "run-sync-check",
"message": "Run python transform.py --check to verify generated files are current.",
"severity": "warning"
}
]
}
