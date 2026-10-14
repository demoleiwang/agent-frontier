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
| OSWorld-Verified | 86.2 / 87.6 (Max) | Qwen-CUA | 2026-08-03 | [报告](https://github.com/xlang-ai/Qwen-CUA)（自报） | 纯像素，100 步；已接近饱和 |
| OSWorld-Verified | 84.8 | Kimi K3 | 2026-07-27 | [K3 报告](https://github.com/MoonshotAI/Kimi-K3)（自报） | max effort |
| OSWorld 2.0（offline，partial） | 72.6 | [GPT-6 Astra](https://openai.com/index/gpt-6-astra) | 2026-09-03 | OpenAI（自报） | 每任务耗时比 GPT-5.6 Sol 少约 47% |
| OSWorld 2.0（binary / partial） | 18.5 / 48.4 | [Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA) | 2026-08-03 | 报告（自报） | 单步动作，平均 219 轮 |
| RedTeamCUA ASR ↓ | 16.4（Opus 4.8 为 0.7） | [Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA) | 2026-08-03 | 报告（自报） | prompt injection 抗性差距 |
| AndroidWorld | | | | | |
| ScreenSpot-Pro | | | | | |

## 条目

### 2026-08 → 10 lab 动态（深读结论，详见 [frontier-labs review](../reviews/2026-10-14_frontier-labs.md) §3.1）
- **开源配方**：[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA)（权重 08-26 开放）
  - 纯截图；保留 20 张截图、每次整块折叠 10 张以稳定 KV 前缀；训练切片继承整条 episode 的奖励（[Qwen-CUA 报告](https://github.com/xlang-ai/Qwen-CUA)）。
  - SAPO（τ+ 1.0 / τ− 1.05），G=16；约 40k 可验证任务，pass@8 只保留 0<c<8（[Qwen-CUA 报告](https://github.com/xlang-ai/Qwen-CUA)）。
  - 512 H200，单次 run 约 61k GPU·h（[Qwen-CUA 报告](https://github.com/xlang-ai/Qwen-CUA)）。
  - 作者自列开放问题：单步动作效率低；GUI 与 Bash 的路由（加 Bash 后准确率反而下降）；prompt injection（[Qwen-CUA 报告](https://github.com/xlang-ai/Qwen-CUA)）。
- **企业软件真环境**：OpenAI × [Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad/)，SEC EDGAR 合成任务加 rubric 评分，Astra 55.0 对 GPT-5.6 Sol 41.6。
- **观测空间分歧**：模型侧研究走纯像素；产品 harness 侧走 AX-tree / DOM 优先（[ZCode](https://github.com/zai-org/ZCode) CUA 插件、[Meta Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) 浏览器只给 AX 快照且不能执行 JS）。
- **Google**：computer use 是 Gemini [3.8 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) 的 Preview 能力，窗口内无 CUA 分数；动作集改为桌面级（mouse_down/up、key_down/up、hotkey 等）；[ADK](https://github.com/google/adk-python) 修复了一个跨会话串用沙箱的 bug。
- **常驻云电脑 agent**：不到 4 周内上线 4 个（[Grok Bot](https://x.ai/news/designing-grok-bot) 09-03、Muse 09-08、Copilot [Autopilot](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/) 09-25、[dots](https://openai.com/index/introducing-dots) 09-29）。隔离设计对比见 review §3.1。
- **安全信号**
  - Anthropic：“[这只是模拟](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents)”式[偏置推理](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents)集中在预期解不可达的 GUI computer-use RL 任务中。
  - OpenAI：同家族模型 [unwanted persistence](https://deploymentsafety.openai.com/gpt-6-1-sol) 在 16–28% 之间。

### 候选底座模型

- 2026-08-10 · [Muse Glimmer](https://huggingface.co/blog/muse-glimmer)（Meta，30B dense，Apache 2.0）— 主打本地 agentic + 多模态 tool calling，2B Perception Encoder 偏大，值得测 GUI grounding。
- 2026-07-15 · [Inkling](https://huggingface.co/blog/thinkingmachines-inkling)（Thinking Machines，975B/41B MoE，1M ctx）— 图/文/音原生多模态，另有 276B Inkling-Small。

### 近期论文（2026-09-14 → 10-14，详见 [papers review](../reviews/2026-10-14_papers.md) §3.1）
- **环境**：[RecreationWorld](https://arxiv.org/abs/2609.22000)（Qwen，参考 app 当 oracle）· [SoftwareGym](https://arxiv.org/abs/2610.12611)（SJTU，合成原生应用，Pass@3）· [AutoGUIWorld](https://arxiv.org/abs/2610.01215)（混元，视觉 world model，无执行验证）· DeskForge
- **训练**：[HybridCUA](https://arxiv.org/abs/2609.38008)（ZJU，GUI+CLI 统一动作 + CLI-aware RL，9B 模型 OSWorld 53.6%）
- **评测**：[OSWorld-Pro](https://arxiv.org/abs/2609.24890)（NVIDIA，过程式，2,800+ 子目标）· OSWorld-Science · CUA-SWE（CMU）
- **安全**：[HazardAuditor](https://arxiv.org/abs/2609.15134)（蚂蚁，基于执行轨迹的 guard）
