# psychology-knowledge-atlas — 交接狀態

## ACTIVE WORK

```yaml
phase: P1-universe
status: validated
started_at: 2026-07-22
targets:
  - reference-system and coverage contracts
  - first bounded authoritative inventory
  - deterministic coverage report
validation:
  - canonical validator baseline PASS
  - 22 foundation and P1 system tests PASS
  - git diff whitespace gate PASS
  - APA CoA C-5 P snapshot: 11/11 candidates adjudicated
  - ANZSRC 2020 FoR Division 52 group slice: 6/6 candidates adjudicated
  - ANZSRC 2020 FoR Division 52 field inventory: 36/36 registered; 21 resolved; 15 pending
  - clean GitHub clone at 5faead9 + validator + 19 tests PASS
  - clean GitHub clone at 7e2c41f + validator + 20 tests PASS
  - clean GitHub clone at 6cc662d + validator + 21 tests PASS
remote: https://github.com/Hangsau/psychology-knowledge-atlas
next_gate: adjudicate ANZSRC field groups 5203, 5204 and 5205 in order, then add a genuinely global or multi-region reference system and an explicit Indigenous-psychology axis before knowledge claims
```

## P1 progress

- `apa-coa-postdoctoral-specialty-practice-areas` is the first completed reference-system slice: 11/11 official candidates are recorded and mapped to non-publishable `subfield` identities.
- Its scope is deliberately narrow: United States health-service psychology postdoctoral specialty accreditation. It is not evidence for a global or exhaustive psychology taxonomy.
- `anzsrc-2020-for-psychology-groups` is the second completed slice: 6/6 group-level candidates under Division 52 are adjudicated. Five substantive groups are included; residual code 5299 `Other psychology` is recorded but excluded as a non-coherent entity.
- ANZSRC is an Australia/New Zealand R&D classification, not a global ontology. Its Division 52 explicitly sends Indigenous psychology to Division 45 Indigenous studies, so the atlas must inspect that axis rather than treating the omission as absence.
- Similar labels remain distinct when their scopes differ: ANZSRC `Clinical and health psychology` is not merged into the narrower APA CoA `Clinical Health Psychology` specialty.
- `anzsrc-2020-for-psychology-fields` registers all 36 Division 52 field codes. The 5201 batch is resolved: 7 included, 1 identity merge (`Forensic psychology`), and 1 NEC residual excluded. The 5202 batch is also resolved: 7 substantive biological-psychology fields included and its NEC residual remains excluded. Across the full field inventory, 15 substantive candidates remain explicitly `pending`; all six NEC residuals are excluded.
- Coverage reports now separate `complete` (every source candidate has a record) from `resolved` (no pending decisions). The field inventory is `complete:true`, `resolved:false`; this prevents a full candidate scrape from masquerading as completed adjudication.
- Coverage completeness is now executable: every declared candidate must have exactly one `included`, `merged`, `excluded`, or `pending` decision, and included/merged targets must resolve.
- Generated `views/generated/coverage-report.json` is disposable and reproducible from canonical records.

## Legacy provenance

- 舊 repo：`C:\claudehome\projects\psychology-schools`
- 舊正式 checkpoint：`master@3be7f99`（建立新版時）
- 舊完整 WIP：branch `archival/wip-atlas-migration-2026-07-22`、commit `eb115a5`
- 舊 §3a 本土心理學改動未匯入；Axline 修正已在舊 master 獨立保存。

## 發布狀態

`evidence_release: false`。目前有未驗證 legacy identity seeds 與一個已擷取的 reference-system identity slice，沒有可發布知識 claim。
