# Paper TODOs: Parallel Compositions Paper

## Sources
- `response paper.docx` (February 2026) — internal review
- `working/PEER_REVIEW.md` — simulated academic peer review

Status key: `[ ]` = not started, `[~]` = partially done, `[x]` = complete

---

## Recommended Execution Order

### Phase 1: Foundation (do first — everything else builds on these)
1. **#4 Japanese/Chinese literature review** — Highest-risk item. If parallel composition was already proposed in Japanese, it reshapes the paper. Pure research, no writing dependency.
2. **#1 Strengthen the deletion case** — The 抄經 comparative study. Key research before writing.

### Phase 2: Core argument strengthening
3. **#3 Passage-by-passage comparison** — Extends strongest evidence from one example to a systematic pattern.
4. **#5 Falsifiability/counterevidence** — Forces identification of where the argument is weakest.
5. **#8 Separate interpretive from descriptive** — Restructuring that makes the paper more defensible.

### Phase 3: Scholarly framing
6. **#2 Engagement with critics** — Drafts exist; condense and integrate once core argument is solid.
7. **#11 Terminological precision** — Quick definitional work.
8. **#12 Broaden authority base** — Can happen during revision.

### Phase 4: Infrastructure (for the edition; less urgent for the paper)
9. **#2b Primary manuscript collation** — Important for the edition; paper can acknowledge as a limitation.
10. **#6 Reproducible pipeline** — Same: important for edition, less blocking for the paper.
11. **#7 Variant classification formalization** — Pairs with #6.

### Phase 5: Polish
12. **#10 Dating methodology** — Brief section, write late.
13. **#9 Māyā→Śūnyatā** — Decide in/out.
14. **#13 Prose tightening** — Always last.

---

## Critical Priority

### 1. Strengthen the Negative Case for Deletion
- [ ] Conduct comparative study of revision practice in 抄經 (digest text) tradition
- [ ] Identify 5-10 Chinese Buddhist digest texts where both source and digest survive
- [ ] Document whether revision between versions involved deletion of coherent doctrinal content
- [ ] Move argument from "deletion seems unlikely" to "deletion contradicts documented revision practice"
- **Why critical:** Without this, a reviewer can simply say "revisers sometimes abridge" and the paper lacks a counter

### 2. Engagement with Nattier's Critics
- [~] Address Fukui Fumimasa, Harada Waso, Ishii Kōsei, Dan Lusthaus, Hyun Choo
- **Done so far:** `research/ENGAGEMENT_WITH_CRITICS.md` has detailed responses drafted
- [ ] Integrate a condensed version into the paper's Introduction or Discussion section
- [ ] Consult Fukui's *Hannya shingyō no rekishiteki kenkyū* (般若心経の歴史的研究, 1987) — most important single work; may address T250/T251 relationship directly
- [ ] Ensure the paper explicitly argues the parallel composition hypothesis does NOT depend on resolving the Chinese-vs-Sanskrit origin debate
- **Peer review note:** Engagement currently "shallow" — need fuller review of dissenting arguments with direct responses (PEER_REVIEW §Major Concern 5)

### 2b. Primary Manuscript Collation Evidence
- [ ] Provide diplomatic transcriptions or images of at least a subset of key witnesses (Dunhuang, Hōryū-ji, Gilgit fragments)
- [ ] Show collation steps from primary sources, not just published editions
- [ ] Consider a primary-manuscript appendix with direct evidence for highest-stakes claims
- **Why critical:** Peer review identifies this as the #1 concern — reliance on published editions and digital texts is a serious limitation for a critical edition claiming new textual history (PEER_REVIEW §Major Concern 1)
- **Practical constraint:** Physical manuscript access is limited; note honestly what has and hasn't been consulted directly

---

## High Priority

### 3. Extend the Epithet Argument to Systematic Passage-by-Passage Comparison
- [ ] Create systematic passage-by-passage comparison table showing extraction fidelity in both T250 and T251 relative to T223
- [ ] Determine: Does T250 match T223 exactly in other passages too, or only in the epithets?
- [ ] If T250 consistently reproduces T223 verbatim while T251 transforms its source, that pattern is far more compelling than a single example
- **Why important:** Transforms the epithet observation from an illustration into a pattern

### 4. Japanese and Chinese Secondary Literature Review
- [ ] Search INBUDS (Japanese Buddhist studies article database) for T250/T251 articles
- [ ] Search CiNii for relevant articles
- [ ] Consult *Bukkyō Daijiten*
- [ ] Document search results even if negative ("a search of INBUDS yielded N results, none proposing parallel composition")
- [ ] Consult Fukui Fumimasa (1987) *Hannya shingyō no rekishiteki kenkyū*
- **Why important:** Risk of rejection if parallel composition hypothesis was already proposed in Japanese literature
- **Peer review note:** Both reviews flag this as a gap that could prompt rejection on its own (PEER_REVIEW §Specific Issue 3)

---

## Medium Priority

### 5. Add Falsifiability Statement and Counterevidence Checklist
- [ ] State explicitly what evidence would disprove the hypothesis
- [ ] Examples: an intermediate manuscript with T250's skandha passage but T251's four epithets; evidence that doctrinal deletion was common in 抄經 practice
- [ ] Provide a formal "counterevidence checklist" specifying what findings would challenge the Chinese-priority hypothesis
- [ ] Address confirmation bias concern: the project starts from Chinese priority and frames evidence accordingly — need systematic falsification strategy
- **Why useful:** Demonstrates testable claim rather than unfalsifiable assertion
- **Peer review note:** Major Concern 3 flags potential confirmation bias; Revision Plan 4 requests formal counterevidence checklist

### 6. Reproducible Collation Pipeline
- [ ] Implement a reproducible variant-detection or alignment pipeline
- [ ] Ensure outputs are generated from a clearly defined, versioned data pipeline
- [ ] Document the computational chain from sources to claims in `docs/METHODOLOGY.md`
- [ ] Move findings from narrative synthesis toward reproducible critical edition
- **Peer review note:** Major Concern 2 — without this, findings read as narrative synthesis rather than reproducible critical edition; Revision Plan 1

### 7. Formalize Variant Classification Logic
- [ ] Define explicit, replicable criteria for variant classifications (orthographic, back-translation, extraction artifact)
- [ ] Provide worked examples across multiple witnesses for each classification type
- [ ] Ensure another scholar could apply the same criteria and reach the same classifications
- **Peer review note:** Specific Issue 2

### 8. Separate Interpretive Claims from Descriptive Findings
- [ ] Frame "parallel composition" hypothesis more explicitly as a provisional model, not a firm conclusion
- [ ] Clearly distinguish descriptive findings (T250 matches T223 here, T251 diverges there) from interpretive claims (therefore they are parallel compositions)
- [ ] Ensure readers can accept the textual data without necessarily accepting the hypothesis
- **Peer review note:** Specific Issue 4

### 9. Māyā→Śūnyatā Observation
- [ ] Decide: integrate into argument (does T250 handle māyā/śūnyatā differently from T251?) or remove
- [ ] If no T250/T251 difference exists, save for separate publication
- **Current status:** In Discussion section; does not directly support the parallel composition hypothesis

---

## Lower Priority

### 10. Dating Methodology Discussion
- [ ] Add methodological discussion of dating reliability and confidence bounds for key witnesses
- [ ] Address which claims depend on dating and how sensitive they are to dating uncertainty
- **Peer review note:** Minor Concern 1

### 11. Terminological Precision
- [ ] Define and operationalize "compositionally prior," "derived," and "back-translation" more carefully
- [ ] Ensure definitions avoid circular reasoning (e.g., "derived because it shows back-translation features" where "back-translation" presupposes derivation)
- **Peer review note:** Minor Concern 2

### 12. Broaden Authority Base
- [ ] Reduce over-reliance on Nattier and Attwood as primary authorities
- [ ] Cite additional independent scholars who support or engage with the evidence
- [ ] Frame analysis as building on but independent from Nattier/Attwood
- **Peer review note:** Minor Concern 3

### 13. Prose Tightening
- [ ] Compress by ~20%, reduce repetition
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
