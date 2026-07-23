# Reference systems

每個權威參考系必須登錄可重取書目／URL、涵蓋範圍、版本與候選清單。每個候選都要有 `included`、`merged`、`excluded` 或 `pending` 裁決，coverage 才能計為完整。

第一個已完成切片是 `apa-coa-postdoctoral-specialty-practice-areas`（11/11），範圍僅限 APA CoA 的美國健康服務心理學博士後專業領域。四個 legacy seeds 不計入 reference-system coverage。

第二個已完成切片是 `anzsrc-2020-for-psychology-groups`（6/6），範圍是 ANZSRC 2020 FoR Division 52 的 group level。它是澳洲／紐西蘭 R&D 統計分類；`5299 Other psychology` 是 residual bucket，因此記錄後排除，不建立假實體。Division 52 對 Indigenous psychology 的排除指向 Division 45，必須在後續 P1 另行盤點。

`anzsrc-2020-for-psychology-fields` 已完整登錄並裁決 Division 52 的 36 個 field codes：28 個實質 fields 納入、2 個跨參考系 identity 合併、6 個 NEC residual codes 排除，`complete:true` 且 `resolved:true`。此結果只代表 ANZSRC 來源內完成，仍不代表全球心理學 universe 完整。

新增參考系時，必須建立一個 `reference_system` record，並在 `catalog/coverage/` 為 `candidate_ids` 中每一項建立恰好一個裁決 record。`included`／`merged` 必須指向可解析的 entity；`excluded`／`pending` 不得假造 target。
