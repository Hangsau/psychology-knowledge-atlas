# Reference systems

每個權威參考系必須登錄可重取書目／URL、涵蓋範圍、版本與候選清單。每個候選都要有 `included`、`merged`、`excluded` 或 `pending` 裁決，coverage 才能計為完整。

第一個已完成切片是 `apa-coa-postdoctoral-specialty-practice-areas`（11/11），範圍僅限 APA CoA 的美國健康服務心理學博士後專業領域。四個 legacy seeds 不計入 reference-system coverage。

新增參考系時，必須建立一個 `reference_system` record，並在 `catalog/coverage/` 為 `candidate_ids` 中每一項建立恰好一個裁決 record。`included`／`merged` 必須指向可解析的 entity；`excluded`／`pending` 不得假造 target。
