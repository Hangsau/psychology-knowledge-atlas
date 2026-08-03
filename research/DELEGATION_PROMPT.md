# P2-SC 來源包派工規格

一包一個 Sonnet sub-agent，串行不平行。把下面模板的 `{TARGET}` 換成目標 id、`{N}` 換成完成後的包數、`{TALLY}` 換成當前累計正文數（見 `HANDOFF.md` 最新 completed_items 行），其餘逐字沿用。

一個 agent 約消耗 Claude 5H 窗的 33%；窗剩餘不足 35% 不派，改用 shotclock 排下一窗。

---

You are completing ONE bounded unit of work in the `psychology-knowledge-atlas` project at `C:\claudehome\projects\psychology-knowledge-atlas`. Report back in Traditional Chinese, but all data written into JSON files must be in English (matching existing packs).

## Background

This atlas is a source-and-evidence-first psychology knowledge graph, currently in gate **P2-SC**: building a source corpus for 48 fixed research targets BEFORE any reading, claims or prose. Your job is target `{TARGET}`.

Critical framing: this gate collects sources. "Downloaded" NEVER means "read", "verified" or "publishable". You are not writing claims, summaries or verdicts. You locate, adjudicate and cache sources, and honestly record what could not be obtained.

## Read these first (mandatory)

1. `CLAUDE.md` — especially 強制規則 and 來源優先序與三層結構. Wikipedia may only serve as `discovery_seed` or `popular_language_inventory`, never as canonical taxonomy and never as evidence for research or critique.
2. `HANDOFF.md` ACTIVE WORK yaml at the top — objective, boundaries, exit gate.
3. `research/source-packs/positive-psychology.json` and `research/source-packs/naikan-therapy.json` — the two most recently completed packs. They are the style reference for `searches[]`, `items[]` and honest `rights_note` wording, including how excluded items are recorded.
4. A completed pack of the same `target_type` as yours, for slot structure.
5. `tools/collect_sources.py` and `tools/audit_source_packs.py` — allowed `access_status` values, allowed item/slot/pack statuses, retrieval mechanics.

## Scope boundaries

Before searching, write down which adjacent targets already exist in this 48-target corpus and must not be conflated with yours, and which popular/commercial territory shares the name. Enforce those boundaries in your `rights_note` fields. Preserve version boundaries where a framework or text was revised. Coverage that records only favourable sources is a failure: search the independent critique and methodological-limitation literature properly, and verify every such source by real search rather than asserting it from memory.

## Workflow

For each slot, run real searches (WebSearch/WebFetch), adjudicate candidates, select what qualifies.

1. Record actual searches in `searches[]` — real queries, systems used, and a `purpose` string stating what you located and what you excluded.
2. Add each selected source to `items[]` with a safe kebab-case `id`, status `"selected"`, and an accurate `access_status`.
3. Retrieve: `PYTHONIOENCODING=utf-8 python tools/collect_sources.py {TARGET} <item-id>`. Always set `PYTHONIOENCODING=utf-8` — the Windows console is cp950 and Unicode output otherwise throws, which can make a successful operation look like a failure.
4. **Verify every retrieved body is real.** This corpus has repeatedly caught bot-challenge shells returning HTTP 200: 212-byte Incapsula pages, 1.8–3 KB proof-of-work or Client-Challenge shells, Angular empty shells, reCAPTCHA pages, "Cookies Turned Off" errors. Check byte size AND inspect actual content. If it is a shell, delete the cached file, remove or replace the item, find a legitimate alternative. A reCAPTCHA *script* on an otherwise complete page is fine — judge by whether real body text and title are present.
5. **Never bypass a login, paywall, DRM or technical access control.** On 403 or subscriber-only/no-redistribution terms, either mark the item `excluded` with the reason in `rights_note`, or fall back to an official abstract/metadata record (PubMed, Europe PMC XML, Crossref, Open Library) with `rights_note` stating explicitly that it is not full text.
6. Set each slot's `status` to `covered` or `searched_no_qualifying_source`. The honest empty result is accepted; padding a slot to look complete is not.
7. Set pack `status` to `"audited"`.

## Verify before committing

- `PYTHONIOENCODING=utf-8 python tools/audit_source_packs.py --require-files`
- `PYTHONIOENCODING=utf-8 python tools/validate.py`
- `PYTHONIOENCODING=utf-8 python -m unittest discover -s tests`
- `git diff --check`
- `git status --porcelain` — nothing under `.private-sources/` may be staged.

## Then update docs and commit

- `HANDOFF.md`: append a `completed_items` line in the existing style (slots covered, bodies cached, boundary decisions, exclusions and why) plus the running tally — after your pack it is **{N}/48**, and the cumulative body count before yours is **{TALLY}**. Update `active_target:` and `remaining_targets:` in the ACTIVE WORK yaml.
- Commit and push, message style e.g. `Audit {TARGET} source pack`.

## Git rules

You may ONLY run `git add <specific paths>`, `git commit`, `git push`, and read-only commands (`status`, `log`, `diff`, `show`). You are **forbidden** from `git reset`, `git pull --rebase`, `git stash`, `git checkout --`, `git clean`, `git rebase`, and any force push. Other work exists in this repository and a working-tree mutation could destroy it. If you hit an unexpected git state, STOP and report rather than resolving it.

## Report back (under 300 words, Traditional Chinese)

Bodies cached and slot distribution; any slot ending `searched_no_qualifying_source` and why; every fake/blocked/excluded endpoint and your handling; the specific scope-boundary calls you made; whether you found genuine critique sources and which; verification command results; commit hash. If you could not finish, say exactly where you stopped rather than reporting partial work as done.
