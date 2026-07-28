# Psychology Knowledge Atlas

心理學的來源、實體、證據、主張與關係知識庫。文章、時間線、比較表與網站資料都是由 canonical records 重生的 views，不是知識真相源。

## 品質原則

- LLM 不是來源；只能協助 discovery、來源內候選摘取、整理已核准 claims 與找缺口。
- `metadata_only`、搜尋 snippet 與未讀 paywall 不能支持全文主張。
- 舊 `psychology-schools` 只提供 `legacy_seed` identity／vocabulary／regression seeds；舊文章與 verdict 不匯入。
- 公開 repo 不保存未授權全文、PDF、EPUB、私人 cache 或帳號內容。
- 「所有學派」指對明列參考系的候選達成 100% 收錄、合併、排除或待裁決紀錄，不宣稱存在封閉全集。

## 資料流

`catalog + library + knowledge + vocabularies + crosswalks` → validator → generated views/indexes。

目前另有來源先行層：`research/targets.json` 固定48項研究目標，`research/source-packs/` 記錄系統性搜尋與下載清冊，全文放在 Git 忽略的 `.private-sources/`。它只代表已發現／已取得，不能直接成為 claim 或 evidence。

## 驗證

```powershell
python tools\validate.py
python -m unittest discover -s tests -v
```

P1 coverage、P1-E 命名現象 universe、P2-E 證據路由與 P3-S 四個學派 pilots 均已通過明確退出門檻。`structuralism`、`psychoanalysis`、`cbt`、`indigenous-psychology` 各完成七個固定問題，publishable claims 均有全文 locator 與短引文，關係均有獨立 evidence。P4 已完成 coverage comparison 與 bounded chronology；P3-M0 已固定九層 mechanism vocabulary 與 relation–evidence 雙向合約，P3-M1 已建立夜間亮光到相位延遲與褪黑激素抑制的兩條直接人體實驗 hops。Atlas 層仍為 `evidence_release:false`。

四個薄型 reader previews 亦已完成：執行 `python tools\build_views.py` 會為四個 pilots 生成 Markdown 與同內容的 JSON dossiers。頁面只收錄 verified/publishable records；generated output 可刪除重建，不是第二套 canonical truth。

第一個跨 pilot P4 view 也已完成：`views/comparisons/p3-school-pilots-comparison.json` 只列四份 profile IDs 與呈現邊界，builder 會直接從 canonical records 重生 `p3-school-pilots-comparison.{md,json}`。它比較發布覆蓋與結構計數，不把章節名稱視為同義，也不以數量推論品質或學派重要性。

第二個 P4 view 是 `views/chronologies/p3-school-pilots-chronology.json`：它由四筆 canonical chronology claims 重生形成時間錨點，明確區分確切年份與 decade-level 範圍。輸出不把時間錨點當成學派創立日期，也不從文字猜測更精確的年份。

第一個 Mechanism Ladder view 是 `views/mechanisms/light-circadian-first-slice.json`。它把夜間亮光呈現為分叉到褪黑激素抑制與晝夜節律相位延遲的兩條直接人體實驗 hops，並把「兩個結果不可互當 proxy」放在獨立 boundary；不建立未測量的串行中介鏈。
