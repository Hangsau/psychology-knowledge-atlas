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

## P2-SC：48項來源先行蒐集（進行中）

本階段依使用者核准，暫停新增正文與 claims，先完成固定48項研究目標的來源母體。`research/targets.json` 保留原版順序，但明確區分 school、tradition、paradigm、theory、therapy、subfield 與 model；舊庫只提供 identity/order seed，不提供文章、摘要或 verdict。

每個目標在 `research/source-packs/` 有獨立來源包，按 history、primary works、theory/methods、independent critique、empirical status、current status 與 cultural/language context 搜尋；治療類另含 outcomes 與 safety/guidelines。可取得全文下載至 Git 忽略的 `.private-sources/`，並保存 URL、版本、取得狀態、權利註記、MIME、大小、時間與 SHA-256。公開可讀但授權不明資料可私人快取；禁止繞過登入、付費牆、DRM 或技術存取控制。

非英語來源採價值門檻，不設篇數配額：只有原始語言、地方傳統或翻譯／版本差異會影響解讀時才必須補；英語資料已能可靠處理的實證問題不為形式另找外語文章。

退出門檻：48項來源包皆完成明列搜尋協定與來源槽位裁決；所有選定且可直接取得檔案通過格式與雜湊驗證；失敗、重複、版本差異及無合格來源均明確記錄；未授權正文不進 Git；validator、source-pack audit、完整 tests 與 diff checks 通過。退出前不得把「已下載」寫成「已閱讀／已驗證」。

舊 `psychology-schools` 保留為 legacy archive，不刪除、不改寫歷史。

## 即時階段

目前 active gate 是 P2-SC。48項母表與來源包已建立，前36項已完成搜尋、槽位裁決與可取得來源稽核；下一項是 `art-therapy`。已下載／正式書目或摘要頁只代表來源蒐集，不代表已讀全文、已驗證或可發布。原 P4-M1 已完成，不再是 active work。

P1、P1-E、P2-E 與 `P3-S` 均已完成並有可執行退出門檻。四個學派 pilots：`structuralism`、`psychoanalysis`、`cbt`、`indigenous-psychology` 已全部完成。P4-V1 coverage comparison 與 P4-V2 bounded chronology 均已完成；下一個 gate 開始前仍須固定讀者問題、canonical input 集合與退出門檻。

四個 P3-S pilots 均已完成 S1-S7 退出門檻，並各有一個不改變 gate 順序的薄型 P4 reader preview。完整 P4 views 現在可依新的 bounded gate 開始，但不得把 generated output 變成第二套 canonical truth。

## P4-V1：四個學派 pilot 可發布覆蓋比較（完成）

讀者問題：`structuralism`、`psychoanalysis`、`cbt`、`indigenous-psychology` 目前各有多少已驗證／可發布的 claims、evidence、sources、relations 與章節覆蓋，讀者應從哪一節進入？

固定輸入是四份 `views/specs/*.json` reader profiles 及其直接參照的 canonical entities、claims、evidence、relations、sources。輸出是 `views/generated/p3-school-pilots-comparison.{json,md}`。此 view 只比較一致的結構指標與列出各 profile 自己的 section titles；不同 pilots 的七題不宣稱語義等價，也不從數量推論品質高低或學派重要性。

退出門檻：

1. spec 必須恰含四個唯一 profile IDs，且全部可解析。
2. 每個納入的 claim、evidence 與 relation 必須 verified/publishable；source 參照全部可解析。
3. JSON 與 Markdown 可由 canonical inputs 決定性、原子地重生；generated output 不作下一輪輸入。
4. 空 profile list、重複 ID、缺 profile、未發布 claim/relation 與 malformed spec 均有可執行拒絕測試。
5. validator、完整 unittest、concurrent/atomic/reproducible build 與 `git diff --check` 通過後停止；不在本 gate 建立跨學派實質比較 claim。

退出門檻已滿足：四份 profile 精確解析；comparison 直接由 canonical records 產生；空、重複、缺失、不安全、未發布與 orphan endpoint 輸入均有拒絕測試；deterministic、concurrent、atomic build 通過。輸出固定保留「數量不等於品質／重要性／語義等價」警告。

## P4-V2：四個學派形成時間錨點（完成）

讀者問題：四個 P3-S pilots 各有哪些已驗證的形成時間錨點，如何在不製造單一起源或虛假日期精度下依時間閱讀？

固定輸入只有四筆既有 verified/publishable chronology claims：精神分析 1896 術語錨點、結構心理學 1898 綱領錨點、本土心理學 1960 年代末多地倡議，以及 CBT 1970 年代中後期逐步整合。每筆 claim 使用 optional `time_anchor` 保存 start/end、precision 與 qualifier；chronology spec 只列 claim IDs 與呈現邊界，不複製事件文字或日期。

退出門檻：

1. 一筆原子 chronology claim 等於一個 event，四筆 claim 與四個 subject 必須唯一。
2. exact year 與 decade range 由 validator 區分；`late`、`mid_to_late` 不得壓成單一年份。
3. 每個 event 必須 verified/publishable，且至少有一筆 verified/publishable full-text evidence 與可解析 source。
4. 空、重複、缺失、不安全、未發布、無 anchor、錯誤 range 與虛假精度輸入均有拒絕測試。
5. JSON／Markdown 可決定性、原子地重生；並行 build、完整 unittest、validator 與 `git diff --check` 通過。

此 view 固定顯示「時間錨點不等於學派創立日期」；不納入 bibliographic 版本史，也不宣稱四個事件具有相同歷史意義。

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

### CBT 固定七題（完成）

1. 身分、範圍與交付形式：保留 protocol plurality，不把 CBT 寫成單一固定腳本。
2. 認知治療與行為治療的歷史合流：區分 Beck 參與者史、認知治療命名與 1970 年代逐步整合。
3. 認知模型、自動思考、信念與蘇格拉底式評估；模型陳述不冒充所有 CBT 的已證實共同機制。
4. 行為改變、思考紀錄、行為實驗與暴露的功能邊界。
5. 1963、1970、1976、1979 與 2024 關鍵書目及版本差異；新版本內容不得回填舊版。
6. 診斷範圍、控制組、研究品質與追蹤期對療效估計的限制。
7. REBT、第二波與第三波／ACT 的關係；相鄰取向保留獨立 identity，關係必須有 evidence。

退出門檻已滿足：七題 7/7、29 筆 publishable claims、3 筆 evidence-backed relations、七節 reader preview、legacy prose/verdict 零匯入、validator 與完整測試通過。下一個 bounded target 是 `indigenous-psychology`。

### Indigenous psychology 固定七題（完成）

1. 名稱、地域與範圍：區分 indigenous psychologies 方法論傳統、特定 Indigenous Peoples 的心理學，以及華語「本土心理學」的多義用法；三者不得自動視為同義。
2. 歷史與制度形成：保留 1960 年代末以降的多地在地化運動與 Sikolohiyang Pilipino 等地方路徑，不建立單一起源神話。
3. 世界觀、自我、關係與社群：心理現象須放回家庭、社會、文化、生態與歷史脈絡；文化構念不得直接翻譯成既有西方構念。
4. 知識論與研究方法：區分 indigenization from without／from within，保留方法多元、參與者語言、研究關係與跨文化不可直接移植的邊界。
5. 關鍵著作、組織與版本：分開 1993 奠基選集、2000 理論論文、2006 綜合卷及其書目身份，不以後來表述回填早期文本。
6. 殖民性、測量效度、研究倫理與資料／知識主權：以 Indigenous-led 準則固定 self-determination、leadership、benefit、accountability 與 CARE 邊界。
7. 與 cross-cultural、cultural psychology 及地方傳統的關係：相鄰取向保留獨立 identity；branch／comparison 關係必須有全文 evidence，不建立無證據 alias 或 equivalence。

退出門檻已滿足：七題 7/7、26 筆 publishable claims、2 筆 evidence-backed relations、七節 reader preview、context domains 未冒充 psychology subfields、legacy prose/verdict 零匯入、validator、reader build 與 63 tests 通過。P3-S 四個 bounded pilots 已關閉。

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

#### P3-M0：層級與 relation evidence 合約（完成）

- 九個受控層級已固定為 physical、chemical/molecular、cellular、neural circuit、physiological system、cognitive/affective、behavioral、interpersonal/social、cultural/institutional。
- `mechanism_level` 只允許用於明確的 construct／event／finding／model mechanism nodes；不套用到學派、人物或 broad subfield。
- `mechanism_link` 必須跨不同層級，且每筆 relation evidence 必須由 evidence-side `relation_ids` 雙向回鏈。
- 既有 12 筆 relations、17 筆被引用 evidence 已完成 backlink migration；單向、孤兒、未標層級及同層輸入均有拒絕測試。
- Validator 與完整 70-test suite 通過後，才允許建立第一個光照 pilot 資料。

#### P3-M1：夜間亮光的第一個跨層 slice（完成）

- 來源固定為 Rahman et al. (2018) 可讀全文的一手人體實驗（DOI `10.1113/JP275501`；PMCID `PMC5983136`）。
- 建立三個 mechanism nodes：夜間亮光暴露（physical）、人類晝夜節律相位延遲反應（physiological system）、夜間褪黑激素抑制（chemical/molecular）。
- 兩條 `mechanism_link` 分別記錄亮光對相位延遲與褪黑激素抑制的直接實驗結果；每條均有獨立 atomic claim、locator、短引文與雙向 evidence backlink。
- 額外建立一筆 `compares_with` 邊界：在受測連續／間歇模式下，褪黑激素抑制不可作為相位移動的 proxy。它不是第三條 mechanism edge，也不主張兩反應在所有條件下無關。
- 本 slice 不建立睡眠、認知情緒、行為或社會作息 hops；validator 與完整 71-test suite 通過。

### P4-E/M：衍生視圖

- Named Effect Card：名稱、別名、popular claim、證據摘要、複現／爭議、邊界條件與相關機制。
- Popular Claim vs Evidence：把常見說法與文獻實際支持程度並列。
- Mechanism Ladder：由物理／化學／生物層連到認知、行為與社會層，且每一跳都可追溯到 claim 與 source。

#### P4-M1：夜間亮光 bounded Mechanism Ladder（完成）

- `views/mechanisms/light-circadian-first-slice.json` 只列 P3-M1 的三筆 relation IDs；所有 nodes、claims、evidence、sources、levels 與文字均在 build 時由 canonical records 解參照。
- 輸出固定保留兩條共享 physical source node 的分叉 hops，不得重排成 light→melatonin→phase。
- `compares_with` non-proxy relation 在獨立 boundary 區呈現，不計入 mechanism hops。
- 空、重複、缺失、不安全、未發布與錯誤 relation-type 組合均被拒絕；JSON／Markdown 決定性、原子、並行可重生，完整 73-test suite 通過。
