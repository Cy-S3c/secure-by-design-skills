# 05 — API Documentation

| | |
|---|---|
| **Document ID** | {{PREFIX}}-API-001 |
| **Product** | {{PRODUCT}} (working codename `{{CODENAME}}`) |
| **Version** | 1.0.0-draft |
| **Status** | Pending approval |
| **Owner** | Backend lead |
| **Last updated** | {{DATE}} |
| **Audience** | Backend, frontend, QA, integrators, security review |
| **Depends on** | `00-canonical-model.md` §3, §4, §6, `04-data-model.md`, `07-user-roles-and-permissions.md` §4, `06-features-and-functions.md` |
| **Consumed by** | `03-architecture.md`, `08-security-design.md`, `12-frontend-screen-specifications.md`, `09-development-plan.md` |
| **Machine-readable artifacts** | `api/openapi.yaml` (OpenAPI 3.1; skeleton pre-build, parity with §3 by the first API sprint), `api/postman_collection.json` |

> **Purpose.** The contract humans read. It owns the problem types, the
> event envelope and the event catalogue. It is **not** the permission
> matrix (07) or the storage design (04); it states the permission gate per
> endpoint. Vocabulary follows `00-canonical-model.md`.

---

## Table of Contents

---

## 1. Overview

### 1.1 Conventions (from `00-canonical-model.md` §6)

<!-- Repeat only what the API adds: header names, envelope examples. Personal or sensitive data never appears in URLs or query strings; filtered searches over such data are `POST /<resources>/search`. -->

### 1.2 Optimistic concurrency (`ETag` / `If-Match`, 412 on mismatch)
### 1.3 Rate limiting

## 2. Authentication & Authorization

### 2.1 Authentication model
### 2.2 Login flow (with MFA)
### 2.3 Auth endpoints
### 2.4 Token lifecycle (00 §10 PRM-n)
### 2.5 Scope model

<!-- Minimal profile without 07: the role → permission table lives here. -->

### 2.6 401 vs 403 vs 404-on-invisible

## 3. Endpoint Catalogue

Legend — **Idempotent?**: `—` safe method · `Key` mutation, `Idempotency-Key` required · `Yes` inherently idempotent · `Safe-POST` read-only POST (search). Paths relative to `/api/v1`; `{…}` are UUID v7 ids.

### 3.1 `<resource>` — <purpose>

| Method | Path | Description | Permission (`x-permission` / `x-scope`) | Idempotent? |
|---|---|---|---|---|
| GET | `/<resources>` | List (`?cursor=&limit=`; no personal data in filters) | `resource.view` / tenant | — |
| POST | `/<resources>/search` | Filtered search with body filters | `resource.view` / tenant | Safe-POST |
| POST | `/<resources>` | Create | `resource.manage` / tenant | Key |
| GET | `/<resources>/{id}` | Detail | `resource.view` / assigned | — |
| PATCH | `/<resources>/{id}` | Update (`If-Match` required) | `resource.manage` / assigned | Key |
| DELETE | `/<resources>/{id}` | Soft-delete | `resource.manage` / assigned | Yes |
| POST | `/<resources>/{id}/transitions` | State transition `{ "action": "submit", "notes": "" }` | per transition | Key |

<!-- One subsection per module in 03 §3; every FR with an API surface appears. -->

## 4. Schemas (representative payloads)

### 4.1 `<Entity>`

```json
{ "id": "018f…", "status": "DRAFT", "created_at": "2026-10-26T09:41:02Z" }
```

### 4.n Error — RFC 9457 problem+json
### 4.n Pagination envelope

## 5. Error Catalogue

All errors are `application/problem+json`; `type` is a stable URN — clients switch on `type`, never on `detail`.

| `type` (urn:{{CODENAME}}:problem:…) | HTTP | When |
|---|---|---|
| `auth-required` | 401 | No credentials on a protected endpoint |
| `auth-invalid` | 401 | Bad / expired / revoked token |
| `forbidden` | 403 | Role or scope denies the action on a visible object |
| `not-found` | 404 | Missing **or** invisible to the caller |
| `validation` | 422 | Schema or business validation failure |
| `conflict` | 409 | State-machine violation or duplicate resource |
| `precondition-failed` | 412 | `If-Match` does not match the current `ETag` (extension `current_etag`) |
| `precondition-required` | 428 | Mutation without `If-Match` where required (RFC 6585) |
| `idempotency-key-required` | 400 | Mutation without `Idempotency-Key` (IETF idempotency draft) |
| `idempotency-mismatch` | 422 | `Idempotency-Key` reused with a different request body |
| `rate-limited` | 429 | `Retry-After` present |

## 6. Webhooks & Events

### 6.1 Event envelope (owned here; 03 §3 cites it)

```json
{ "event_id": "…", "stream": "…", "type": "module.entity.verb", "actor_id": "…", "resource_type": "…", "resource_id": "…", "before": {}, "after": {}, "occurred_at": "…", "trace_id": "…" }
```

### 6.2 Delivery semantics (signing, retries, ordering)
### 6.3 Event catalogue

## 7. External Surface Isolation (portal / partner API, if any)

## 8. Versioning & Deprecation Policy

## 9. OpenAPI & Collections

<!-- Every operation carries `operationId`, `x-permission` (one permission string, or `none` for unauthenticated operations) and `x-scope` (`tenant` | `assigned` | `own` | `public`); transition routes list the permission per action in the description. -->

## 10. Open Items

1. <question>? — *default: <default>*.
