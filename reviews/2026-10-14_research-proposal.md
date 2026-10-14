# 下半年研究主方向与模块拆解（v2.1，2026-10-14）

> 立场假设：在一个最前沿的 lab 里，为 2026-11 到 2027-04 选题，目标是影响最大。
> 本版取代同日早些时候的 v1；v2.1 只改了命名：从“Muse 级个人 agent”改为“常驻 agent”，Muse 只是其中的代表。v1 以“办公与专业软件练习场 + 环境安全”为主线（[v1 原文](https://github.com/demoleiwang/agent-frontier/blob/c31b2b5/reviews/2026-10-14_research-proposal.md)）。改动原因见 §6 的方向修正记录。
> 证据底稿：[个人 agent 技术深挖](2026-10-14_personal-agent.md)、[办公与专业环境全景](2026-10-14_office-pro-env.md)、[前沿 lab 追踪](2026-10-14_frontier-labs.md)。
> 证据规则：事实就地附原始出处；本文自己的判断标“推论”并附依据。所有数字都是厂商或作者自报。

---

## 0. 一句话主方向

**主方向**：为常驻 agent（自带电脑、一直在线、不用提示也会干活的 agent，个人与团队都算）打造“练习场 + 训练方法”：在一个模拟出来的、属于某个人或某个团队的数字生活里，让 agent 连续几周自己安排时间、记住该记的事、在对的时候出手、用最合适的方式动手（调接口、写代码或点屏幕），把事办成（推论，依据见下方三条与 §1，核心证据为 [VibeLifeBench task.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py#L471-L492) 与 [Grok Bot](https://x.ai/news/designing-grok-bot)）。

这句话的依据（推论，各条出处见 §1）：
- 产品已经冲出去了，但能力不够（[Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)、[VibeLifeBench](https://vibebench.github.io/VibeLifeBench_homepage/)，二手）；
- 练习场和训练方法是学术界和开源界都还没解决的部分（[学术附录 §5](2026-10-14_personal-agent/academic.md)，依据 [K3 §4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）；
- 前沿 lab 恰好具备做这件事的条件（[K3](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf) 的沙箱规模、[Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad) 式的厂商合作）。

---

## 1. 为什么是这个方向：六条理由

1. **这是这一季最热的产品形态，五家前沿公司同时押注。** 9 月 3 日到 29 日，Grok Bot、Muse、Autopilot、dots 先后上线，Gemini Spark 同期扩展（[Grok Bot](https://x.ai/news/designing-grok-bot)、[Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)、[Autopilot](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)、[dots](https://openai.com/index/introducing-dots)、[Spark](https://blog.google/innovation-and-ai/products/gemini-app/gemini-app-now-on-windows/)）。Muse 上线 11 天约 56 万日活（[CNBC](https://www.cnbc.com/2026/09/27/meta-muse-ai-personal-agent.html)，二手）。
2. **产品跑在能力前面，差距很大。**
   - 替人打理几周生活，最强模型平均 32.5 分，越往后越差（[VibeLifeBench](https://vibebench.github.io/VibeLifeBench_homepage/)，二手）。
   - 记忆要靠检索时，最高只有 14.4% 能用上（[InMind](https://arxiv.org/abs/2607.24368)）。
   - 有用户报告 Muse 大约 15 分钟后就反复卡住（[KuCoin](https://www.kucoin.com/news/flash/meta-s-muse-ai-agent-hits-2-8m-downloads-faces-privacy-and-security-challenges)，二手，单一来源）。
3. **模型厂商已经把这些能力当成训练目标，说明方向对。** Meta 把“记得住、不放弃、重要动作前先问”作为 Muse Wonder 的训练目标（[Muse Wonder](https://research.meta.ai/blog/muse-wonder)）；Grok 4.7 专门训练数小时级的任务（[Grok 4.7](https://x.ai/news/grok-4-7)）；Opus 5.5 能连续独立干 18 个多小时（[Anthropic](https://www.anthropic.com/claude-opus-5-5)）。
4. **最核心的能力没人能练、也没人能测。**
   - 产品卖点是“不用提示就开工”（[Grok Bot](https://x.ai/news/designing-grok-bot)），但开源环境里 agent 只在剧本写好的时间点被叫醒（[VibeLifeBench task.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py#L471-L492)）。
   - 没有一家公开“什么时候该打扰”的评测（[nanoMuse roadmap](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/roadmap.md)）。
   - 在多周个人环境里训练，只有 Kimi 自述做过（[K3 §4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
5. **“怎么动手”正处在路线分叉口，谁先回答谁占先机。** OpenAI 把电脑操作全面改成写代码（[commit a0f5a76](https://github.com/openai/openai-cua-sample-app/commit/a0f5a7641df9fbe76968ca41245a5eceee6061ce)），Anthropic 反过来不让代码去点屏幕（[tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference)），而公开材料里没有任何受控对比（[code-CU 附录](2026-10-14_personal-agent/code-computer-use.md)，依据 [Astra](https://openai.com/index/gpt-6-astra)）。
6. **只有前沿 lab 做得起。**
   - 要大量算力并行跑几周长的模拟：Kimi 开发期创建了约 5,100 万个沙箱（[K3](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
   - 要能拿到经过同意的真实使用数据：现有学术数据只有 8 人、83 人、1 人（[MobileMem-Omni](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/README.md)、[Fingertip20k](https://github.com/fyzhang1/ExpActivator/blob/3ef8ce5d923de56e56dc17eada833306dd92ea63/samples/user_profile.csv)、[Activity Frames](https://github.com/nossa-y/activity-frames/blob/a2ce997ef45e9c865d632b8ac601080a758d29d8/research/RESULTS.md)）。
   - 要能和软件公司合作拿到真实应用：OpenAI 已和 Ironclad 这样做（[Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad)）。

## 1.5 为什么是常驻 agent，而不是其他类型的 agent

“Muse 级”只是代称。Muse 是这一类里用户最多、公开细节最多的代表，但 dots、Grok Bot、Autopilot、Spark 都属同一类，团队版的 Team Bots 和 Autopilot 也在内（[Team Bots](https://x.ai/news/team-bots)、[Autopilot](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)）。下面逐类对比：

- **编程 agent：最成熟、最拥挤**：分数已经很高：Opus 5.5 在 Terminal-Bench 4.0 上 66.4%（[Anthropic](https://www.anthropic.com/claude-opus-5-5)），Gemini 4 Argon 在 DeepSWE 上自报 77.9%（[Google](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/)，摘录）。练习环境也最成熟：代码仓库加测试天然可判分，小米已开源整套编程 RL 环境（[MiMo-V2.6](https://arxiv.org/abs/2610.11959)）。结论（推论）：价值最大但各家都在做，新进入者难拉开差距。
- **深度研究 / 搜索 agent：接近饱和**：BrowseComp 换个框架就能到 92.2（[HarnessDev](https://arxiv.org/abs/2609.01437)）。结论（推论）：剩下的主要是框架工程，研究空间在收窄。
- **通用电脑操作：测试已饱和**：OSWorld-Verified 到 86.2（[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA)），Opus 5.5 在 OSWorld 2.1 上 81.8%（[Anthropic](https://www.anthropic.com/claude-opus-5-5)）。真正没定论的是“写代码还是点屏幕”（[OpenAI commit](https://github.com/openai/openai-cua-sample-app/commit/a0f5a7641df9fbe76968ca41245a5eceee6061ce)），这一点放进 M6。
- **办公与专业 agent：分数低，但卡在拿不到环境**：DAYJOB 最强 24.7%（[DAYJOB](https://arxiv.org/abs/2610.01306)），CADWorld 17.5%（[CADWorld](https://arxiv.org/abs/2609.16251)）。瓶颈是商业软件授权和厂商合作（[OSWorld-Science](https://github.com/DiscoAILab/OSWorld-Science/blob/main/configs/snapshots.yaml)、[Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad)）。结论（推论）：值得做，作为 M9 并入同一个练习场。
- **常驻 agent：产品最热、分数最低、环境最缺**：五家一个月内上线（[Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)、[Autopilot](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)）；多周任务最强 32.5 分（[VibeLifeBench](https://vibebench.github.io/VibeLifeBench_homepage/)，二手）；核心能力“自己决定何时开工”没有任何开源环境能测（[VibeLifeBench task.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py#L471-L492)）。
- **而且常驻 agent 是装其他 agent 的“容器”**：Muse Wonder 同时面向个人、专业和编程任务（[Muse Wonder](https://research.meta.ai/blog/muse-wonder)），Grok Bot 跑在 Cursor 的基础设施上（[Grok Bot Enterprise](https://x.ai/news/grok-bot-for-enterprise)），Autopilot 横跨 Teams、Outlook 和文档（[Autopilot](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)）。结论（推论）：常驻 agent 把编程、研究、操作电脑、办公串成一个长期运行的整体，做它的练习场等于同时覆盖了其他几类。

---

## 2. 把大目标拆成 10 个模块

**总体结构**（推论，各模块依据见下文）：

```
M0 持续跟踪与方向校准（贯穿始终）
          │
  ┌───────┴──────────────────────────────┐
  │           练习场（环境）               │
  │  M1 模拟服务层 ─┐                       │
  │  M2 数字人生成器 ─┼─→ M3 时钟与事件引擎 ─┐ │
  │  M6 动手层 ──────┘                    │ │
  │  M4 用户模拟器 ───────────────────────┤ │
  │  M5 任务与判分 ←──────────────────────┘ │
  └───────┬──────────────────────────────┘
          ↓
  M7 基线评测（先看现有模型差在哪）
          ↓
  M8 训练（记忆、主动性、自主安排时间、选对动手方式）
          ↓
  M9 办公与专业任务包（接入 v1 的成果，扩到工作场景）
```

**阅读说明**：每个模块都按同一格式写：做什么、为什么、可以借鉴什么、完成标准、第一步。

### M0 持续跟踪与方向校准（贯穿始终）

- **做什么**：每天自动抓取 lab 博客和论文，每周人工复盘一次；遇到 §5 列出的信号就修正方向，并记入 §6。
- **为什么**：这个领域一个月内就有五个产品、五个前沿模型发布（[前沿 lab 追踪](2026-10-14_frontier-labs.md) 的模型表，依据 [Opus 5.5](https://www.anthropic.com/claude-opus-5-5)、[Gemini 4 Argon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/)），方向可能几周就过时。
- **已有**：本仓库的每日抓取流水线（[PLAN.md](https://github.com/demoleiwang/agent-frontier/blob/claude/inspiring-lovelace-umqw6v/PLAN.md)），以及新增的 personal-agent、code-computer-use 两个追踪主题（[topics.yaml](https://github.com/demoleiwang/agent-frontier/blob/claude/inspiring-lovelace-umqw6v/config/topics.yaml)）。
- **完成标准**：每周一份“变化与是否修正方向”的记录，写在 README 罗盘里。

### M1 模拟服务层

- **做什么**：做一批模拟的常用服务，包括邮件、日历、聊天、文档与表格、网盘、网购、银行账单、出行、外卖。接口照搬真实服务的 MCP，数据存在小数据库里，统一支持“设置状态、重置、对比前后差异、存档、分叉”。
- **为什么**：判分要读后台数据，这是现在最可信的办法（[VibeLifeBench](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)、[CUA-Gym-Hub](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）。服务数量差两个数量级：开源 18–22 个，dots 有 4,000 多个插件（[dots](https://openai.com/index/introducing-dots)）。
- **可借鉴**：
  - VibeLifeBench 的 email_mock，照搬真实接口、只换后端（[SPEC](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/servers/email_mock/SPEC.md)）；
  - Echoverse 的“规格 → 自动检查 → 修到全过”流水线，用来批量生成服务（[Echoverse](https://github.com/microsoft/Echoverse/blob/main/README.md)）；
  - SoftwareGym 的可测试性契约（[Coderprompt.json](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/prompt/Coderprompt.json)）。
- **完成标准**：第一批 8 个服务；重置后状态完全一致；每个接口都有对照真实接口的测试（推论）。
- **第一步**：把 VibeLifeBench 开源的服务跑起来，读清它的接口和数据结构，再决定是改造它还是自己重写（推论，依据 [VibeLifeBench servers](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）。

### M2 数字人生成器

- **做什么**：输入一份人物设定，输出这个人“一年的数字生活”：邮件往来、日程、聊天记录、文件、账单、购物记录、手机使用记录，以及藏在里面的偏好和约束（比如过敏、预算、不坐红眼航班）。所有数据要彼此一致，并填进 M1 的服务里。
- **为什么**：个人 agent 的难点在“懂这个人”。代理交易实验里，85% 的差距来自误读偏好（[Project Swap](https://www.anthropic.com/research/project-swap)）。而模型又爱编造用户特征，比例 35–49%（[Mirage](https://arxiv.org/abs/2608.04570)）。
- **可借鉴**：
  - MobileMem：人设 → 年度事件 → 落成各应用的记录（[MobileMem](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/text/README.md)）；
  - SenWorld：用真实地图、天气、节假日约束，并和真人数据比分布（[SenWorld](https://arxiv.org/abs/2607.19949)）；
  - InMind：“隐藏关联”的设计，比如坚果过敏和马卡龙（[InMind](https://arxiv.org/abs/2607.24368)）。
- **完成标准**：100 个数字人；自动一致性检查通过率达到设定阈值；抽样与真人数据比分布（推论，依据 [SenWorld](https://arxiv.org/abs/2607.19949)）。
- **第一步**：先手写 3 个数字人的“生活剧本”，再写生成器去复现它们，对比差异（推论）。

### M3 时钟与事件引擎（最有新意的一块）

- **做什么**：
  - 让模拟世界有自己的时间，世界可以“悄悄变化”，比如航班改期、价格变动、对方回邮件；
  - **关键是让 agent 可以给自己定闹钟**，比如“明早 9 点查一下退款到没到”。引擎按 agent 自己的安排推进时间、叫醒它，而不是只按剧本叫醒。
- **为什么**：这正是产品卖点和现有环境之间的最大空白（[Grok Bot](https://x.ai/news/designing-grok-bot)、[VibeLifeBench task.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py#L471-L492)）。
- **可借鉴**：
  - VibeLifeBench 的分阶段事件文件（[event.yaml](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/event.yaml)）；
  - nanoMuse 的三种触发器和“没事就安静”的约定（[triggers](https://github.com/nano-muse/nanoMuse/blob/2ab584c/nanomuse/triggers/store.py)、[app.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/app.md)）；
  - Kimi 的“暂停 / 分叉沙箱”，模拟时间跳过时不浪费算力（[K3](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
- **完成标准**：agent 自己设的闹钟确实影响时间推进；同一条事件序列重放结果完全一致；跑一个“7 天模拟”的真实耗时可接受（推论）。
- **第一步**：在 M1 的 3 个服务上，做一个支持“agent 自设闹钟”的最小时钟，跑通一个 7 天任务（推论）。

### M4 用户模拟器

- **做什么**：一个扮演“主人”的模型。它知道 M2 里那个人的真实偏好，只在被问时回答；会因为被频繁打扰而不满，会改主意，也会给出模糊的指令。
- **为什么**：只换模拟用户，同一个 agent 的分数就差 15.2（[UserProxyBench](https://arxiv.org/abs/2609.38043)）；专门训练的模拟用户比直接用大模型扮演更好（[MIMESIS](https://github.com/VietHoang1512/mimesis/blob/main/README.md)）；时机不对的打扰会让信任骤降（[Proactivity-Gym](https://arxiv.org/abs/2609.37267)）。
- **完成标准**：用 UserProxyBench 的方法测它的保真度；它给出的“满意度”要和少量真人评价对得上（推论，依据 [Proactivity-Gym](https://arxiv.org/abs/2609.37267) 的 30 人研究）。
- **第一步**：以 MIMESIS 的开源模拟器为起点，加上“对打扰的反应”（推论，依据 [MIMESIS](https://github.com/VietHoang1512/mimesis/blob/main/README.md)）。

### M5 任务与判分

- **做什么**：设计跨几天到几周的任务，比如搬家、报销、准备考试、组织团建、处理一次退款纠纷。判分只读后台数据，分六个维度：
  1. 事办成没有；
  2. 办得及不及时；
  3. 有没有守住约束；
  4. 记忆有没有用上；
  5. 有没有编造；
  6. 打扰得是否恰当。
- **为什么**：嘴上说办了、实际没办，必须是 0 分（[VibeLifeBench](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）；LLM 当裁判会把“能力”和“信任”混在一起（[Proactivity-Gym](https://arxiv.org/abs/2609.37267)）。
- **可借鉴**：
  - 难度用参考模型的通过率来定（[GDPevo](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/calibration_and_review.md)）；
  - 判分器做“负对照”：初始状态不能通过，解完必须通过（[VeriGen](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/agent_feasibility_verification.md)）。
- **完成标准**：每个任务都满足三条：标准答案能拿满分、什么都不做得 0 分、几种常见的取巧做法拿不到分（推论，依据 [VibeLifeBench 关键词检查的隐患](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/rubrics/_stage_checks.py)）。
- **第一步**：从 VibeLifeBench 开源的 100 个任务里挑 10 个改写，加上“自设闹钟”和“打扰质量”两项判分（推论）。

### M6 动手层：调接口、写代码、点屏幕

- **做什么**：同一个任务同时提供多种做法：直接调接口、带登录态请求网页、在一直开着的浏览器里写代码、点屏幕。每个任务写明“允许用哪些方式”；存档时连代码运行时的状态一起存。
- **为什么**：
  - 路线分叉没有受控对比（§1 第 5 条，依据 [Astra](https://openai.com/index/gpt-6-astra)、[tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference)）；
  - 只换动手方式，成功率就能差 30% 以上（[ComponentBench](https://arxiv.org/abs/2608.18307)）；
  - 不经训练直接给命令行反而掉分（[HybridCUA](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)）；
  - 国内很多服务没有接口，只能点屏幕（[nanoMuse gui.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/gui.md)）。
- **可借鉴**：OpenAI 的单工具 `code` 循环（[sample app](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)）、nanoMuse 的四级阶梯（[gui.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/gui.md)）、ASIL 的“结构化状态加语义动作”（[ASIL](https://arxiv.org/abs/2608.26991)）。
- **完成标准**：每个任务至少能用两种方式完成；同一模型在不同方式下的成功率、步数、耗时、成本可以成对比较（推论）。
- **第一步**：把 OpenAI 示例的 `exec_js` 循环接到 M1 的网页版服务上（推论）。

### M7 基线评测

- **做什么**：用 M1–M6 搭起来的 v0 练习场，测前沿模型（GPT-6 Astra、Opus 5.5、Gemini 4 Argon、Muse Wonder、Grok 4.7）和开源 agent（如 nanoMuse 那套框架），写一份“差在哪”的失败分析。
- **为什么**：先知道问题出在记忆、时机、计划，还是动手，训练才有方向（推论，依据 [VibeLifeBench](https://vibebench.github.io/VibeLifeBench_homepage/) 报告的“随时间衰退”）。
- **完成标准**：一张排行榜和一份失败分类；同时跑一遍外部基准（VibeLifeBench、PAST-Bench、InMind），确认我们的练习场和它们的结论方向一致（推论）。

### M8 训练

- **做什么**：先用已验证的成功轨迹做监督微调，再在练习场里做强化学习。重点练四件事：
  1. 该想起时想起；
  2. 在对的时候出手、没事别打扰；
  3. 给自己安排好时间；
  4. 选对动手方式。
- **为什么**：开源的记忆和主动性训练都还停留在短任务上（[Proactive Memory Agent](https://arxiv.org/abs/2607.08716)、[MIMESIS](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/README.md)）；有好的判分时，强化学习的提升很明显（[NeutronGym](https://arxiv.org/abs/2610.03631)）。
- **完成标准**：在留出的数字人和任务上提升；外部基准同时提升；推理成本不明显增加，因为 Grok 4.7 的教训是输出变长、成本变高（[Grok 4.7](https://x.ai/news/grok-4-7)，第三方测量为二手）。

### M9 办公与专业任务包

- **做什么**：把 v1 积累的办公与专业环境做法，接到同一个练习场里，覆盖电子表格、合同、报销、小生意经营，让个人 agent 也能处理工作上的事。
- **为什么**：Muse 已推出面向小生意的版本（[Muse for Small Business](https://about.fb.com/news/2026/09/introducing-muse-small-business/)）；办公和专业任务的分数仍然偏低（[DAYJOB](https://arxiv.org/abs/2610.01306)）；v1 的方法可以直接复用（[office-pro-env](2026-10-14_office-pro-env.md)，依据 [EngiWorld](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)、[OfficeVal](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)）。

---

## 3. 一步一步的顺序

| 阶段 | 时间 | 要完成的模块 | 阶段终点（看得见的成果） |
|---|---|---|---|
| 1. 跑通最小闭环 | 第 1–4 周 | M1（3 个服务）、M2（3 个手写数字人）、M3（最小时钟）、M5（10 个任务） | 一个前沿模型能在里面跑完一个“7 天任务”，判分正确 |
| 2. 补齐练习场 | 第 5–10 周 | M1 扩到 8 个服务、M2 生成器、M4 用户模拟器、M6 动手层 | v0 练习场：100 个数字人 × 50 个任务 |
| 3. 摸清差距 | 第 9–12 周 | M7 基线评测 | 排行榜和失败分析报告 |
| 4. 开始训练 | 第 12–20 周 | M8 训练 | 第一个在练习场和外部基准上同时提升的模型 |
| 5. 扩展与发布 | 第 20–26 周 | M9、对外开源一部分练习场 | 论文或技术报告，以及开源环境 |

M0 贯穿全程。以上排期是本文的建议（推论），各阶段的依据见 §2 对应模块，例如 [VibeLifeBench](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md) 证明“多服务 + 时间线 + 读后台判分”在几周内可以搭起来。

---

## 4. 不建议做的

- **再做一个通用电脑操作的考试**：通用电脑操作测试的分数已经很高，Opus 5.5 是 81.8（[Opus 5.5](https://www.anthropic.com/claude-opus-5-5)）。
- **只测“问了能不能答”的记忆**：问题出在“该想起时没想起”（[InMind](https://arxiv.org/abs/2607.24368)）。
- **用 LLM 当唯一的裁判**：它会混淆能力和信任（[Proactivity-Gym](https://arxiv.org/abs/2609.37267)）。
- **把安全作为主线**：按你的要求，只在影响设计时顺带处理。例如练习场默认不连外网、模拟服务坏了就停，以免误碰真实网站（[Anthropic](https://www.anthropic.com/research/investigating-unintended-model-actions)）。

---

## 5. 什么情况下要修正主方向（M0 的触发条件）

| 信号 | 如果出现，怎么改 | 盯哪里 |
|---|---|---|
| 有 lab 或团队开源了“agent 能自设闹钟”的多周个人环境 | 不再自建 M3，直接用它，资源转到 M8 训练 | [VibeLifeBench](https://github.com/evolvent-ai/VibeLifeBench)、[nanoMuse](https://github.com/nano-muse/nanoMuse) 的更新，以及论文池里的 personal-agent 主题（[digests/papers.md](https://github.com/demoleiwang/agent-frontier/blob/claude/inspiring-lovelace-umqw6v/digests/papers.md)） |
| 出现受控实验，证明写代码明显优于或不如点屏幕 | 调整 M6 的比重 | [openai-cua-sample-app](https://github.com/openai/openai-cua-sample-app/commits/main)、[Anthropic 文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference) |
| 个人 agent 产品的使用量明显回落，或被平台大面积封堵 | 主线偏向 M9 的工作场景 | 媒体报道，例如 Amazon 封堵（[The Star](https://www.thestar.com.my/tech/tech-news/2026/09/22/amazon-blocks-metas-muse-ai-agent-from-its-retail-site)） |
| Meta 等公开了记忆或主动性的训练方法或基准 | 对齐它们的定义，避免重复造轮子 | [Muse Wonder](https://research.meta.ai/blog/muse-wonder)、Meta 研究博客 |
| 新一代模型在 VibeLifeBench 一类基准上大幅提升 | 把练习场难度往上推：更长时间、更多服务、多设备 | [VibeLifeBench 主页](https://vibebench.github.io/VibeLifeBench_homepage/) |

---

## 6. 方向修正记录

| 版本 | 日期 | 主方向 | 为什么改 |
|---|---|---|---|
| v1 | 2026-10-14（早） | 办公与专业软件练习场，加环境审计与安全（[v1](https://github.com/demoleiwang/agent-frontier/blob/c31b2b5/reviews/2026-10-14_research-proposal.md)） | 起点：用户关注办公与专业场景的环境构建（[office-pro-env](2026-10-14_office-pro-env.md)，依据 [EngiWorld](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)） |
| v2 | 2026-10-14 | Muse 级个人 agent 的练习场与训练方法；办公与专业作为 M9 并入 | 用户指出 v1 漏了 Muse 这一波，并且对安全不感兴趣；补充调研确认五家产品同时押注、能力差距大、核心能力无人能练（[个人 agent 深挖](2026-10-14_personal-agent.md)，依据 [VibeLifeBench task.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py#L471-L492)） |
| v2.1 | 2026-10-14 | 命名改为“常驻 agent”（个人与团队），内容不变 | 用户问为什么一定是 Muse；Muse 只是同类产品中的代表，见 §1.5（依据 [Team Bots](https://x.ai/news/team-bots)） |
