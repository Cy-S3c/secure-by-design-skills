# Threat model summary — Acme Scheduler v0.1.0 (2026-10-29)

Source: planning suite v1.0.0-draft (docs 03, 04, 05, 07, 08). Elements 7, flows 6 (4 cross-boundary), threats 3, coverage gaps 42.

| Band | Count |
|---|---|
| Critical | 0 |
| High | 1 |
| Medium | 2 |
| Low | 0 |

## Open Critical / High

none

## Summary

The design covers the main entry points well; the open items concern the job queue and operational hardening.

## Decisions needed

1. Fund Redis authentication and worker re-authorization before the first customer tenant goes live. — owner Product owner, by S03 planning

## By owner and status

| Owner | open | mitigated | accepted | transferred |
|---|---|---|---|---|
| Backend lead | 1 | 2 | 0 | 0 |

Explicit no-threat decisions: 1.

## All threats

| ID | Target | Cat | Title | L×I | Band | Status | Owner |
|---|---|---|---|---|---|---|---|
| T-1 | E-1 | S | Session cookie theft via XSS | 3×4 | High | mitigated | Backend lead |
| T-2 | F-5 | T | Forged job payload in the queue | 2×4 | Medium | open | Backend lead |
| T-3 | P-2 | D | Unbounded list endpoints | 4×2 | Medium | mitigated | Backend lead |

## Coverage gaps

- E-1 × Repudiation
- E-2 × Spoofing
- P-1 × Spoofing
- P-1 × Tampering
- P-1 × Repudiation
- P-1 × Information disclosure
- P-1 × Denial of service
- P-1 × Elevation of privilege
- P-2 × Spoofing
- P-2 × Tampering
- P-2 × Repudiation
- P-2 × Information disclosure
- P-2 × Elevation of privilege
- P-3 × Spoofing
- P-3 × Tampering
- P-3 × Repudiation
- P-3 × Information disclosure
- P-3 × Denial of service
- P-3 × Elevation of privilege
- D-1 × Tampering
- D-1 × Information disclosure
- D-1 × Denial of service
- D-2 × Tampering
- D-2 × Information disclosure
- D-2 × Denial of service
- F-1 × Tampering
- F-1 × Information disclosure
- F-1 × Denial of service
- F-2 × Tampering
- F-2 × Information disclosure
- F-2 × Denial of service
- F-3 × Tampering
- F-3 × Information disclosure
- F-3 × Denial of service
- F-4 × Tampering
- F-4 × Information disclosure
- F-4 × Denial of service
- F-5 × Information disclosure
- F-5 × Denial of service
- F-6 × Tampering
- F-6 × Information disclosure
- F-6 × Denial of service

## Divergences

- **V-1** (08 §7.1 vs 13 §3.1) 08 says the CSP has no inline script; the shipped env default allows 'unsafe-inline'. → Tighten the default; owner Backend lead
