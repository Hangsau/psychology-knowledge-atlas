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
  - 19 foundation and P1 system tests PASS
  - git diff whitespace gate PASS
  - APA CoA C-5 P snapshot: 11/11 candidates adjudicated
remote: https://github.com/Hangsau/psychology-knowledge-atlas
next_gate: add complementary international and general-psychology reference systems; do not start knowledge claims until P1 coverage axes are explicitly bounded
```

## P1 progress

- `apa-coa-postdoctoral-specialty-practice-areas` is the first completed reference-system slice: 11/11 official candidates are recorded and mapped to non-publishable `subfield` identities.
- Its scope is deliberately narrow: United States health-service psychology postdoctoral specialty accreditation. It is not evidence for a global or exhaustive psychology taxonomy.
- Coverage completeness is now executable: every declared candidate must have exactly one `included`, `merged`, `excluded`, or `pending` decision, and included/merged targets must resolve.
- Generated `views/generated/coverage-report.json` is disposable and reproducible from canonical records.

## Legacy provenance

- 舊 repo：`C:\claudehome\projects\psychology-schools`
- 舊正式 checkpoint：`master@3be7f99`（建立新版時）
- 舊完整 WIP：branch `archival/wip-atlas-migration-2026-07-22`、commit `eb115a5`
- 舊 §3a 本土心理學改動未匯入；Axline 修正已在舊 master 獨立保存。

## 發布狀態

`evidence_release: false`。目前有未驗證 legacy identity seeds 與一個已擷取的 reference-system identity slice，沒有可發布知識 claim。
