# 10 — <Domain Specification name>

| | |
|---|---|
| **Document ID** | {{PREFIX}}-DOM-001 |
| **Product** | {{PRODUCT}} |
| **Version** | 1.0.0-draft |
| **Status** | Pending approval |
| **Owner** | Domain lead |
| **Last updated** | {{DATE}} |
| **Audience** | Product, engineering, domain reviewers |
| **Derived from** | <sample corpus / published standards / research notes in `docs/research/`; or "greenfield — published rules, validated against pilot samples (§7)"> |
| **Depends on** | `00-canonical-model.md`; `07-user-roles-and-permissions.md` §4 when fields are permission-gated |
| **Consumed by** | `04-data-model.md`, `06-features-and-functions.md`, `05-api-documentation.md` |

> **Purpose.** The product's domain standard: <a report format, a form
> schema, a message standard, a protocol>, versioned as a standard of its
> own. It owns the domain keys and presets it introduces (`conventions.md` §5);
> entities and enums it needs are defined in `00-canonical-model.md`. It is
> **not** the data model or the feature specification. When the product has
> several sub-standards, repeat §2–§7 once per sub-standard.

---

## 1. Sources and Method

<!-- What was studied (count, provenance) and how the structure was derived. Greenfield: which published rules it derives from, and the validation gate (how many real samples, by when) before it is called conformant. -->

## 2. Structure

| # | Section / element | Required | Content | Computed from |
|---|---|---|---|---|

## 3. Record Schema

| Field | Type | Required | Validation | Classification / visibility |
|---|---|---|---|---|

## 4. Computed Values, Bands and Rules

<!-- Score → band mappings, colours, ordering, totals never hand-entered. Document-local rule ids (R-1…) are declared here and cited only inside this document. -->

## 5. Variants / Profiles

## 6. Generation / Rendering Contract

### 6.1 Inputs
### 6.2 Output formats and fidelity requirements
### 6.3 Acceptance criteria

- **Given** <input>, **when** <generated>, **then** <observable property>.

## 7. Release Gate

<!-- What must be true before a generated artifact is conformant; for greenfield, the pilot validation. -->

## 8. Open Items

1. <question>? — *default: <default>*.
