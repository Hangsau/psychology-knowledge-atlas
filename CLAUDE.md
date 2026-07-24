# psychology-knowledge-atlas — AI 工作守則

## 一句話

來源與證據優先的心理學知識 atlas；canonical 單位是來源、實體、原子 claim、evidence 與 relation，不是 AI 文章。

## 開工順序

1. 讀 `HANDOFF.md` 的 ACTIVE WORK。
2. 讀 `MAP.md` 的決策索引與踩雷點。
3. 修改 canonical records 前執行 `python tools/validate.py`。
4. 完成後執行 validator 與完整 unittest。

## 計畫與執行節奏

- 若工作已列入 `PLAN.md`／`HANDOFF.md`，或已在對話中核准，使用者說「開始／繼續」後直接執行，不重跑 `plan-check`。
- 只有使用者明確要求、出現未核准的重大跨階段擴張，或涉及高風險／不可逆操作時，才執行完整 `plan-check`。
- 已排入後續 roadmap 不等於立即開工；必須遵守 `PLAN.md` 的 gate 順序。

## 強制規則

- LLM 不得作 `source_id`，也不得自行把 claim 判為已證實。
- 每個 record 一個 JSON 檔；禁止多 agent 共寫巨大 JSONL。
- 所有 ID、tag、relation、claim、evidence 參照必須可解析。
- 來源取得狀態與證據品質分開；metadata／snippet 不能冒充讀過全文。
- 具體事實必須是單一可裁決 claim；複合 claim 拆分。
- `publishable:true` 必須有合格 evidence 與 locator，並通過發布閘門。
- generated views 不手改；刪除後必須能由 canonical data 重生。
- 未授權全文放在 repo 外或 `.private-sources/`，不得 commit。
- 維基百科只能當 `discovery_seed`（候選清單）與 `popular_language_inventory`（通俗說法）兩種角色；它是三手資料，不得作 canonical taxonomy，也不得支撐 research／critique 主張的證據。證據一律取一手研究、meta-analysis 或 replication 專案（Many Labs、Reproducibility Project）；找候選優先用教科書／手冊、課綱與專業機構分類法（ANZSRC／APA CoA／IAAP），避免反射式抓維基造成覆蓋偏誤。
- 新增／改 schema 時同步 tests、HANDOFF、MAP。

## Legacy 邊界

舊庫只可匯入 identity、vocabulary 與 regression-test seeds，且必須同時標為 `legacy_seed`、`unverified`、`publishable:false`。禁止搬入舊綜述文字、emoji confidence 或舊 evidence verdict。
