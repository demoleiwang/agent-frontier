# Agent infra

> harness、memory、MCP、tool calling、agent 生态数据。人工维护；降权 topic，只留真正有用的。

## 条目

### 生态数据
- 2026-08-14 · [State of Open Models: Summer 2026](https://huggingface.co/blog/state-of-open-models-summer-2026) —「Agents are the new user」：按 agent token 统计调用 Hub 的流量，Claude Code 7 月 44.4%（4 月 67.8%），Codex 10.4% → 20.8%，约 1/4 来自未登记 harness。HF 侧面向 agent 的改造：papers 输出 Markdown、agent trace 成为 dataset 类型、Space 的 agents.md、MCP `hf_fs` 工具 + 可挂载 sandbox。

### Memory
- 2026-09-03 · [funes: Give Your Coding Agents a Memory You Own](https://huggingface.co/blog/funes) — 把多个 coding agent 的 session trace 统一解析为 turn/block，本地 Lance 索引（向量 + BM25 → rerank → 时间衰减），`recall` 返回原文 + 出处，不在写入时做摘要；可同步到私有 HF dataset。

### 自动化 ML agent
- 2026-10-08 · [Building with ML Intern](https://huggingface.co/blog/building-with-ml-intern) — 需求 → 训练 → 评测 → 发布全自动，预算默认为 0、超支需批准。prompt 技巧：“Verified facts, do not re-derive”、先测 baseline、先 smoke test。
