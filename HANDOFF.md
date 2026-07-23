# psychology-knowledge-atlas — 交接狀態

## ACTIVE WORK

```yaml
phase: P1-universe
status: validated
started_at: 2026-07-22
targets:
  - reference-system and coverage contracts
  - bounded authoritative inventories
  - deterministic coverage report
validation:
  - canonical validator baseline PASS
  - 26 foundation and P1 system tests PASS
  - git diff whitespace gate PASS
  - APA CoA C-5 P snapshot: 11/11 candidates adjudicated
  - ANZSRC 2020 FoR Division 52 group slice: 6/6 candidates adjudicated
  - ANZSRC 2020 FoR Division 52 field inventory: 36/36 registered and resolved; 28 included; 2 merged; 6 excluded; 0 pending
  - ANZSRC field group 5203: 4/4 substantive candidates adjudicated; 520399 NEC residual excluded
  - ANZSRC field group 5204: 6/6 substantive candidates adjudicated as research-field identities; 520499 NEC residual excluded
  - ANZSRC field group 5205: 5/5 substantive candidates adjudicated; 520599 NEC residual excluded
  - IAAP active divisions: 18/18 candidates registered and resolved; 12 included; 4 merged; 2 excluded; 0 pending
  - clean GitHub clone at 5faead9 + validator + 19 tests PASS
  - clean GitHub clone at 7e2c41f + validator + 20 tests PASS
  - clean GitHub clone at 6cc662d + validator + 21 tests PASS
  - clean GitHub clone at cd3d1f6 + validator + 22 tests PASS
remote: https://github.com/Hangsau/psychology-knowledge-atlas
next_gate: add an explicit Indigenous-psychology axis before knowledge claims
```

## P1 progress

- `apa-coa-postdoctoral-specialty-practice-areas` is the first completed reference-system slice: 11/11 official candidates are recorded and mapped to non-publishable `subfield` identities.
- Its scope is deliberately narrow: United States health-service psychology postdoctoral specialty accreditation. It is not evidence for a global or exhaustive psychology taxonomy.
- `anzsrc-2020-for-psychology-groups` is the second completed slice: 6/6 group-level candidates under Division 52 are adjudicated. Five substantive groups are included; residual code 5299 `Other psychology` is recorded but excluded as a non-coherent entity.
- ANZSRC is an Australia/New Zealand R&D classification, not a global ontology. Its Division 52 explicitly sends Indigenous psychology to Division 45 Indigenous studies, so the atlas must inspect that axis rather than treating the omission as absence.
- Similar labels remain distinct when their scopes differ: ANZSRC `Clinical and health psychology` is not merged into the narrower APA CoA `Clinical Health Psychology` specialty.
- `anzsrc-2020-for-psychology-fields` registers and resolves all 36 Division 52 field codes. The 5201 batch has 7 included fields, 1 identity merge (`Forensic psychology`), and 1 NEC residual excluded. The 5202 batch has 7 substantive biological-psychology fields included. The 5203 batch has 3 included fields, 1 identity merge (`Clinical neuropsychology`), and a preserved boundary between ANZSRC `Health psychology` and the narrower APA CoA `Clinical Health Psychology` specialty. The 5204 batch preserves all 6 entries as research-field identities, including compound statistical labels, without converting them into construct claims. The 5205 batch includes 5 research fields while preserving compound-label, adjacent-discipline, and cross-project boundaries. Final field totals are 28 included, 2 merged, 6 excluded, and 0 pending.
- `iaap-active-divisions` is the first global organizational slice: all 18 active IAAP divisions are registered and resolved from the official live page. Its scope is explicitly global applied psychology and membership organization, not an exhaustive psychology taxonomy. Twelve substantive or compound applied fields are included; Work and Organizational Psychology, Health Psychology, Sport Psychology, and Counseling Psychology merge into existing cross-system identities while preserving source scope; the student/early-career cohort and cross-cutting Professional Practice function are excluded. Final totals are 12 included, 4 merged, 2 excluded, and 0 pending.
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

`evidence_release: false`。目前有未驗證 legacy identity seeds 與一個已擷取的 reference-system identity slice，沒有可發布知識 claim。
