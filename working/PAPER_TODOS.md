# Paper TODOs: Parallel Compositions Paper

## Sources
- `response paper.docx` (February 2026) — internal review
- `working/PEER_REVIEW.md` — simulated academic peer review

Status key: `[ ]` = not started, `[~]` = partially done, `[x]` = complete

---

## Recommended Execution Order

### Phase 1: Foundation ✓ COMPLETE
1. **#4 Japanese/Chinese literature review** ✓ — Hypothesis appears novel. No prior proposal found across 3 existing models (traditional, reversed, Indian origin). See `research/` output.
2. **#1 Strengthen the deletion case** ✓ — 10 case studies documented in `research/CHAOJING_REVISION_PRACTICES.md`. No attested deletion of doctrinally correct content. Still needs integration into paper text.

### Phase 2: Core argument strengthening ✓ COMPLETE
3. **#3 Passage-by-passage comparison** ✓ — T250 closer to T223 in 8/10 sections, T251 in 0. See `research/PASSAGE_COMPARISON.md`.
4. **#5 Falsifiability/counterevidence** ✓ — 5 falsifying conditions + 6-item counterevidence checklist. See `research/FALSIFIABILITY.md`.
5. **#8 Separate interpretive from descriptive** ✓ — 6 descriptive findings, 4 interpretive claims, paper structure guidance. See `research/INTERPRETIVE_DESCRIPTIVE.md`.

### Phase 3: Scholarly framing ✓ COMPLETE
6. **#2 Engagement with critics** ✓ — Condensed paper-ready Introduction + Discussion text. See `research/PAPER_DRAFT_SECTIONS.md` §A.
7. **#11 Terminological precision** ✓ — Definitions for 5 key terms with circularity note. See `research/PAPER_DRAFT_SECTIONS.md` §B.
8. **#12 Broaden authority base** ✓ — 8 additional scholars identified with framing language. See `research/PAPER_DRAFT_SECTIONS.md` §C.

### Phase 4: Infrastructure ✓ COMPLETE
9. **#2b Primary manuscript collation** ✓ — Limitations documented. See `research/PRIMARY_MANUSCRIPT_LIMITATIONS.md`.
10. **#6 Reproducible pipeline** ✓ — Pipeline documented in `docs/METHODOLOGY.md` §13. 61 tests pass. CI added.
11. **#7 Variant classification formalization** ✓ — Formal criteria with worked examples. See `research/VARIANT_CLASSIFICATION_CRITERIA.md`.

### Phase 5: Polish ✓ COMPLETE
12. **#10 Dating methodology** ✓ — Dating hierarchy, sensitivity analysis. See `research/DATING_METHODOLOGY.md`.
13. **#9 Māyā→Śūnyatā** ✓ — Decision: REMOVE from paper, save for separate publication. See `research/MAYA_SUNYATA_DECISION.md`.
14. **#13 Prose tightening** ✓ — Consolidation guide with ~2,000-word savings. See `research/PROSE_TIGHTENING_GUIDE.md`.

---

## Critical Priority

### 1. Strengthen the Negative Case for Deletion
- [x] Conduct comparative study of revision practice in 抄經 (digest text) tradition
- [x] Identify 5-10 Chinese Buddhist digest texts where both source and digest survive — 10 cases documented
- [x] Document whether revision between versions involved deletion of coherent doctrinal content — no case found
- [x] Move argument from "deletion seems unlikely" to "deletion contradicts documented revision practice"
- **Research complete:** See `research/CHAOJING_REVISION_PRACTICES.md` (466 lines, 10 case studies, counter-arguments addressed)
- [ ] Integrate findings into paper draft (Section 2.3 / new subsection)
- **Why critical:** Without this, a reviewer can simply say "revisers sometimes abridge" and the paper lacks a counter

### 2. Engagement with Nattier's Critics
- [x] Address Fukui Fumimasa, Harada Waso, Ishii Kōsei, Dan Lusthaus, Hyun Choo
- [x] Condensed paper-ready text drafted — see `research/PAPER_DRAFT_SECTIONS.md` §A
- [x] Ensure the paper explicitly argues the parallel composition hypothesis does NOT depend on resolving the Chinese-vs-Sanskrit origin debate
- [x] Engage directly with Attwood's T250-as-forgery model with specific response
- [x] Consult Fukui's *Hannya shingyō no rekishiteki kenkyū* (般若心経の歴史的研究, 1987) — consulted via secondary literature and English-language reviews; 1994 and 2000 publications also added to bibliography
- [ ] Integrate condensed text into actual paper draft
- **Peer review note:** Engagement now substantive; Attwood response directly addresses "deliberate restoration" alternative
- **CJK update (Feb 2026):** Engagement with Critics expanded with detailed arguments from Fukui, Harada, Ishii, Ji Yun, Siu, plus Acta Asiatica 121. CJK limitation acknowledgment added.

### 2b. Primary Manuscript Collation Evidence
- [x] Document which sources have been consulted and which have not — see `research/PRIMARY_MANUSCRIPT_LIMITATIONS.md`
- [x] Assess impact on claims: macro-level compositional arguments don't depend on primary manuscript access
- [x] Identify path forward for future primary collation (IDP images, temple archives)
- [ ] Provide diplomatic transcriptions or images of at least a subset of key witnesses (Dunhuang, Hōryū-ji, Gilgit fragments) — **deferred: requires physical access**
- [ ] Show collation steps from primary sources, not just published editions — **deferred**
- **Why critical:** Peer review identifies this as the #1 concern — reliance on published editions and digital texts is a serious limitation for a critical edition claiming new textual history (PEER_REVIEW §Major Concern 1)
- **Practical constraint:** Physical manuscript access is limited; honestly documented in `research/PRIMARY_MANUSCRIPT_LIMITATIONS.md`
- **Resolution:** Paper reframed as "analysis of received textual tradition" with explicit limitation acknowledgement

---

## High Priority

### 3. Extend the Epithet Argument to Systematic Passage-by-Passage Comparison
- [x] Create systematic passage-by-passage comparison table — see `research/PASSAGE_COMPARISON.md`
- [x] Determine: Does T250 match T223 exactly in other passages too? — **Yes, in 8 of 10 sections**
- [x] Pattern confirmed: T250 consistently reproduces T223; T251 consistently transforms. No exceptions.
- [ ] Integrate comparison table into paper (Section 2 or new Section 3)
- **Result:** Epithet observation now demonstrated as systematic pattern across entire text

### 4. Japanese and Chinese Secondary Literature Review
- [x] Search INBUDS (Japanese Buddhist studies article database) for T250/T251 articles — remote search inconclusive, recommend direct access
- [x] Search CiNii for relevant articles — no parallel composition proposal found
- [x] Search J-STAGE — Watanabe (1991) closest but concludes T250 is spurious, not parallel
- [x] Consult *Bukkyō Daijiten* — no online entry on parallel composition
- [x] Document search results even if negative — comprehensive report with scholar-by-scholar analysis
- [x] Consult Fukui Fumimasa (1987/1994/2000) — consulted via secondary literature; Fukui 1994 (Nattier rebuttal) and 2000 (comprehensive study) added to bibliography
- [x] Consult Siu Sai Yau's *Catalogue of Academic Research on Prajñāpāramitāhṛdaya (1912-2013)* — cited in bibliography and engagement docs
- [x] CJK literature search conducted (Feb 2026): 9 scholars covered, ~30 new bibliography entries added, engagement with critics expanded with detailed arguments
- [ ] Integrate literature review findings into paper Introduction
- **Key finding:** Parallel composition hypothesis appears novel. Three existing models identified (traditional, reversed/forgery, Indian origin); none proposes parallel extraction from T223.
- **Caveats:** INBUDS, CNKI not fully searchable remotely. Qualification added to ENGAGEMENT_WITH_CRITICS.md and METHODOLOGY.md.
- **Peer review note:** Both reviews flag this as a gap that could prompt rejection on its own — NOW ADDRESSED with ~30 CJK bibliography entries and expanded engagement

---

## Medium Priority

### 5. Add Falsifiability Statement and Counterevidence Checklist
- [x] State explicitly what evidence would disprove the hypothesis — 5 falsifying conditions identified
- [x] Provide formal counterevidence checklist — 6-item table for Chinese-priority framework
- [x] Address confirmation bias — 5-point response documented
- [ ] Integrate into paper (Section 5 / Limitations)
- **Research complete:** See `research/FALSIFIABILITY.md`
- **Peer review note:** Major Concern 3 addressed

### 6. Reproducible Collation Pipeline
- [x] Implement a reproducible variant-detection or alignment pipeline — `hrdaya.collate` module, 61 tests
- [x] Ensure outputs are generated from a clearly defined, versioned data pipeline — provenance metadata in all outputs
- [x] Document the computational chain from sources to claims in `docs/METHODOLOGY.md` — §13 added
- [x] Add CI automation — `.github/workflows/test.yml` (Python 3.10/3.11/3.12)
- [ ] Move findings from narrative synthesis toward reproducible critical edition — ongoing, pipeline supports this
- **Peer review note:** Major Concern 2 addressed — pipeline now reproducible with `hrdaya-collate` and `hrdaya-synoptic` CLI tools

### 7. Formalize Variant Classification Logic
- [x] Define explicit, replicable criteria for variant classifications (orthographic, back-translation, extraction artifact) — see `research/VARIANT_CLASSIFICATION_CRITERIA.md`
- [x] Provide worked examples across multiple witnesses for each classification type — 7 categories with examples
- [x] Confidence levels defined (0.0-1.0 scale with criteria)
- [x] Decision procedure documented for applying classifications
- [ ] Ensure another scholar could apply the same criteria and reach the same classifications — criteria published, needs external testing
- **Peer review note:** Specific Issue 2 addressed

### 8. Separate Interpretive Claims from Descriptive Findings
- [x] Frame as provisional model — guidance drafted with recommended language
- [x] Distinguish descriptive (6 findings) from interpretive (4 claims) — see `research/INTERPRETIVE_DESCRIPTIVE.md`
- [x] Paper structure recommendation: Sections 2 (descriptive) → 3 (analysis) → 4 (argument) → 5 (limitations)
- [ ] Apply restructuring to actual paper draft
- **Peer review note:** Specific Issue 4 addressed

### 9. Māyā→Śūnyatā Observation
- [x] Decide: integrate into argument (does T250 handle māyā/śūnyatā differently from T251?) or remove — **REMOVE**
- [x] T250 and T251 both use the same śūnyatā formula; observation does not distinguish them
- [x] Saved for separate publication — see `research/MAYA_SUNYATA_DECISION.md`
- **Decision:** Remove from paper. Add one-sentence forward reference in Conclusion.

---

## Lower Priority

### 10. Dating Methodology Discussion
- [x] Add methodological discussion of dating reliability and confidence bounds for key witnesses — see `research/DATING_METHODOLOGY.md`
- [x] Sensitivity analysis: T250's date is critical; all other claims are date-insensitive
- [x] Dating hierarchy table with confidence levels
- [ ] Integrate as brief (500–800 word) subsection into paper Methodology section
- **Peer review note:** Minor Concern 1 addressed

### 11. Terminological Precision
- [x] Define "compositionally prior," "derived," "back-translation," "digest text," "parallel composition"
- [x] Circularity note included — evidence distinguished from conclusion
- [ ] Integrate definitions into paper Methodology section
- **See:** `research/PAPER_DRAFT_SECTIONS.md` §B

### 12. Broaden Authority Base
- [x] 8 additional scholars identified beyond Nattier/Attwood (Watanabe, Huifeng, Silk, Funayama, Storch, Tokuno, Buswell, Woncheuk)
- [x] Framing language drafted to distribute authority
- [ ] Apply framing to paper citations
- **See:** `research/PAPER_DRAFT_SECTIONS.md` §C

### 13. Prose Tightening
- [x] Identify consolidation targets — see `research/PROSE_TIGHTENING_GUIDE.md`
- [x] Estimated ~2,000-word savings identified across 6 areas
- [ ] Compress by ~20%, reduce repetition — apply guide to actual paper draft
- [ ] Consolidate "deletion is unlikely" argument (currently in Section 2.3, restated in 4.2, implied in 5.1)
- [ ] Consolidate terminological consistency observation (Section 4 and Discussion)

---

## Additional Considerations

### Japanese Manuscripts
- [ ] Note as desideratum: Nara-period 写経 (shakyō) copies may preserve T250-type readings
- [ ] Major temple archives (Tōdai-ji, Kōya-san, Shōsōin) not freely accessible
- [ ] Note Shōsōin digitization project as future opportunity

### Target Journal
1. **JIABS** — First choice. Nattier 1992 published here. Exact right readership. Slow review.
2. **JOCBS** — Second choice. Attwood's series published here. Open access, faster.
3. **Indo-Iranian Journal** — Third choice. Strong philological tradition.

### Companion Paper (Digital Humanities)
- [ ] Consider separate paper on non-Lachmannian editorial framework, direction-of-dependence annotation, variant classification, AI-assisted workflow
- [ ] Venues: *Digital Scholarship in the Humanities*, *DHQ*, *Journal of the Text Encoding Initiative*
- [ ] Philological paper should be submitted first

---

*Extracted from response paper.docx and working/PEER_REVIEW.md, February 2026*
