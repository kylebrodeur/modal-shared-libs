---
name: shared-libs-module-authoring
description: Use when changing libs/hooks.py, cutting a modal-shared-libs release, or when mtk libs check rejects a vendored copy. Author or upgrade shared stdlib modules in the canonical home, refresh vendored copies, keep the parity contract.
license: Apache-2.0
metadata:
  author: kylebrodeur
  family: modal-toolkit
  repo: modal-shared-libs
---

# shared-libs: the canonical module home

This repo owns the family's shared stdlib modules. The current
resident: `libs/hooks.py` (the lifecycle seam).

**The golden rule: fixes land HERE, not in vendored copies.** A vendored
copy hand-edit = drift = refused by `mtk libs check`.

## Making a change

1. Edit `libs/hooks.py` (stdlib-only; no Modal, no framework imports).
2. `uv run pytest tests -q` (9 hooks tests) + `uv run ruff check .` +
   `uv run ruff format --check .` (line-length 120 config in
   pyproject; vendored consumers copy the BYTES = they need this exact
   format to pass their own format floors).
3. Cut the release: bump `pyproject` version + `uv.lock` self-version,
   commit, tag `vX.Y.Z`, `gh release create` with real notes (see the
   family release conventions).
4. Propagate: from the modal-toolkit sibling run `mtk libs sync`
   (refreshes ALL consumers; every package's tree goes byte-identical
   again) then per-repo suites + `mtk libs check`.

## API contract (do not break)

- Hooks(tags, name): closed tag set per consumer; registering an
  undeclared tag raises ValueError("unknown hook tag").
- fire(tag, *args): ordered; errors contained + reported via
  last_errors(tag); returns the list of contained ERROR strings (handler
  return values are discarded).
- Two registration forms: @hooks.on(tag) decorator +
  hooks.register(tag, fn); registrations coexist in call order.
- New tags = the CONSUMER's release (its tag set is closed); the
  module only carries the mechanism.
