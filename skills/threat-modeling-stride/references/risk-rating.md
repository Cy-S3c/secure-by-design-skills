# Risk rating

Score = **likelihood × impact**, each 1–5. Bands: **Critical** 20–25 ·
**High** 12–19 · **Medium** 6–11 · **Low** 1–5. Record both factors; the
generator computes the band and draws the heat map.

## Likelihood (how plausible within one year, given existing controls)

| Score | Meaning |
|---|---|
| 1 | needs insider with privileged access plus an unlikely chain |
| 2 | needs authenticated access and a specific misconfiguration |
| 3 | reachable by any authenticated user with moderate effort |
| 4 | reachable by an unauthenticated attacker with public tooling |
| 5 | trivially exploitable, likely automated, known active exploitation |

## Impact (worst credible outcome for the business)

| Score | Meaning |
|---|---|
| 1 | single non-sensitive record or a transient glitch |
| 2 | one user's data or hours of degraded service |
| 3 | one tenant's confidential data, or a day of outage |
| 4 | all tenants' confidential data, integrity of audit or deliverables |
| 5 | regulated data breach across tenants, legal exposure, safety impact |

Single-tenant systems: read "one tenant" as "one client's data" and "all tenants" as "the whole instance"; state the mapping in `assumptions`. Insider and operator-plane threats: rate likelihood by the number of people with the access and the controls on it (2 for a small, audited operator group; 3 when access is shared or unaudited), not by default 1.

## Status rules

- `open`: no adequate control; mitigation named and owned; `sprint` (09 row) or `plan` (BACKLOG item, ticket) set — the validator warns otherwise.
- `mitigated`: greenfield — the control exists in the design (cite `08 §n`); brownfield — it exists in the design **and** in code (cite the path). A control that is designed but absent from code is `open` with the divergence recorded.
- `accepted`: residual risk signed off by the `approver` named in the record, with a `revisit` date or trigger.
- `transferred`: handled contractually or by a provider; `agreement` names it.

A Critical or High threat may not be `accepted` without an approver named
in the record. The executive summary lists every open Critical/High first.
