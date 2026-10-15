# Contributing

Thanks for your interest. This library is the Modal Toolkit family's shared
home: stdlib-only modules vendored verbatim into every consuming package and
parity-checked there. This repo's CONTRIBUTING narrows the
[family defaults](https://github.com/kylebrodeur/.github/blob/main/CONTRIBUTING.md)
to what is specific here.

## What belongs in this repo

A module goes here when TWO OR MORE family members need the exact same
bytes: the lifecycle hooks seam is the founding example. A module for one
consumer belongs in that consumer; a module for "the family, sort of" is
not here until the second real consumer exists.

## The vendoring contract (the rule changes never break)

- Vendored copies are byte-identical to the canonical source here. NEVER
  edit a vendored copy in a consuming repo; fix here, release, and the
  consumers refresh (`mtk libs sync`, md5-parity via `mtk libs check`).
- Public API of a vendored module changes only in a minor+ release with
  the consumers' pins moving deliberately.
- Every vendored file's header names this repo as the canonical home;
  fixes report here, not in the vendored copy.

## Ground rules specific to this repo

- **Stdlib only.** No Modal, no framework, no third-party imports: the
  module must work inside Modal containers, overlay lanes, laptops, and
  plain Python consumers alike.
- **Contained errors.** Extension-seam handlers must never be able to
  break the host (`fire()` records errors; the host decides policy).
- The repo has no Modal code at all: CI is pytest + ruff only.

## Workflow

1. Fork + branch.
2. `uv sync`; add tests under `tests/` covering the module contract
   (behavior, boundaries, real errors).
3. `uv run pytest tests -q` and `uv run ruff check .` green.
4. PR against `main`. A release cuts after two consumers verify.

The project is Apache-2.0; by contributing you agree your contributions
are licensed under its terms.