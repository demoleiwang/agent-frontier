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

> 只记录有出处的数字，注明 setup（模型、harness、推理预算）——AISI/EvalEval 的结论是分数强依赖评测协议。

| Benchmark | SOTA | 系统 | 日期 | 出处 | setup 备注 |
|---|---|---|---|---|---|
| WebArena | | | | | |
| Online-Mind2Web | | | | | |
| BrowseComp | | | | | |
| WebVoyager | | | | | |

## 条目

_HF blog 2026-07 → 2026-10 无直接相关文章。_

- 2026-08 → 10 lab 动态（深读结论，详见 [frontier-labs review](../reviews/2026-10-14_frontier-labs.md) §3.2）：
  - **实网 benchmark 有真实副作用**：Anthropic 10-09 报告，BrowseComp、DeepSearchQA 等评测中发生了利用第三方站点软件漏洞执行命令、提交真实表单、绕过付费墙、用短链绕过抓取限制等行为。应离线或回放化评测，mock 失败即关闭，并拦截不可逆动作。
  - **成本主要在 harness**：Asana 浏览器 agent 降本 76×，约 29× 来自缓存布局修复（历史截图和页面文本未缓存），换模型只贡献约 2.6×。
  - **安全参考架构**：Meta Muse 浏览器子 agent 只看 AX 快照、不能执行 JS，由独立 broker 持有 CDP。
  - **检索即环境**：Mistral Agentic Search 的 search / open / navigate / read / grep。
  - 纯 BUA 研究型官方 post 很少；浏览器正成为模型分发入口（Firefox × Mistral、Chrome auto browse）。
