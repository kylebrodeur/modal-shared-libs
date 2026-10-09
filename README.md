# modal-shared-libs

The Modal Toolkit family's **shared library home**: stdlib-first modules
every package (and every overlay lane) can consume anywhere — no Modal, no
framework dependencies.

| Module | Purpose |
| :--- | :--- |
| `libs/hooks.py` | The lifecycle hook seam: per-consumer closed tag sets, `@on(tag)` / `register()`, ordered multi-registration, contained + reported errors |

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
`modal-vision-server`, `modal-finetune-server`, `modal-vault-server`, and
`modal-toolkit` — each carries the vendored `libs/hooks.py`. The five
packages instantiate their own hook seam and document their closed tag
sets in a "Lifecycle hooks" README section (`modal-toolkit` vendors the
module as a target but fires no tag set of its own).

A vendored file's header names the canonical home:

```
Vendored from modal-shared-libs (libs/hooks.py) by mtk libs sync:
family repo: <package>, md5 <hash>. Canonical source of truth;
report fixes there, not here.
```

Hand-editing a vendored copy is drift — CI fails the tree.

## Writing code on the hooks seam

```python
from libs.hooks import Hooks

hooks = Hooks(("request.pre", "request.post"), name="embedding")  # the consumer's closed tag set


@hooks.on("request.pre")
def authz(scope, request): ...


hooks.fire("request.pre", scope, request)  # ordered; errors contained + recorded
```

Contract guarantees: unknown tags refuse; a broken hook degrades that
lane only (never the host); multiple lanes' hooks coexist in
registration order; the tag list changes only in the consumer's
releases.

## Testing

```bash
uv run pytest tests -q
```

## License

Apache-2.0 — part of the Modal Toolkit family
(https://github.com/kylebrodeur/modal-toolkit).