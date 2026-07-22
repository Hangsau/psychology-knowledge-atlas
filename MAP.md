# psychology-knowledge-atlas — 導航地圖

## 1. 結構

```text
schemas/                 JSON Schema 合約
catalog/entities/        心理學實體與收錄裁決
catalog/reference-systems/ 權威參考系與 coverage 母體
library/sources/         書目、版本、取得狀態
knowledge/claims/        原子主張
knowledge/evidence/      claim ↔ source locator 證據
knowledge/relations/     有方向、有依據的實體關係
knowledge/controversies/ 爭議與競爭性解釋
vocabularies/            多軸受控詞彙
crosswalks/              D1–D13 與跨 repo 合約
views/generated/         可刪除、可重生輸出（Git ignore）
tools/validate.py        canonical integrity validator
tools/store.py           原子寫入與同實體鎖
tests/                   邊界、schema、參照、併發、安全測試
```

## 2. 決策索引

| 要做 | 先看 |
|---|---|
| 新增實體 | `schemas/entity.schema.json` + `catalog/reference-systems/` |
| 新增來源 | `schemas/source.schema.json`；取得狀態不等於證據品質 |
| 新增主張／證據 | claim + evidence schema；locator 與 source access gate |
| 對接宗教庫 | `crosswalks/d1-d13.json`；第一階段不改 religions-history |
| 產文章／索引 | 只從 canonical records 生成到 `views/generated/` |

## 3. 踩雷點

- 舊 48 項不是封閉全集，也不是同一實體類型。
- 舊文章、confidence emoji、`reviewed` 與 `corroborated` 不可繼承。
- metadata、snippet、abstract 與全文證據必須區分。
- 同一實體寫入必須取得 lock；禁止直接覆寫 canonical JSON。
