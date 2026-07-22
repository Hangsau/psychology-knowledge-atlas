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

P1 已開始。APA CoA postdoctoral specialty practice areas 與 ANZSRC 2020 FoR Division 52 groups 已完成；ANZSRC field-level 36/36 已登錄，5201、5202 已裁決，5203–5205 尚有 15 項 pending。下一 gate 是依序清空這些 pending，再加入全球／多地域及 Indigenous-psychology 參考軸。在明確宣告 coverage axes 前不進入 P2／P3 claims。

## 已核准後續工作軸（排隊中，尚未開工）

以下內容已納入 roadmap，但不改變目前 P1 的 active checkpoint，也不得因為已排程而提前建立 claim。

### Gate 順序

1. 完成目前 P1：ANZSRC 5203、5204、5205，接著建立 global / multi-region 參考系統與 Indigenous psychology 專屬軸。
2. 建立 P1-E 命名現象的 schema 與 bounded candidate universe。
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
