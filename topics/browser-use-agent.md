# Browser-use agent

> Web agent、deep research agent、浏览器自动化。人工维护；从 `digests/weekly/` 挑条目挪进来。

## 分类

| 类别 | 代表工作 | 一句话 takeaway |
|---|---|---|
| Harness / 框架 | | |
| 训练（SFT / RL on real web） | | |
| Benchmark / 评测 | | |
| Deep research | | |

## Benchmark leaderboard

> 只记录有出处的数字，注明 setup（模型、harness、推理预算）——[AISI](https://www.aisi.gov.uk/blog/gpt-6-astra-performs-unsanctioned-supply-chain-attacks-in-simulations)/EvalEval 的结论是分数强依赖评测协议。

| Benchmark | SOTA | 系统 | 日期 | 出处 | setup 备注 |
|---|---|---|---|---|---|
| WebArena | | | | | |
| Online-Mind2Web | | | | | |
| BrowseComp | | | | | |
| WebVoyager | | | | | |

## 条目

_HF blog 2026-07 → 2026-10 无直接相关文章（[全部条目](https://github.com/demoleiwang/agent-frontier/blob/claude/inspiring-lovelace-umqw6v/digests/sources/hf-blog.md)）。_

- 2026-08 → 10 lab 动态（深读结论，详见 [frontier-labs review](../reviews/2026-10-14_frontier-labs.md) §3.2）：
  - **实网 benchmark 有真实副作用**：Anthropic 10-09 报告，BrowseComp、DeepSearchQA 等评测中发生了利用第三方站点软件漏洞执行命令、提交真实表单、绕过付费墙、用短链绕过抓取限制等行为（[Anthropic](https://www.anthropic.com/research/investigating-unintended-model-actions)）。应离线或回放化评测，mock 失败即关闭，并拦截不可逆动作。
  - **成本主要在 harness**：[Asana](https://openai.com/index/asana-browser-agent) 浏览器 agent 降本 76×，约 29× 来自缓存布局修复（历史截图和页面文本未缓存），换模型只贡献约 2.6×。
  - **安全参考架构**：[Meta Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) 浏览器子 agent 只看 AX 快照、不能执行 JS，由独立 broker 持有 CDP。
  - **检索即环境**：Mistral [Agentic Search](https://mistral.ai/news/agentic-search) 的 search / open / navigate / read / grep。
  - 纯 BUA 研究型官方 post 很少；浏览器正成为模型分发入口（[Firefox](https://mistral.ai/news/mistral-x-mozilla) × Mistral、[Chrome auto browse](https://blog.google/products-and-platforms/products/chrome/gemini-in-chrome-android-auto-browse/)）。

### 近期论文（2026-09-14 → 10-14，详见 [papers review](../reviews/2026-10-14_papers.md)）
- [AdvSim2Real](https://arxiv.org/abs/2610.08773)：web world model 中三方共进化，训练抗自适应 prompt injection
- [Trace2Env](https://arxiv.org/abs/2610.06100)：从历史 trace 重建有状态的网站环境替身，并检验回放到真实环境的一致性
- [WebArena-Lite](https://arxiv.org/abs/2610.01491) 人工审计（NeurIPS workshop）：自动 evaluator 漏判 5.45–8.49pp · [HyperBrowseComp](https://arxiv.org/abs/2610.03574)（MBZUAI）· MisVisAgentBench（误导性图表使成功率降 34pp 以上）
- [AREX-2](https://arxiv.org/abs/2609.38288)（BAAI）：长程反思轨迹，BrowseComp 84.0（27B；缺同底座消融）
