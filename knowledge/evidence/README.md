# Evidence

Evidence 連接 claim、source 與可重現 locator。來源身份存在不代表足以支持 claim。

同一 evidence 可支撐一筆 claim 與零到多筆 relations；支撐 relation 時必須以 `relation_ids` 明列，且 relation 的 `evidence_ids` 必須反向包含該 evidence。
