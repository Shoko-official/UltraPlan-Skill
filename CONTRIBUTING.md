# Contributing to UltraPlan-Skill

Thank you for your interest in improving UltraPlan.

## How to contribute

1. **Open an issue first.** Describe the problem or improvement before writing code. This avoids wasted effort.

2. **Fork the repo** and create a branch from `main`:
   ```
   git checkout -b feat/short-description
   ```

3. **Make your change.** Keep diffs focused -- one concern per PR.

4. **Test your change.** If you modify `scripts/bootstrap_ultraplan.py`, verify it runs without errors on at least one Python 3.9+ environment. If you modify `SKILL.md` or the references, test the skill in your target AI runtime.

5. **Open a pull request** against `main`. Include:
   - What problem the PR solves
   - How you validated the change
   - Any risks or rollback notes

## Skill file conventions

- `SKILL.md` frontmatter must keep `name` and `description` fields -- these are the trigger-match fields for AI runtimes.
- Reference files in `references/` use plain Markdown. Keep them under 500 lines.
- Scripts in `scripts/` must be idempotent and support a `--dry-run` mode where state changes are possible.
- Use English for all identifiers, filenames, and comments.
- Avoid decorative comments, emojis in code, or em dashes in engineering artifacts.

## Reporting bugs

Open an issue with:
- The AI runtime and version you used
- The exact trigger or prompt
- What you expected vs what happened
- Any relevant output or logs

## License

By contributing, you agree your contributions are licensed under the MIT License.
