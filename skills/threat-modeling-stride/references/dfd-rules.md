# Deriving the data-flow diagram

## Sources (greenfield: the planning suite; brownfield: suite + code)

| DFD element | Take it from |
|---|---|
| External entities | principals in `00 §2` and `00 §2.1`; third-party systems in `03 §1` context (SMTP, IdP, payment, LLM provider) |
| Processes | containers and components in `03 §1` (L2/L3), background jobs in `03 §6`; brownfield: one process per deployable unit and one per worker queue, confirmed against the compose file and the module list |
| Data stores | `03 §1` stores (database, cache/broker, object storage), `04 §8` cache keys, log and audit sinks, queues |
| Data flows | `03 §4` request lifecycle, `03 §8` data flows, `05 §3` endpoint groups (one flow per group, not per endpoint), `05 §6` webhooks, `03 §6` job triggers |
| Trust boundaries | `08 §2.3` boundaries; else: public network · ingress/DMZ · application network · data network · third parties · operator plane. Every flow that crosses one is where threats concentrate |
| Data classification | `04 §6` retention classes and the assets listed in `08 §2`: label each flow and store with the most sensitive class it carries (`public` · `internal` · `confidential` · `restricted`) |

## Levels

- **L0 context**: the system as one process, external entities around it, third parties, boundaries drawn around the system and around each external party.
- **L1 container**: every deployable unit, store and worker; boundaries as in `08 §2.3`. This is the level STRIDE is applied to.
- **L2 (optional)**: one diagram per sensitive flow (upload, render/export, auth, payment, AI inference) when the L1 flow hides several hops.

## Rules

0. The diagram is generated from the model: edges carry flow ids and the flow table is the legend; never draw by hand.

1. Every element has a stable id (`E-<n>` entity, `P-<n>` process, `D-<n>` store, `F-<n>` flow, `B-<n>` boundary) and a name identical to the one in `03`. Brownfield: when the code differs from `03`, name the element after what runs (cite `03` in `doc`) and record the difference as a divergence.
2. Every flow names protocol, direction, the data it carries and the classification; the generator marks flows that cross a boundary.
3. Every process and store sits in exactly one boundary; external entities sit in the public or third-party boundary.
4. Internal-only flows (same boundary, same classification) may be grouped. At the public edge, group by principal and surface — one flow per browser or client type per API surface (internal API, portal API, uploads) — and list the endpoint groups it carries in `data`; cross-boundary flows between processes and stores are never grouped. Fifteen browser flows make an unreadable diagram and add no threats.
5. Nothing appears on the diagram that is not in the model file, and every model element appears on the diagram — the generator fails on orphans.
6. Name the diagram's assumptions (`assumptions:` list) — "ingress terminates TLS", "workers cannot reach the internet" — because threats that depend on them become `accepted` risks if the assumption is wrong.
