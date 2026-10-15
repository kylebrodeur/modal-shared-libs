# Security Policy

## Supported Versions

| Version | Supported |
| :--- | :--- |
| main | latest |
| older tags | best-effort (backport security fixes as needed) |

## Reporting a Vulnerability

**Do not open a public issue for a security vulnerability.**

Use GitHub's **Private Vulnerability Reporting** to reach the maintainer:

1. Go to the **Security** tab in this repository.
2. Click **"Report a vulnerability."**
3. Provide a clear description, reproduction steps, and impact assessment.

You'll receive an acknowledgment within 72 hours. If you don't hear back,
follow up via the contact info on the maintainer's profile.

## Scope Notes

This repo is a **library** (no server, no endpoints): the interesting
surface is the extension-seam contract. Reports especially welcome:

- A way a registered hook handler could crash or corrupt the host
  (containment is the contract: `fire()` records, never raises).
- A way a vendored copy could drift from the canonical source silently
  (the md5 parity in `mtk libs check` is the guard).
- Any code path here that reaches disk, the network, or process
  execution (the module is stdlib-only and touches none).

## Disclosure Process

- We'll triage the report, confirm the issue, and work on a fix.
- We'll ask for a coordinated disclosure embargo (60-120 days typical).
- We'll credit the reporter in the security advisory and release notes
  unless you prefer to stay anonymous.