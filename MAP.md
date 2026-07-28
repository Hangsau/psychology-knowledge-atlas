# psychology-knowledge-atlas — 導航地圖

## 1. 結構

```text
schemas/                 JSON Schema 合約
catalog/entities/        心理學實體與收錄裁決
catalog/reference-systems/ 權威參考系與 coverage 母體
catalog/coverage/          每個參考系候選的收錄／合併／排除／待裁決紀錄
library/sources/         書目、版本、取得狀態
knowledge/claims/        原子主張
knowledge/evidence/      claim ↔ source locator 證據
knowledge/relations/     有方向、有依據的實體關係
knowledge/controversies/ 爭議與競爭性解釋
vocabularies/            多軸受控詞彙
crosswalks/              D1–D13 與跨 repo 合約
views/generated/         可刪除、可重生輸出（Git ignore）
views/comparisons/       跨 profile 呈現規格；只列 canonical input IDs 與顯示邊界
views/chronologies/      bounded 時間線規格；只列 chronology claim IDs 與顯示邊界
tools/validate.py        canonical integrity validator
tools/store.py           原子寫入與同實體鎖
tools/build_views.py     由 canonical records 原子重生 indexes 與 reader profiles
tests/                   邊界、schema、參照、併發、安全測試
```

## 2. 決策索引

| 要做 | 先看 |
|---|---|
| 新增實體 | `schemas/entity.schema.json` + `catalog/reference-systems/` |
| 新增參考系 | `schemas/reference-system.schema.json` + `schemas/coverage.schema.json`；候選集合必須與裁決集合完全一致 |
| 新增來源 | `schemas/source.schema.json`；取得狀態不等於證據品質 |
| 新增主張／證據 | claim + evidence schema；locator 與 source access gate |
| 新增命名效應 | `schemas/entity.schema.json` 的 `phenomenon` contract + `vocabularies/phenomenon-kinds.json`；必須有受控 kind 與可解析 `domain_entity_ids`，名稱本身不得建立 claim |
| 新增命名現象參考系 | `schemas/reference-system.schema.json` + `vocabularies/reference-system-roles.json`；先判定 canonical taxonomy / specialist index / discovery seed / popular-language inventory |
| 新增跨層機制（後續） | `PLAN.md` 的 P3-M；先驗證 relationship evidence linkage，每一跨層跳接都必須可追溯到 claim 與 source |
| 對接宗教庫 | `crosswalks/d1-d13.json`；第一階段不改 religions-history |
| 產文章／索引 | 只從 canonical records 生成到 `views/generated/` |
| 產跨 pilot 比較 | `views/comparisons/` spec + `tools/build_views.py`；只比較一致結構指標，不把 sections 當語義等價 |
| 產 bounded 時間線 | chronology claim 的 optional `time_anchor` + `views/chronologies/`；保留日期 precision／qualifier，不從 prose 猜日期 |

## 3. 踩雷點

- 舊 48 項不是封閉全集，也不是同一實體類型。
- 舊文章、confidence emoji、`reviewed` 與 `corroborated` 不可繼承。
- metadata、snippet、abstract 與全文證據必須區分。
- 同一實體寫入必須取得 lock；禁止直接覆寫 canonical JSON。
- 單一參考系的 100% coverage 只證明該來源內沒有漏項，不代表心理學宇宙完整；每個參考系都必須保留地域、用途與版本邊界。
- 名稱近似不等於同一 entity：例如 ANZSRC `Clinical and health psychology` 是研究群組，APA CoA `Clinical Health Psychology` 是較窄的專業認證領域，未有 equivalence evidence 前不得合併。
- Coverage view 的 `complete`＝候選集合與裁決紀錄集合相等；`resolved`＝`complete` 且 pending 為零。不得把 `complete:true, resolved:false` 寫成「完成裁決」。
- `context_domain` 是心理學主張的文化／制度／跨學科背景軸，不是心理學 `subfield`；不得因 context record 被納入就宣稱該完整領域屬於心理學。
- `phenomenon` 只登錄命名身份與分類角色；`phenomenon_kind: effect` 不表示效應存在、可重複或已有因果證據。`name_zh` 是譯名，不是獨立 identity。
- `system_role` 決定 reference system 的知識權重；discovery seed 與 popular-language inventory 只能產生候選，不能直接支持 evidence verdict。
- P2-E 每個命名效應拆成 `popular`／`research`／`critique` 三筆獨立 atomic claim；popular framing 不得冒充 research verdict。`metadata_only` 證據與未讀全文的 source 一律 `publishable:false`，validator 的發布閘門（verified + 可讀全文證據）尚未觸發。
- 維基百科只准當 `discovery_seed`（候選清單）與 popular 通俗說法來源，是三手資料；不得當 canonical taxonomy 或 research／critique 證據。候選改用教科書／手冊、課綱、專業機構分類法（ANZSRC／APA CoA／IAAP），證據改用一手研究／meta-analysis／replication 專案，避免反射式抓維基的覆蓋偏誤。
- `indigenous psychology` 有大小寫、地域與語境多義：plural indigenous psychologies 方法論傳統不自動等同「研究 Indigenous Peoples」，華語「本土心理學」也不是無條件 equivalence。每筆 claim 必須寫明所採來源用法與地域範圍。
- Indigenous research 的公開／可重用性不能只靠 FAIR 或一般 open-data 假設判定；涉及 Indigenous data、knowledge 或 community 時，須同時保留 self-determination、leadership、benefit、accountability、CARE 與當地 protocol 邊界。
- ANZSRC Division 45 records 仍是 `context_domain`；P3-S Indigenous psychology pilot 不得把它們升格成 psychology `subfield`，也不得把 Aboriginal and Torres Strait Islander、Māori、Pacific Peoples 或其他民族合成單一文化。
- P4 comparison spec 只能列 profile IDs 與呈現邊界；claims、evidence、sources、relations 和統計都必須在 build 時直接由 canonical records 解參照，禁止把計數或摘要手寫成第二套真相。
- P4 chronology spec 只能列 chronology claim IDs；日期範圍與精度屬 canonical claim 的 `time_anchor`。`year` 不得帶模糊 qualifier，`decade` 必須保存完整十年範圍；時間錨點不得改寫成學派創立日期。
