"""Validation helpers for bounded CleanLoop genome mutations."""

from __future__ import annotations

import ast
from pathlib import Path


def validate_candidate_module(
    source: str,
    *,
    baseline_source: str,
    genome_path: Path,
) -> None:
    """Reject candidate modules that violate the bounded CleanLoop contract."""
    candidate_tree = ast.parse(source, filename=str(genome_path))
    baseline_tree = ast.parse(baseline_source, filename=str(genome_path))

    if _module_imports(candidate_tree) != _module_imports(baseline_tree):
        raise ValueError("candidate must preserve module imports; mutate clean() only")

    if _top_level_definition_names(candidate_tree) != _top_level_definition_names(
        baseline_tree
    ):
        raise ValueError(
            "candidate must keep the same top-level functions; mutate clean() only"
        )

    candidate_clean = _find_clean_function(candidate_tree)
    baseline_clean = _find_clean_function(baseline_tree)
    if candidate_clean is None or baseline_clean is None:
        raise ValueError("candidate must define clean(input_dir, output_path)")

    if ast.dump(candidate_clean.args, include_attributes=False) != ast.dump(
        baseline_clean.args,
        include_attributes=False,
    ):
        raise ValueError(
            "candidate must preserve the clean(input_dir, output_path) signature"
        )


def _module_imports(tree: ast.Module) -> list[str]:
    """Return a normalized list of top-level import statements."""
    imports: list[str] = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            imports.append(ast.dump(node, include_attributes=False))
            continue
        if isinstance(node, ast.ImportFrom):
            if node.module == "cleanloop.clean_data_runtime":
                normalized_aliases: list[str] = []
                for alias in node.names:
                    if alias.asname == "_runtime_clean" and alias.name in {
                        "clean",
                        "clean_starter",
                    }:
                        normalized_aliases.append("runtime_clean_alias")
                    else:
                        normalized_aliases.append(
                            ast.dump(alias, include_attributes=False)
                        )
                imports.append(
                    f"ImportFrom(module='cleanloop.clean_data_runtime', names={normalized_aliases})"
                )
                continue
            imports.append(ast.dump(node, include_attributes=False))
    return imports


def _top_level_definition_names(tree: ast.Module) -> list[str]:
    """Return top-level function names in source order."""
    names: list[str] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            names.append(node.name)
        elif isinstance(node, ast.ClassDef):
            names.append(node.name)
    return names


def _find_clean_function(
    tree: ast.Module,
) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    """Return the top-level clean function when present."""
    for node in tree.body:
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == "clean"
        ):
            return node
    return None
