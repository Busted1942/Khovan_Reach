# CODEX.md — Khovan Reach

**`AGENTS.md` in this directory is the single governing control file for this repo — read it before any artifact-changing work.**

This file exists for the same reason `CLAUDE.md` does: some coding-agent tools look for a tool-named entry file at the repo root, and this repo's actual rules should never fork across tool-specific copies. This file carries no rules of its own. Every rule lives in `AGENTS.md` — source authority, work boundaries, orientation and repo shape, MAST-writing rules, evidence classes, Git/branch discipline, and the operator test-expectation format.

`AGENTS.md` is itself a filename many coding-agent tools, including Codex-style CLIs, already treat as a default context file — so this stub may be redundant with what Codex auto-loads. It costs nothing to keep either way, and it guarantees a Codex session that goes looking for a `CODEX.md` by name finds the same governing rules instead of nothing.
