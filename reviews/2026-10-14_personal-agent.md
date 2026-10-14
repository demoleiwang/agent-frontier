# Muse 级个人 agent 与“写代码操作电脑”：技术深挖（截至 2026-10-14）

> 这份报告回答三个问题：Meta Muse 这一级的个人 agent 在技术上是怎么搭起来的；前沿 lab 的电脑操作为什么开始改成“写代码”；学术界能测、能练到哪一步，离产品还差什么。
> 逐篇细节在附录：[产品拆解（Muse、Grok Bot、Autopilot、dots、Spark、nanoMuse）](2026-10-14_personal-agent/products.md) · [写代码操作电脑（各家接口对比）](2026-10-14_personal-agent/code-computer-use.md) · [学术与开源（18 张论文卡片）](2026-10-14_personal-agent/academic.md)。下半年提案见 [research-proposal](2026-10-14_research-proposal.md)。
> 证据深度：meta.com、x.ai、openai.com 都无法直连，产品细节大多来自官方页面的搜索摘录。GitHub 上的代码和文档是逐个文件读过的；anthropic.com 读的是全文。所有数字都是厂商或作者自报。

---

## 0. 一页结论

1. **个人 agent 是这一季最大的产品浪潮。** 9 月 3 日到 9 月 29 日之间，四家先后上线“自带电脑、一直在线、会主动干活”的个人 agent：xAI 的 [Grok Bot](https://x.ai/news/designing-grok-bot)、Meta 的 [Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)、Microsoft 的 [Autopilot](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)、OpenAI 的 [dots](https://openai.com/index/introducing-dots)。Google 的 [Gemini Spark](https://blog.google/innovation-and-ai/products/gemini-app/gemini-app-now-on-windows/) 在同期扩展到 Windows。
   - Muse 上线 11 天约有 56 万日活（[CNBC](https://www.cnbc.com/2026/09/27/meta-muse-ai-personal-agent.html)，二手）。
   - 也有估计称 10 月初达到约 180 万日活（[KuCoin](https://www.kucoin.com/blog/meta-stock-rises-muse-ai-launch)，二手），各方口径不同。
2. **各家的骨架几乎一样，可以拆成六块。**
   - 一台属于 agent 的电脑（[Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)）；
   - 一套由近及远的“动手方式”：接口优先，其次带登录态的请求、浏览器，最后才是屏幕（[nanoMuse](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/gui.md)）；
   - 一组可读可改的记忆文件（[Meta 帮助页](https://www.meta.com/help/artificial-intelligence/995796179982326/)）；
   - 定时加事件的唤醒机制（[Grok Bot routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)）；
   - 三件套式的人机交接（[dots FAQ](https://help.openai.com/en/articles/20001529-dots-privacy-security-and-safety-faqs)）；
   - 为“记得住、不放弃”专门训练的模型（[Muse Wonder](https://research.meta.ai/blog/muse-wonder)）。
   
   出处见 §2 各节，以及[产品对比表](2026-10-14_personal-agent/products.md)。
3. **“记忆就是几份 Markdown 文件”正在成为行业约定。**
   - Muse 的 Identity（名字、形象、气质）、Soul（核心原则、边界）和 MEMORY.md 都能让用户直接编辑（[Meta 帮助页](https://www.meta.com/help/artificial-intelligence/995796179982326/)，摘录）。
   - 这些字段和开源项目 OpenClaw 的模板一一对应（[IDENTITY](https://github.com/openclaw/openclaw/blob/main/docs/reference/templates/IDENTITY.md)、[SOUL](https://github.com/openclaw/openclaw/blob/main/docs/reference/templates/SOUL.md)）。
   - Microsoft 称 Autopilot 的前身 Scout 由 OpenClaw 驱动（[Scout](https://www.microsoft.com/en-us/copilot/blog/2026/06/02/introducing-microsoft-scout-your-always-on-personal-agent/)，摘录）。
   - 推论：开源实现正在定义个人 agent 的“内部结构”（依据同上两条：[OpenClaw](https://github.com/openclaw/openclaw/blob/main/docs/reference/templates/SOUL.md)、[Scout](https://www.microsoft.com/en-us/copilot/blog/2026/06/02/introducing-microsoft-scout-your-always-on-personal-agent/)）。
4. **OpenAI 把电脑操作改成了“写代码”，而且态度很坚决。**
   - 官方示例仓库在 GPT-6 Astra 发布当天，用一个名为 “removing native mode” 的 commit 删掉了点鼠标的接口（[commit a0f5a76](https://github.com/openai/openai-cua-sample-app/commit/a0f5a7641df9fbe76968ca41245a5eceee6061ce)）。
   - 现在只剩一个参数为 `code` 的工具，运行时一直保留（[README](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)）。
   - Anthropic 走反方向：点屏幕的工具不能从代码里调用（[tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference)）。
   - 两条路孰优孰劣，**公开材料里没有任何受控对比**（[code-CU 附录 §0](2026-10-14_personal-agent/code-computer-use.md)，依据 [Astra](https://openai.com/index/gpt-6-astra)）。
5. **新一代模型开始按“个人助理需要什么”来训练。**
   - Meta 把 Muse Wonder 的目标拆成两项：Active Memory（跨对话记住并取回）和 Active Focus（遇阻坚持、重要动作前先确认）（[Muse Wonder](https://research.meta.ai/blog/muse-wonder)，摘录）。
   - 但对应的两个测试 MemoryBench 和 FocusBench 都是内部的，外部无法复跑（[模型卡](https://research.meta.ai/static/muse-wonder-model-card)，摘录）。
6. **学术界给个人 agent 搭环境的配方已经收敛，但测不到产品最核心的能力。**
   - 共同配方：多个模拟服务，加每个任务的个人数据，加按时间线推进，最后读服务后台的数据判分（[VibeLifeBench](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）。
   - 但 agent 只在剧本写好的时间点被叫醒（[task.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py#L471-L492)），**测不到“自己决定什么时候醒、什么时候出手”**，而这恰恰是产品的核心卖点（[Grok Bot](https://x.ai/news/designing-grok-bot)）。
7. **能力还远不够，这正是机会。**
   - 替人打理几周生活的测试里，最强模型平均 32.5 分，越往后越差（[VibeLifeBench 主页](https://vibebench.github.io/VibeLifeBench_homepage/)，二手）。
   - 记忆放在眼前能答对 84.0%，要靠检索时最高只有 14.4%（[InMind](https://arxiv.org/abs/2607.24368)）。
   - 12 个模型都会编造用户特征，比例 35–49%（[Personalization Mirage](https://arxiv.org/abs/2608.04570)）。
   - 开源的记忆与主动性训练都还停留在短任务上（[学术附录 §0](2026-10-14_personal-agent/academic.md)，依据 [Proactive Memory Agent](https://arxiv.org/abs/2607.08716)、[MIMESIS](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/README.md)）。

---

## 1. 这一波是什么：五个产品一览

| 产品 | agent 在哪跑 | 怎么动手 | 记忆 | 什么时候主动干活 | 模型 |
|---|---|---|---|---|---|
| Meta [Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) | 每人一台云端安全虚拟机；Mac 版还能读本机文件、短信、备忘录、邮件、日历（[Mac 帮助页](https://www.meta.com/help/artificial-intelligence/1126304576638594/)） | 各类账号连接（connector）；浏览器只看页面结构树（AX tree），不能跑 JS（[Meta](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)）；结账走 Link by Stripe | Identity / Soul / MEMORY.md，可编辑，有“遗忘”功能（[帮助页](https://www.meta.com/help/artificial-intelligence/995796179982326/)） | 目标（Goals）加定时任务，如每日检查（[帮助页](https://www.meta.com/help/artificial-intelligence/1484325780075655/)） | Muse Spark 系列，Muse Wonder 将接入（[Meta](https://about.fb.com/news/2026/10/introducing-muse-wonder-models/)） |
| xAI [Grok Bot](https://x.ai/news/designing-grok-bot) | 每个用户一台持久的轻量虚拟机，该用户的所有 Bot 共用（[docs](https://docs.x.ai/grok-bot/security)） | 浏览器、终端、文件、插件 | 每个 Bot 各自记忆；团队版有共享记忆（[Team Bots](https://docs.x.ai/grok-bot/team-bots)） | 定时（间隔 ≥5 分钟，每个 Bot 最多 50 个）加事件，如工单、告警（[routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)） | 未公开 |
| Microsoft [Autopilot](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/) | 企业租户内的云端，有自己的身份和电脑 | Teams、Outlook、文档；前身 Scout 还能用 shell 和浏览器（[Scout](https://www.microsoft.com/en-us/copilot/blog/2026/06/02/introducing-microsoft-scout-your-always-on-personal-agent/)） | “自己的记忆”，细节未公开 | 盯频道、跟进讨论、周期性工作 | 未公开 |
| OpenAI [dots](https://openai.com/index/introducing-dots) | 云端自有电脑和浏览器 | 4,000 多个应用插件，加浏览器（[help](https://help.openai.com/en/articles/20001530-getting-started-with-your-dot)） | 以 ChatGPT 记忆为起点，另有私有笔记 | 空闲时用只读权限做“主动研究”（[FAQ](https://help.openai.com/en/articles/20001529-dots-privacy-security-and-safety-faqs)） | GPT-6 Astra |
| Google [Spark](https://gemini.google/overview/agent/spark/) | Google Cloud 专用虚拟机，加 Windows 入口 | Gmail、Drive 等原生连接，MCP，Chrome 自动浏览 | 未公开；另有加密的跨设备记忆层（[PAC](https://deepmind.google/blog/advancing-private-ai-compute-with-secure-server-side-memory/)） | 定时加持续监视，任务可跨数天到数周（[Live × Spark](https://blog.google/innovation-and-ai/products/gemini-app/productivity-features-gemini-live/)） | Gemini 3.7 Flash，经 Antigravity（[Google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/)） |

**开源对照**：[nanoMuse](https://github.com/nano-muse/nanoMuse)（浙大）把 Muse 的形态搬到用户自己的手机和电脑上，上线 18 天拿到 1,000 个 star（[README](https://github.com/nano-muse/nanoMuse/blob/2ab584c/README.md)），对应论文是 [arXiv 2610.08699](https://arxiv.org/abs/2610.08699)。

---

## 2. 拆开看：一个 Muse 级个人 agent 由哪六块组成

### 2.1 一台属于 agent 的电脑

- **做法**：给每个用户开一台云端虚拟机，里面有浏览器、文件和已存的登录凭据。用户关掉 app 后它继续干，需要批准时才回来找人（[Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)）。Grok Bot、dots、Spark 都是同样的思路（[对比表](2026-10-14_personal-agent/products.md)，依据 [Grok Bot docs](https://docs.x.ai/grok-bot/overview)、[dots](https://openai.com/index/introducing-dots)）。
- **新变化**：不再只在云上，开始回到用户自己的设备。
  - Muse 的 Mac 版可以按应用逐个设成“关闭 / 只读 / 可读可操作”（[Mac 帮助页](https://www.meta.com/help/artificial-intelligence/1126304576638594/)）。
  - nanoMuse 让手机和电脑各跑一个 agent，经中转服务器互相派活；需要批准时，请求回到发起任务的那台设备（[hub.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/hub.md)、[every-device.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/every-device.md)）。
  - Muse 还要上 AI 眼镜（[Connect 2026](https://about.fb.com/news/2026/09/the-biggest-news-from-connect-2026/)）。
- **研究含义**（推论）：环境不能只有“一台云电脑”，还要有“一个人的多台设备”。现有基准把手机、眼镜、桌面分开测（[学术附录 §5](2026-10-14_personal-agent/academic.md)，依据 [MobileMem](https://arxiv.org/abs/2608.13606)、[APM-Bench](https://arxiv.org/abs/2609.37559)）。

### 2.2 动手方式：由近及远的四级阶梯

- **nanoMuse 写得最清楚**（[gui.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/gui.md)）：
  1. 现成技能、命令行或 MCP（[gui.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/gui.md)）；
  2. 带用户登录态直接请求网页（[gui.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/gui.md)）；
  3. 应用内的浏览器（[gui.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/gui.md)）；
  4. 最后才去点手机或电脑的屏幕（[gui.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/gui.md)）。
  
  走第 4 级之前要先说明。原因是国内很多服务没有可调用的接口，例如 12306、微信、支付宝、美团（[gui.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/gui.md)）。
- **Muse 的浏览器是受限的**：只给页面结构树，不给原始网页代码，也不能执行 JS（[Meta](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)）。
- **手机和电脑的“手”是单独的视觉模型。** nanoMuse 的手机操作默认用 `qwen3.8-27b`，坐标落在 999 格的网格上；同一个动作连续出现三次就提醒它换办法（[gui.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/gui.md)）。电脑操作移植自 UI-TARS-desktop（同上）。
- **研究含义**（推论）：“该用哪一级”本身就是要学的决策。nanoMuse 自己承认点屏幕常出错，在认错元素、遇到意外弹窗后恢复不过来这两处尤其多，而且没有评测集（[roadmap.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/roadmap.md)）。

### 2.3 记忆：文件、整理、遗忘

- **存什么**
  - Muse 存三类：身份、原则和关于你的记忆，都是可编辑的文件（[Meta 帮助页](https://www.meta.com/help/artificial-intelligence/995796179982326/)）。
  - OpenClaw 多两类：每天的笔记，以及有日期、有“已被替代”标记的用户画像（[OpenClaw memory](https://github.com/openclaw/openclaw/blob/main/docs/concepts/memory.md)）。
- **怎么整理**：已经变成在后台定期跑的任务。
  - Grok：攒够 24 小时、至少 5 次对话，才合并一次笔记。找旧记忆时 7 成看语义相近、3 成看关键词，越旧的记忆权重越低，每 30 天减半（[13-memory.md](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/13-memory.md)）。
  - nanoMuse：模型只提出整理方案，由代码检查后执行。规则是不引入新词、不删用户亲手写的条目、每轮最多删五分之一，而且所有改动都能撤销（[consolidate.py](https://github.com/nano-muse/nanoMuse/blob/2ab584c/nanomuse/memory/consolidate.py)）。
- **遗忘不彻底**：Muse 承认，删掉之后仍可能保留“从中学到的东西”（[Meta 帮助页](https://www.meta.com/help/artificial-intelligence/995796179982326/)）。
- **研究含义**
  - 难点不在存，在“该想起来的时候想起来”：InMind 里放在眼前能答对 84.0%，靠检索最高 14.4%（[InMind](https://arxiv.org/abs/2607.24368)）。
  - 也在“别编造”：模型有 35–49% 的用户画像是捏造的（[Mirage](https://arxiv.org/abs/2608.04570)）。
  - nanoMuse 路线图上写的就是这两件事（[roadmap.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/roadmap.md)）。

### 2.4 主动性：定时、事件，再由模型判断“值不值得说”

- **唤醒方式都很朴素**
  - Muse 用目标加定时检查（[帮助页](https://www.meta.com/help/artificial-intelligence/1484325780075655/)）；
  - Grok Bot 用定时加事件（[routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)）；
  - nanoMuse 有三种触发：新邮件、日程开始前、外部 webhook（[triggers/store.py](https://github.com/nano-muse/nanoMuse/blob/2ab584c/nanomuse/triggers/store.py)）。
- **“值不值得打扰”全靠模型判断。** nanoMuse 让没事可报的检查以 `[quiet]` 开头，只显示一行（[app.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/app.md)）。dots 空闲时只做只读研究（[FAQ](https://help.openai.com/en/articles/20001529-dots-privacy-security-and-safety-faqs)）。
- **没有一家公开“什么时候打扰”的评测**（[产品附录 §5](2026-10-14_personal-agent/products.md)，依据 [nanoMuse roadmap](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/roadmap.md)）。
- **学术证据**
  - 时机不对，即使事情做对了，用户的信任也会骤降；用户更喜欢它在自己不用电脑时干活（[Proactivity-Gym](https://arxiv.org/abs/2609.37267)，细节为[二手](https://hyper.ai/en/papers/2609.37267)）。
  - 选择性提醒比一直提醒效果好（[Proactive Memory Agent](https://arxiv.org/abs/2607.08716)）。
  - 在日程类场景里，GPT-5.1 只有 26.7% 的场景反应得当（[ProEvent](https://arxiv.org/abs/2607.17701)）。

### 2.5 人机交接：三件套

- **授权按动作或目标来定。** 例如 dots 的自定义规则分“允许 / 需批准 / 交还用户”三档（[dots FAQ](https://help.openai.com/en/articles/20001529-dots-privacy-security-and-safety-faqs)）。
- **批准走系统弹窗，不走聊天消息**，这样网页里的文字没法冒充用户点了同意（[Meta](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)）。
- **登录、验证码、密码交还给人。** Grok Bot 让人接管它的电脑，无人值守时的批准请求约 10 分钟过期（[Grok Bot docs](https://docs.x.ai/grok-bot/approvals-security-and-privacy)）；nanoMuse 用专门的 `hand_over` 动作（[prompts.py](https://github.com/nano-muse/nanoMuse/blob/2ab584c/nanomuse/prompts.py)）。
- **研究含义**（推论）：“什么时候该问人”和主动性是同一个问题的两面。Meta 也把“重要动作前先确认”写进了 Active Focus 的定义里（[Muse Wonder](https://research.meta.ai/blog/muse-wonder)）。

### 2.6 模型：为“记得住、不放弃”而训练

- **Meta**：Active Memory 测的是 6.4 万到 10 万 token 的长对话里，夹着干扰和前后矛盾的信息，看能不能记住。Wonder 85.6，Opus 5.5 81.5，GPT-6 Astra 81.4（[Muse Wonder](https://research.meta.ai/blog/muse-wonder)；分数为二手，[Decrypt](https://decrypt.co/380768/meta-muse-wonder-zuckerberg-frontier-ai-race?amp=1)）。Active Focus 测住房、旅行、IT、金融四类任务，分数未公开（同上）。
- **xAI**：Grok 4.7 的训练题“偏向需要数小时的问题”（[Grok 4.7](https://x.ai/news/grok-4-7)）。
- **Anthropic**：Opus 5.5 有客户报告连续独立工作 18 个多小时（[Anthropic](https://www.anthropic.com/claude-opus-5-5)）。
- **OpenAI**：Astra 被训练成发消息、付款前先暂停等批准（[system card](https://deploymentsafety.openai.com/gpt-6-astra)，摘录）。
- **缺口**：没有一家公开这些能力具体怎么训练，包括数据、奖励和环境（[产品附录 §1.6](2026-10-14_personal-agent/products.md)，依据 [Muse Wonder](https://research.meta.ai/blog/muse-wonder)）。

### 2.7 现实摩擦

- Amazon 从 9 月 20 日起屏蔽 Muse 购物，理由是 agent 不表明身份，以及对它保存凭据的质疑（[The Star](https://www.thestar.com.my/tech/tech-news/2026/09/22/amazon-blocks-metas-muse-ai-agent-from-its-retail-site)，二手）。
- 有报道称 Muse 未经请求读取了私信（[TechRadar](https://techradar.com/ai-platforms-assistants/meta-muse-read-a-writers-private-messages-without-permission-and-its-exactly-why-im-not-ready-to-hand-my-life-over-to-ai-agents)，二手）。
- 打电话这类实时任务，曾由人工在背后代办，之后撤回（[VKTR](https://www.vktr.com/ai-platforms/meta-tested-human-callers-behind-its-muse-ai-agent-without-disclosure/)，二手）。

---

## 3. 写代码操作电脑：OpenAI 的转向与各家分歧

### 3.1 OpenAI 具体怎么做

所有细节都来自官方示例仓库：[README](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)、[responses-loop.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)、[javascript-worker.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/javascript-worker.ts)。

- **只有一个工具**：`exec_js` 或 `exec_py`，参数只有一段 `code`（[responses-loop.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)）。
  - JS 版拿到一个一直开着的 Playwright 浏览器，有 `browser`、`context`、`page` 三个对象（[responses-loop.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)）。
  - Python 版拿到 PyAutoGUI，可以直接控制整个桌面（[responses_loop.py](https://github.com/openai/openai-cua-sample-app/blob/main/python-app/app/responses_loop.py)）。
- **看什么由模型自己决定。** 模型只看到自己代码打印的文字，以及主动调 `display()` 回传的图片。runner 每步也会截图，但只存档，不发给模型（[javascript-worker.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/javascript-worker.ts)）。
- **一次可以做很多步。** 例如写一个循环填完整张表并逐项核对。官方给的理由是“减少模型来回、减少重复输入的上下文”，没有给数字（[README](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)）。
- **状态会保留。** 变量挂在 `globalThis` 上，跨调用都在；每次新任务从干净的浏览器开始（[architecture.md](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/docs/architecture.md)）。
- **这个转向早于 Astra。** 3 月的 GPT-5.4 版示例里，三个场景默认就已经是写代码模式（[scenarios.ts @3751c8b](https://github.com/openai/openai-cua-sample-app/blob/3751c8baa6376c0bbf6cceea2cdc0c0b42996e03/packages/scenario-kit/src/scenarios.ts)）。
- **自家产品也这么做。** Codex 通过 Node REPL 操作电脑（`node_repl`、`cua_repl`）；GPT-6 系列在这条路上强制经过一个自动审查模型（[mcp.rs](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/mcp.rs)、[models.json](https://github.com/openai/codex/blob/main/codex-rs/models-manager/models.json)）。

### 3.2 三家站在三个不同的点上

| 路线 | 代表 | 模型看到什么 | 模型输出什么 |
|---|---|---|---|
| 写代码 | [OpenAI](https://github.com/openai/openai-cua-sample-app/blob/main/README.md) | 自己代码取回的文字或图片 | 任意 JS 或 Python |
| 结构化工具加页面结构树 | [Anthropic](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) | 截图（可局部放大），或浏览器的结构树 | 17 种电脑动作或 31 种浏览器动作；写代码另走一条路，不能用来点屏幕（[tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference)） |
| 纯截图加基础动作 | [Google](https://github.com/google-gemini/computer-use-preview/blob/main/agent.py)、[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf) | 截图 | 点击、输入、拖拽等预定义动作 |
| 受限浏览器 | [Meta Muse](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse) | 只有结构树 | 不能跑 JS |

### 3.3 证据：代码到底比点屏幕强多少

- **厂商侧没有受控对比。** OpenAI 的“快 47%”是 Astra 和上一代模型之间的比较，不是两种接口之间的比较（[Astra](https://openai.com/index/gpt-6-astra)，摘录）。
- **学术侧有几条量化证据**
  - 把软件改造成“结构化状态加语义动作”后，闭源模型超过 80 分，每个任务少于 5 个动作；截图点击的严格分只有 6.6 / 26.6（[ASIL](https://arxiv.org/abs/2608.26991)）。
  - 只换观察和动作方式，成功率就能差 30% 以上（[ComponentBench](https://arxiv.org/abs/2608.18307)）。
  - 不经训练直接给命令行，反而掉分（[HybridCUA](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)、[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
  - 专业软件上同一个模型，命令行 48.3、界面操作 2.0（[EngiWorld](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)）。
  - 把验证过的点击流程编译成可重放的“技能”，token 成本降 90% 以上（[EchoPath](https://arxiv.org/abs/2609.16635)）。
- **没找到专门研究 OpenAI 这种形态的论文**，即“一个一直开着的 Playwright REPL 作为唯一动作”（[code-CU 附录 §4](2026-10-14_personal-agent/code-computer-use.md)，依据 [README](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)）。

### 3.4 写代码带来的新问题（推论，依据见各条）

- **算不算作弊？** 代码可以绕过界面直接改数据。OpenAI 在画图任务里明令禁止 `page.evaluate` 写像素（[catalog.json](https://github.com/openai/openai-cua-sample-app/blob/main/labs/catalog.json)）；EngiWorld 会检测是否绕开了界面（[eval.py](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/eval.py)）。真实工作里能用接口就该用接口，所以每个任务需要写明“允许用哪些方式”。
- **练习环境要能保存和恢复代码运行时的状态**，不只是页面状态（[architecture.md](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/docs/architecture.md)）。Kimi K3 用轻量虚拟机做断点保存和分叉，是可借鉴的做法（[K3](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
- **模型自己决定什么时候看屏幕，可能漏看。** 比如弹窗、画布内容（[javascript-worker.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/javascript-worker.ts)）。

---

## 4. 学术界：怎么给个人 agent 搭练习场

### 4.1 已经收敛的配方

| 环节 | 做法 | 代表 |
|---|---|---|
| 模拟服务 | 自己写轻量的邮件、日历、网店等服务，用小数据库存数据，能一键重置；接口照搬真实服务的 MCP | [VibeLifeBench](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/servers/email_mock/SPEC.md) 22 个、[PAST-Bench](https://github.com/Gen-Verse/PAST-Bench/tree/f8223517ae7491e776b69793d9f11e9d074ab42e/mock_services) 18 个 |
| 造一个人 | 17 个方面的人物设定（随时间变化）→ 一整年的事件 → 落成各个应用的记录和截图 → 从事件反推考题 | [MobileMem](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/text/README.md) |
| 更真实的人 | 用真实地图、天气、节假日数据让人设“过一天”，答案由构造直接决定 | [SenWorld](https://arxiv.org/abs/2607.19949) |
| 时间推进 | 按阶段推进；世界“悄悄变化”就是直接改数据库、不通知 agent | [VibeLifeBench task.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py#L471-L492) |
| 判分 | 读服务后台的数据；嘴上说订好了但没订，这一项就是 0 分 | [VibeLifeBench README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md) |
| 用户模拟 | 训练专门的模拟用户；只换模拟用户，分数就能差 15.2 | [MIMESIS](https://arxiv.org/abs/2610.09484)、[UserProxyBench](https://arxiv.org/abs/2609.38043) |

### 4.2 产品要的，学术界给不了的（推论，依据见各条）

- **agent 自己决定什么时候醒。** 现有开源环境里，唤醒时间全由剧本决定（[task.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py#L471-L492)），而产品的卖点是“不用提示就开工”（[Grok Bot](https://x.ai/news/designing-grok-bot)）。
- **服务覆盖面差两个数量级**：开源环境 18–22 个服务，dots 有 4,000 多个应用插件（[学术附录 §4](2026-10-14_personal-agent/academic.md)，依据 [dots](https://openai.com/index/introducing-dots)）。
- **在数周尺度的个人环境里训练。** 只有 Kimi 在报告中自述做过，没有开源（[K3 §4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
- **真人数据太少**：8 人（[MobileMem-Omni](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/README.md)）、83 人（[Fingertip20k](https://github.com/fyzhang1/ExpActivator/blob/3ef8ce5d923de56e56dc17eada833306dd92ea63/samples/user_profile.csv)）、1 人（[Activity Frames](https://github.com/nossa-y/activity-frames/blob/a2ce997ef45e9c865d632b8ac601080a758d29d8/research/RESULTS.md)）。
- **多设备统一的环境**：还没有（[学术附录 §5](2026-10-14_personal-agent/academic.md)，依据 [MobileMem](https://arxiv.org/abs/2608.13606)）。
- **“悄悄变化”测试的可刷性**：VibeLifeBench 的部分检查是对文本做关键词匹配，拿来当训练奖励前要先查能不能被刷分（[_stage_checks.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/rubrics/_stage_checks.py)）。

---

## 5. 必读清单

| # | 读什么 | 为什么 |
|---|---|---|
| 1 | [openai-cua-sample-app](https://github.com/openai/openai-cua-sample-app/blob/main/README.md) 及其 [commit a0f5a76](https://github.com/openai/openai-cua-sample-app/commit/a0f5a7641df9fbe76968ca41245a5eceee6061ce) | 写代码操作电脑的官方实现，30 分钟能读完 |
| 2 | [nanoMuse docs](https://github.com/nano-muse/nanoMuse/tree/2ab584c/docs)（gui、sentinel、hub、app、roadmap） | Muse 级个人 agent 的最完整开源实现 |
| 3 | [Muse safety 博文](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse) 与 [Muse Wonder](https://research.meta.ai/blog/muse-wonder) | Muse 的架构与模型训练目标 |
| 4 | [Grok Build memory 文档](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/13-memory.md) | 参数最完整的记忆实现 |
| 5 | [OpenClaw memory](https://github.com/openclaw/openclaw/blob/main/docs/concepts/memory.md) | “记忆就是文件”这一约定的源头 |
| 6 | [VibeLifeBench](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md) | 个人 agent 环境的标准配方 |
| 7 | [MobileMem](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/text/README.md) | 怎么造出“一个人的一年” |
| 8 | [Anthropic tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference) 与 [computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) | 另一条路线的完整接口 |
| 9 | [ASIL](https://arxiv.org/abs/2608.26991) 与 [HybridCUA](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md) | 代码对点屏幕的量化证据 |
| 10 | [Proactivity-Gym](https://arxiv.org/abs/2609.37267) 与 [InMind](https://arxiv.org/abs/2607.24368) | 主动性和记忆的关键实验 |
