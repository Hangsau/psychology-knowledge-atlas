# Relations

Relation 必須有方向、類型、適用範圍與 evidence；名稱相似不是關係證據。每個 `evidence_id` 都必須在對應 evidence 的 `relation_ids` 回鏈；單向引用由 validator 拒絕。

`mechanism_link` 只表達來源直接支持的一個跨層跳接。兩端必須是具有不同受控 `mechanism_level` 的 mechanism nodes；不得把多篇研究拼成來源未直接檢驗的完整因果鏈。
