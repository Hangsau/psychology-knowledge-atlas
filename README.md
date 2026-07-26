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

## 驗證

```powershell
python tools\validate.py
python -m unittest discover -s tests -v
```

目前階段是 `P3-S` 學派 pilot。P1 coverage、P1-E 命名現象 universe、P2-E 證據路由與第一個學派 target `structuralism` 均已通過明確退出門檻；結構主義的七個固定問題已完成 7/7，且關係具獨立 evidence。下一個 bounded target 是 `psychoanalysis`，開始前先固定問題清單，不沿用舊庫 prose 或 verdict。Atlas 層仍為 `evidence_release:false`。

第一個薄型 P4 讀者預覽亦已完成：執行 `python tools\build_views.py` 會由 34 筆 verified/publishable structuralism claims 生成 `views/generated/structuralism.md` 與同內容的 JSON dossier。頁面不收錄未發布待辦 claim，且 generated output 仍可刪除重建，不是第二套 canonical truth。
