# psychology-knowledge-atlas — 交接狀態

## ACTIVE WORK

```yaml
phase: P2-E
status: validated
started_at: 2026-07-22
targets:
  - phenomenon entity contract
  - controlled phenomenon_kind and reference-system system_role vocabularies
  - explicit roles for all existing reference systems
  - first named-phenomenon candidate universe (cognitive-bias discovery seed)
  - P2-E pilot phenomena outside cognitive biases registered (misattribution of arousal, broken windows)
  - P2-E evidence source routing for the three pilots: popular / research / critique claims per pilot, each with a source and metadata-only evidence, all publishable:false
validation:
  - canonical validator baseline PASS
  - 32 foundation and P1/P1-E system tests PASS
  - git diff whitespace gate PASS
  - APA CoA C-5 P snapshot: 11/11 candidates adjudicated
  - ANZSRC 2020 FoR Division 52 group slice: 6/6 candidates adjudicated
  - ANZSRC 2020 FoR Division 52 field inventory: 36/36 registered and resolved; 28 included; 2 merged; 6 excluded; 0 pending
  - ANZSRC field group 5203: 4/4 substantive candidates adjudicated; 520399 NEC residual excluded
  - ANZSRC field group 5204: 6/6 substantive candidates adjudicated as research-field identities; 520499 NEC residual excluded
  - ANZSRC field group 5205: 5/5 substantive candidates adjudicated; 520599 NEC residual excluded
  - IAAP active divisions: 18/18 candidates registered and resolved; 12 included; 4 merged; 2 excluded; 0 pending
  - ANZSRC Division 45 Indigenous studies groups: 20/20 registered and resolved; 19 context domains included; 4599 residual excluded; 0 pending
  - context_domain entity type added to distinguish contextual axes from psychology subfields
  - Division 45 groups 4501–4506: 6/6 included as Aboriginal and Torres Strait Islander context domains
  - Division 45 groups 4507–4512: 6/6 included as Māori context domains; te reo Māori canonical names preserved
  - Division 45 groups 4513–4518: 6/6 included as Pacific Peoples context domains
  - Division 45 group 4519: included as a global Indigenous data, methodologies and studies context domain
  - corrected ABS 2025 labels: 4517 Pacific Peoples society and community; 4518 Pacific Peoples sciences
  - phenomenon contract: controlled kind, optional Chinese label, and non-empty resolvable domain_entity_ids
  - reference-system role contract: canonical taxonomy, specialist index, discovery seed, or popular-language inventory
  - wikipedia-cognitive-biases-core discovery seed: 23/23 candidates registered, resolved and included as phenomenon identities; complete:true, resolved:true, pending 0
  - cognitive-bias slice is a bounded discovery seed, NOT the exhaustive ~210-entry source list; complete here means every DECLARED candidate is adjudicated, not that the cognitive-bias universe is exhausted
  - named-effects-routing-pilot discovery seed: 2/2 candidates (misattribution of arousal 吊橋效應, broken windows 破窗效應) registered, resolved and included; complete:true, resolved:true, pending 0
  - three P2-E routing pilots now all have identities: Dunning-Kruger (under the cognitive-bias seed), misattribution of arousal, and broken windows
  - no evidence claims created: every phenomenon is status retrieved, publishable:false, provenance reference_system; identity-only registration
  - entity-types vocabulary now matches validator and includes context_domain plus phenomenon
  - clean GitHub clone at 5faead9 + validator + 19 tests PASS
  - clean GitHub clone at 7e2c41f + validator + 20 tests PASS
  - clean GitHub clone at 6cc662d + validator + 21 tests PASS
  - clean GitHub clone at cd3d1f6 + validator + 22 tests PASS
  - P2-E: 7 new source records registered from search-confirmed identifiers only; where no DOI was confirmed (kruger-dunning-1999, gignac-zajenkowski-2020, wilson-kelling-1982, harcourt-ludwig-2006) identifiers left empty rather than guessed
  - P2-E: 9 claims + 9 evidence records for the three pilots; each pilot has exactly one popular (definition), one research (finding or mechanism), and one critique claim as distinct atomic records, not one blended verdict
  - P2-E: every claim status retrieved, publishable:false, provenance source_derived, with a scope_note bounding overreach; every evidence evidence_level metadata_only, publishable:false, bidirectionally linked to its claim
  - P2-E: access_status recorded honestly (paywalled_unread / publicly_readable_license_unclear / open_fulltext); no full text was read this session, so no fulltext evidence is asserted and nothing is publishable or verified
  - 33 foundation and P1/P1-E/P2-E system tests PASS (added test_p2e_pilot_evidence_routing_is_identity_only)
  - clean GitHub clone at 982ce96 + validator + 33 tests PASS
  - publish/verification gate defined and codified: per-claim_type verified conditions written into CLAUDE.md (popular stays documented framing, research/attribution/mechanism/critique require fulltext + locator + verbatim short_quote); Wikipedia confined to discovery_seed + popular framing in CLAUDE.md and MAP
  - validator strengthened: publishable evidence now requires a non-empty verbatim short_quote, and a publishable claim now requires at least one linked publishable evidence record (closes the metadata-backed-publish loophole)
  - 34 tests PASS (added test_publish_gate_requires_readable_fulltext_with_quote)
  - clean GitHub clone at d5a5311 + validator + 34 tests PASS
  - FIRST worked promotion done: c-dk-popular upgraded end-to-end to status verified + publishable:true via a genuinely fetched Wikipedia lead quote; ev-dk-popular is now fulltext_direct with a verbatim short_quote and a specific locator (Lead section, opening definition sentence). This is a documented-popular-framing claim, not an "effect is real" claim
  - honest no-fulltext case registered alongside it: nuhfer-etal-2017-numeracy (open-access critique, DOI 10.5038/1936-4660.10.1.4) registered as access_status open_fulltext, but its PDF body returned 403 to the fetch tool this session, so c-dk-critique-noise + ev-dk-critique-noise stay abstract_only, publishable:false — a queued citation, deliberately NOT a faked read
  - Dunning-Kruger now spans all three layers on purpose: c-dk-popular (published), c-dk-research + c-dk-critique + c-dk-critique-noise (honest citation/queue), demonstrating tiering rather than uniform verdicts
  - source-prioritization + three-layer policy codified in CLAUDE.md (open replication/meta-analysis first, textbooks/handbooks next, paywalled originals last and allowed to stay metadata_only forever); no-fulltext produces a queued record, not garbage
  - reworked test to test_p2e_pilot_evidence_routing_and_first_promotion: asserts all base claims stay publishable:false EXCEPT c-dk-popular, checks the promoted popular claim + evidence, and pins the Nuhfer no-fulltext honest case
  - 34 tests PASS (test renamed/reworked, no net count change)
  - FIRST research-tier verified claim done: c-anchoring-manylabs-replication (claim_type finding, subject anchoring-bias) promoted through the gate from an openly readable multi-lab replication. Source klein-etal-2014-many-labs (Many Labs 1, Klein et al. 2014, Social Psychology 45(3):142-152, DOI 10.1027/1864-9335/a000178, Hogrefe OpenMind open-access license) full text was read this session: Hogrefe returned 403, but the openly hosted PDF (stanford.edu/~knutson/jdm/klein14.pdf) was fetched and its body extracted with pypdf; abstract, Table 2 and the 'Variation Across Samples and Settings' section were read directly
  - ev-anchoring-manylabs-replication is fulltext_direct with a verbatim short_quote naming anchoring among the "very large effects", locator "Results, 'Variation Across Samples and Settings' subsection, p. 149"; claim scope_note bounds it to a replication finding (Table 2 d approx 1.17-2.42, all p<.001), not a mechanism claim
  - 35 tests PASS (added test_first_research_tier_verified_claim)
next_gate: broaden the verified layer beyond the first two worked examples. Options in priority order: (a) promote c-dk-research or c-bw-research (mechanism/finding) if their primary sources are genuinely readable — note c-bw-research is about what Wilson & Kelling 1982 PROPOSED (readable open Atlantic essay), not that broken windows is real; (b) build a second anchoring or misattribution finding from another open replication; (c) attempt the Nuhfer full text again via an alternate open host to promote c-dk-critique-noise. For any contested effect, an "effect is real" claim still needs meta-analysis/replication evidence, not a single primary study. Keep atlas-level evidence_release false. If no full text can actually be read, STOP and register in the honest citation/queue layer — never fake a quote or a read.
```

## P2-E progress

- P2-E routes evidence for the three pilots (`misattribution-of-arousal` 吊橋效應, `dunning-kruger-effect` 達克效應, `broken-windows-effect` 破窗效應) into three distinct atomic claims each: a `popular` claim (`claim_type: definition`) recording how the effect is described in popular language, a `research` claim (`finding`, or `mechanism` for broken windows) tied to the primary source, and a `critique` claim (`critique`) tied to a documented non-replication or methodological objection. Popular, research and critique are separate records so a popular framing can never masquerade as a research verdict.
- Every P2-E claim carries a `scope_note` that bounds overreach (single study, US undergraduate sample, contested criminological claim, statistical-artefact objection, etc.), status `retrieved`, `publishable:false`, provenance `source_derived`. Every claim links exactly one evidence record, and each evidence record backlinks its claim (validator enforces the backlink).
- Seven new sources were registered from search-confirmed identifiers only: `dutton-aron-1974-bridge` (DOI + PMID), `kenrick-cialdini-linder-1979` (DOI), `kruger-dunning-1999`, `gignac-zajenkowski-2020`, `wilson-kelling-1982-broken-windows`, `harcourt-ludwig-2006`, and `wikipedia-dunning-kruger-effect`. Where no DOI was confirmed, `identifiers` is left empty rather than guessed. Popular claims reuse the existing Wikipedia article sources for the bridge and broken-windows effects.
- P2-E initially wrote all 9 claims as `metadata_only`, `publishable:false`; the publish gate was then exercised for real. `c-dk-popular` became the atlas's first `verified` + `publishable:true` claim by fetching the live Wikipedia Dunning-Kruger lead and recording its opening definition sentence as a verbatim `short_quote` at a specific locator; `ev-dk-popular` is now `fulltext_direct`. This is a documented-popular-framing claim (`claim_type: definition`), never an assertion that the effect is real.
- The honest no-fulltext path was demonstrated in the same session: `nuhfer-etal-2017-numeracy` (open-access noise/graphical-convention critique, DOI 10.5038/1936-4660.10.1.4, CC BY-NC 4.0) is registered as `access_status: open_fulltext` because that is its license status, but the PDF body returned 403 to the fetch tool, so `c-dk-critique-noise` + `ev-dk-critique-noise` stay `abstract_only`, `publishable:false`. That is the citation/queue layer, not garbage: a resolvable DOI with a pending full-text read, no fabricated body quote.
- Dunning-Kruger now deliberately spans layers: one published popular-framing claim, three unpublished (research finding, Gignac critique, Nuhfer noise critique) awaiting readable full text. All other P2-E claims remain `metadata_only`, `publishable:false`. The validator's gate is now actually exercised (one claim through it) rather than merely intact.

## P1 progress

- `named-effects-routing-pilot` is the second named-phenomenon slice: a deliberately bounded two-item `discovery_seed` pairing chosen by PLAN P2-E to test evidence routing across different evidence types. It registers `misattribution-of-arousal` (吊橋效應, Dutton–Aron bridge experiment; a lab social-psychology emotion effect) and `broken-windows-effect` (破窗效應, Wilson & Kelling 1982; a contested field criminology/social-order effect). Both are `included` identity-only, `publishable:false`. With the already-registered Dunning–Kruger effect, all three P2-E routing pilots now have identities. The broken-windows note explicitly records that the effect is contested, so identity registration cannot be mistaken for validity.
- `wikipedia-cognitive-biases-core` is the first named-phenomenon slice and the first `discovery_seed`. It registers 23 widely taught cognitive biases (confirmation bias, anchoring, availability/representativeness heuristics, Dunning–Kruger, framing, halo, fundamental attribution error, loss aversion, etc.) as `phenomenon` entities with a controlled `phenomenon_kind`, a resolvable `domain_entity_ids` host, and a Chinese label. All 23 are `included`; there are no merges because no prior entity represented a phenomenon. This is deliberately bounded: the source page has ~210 loosely structured entries, so `complete:true` means every declared candidate is adjudicated, not that the cognitive-bias universe is exhausted. A discovery seed can only produce candidates; it cannot support an evidence verdict, and every record stays `publishable:false`.
- `apa-coa-postdoctoral-specialty-practice-areas` is the first completed reference-system slice: 11/11 official candidates are recorded and mapped to non-publishable `subfield` identities.
- Its scope is deliberately narrow: United States health-service psychology postdoctoral specialty accreditation. It is not evidence for a global or exhaustive psychology taxonomy.
- `anzsrc-2020-for-psychology-groups` is the second completed slice: 6/6 group-level candidates under Division 52 are adjudicated. Five substantive groups are included; residual code 5299 `Other psychology` is recorded but excluded as a non-coherent entity.
- ANZSRC is an Australia/New Zealand R&D classification, not a global ontology. Its Division 52 explicitly sends Indigenous psychology to Division 45 Indigenous studies, so the atlas must inspect that axis rather than treating the omission as absence.
- Similar labels remain distinct when their scopes differ: ANZSRC `Clinical and health psychology` is not merged into the narrower APA CoA `Clinical Health Psychology` specialty.
- `anzsrc-2020-for-psychology-fields` registers and resolves all 36 Division 52 field codes. The 5201 batch has 7 included fields, 1 identity merge (`Forensic psychology`), and 1 NEC residual excluded. The 5202 batch has 7 substantive biological-psychology fields included. The 5203 batch has 3 included fields, 1 identity merge (`Clinical neuropsychology`), and a preserved boundary between ANZSRC `Health psychology` and the narrower APA CoA `Clinical Health Psychology` specialty. The 5204 batch preserves all 6 entries as research-field identities, including compound statistical labels, without converting them into construct claims. The 5205 batch includes 5 research fields while preserving compound-label, adjacent-discipline, and cross-project boundaries. Final field totals are 28 included, 2 merged, 6 excluded, and 0 pending.
- `iaap-active-divisions` is the first global organizational slice: all 18 active IAAP divisions are registered and resolved from the official live page. Its scope is explicitly global applied psychology and membership organization, not an exhaustive psychology taxonomy. Twelve substantive or compound applied fields are included; Work and Organizational Psychology, Health Psychology, Sport Psychology, and Counseling Psychology merge into existing cross-system identities while preserving source scope; the student/early-career cohort and cross-cutting Professional Practice function are excluded. Final totals are 12 included, 4 merged, 2 excluded, and 0 pending.
- `anzsrc-2020-for-indigenous-studies-groups` registers and resolves all 20 group-level codes under Division 45 as a contextual Indigenous axis. It preserves separate Aboriginal and Torres Strait Islander, Māori, Pacific Peoples, and global Indigenous data/methodologies structures rather than selecting only health or society categories. A new `context_domain` entity type prevents these broad fields from masquerading as psychology subfields. Groups 4501–4506 are included as Aboriginal and Torres Strait Islander context domains; groups 4507–4512 are included as Māori context domains with te reo Māori canonical names and English aliases; groups 4513–4518 are included as Pacific Peoples context domains; group 4519 preserves global Indigenous data, technologies, methodologies and source-specific exclusions. Groups 4504, 4510 and 4516 are directly psychology-relevant because their official definitions explicitly include psychological wellbeing. The corrected ABS cube assigns 4517 to society and community and 4518 to sciences. Final totals are 19 included context domains, 1 excluded residual, and 0 pending.
- Coverage reports now separate `complete` (every source candidate has a record) from `resolved` (no pending decisions). The field inventory is `complete:true`, `resolved:false`; this prevents a full candidate scrape from masquerading as completed adjudication.
- Coverage completeness is now executable: every declared candidate must have exactly one `included`, `merged`, `excluded`, or `pending` decision, and included/merged targets must resolve.
- Generated `views/generated/coverage-report.json` is disposable and reproducible from canonical records.

## APPROVED FUTURE WORK（QUEUED, NOT ACTIVE）

- P1-E：建立命名效應／偏誤／現象的 schema 與 bounded candidate universe；名稱不等於證據。
- P2-E：建立來源庫與證據路由，先以吊橋效應、達克效應、破窗效應測試不同證據型態。
- P3-M：建立 physical → chemical / biological → cognitive / behavioral → social / cultural 的受控機制層級，並先驗證 relationship evidence linkage。
- P3-M 首個建議 pilot：光照、晝夜節律／褪黑激素、睡眠、認知情緒、行為與社會作息的跨層鏈。
- P4-E/M：產生 Named Effect Card、Popular Claim vs Evidence、Replication / Controversy 與 Mechanism Ladder 視圖。
- 啟動條件：必須先完成 `ACTIVE WORK` 的 `next_gate`；排入 roadmap 不代表可提前建立 claims。

## Legacy provenance

- 舊 repo：`C:\claudehome\projects\psychology-schools`
- 舊正式 checkpoint：`master@3be7f99`（建立新版時）
- 舊完整 WIP：branch `archival/wip-atlas-migration-2026-07-22`、commit `eb115a5`
- 舊 §3a 本土心理學改動未匯入；Axline 修正已在舊 master 獨立保存。

## 發布狀態

`evidence_release: false`（atlas 層仍未發布）。已有兩筆通過閘門的 `publishable:true` claim：`c-dk-popular`（達克效應的通俗說法，非「效應為真」主張）與 `c-anchoring-manylabs-replication`（第一筆 research 層 finding，錨定效應在 Many Labs 1 多實驗室複製中屬「非常大的效應」，讀自開放全文）。其餘 claim 落在誠實引用／待辦層或候選層。個別 claim 可 publishable 不等於整個 atlas 進入 evidence_release。
