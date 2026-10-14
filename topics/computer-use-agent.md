# Computer-use agent

> GUI / desktop / mobile agent、GUI grounding。人工维护。

## 分类

| 类别 | 代表工作 | 一句话 takeaway |
|---|---|---|
| 端到端 CUA 模型 | | |
| GUI grounding | | |
| Harness / 框架 | | |
| 训练环境 / 数据 | | |

## Benchmark leaderboard

| Benchmark | SOTA | 系统 | 日期 | 出处 | setup 备注 |
|---|---|---|---|---|---|
| OSWorld-Verified | 86.2 / 87.6 (Max) | Qwen-CUA | 2026-08-03 | arXiv 2608.02352（自报） | 接近饱和 |
| OSWorld-2.0 | 69.2 | Gemini 4 Argon | 2026-10-13 | [model card 摘要](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/)（自报） | offline subset |
| Agent's Last Exam | 39.5 | Gemini 4 Argon | 2026-10-13 | 同上（自报） | |
| AndroidWorld | | | | | |
| ScreenSpot-Pro | | | | | |

## 条目

### 2026-08 → 10 lab 动态（详见 [reviews/2026-10-14_frontier-labs.md](../reviews/2026-10-14_frontier-labs.md)）
- **CUA 并入旗舰模型**：Google 下线独立的 2.5 Computer Use 模型，3.8 Flash 成为推荐 CUA 模型；GPT-6.1 Sol / Argon 直接报 OSWorld-2.0。
- **“一 agent 一云电脑”产品化**：OpenAI [dots](https://openai.com/index/introducing-dots/)、Meta [Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)（独立 VM + 浏览器 + Sentinel 出站审批）、xAI [Grok Bot](https://x.ai/news/grok-bot-for-enterprise)、Microsoft Copilot Autopilot、Qwen Book。
- **真实企业软件训练环境**：OpenAI × [Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad/)，在托管的 Ironclad 副本里训练/测试多步合同工作流。

### 候选底座模型

- 2026-08-10 · [Muse Glimmer](https://huggingface.co/blog/muse-glimmer)（Meta，30B dense，Apache 2.0）— 主打本地 agentic + 多模态 tool calling，2B Perception Encoder 偏大，值得测 GUI grounding。
- 2026-07-15 · [Inkling](https://huggingface.co/blog/thinkingmachines-inkling)（Thinking Machines，975B/41B MoE，1M ctx）— 图/文/音原生多模态，另有 276B Inkling-Small。
