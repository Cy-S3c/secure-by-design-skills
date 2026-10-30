# 13 — Operations Runbooks

| | |
|---|---|
| **Document ID** | {{PREFIX}}-OPS-001 |
| **Product** | {{PRODUCT}} |
| **Version** | 1.0.0-draft |
| **Status** | Draft |
| **Owner** | DevOps / on-call lead |
| **Last updated** | {{DATE}} |
| **Audience** | Operators running the platform; on-call |
| **Depends on** | `03-architecture.md` §9, §10, `04-data-model.md` §6, §7, `08-security-design.md` §6, §8, §10 |
| **Consumed by** | on-call, `14-admin-guide.md` |

> **Purpose.** Copy-pasteable procedures for deploying, backing up and
> recovering {{PRODUCT}}, and for responding to incidents. It is **not** the
> security policy (08) or the admin guide (14). Once code exists every
> command, env var, path and bucket name is verified against the repository
> (<list the files checked: compose file, Makefile, settings module, scripts>).
>
> **Build status (pre-build; reconciled through S00).** Skeleton: sections the
> frozen documents determine are filled; the rest are marked
> `*Filled during Sxx*`.

---

## Table of Contents

---

## 1. Topology & Ports (from `03-architecture.md` §9)

| Service | Image / runtime | Port | Depends on |
|---|---|---|---|

## 2. Deploy

### 2.1 Bring-up

```bash
<one-command boot>
```

### 2.2 Services checklist after bring-up
### 2.3 Local dev helpers

## 3. Configuration Reference

### 3.1 Application (`<PREFIX>_*`)

| Variable | Default | Secret? | Meaning |
|---|---|---|---|

### 3.2 Infrastructure

## 4. First Boot: bootstrap admin, migrations, seed

### 4.1 Bootstrap admin (`04-data-model.md` §7.1)
### 4.2 Migrations
### 4.3 Seed

## 5. Backup & Restore

### 5.1 <Database> (system of record)
### 5.2 <Object storage>
### 5.3 <Cache / broker> — what is actually lost

## 6. Incident Response

Severity classes and notification workflow: `08-security-design.md` §10. Platform-specific procedures:

### 6.1 Compromised account

Sequence (stop-the-bleed → investigate → recover):

```bash
# 1. LOCK
# 2. INVESTIGATE
# 3. RECOVER
```

### 6.2 <Integrity incident>
### 6.3 <Leak incident>

## 7. Key & Credential Rotation

### 7.1 <Session secret or token-signing key, if tokens are signed>
### 7.2 <Encryption key>
### 7.3 <Storage credentials>

## 8. <Domain-specific operations>

## 9. Monitoring, Alerting & On-call

### 9.1 Health endpoints
### 9.2 Structured logs
### 9.3 Events worth alerting on (`08-security-design.md` §8.3)
### 9.4 SLO monitoring (`03-architecture.md` §10)
### 9.5 On-call rota & escalation
### 9.6 Not yet available (planned)

## 10. Open Items

1. <question>? — *default: <default>*.
