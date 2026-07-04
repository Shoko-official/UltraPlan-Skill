# AGENTS.md
# Source: https://github.com/Shoko-official/UltraPlan-Skill
#
# This file is a Codex instruction artifact for the UltraPlan skill.
# It is private -- add /AGENTS.md to .git/info/exclude before using.
# Do not commit this file.

## Project context

<!-- Fill in: short architecture summary, goal of the current session, stack, services. -->

## Commands

- Install: <!-- e.g. npm install / pip install -e . / go mod tidy -->
- Test: <!-- e.g. npm test / pytest / go test ./... -->
- Lint: <!-- e.g. eslint . / ruff check . / golangci-lint run -->
- Typecheck: <!-- e.g. tsc --noEmit / mypy . -->
- Build: <!-- e.g. npm run build / go build ./... -->

## Code style

- English identifiers, filenames, comments, and commit messages.
- Minimal comments. Prefer self-explanatory names and small functions.
- Follow existing repository conventions when they differ.

## Testing

- Add or update tests for every behavior touched.
- Choose coverage targets from risk, not from a fixed number.
- Prefer behavior tests over implementation tests.

## PR rules

- Keep diffs reviewable. One concern per PR.
- State the problem, approach, validation, and rollback plan in the PR body.
- Do not stage `.ultraplan/` or `.codex/ultraplan/` files.
- Do not stage this file.

## UltraPlan coordination

- Active plan: `.ultraplan/plan.md`
- Worklog: `.ultraplan/worklog.md`
- Issue files: `.ultraplan/issues/`
- Milestone files: `.ultraplan/milestones/`
- All of the above are git-ignored via `.git/info/exclude`.
