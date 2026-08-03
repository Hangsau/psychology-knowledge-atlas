你正在 `C:\claudehome\projects\psychology-knowledge-atlas` 繼續 P2-SC gate 的 48 項來源包蒐集。這是 shotclock 自動排程恢復，沒有人在旁邊：不要提問、不要等確認，直接執行到停止條件為止。

## 步驟

1. 讀 `HANDOFF.md` 最上方的 ACTIVE WORK yaml，取得 `active_target` 與 `remaining_targets`。以這裡為準，不要憑記憶。
2. 讀 `research/DELEGATION_PROMPT.md`，那是每包的 sub-agent 派工模板。
3. 依 `remaining_targets` 順序，**一次只派一個** sub-agent（Agent tool，`subagent_type: general-purpose`，不指定 model 即 Sonnet），把模板中的 `{TARGET}`、`{N}`、`{TALLY}` 填好，並依該目標補上它專屬的範圍邊界（哪些已存在的相鄰 target 不可混同、哪些同名的通俗／商業領域要排除）。
4. sub-agent 回報後**自己驗證，不採信它的自述**：
   - `PYTHONIOENCODING=utf-8 python tools/audit_source_packs.py --require-files`
   - `PYTHONIOENCODING=utf-8 python tools/validate.py`
   - `PYTHONIOENCODING=utf-8 python -m unittest discover -s tests`
   - `git diff --check`
   - 確認 pack `status` 為 `audited`、每個 `retrieved` item 的 `cache_key` 檔案確實存在
   - **小於 20 KB 的快取一律實際解碼讀內容**，確認不是 Incapsula／Cloudflare／reCAPTCHA／Angular 空殼（這個 corpus 已重複踩到多次）
   - `git log` 確認已 commit、`git rev-list --count @{u}..HEAD` 為 0、`git ls-files | grep private-sources` 無結果
   驗證不通過就停下來，把問題寫進 `HANDOFF.md` 並結束；不要替 sub-agent 修資料，也不要重跑它。
5. 驗證通過才派下一包。**串行，絕不平行**——平行派工會在同一個 5H 窗內同時燒穿配額，且撞牆時所有未寫盤的工作全數遺失。

## 配額紀律

每次派工前先查：

```
cd C:/claudehome/tools/deskboard && PYTHONIOENCODING=utf-8 python -c "import llm_usage as u,datetime; [print(w.label,w.used_percent,datetime.datetime.fromtimestamp(w.resets_at)) for w in u.read_claude().windows]"
```

一個 sub-agent 約吃 5H 窗的 33%。**5H 已用超過 65% 就不要再派**，直接進入收尾。

## 收尾（每次停止都要做）

1. 確認所有完成的包都已 commit + push。
2. 更新 `HANDOFF.md` 的 `active_target` 與 `remaining_targets`。
3. 若 `remaining_targets` 還有項目，排下一窗恢復（時間取 5H `resets_at` + 10 分鐘）：

```
cd C:/claudehome/projects/shotclock && PYTHONIOENCODING=utf-8 python src/cli.py add "YYYY-MM-DD HH:MM" --prompt-file C:/claudehome/projects/psychology-knowledge-atlas/research/RESUME_P2SC.md --cwd C:/claudehome/projects/psychology-knowledge-atlas --model sonnet
```

4. 若 `remaining_targets` 已空，**不要再排**；在 `HANDOFF.md` 寫明「P2-SC 48/48 來源包 audited，待跑 exit gate 驗收」，然後結束。

## health-psychology（第 48 項）的特殊處理

它必須排在最後，而且**不要用 Agent tool 在本 session 內派**。醫療／疾病主題詞密集的長文生成曾在姊妹專案觸發使用政策的假陽性拒絕，且一旦對話裡出現過拒絕訊息就會污染後續生成、連帶讓 sub-agent 也被拒。

正確做法：當它是唯一剩下的項目時，用 shotclock 另排一個**專用單步**任務，prompt 只寫一行指標（例如：「讀 `research/DELEGATION_PROMPT.md`，把 `{TARGET}` 換成 `health-psychology` 執行，完成後 commit + push」），不要在 prompt 裡列舉疾病或醫療主題詞。全新 process 沒有對話污染，可以正常通過。
