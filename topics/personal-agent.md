# Personal agent

> Muse 级个人 agent：自带电脑、一直在线、记忆、主动性、多设备、写代码或点屏幕动手。人工维护。
> 技术深挖见 [personal-agent 报告](../reviews/2026-10-14_personal-agent.md)，主方向与模块见 [research-proposal](../reviews/2026-10-14_research-proposal.md)。

## 产品

| 产品 | 上线 | 要点 |
|---|---|---|
| [Grok Bot](https://x.ai/news/designing-grok-bot) | 09-03 | 每用户一台 microVM，Bot 名册，定时加事件触发 |
| [Meta Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) | 09-08 | 云端安全虚拟机加 Mac 本机；Identity / Soul / MEMORY.md；Link by Stripe 结账 |
| [Copilot Autopilot](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/) | 09-25 | 租户内有身份的常驻 agent；前身 Scout 由 OpenClaw 驱动 |
| [OpenAI dots](https://openai.com/index/introducing-dots) | 09-29 | GPT-6 Astra，空闲时只读主动研究，自定义规则三档 |
| [Gemini Spark](https://gemini.google/overview/agent/spark/) | 持续更新 | Google Cloud 虚拟机，任务可跨数天到数周 |
| [nanoMuse](https://github.com/nano-muse/nanoMuse)（开源） | 09-25 | 每台设备一个 agent，四级动手阶梯，三种触发器 |

## 基准与环境

| 名称 | 测什么 | 最强（自报） | 出处 |
|---|---|---|---|
| VibeLifeBench | 多周、22 个模拟服务的生活任务 | 32.5（二手），随时间衰退 10–15 分 | [repo](https://github.com/evolvent-ai/VibeLifeBench)、[主页](https://vibebench.github.io/VibeLifeBench_homepage/) |
| InMind | 记忆的隐藏关联 | 检索式最高 14.4%，放进上下文 84.0% | [arXiv](https://arxiv.org/abs/2607.24368) |
| Personalization Mirage | 编造用户特征 | 12 个模型都在 35–49% | [arXiv](https://arxiv.org/abs/2608.04570) |
| PAST-Bench | 跨会话从经验中改进 | 提升真实但不均匀 | [repo](https://github.com/Gen-Verse/PAST-Bench) |
| MobileMem | 一年手机经历的记忆 | — | [repo](https://github.com/zjunlp/MobileMem) |
| Proactivity-Gym | 主动性：能力、时机、信任 | 23 种配置差距明显 | [arXiv](https://arxiv.org/abs/2609.37267) |
| MemoryBench（Meta 内部） | 长对话记忆 | Muse Wonder 85.6（二手） | [Muse Wonder](https://research.meta.ai/blog/muse-wonder) |
