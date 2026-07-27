# Psychology Knowledge Atlas — Plan

## 目標

建立超越一般教科書深度、以可重取來源和原子主張為核心的心理學知識圖譜，並保留透明的缺口、爭議、版本與文化邊界。

## 階段

1. `P0 foundation`：repo、schema、validator、tests、legacy seeds。
2. `P1 universe`：權威參考系、候選實體、alias、收錄裁決、coverage report。
3. `P2 library`：來源身份、版本、取得狀態與可再發布邊界。
4. `P3 pilots`：structuralism、psychoanalysis、cbt、indigenous-psychology。
5. `P4 views`：由 canonical data 重生文章、索引、時間線與比較。
6. `P5 cross-project`：D1–D13、細標籤與 evidence-backed relations 對接 religions-history。
7. `P6 expansion`：門檻通過後才擴展全庫。

舊 `psychology-schools` 保留為 legacy archive，不刪除、不改寫歷史。

## 即時階段

P1、P1-E 與 P2-E 已完成並有可執行退出門檻。當前位於 `P3-S` 學派 pilots；第一個 target `structuralism` 已完成，第二個 bounded target 是 `psychoanalysis`。本階段建立來源、原子 claim、evidence 與 relation，不回填舊庫綜述文字。

`structuralism` 已完成 S1-S7 退出門檻，並額外完成一個不改變 gate 順序的薄型 P4 reader preview。當前 bounded target 是 `psychoanalysis`；其七題已固定，S1-S6 已完成並有可重生的繁中 reader preview。完整 P4 views 仍待四個 pilots 後進行。

## 已完成 gate

### P2-E exit gate（完成）

P2-E 的目的，是驗證命名效應的資料路由與發布安全，不是無限累積效應研究。以下條件全部通過即結束：

1. 吊橋效應、達克效應、破窗效應三個 bounded pilots 均有 popular／research／critique 三條互相分離的 claim + evidence 路由。
2. 至少一筆 popular claim 以實讀全文、locator 與逐字短引文通過發布閘門。
3. 至少一筆 research finding 以開放全文通過相同閘門。
4. 至少一筆取不到全文的來源誠實停在 abstract／metadata 待辦層。
5. validator、完整測試與專用 `test_p2e_exit_gate_is_satisfied` 全部通過。

上述門檻已由達克效應通俗 claim、Many Labs 1 錨定 finding 與 Nuhfer 待辦案例滿足。其餘效應仍可日後依內容需求研究，但不再阻擋 P3。

## P3-S：學派 pilot

第一個 target 是 `structuralism`。完成條件不是篇幅，而是以下七個固定問題全部有明確裁決；可驗證者建立原子 claim + evidence，證據不足者必須維持 retrieved／disputed／unverified 並寫明缺口：

1. 學派名稱、時間與範圍邊界。
2. Wundt 與 Titchener 的歸屬差異，避免把兩者簡化為同一套 structuralism。
3. introspection／experimental self-observation 的方法定義與限制。
4. 心理元素、聯結與意識結構的核心主張。
5. 關鍵一手著作的書目身份與版本。
6. 主要批評、衰退敘事及其證據邊界。
7. 對後續心理學的影響；影響 claim 必須有 evidence-backed relation，不靠相似性推定。

退出門檻：七題 7/7 均有裁決、所有參照可解析、publishable claim 全部通過全文閘門、沒有把 legacy prose 或 verdict 匯入、validator 與完整測試通過。完成後才進入 `psychoanalysis`，不在單一問題上無限擴張。

### Psychoanalysis 固定七題

1. 名稱、時間與範圍：分開研究程序、治療方法、知識／理論體系與當代機構用法。
2. Breuer–Freud 起源與歸屬邊界：不把催眠／宣洩法直接等同後來的精神分析。
3. 自由聯想、詮釋、阻抗與移情的方法定義及技術邊界。
4. 無意識、壓抑與心理模型的核心主張及版本變化；不把不同年代模型壓成單一教義。
5. 關鍵一手著作的書目身份、版本、翻譯與文本時間線。
6. 療效研究、經驗批評與史學爭議的證據邊界；理論主張、臨床結果與通俗批評分層裁決。
7. 後續學派、心理動力取向與跨領域遺產；每一筆影響或分支關係都必須有 evidence-backed relation。

退出門檻沿用 structuralism pilot：七題 7/7 裁決、publishable records 通過全文閘門、legacy prose/verdict 零匯入、validator 與完整測試通過；之後才進入 `cbt`。

## 已核准後續工作軸

以下內容已納入 roadmap；P1-E/P2-E 已完成，P3-M 與 P4-E/M 仍須遵守 gate 順序。

### Gate 順序

1. P1 核心 coverage axes：已完成。
2. P1-E schema 已完成；下一步建立 bounded candidate universe。
3. 在 P2-E 建立命名效應來源庫與證據路由。
4. 在 P3-M 驗證跨層機制 claim 與 relationship evidence contract。
5. 在 P4-E/M 產生效應卡與機制階梯等衍生視圖。

### P1-E：命名效應、偏誤與現象候選宇宙

- 建立 `phenomenon` entity type，並以 `phenomenon_kind` 區分 effect、bias、illusion、paradox、heuristic、law、syndrome、popular label 等名稱角色；名稱本身不視為真實性或證據強度。
- 以 `system_role` 區分 canonical taxonomy、specialist index、discovery seed、popular-language inventory，避免網路清單直接成為知識事實。
- 每個候選項保留正式名稱、別名、中文譯名、領域、來源系統、納入狀態與排除理由；先完成有邊界的母體，再進入逐項文獻蒐集。

### P2-E：命名效應來源庫

- 為已納入候選建立原始研究、系統性回顧／統合分析、重複驗證、批判或邊界條件、教科書／專業摘要等來源路由。
- 先以吊橋效應、達克效應、破窗效應作為 routing pilots；它們只用來測試不同證據型態，不預設結論相同。
- 明確區分 popular claim、研究實際主張、複現狀態、爭議、適用範圍與常見誤傳。

### P3-M：物理—化學—生物—心理—社會跨層機制

- 建立受控的 `mechanism_level`：physical、chemical / molecular、cellular、neural circuit、physiological system、cognitive / affective、behavioral、interpersonal / social、cultural / institutional。
- 關係只能表達有來源支持的機制或關聯，不把跨層敘事寫成單一路徑的還原論；先修正並驗證 relationship 的 evidence linkage，再建立資料。
- 首個建議 pilot 為「光照 → 晝夜節律／褪黑激素 → 睡眠與認知情緒 → 行為 → 社會作息」，用來測試多層 claim、邊界條件與不同證據類型。

### P4-E/M：衍生視圖

- Named Effect Card：名稱、別名、popular claim、證據摘要、複現／爭議、邊界條件與相關機制。
- Popular Claim vs Evidence：把常見說法與文獻實際支持程度並列。
- Mechanism Ladder：由物理／化學／生物層連到認知、行為與社會層，且每一跳都可追溯到 claim 與 source。
