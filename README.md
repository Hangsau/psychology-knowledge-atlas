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

目前階段是 P1 universe：foundation 已驗收；APA CoA 美國專業領域切片完成 11/11，ANZSRC 2020 澳紐研究領域 group-level 切片完成 6/6。兩者合計 17/17 僅代表各自來源內 coverage，不是全球心理學全集；仍須展開 ANZSRC field-level、全球／多地域與 Indigenous-psychology 軸。尚未開始四類 pilot 的實質 claims 研究，也尚未對外發布 evidence-verified 內容。
