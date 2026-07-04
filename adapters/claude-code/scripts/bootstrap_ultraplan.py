#!/usr/bin/env python3
"""Bootstrap a private Ultraplan workspace inside a Git repository."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

BEGIN_MARKER = "# >>> ultraplan-engineering private artifacts"
END_MARKER = "# <<< ultraplan-engineering private artifacts"

BASE_PATTERNS = [
    "/.ultraplan/",
    "/.codex/ultraplan/",
    "/.claude/agents/ultraplan-*.md",
]


def run_git(repo: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {message}")
    return result


def find_repo(start: Path) -> tuple[Path, Path]:
    root_result = run_git(start, ["rev-parse", "--show-toplevel"])
    root = Path(root_result.stdout.strip()).resolve()
    common_result = run_git(root, ["rev-parse", "--git-common-dir"])
    common_raw = common_result.stdout.strip()
    common = Path(common_raw)
    if not common.is_absolute():
        common = (root / common).resolve()
    return root, common


def ensure_exclude(common_dir: Path, patterns: list[str]) -> Path:
    info_dir = common_dir / "info"
    info_dir.mkdir(parents=True, exist_ok=True)
    exclude_path = info_dir / "exclude"
    existing = exclude_path.read_text(encoding="utf-8") if exclude_path.exists() else ""
    block = BEGIN_MARKER + "\n" + "\n".join(patterns) + "\n" + END_MARKER

    if BEGIN_MARKER in existing and END_MARKER in existing:
        before, rest = existing.split(BEGIN_MARKER, 1)
        _, after = rest.split(END_MARKER, 1)
        new_content = before.rstrip() + "\n\n" + block + after
    else:
        sep = "" if not existing else "\n" if existing.endswith("\n") else "\n\n"
        new_content = existing + sep + block + "\n"

    exclude_path.write_text(new_content, encoding="utf-8")
    return exclude_path


def is_tracked(root: Path, relative_path: str) -> bool:
    result = run_git(root, ["ls-files", "--error-unmatch", "--", relative_path], check=False)
    return result.returncode == 0


def write_file(root: Path, relative_path: str, content: str, force: bool, created: list[str], skipped: list[str]) -> None:
    if is_tracked(root, relative_path):
        skipped.append(f"{relative_path} is tracked")
        return

    path = root / relative_path
    if path.exists() and not force:
        skipped.append(f"{relative_path} exists")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    created.append(relative_path)


def ensure_dirs(root: Path, dirs: list[str]) -> None:
    for item in dirs:
        (root / item).mkdir(parents=True, exist_ok=True)


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def file_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def plan_template() -> str:
    return dedent(
        """
        # Ultraplan

        ## Mission
        To be defined from the current engineering goal.

        ## Assumptions
        - Add assumptions here when the grill-me intake is skipped or incomplete.

        ## Milestones
        | Milestone | Outcome | Issues | Exit gate |
        | --- | --- | --- | --- |

        ## Issue sequence
        | Issue | Branch | MR/PR | Status |
        | --- | --- | --- | --- |

        ## Validation strategy
        Define tests, coverage target, and manual checks from risk.

        ## Risks
        | Risk | Impact | Mitigation | Reopen trigger |
        | --- | --- | --- | --- |
        """
    )


def readme_template() -> str:
    return dedent(
        """
        # Ultraplan private workspace

        This directory is a local coordination system for complex engineering work.
        It is intentionally ignored through `.git/info/exclude` and must not be committed.

        Suggested contents:

        - `plan.md`: current execution plan.
        - `issues/`: issue specs.
        - `milestones/`: milestone specs.
        - `prs/`: MR/PR drafts.
        - `worklogs/`: append-only session logs.
        - `decisions/`: decision records.
        - `automations/`: local helper automation.
        - `subagents/`: subagent specs or drafts.
        - `skills/`: project-specific skill drafts.
        - `checks/`: validation notes and command output summaries.
        """
    )


def worklog_template(timestamp: str) -> str:
    return dedent(
        f"""
        # Worklog

        ## {timestamp} bootstrap

        ### Context
        Created private Ultraplan coordination workspace.

        ### Actions
        - Installed ignore patterns in Git local exclude.
        - Created initial planning directories and templates.

        ### Results
        - Ready for issue -> milestone -> MR/PR planning.

        ### Next
        - Map repository context.
        - Run grill-me intake or write assumptions lock.
        - Create milestone and issue graph.
        """
    )


def assumptions_template() -> str:
    return dedent(
        """
        # Assumptions lock

        ## Chosen assumptions
        - Add assumptions here.

        ## Risks created by these assumptions
        - Add risks here.

        ## Decisions made autonomously
        - Add decisions here.

        ## Reopen triggers
        - Add triggers here.
        """
    )


def risk_template() -> str:
    return dedent(
        """
        # Risk register

        | Risk | Impact | Likelihood | Mitigation | Owner | Status |
        | --- | --- | --- | --- | --- | --- |
        """
    )


def decision_template() -> str:
    return dedent(
        """
        # Decision log

        | ID | Date | Decision | Rationale | Status |
        | --- | --- | --- | --- | --- |
        """
    )


def claude_agent_templates() -> dict[str, str]:
    return {
        "ultraplan-codebase-researcher.md": dedent(
            """
            ---
            name: ultraplan-codebase-researcher
            description: Read-only codebase researcher for architecture, dependencies, tests, and risk discovery before implementation.
            tools: Read, Grep, Glob, Bash
            model: sonnet
            ---
            You are a codebase research specialist. Map only the facts needed for the current issue. Return concise findings, relevant paths, commands discovered, risks, and open questions. Do not edit files.
            """
        ),
        "ultraplan-test-engineer.md": dedent(
            """
            ---
            name: ultraplan-test-engineer
            description: Designs and audits tests, coverage targets, fixtures, and validation strategy for high-risk engineering work.
            tools: Read, Grep, Glob, Bash, Edit, Write
            model: sonnet
            ---
            You are a pragmatic test engineer. Prefer behavior tests over implementation tests. Choose coverage targets from risk. Add or update focused tests when useful. Avoid brittle tests that only satisfy a number.
            """
        ),
        "ultraplan-reviewer.md": dedent(
            """
            ---
            name: ultraplan-reviewer
            description: Reviews diffs for correctness, maintainability, security, rollback, and MR/PR readiness after implementation.
            tools: Read, Grep, Glob, Bash
            model: sonnet
            ---
            You are a skeptical senior reviewer. Inspect the diff against the issue and acceptance criteria. Report blockers, risky assumptions, missing tests, and simplifications. Do not edit files.
            """
        ),
    }


def codex_agents_template() -> str:
    return dedent(
        """
        # AGENTS.md

        ## Project context
        This local file supports Ultraplan engineering sessions. Keep it private unless the team explicitly adopts it.

        ## Commands
        - Discover install, test, lint, typecheck, build, and migration commands from repository files before editing.
        - Run focused checks first, then broaden checks according to risk.

        ## Code style
        - Use English identifiers, filenames, comments, commit messages, and PR text unless repository convention differs.
        - Keep comments minimal and useful.
        - Follow existing project conventions over generic preferences.
        - Avoid decorative comments, em dashes, and emojis.

        ## Testing
        - Add or update tests for touched behavior.
        - Choose coverage target from risk.
        - Prefer behavior tests over implementation tests.

        ## PR rules
        - Keep diffs reviewable and scoped to an issue.
        - Explain validation and rollback.
        - Do not stage `.ultraplan/`, `.codex/ultraplan/`, or `.claude/agents/ultraplan-*`.
        """
    )


def create_workspace(root: Path, profile: str, codex_manifest: str, force: bool) -> tuple[list[str], list[str]]:
    created: list[str] = []
    skipped: list[str] = []
    timestamp = now_stamp()

    ensure_dirs(
        root,
        [
            ".ultraplan/issues",
            ".ultraplan/milestones",
            ".ultraplan/prs",
            ".ultraplan/worklogs",
            ".ultraplan/decisions",
            ".ultraplan/risks",
            ".ultraplan/automations",
            ".ultraplan/subagents",
            ".ultraplan/skills",
            ".ultraplan/checks",
            ".ultraplan/codex",
        ],
    )

    write_file(root, ".ultraplan/README.md", readme_template(), force, created, skipped)
    write_file(root, ".ultraplan/plan.md", plan_template(), force, created, skipped)
    write_file(root, ".ultraplan/assumptions.md", assumptions_template(), force, created, skipped)
    write_file(root, ".ultraplan/risk-register.md", risk_template(), force, created, skipped)
    write_file(root, ".ultraplan/decision-log.md", decision_template(), force, created, skipped)
    write_file(
        root,
        ".ultraplan/state.json",
        json.dumps({"created_at": timestamp, "profile": profile, "version": 1}, indent=2),
        force,
        created,
        skipped,
    )
    write_file(root, f".ultraplan/worklogs/{file_stamp()}-bootstrap.md", worklog_template(timestamp), False, created, skipped)

    if profile in {"claude", "both"}:
        for filename, content in claude_agent_templates().items():
            write_file(root, f".claude/agents/{filename}", content, force, created, skipped)

    if profile in {"codex", "both"}:
        if codex_manifest == "root":
            write_file(root, "AGENTS.md", codex_agents_template(), force, created, skipped)
        elif codex_manifest == "proposal":
            write_file(root, ".codex/ultraplan/AGENTS.md", codex_agents_template(), force, created, skipped)
            write_file(root, ".ultraplan/codex/AGENTS.md", codex_agents_template(), force, created, skipped)

    return created, skipped


def audit_ignored(root: Path, paths: list[str]) -> list[str]:
    failures: list[str] = []
    for relative_path in paths:
        if not (root / relative_path).exists():
            continue
        if is_tracked(root, relative_path):
            continue
        result = run_git(root, ["check-ignore", "-q", "--", relative_path], check=False)
        if result.returncode != 0:
            failures.append(relative_path)
    return failures


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap a private Ultraplan workspace.")
    parser.add_argument("--repo", default=".", help="Path inside the target Git repository.")
    parser.add_argument("--profile", choices=["both", "claude", "codex", "none"], default="both")
    parser.add_argument("--codex-manifest", choices=["proposal", "root", "none"], default="proposal")
    parser.add_argument("--force", action="store_true", help="Overwrite existing untracked private files.")
    parser.add_argument("--audit", action="store_true", help="Only audit ignore visibility after ensuring exclude patterns.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    start = Path(args.repo).resolve()

    try:
        root, common_dir = find_repo(start)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        print("The path must be inside a Git repository to use .git/info/exclude.", file=sys.stderr)
        return 2

    patterns = list(BASE_PATTERNS)
    if args.codex_manifest == "root" and args.profile in {"codex", "both"}:
        patterns.append("/AGENTS.md")

    exclude_path = ensure_exclude(common_dir, patterns)
    created: list[str] = []
    skipped: list[str] = []

    if not args.audit:
        created, skipped = create_workspace(root, args.profile, args.codex_manifest, args.force)

    audit_paths = [
        ".ultraplan/plan.md",
        ".codex/ultraplan/AGENTS.md",
        ".ultraplan/codex/AGENTS.md",
        ".claude/agents/ultraplan-codebase-researcher.md",
    ]
    if args.codex_manifest == "root" and args.profile in {"codex", "both"}:
        audit_paths.append("AGENTS.md")

    failures = audit_ignored(root, audit_paths)

    print(f"Repository: {root}")
    print(f"Local exclude: {exclude_path}")
    if created:
        print("Created:")
        for item in created:
            print(f"  {item}")
    if skipped:
        print("Skipped:")
        for item in skipped:
            print(f"  {item}")
    if failures:
        print("Ignore audit failed:")
        for item in failures:
            print(f"  {item}")
        return 1

    print("Ignore audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
