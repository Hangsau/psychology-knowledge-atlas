# Views

所有文章、索引、時間線與比較表均由 canonical records 生成。輸出放在 `views/generated/`，可整批刪除後重生，不得手改成第二套真相源。

`views/specs/` 只保存讀者視圖的章節、排序與 canonical record IDs，不得保存事實正文。繁體中文原子敘述保存在 claim 的 `statement_zh`，原文引文仍由 evidence 提供。執行 `python tools/build_views.py` 可重建索引、coverage report、Markdown 讀者頁與相同內容的 JSON dossier。
