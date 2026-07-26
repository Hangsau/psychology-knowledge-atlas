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

目前階段是 `P3-S` 學派 pilot。P1 coverage、P1-E 命名現象 universe 與 P2-E 證據路由均已通過明確退出門檻；P2-E 只驗證路由與發布安全，不要求無限研究效應。第一個學派 target 是 `structuralism`，以七個固定問題建立來源、原子 claim、evidence 與 relation，完成 7/7 後才進入 `psychoanalysis`。Atlas 層仍為 `evidence_release:false`。
