# modal-shared-libs

The Modal Toolkit family's **shared library home**: stdlib-first modules
every package (and every overlay lane) can consume anywhere - no Modal, no
framework dependencies.

| Module | Purpose |
| :--- | :--- |
| `libs/hooks.py` | The lifecycle hook seam: per-consumer closed tag sets, `@on(tag)` / `register()`, ordered multi-registration, contained + reported errors |

## Docs

This repo has no `docs/` tree: this README is its only doc, and the
source docstring (`libs/hooks.py`) stays authoritative. Each consuming
package documents its own closed tag set in a "Lifecycle hooks" section
of its README.

## Install

```bash
uv pip install modal-shared-libs   # or vendor (below)
```

## Vendoring (the family pattern)

Packages do NOT take a runtime dependency: shared modules are vendored
**verbatim** into the package tree and refreshed by the toolkit:

```bash
mtk libs sync            # refresh vendored copies from this repo
mtk libs check           # parity-check every vendored module (md5); CI runs it
```

Vendoring targets: `modal-embedding-server`, `modal-inference-server`,
`modal-vision-server`, `modal-finetune-server`, `modal-vault-server`,
`modal-victoriametrics-server`, and `modal-toolkit` - each carries the
vendored `libs/hooks.py`. The five packages instantiate their own hook seam
and document their closed tag sets in a "Lifecycle hooks" README section
(`modal-toolkit` vendors the module as a target but fires no tag set of
its own).

A vendored file's header names the canonical home:

```
Vendored from modal-shared-libs (libs/hooks.py) by mtk libs sync:
family repo: <package>, md5 <hash>. Canonical source of truth;
report fixes there, not here.
```

Hand-editing a vendored copy is drift - CI fails the tree.

## Writing code on the hooks seam

```python
from libs.hooks import Hooks

hooks = Hooks(("request.pre", "request.post"), name="embedding")  # the consumer's closed tag set


@hooks.on("request.pre")
def authz(scope, request): ...


# dynamic form (same registry): hooks.register("request.pre", fn)

hooks.fire("request.pre", scope, request)  # ordered; errors contained + recorded
```

An overlay lane consumes the package's own instance, not a private one:
the package constructs its hook seam (say `Hooks(("boot.pre", "boot.post"), name="victoriametrics")`)
and an overlay registers on the same closed tag set from deploy-side
code, so the lane's hooks run inside the package's fires without a
source edit (see any package README's "Lifecycle hooks" section for
that package's authoritative tags).

Contract guarantees: unknown tags refuse; a broken hook degrades that
lane only (never the host); multiple lanes' hooks coexist in
registration order; the tag list changes only in the consumer's
releases. Every fire's errors are contained and reported: `fire(tag, ...)` returns
the error strings and `last_errors(tag)` keeps the latest
fire's errors for health-style reporting (both refuse undeclared tags);
`unregister(tag, fn)` is an idempotent no-op for a missing handler and
`registered(hooks, tag, fn)` yields scoped one-off registration that
unregisters on exit.

## Testing

```bash
uv run pytest tests -q
```

## License

Apache-2.0 - part of the Modal Toolkit family
(https://github.com/kylebrodeur/modal-toolkit).