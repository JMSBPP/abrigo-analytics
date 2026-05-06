---
name: Schema-stability pre-flights MUST verify value-content not just headers
description: NON-NEGOTIABLE — any schema-stability pre-flight on multi-source data (DANE GEIH, central bank series, etc.) must verify BOTH column-header names AND sample value-content against a published codebook. Header-only verification is necessary but not sufficient and has produced 1 BLOCK-class failure (CORRECTIONS-α invalidated by Empalme RAMA4D-as-Rev.3 contents).
type: feedback
originSessionId: d1cfac41-85eb-4cae-ae40-bddd97fffc23
---
NON-NEGOTIABLE: schema-stability pre-flights on multi-source data must verify BOTH (a) column-header names AND (b) sample value-content per file against a published codebook (or other authoritative source for the encoding). Header-only verification is necessary but not sufficient.

**Why:** Pair D Task 1.1 Step 0 disposition memo (2026-04-28 AM) verified that GEIH Empalme files for 2010-01 + 2014-01 had columns named `RAMA4D + RAMA2D` and concluded — based on column-name inspection alone — that "DANE has done the Rev.3.1 → Rev.4 mapping inside the Empalme publishing for 2010-2014." This drove the CORRECTIONS-α v1.2 / v1.2.1 revision (spec sha256 `b90be50b…4c6d`, commit `5f3ab4d2f`). When Task 1.1 was re-dispatched and the executing DE inspected actual *value content* in those columns, the codes `5211, 9500, 6031, 8511, 1810, 8043` were CIIU **Rev.3** codes, not Rev.4 — DANE pre-applied Rev.4 only from 2015-01 onward (column rename to `RAMA4D_R4`). The CORRECTIONS-α pinned harmonization rule was factually wrong for 2010-2014. Second HALT triggered (typed exception `PairDEmpalmeSchemaContradictsHarmonizationPin`); Option α' = shorten to 2015-01 → 2026-03 became default-recommended in the new disposition memo.

The HALT discipline worked twice — both pre-flights caught what would otherwise have been silent data corruption — but the cost of the second HALT was a full CORRECTIONS-block revision cycle (spec v1.2 → v1.2.1 → v1.3 plus plan v2.2 → v2.3) that would have been avoidable had Step 0 verified value-content alongside headers.

**How to apply:**
- Any schema-stability pre-flight on data spanning multiple source-format eras MUST sample 3-5 random value-rows per identified era and cross-check the encoded values against a published codebook (DANE classification PDF, central bank series description, etc.).
- For categorical / classification fields (sector codes, occupation codes, region codes), value-content verification is the binding step — column-header verification is necessary but not sufficient.
- For continuous / numeric fields (FEX, exchange rates, prices), header-name verification + a unit-of-measurement sanity check (e.g., "values in thousands?") is usually sufficient.
- Pre-flight findings reports MUST distinguish: (a) "column header verified" from (b) "value content verified against codebook" — these are different claims and the second is harder.
- When the value-content cross-check is impossible (codebook unavailable, ambiguous), HALT and surface to user — do NOT assume header semantics imply value semantics.

**Closure cost from this lesson:** v1.2.1 → v1.3 CORRECTIONS revision; ~2-4 hours of orchestrator time to draft + 3-way review + re-pin. Well worth catching, but worth more to prevent.

**References:**
- Disposition memo for the precipitating HALT: `scratch/2026-04-28-task-1.1-step-1-empalme-rev3-vs-rev4-disposition.md`
- Prior CORRECTIONS-α memo whose Step-0 verification was insufficient: `scratch/2026-04-28-task-1.1-step-0-schema-pathological-disposition.md` §2.1 line 45 ("the 2010-01 and 2014-01 Empalme Ocupados.CSV contain RAMA4D + RAMA2D with Rev.4 a.c. codes" — verified by column-header presence only).
- Spec v1.2.1 (now sha256-superseded by next CORRECTIONS-α' revision): `docs/specs/2026-04-27-simple-beta-pair-d-design.md` (sha256 `b90be50b…4c6d`).
