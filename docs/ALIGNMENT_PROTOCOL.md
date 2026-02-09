# Cross-Linguistic Alignment Protocol

## Purpose

This document describes how `chinese_parallel` annotations in the witness data files were produced, what criteria govern them, and how they can be verified or modified. It provides the methodological transparency required for scholarly publication of the critical apparatus.

## 1. Alignment Principles

### Base Text

T251 (Xuanzang's short recension, 260 characters) serves as the analytical base. All cross-linguistic alignments point *to* T251 segments from other witnesses, never the reverse. T251 defines the segment boundaries.

### Unit of Alignment

The unit of alignment is the **segment** — a discrete text unit corresponding to one doctrinal passage. T251 is divided into 12 segments (T251:1 through T251:12), following natural breaks in content:

| Segment | Section | Content |
|---------|---------|---------|
| T251:1 | opening | Avalokiteśvara practicing prajñāpāramitā |
| T251:2 | form_emptiness | Form/emptiness equations |
| T251:3 | characteristics | Emptiness characteristics (not arising, not ceasing...) |
| T251:4 | negations_skandhas | Negation of aggregates in emptiness |
| T251:5 | negations_ayatanas | Negation of sense bases |
| T251:6 | negations_dhatus | Negation of sense realms |
| T251:7 | negations_pratityasamutpada | Negation of dependent origination |
| T251:8 | negations_path | Negation of path (suffering, origin, cessation, path) |
| T251:9 | bodhisattva_attainment | Bodhisattva's attainment through prajñāpāramitā |
| T251:10 | buddha_attainment | All buddhas' attainment through prajñāpāramitā |
| T251:11 | mantra_praise | Praise of the mantra (great mantra, great clarity mantra...) |
| T251:12 | mantra | The mantra itself (gate gate pāragate...) |

### Correspondence Criterion

A segment in a non-base witness is aligned to a T251 segment when it **conveys the same doctrinal content within the same structural position**. Both criteria must be satisfied:

1. **Semantic equivalence**: The content addresses the same Buddhist teaching (e.g., the form/emptiness equation, the negation of the twelve sense bases)
2. **Structural position**: The passage occupies the same relative position in the sūtra's argument

In practice, the Heart Sūtra's concise structure makes alignments unambiguous for the core text. The 12 T251 segments map to distinct, well-known doctrinal passages that are readily identifiable in any recension or translation.

### Null Alignment

A segment receives `"chinese_parallel": null` when it has **no corresponding content in T251**. This occurs for:
- Material unique to one tradition (Sanskrit invocations, colophons)
- Long-recension frame narratives absent from the short recension
- Tradition-specific interpolations

Segments without a `chinese_parallel` field (as opposed to `null`) are handled identically: they are excluded from automated collation.

## 2. Alignment Decisions by Witness

### Sanskrit GRETIL (14 segments)

| GRETIL Segment | chinese_parallel | Rationale |
|----------------|-----------------|-----------|
| GRETIL:1 (invocation) | null | *Oṃ Namo Bhagavatyai* — Tantric maṅgala absent from T251 and earliest witnesses. Late Nepalese interpolation (Attwood 2024). |
| GRETIL:2–13 | T251:1–12 | 1:1 correspondence with T251 segments. Content matches semantically and structurally. |
| GRETIL:14 (colophon) | null | *Ity ārya-prajñāpāramitā-hṛdayaṃ samāptam* — Closing formula absent from T251. Standard Sanskrit manuscript convention, not part of the sūtra text. |

### Tibetan Toh 21 (Degé Kangyur, long recension)

Toh 21 is a long recension containing a frame narrative (setting, assembly, Buddha's samādhi, Avalokiteśvara's dialogue, Buddha's approval). The 12 core segments align 1:1 with T251. Frame narrative sections have no `chinese_parallel` because T251 (short recension) lacks frame material.

### Tibetan IOL Tib J 751 (Dunhuang, short recension)

All 12 segments align 1:1 with T251:1–12. As a short recension without frame narrative, this witness has no unaligned material.

### Chinese T250

T250 segments carry `chinese_parallel` references to their T251 counterparts (e.g., `"chinese_parallel": "T251:2"`), enabling inter-Chinese collation. T250's content matches T251's segmentation with minor variations in scope.

## 3. Annotation Process

### Method

Alignments were produced by **manual scholarly analysis** following this procedure:

1. **Segmentation of T251**: The base text was divided into 12 segments at natural doctrinal boundaries, following the standard scholarly division established by Conze (1967, pp. 148–152) and refined by Attwood (2023, pp. 162–165).

2. **Identification of parallels**: For each non-base witness, the editor identified the passage corresponding to each T251 segment by comparing content. The Heart Sūtra's brevity (260 characters in Chinese, ~65 words in Sanskrit) makes this straightforward — there is no ambiguity about which Sanskrit passage corresponds to which Chinese passage for the core text.

3. **Verification against published editions**: Alignments were cross-checked against:
   - Conze (1967) — Sanskrit critical edition with Chinese references
   - Attwood (2023) — Section-by-section Chinese/Sanskrit comparison
   - Attwood (2024) — Revised parallel editions of both texts
   - Silk (1994) — Tibetan critical edition with cross-references

4. **Recording**: The `chinese_parallel` field was set in each witness's JSON data file. Values take the form `"T251:N"` where N is the segment number (1–12), or `null` for unaligned material.

### No Computational Alignment

No automatic alignment algorithm was used. The alignments are entirely the product of scholarly editorial judgment, verified against the published parallel editions listed above. This is appropriate given the text's brevity and the extensive prior scholarly work establishing cross-linguistic correspondences.

## 4. Edge Cases and Difficult Decisions

### Sanskrit Invocation (GRETIL:1)

The *Oṃ Namo Bhagavatyai Ārya-prajñāpāramitāyai* invocation is absent from T251, from the earliest Chinese witnesses, and from most early Sanskrit witnesses. Following Attwood (2024), it is classified as a late Tantric interpolation from Nepalese manuscripts. It receives `null` rather than being aligned to T251:1 (which begins with Avalokiteśvara, not with an invocation).

### Sanskrit Colophon (GRETIL:14)

The closing formula *Ity ārya-prajñāpāramitā-hṛdayaṃ samāptam* is a standard Sanskrit manuscript convention (not part of the sūtra text proper). It has no Chinese counterpart.

### Tibetan Frame Narrative (Toh 21)

The Degé Kangyur long recension contains extensive frame narrative material (setting at Vulture Peak, assembly of bodhisattvas and arhats, Buddha entering samādhi, dialogue authorization, Buddha's approval). This material is absent from T251 (short recension) and cannot be meaningfully aligned to it. These sections have no `chinese_parallel` field.

### Combined/Split Segments

No cases of segment splitting or combining were encountered. The Heart Sūtra's concise structure produces natural 1:1 correspondences across all three linguistic traditions for the core text.

## 5. Verification Procedure

To verify or modify an alignment:

1. Open the witness JSON file (e.g., `data/sanskrit/gretil/prajnaparamitahrdaya.json`)
2. Locate the segment by its `id` field
3. Read the segment's text content (IAST, Devanagari, or Tibetan)
4. Compare against the corresponding T251 segment (in `data/chinese/taisho/t251.json`)
5. Confirm that the content addresses the same doctrinal passage
6. If the alignment is incorrect, edit the `chinese_parallel` field
7. Run `hrdaya-validate` to confirm the reference format is valid

The pipeline's cross-reference validation (`hrdaya-validate`) automatically confirms that all `chinese_parallel` targets exist in the Chinese witness files.

## 6. Replicability

All alignment decisions are transparent: they are recorded as `chinese_parallel` fields in the JSON data files and can be inspected, verified, or modified by any scholar. The alignment protocol described here provides the criteria for producing or evaluating these annotations.

The deliberate choice to exclude unaligned segments from automated collation (rather than guessing at correspondences) means the apparatus is conservative: it may omit interesting material, but it will not produce spurious alignments.

---

*Compiled February 2026*
