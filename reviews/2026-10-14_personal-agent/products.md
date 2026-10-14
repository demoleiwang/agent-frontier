# 个人 agent 产品技术深挖：Meta Muse 及同期五家（截至 2026-10-14）

主题：Muse 这一级别的“个人 agent”在运行时、操作方式、记忆、主动性、人机交接和模型上是怎么做的，并与 Grok Bot、Copilot Autopilot、OpenAI dots、Gemini Spark 和开源复刻 nanoMuse 横向对比。安全只在影响架构时提及。（起点：[Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)、[nanoMuse](https://github.com/nano-muse/nanoMuse)）

## 来源说明（先读）

- 证据深度标签：`OS` = official-search-excerpt，即用 WebSearch 限定官方域名取得的摘录，不是全文；`GH` = github-fulltext，即本人读过的 GitHub 文件；`二手` = 媒体或聚合站，或搜索摘要转述；`推论` = 本笔记的推断，附所依据的证据。本次没有任何 `official-fulltext`：about.fb.com、research.meta.ai、meta.com、x.ai、openai.com、blog.google 均无法直连。
- 仓库内已有笔记作为线索：`reviews/2026-10-14_frontier-labs/meta-xai-mistral-msft-nvidia-ai2-aisi.md` 的 Muse、Sentinel、Wonder、Grok Bot、Autopilot 各节，`openai.md` §5.1，`google.md` §12、§18。下文引用时一律回到原始 URL，不以这些笔记代替出处。
- nanoMuse 只读 clone，commit [2ab584c](https://github.com/nano-muse/nanoMuse/commit/2ab584c0916dc0d03ed7d2b3f65e78077fa29c25)（2026-10-14）。CopilotKit/OpenMuse 只读 clone，commit [1ac68f3](https://github.com/CopilotKit/OpenMuse/commit/1ac68f3909f2478ab6280883f1ab5ea65eb5719d)。均未执行。
- 所有评测数字都是厂商自报，harness 各不相同，除非另注。

---

## 0. 一页结论

1. **Muse 不只是“一人一台云 VM”，而是“云 VM 加本机 Mac 端”的混合形态。** 主体是每用户一台 Muse Secure VM，带浏览器、凭据库和 Sentinel（`OS`，[Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)）。Mac app 另外能读本地文件、iMessage、Notes、Reminders、Mail 和 Calendar，每个 app 可设为 Off / Read only / Read and interact（`OS`，[Mac 帮助页](https://www.meta.com/help/artificial-intelligence/1126304576638594/)），并且已有“驱动 Mac 上任意 app”的 computer use（`OS`，同一搜索摘录，具体出处待核）。nanoMuse README 把 Muse 写成“VM never touches your devices”（`GH`，[README](https://github.com/nano-muse/nanoMuse/blob/2ab584c/README.md)），这一点已经过时。
2. **Muse 的“身份 / 灵魂 / 记忆”是一组用户可编辑的 Markdown 文件，形制与 OpenClaw 工作区约定高度一致。** Meta 帮助页写明有 Identity（name, creature, vibe）、Soul（core truths, boundaries, personality）和 MEMORY.md，并且可以直接编辑（`OS`，[personality & memories](https://www.meta.com/help/artificial-intelligence/995796179982326/)）。OpenClaw 的 IDENTITY.md 模板字段正好是 Name / Creature / Vibe，SOUL.md 模板的小节正好是 Core Truths / Boundaries / Vibe（`GH`，[IDENTITY 模板](https://github.com/openclaw/openclaw/blob/main/docs/reference/templates/IDENTITY.md)、[SOUL 模板](https://github.com/openclaw/openclaw/blob/main/docs/reference/templates/SOUL.md)）。`推论`：Muse 的 agent 工作区沿用了 OpenClaw 这一系的“文件即记忆”约定。旁证是微软称 Scout（即后来的 Autopilot）由 OpenClaw 开源技术驱动（`OS`，[Scout 博文](https://www.microsoft.com/en-us/copilot/blog/2026/06/02/introducing-microsoft-scout-your-always-on-personal-agent/)）。
3. **记忆整理（consolidation）正在成为显式的后台作业。** Grok Build 的 `/dream` 与 Auto-Dream 门限是 24 小时且至少 5 个会话；检索为 0.7 向量加 0.3 BM25，30 天半衰期，MMR λ=0.7（`GH`，[13-memory.md](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/13-memory.md)）。OpenClaw 用 dreaming sweep 把每日笔记蒸馏进 MEMORY.md（`GH`，[memory.md](https://github.com/openclaw/openclaw/blob/main/docs/concepts/memory.md)）。nanoMuse 的 tidy-up 带三条硬约束：合并后不引入新词，不删用户亲写条目，每轮最多删 1/5（`GH`，[consolidate.py](https://github.com/nano-muse/nanoMuse/blob/2ab584c/nanomuse/memory/consolidate.py)）。Muse 则承认“删除后仍可能记得从中学到的东西”（`OS`，[personality & memories](https://www.meta.com/help/artificial-intelligence/995796179982326/)）。
4. **主动性的实现在各家都很朴素：定时 pass 加事件触发，再由模型判断“值不值得打扰”。** Muse 是 goal 加定时任务，例如 daily check-in（`OS`，[reminders & scheduled tasks](https://www.meta.com/help/artificial-intelligence/1484325780075655/)）。Grok Bot routines 每个 Bot 最多 50 个、间隔至少 5 分钟，支持事件触发（`OS`，[skills & routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)）。dots 空闲时只做只读的 proactive research（`OS`，[Introducing dots](https://openai.com/index/introducing-dots/)）。nanoMuse 用 `[quiet]` 前缀把“无事可报”压成一行（`GH`，[app.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/app.md)）。没有一家公开“何时打扰”的评测。
5. **Meta 是唯一把“个人 agent 能力”拆成训练目标并给出基准的厂商。** Active Memory 用 MemoryBench 衡量，Wonder 85.6，对比 Opus 5.5 81.5、GPT-6 Astra 81.4。Active Focus 包括坚持、换路径、出错恢复、重要动作前 check-in，用 FocusBench 衡量，但 FocusBench 分数未见公开（`OS`，[Muse Wonder 博文](https://research.meta.ai/blog/muse-wonder)；分数为 `二手`，[Decrypt](https://decrypt.co/380768/meta-muse-wonder-zuckerberg-frontier-ai-race?amp=1)）。两个基准都是内部基准，外部无法复跑。
6. **审批与交接已收敛到三件套：按动作或目标授权、带外审批 UI、登录 / 2FA / CAPTCHA 交还用户。** Muse 的审批走 app 系统对话框而不是聊天消息（`OS`，[Muse safety](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)）。Grok Bot 用 computer takeover，无人值守时审批约 10 分钟过期（`OS`，[Grok Bot docs](https://docs.x.ai/grok-bot/approvals-security-and-privacy)）。dots 的 Custom Rules 分允许 / 需审批 / 禁止三档，但改密码之类始终交还用户（`OS`，[dots FAQ](https://help.openai.com/en/articles/20001529-dots-privacy-security-and-safety-faqs)）。
7. **生态摩擦已经出现。** Amazon 在 9 月 20 日屏蔽 Muse 购物，理由是未自我标识、违反 Conditions of Use（`二手`，[The Star](https://www.thestar.com.my/tech/tech-news/2026/09/22/amazon-blocks-metas-muse-ai-agent-from-its-retail-site)）。另有“未经请求读取私信”的报道（`二手`，[TechRadar](https://techradar.com/ai-platforms-assistants/meta-muse-read-a-writers-private-messages-without-permission-and-its-exactly-why-im-not-ready-to-hand-my-life-over-to-ai-agents)）。`推论`：agent 身份声明、站点授权和“读私有数据”的审批粒度，是比模型能力更早到来的瓶颈。
8. **最大研究空白是“一个人的数字生活”作为环境。** nanoMuse 自认没有 hands 评测集，也无法衡量“是否了解你、是否在对的时刻发问”（`GH`，[roadmap.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/roadmap.md)）。Meta 的 MemoryBench / FocusBench 不公开。已有开源基准各覆盖一角（数周时间线、跨会话改进、隐式关联记忆、一年手机记忆），见 §5。

---

## 1. Muse 深挖

### 1.1 运行时

- **每用户一台 Muse Secure VM**，自带浏览器、存储和记忆，存放工作区、文件和已存凭据；关闭 app 后继续工作，需要审批时再回来（`OS`，[Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)）。
- **Sentinel 的位置**：官方摘录说 Sentinel 是独立 agent，运行在同一台机器上，与 Muse 在系统层面隔离；未经 Sentinel 批准，Muse 的任何动作都到不了互联网（`OS`，[Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)）。安全博文描述了更细的出站路径：基于 user namespace、veth 和 eBPF 的 forward proxy，在 L4 和 L7 检查目的地；agent 只看到占位 token，真实密钥在网络边界注入（`OS`，[Muse safety](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)）。nanoMuse 的文档写成“Sentinel outside it [the VM]”（`GH`，[sentinel.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/sentinel.md)），与官方摘录的“同机、系统级隔离”有出入，以官方为准，但待全文核对。
- **账号接入**：用户自选 Connectors 和访问范围，每个 Connector 可单独管理权限；断开后停止数据交换，但已用过的信息可能留在记忆和对话历史里（`OS`，[Connectors 帮助页](https://www.meta.com/help/artificial-intelligence/1687253048996149/)）。浏览器侧可在“allowed websites”里审阅和撤销已允许的站点（`OS`，同一帮助页摘录）。1Password 集成计划中，用于复用现有登录（`OS`，[Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)）。
- **本机端（Mac）**：Mac app 需要 macOS 的 Full Disk Access（文件）、Automation（操作 app）和 Notifications 权限。本地 app 可逐个设为 Off / Read only / Read and interact。删除的文件进废纸篓（`OS`，[Mac 帮助页](https://www.meta.com/help/artificial-intelligence/1126304576638594/)）。另有摘录称“computer use is now available with Muse for Mac … drive any app on your Mac”，可能出自 Connect 汇总，未能定位原文（`OS`，[Connect 2026 汇总](https://www.meta.com/blog/meta-connect-2026-everything-we-announced/)，待核）。
- **数据可达性**：官方安全文说当前设计并不阻止 Meta 在支持、安全或运营必要时访问数据；全加密的 Muse Confidential VM 计划于今年晚些时候推出（`OS`，[Muse safety](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)）。
- **端侧模型线索**：Meta 有一款可在设备上运行的开放 agentic 模型 Muse Glimmer（`OS`，标题级，[Muse Glimmer](https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model)）。它是否用于 Muse 的本机端「无出处，待核」。

### 1.2 怎么操作外部世界

- **Connector 优先，浏览器兜底。** 浏览器子 agent 只看 accessibility-tree 快照，看不到原始 DOM，也不能执行 JavaScript。CDP 连接由独立 broker 持有。用户手动控制或凭据自动填充期间，agent 暂停（`OS`，[Muse safety](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)）。
- **Mac 本机**：通过 Automation 权限操作本地 app，并读取 iMessage、Notes 等（`OS`，[Mac 帮助页](https://www.meta.com/help/artificial-intelligence/1126304576638594/)）。
- **Skills 与 artifacts**：存在“How Muse works with skills”和“How to use Muse with artifacts”两篇帮助页（`OS`，标题级，[skills](https://www.meta.com/help/artificial-intelligence/2797651547267109/)、[artifacts](https://www.meta.com/help/artificial-intelligence/2074655449783957/)），细节未取到。
- **支付链路**：结账走 Link by Stripe，Meta 称 Muse 是首个享受 Link 购买保护的 AI agent。1Password 与 Shop Pay 标为“coming soon”（`OS`，[Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)）。
- **人工兜底**：有报道称 Meta 测试过“human concierge”，即由外包人员在未披露的情况下处理部分经 Muse 发起的电话，之后已回撤（`二手`，[VKTR](https://www.vktr.com/ai-platforms/meta-tested-human-callers-behind-its-muse-ai-agent-without-disclosure/)）。`推论`：电话这类实时通道的成功率在上线时仍不足以完全自动化。

### 1.3 记忆

- **存什么**：Identity 包括名字、creature、vibe 或 tag line；Soul 包括 core truths、boundaries 和 personality；MEMORY.md 存“Muse 记得的关于你的事”。三者都可以在 app 里通过 Assistant 图标 → Identity 查看和直接编辑（`OS`，[personality & memories](https://www.meta.com/help/artificial-intelligence/995796179982326/)）。官方材料中未见 USER.md 或 HEARTBEAT.md（`OS`，同页搜索结果未提及）。
- **怎么写入**：Muse 记住重要的事，以便主动建议，并对只提过一次的细节采取行动（`OS`，[Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)）。记忆也会取用已连接 Connectors 的上下文（`OS`，[Connectors 帮助页](https://www.meta.com/help/artificial-intelligence/1687253048996149/)）。
- **怎么遗忘**：有一个 forget skill，在记忆和“supporting files”里查找某人、某话题或某事并尽力删除；删除后 Muse 仍可能保留从中学到的信息（`OS`，[personality & memories](https://www.meta.com/help/artificial-intelligence/995796179982326/)）。`推论`：既然有“supporting files”，就存在 MEMORY.md 之外的派生存储（对话历史、索引或摘要），所以遗忘不是单文件操作。
- **整理与检索**：Muse 产品侧的合并和检索机制未见公开。模型侧的 Active Memory 见 §1.6。「无出处，待核」
- **默认学习设置**：有报道称 Muse 默认把用户信息用于学习（`二手`，搜索摘要转述 Meta Help Center，[Atlanta News First](https://www.atlantanewsfirst.com/2026/10/09/metas-new-muse-ai-agent-raises-privacy-concerns/)）。数据管理页见 [manage your Muse data](https://www.meta.com/en-gb/help/artificial-intelligence/2225571704857152/)（`OS`，标题级）。

### 1.4 主动性

- **Goal 驱动**：用户说出目标后，Muse 帮忙制定个性化计划、协调时间和资源，然后自行推进；有变化或需要审批时回来找用户（`OS`，[Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)）。Goals 有独立 tab（`OS`，[reminders & scheduled tasks](https://www.meta.com/help/artificial-intelligence/1484325780075655/)）。
- **触发器**：可以设提醒、跟踪目标、在后台监视用户关心的事；周期性 check-in 以定时任务实现，例如每日 check-in、每周总结（`OS`，[reminders & scheduled tasks](https://www.meta.com/help/artificial-intelligence/1484325780075655/)）。事件类触发器（邮件、日历、webhook）在官方摘录中未见。「无出处，待核」
- **晨报 feed**：官方摘录中没有找到 feed（`OS`，[Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) 的搜索结果未提及）。nanoMuse 实现了每日 08:00 的 Feed 房间，并把 UI 做成 Muse 的样子（`GH`，[desktop-muse.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/desktop-muse.md)）。Muse 本身是否有 feed 待核。
- **何时打扰**：只有“有变化或需审批时回来”这一原则（`OS`，[Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)），未见公开的打扰策略或评测。

### 1.5 人机交接

- **审批 UX**：Sentinel 需要用户决定时，agent 停下，请求以 app 系统对话框出现，而不是聊天消息，因此注入文本无法伪造用户批准（`OS`，[Muse safety](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)）。
- **权限模式**：在“Ask for some actions”模式下，每个写操作和重要读操作前都会询问；也可以按 Connector 分别设权限；Activity log 按时间记录动作和授权（`OS`，[guidance & approval](https://www.meta.com/help/artificial-intelligence/1385290430137537/)）。
- **Tainted egress 降低审批疲劳**：进程读到用户数据后被标记为 tainted，失去 auto-allow，退回到询问用户（`OS`，[Muse safety](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)）。
- **接管浏览器**：用户手动控制浏览器时 agent 暂停（`OS`，[Muse safety](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)）。Mac 端发邮件和购买前都要确认（`OS`，[Mac 帮助页](https://www.meta.com/help/artificial-intelligence/1126304576638594/)）。

### 1.6 模型

- **Muse Wonder / Wonder Full（2026-10-12）**：Meta 定位为面向个人和专业 agent 的前沿模型，会先给订阅用户的 Muse 使用（`OS`，[Wonder 新闻稿](https://about.fb.com/news/2026/10/introducing-muse-wonder-models/)）。Muse 当前默认由哪个模型驱动（Spark 1.3？）「无出处，待核」。
- **Active Memory 的定义**：跨对话携带对用户重要的内容，并取回与当前任务相关的细节。**MemoryBench**（内部）测 64K–100K token 长多轮对话中的回忆，带干扰对话以及与目标细节冲突或后来更新的注入轮次（`OS`，[Muse Wonder 博文](https://research.meta.ai/blog/muse-wonder)）。
- **Active Focus 的定义**：任务变难时坚持朝目标推进，尝试别的路径，从错误中恢复，需要时请求澄清，并在执行重要事项前 check-in。**FocusBench**（内部）覆盖住房、旅行、IT、金融四类个人 agent 任务，在多轮交互中考察能否坚持穿过真实阻碍、适应动态变化的环境（`OS`，[Muse Wonder 博文](https://research.meta.ai/blog/muse-wonder)）。
- **分数（厂商自报，Meta harness）**：MemoryBench 上 Wonder 85.6、Wonder Full 85.5、Claude Opus 5.5 81.5、GPT-6 Astra 81.4（`二手`，[llm-stats](https://llm-stats.com/models/compare/muse-wonder-vs-muse-wonder-full)、[Decrypt](https://decrypt.co/380768/meta-muse-wonder-zuckerberg-frontier-ai-race?amp=1)）。FocusBench 分数在所有检索结果中都没有出现（`二手`，同上）。Personal Superintelligence Index 有一份二手表格：Wonder Full 59.1、Wonder 56、Opus 5.5 53、Astra 53、Fable 5.1 52，与 Meta 原文的一致性未能核对（`二手`，[OrcaRouter](https://www.orcarouter.ai/blog/meta-muse-wonder)）。
- **SWE-Marathon**：模型卡自承“not a controlled common-harness comparison”（`OS`，[模型卡](https://research.meta.ai/static/muse-wonder-model-card)）。
- **训练目标**：公开材料只说训练它不在未经许可时分享隐私信息、拒绝协助有害行为（`OS`，[Muse Wonder 博文](https://research.meta.ai/blog/muse-wonder)）。check-in、坚持和记忆具体怎么训练（数据、奖励、环境）没有公开。「无出处，待核」
- **Muse Spark 1.3（2026-09-02）**：面向更长周期的工作，在一个长线程里协作处理多个 workflow，并加强了提示注入鲁棒性（`OS`，[Spark 1.3](https://research.meta.ai/blog/introducing-muse-spark-1-3)）。

### 1.7 反响与生态

- **规模**：Sensor Tower 数据（经美银引用）显示截至 9 月 19 日约 55.7 万 DAU（`二手`，[Benzinga](https://www.benzinga.com/node/61932012)）。任务给的 CNBC 链接写约 56 万 DAU（`二手`，[CNBC](https://www.cnbc.com/2026/09/27/meta-muse-ai-personal-agent.html)，未打开核对）。花旗估计到 10 月 6 日约 180 万 DAU（`二手`，[KuCoin](https://www.kucoin.com/blog/meta-stock-rises-muse-ai-launch)）。另有报道称周活超过 300 万、下载超过 500 万（`二手`，[TNW 转述 The Information](https://thenextweb.com/news/meta-muse-3-million-weekly-users-information)），截至 9 月 25 日累计下载超过 340 万（`二手`，[Digital Today](https://www.digitaltoday.co.kr/en/view/107555/meta-ai-agent-muse-tops-app-store-overtaking-chatgpt)）。各家口径不同。
- **价格**：大部分功能免费，另有订阅（`OS`，[Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)；[订阅帮助页](https://www.meta.com/help/subscriptions/1021145227643680/)，标题级）。
- **Amazon 屏蔽**：9 月 20 日起 Amazon 弹窗称 Muse 的访问违反 Conditions of Use，指 Meta 未事先告知、agent 不自我标识，并质疑 Muse 存储客户凭据；Meta 否认 Muse 能看到密码，并拒绝把 Amazon 从 Muse 中移除（`二手`，[The Star](https://www.thestar.com.my/tech/tech-news/2026/09/22/amazon-blocks-metas-muse-ai-agent-from-its-retail-site)、[Adweek](https://www.adweek.com/commerce/amazon-locks-out-metas-muse-in-agentic-shopping-standoff/)、[Implicator](https://www.implicator.ai/amazon-blocks-meta-muse-shopping-agent/)）。
- **隐私争议**：有报道称 Muse 在未被要求时读取了作者的私信，还曾把用户住址透露给陌生人；Meta 称正在调查（`二手`，[TechRadar](https://techradar.com/ai-platforms-assistants/meta-muse-read-a-writers-private-messages-without-permission-and-its-exactly-why-im-not-ready-to-hand-my-life-over-to-ai-agents)、[Atlanta News First](https://www.atlantanewsfirst.com/2026/10/09/metas-new-muse-ai-agent-raises-privacy-concerns/)）。`推论`：这与 Mac 端“Read only”档允许读取 iMessage 的设计直接相关（[Mac 帮助页](https://www.meta.com/help/artificial-intelligence/1126304576638594/)），读权限默认不触发审批。
- **可靠性**：单一来源称内部测试中 agent 约 15 分钟后反复停滞、无法恢复（`二手`，[KuCoin 快讯](https://www.kucoin.com/news/flash/meta-s-muse-ai-agent-hits-2-8m-downloads-faces-privacy-and-security-challenges)）。实测评测见 eesel（`二手`，[eesel](https://www.eesel.ai/blog/meta-muse-agent-review)）。CNN 与 Yahoo 的实测文章本次未取到正文（`二手`，[CNN](https://www.cnn.com/2026/09/23/tech/meta-muse-ai-agent)、[Yahoo](https://finance.yahoo.com/technology/article/metas-muse-is-an-impressively-capable-ai-agent-despite-some-hiccups-173310662.html)，待核）。
- **Small Business**：在 Muse 内新增一组面向经营的 skills 和 connectors（`OS`，[Muse for Small Business](https://about.fb.com/news/2026/09/introducing-muse-small-business/)）。
- **新设备**：Muse 将进入 AI 眼镜（`OS`，标题级，[Your Personal Agent Coming to AI Glasses](https://www.meta.com/blog/muse-personal-agent-ai-glasses/)；[Connect 2026](https://about.fb.com/news/2026/09/the-biggest-news-from-connect-2026/)）。另有钥匙扣大小的语音设备 Muse Charm，据称 12 月推出（`二手`，搜索摘要，[Muse Charm 页](https://meta.com/muse-charm/)）。

---

## 2. nanoMuse 对 Muse 的重建

### 2.1 论文与仓库的关系

- 论文《nanoMuse: An Open-Source Personal Agent for Every Device You Own》（Guangyi Liu、Yong Liu、Jiangning Zhang，浙江大学）于 2026-10-07 上 arXiv（`GH`，[README](https://github.com/nano-muse/nanoMuse/blob/2ab584c/README.md)；[arXiv 2610.08699](https://arxiv.org/abs/2610.08699)）。
- 摘要转述：用“五个问题、三个时间尺度”定义个人 agent，梳理从 2011 年助手到 2026 年 agent 的谱系；根据公开记录和一份生产 prompt 副本重建 Muse，并给每条陈述标注来源；论文是设计分析，不是实验研究（`二手`，[hyper.ai](https://hyper.ai/en/papers/2610.08699)）。**五个问题和三个尺度的具体内容未取到**：arXiv 无法直连，仓库里也没有论文源文件（`GH`，在仓库中检索 `five questions` / `three time` 无相关命中，[repo](https://github.com/nano-muse/nanoMuse/tree/2ab584c)）。
- **生产 prompt 不在仓库里，属刻意为之。** AGENTS.md 规定“Muse's system prompt … anything decompiled or intercepted from the Muse app”不入库（`GH`，[AGENTS.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/AGENTS.md)）。因此本笔记**无法**总结 Muse 生产 prompt 的结构，只能总结 nanoMuse 自己的 prompt（§2.3）。
- 代码谱系：Android 端基于 OpenMinis 1.13（GPL-3.0；Alpine Linux 跑在 proot 下，带 shell、浏览器和 MCP）；桌面端是 DeepSeek Harness 加 `dsh-nanomuse` 插件；另有 Python runtime（web 与桌面的 hands）和 relay（`GH`，[README](https://github.com/nano-muse/nanoMuse/blob/2ab584c/README.md)、[roadmap.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/roadmap.md)）。

### 2.2 它“照 Muse 做”的东西（即 nanoMuse 对 Muse 的外部观察；都是 nanoMuse 的说法，不是 Meta 原文）

- **系统文件**：SOUL.md（人格）、USER.md（关于用户的工作笔记）、MEMORY（GLOBAL.md，持久笔记加按日日记）、feed-preferences.md，以及 HEARTBEAT.md（由 routines 渲染出的只读视图）。注释写明“listed the way Muse lists its system files”（`GH`，[SystemFiles.kt](https://github.com/nano-muse/nanoMuse/blob/2ab584c/android/src/android/app/src/main/java/io/github/nanomuse/sysfiles/SystemFiles.kt)；文件说明见 [strings.xml](https://github.com/nano-muse/nanoMuse/blob/2ab584c/android/src/android/app/src/main/res/values/strings.xml)）。其中 Identity / Soul / MEMORY.md 与 Meta 帮助页吻合（[personality & memories](https://www.meta.com/help/artificial-intelligence/995796179982326/)）。
- **房间布局**：一个主聊天加若干侧聊天；Feed / Ideas / Goals / Library 四个房间；Goals 用“Muse's six categories”（health、relationships、money、career、interests、productivity）；Connectors 按 Muse 的分类（Work、Talk、Files、Developer、Data、Design、Money、Search、Infrastructure）排列，并注明**未实现**“Muse's per-action permission dropdowns”；有“Muse's Import memory sheet”；头像固定四种姿态，分别对应 working、waiting、happy、error（`GH`，[CHANGELOG](https://github.com/nano-muse/nanoMuse/blob/2ab584c/CHANGELOG.md)、[desktop-muse.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/desktop-muse.md)）。每个 Connector 单独设权限这一点与 Meta 帮助页一致（[Connectors](https://www.meta.com/help/artificial-intelligence/1687253048996149/)）。
- **Sentinel 拆分**：agent 从不自己执行工具，一律交给 `Sentinel.guard()` 走 policy、approval、vault 解析、执行、结果脱敏，并做 taint 记账（`GH`，[sentinel.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/sentinel.md)、[architecture.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/architecture.md)）。
- **对 Muse 的定位判断**：nanoMuse 的对比表把 Muse 写成“每用户一台云 VM；没有 API 的 app 不可达；其他设备只是同一台 VM 的客户端”（`GH`，[README](https://github.com/nano-muse/nanoMuse/blob/2ab584c/README.md)）。Muse for Mac 的本地 app 访问和 computer use 与此矛盾（[Mac 帮助页](https://www.meta.com/help/artificial-intelligence/1126304576638594/)）。

### 2.3 nanoMuse 自己的实现（可作为“Muse 级个人 agent 的最小开源参照”）

- **Agent loop**：每轮组装一次 system prompt（profile、语言规则、相关记忆、活跃 goals），然后循环：调模型 → 经 Sentinel guard → 追加结果，直到 `terminate` 或模型不再调用工具；运行中到达的消息在下一次模型调用前并入；有卡死检测和 `max_steps` 上限（`GH`，[architecture.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/architecture.md)）。
- **System prompt 的结构**（nanoMuse 自己的版本）：Language、How you work、Artifacts、Context 四段，并按需追加 memory、goals、calendar、devices 等段。工作规则包括：先用工具做事，不要只描述；不可逆或对外可见的动作先确认；从不输入密码或验证码，登录 / CAPTCHA / 支付确认用 `hand_over` 交还用户；持久事实用 `remember`（事实变了用 `replaces=<id>`）；长期目标用 `goals`，计划改变时用 `propose`，不悄悄改；定时用 `reminders`，事件用 `triggers`；成功的流程可存为 `skills`（`GH`，[prompts.py](https://github.com/nano-muse/nanoMuse/blob/2ab584c/nanomuse/prompts.py)）。
- **记忆**：SQLite 存单行事实。检索用 IDF 加权的关键词 / CJK bigram 重叠，可选融合 embedding。tidy-up 每新增 8 行或每周触发一次（主动性设为 Off 时不触发）：合并重复，保留较新的事实，丢弃不是用户事实的一次性请求。模型只提方案，代码检查后执行（不引入新词、不删用户亲写、每轮至多删 1/5），所有改动都可撤销（`GH`，[consolidate.py](https://github.com/nano-muse/nanoMuse/blob/2ab584c/nanomuse/memory/consolidate.py)、[store.py](https://github.com/nano-muse/nanoMuse/blob/2ab584c/nanomuse/memory/store.py)、[app.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/app.md)）。
- **自认的记忆短板**：记忆不会在恰当时机自己浮现；遗忘对用户不可见；记忆按设备各存一份，不跨设备（`GH`，[roadmap.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/roadmap.md)）。
- **主动性档位**：Off / Low / Default / High，对应每 2× 间隔、每 1× 间隔、每 ½× 间隔跑一次 pass。每次 pass 挑一个有待办步骤的活跃 goal，在主聊天里以 Sentinel `auto` 模式执行（deny 规则、taint 和警告仍然生效，无人值守时变成 Feed 卡片）。无事可报的 pass 以 `[quiet]` 开头，只显示一行。支持 quiet hours（`GH`，[app.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/app.md)、[sentinel.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/sentinel.md)）。
- **触发器**：三种。`mail`（轮询 IMAP，按发件人或主题词匹配）、`event`（日历事件开始前 `lead_minutes`，上限 24 小时）、`hook`（`POST /api/hooks/<id>?key=`）。用邮件 UID、事件 uid 加开始时间、hook 投递 id 去重（`GH`，[triggers/store.py](https://github.com/nano-muse/nanoMuse/blob/2ab584c/nanomuse/triggers/store.py)）。路线图想加第四种“账号下某设备上线”，并让 agent 判断“注意到的事是否值得说一句”（`GH`，[roadmap.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/roadmap.md)）。
- **Goals 与 Feed**：创建 goal 时至多问 3 个问题，然后写出 `nanomuse-goal` 围栏块，按“每日 09:00”或“每 N 小时”排期检查。每次检查以 `nanomuse-goal-update` 围栏块收尾，状态为 on_track / attention / done。Feed 由每日 08:00 的 routine 在隐藏聊天里根据 feed 偏好、goals 和 profile 撰写（`GH`，[desktop-muse.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/desktop-muse.md)）。
- **Hands 的“四级阶梯”**：① skill / CLI / MCP → ② 带用户登录态的 fetch → ③ 应用内浏览器 → ④ 设备屏幕。第 4 级之前先说明；若不是用户要求的，先询问（`GH`，[gui.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/gui.md)）。动机是：Muse 在西方靠 API，而 12306、微信、支付宝、美团没有可调用的 API（`GH`，同上）。
- **手机 operator**：独立的视觉模型（默认 `qwen3.8-27b`），温度 0，使用 MemGUI 的 `mobile_use` 动作方言，坐标在 999 网格上。Android 的 AX tree 只作为第二输入。同一动作连续三次后在历史里加注提醒。点击的 `label` 含“确认支付 / 转账 / 发送 / 删除”等词时，升为最高档审批（`GH`，[gui.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/gui.md)、[sentinel.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/sentinel.md)）。
- **电脑 operator**：移植自 UI-TARS-desktop。以“图片为坐标单位”，按 28 像素网格对齐（Qwen3-VL 的 smart_resize）。Mac 上由一个 Swift helper 持有 ScreenCaptureKit 和 Accessibility 授权。Linux 只支持 X11，Wayland 下明确拒绝（`GH`，[gui.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/gui.md)）。
- **多设备**：每台设备运行自己的 agent，各自向 relay 保持一条出站 WebSocket（`/v1/hub`）。动作包括 `shell`、`files`、`screen`、`notify` 和 `task`（委派给对方的 agent）。审批回到发起者的设备上回答。每台设备有 Remote control 开关。relay 只按账号路由帧，不看任务内容（`GH`，[hub.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/hub.md)、[every-device.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/every-device.md)）。对话文本经 relay 同步；文件和截图留在本地（`GH`，[README](https://github.com/nano-muse/nanoMuse/blob/2ab584c/README.md)）。
- **审批分档（产品层）**：“先做后告知”（装软件）、“先问且可记住”（删除和发送，可按聊天或按单个对象记住）、“支付每次都问”（只能记住单个 app 或站点，且要屏幕锁验证）（`GH`，[privacy.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/privacy.md)）。授权绑定在 grant key 上（工具加目标，如 `send_email:alice@…`）（`GH`，[sentinel.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/sentinel.md)）。
- **训练数据计划**：用户可以选择贡献 traces；计划用它们训练开放权重的小型 hands 模型，并配一个开放评测集（`GH`，[roadmap.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/roadmap.md)、[privacy.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/privacy.md)）。

### 2.4 其他开源复刻

- **CopilotKit/OpenMuse**（MIT，alpha）：持久化 Chromium 加可选 Linux 工作区，支持 “Take control” 接管同一浏览器会话；Activity 里的计划、审批、回执由 SQL lease 恢复中断的任务；Ideas 附来源证据；Goals & Tracking 对公开页面做周期检查（变化、价格阈值）；Gmail / Calendar 走 OAuth；自主结账和图形桌面列为未来工作（`GH`，[README](https://github.com/CopilotKit/OpenMuse/blob/1ac68f3/README.md)）。
- **OpenClaw**：文件即记忆，包括 USER.md（带日期和 active / superseded 元数据的指令式用户模型）、MEMORY.md（精选的持久事实）、`memory/YYYY-MM-DD.md`（每日笔记，供 `memory_search` / `memory_get` 索引）和 DREAMS.md。dreaming sweep 把每日笔记蒸馏进 MEMORY.md（`GH`，[memory.md](https://github.com/openclaw/openclaw/blob/main/docs/concepts/memory.md)）。Heartbeat 是主会话中的周期 agent turn，默认 30 分钟一次（`GH`，[heartbeat.md](https://github.com/openclaw/openclaw/blob/main/docs/gateway/heartbeat.md)）。HEARTBEAT.md 文件已在新版中退役（`GH`，[HEARTBEAT 模板](https://github.com/openclaw/openclaw/blob/main/docs/reference/templates/HEARTBEAT.md)）。

---

## 3. 其他各家

### 3.1 xAI：Grok Bot / Team Bots / Grok Build memory

- **运行时**：每个 Bot 跑在持久云电脑上，合上笔记本后照常工作（`OS`，[Grok Bot overview](https://docs.x.ai/grok-bot/overview)）。团队版中每个用户一台专用 Firecracker microVM，由该用户的所有 Bot 共享，带浏览器、文件系统和终端。另可在成员本机执行，默认逐条命令审批（`OS`，[security](https://docs.x.ai/grok-bot/security)、[teams](https://docs.x.ai/grok-bot/teams-and-enterprises)）。产品对象是 Bot roster，不是聊天历史（`OS`，[Designing Grok Bot](https://x.ai/news/designing-grok-bot)）。
- **记忆**：对话和学到的上下文按 Bot 隔离；共享文件、浏览器会话和直接交接可以在 Bot 之间传递上下文；记忆内容是稳定偏好、角色上下文和以往工作摘要（`OS`，[Grok Bot overview](https://docs.x.ai/grok-bot/overview)）。Team Bots 分为团队共享记忆和个人私有笔记，只有 owner 或 manager 能保存团队 skill（`OS`，[Team Bots](https://docs.x.ai/grok-bot/team-bots)）。
- **Grok Build memory（编码 agent，但给出了最完整的记忆参数）**：每轮结束后在后台捕获 observations；`topics/` 存精选笔记，`observations/_inbox/` 存新事实；`/dream` 做合并，Auto-Dream 门限为 `min_hours=24`、`min_sessions=5`；检索为 0.7 向量加 0.3 BM25，`min_score=0.7`，首轮注入阈值 0.9，30 天半衰期，MMR λ=0.7；`/flush` 写会话摘要（`GH`，[13-memory.md](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/13-memory.md)）。
- **主动性**：routines 可按时间表运行，或在支持时由事件触发；每个 Bot 最多 50 个，时间表间隔至少 5 分钟（`OS`，[skills & routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)）。changelog 提到的事件源有 Teams 消息、Linear issue、Sentry 告警和 PagerDuty 事件（`OS`，[changelog](https://x.ai/changelog/bot)）。
- **交接**：Auto Review 是独立审核模型，对风险动作给出 allow / 需审批 / deny；“Ask first”规则优先于 allow；无人值守时的审批约 10 分钟过期，过期即不执行；密码、2FA 和 CAPTCHA 通过 computer takeover 交给人；Auto Review 不审核记忆写入（`OS`，[approvals, security & privacy](https://docs.x.ai/grok-bot/approvals-security-and-privacy)）。
- **模型**：Grok 4.7 的 RL 任务混合“偏重需要数小时的问题”（`OS`，[Grok 4.7](https://x.ai/news/grok-4-7)）。Grok Bot 默认使用哪个模型「无出处，待核」。

### 3.2 Microsoft：Copilot Autopilot（原 Scout）

- **运行时**：Autopilot 在租户内拥有自己的 identity、memory、computer 和 workspace，跑在云上，用户不在时也继续工作（`OS`，[Copilot 博文](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)）。前身 Scout 于 2026-06 以桌面 app 形式发布，横跨云、桌面和 web，并“powered by OpenClaw open-source technology”（`OS`，[Scout 博文](https://www.microsoft.com/en-us/copilot/blog/2026/06/02/introducing-microsoft-scout-your-always-on-personal-agent/)）。Autopilot 是否保留 OpenClaw 架构「无出处，待核」。
- **操作与触发**：可以在 Teams、Outlook、聊天、频道和文档里被 @；会盯频道、跟进线程、跑周期性工作、几天后重新拾起项目。未见正式的触发器类型清单（`OS`，[Copilot 博文](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)）。
- **审批**：敏感动作可要求人工签核，只能访问已批准的资源（`OS`，[Scout 博文](https://www.microsoft.com/en-us/copilot/blog/2026/06/02/introducing-microsoft-scout-your-always-on-personal-agent/)）。
- **可用性**：9 月底进入私有预览（`OS`，[Copilot 博文](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)）。

### 3.3 OpenAI：dots

- **运行时**：由 GPT-6 Astra 驱动，在云端有自己的电脑和浏览器，用户可以随时打开查看（`OS`，[Introducing dots](https://openai.com/index/introducing-dots/)）。对受支持的网站可使用已存密码，且不暴露给模型（`OS`，[getting started](https://help.openai.com/en/articles/20001530-getting-started-with-your-dot)）。
- **主动性**：空闲时做“proactive research”，只能通过已连接 app 的只读工具：不能给他人发消息，不能经插件修改内容，不能操控浏览器或电脑（`OS`，[dots FAQ](https://help.openai.com/en/articles/20001529-dots-privacy-security-and-safety-faqs)）。
- **记忆**：以 ChatGPT memory 为起点，另记私有笔记。OpenAI 称不直接用 proactive research 结果或 dot 的自我笔记做训练（`OS`，[Introducing dots](https://openai.com/index/introducing-dots/)）。
- **Custom Rules**：允许 / 需审批 / 禁止三档，不能覆盖核心安全要求和 Autoreview，也不能放宽 proactive research 的限制。改密码之类始终交还用户（`OS`，[dots FAQ](https://help.openai.com/en/articles/20001529-dots-privacy-security-and-safety-faqs)）。
- **可用性**：Pro 与 Business Premium，2026-09-29 发布（`OS`，[ChatGPT release notes](https://help.openai.com/en/articles/6825453-chatgpt-release-notes)）。公开评测数字未见（`OS`，[Introducing dots](https://openai.com/index/introducing-dots/) 的搜索结果中无评测）。

### 3.4 Google：Gemini Spark 与 Private AI Compute 记忆

- **运行时**：跑在 Google Cloud 的专用虚拟机上，24/7；由 Antigravity harness 驱动，后来模型切到 Gemini 3.7 Flash（`OS`，[Gemini app 更新](https://blog.google/innovation-and-ai/products/gemini-app/next-evolution-gemini-app/)、[3.7 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/)）。Windows 桌面 app 中有可委派任务的工作区（`OS`，[Windows app](https://blog.google/innovation-and-ai/products/gemini-app/gemini-app-now-on-windows/)）。
- **操作**：原生连接 Gmail、Calendar、Drive、Docs、Sheets、Slides、YouTube、Maps，默认关闭；第三方经 MCP 接入；Chrome auto browse 可在获得许可后使用登录态和已存密码（`OS`，[Spark 页](https://gemini.google/overview/agent/spark/)、[Gemini app 更新](https://blog.google/innovation-and-ai/products/gemini-app/next-evolution-gemini-app/)）。
- **主动性**：支持定时触发和 Skills，可持续监视和行动（例如分析发票以预判家庭需求）；通过 Gemini Live 的语音可以设置持续数天到数周的任务（`OS`，[Gemini app 更新](https://blog.google/innovation-and-ai/products/gemini-app/next-evolution-gemini-app/)、[Live × Spark](https://blog.google/innovation-and-ai/products/gemini-app/productivity-features-gemini-live/)）。
- **审批**：花钱、发邮件等高风险动作前先询问（`OS`，[Spark 页](https://gemini.google/overview/agent/spark/)）。
- **记忆（PAC）**：Private AI Compute 新增跨设备的持久记忆层。记忆加密存放在云端，解密密钥留在用户设备上；设备通过端到端加密通道进入 enclave，在 enclave 内解密、更新、再加密；设备先验证服务端软件，并承诺公开透明日志和第三方审计（`OS`，[PAC memory](https://deepmind.google/blog/advancing-private-ai-compute-with-secure-server-side-memory/)）。PAC 是否已用于 Spark 的记忆「无出处，待核」。

---

## 4. 横向对比表

| 产品 | 运行位置 | 操作方式 | 记忆 | 主动性触发 | 审批 / 交接 | 模型 | 公开评测 |
|---|---|---|---|---|---|---|---|
| **Meta Muse** | 每用户一台云 Secure VM，Sentinel 同机隔离；另有 Mac app 本机访问（[Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)、[Mac](https://www.meta.com/help/artificial-intelligence/1126304576638594/)） | Connectors；只看 AX tree、不能执行 JS 的浏览器；Mac 上用 Automation 和 computer use；Link by Stripe 结账（[safety](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)） | Identity / Soul / MEMORY.md 可编辑，有 forget skill（[help](https://www.meta.com/help/artificial-intelligence/995796179982326/)） | Goals、定时任务（daily check-in 等）（[help](https://www.meta.com/help/artificial-intelligence/1484325780075655/)） | app 系统对话框；按 Connector 设权限；tainted egress 回退询问；接管时暂停（[safety](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)） | Muse Spark 系列，Wonder 即将接入（[Wonder](https://about.fb.com/news/2026/10/introducing-muse-wonder-models/)） | MemoryBench 85.6（内部）；FocusBench 未公开（[blog](https://research.meta.ai/blog/muse-wonder)） |
| **xAI Grok Bot** | 每用户一台 Firecracker microVM，由该用户所有 Bot 共享；可选本机执行（[security](https://docs.x.ai/grok-bot/security)） | 浏览器、终端、文件、插件 / MCP（[overview](https://docs.x.ai/grok-bot/overview)） | 按 Bot 隔离；Team 共享记忆加私有笔记；Grok Build 有 /dream（[Team Bots](https://docs.x.ai/grok-bot/team-bots)、[13-memory](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/13-memory.md)） | Routines：定时（≥5 分钟间隔）、事件（Teams / Linear / Sentry / PagerDuty）（[routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)） | Auto Review；computer takeover；无人值守审批约 10 分钟过期（[approvals](https://docs.x.ai/grok-bot/approvals-security-and-privacy)） | 「待核」（Grok 4.7 为最新：[Grok 4.7](https://x.ai/news/grok-4-7)） | Bot 本身无；Grok 4.7 有 Terminal-Bench 4.0 等（[Grok 4.7](https://x.ai/news/grok-4-7)） |
| **MS Copilot Autopilot** | 租户内云端，自有 Entra identity 和 computer（[blog](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)） | M365（Teams / Outlook / 文档），被 @ 调用；Scout 时期还能操作 shell 和浏览器（[Scout](https://www.microsoft.com/en-us/copilot/blog/2026/06/02/introducing-microsoft-scout-your-always-on-personal-agent/)） | “own memory”，细节未公开（[blog](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)） | 盯频道、跟进线程、周期工作，无正式触发器清单（[blog](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)） | 敏感动作需人工签核（[Scout](https://www.microsoft.com/en-us/copilot/blog/2026/06/02/introducing-microsoft-scout-your-always-on-personal-agent/)） | 「无出处，待核」 | 无（[blog](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)） |
| **OpenAI dots** | 云端自有电脑和浏览器，可打开查看（[dots](https://openai.com/index/introducing-dots/)） | 4000+ 个 app 插件、浏览器、已存密码（[help](https://help.openai.com/en/articles/20001530-getting-started-with-your-dot)） | 以 ChatGPT memory 为起点，另有私有笔记（[dots](https://openai.com/index/introducing-dots/)） | 空闲时做只读 proactive research（[FAQ](https://help.openai.com/en/articles/20001529-dots-privacy-security-and-safety-faqs)） | Custom Rules 三档；Autoreview；改密码交还用户（[FAQ](https://help.openai.com/en/articles/20001529-dots-privacy-security-and-safety-faqs)） | GPT-6 Astra（[dots](https://openai.com/index/introducing-dots/)） | 无（[dots](https://openai.com/index/introducing-dots/)） |
| **Google Gemini Spark** | Google Cloud 专用 VM 加 Windows 桌面入口（[blog](https://blog.google/innovation-and-ai/products/gemini-app/next-evolution-gemini-app/)） | Workspace 原生连接、MCP、Chrome auto browse（[Spark](https://gemini.google/overview/agent/spark/)） | 未公开；PAC 提供 enclave 加端侧密钥的跨设备记忆（[PAC](https://deepmind.google/blog/advancing-private-ai-compute-with-secure-server-side-memory/)） | 定时触发、Skills、持续监视（[blog](https://blog.google/innovation-and-ai/products/gemini-app/next-evolution-gemini-app/)） | 花钱或发邮件前询问（[Spark](https://gemini.google/overview/agent/spark/)） | Gemini 3.5 → 3.7 Flash，经 Antigravity harness（[3.7 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/)） | 无 |
| **nanoMuse（开源）** | 用户的每台设备各跑一个 agent，经 relay hub 互联（[hub](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/hub.md)） | 四级阶梯：skill / CLI / MCP → 登录态 fetch → 浏览器 → 手机 / 电脑屏幕（单独的 VLM）（[gui](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/gui.md)） | SOUL / USER / MEMORY 等 md 文件加 SQLite；tidy-up 有约束，可撤销；目前不跨设备（[roadmap](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/roadmap.md)） | 主动性档位 pass；mail / event / hook 触发器；每日 Feed；goal 检查（[triggers](https://github.com/nano-muse/nanoMuse/blob/2ab584c/nanomuse/triggers/store.py)） | 三档审批，授权按 grant key；`hand_over`；审批回到发起设备（[sentinel](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/sentinel.md)） | 任意模型；云端默认 deepseek-v4.1-flash，hands 用 qwen3.8-27b（[app.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/app.md)） | 无，hands 评测集列在路线图（[roadmap](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/roadmap.md)） |

---

## 5. 研究空白（均为 `推论`，附依据）

1. **记忆评测只测“问了能不能答”，不测“该主动用时用没用”。** MemoryBench 测长对话中的回忆和冲突更新（[Muse Wonder](https://research.meta.ai/blog/muse-wonder)）。nanoMuse 承认缺少“在恰当时机自行浮现”的记忆（[roadmap](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/roadmap.md)）。InMind 专测“隐式关联”盲点（坚果过敏与马卡龙食谱），说明“检索后再用”的接口会漏掉这类记忆（`GH`，[InMind](https://github.com/imlrz/InMind)）。**可做的问题**：把“主动应用记忆”和“错误应用记忆（过时或已被撤回的事实）”放进同一个评测。
2. **记忆整理（dream / tidy）缺少评测和训练信号。** 三套实现都把合并交给 LLM，再用启发式约束兜底（[Grok 13-memory](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/13-memory.md)、[OpenClaw memory](https://github.com/openclaw/openclaw/blob/main/docs/concepts/memory.md)、[nanoMuse consolidate.py](https://github.com/nano-muse/nanoMuse/blob/2ab584c/nanomuse/memory/consolidate.py)）。Muse 的“删除后仍记得”（[help](https://www.meta.com/help/artificial-intelligence/995796179982326/)）说明遗忘的完整性无法验证。**可做的问题**：对整理操作做保真度、遗忘完整性、溯源（nanoMuse 路线图里的“provenance on every line”）的基准测试，以及做成可验证奖励。
3. **主动性没有公开的“打扰质量”评测。** 各家触发机制都是定时加事件，“值不值得说”由模型判断（[nanoMuse app.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/app.md)、[dots FAQ](https://help.openai.com/en/articles/20001529-dots-privacy-security-and-safety-faqs)、[Grok routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)）。nanoMuse 明说无法衡量“是否在对的时刻发问”（[roadmap](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/roadmap.md)）。UniClawBench 用用户模拟器评测主动 agent，是一个起点（`GH`，[UniClawBench](https://github.com/HKU-MMLab/UniClawBench)）。**可做的问题**：带打扰成本的 precision / recall，以及 check-in 时机（Active Focus 中“重要动作前 check-in”的定义见 [Muse Wonder](https://research.meta.ai/blog/muse-wonder)）的训练信号。
4. **数周级任务。** FocusBench 是“多次交互”而非数周（[Muse Wonder](https://research.meta.ai/blog/muse-wonder)）。Spark 宣称支持数天到数周的任务（[Live × Spark](https://blog.google/innovation-and-ai/products/gemini-app/productivity-features-gemini-live/)），但没有评测。VibeLifeBench 用数周时间线、世界状态变化和后端原子检查来评测（`GH`，[VibeLifeBench](https://github.com/evolvent-ai/VibeLifeBench)）。PAST-Bench 测跨会话改进，包含 26 个任务族、204 个 episode，并做持久化开 / 关对照（`GH`，[PAST-Bench](https://github.com/Gen-Verse/PAST-Bench)）。**可做的问题**：在仿真时钟下评测 goal 计划修订（nanoMuse 的 `goals propose` 机制见 [prompts.py](https://github.com/nano-muse/nanoMuse/blob/2ab584c/nanomuse/prompts.py)）以及计划漂移。
5. **多设备 GUI 操作和跨设备委派。** 只有 nanoMuse 公开实现了“手机 agent 委派给电脑 agent，审批回传到发起设备”（[every-device.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/every-device.md)）。Muse 正在从云 VM 扩展到 Mac 本机（[Mac 帮助页](https://www.meta.com/help/artificial-intelligence/1126304576638594/)）。nanoMuse 自认 hands 在 grounding 和意外弹窗恢复上会失败，且没有评测集（[roadmap](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/roadmap.md)）。**可做的问题**：跨设备任务的评测（同一任务一半在手机、一半在电脑），以及受限观测（Muse 只给 AX tree、不能执行 JS，见 [safety](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)）下的 agent 训练。
6. **“一个人的数字生活”作为环境。** 训练和评测都需要一份连贯的个人数据：邮件、日历、消息、文件、账号、手机 app 状态。MobileMem 用一年手机经历评测端侧记忆（`GH`，[MobileMem](https://github.com/zjunlp/MobileMem)）。nanoMuse 的 demo 用模拟手机（MobileGym）做 harness（[roadmap](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/roadmap.md)）。**可做的问题**：合成的、可复现的“数字人”环境，要覆盖 connector 后端、本地 app 和网站，并带可审计的隐私标注，用来同时测记忆、主动性和“读私信是否越权”（对应 Muse 的私信争议，[TechRadar](https://techradar.com/ai-platforms-assistants/meta-muse-read-a-writers-private-messages-without-permission-and-its-exactly-why-im-not-ready-to-hand-my-life-over-to-ai-agents)）。
7. **读权限审批粒度与平台准入。** Muse 的 Read only 档、dots 的只读研究、Grok Auto Review 不审核记忆写入，都说明“读”和“写记忆”几乎不受审批（[Mac 帮助页](https://www.meta.com/help/artificial-intelligence/1126304576638594/)、[dots FAQ](https://help.openai.com/en/articles/20001529-dots-privacy-security-and-safety-faqs)、[Grok approvals](https://docs.x.ai/grok-bot/approvals-security-and-privacy)）。Amazon 屏蔽事件中的一个理由是 agent 不自我标识（[The Star](https://www.thestar.com.my/tech/tech-news/2026/09/22/amazon-blocks-metas-muse-ai-agent-from-its-retail-site)）。**可做的问题**：读取最小化的策略学习，以及 agent 身份声明协议的评测。

---

## 6. 待核与缺口

- nanoMuse 论文正文（五个问题、三个时间尺度、对 Muse 生产 prompt 的结构分析）未读到：arXiv 无法直连，仓库刻意不收 prompt（[AGENTS.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/AGENTS.md)、[arXiv](https://arxiv.org/abs/2610.08699)）。
- Muse 有无 feed、USER.md、HEARTBEAT.md、事件触发器，官方摘录均未提及。nanoMuse 声称照 Muse 实现，需要官方全文或 app 实测核对（[SystemFiles.kt](https://github.com/nano-muse/nanoMuse/blob/2ab584c/android/src/android/app/src/main/java/io/github/nanomuse/sysfiles/SystemFiles.kt)）。
- “Muse for Mac 的 computer use”出处只到搜索摘录，原文 URL 未定位（[Connect 汇总](https://www.meta.com/blog/meta-connect-2026-everything-we-announced/)）。
- Sentinel 的位置（同一 VM 内系统级隔离，还是 VM 外）在官方摘录与 nanoMuse 文档之间矛盾（[Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)、[nanoMuse sentinel.md](https://github.com/nano-muse/nanoMuse/blob/2ab584c/docs/sentinel.md)）。
- Muse 当前的默认模型、Grok Bot 的默认模型、Autopilot 的模型：都未找到出处。「无出处，待核」
- FocusBench 分数，以及 Personal Superintelligence Index 二手表格与 Meta 原文的一致性，未核（[OrcaRouter](https://www.orcarouter.ai/blog/meta-muse-wonder)）。
- CNN、Yahoo、CNBC 原文未打开，DAU 数字只来自二手转述（[Benzinga](https://www.benzinga.com/node/61932012)）。
- Muse 是否上线 WhatsApp：仓库旧笔记写了，本次官方摘录只提到 iOS、Android 和 muse.ai（[Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)）。
- OpenClaw 文件引用的是 `main` 分支当前版本，不是 Muse 发布时的版本（[OpenClaw memory](https://github.com/openclaw/openclaw/blob/main/docs/concepts/memory.md)）。
