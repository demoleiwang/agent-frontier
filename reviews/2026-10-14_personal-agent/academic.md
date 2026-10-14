# 个人 agent 的学术与开源工作：环境、基准、记忆、主动性、个性化、长期任务（精读笔记，2026-10-14）

> 方法与来源说明：论文池为本仓库 `data/items/**/*.jsonl`，用关键词检索得到约 400 条命中（两轮检索去重后），人工筛出约 50 篇候选，精读 18 篇。arXiv abs 链接表示内容来自摘要（jsonl 的 excerpt）。GitHub blob 链接（带 commit）表示我读过对应仓库文件。仓库都以只读方式 只读 clone 到本地，没有执行任何代码。“二手”指搜索摘要或聚合站，“推论”指本笔记自己的判断，后面附依据链接。安全类论文只列名，不展开。数字一律是作者或厂商自报。

---

## 0. 一页结论

1. **个人 agent 环境已有一套共识配方：多服务 mock + 预置个人数据 + 脚本化时间线 + 读后端状态判分。** 代表作有 VibeLifeBench（22 个 MCP mock 服务，SQLite 种子，按 stage 回放 `event.yaml`，用 rubric 读后端状态）（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）和 Kimi K3 的个人助理环境（mock Gmail/Notion/Slack/Canvas，跨多个模拟日，每个事件一条判据）（[K3 §4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。MyPCBench 是同一思路的桌面 GUI 版：17 个模拟 web app，加 LibreOffice 和用户文件（[Qwen-CUA 附录 D.3](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
2. **“世界静默变化”在开源实现里，本质是“改库但不叫醒 agent”。** VibeLifeBench 的 mutation 事件直接执行 SQL 或写工作区，不进入 agent 的对话（[task.py L471-L492](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py#L471-L492)）。agent 只在 `user_message`、`notification`、`world`、`cron_fire` 这几类脚本事件上被唤醒。所以它测的是“下次被叫醒时会不会去复查”，**测不到“自己决定何时醒来”**（推论，依据同一文件，以及 [cron_fire 事件](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/litigation/food_safety_dispute_33d/event.yaml#L124-L131)）。
3. **造一个人的数字生活，主流做法是“结构化人设 → 年度事件图 → 按 app 落地成记录或截图 → 从事件图反推问题”。** MobileMem/KEME 的人设有 17 个维度，字段可随时间追踪变化；先把人设扩展成分层时间事件图，再把预合成的 app 会话挂到事件上（[text/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/text/README.md)）。多模态版用 HTML 模板渲染支付、票务、聊天等截图，并用换脸保持人物一致（[omni generation](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/src/generation/README.md)）。真人数据极少：MobileMem-Omni 只有 8 名招募参与者（[omni/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/README.md)）；PersonalAlign/Fingertip20k 是 83 名用户、2 万条手机意图记录（[ExpActivator samples](https://github.com/fyzhang1/ExpActivator/blob/3ef8ce5d923de56e56dc17eada833306dd92ea63/samples/user_profile.csv)）；Activity Frames 只有作者一人（n=1）（[RESULTS.md](https://github.com/nossa-y/activity-frames/blob/a2ce997ef45e9c865d632b8ac601080a758d29d8/research/RESULTS.md)）。
4. **记忆的主要瓶颈不在“存”，而在“什么时候想起来、想起来后用不用”。** InMind：记忆放进上下文时能答对 84.0%，走检索时最高只有 14.4%（[2607.24368](https://arxiv.org/abs/2607.24368)）。Know-vs-Act 研究：能回忆出偏好，却不在行为里体现（[2607.29433](https://arxiv.org/abs/2607.29433)）。ExpActivator：检索到的历史只对第一步有帮助（[2609.33304](https://arxiv.org/abs/2609.33304)）。反方向的失败同样普遍：12 个模型有 35%–49% 的用户画像论断属于捏造（[2608.04570](https://arxiv.org/abs/2608.04570)）。
5. **主动性评测正从“会不会主动”转向“该不该、什么时候、做多深”。** 依据：ProEvent 发现模型经常过度反应，GPT-5.1 只在 26.7% 的场景里反应正确（[2607.17701](https://arxiv.org/abs/2607.17701)）；Proactivity-Gym 发现即使结果正确，介入时机不对也会让信任骤降，用户更偏好“睡眠时间”辅助（[2609.37267](https://arxiv.org/abs/2609.37267)，细节为 [二手](https://hyper.ai/en/papers/2609.37267)）；Proactive Memory Agent 发现选择性介入优于始终注入（[2607.08716](https://arxiv.org/abs/2607.08716)）。
6. **判分在回避 LLM judge。** 有几种替代：读后端状态（[VibeLifeBench](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）、指向快照记录的指针标签（[SenWorld](https://arxiv.org/abs/2607.19949)）、从 need graph 直接判（[2609.37236](https://arxiv.org/abs/2609.37236)）、rule 占 85% 加 judge 占 15%（[PAST-Bench grader](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/src/past_bench/graders/self_evolve_helpers.py#L806-L807)）。用 LLM 做监督者的 UniClawBench 也把 hidden reference 与用户模拟器隔开（[docs/03_user.md](https://github.com/HKU-MMLab/UniClawBench/blob/a8ac4df6c554178c339f42696e3afe688a61f4b7/docs/03_user.md)）。另有 Proactivity-Gym 报告 LLM judge 会混淆能力与信任（[2609.37267](https://arxiv.org/abs/2609.37267)）。
7. **用户模拟器本身成了研究对象，影响不可忽略。** 只换用户代理（agent 固定为 GPT-5.5），任务分就变动 15.2 分；24.4% 的成功回合里用户违反了设定（[UserProxyBench 2609.38043](https://arxiv.org/abs/2609.38043)）。专门训练的 9B 模拟器拿来做 RL 环境，效果优于用 GPT-5.5 当用户（[MIMESIS 2610.09484](https://arxiv.org/abs/2610.09484)）。
8. **训练侧明显落后于评测侧。** 我见到的开源 RL 工作都在短程或代理环境上：Terminal-Bench、τ²-Bench、MuSiQue、UserRL gyms、推荐代理环境（[2607.08716](https://arxiv.org/abs/2607.08716)、[2609.37236](https://arxiv.org/abs/2609.37236)、[MIMESIS agent/](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/README.md)、[2610.07588](https://arxiv.org/abs/2610.07588)）。在多周个人生活环境里做 RL 的，我只看到工业界的 K3 自述（[K3 §4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）（推论，依据本笔记候选表里没有一篇摘要提到在此类环境训练）。

### 必读 Top-8（按“对构建环境与数据的参考价值”排序）

1. VibeLifeBench：多周时间线 + 22 个 mock 服务 + 静默 mutation + 后端状态 rubric，开源 100 个任务。[2608.10875](https://arxiv.org/abs/2608.10875) / [repo](https://github.com/evolvent-ai/VibeLifeBench)
2. MobileMem：人设到一年手机经历的完整合成管线，覆盖文本、多模态、结构化三条轨道。[2608.13606](https://arxiv.org/abs/2608.13606) / [repo](https://github.com/zjunlp/MobileMem)
3. MyPCBench（经 Qwen-CUA 报告）：在个性化桌面上用 17 个模拟 web app 做单人设一致的历史。[Qwen-CUA 附录 D.3](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf) / [arXiv 2606.16748](https://arxiv.org/abs/2606.16748)
4. PAST-Bench：用“持久化开/关”配对做跨会话自我改进的归因，并用机制上限（mechanism caps）防“碰巧对”。[2608.04003](https://arxiv.org/abs/2608.04003) / [repo](https://github.com/Gen-Verse/PAST-Bench)
5. SenWorld：基于真实地图、天气和节假日数据的确定性数字孪生，ground truth 由构造决定。[2607.19949](https://arxiv.org/abs/2607.19949)
6. Proactivity-Gym：主动性的 3T 框架、多日场景、人设化模拟用户和 30 人用户研究。[2609.37267](https://arxiv.org/abs/2609.37267)
7. InMind：记忆“隐性关联盲点”的配对对照设计。[2607.24368](https://arxiv.org/abs/2607.24368) / [repo](https://github.com/imlrz/InMind)
8. UserProxyBench 与 MIMESIS：用户模拟器的保真度评测与训练。[2609.38043](https://arxiv.org/abs/2609.38043) / [2610.09484](https://arxiv.org/abs/2610.09484)

---

## 1. 候选与筛选

### 筛选说明

检索词包括 personal agent/assistant、proactive、always-on、persistent、long-term memory、agent memory、personaliz、user simulat、lifelong、digital life、mobile/on-device、calendar、email、multi-day、living world、claw、wearable、digital twin 等，两轮检索共约 400 条命中，人工去掉视频、机器人、推荐 CTR 等不相关条目。相关度：**H** = 个人 agent 环境/基准/数据本身；**M** = 记忆、主动性、个性化或用户模拟的关键组件；**L** = 只列名（含安全类）。机构取自 jsonl，未标注时写“—”。

| id | 标题（简） | 机构 | 相关度 | 一句话 |
|---|---|---|---|---|
| [2608.10875](https://arxiv.org/abs/2608.10875) | VibeLifeBench | dots studio | H（精读） | 200 个多周生活任务，22 个 mock 服务，含静默世界变化 |
| [2609.37267](https://arxiv.org/abs/2609.37267) | Foundations of Proactive Agents / Proactivity-Gym | Minnesota NLP | H（精读） | 3T 原则，多日场景，人设模拟用户，30 人研究 |
| [2608.04003](https://arxiv.org/abs/2608.04003) | PAST-Bench | Princeton | H（精读） | 26 个场景、204 个 episode，测跨会话经验是否带来改进 |
| [2607.08768](https://arxiv.org/abs/2607.08768) | UniClawBench | HKU | H（精读） | 400 个双语真实任务，executor + 隐藏监督者 + 用户 agent 闭环 |
| [2608.13606](https://arxiv.org/abs/2608.13606) | MobileMem | OpenKG / OPPO | H（精读） | 一年手机经历合成，测端侧长期记忆 |
| [2607.19949](https://arxiv.org/abs/2607.19949) | SenWorld | — | H（精读） | 手机助理的数字孪生，用指针标签定 ground truth |
| [2606.16748](https://arxiv.org/abs/2606.16748) | MyPCBench（不在池中，经 Qwen-CUA） | CMU（[二手](https://arxiv.org/pdf/2606.16748)） | H（精读） | 个性化 Ubuntu 桌面，17 个模拟 web app，184 个任务 |
| [K3 报告](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf) | Kimi K3 个人助理“活”环境 | Moonshot | H（精读） | 多模拟日事件流，mock Gmail/Notion/Slack/Canvas |
| [2607.24368](https://arxiv.org/abs/2607.24368) | InMind | muset.ai | H（精读） | 记忆的隐性关联盲点，125 个任务 |
| [2608.04570](https://arxiv.org/abs/2608.04570) | Personalization Mirage | HKUST | H（精读） | 画像过度推断，比例 35–49% |
| [2609.33304](https://arxiv.org/abs/2609.33304) | ExpActivator | NTU / Alibaba | H（精读） | 个人 GUI agent 的经验激活与主动建议 |
| [2608.05784](https://arxiv.org/abs/2608.05784) | Activity Frames | — | H（精读） | 被动屏幕采集 → 确定性活动帧记忆 |
| [2607.08716](https://arxiv.org/abs/2607.08716) | Proactive Memory Agent | Meta | M（精读） | 旁路记忆 agent 决定是否插入提醒 |
| [2609.37236](https://arxiv.org/abs/2609.37236) | Horizontal / Vertical proactivity | IBM | M（精读） | 主动追问“内容”，用 need graph 判分，Q&D 训练 |
| [2610.09484](https://arxiv.org/abs/2610.09484) | MIMESIS | Meta | M（精读） | 训练用户模拟器，再拿来当 RL 环境 |
| [2609.38043](https://arxiv.org/abs/2609.38043) | UserProxyBench | — | M（精读） | 评测用户模拟器的保真度 |
| [2610.07588](https://arxiv.org/abs/2610.07588) | MediateRec | Meta | M（精读） | 个人 agent 用跨平台历史改写平台推荐 |
| [2608.28476](https://arxiv.org/abs/2608.28476) | ContextPilot | Tencent | M（精读） | 用细粒度 RL 学上下文管理 |
| [2610.08699](https://arxiv.org/abs/2610.08699) | nanoMuse | ZJU | M（只作系统提及） | 开源个人 agent，覆盖多设备 |
| [2607.17701](https://arxiv.org/abs/2607.17701) | ProEvent | — | M（简卡） | 从 IM 聊天里维护用户日程的主动性基准 |
| [2608.23035](https://arxiv.org/abs/2608.23035) | MobilePA-Bench | Tongyi-MAI | M（简卡） | 有状态的手机工具沙箱，212 个工具 |
| [2607.27056](https://arxiv.org/abs/2607.27056) | Setoka | — | M（简卡） | 用心理测量管线合成异构个人数据 |
| [2608.19652](https://arxiv.org/abs/2608.19652) | StateMemBench / StateMem | — | M（简卡） | 记忆系统能否跟踪“当前状态” |
| [2607.29433](https://arxiv.org/abs/2607.29433) | Know It, Act on It | — | M（简卡） | 记得住 ≠ 用得上 |
| [2608.04095](https://arxiv.org/abs/2608.04095) | FinPerMA | — | M（简卡） | 事件驱动的个性化记忆，276 个人设 |
| [2608.02171](https://arxiv.org/abs/2608.02171) | IBA-Bench | — | M | 从纵向交互历史中推断隐性约束 |
| [2607.05363](https://arxiv.org/abs/2607.05363) | SovereignPA-Bench | — | M | 用户主权：同意、隐私、平台中介 |
| [2607.12893](https://arxiv.org/abs/2607.12893) | MemOps | — | M | 记忆生命周期操作的轨迹级评测 |
| [2608.28378](https://arxiv.org/abs/2608.28378) | PersonaForge | — | M | 用 1.6 万真实会话校准多轮用户模拟 |
| [2609.08592](https://arxiv.org/abs/2609.08592) | Three-Tier Persona Vector | — | M | 23 维人设向量控制用户模拟 |
| [2610.13617](https://arxiv.org/abs/2610.13617) | User Simulators with Latent Intrinsic Feedback | — | M | 模拟器内部评分充当 RL 奖励 |
| [2609.00982](https://arxiv.org/abs/2609.00982) | Disclosure-Gated User Simulation | — | M | 解决模拟用户过度配合的问题 |
| [2608.09420](https://arxiv.org/abs/2608.09420) | UserIDA | Beihang | M | 逐轮显式意图控制用户模拟 |
| [2608.17150](https://arxiv.org/abs/2608.17150) | KnowSim | — | M | 模拟器带随学习演化的知识状态 |
| [2607.12625](https://arxiv.org/abs/2607.12625) | KnowAct-GUIClaw | Lychee | M | 跨平台 GUI 个人助理，带自进化记忆 |
| [2607.13027](https://arxiv.org/abs/2607.13027) | PalmClaw | ModalityDance | M | 原生运行在手机端的 agent 框架 |
| [2609.35671](https://arxiv.org/abs/2609.35671) | PhoneCLI | — | M | 把 app GUI 导航编译成命令 |
| [2607.11487](https://arxiv.org/abs/2607.11487) | LightMem-Ego | ZJUNLP | M | 眼镜和手机上的第一人称生活记忆 |
| [2609.37559](https://arxiv.org/abs/2609.37559) | APM-Bench | SJTU | M | 跨会话的第一人称视频持久记忆 |
| [2607.11523](https://arxiv.org/abs/2607.11523) | Vinci2 | UTokyo | M | 第一人称视频里何时主动介入 |
| [2609.07099](https://arxiv.org/abs/2609.07099) | EgoProactive challenge entry | Ambient | L | 介入/沉默的单 token 分类 |
| [2610.06505](https://arxiv.org/abs/2610.06505) | Proactive Hierarchical Procedural | SKKU | L | 引导粒度随进度调整 |
| [2609.03727](https://arxiv.org/abs/2609.03727) | Proactive Service Agents（综述） | — | M | 把主动服务表述为 POMDP，含指标体系 |
| [2608.30478](https://arxiv.org/abs/2608.30478) | Agents in the Large | Fudan | L | 持久 agent 的感知中心架构（框架文） |
| [2609.01852](https://arxiv.org/abs/2609.01852) | Memory Trust Gap | — | L | 过期记忆压过权威证据 |
| [2608.28833](https://arxiv.org/abs/2608.28833) | Hidden Costs of Personalization | UIUC | L | 无关个性化、回音室、谄媚 |
| [2609.05405](https://arxiv.org/abs/2609.05405) | WearableQA | Meta | L | 200 名真人、最长 500 天的可穿戴数据问答 |
| [2607.13940](https://arxiv.org/abs/2607.13940) | HealthClaw | — | L | 一年期合成健康管理基准 |
| [2610.12984](https://arxiv.org/abs/2610.12984) | Work2Skill | Nex AGI | L | 采集真人 GUI 经验做 skill |
| [2608.11434](https://arxiv.org/abs/2608.11434) | MobileJudgeBench | — | L | 移动端 LLM judge 的可靠性 |
| [2610.13886](https://arxiv.org/abs/2610.13886) | X-AgentRed（安全，只列名） | — | L | 多服务组合导致的伤害路径 |
| [2610.06454](https://arxiv.org/abs/2610.06454) | AgentPrivArena（安全，只列名） | — | L | 真实 agent 的隐私审计 |
| [2608.03700](https://arxiv.org/abs/2608.03700) | AntiSkillBench（安全，只列名） | — | L | persona skill 的隐私泄露与冒充 |
| [2609.01836](https://arxiv.org/abs/2609.01836) | Memory authorization laundering（安全，只列名） | EleutherAI | L | 记忆作为越权通道 |

---

## 2. 论文卡片

### 卡片 1｜VibeLifeBench：多周“活世界”中的生活 agent

- **来源**：[arXiv 2608.10875](https://arxiv.org/abs/2608.10875)；[repo @cd21b2c](https://github.com/evolvent-ai/VibeLifeBench/tree/cd21b2cb5d18a81b0fcdb4a948889a2148f48958)（2026-09-16）；机构 dots studio / Evolvent AI。
- **问题**：生活类任务一跑就是几周，期间世界会在无人提示时变化，约束常常不明说；agent 需要自己判断何时行动、何时询问、何时保持沉默（[摘要](https://arxiv.org/abs/2608.10875)）。
- **环境形态**
  - 22 个 mock 服务，每个服务一个目录，有独立 Dockerfile 和 SPEC，以 MCP 形式提供；开源的 20 个原生任务实际用到 21 个服务（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）。
  - 服务包括 calendar、email、notion、banking、credit_card、brokerage、flight/hotel/rail booking、maps、weather、ecommerce、legal_search、health_tracker、job_board、visa_and_advisory 等（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）。
  - 后端用纯 SQLite，冷启动时执行 `init.sql`；服务端“没有 admin 工具，也没有时钟”，按 stage 发生的行变更由编排器直接写进 `runtime.db`（[email_mock SPEC](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/servers/email_mock/SPEC.md)）。
  - Harbor 版每个任务一个 docker compose 栈，包含 world-controller、evidence-collector，以及共享的 `WORLD_CLOCK_FILE`（[compose](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/harbor/travel/galapagos_no_us_transit/environment/docker-compose.yaml)）。
  - 没有真机，完全离线，所有数据都是合成的（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）。
  - 被测 agent 固定为 OpenClaw 2026.7.1，运行在 Terrarium 中，两者都钉了版本（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）。
- **时间线与静默变化**
  - 每个任务 20–33 个 stage；stage 是检查点，不对应自然日；事件类型有 `user_message`、`mutation`、`notification`、`world`、`policy_update`（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）。
  - 例子：加拉帕戈斯任务有 25 个 stage、66 个事件，其中 24 个是 mutation，时间窗 2026-07-24 到 08-25（[task.md](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.md)）。
  - mutation 是 SQL 文件或工作区文件，例如“火山灰预警升级”就是往 weather 库插一条 alert（[S08 SQL](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/mutations/S08_weather_ash_advisory.sql)）。
  - 运行时对 mutation 只执行 apply，返回空文本，**不触发 agent 回合**；只有 user_message、notification、world、cron_fire 会调用 `agent.act`（[task.py L471-L492](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py#L471-L492)）。
  - 诉讼类任务用 `cron_fire` 模拟“定时提醒”，同样会唤醒 agent（[food_safety event.yaml](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/litigation/food_safety_dispute_33d/event.yaml#L124-L131)）。
  - 本笔记统计了 20 个原生任务：mutation 280 个，user_message 234 个，notification 205 个，world 154 个，cron_fire 4 个；其中 215 个 mutation 显式标了 `silent: true`。统计方法是解析各任务的 `event.yaml`（[eval_set](https://github.com/evolvent-ai/VibeLifeBench/tree/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set)）。
- **个人数据/人设**
  - 每个任务的 `workspace/` 里有 OpenClaw 风格的 `PERSONA.md`、`USER.md`、`SOUL.md`、`IDENTITY.md`、`HEARTBEAT.md`，以及预算、行程、风险登记等工作文件（[workspace](https://github.com/evolvent-ai/VibeLifeBench/tree/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/workspace)）。
  - 用户背景大量通过早期 user_message 一次性给出，例如“许闻容易晕船”“同伴费用不能报销”（[event.yaml](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/event.yaml)）。
  - 各服务的个人数据（邮件、日历、订单）是每个任务各自的 SQL 种子，全部经过 SQLite 完整性和外键检查，共 137 个环境绑定（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）。
  - 仓库没有数据生成脚本；Harbor 子集里有 `rental_seed_013_task` 之类的任务名，暗示存在基于种子的生成流程（推论，依据 [harbor/README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/harbor/README.md)）。
- **任务合成**：10 个领域（职业、考试、金融、健身、诉讼、装修、租房、购物、团建、出行），每个 Harbor 任务都附带每个 stage 的 oracle 参考轨迹（`solve.sh`、`oracle.py`）（[harbor/README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/harbor/README.md)）。
- **判分**
  - 采用 `flat_pool`：原子检查共用一个加权池；包括 `stage_<N>.py`、`cross_stage.py`、`final.py`、`tool_quality.py`（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）。
  - 加拉帕戈斯任务的权重固定为 stage 52 / cross 28 / tool 8 / final 12（[task.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py)）。
  - 检查通过 MCP 调用读取后端状态，例如“所有有效预订都不经美国机场”（[_backend_checks.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/rubrics/_backend_checks.py)）。
  - 但有相当一部分检查是对工作区文本做关键词组匹配，例如 stage 0 要求工作区出现“晕船/seasick”“授权/approval”（[_stage_checks.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/rubrics/_stage_checks.py)）。
  - 未授权的高影响动作会扣分，什么都问也会扣分（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）。
- **规模**：200 个任务，开源 100 个（Harbor 格式），其中 20 个另附原生格式；全量评测需发邮件申请（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）。
- **关键结果**
  - 摘要只说 7 个前沿模型“全部低分”（[摘要](https://arxiv.org/abs/2608.10875)）。
  - 二手：Claude Opus 5 avg@3 为 32.5、best-of-3 为 41.2；最弱的 DeepSeek-V4-Pro 为 21.1；所有模型从时间线开头到结尾掉 10–15 分（[主页](https://vibebench.github.io/VibeLifeBench_homepage/)、[HF](https://huggingface.co/papers/2608.10875)，均为二手，本次检索未能独立确认）。
- **局限**
  - agent 只在脚本事件上醒来，测不到自主调度（推论，依据 [task.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py#L471-L492)）。
  - 关键词检查可能被“写日志”刷分（推论，依据 [_stage_checks.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/rubrics/_stage_checks.py)）。
  - harness 只有 OpenClaw，单次全量评测要跑很多小时（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）。
  - 仓库没有 license 文件（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）。
- **可抄**：用 SQL mutation 文件加 `silent` 标志实现静默变化；用 world clock 文件统一各服务时间；每个 stage 附 oracle，可直接当 SFT 或 RL 的参考轨迹（推论，依据 [harbor/README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/harbor/README.md)）。

### 卡片 2｜Proactivity-Gym（Foundations of Proactive Agents）

- **来源**：[arXiv 2609.37267](https://arxiv.org/abs/2609.37267)，Minnesota NLP；另据二手信息有 KAIST 参与（[二手](https://hyper.ai/en/papers/2609.37267)）。无仓库。深度：仅摘要 + 二手。
- **问题**：主动 agent 能把闲置算力变成支持，但即使做对了，也可能误读用户情境、增加审阅成本、损害信任（[摘要](https://arxiv.org/abs/2609.37267)）。
- **框架**：3T，即 Task Capability、Temporal Allocation、Trust；设计空间有 5 维：task scope、anticipation horizon、activation trigger、processing timing、intervention depth；还需要用户与环境表示（[摘要](https://arxiv.org/abs/2609.37267)）。
- **环境形态**：基于模拟的测试床，包含多日场景、有状态环境和人设化的模拟用户，用来评估主动辅助在多次交互中的后果（[摘要](https://arxiv.org/abs/2609.37267)）。mock 服务数量、时间推进机制和人设合成方法「无出处，待核」。
- **判分**：评测了 23 种模型-harness 配置，发现 LLM judge 常把任务能力和信任混为一谈（[摘要](https://arxiv.org/abs/2609.37267)）。
- **关键结果**：30 人用户研究中，即使结果正确，介入时机不对也会让信任骤降（[摘要](https://arxiv.org/abs/2609.37267)）；用户偏好睡眠时间辅助，即使不完美，也是为了不打断手头的专注（[二手](https://hyper.ai/en/papers/2609.37267)）。
- **开源**：未见仓库（jsonl 中 `github_repo` 为空，见 [摘要页](https://arxiv.org/abs/2609.37267)）。
- **局限**：只有 30 名参与者；从摘要看不出模拟用户与真人的一致性（推论，依据 [摘要](https://arxiv.org/abs/2609.37267)）。

### 卡片 3｜PAST-Bench：个人 agent 能否从过往经验中改进

- **来源**：[arXiv 2608.04003](https://arxiv.org/abs/2608.04003)；[repo @f822351](https://github.com/Gen-Verse/PAST-Bench/tree/f8223517ae7491e776b69793d9f11e9d074ab42e)；Princeton。
- **问题**：保留下来的偏好、任务历史和技能，是否真的让 agent 越用越好（[摘要](https://arxiv.org/abs/2608.04003)）。
- **环境形态**
  - 18 个 mock 服务目录：calendar、contacts、crm、documents、finance、gmail、helpdesk、inventory、kb、notes、ocr、scheduler、slack、todo、web、x 等。每个任务按 YAML 声明要启动的服务、端口、reset 端点和 fixtures（[mock_services](https://github.com/Gen-Verse/PAST-Bench/tree/f8223517ae7491e776b69793d9f11e9d074ab42e/mock_services)、[task.yaml 例](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/self-evolve-tasks-v2/memory_ability/SM01_preference_adoption/eval_near_apply_saved_style/task.yaml)）。
  - 沙箱是 Docker（[README](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/README.md)）。
- **时间线**：不推进世界时钟，而是排一串有序的“新会话”episode：cold → learn_a → learn_b → eval_near → eval_far → 控制组。控制组包括 shortcut-visible、no-persistence 等，并在 learn 之后保存 history anchor 供分支（[family.yaml](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/self-evolve-tasks-v2/memory_ability/SM01_preference_adoption/family.yaml)）。
- **人设/数据**：没有完整人设，“个人性”体现在偏好（例如 TSV 格式、YYYY/MM/DD 日期）、约束、SOP 和例外清单上；场景大多是办公情境，如 helpdesk、oncall、发布决策（[README 家族列表](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/README.md)）。
- **任务合成**
  - 每个家族的 `family.yaml` 显式写出 trigger 的强度与可见路径、注入与移除计划、干扰信号、迁移距离等元数据（[family.yaml](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/self-evolve-tasks-v2/memory_ability/SM01_preference_adoption/family.yaml)）。
  - 四类能力：memory（5 个家族、41 个 episode）、procedural（8 / 64）、proactive information gathering（6 / 48）、update（7 / 51）（[README](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/README.md)）。
- **判分**
  - `expectations.json` 规定产物契约（记忆里必须出现的规则关键词）、检索契约（至少注入 1 次记忆）、必须和禁止的收件人等（[expectations.json](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/self-evolve-tasks-v2/memory_ability/SM01_preference_adoption/eval_near_apply_saved_style/expectations.json)）。
  - 最终得分 = 0.85×规则完成度 + 0.15×LLM judge，默认 judge 是 MiniMax-M2.7（[grader L806-L807](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/src/past_bench/graders/self_evolve_helpers.py#L806-L807)、[README](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/README.md)）。
  - **机制上限**：没检索就最多 0.25 分，检索太晚最多 0.35，没写入学习最多 0.45，用来区分“碰巧做对”和“走了预期路径”（[grader L646-L680](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/src/past_bench/graders/self_evolve_helpers.py#L646-L680)）。
  - 实验报告持久化开/关两种条件下的差值（`--compare-no-persistence`）（[README](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/README.md)）。
- **关键结果**：改进真实存在，但在不同能力间不均衡；表面增益相同的 agent，在是否走了预期路径上差别很大；Hermes+ 在“替换过时状态”类任务上提升最明显（[摘要](https://arxiv.org/abs/2608.04003)）。具体数字「无出处，待核」。
- **规模**：摘要称覆盖 7 个基座模型和 4 个框架（[摘要](https://arxiv.org/abs/2608.04003)）；仓库 `configs/agents.yaml` 里只列了 5 个模型 profile，即 MiniMax-M2.7、GLM-5.1、Kimi K2.6、DeepSeek-V4-Pro、GPT-5.4（[README](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/README.md)）。
- **局限**：没有真实时间推进和静默变化；场景偏办公（推论，依据 [家族列表](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/README.md)）。

### 卡片 4｜UniClawBench：真实容器、真实 app 与三角色闭环

- **来源**：[arXiv 2607.08768](https://arxiv.org/abs/2607.08768)；[repo @a8ac4df](https://github.com/HKU-MMLab/UniClawBench/tree/a8ac4df6c554178c339f42696e3afe688a61f4b7)；HKU。
- **问题**：已有基准依赖沙箱和单轮评测，按场景分类会把多种能力混在一起（[摘要](https://arxiv.org/abs/2607.08768)）。
- **环境形态**
  - 在活的 Docker 容器里跑，包含真实桌面 app，例如 Zotero、Obsidian、LibreOffice。setup service 负责安装和校验这些应用；任务明确要求“用真实桌面应用，不要用 web mock”（[task_105_01](https://github.com/HKU-MMLab/UniClawBench/blob/a8ac4df6c554178c339f42696e3afe688a61f4b7/tasks/105_cross_platform/task_105_01_rag_survey_gui_zotero_obsidian.yaml)）。
  - 约 4.1 GB 的 fixture 放在 HF 上，固定 revision 并带 SHA-256 校验（[README](https://github.com/HKU-MMLab/UniClawBench/blob/a8ac4df6c554178c339f42696e3afe688a61f4b7/README.md)）。
  - 没有时间线推进和静默变化（推论，依据 [任务 schema 文档](https://github.com/HKU-MMLab/UniClawBench/blob/a8ac4df6c554178c339f42696e3afe688a61f4b7/docs/TASK_SCHEMA.md)）。
- **人设/数据**：没有个人人设；输入是真实资料包，例如真实 RAG 综述 PDF（[task_105_01](https://github.com/HKU-MMLab/UniClawBench/blob/a8ac4df6c554178c339f42696e3afe688a61f4b7/tasks/105_cross_platform/task_105_01_rag_survey_gui_zotero_obsidian.yaml)）。
- **任务合成**：按 5 种能力组织（Skill Usage、Exploration、Long Context、Multimodal、Cross Platform），每种 40 个英文任务和 40 个中文镜像，共 400 个（[README](https://github.com/HKU-MMLab/UniClawBench/blob/a8ac4df6c554178c339f42696e3afe688a61f4b7/README.md)）。
- **判分**
  - 隐藏的 answer supervisor（Codex）读私有 reference 和 `eval_rule.md`，给出 pass、continue 或 fail，外加分数（[README](https://github.com/HKU-MMLab/UniClawBench/blob/a8ac4df6c554178c339f42696e3afe688a61f4b7/README.md)）。
  - 规则示例：截图必须显示真实应用和最终状态才给分；setup 状态文件只能证明环境可用（[eval_rule.md](https://github.com/HKU-MMLab/UniClawBench/blob/a8ac4df6c554178c339f42696e3afe688a61f4b7/injection/105_cross_platform/task_105_01_rag_survey_gui_zotero_obsidian/references/eval_rule.md)）。
  - 公开的用户模拟器只能看到可见轨迹，以及 verdict、attempt_state、recoverable、score 四个字段，看不到 reference 和 rationale（[docs/03_user.md](https://github.com/HKU-MMLab/UniClawBench/blob/a8ac4df6c554178c339f42696e3afe688a61f4b7/docs/03_user.md)）。
- **关键结果**：agent 在长程记忆和跨平台协调上吃力；框架架构常常限制模型本身的能力；性能随交互轮次提升（[二手](https://www.emergentmind.com/papers/2607.08768)）。二手：Claude Opus 4.8 通过 47.5%，GPT-5.4 为 40.7%（[agentmarketcap 博客，二手](https://agentmarketcap.ai/blog/2026/07/16/uniclawbench-proactive-agent-benchmark)）。
- **局限**：这里的“proactive”指自主完成任务，不是主动发起，与生活助理语境里的主动性不同（推论，依据 [task_105_01](https://github.com/HKU-MMLab/UniClawBench/blob/a8ac4df6c554178c339f42696e3afe688a61f4b7/tasks/105_cross_platform/task_105_01_rag_survey_gui_zotero_obsidian.yaml)）。另外，判分依赖 LLM supervisor（[README](https://github.com/HKU-MMLab/UniClawBench/blob/a8ac4df6c554178c339f42696e3afe688a61f4b7/README.md)）。

### 卡片 5｜MyPCBench：个性化桌面（经 Qwen-CUA 报告与二手）

- **来源**：[Qwen-CUA 报告](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf) §5 与附录 D.3（本笔记读过 PDF 全文）；MyPCBench 原文 [arXiv 2606.16748](https://arxiv.org/abs/2606.16748)，作者 Jang、Jang、Koh、Salakhutdinov（[Qwen-CUA 参考文献](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。原文不在论文池中。
- **环境形态**：Ubuntu 桌面，装有 17 个模拟真实 web 应用、LibreOffice、用户文件和连贯的跨应用历史；每个任务从 benchmark 快照启动（[附录 D.3](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
- **人设/数据**：所有数据围绕一个固定人设填充，即《办公室》里的 Michael Scott（[二手](https://arxiv.org/pdf/2606.16748)，经搜索摘要）。
- **任务合成**：184 个任务，每个都来自 OpenClaw 社区的真实请求（[二手](https://arxiv.org/pdf/2606.16748)，经搜索摘要）；任务切片包括 Aggregation、Contradiction、Counterfactual、Preference inference、Retrieval、Situated action、Long horizon 等（[附录 D.3 表 7](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
- **判分**：rubric 分（加权满足比例，计部分完成）和完美率（全部 rubric 都通过）两个指标（[附录 D.3](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
- **关键结果**
  - rubric 分 / 完美率：Qwen-CUA 84.3 / 58.7，Opus-4.8 88.8 / 62.0，GPT-5.5 79.8 / 47.3（[表 7](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
  - Counterfactual 切片所有模型的完美率都 ≤22%，Opus-4.8 为 0（[表 7](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
  - 加上 Bash 后轨迹变短，但 Qwen 模型的完美率反而下降：Qwen-CUA 从 58.7 降到 55.1（[§5 图 8](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
  - 原文：Claude Opus 4.6 完全解决 55.4% 的任务；失败集中在跨多个应用和长轨迹的任务上（[二手](https://arxiv.org/pdf/2606.16748)）。
- **局限**：只有一个人设，多人设之间的泛化测不到（推论，依据上面的 [二手](https://arxiv.org/pdf/2606.16748)）。

### 卡片 6｜Kimi K3：个人助理“活”环境（训练用，闭源）

- **来源**：[K3 技术报告 §4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)（本笔记读过原文）；另见本仓库 [labs.md 卡片 7](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)。
- **环境形态**：mock 版 Gmail、Notion、Slack、Canvas，“保留真实对应物的核心语义”，无外部 API、无限流（[§4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
- **时间线**：agent 在持久、不断演化的环境里跨多个模拟日工作，会遇到分布在多个 app 上的数十个相互依赖事件；RL 框架因此扩展为支持事件流及其引起的 world-state 转移（[§4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
- **人设/数据**：初始工作区由 agent 自主上网搜参考资料，再加工成连贯的环境（[§4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
- **任务**：参照 HR、法务、金融等真实职业工作流设计（[§4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
- **判分**：每个事件一条判据，由确定性规则或 LLM 评估（[§4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
- **规模**：单个 rollout 可达数千次工具调用、数百万 token（[§4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
- **局限**：环境和数据都不开源；“个人助理”实际偏职业工作流，而不是私人生活（推论，依据 [§4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。

### 卡片 7｜MobileMem：一年手机经历的合成（数据构造重点）

- **来源**：[arXiv 2608.13606](https://arxiv.org/abs/2608.13606)；[repo @fa5cd13](https://github.com/zjunlp/MobileMem/tree/fa5cd13c9c659699df9caf650987ba2bea8ca085)；OPPO + OpenKG（[README 引用](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/README.md)）。
- **问题**：手机上的经历是异构、多模态、不断演化且高度私人的，已有记忆基准覆盖不到（[摘要](https://arxiv.org/abs/2608.13606)）。
- **环境形态**：静态数据集，没有可交互环境；分 text、omni、struct 三条轨道（[README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/README.md)）。struct 轨道给出 bill、calendar、document、note、todo、voice 六类 app 记录，再加图片、屏幕 HTML 和视频描述（[struct/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/struct/README.md)）。
- **个人数据如何合成（重点）**
  - **Text / KEME**
    - 人设是 pydantic 模型，有 17 个维度：BasicInfo、Personality、Career、Diet、Health、Restaurants、Sport、Pet、Shopping、Transportation、Car、LongTravel、Technology、Photography、Entertainment、Finance、SocialCircle（[_builtin_dimensions.py](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/text/keme/models/persona/_builtin_dimensions.py)）。
    - 字段类型是可追踪变化的 `TrackedStr`（[_base.py](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/text/keme/models/persona/_base.py)）。
    - 流水线：先把人设扩展成分层时间事件图，再把**预合成的用户-app 会话**挂到兼容的事件上（grounding），然后生成互补的人机对话，最后从叶子会话往上逐层合成 QA（[text/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/text/README.md)）。
    - 默认生成模型是 gpt-5.2；后处理用向量检索查重，再让 LLM 审核修订（[text/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/text/README.md)）。
  - **Omni**
    - 人设来源有两种：中文人设从 CSV 读取，外国人设由 LLM 新造（[generation/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/src/generation/README.md)）。
    - 生成顺序：生活状态 → 重要日期 → 社交图 → 年度事件 → 子事件（[generation/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/src/generation/README.md)）。
    - app 截图（书、音乐、视频、购物、票务、支付等）由 LLM 填内容，再用 HTML 模板渲染（[app_trace/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/src/generation/app_trace/README.md)）。
    - 事件照片用 InsightFace 做两阶段换脸，保证主角和社交联系人跨照片一致（[event_photo/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/src/generation/event_photo/README.md)）。
    - 用户为 8 名招募参与者 + 8 个 LLM 生成人设（[omni/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/README.md)）。
  - **Struct**：LLM 辅助生成，前后都有大量人工设计、清洗和审校；仓库里的 Skill 只是示例，“不是可复现的数据管线”（[struct/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/struct/README.md)）。
- **任务合成**：每个记忆点带 source（primary、secondary、interference、system）、importance、`is_update` 等字段；问题分 7 类：单跳、多跳、更新、时间、隐性偏好、拒答、视觉（[omni/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/README.md)）。
- **判分**：多选 + 开放题，开放题用 OpenAI 兼容的 judge（[struct/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/struct/README.md)）。
- **规模**：Omni 有 16 名用户、1,589 个事件、155,670 轮对话、19,060 张图、平均每用户 1.72M token、7,415 个问题（[omni/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/README.md)）。
- **关键结果**：排行榜只以图片形式给出（[omni/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/README.md)），具体数字「无出处，待核」。
- **局限**：只测问答，不测 agent 行动；用户数少（推论，依据 [omni/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/README.md)）。

### 卡片 8｜SenWorld：手机助理的确定性数字孪生

- **来源**：[arXiv 2607.19949](https://arxiv.org/abs/2607.19949)，无仓库。深度：仅摘要。
- **环境形态**：物理接地、确定性、事件溯源的模拟；世界由真实的地图、天气、节假日和网络数据构建；每个可观测信号都存进全系统快照（[摘要](https://arxiv.org/abs/2607.19949)）。
- **人设/数据**：人设在世界里“过完一整天”，不需要脚本化交互，人设之间自发形成完全互惠的对话子图和各不相同的行为模式（[摘要](https://arxiv.org/abs/2607.19949)）。
- **判分**：每个评测用例用一个指针指向已存在的记录，不靠事后标注，也不用 LLM judge（[摘要](https://arxiv.org/abs/2607.19949)）。
- **规模与结果**
  - 北京 16 个人设，投影出 717 个用例，在一款量产手机助理上暴露 78 个失败（[摘要](https://arxiv.org/abs/2607.19949)）。
  - 失败集中在通话和短信记录上，联系人、日程、闹钟从未出错（[摘要](https://arxiv.org/abs/2607.19949)）。
  - 与留出的真人基准相比，类别分布 JSD 为 0.070，通信节律 JSD <0.1，但生成的记录比真实记录短（[摘要](https://arxiv.org/abs/2607.19949)）。
- **局限**：只模拟一天；只测检索，不测行动（[摘要](https://arxiv.org/abs/2607.19949)）。

### 卡片 9｜InMind：记忆的隐性关联盲点

- **来源**：[arXiv 2607.24368](https://arxiv.org/abs/2607.24368)；[repo @5a2ab26](https://github.com/imlrz/InMind/tree/5a2ab2686d3d5b832575f0288d41ecc93eab358b)；muset.ai。
- **任务构造**
  - 每个任务 = 一条合成的个人事实 + 直接查询 + 语义上很远的间接查询 + 知识桥（例子：坚果过敏 → 马卡龙要用杏仁粉）（[README](https://github.com/imlrz/InMind/blob/5a2ab2686d3d5b832575f0288d41ecc93eab358b/README.md)）。
  - 125 个任务覆盖 10 个领域，其中健康 46 个（[README](https://github.com/imlrz/InMind/blob/5a2ab2686d3d5b832575f0288d41ecc93eab358b/README.md)）；113 个可追溯到公开来源（[摘要](https://arxiv.org/abs/2607.24368)）。
- **环境/时间线**：固定使用 LongMemEval-s 的背景轨迹，目标事实插在第 9 个背景会话末尾，后面再接 38 个完整会话（[README](https://github.com/imlrz/InMind/blob/5a2ab2686d3d5b832575f0288d41ecc93eab358b/README.md)）。
- **判分**：四项配对测量（naive recall、in-context control、target recall、application），用二元 LLM judge，prompt 已公开（[README](https://github.com/imlrz/InMind/blob/5a2ab2686d3d5b832575f0288d41ecc93eab358b/README.md)、[prompts](https://github.com/imlrz/InMind/tree/5a2ab2686d3d5b832575f0288d41ecc93eab358b/evaluation/prompts)）。
- **结果**
  - 记忆在上下文中时，backbone 能答对 84.0% 的间接查询；6 个向量、图、agentic 记忆系统走检索时最高只有 14.4%，而它们直接回忆同一事实的准确率可达 100%（[摘要](https://arxiv.org/abs/2607.24368)）。
  - 把 embedding 维度提高到 8 倍，差距基本不变；改成在查询到来前就让记忆可见，能恢复大部分差距（[摘要](https://arxiv.org/abs/2607.24368)）。
- **局限**：规模小，作者自己提醒小幅差异不宜过度解读；只针对英文；baseline adapter 还没发布（[README](https://github.com/imlrz/InMind/blob/5a2ab2686d3d5b832575f0288d41ecc93eab358b/README.md)）。

### 卡片 10｜The Personalization Mirage：画像捏造

- **来源**：[arXiv 2608.04570](https://arxiv.org/abs/2608.04570)，HKUST；无仓库。
- **数据**：MirageBench 含 150 个人设，在刻板、反刻板、中性三类之间平衡；6 个个性化任务，按“想象梯度”排列（[摘要](https://arxiv.org/abs/2608.04570)）。
- **判分**：独立 judge 做四分类忠实度判定，与盲评人工的一致性 κ=0.863（四类）、0.900（二类），基于 400 条 claim；共判了 143,616 条 claim（[摘要](https://arxiv.org/abs/2608.04570)）。
- **结果**
  - 12 个模型的过度推断率都在 35%–49%，平均 41.6%（[摘要](https://arxiv.org/abs/2608.04570)）。
  - “自我监控反转”：模型自评的过度推断与 judge 测得的值负相关，ρ=−0.60（作者标为探索性结论，CI 很宽）（[摘要](https://arxiv.org/abs/2608.04570)）。
  - 过度推断率随任务在 27%–59% 之间变化（[摘要](https://arxiv.org/abs/2608.04570)）。
- **对环境构建的意义**：人设化环境的判分应同时惩罚“没用上”和“编出来”（推论，依据本卡与 [InMind](https://arxiv.org/abs/2607.24368)）。

### 卡片 11｜ExpActivator（及其数据 PersonalAlign / Fingertip20k）

- **来源**：[arXiv 2609.33304](https://arxiv.org/abs/2609.33304)；[repo @3ef8ce5](https://github.com/fyzhang1/ExpActivator/tree/3ef8ce5d923de56e56dc17eada833306dd92ea63)；NTU + Alibaba。
- **数据（真实用户）**
  - `samples/total.csv` 共 20,000 行，字段为 user_id、time、scenario（学校、办公场所等）、app 包名、意图描述、意图类别（[total.csv](https://github.com/fyzhang1/ExpActivator/blob/3ef8ce5d923de56e56dc17eada833306dd92ea63/samples/total.csv)）。
  - `user_profile.csv` 有 83 名用户，字段含性别、年龄、职业、城市、家庭、手机品牌，用户以学生为主（[user_profile.csv](https://github.com/fyzhang1/ExpActivator/blob/3ef8ce5d923de56e56dc17eada833306dd92ea63/samples/user_profile.csv)）。
  - 历史截图需要另外从 PersonalAlign 下载 Fingertip20k（[README](https://github.com/fyzhang1/ExpActivator/blob/3ef8ce5d923de56e56dc17eada833306dd92ea63/README.md)）。
- **切分**：每个用户按时间顺序取前 80% 作记忆，并用测试防止与测试 episode 重叠（[README](https://github.com/fyzhang1/ExpActivator/blob/3ef8ce5d923de56e56dc17eada833306dd92ea63/README.md)）。
- **任务**：个性化执行有 775 个 episode、7,915 个动作；主动建议有 215 个正例状态和 100 个负例状态（[README](https://github.com/fyzhang1/ExpActivator/blob/3ef8ce5d923de56e56dc17eada833306dd92ea63/README.md)）。
- **发现**：检索到的历史大幅改善一个 episode 的第一步，但对剩下 90% 的步骤帮助很小；对“该不该给主动建议”的指导也很弱（[摘要](https://arxiv.org/abs/2609.33304)）。
- **方法**：无需训练。在 GUI backbone 的潜空间里匹配历史状态，取对应动作作参考；只有当时间和场景证据充分时才主动提出例行意图，否则弃权（[摘要](https://arxiv.org/abs/2609.33304)）。
- **局限**：判分是离线动作匹配，不是在线环境执行（推论，依据 [README](https://github.com/fyzhang1/ExpActivator/blob/3ef8ce5d923de56e56dc17eada833306dd92ea63/README.md)）。

### 卡片 12｜Activity Frames：被动屏幕采集 → 确定性记忆

- **来源**：[arXiv 2608.05784](https://arxiv.org/abs/2608.05784)；[repo @a2ce997](https://github.com/nossa-y/activity-frames/tree/a2ce997ef45e9c865d632b8ac601080a758d29d8)。
- **数据**：单一用户（作者本人，n=1），128,756 帧、232,898 个 UI 事件，时间为 2026-05-11 至 07-22（[RESULTS.md](https://github.com/nossa-y/activity-frames/blob/a2ce997ef45e9c865d632b8ac601080a758d29d8/research/RESULTS.md)）；摘要写的是 51 个活跃日（[摘要](https://arxiv.org/abs/2608.05784)）。
- **方法**：零模型、确定性的编译器，把采集流切成带类型的活动帧（应用、站点、时长、输入量、证据指针）；重复出现的例行操作可编译成可回放的步骤（[README](https://github.com/nossa-y/activity-frames/blob/a2ce997ef45e9c865d632b8ac601080a758d29d8/README.md)）。
- **结果**
  - 一天的数据压缩到原来的 1/86，耗时 68 ms；基于压缩块的问答准确率 98.4%，同样数据用 LLM 摘要只有 66–80%（[摘要](https://arxiv.org/abs/2608.05784)）。
  - Routine Overhead Ratio 在 60–343× 之间；可委托的重复率在样本内为 9.0%，样本外为 7.7%（[摘要](https://arxiv.org/abs/2608.05784)）。
- **对数据准备的意义**：被动采集的真实行为日志可以作为“个人历史”的真实来源，并带证据指针，可审计（推论，依据 [README](https://github.com/nossa-y/activity-frames/blob/a2ce997ef45e9c865d632b8ac601080a758d29d8/README.md)）。

### 卡片 13｜Proactive Memory Agent（Meta）

- **来源**：[arXiv 2607.08716](https://arxiv.org/abs/2607.08716)；[repo @89e5c0d](https://github.com/yifannnwu/proactive-memory-agent/tree/89e5c0d6aadfe531a1aee42fd290d48be89973dd)。
- **机制**：一个独立的记忆 agent 与未改动的 action agent 并行。它每 N 步更新一次记忆库（状态、知识、流程），然后输出 `<context_for_action>` 提醒或 `<no_intervention/>`（[README](https://github.com/yifannnwu/proactive-memory-agent/blob/89e5c0d6aadfe531a1aee42fd290d48be89973dd/README.md)）。
- **环境**：Terminal-Bench 2.0（Harbor）和 τ²-Bench，不是个人生活环境（[摘要](https://arxiv.org/abs/2607.08716)）。
- **结果**
  - pass@1 在 Terminal-Bench 上提升 8.3 pp，在 τ²-Bench 上提升 6.8 pp；选择性介入优于被动暴露、始终注入和通用检索（[摘要](https://arxiv.org/abs/2607.08716)）。
  - 在 SETA 上对 Qwen3.5-27B 做 SFT + GRPO 训练记忆策略，只部分迁移到 Terminal-Bench（[摘要](https://arxiv.org/abs/2607.08716)）。

### 卡片 14｜Horizontal / Vertical proactivity（IBM，ProactiveInquirer）

- **来源**：[arXiv 2609.37236](https://arxiv.org/abs/2609.37236)；[repo @3e2c079](https://github.com/dolev31/ProactiveInquirer/tree/3e2c0791a059fb96840468ab658eefc4123c9a8f)。
- **问题**：主动性的“内容”维度。水平主动性追当前上下文已经点名的未问信息；垂直主动性追只有新证据才揭示出来的需求（[摘要](https://arxiv.org/abs/2609.37236)）。
- **判分**：从 benchmark 自带的分解里恢复出 need graph，直接从对话记录判分，不用 judge；比较时控制提问数量（[README](https://github.com/dolev31/ProactiveInquirer/blob/3e2c0791a059fb96840468ab658eefc4123c9a8f/README.md)）。
- **训练**：Q&D 方法。从同一状态分叉出多个候选问题，偏好后续检索到更多所需证据的那个；流程是拒绝采样 SFT，再在同状态的样本对上做 DPO（[README](https://github.com/dolev31/ProactiveInquirer/blob/3e2c0791a059fb96840468ab658eefc4123c9a8f/README.md)）。
- **结果**：MuSiQue 上所需证据召回从 78% 提到 90%；不做额外训练直接迁移到 τ²-bench retail，任务成功率从 13% 提到 34%（[README](https://github.com/dolev31/ProactiveInquirer/blob/3e2c0791a059fb96840468ab658eefc4123c9a8f/README.md)）。

### 卡片 15｜MIMESIS：把用户模拟器训练成环境

- **来源**：[arXiv 2610.09484](https://arxiv.org/abs/2610.09484)；[repo @58034ff](https://github.com/VietHoang1512/mimesis/tree/58034ff9887cd67914e7acac2a73965fb7cb3782)；Meta。
- **模拟器数据**：在人类对话上训练，带显式推理监督，并归纳出 13 种真实行为模式（[摘要](https://arxiv.org/abs/2610.09484)）；训练分三段：角色反转 mid-training、ThoughtTrace 推理 SFT、多领域联合 RL（[README](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/README.md)）。
- **环境**：agent RL 用的是 UserRL 的 gym（Function、Telepathy、Intention、Turtle、Search、Persuasion、Travel 等）（[agent/README](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/README.md)、[data_preprocess](https://github.com/VietHoang1512/mimesis/tree/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/examples/data_preprocess)）。
- **CSD**：模拟器的私有思考作为特权信号，由 coach 写成提示，变成逐 token 的监督；部署时 agent 只看公开对话（[agent/README](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/README.md)）。
- **结果**
  - 9B 模拟器的 SOUL-Index 为 65.7，高于 Claude-Opus-5 的 64.9（[README](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/README.md)）。
  - 9 个未见过的评测用户上的平均分：用 GPT-5.5 当用户做 GRPO 为 26.10，换成 MIMESIS-9B 为 29.54，再加 CSD 为 31.09（[README](https://github.com/VietHoang1512/mimesis/blob/58034ff9887cd67914e7acac2a73965fb7cb3782/README.md)）。
- **局限**：环境都是短程对话 gym，没有个人数据和长时间线（推论，依据 [data_preprocess](https://github.com/VietHoang1512/mimesis/tree/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/examples/data_preprocess)）。

### 卡片 16｜UserProxyBench：用户模拟器的保真度

- **来源**：[arXiv 2609.38043](https://arxiv.org/abs/2609.38043)，无仓库。
- **方法**：在 τ-bench 家族上加一层评测，User Fidelity Score 按任务 rubric 检查模拟用户是否遵守了私有指令，打分与 agent 成败无关（[摘要](https://arxiv.org/abs/2609.38043)）。
- **结果**
  - agent 固定为 GPT-5.5，只换用户代理，375 个企业任务的平均奖励变动 15.2 分（[摘要](https://arxiv.org/abs/2609.38043)）。
  - 24.4% 的成功回合里用户违反了设定；最主要的问题是提前泄露信息，这会让 agent 平均少调用 1.06 次工具（[摘要](https://arxiv.org/abs/2609.38043)）。
  - 在 7 个代理上画出了成本-保真度前沿（[摘要](https://arxiv.org/abs/2609.38043)）。

### 卡片 17｜MediateRec（Meta）：个人 agent 介入平台推荐

- **来源**：[arXiv 2610.07588](https://arxiv.org/abs/2610.07588)，无仓库。
- **设定**：平台用本地信息排序，个人 agent 用经用户授权的跨平台历史调整排名，产出最终 top-K（[摘要](https://arxiv.org/abs/2610.07588)）。
- **环境**：可扩展的代理（proxy）跨平台环境，另有一次真实的跨平台测试，平台与 agent 之间设了受控的信息边界（[摘要](https://arxiv.org/abs/2610.07588)）。
- **训练**：PAMO，通过反事实地遮掉个人历史来估计个人介入的贡献，按排名重新分配 advantage，并设平台相对价值下限（[摘要](https://arxiv.org/abs/2610.07588)）。
- **意义**：这是少见的“个人 agent 作为跨平台中介”的 RL 设定（推论，依据 [摘要](https://arxiv.org/abs/2610.07588) 与 [SovereignPA-Bench](https://arxiv.org/abs/2607.05363)）。

### 卡片 18｜ContextPilot（Tencent）：上下文管理的 RL

- **来源**：[arXiv 2608.28476](https://arxiv.org/abs/2608.28476)；仓库 [Tencent/ContextPilot](https://github.com/Tencent/ContextPilot)（未读）。
- **方法**：工具集加入规划、长期记忆和软性上下文卸载；在 RL 中，根据上下文和熵的变化找出关键编辑决策并在那里分叉采样，对经过某个编辑动作的所有分支估计动作级 advantage（[摘要](https://arxiv.org/abs/2608.28476)）。
- **环境**：长上下文 QA 和深度搜索，不是个人环境（[摘要](https://arxiv.org/abs/2608.28476)）。

### 简卡（只读摘要）

- **ProEvent**：基于合成但真实感强的 IM 聊天（考虑多人互动、并发线程和噪声），测 agent 能否主动维护用户日程，评测响应时机、单步和多步正确性；agent 常常过度反应，也处理不好事件取消，GPT-5.1 只有 26.7% 正确（[2607.17701](https://arxiv.org/abs/2607.17701)）。
- **MobilePA-Bench**：可执行沙箱，维护活的 app 数据库；13 个领域、212 个手机工具；测子 agent 协作、记忆（用户画像、过往偏好）和 skill；在工具调用顺序严格、权限受限和运行时出错时性能骤降（[2608.23035](https://arxiv.org/abs/2608.23035)）。
- **Setoka**：基于心理测量学的管线合成 10 个用户的异构数据，理解分 4 层（语义记忆、情景记忆、行为模式、人格特质）；层次越高，各系统表现越差（[2607.27056](https://arxiv.org/abs/2607.27056)）。
- **StateMemBench**：234 个多会话场景，按答案反映当前状态还是被取代的旧状态来判分；StateMem 在 DeepSeek-V4-Flash 上把当前状态准确率从 0.205 提到 0.363（[2608.19652](https://arxiv.org/abs/2608.19652)）。
- **Know It, Act on It**：16 个系统、1,000 条偏好、3 档表达强度；能通过回忆测试却在行为测试中失败的情况很多，健康和治疗类偏好最弱（[2607.29433](https://arxiv.org/abs/2607.29433)）。
- **FinPerMA**：276 个人设、2,994 道题，用确定性的理论规则 + LLM 叙述生成冻结的纵向投资者轨迹；全上下文配置最高约 0.47；基于摘要的记忆会丢失偏好信号，简单检索反而胜过专用记忆系统（[2608.04095](https://arxiv.org/abs/2608.04095)）。
- **nanoMuse**（只作系统提及）：GPL-3.0 开源个人 agent，一个 agent 覆盖用户的所有设备；记忆是用户可读的文件，每个动作都经过 Sentinel；评测套件还在路线图上（[2610.08699](https://arxiv.org/abs/2610.08699)、[repo](https://github.com/nano-muse/nanoMuse)）。

---

## 3. 跨论文归纳

### 3.1 个人 agent 环境的构建配方

**A. 人设与个人数据合成（重点）**

| 配方 | 代表 | 怎么做 | 优点 / 风险 |
|---|---|---|---|
| 结构化人设 → 年度事件图 → 按 app 落地 | MobileMem KEME / Omni | 17 维可追踪人设 → 分层时间事件图 → 把预合成的 app 会话挂上去 → HTML 渲染截图、换脸照片（[text](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/text/README.md)、[omni gen](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/src/generation/README.md)） | 时间一致、跨模态；但 struct 轨道依赖大量人工（[struct](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/struct/README.md)） |
| 物理接地的确定性模拟 | SenWorld | 用真实地图、天气、节假日和网络数据，让人设“过一天”，ground truth 由构造决定（[2607.19949](https://arxiv.org/abs/2607.19949)） | 无需 judge，分布可与真人对齐；记录偏短 |
| 任务专用的 SQL 种子 + 工作区人设文件 | VibeLifeBench | 每个任务独立 `init.sql` + PERSONA/USER/SOUL.md + 首轮消息给出约束（[workspace](https://github.com/evolvent-ai/VibeLifeBench/tree/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/workspace)） | 可直接判后端状态；一任务一人设，人设之间不复用（推论，依据同一目录） |
| 单一固定人设 + 多 app 历史 | MyPCBench | 17 个模拟 web app 都围绕一个人设填充（[Qwen-CUA D.3](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)、[二手](https://arxiv.org/pdf/2606.16748)） | 跨应用一致；但人设泛化测不到 |
| agent 上网找资料 → 生成工作区 | Kimi K3 | 自主检索参考资料，加工成连贯环境（[K3 §4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)） | 内容真实、可规模化；不开源 |
| 心理测量 / 理论规则驱动 | Setoka、FinPerMA | 用心理测量或理论化的影响规则控制人格与事件冲击，LLM 只负责叙述（[2607.27056](https://arxiv.org/abs/2607.27056)、[2608.04095](https://arxiv.org/abs/2608.04095)） | 标签可控；行为真实度没有验证 |
| 真实用户日志 | Fingertip20k、Activity Frames、WearableQA | 83 名用户 2 万条意图（[csv](https://github.com/fyzhang1/ExpActivator/blob/3ef8ce5d923de56e56dc17eada833306dd92ea63/samples/user_profile.csv)）；n=1 屏幕采集（[RESULTS](https://github.com/nossa-y/activity-frames/blob/a2ce997ef45e9c865d632b8ac601080a758d29d8/research/RESULTS.md)）；200 名真人可穿戴数据（[2609.05405](https://arxiv.org/abs/2609.05405)） | 分布真实；规模小、隐私受限、难以做成可交互环境 |

**B. 多服务 mock**
- 开源个人环境都选“自研轻量 mock + SQLite/JSON fixture + reset 端点”：VibeLifeBench 有 22 个 MCP 服务（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)），PAST-Bench 有 18 个 HTTP mock（[mock_services](https://github.com/Gen-Verse/PAST-Bench/tree/f8223517ae7491e776b69793d9f11e9d074ab42e/mock_services)），MobilePA-Bench 有 212 个工具（[2608.23035](https://arxiv.org/abs/2608.23035)）。
- 工具表面往往沿用上游真实 MCP，例如 email_mock 照搬 `emails-mcp` 的接口，只把后端换成 SQLite（[SPEC](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/servers/email_mock/SPEC.md)）。
- 真实 app 路线：UniClawBench 在容器里装 Zotero、Obsidian 等真实桌面应用（[task](https://github.com/HKU-MMLab/UniClawBench/blob/a8ac4df6c554178c339f42696e3afe688a61f4b7/tasks/105_cross_platform/task_105_01_rag_survey_gui_zotero_obsidian.yaml)）。真机路线只出现在工业界，例如 Qwen-CUA 的 30 台 Mac mini（[附录 D.4](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）；学术个人基准里没有用真手机做可交互环境的（推论，依据第 1 节候选表）。

**C. 时间推进与静默变化**
- VibeLifeBench：按 stage 排序事件；mutation 直接改库，不唤醒 agent；用 notification、world、cron_fire 驱动 agent 回合；共享 world clock 文件（[task.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py#L471-L492)、[compose](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/harbor/travel/galapagos_no_us_transit/environment/docker-compose.yaml)）。
- K3：事件流引起 world-state 转移，跨多个模拟日（[§4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
- Qwen-CUA phase-state chaining：每个阶段的完成态序列化后作为下一阶段的起点（本仓库 [labs.md 依据](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
- PAST-Bench：不推进世界，只排有序的新会话（[family.yaml](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/self-evolve-tasks-v2/memory_ability/SM01_preference_adoption/family.yaml)）。
- 共同缺口：没有一个开源环境允许 agent 自己设定唤醒时间（cron 或 heartbeat 由 agent 写入），再按它自己的调度推进时钟（推论，依据 [VibeLife task.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py#L471-L492) 与 [K3 §4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。

**D. 用户模拟器**
- 三种用法：
  - 只在被问到时作答，用于测提问是否有价值（Qwen-CUA 沿用 OSWorld 2.0，见 [labs.md 依据](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）；
  - 从隐藏监督者那里拿到最少的反馈后追问（[UniClawBench](https://github.com/HKU-MMLab/UniClawBench/blob/a8ac4df6c554178c339f42696e3afe688a61f4b7/docs/03_user.md)）；
  - 人设化的模拟用户，跨多日交互（[Proactivity-Gym](https://arxiv.org/abs/2609.37267)）。
- 已知问题与对策：
  - 过度配合、提前泄露（[2609.38043](https://arxiv.org/abs/2609.38043)、[2609.00982](https://arxiv.org/abs/2609.00982)）；
  - 扁平人设导致对话同质化，对策是 23 维人设向量（[2609.08592](https://arxiv.org/abs/2609.08592)）；
  - 意图不可控，对策是逐轮意图指令（[2608.09420](https://arxiv.org/abs/2608.09420)）；
  - 训练专用模拟器（[2610.09484](https://arxiv.org/abs/2610.09484)），或让模拟器直接给奖励（[2610.13617](https://arxiv.org/abs/2610.13617)）。
- VibeLifeBench 不用交互式模拟用户，用户消息全部预先写好（[event.yaml](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/event.yaml)）。因此 agent 的提问不会得到回答，只能从后续事件里获得信息（推论，依据同一文件）。

**E. 判分**
- 后端状态与产物检查：VibeLifeBench（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)），Qwen-CUA 与 K3 也按终态打分（[K3 §4.2.6](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
- 构造即标签：SenWorld 的记录指针（[2607.19949](https://arxiv.org/abs/2607.19949)）、need graph（[2609.37236](https://arxiv.org/abs/2609.37236)）、StateMemBench 的闭集判分（[2608.19652](https://arxiv.org/abs/2608.19652)）。
- 机制归因：PAST-Bench 的检索和写入上限（[grader](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/src/past_bench/graders/self_evolve_helpers.py#L646-L680)）。
- LLM judge 仍用于开放产出：UniClawBench 的 Codex supervisor（[README](https://github.com/HKU-MMLab/UniClawBench/blob/a8ac4df6c554178c339f42696e3afe688a61f4b7/README.md)）、InMind 的二元 judge（[prompts](https://github.com/imlrz/InMind/tree/5a2ab2686d3d5b832575f0288d41ecc93eab358b/evaluation/prompts)）、MobileMem 开放题（[struct](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/struct/README.md)）。
- 主动性里的“信任”维度目前只能靠真人研究来测，LLM judge 会把它和任务能力混在一起（[2609.37267](https://arxiv.org/abs/2609.37267)）。

### 3.2 记忆：评测与训练现状

- **评测已从“能不能回忆”推进到“检索路由、应用、状态更新、画像忠实度”**：
  - 隐性关联（[InMind](https://arxiv.org/abs/2607.24368)）；
  - 知道 vs 行动（[2607.29433](https://arxiv.org/abs/2607.29433)、[IBA-Bench](https://arxiv.org/abs/2608.02171)）；
  - 状态跟踪（[StateMemBench](https://arxiv.org/abs/2608.19652)、[MemOps](https://arxiv.org/abs/2607.12893)）；
  - 画像捏造（[Mirage](https://arxiv.org/abs/2608.04570)）；
  - 层级理解（[Setoka](https://arxiv.org/abs/2607.27056)）；
  - 跨会话改进归因（[PAST-Bench](https://arxiv.org/abs/2608.04003)）；
  - 多模态和端侧场景（[MobileMem](https://arxiv.org/abs/2608.13606)、[APM-Bench](https://arxiv.org/abs/2609.37559)）。
- **训练**：
  - 记忆或上下文管理策略的 RL 在 Terminal-Bench、SETA、长上下文 QA 上做（[2607.08716](https://arxiv.org/abs/2607.08716)、[2608.28476](https://arxiv.org/abs/2608.28476)）；
  - 端侧蒸馏（[DuoMem 2606.29961](https://arxiv.org/abs/2606.29961)）；
  - 无训练的经验激活（[ExpActivator](https://arxiv.org/abs/2609.33304)）；
  - 用自生成任务引导记忆（[DAEDALUS 2610.08048](https://arxiv.org/abs/2610.08048)）。
  - 没有一项以“多周个人生活结果”为奖励（推论，依据 [2607.08716](https://arxiv.org/abs/2607.08716)、[2608.28476](https://arxiv.org/abs/2608.28476)、[2610.08048](https://arxiv.org/abs/2610.08048) 的摘要）。

### 3.3 主动性：评测与训练现状

- **评测维度**：
  - 是否介入与时机（[ProEvent](https://arxiv.org/abs/2607.17701)、[Vinci2](https://arxiv.org/abs/2607.11523)、[EgoProactive](https://arxiv.org/abs/2609.07099)）；
  - 介入后果与信任（[Proactivity-Gym](https://arxiv.org/abs/2609.37267)）；
  - 追问的内容（[2609.37236](https://arxiv.org/abs/2609.37236)）；
  - 复查静默变化（[VibeLifeBench](https://arxiv.org/abs/2608.10875)）；
  - 例行意图建议与弃权（[ExpActivator](https://arxiv.org/abs/2609.33304)）；
  - 统一的 POMDP 表述与指标体系（[2609.03727](https://arxiv.org/abs/2609.03727)）。
- **训练**：
  - 用 Q&D 从提问后果学习（[2609.37236](https://arxiv.org/abs/2609.37236)）；
  - 介入时机做成单 token 分类（[2609.07099](https://arxiv.org/abs/2609.07099)）；
  - 用对比轨迹做探索 RL（[2608.14339](https://arxiv.org/abs/2608.14339)）；
  - 选择性提醒的记忆策略 GRPO（[2607.08716](https://arxiv.org/abs/2607.08716)）。

### 3.4 一致的结论

- **“何时不做”比“会不会做”更难，也更关键**：ProEvent 发现过度反应（[2607.17701](https://arxiv.org/abs/2607.17701)）；Proactive Memory Agent 发现选择性介入优于始终注入（[2607.08716](https://arxiv.org/abs/2607.08716)）；ExpActivator 设计了弃权机制（[2609.33304](https://arxiv.org/abs/2609.33304)）；Proactivity-Gym 发现介入错位会损害信任（[2609.37267](https://arxiv.org/abs/2609.37267)）；VibeLifeBench 对什么都问的行为扣分（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）。
- **LLM 摘要式记忆会丢关键信号**：Activity Frames 中 LLM 摘要只有 66–80%，对比确定性压缩块的 98.4%（[2608.05784](https://arxiv.org/abs/2608.05784)）；FinPerMA 发现摘要记忆丢失偏好信号（[2608.04095](https://arxiv.org/abs/2608.04095)）。
- **时间越长越差**：VibeLifeBench 从开头到结尾掉 10–15 分（[二手](https://vibebench.github.io/VibeLifeBench_homepage/)）；MyPCBench 失败集中在长轨迹（[二手](https://arxiv.org/pdf/2606.16748)）；Setoka 中情景记忆和行为模式层表现下降（[2607.27056](https://arxiv.org/abs/2607.27056)）。
- **专用记忆系统不一定胜过简单基线**：FinPerMA 中简单检索更好（[2608.04095](https://arxiv.org/abs/2608.04095)）；StateMemBench 中长上下文基线有竞争力（[2608.19652](https://arxiv.org/abs/2608.19652)）；InMind 发现记忆进上下文后表现远好于检索（[2607.24368](https://arxiv.org/abs/2607.24368)）。
- **框架/harness 的影响与模型同量级**：UniClawBench 发现框架会限制模型能力（[二手](https://www.emergentmind.com/papers/2607.08768)）；PAST-Bench 中同一模型换框架，表现差别明显（[摘要](https://arxiv.org/abs/2608.04003)）；Proactivity-Gym 按模型-harness 配置分别报告（[摘要](https://arxiv.org/abs/2609.37267)）。

### 3.5 互相矛盾或存在张力的地方

- **个人信息“用得太少” vs “用得太多”**：InMind 和 Know/Act 显示该用的没用上（[2607.24368](https://arxiv.org/abs/2607.24368)、[2607.29433](https://arxiv.org/abs/2607.29433)）；Mirage 和 Hidden Costs 显示会捏造或滥用（[2608.04570](https://arxiv.org/abs/2608.04570)、[2608.28833](https://arxiv.org/abs/2608.28833)）。只优化其中一边的基准，会把模型推向另一种失败（推论，依据这两组结果）。
- **多问 vs 少问**：UniClawBench 发现性能随交互轮次提升（[二手](https://www.emergentmind.com/papers/2607.08768)）；Q&D 训练后提问更少、成功率更高（[README](https://github.com/dolev31/ProactiveInquirer/blob/3e2c0791a059fb96840468ab658eefc4123c9a8f/README.md)）；Disclosure-gated 指出，过度配合的模拟用户会让多问被不当奖励（[2609.00982](https://arxiv.org/abs/2609.00982)）。由此看，“多轮有益”的结论可能部分来自模拟用户太配合（推论，依据 [2609.38043](https://arxiv.org/abs/2609.38043)）。
- **检索是瓶颈 vs 检索是最优解**：InMind 认为检索路由是瓶颈（[2607.24368](https://arxiv.org/abs/2607.24368)）；FinPerMA 发现简单检索胜过专用系统（[2608.04095](https://arxiv.org/abs/2608.04095)）。两者测的分别是隐性关联和事件后偏好，并不直接冲突，但对“该加强检索还是该放弃检索”的指导方向相反（推论）。
- **模型排名不稳定**：MyPCBench 的 Preference inference 切片 GPT-5.5 的完美率是 73，高于 Opus-4.8 的 64；总分则 Opus-4.8 领先（[Qwen-CUA 表 7](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。

---

## 4. 与前沿产品的差距（整节为推论，产品宣称来自本仓库 frontier-labs 笔记，属官方页面的搜索摘要，深度为二手）

| 产品宣称的能力 | 产品出处 | 学术界能测 / 能练到哪 | 差距（推论） |
|---|---|---|---|
| 自有云 VM，app 关闭后继续工作，需要审批时才回来找人（Muse） | [Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)（二手） | VibeLife 测多周跨度，但 agent 只在脚本事件上醒来（[task.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py#L471-L492)） | 测不到自主调度、后台持续运行、“何时回来找人” |
| 不需要提示就能启动工作，靠 routines/automations（Grok Bot）；监视频道、跟进线程、执行周期性任务（Autopilot） | [Grok Bot](https://x.ai/news/designing-grok-bot)、[Autopilot](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)（二手） | ProEvent 从 IM 聊天维护日程（[2607.17701](https://arxiv.org/abs/2607.17701)）；VibeLife 的 cron_fire 由脚本写死（[event.yaml](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/litigation/food_safety_dispute_33d/event.yaml#L124-L131)） | 没有基准测 agent 自己建立 routine、自己设触发器的质量 |
| 空闲时用只读权限做“主动研究”（dots）；按天到按周运行的任务（Gemini Spark） | [dots](https://openai.com/index/introducing-dots)、[Spark](https://blog.google/innovation-and-ai/products/gemini-app/gemini-app-now-on-windows/)（二手） | Proactivity-Gym 的睡眠时间偏好只来自 30 人研究（[二手](https://hyper.ai/en/papers/2609.37267)） | 空闲时间产出的价值、审阅成本、信任，还没有规模化的环境化评测 |
| 4,000+ app 插件（dots）；Gmail/Drive 跨文件综合（Spark） | [dots](https://openai.com/index/introducing-dots)、[Spark](https://blog.google/innovation-and-ai/products/gemini-app/gemini-app-now-on-windows/)（二手） | 开源环境 18–22 个服务、212 个工具（[VibeLife](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)、[PAST](https://github.com/Gen-Verse/PAST-Bench/tree/f8223517ae7491e776b69793d9f11e9d074ab42e/mock_services)、[MobilePA](https://arxiv.org/abs/2608.23035)） | 长尾服务覆盖差两个数量级；mock 的接口语义漂移没有验证 |
| 敏感动作前确认；Custom Rules 规定可做、需审批、需交还用户的动作 | [Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)、[dots](https://openai.com/index/introducing-dots)（二手） | VibeLife 对未授权支付、下单、取消扣分（[README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/README.md)）；SovereignPA 测同意边界（[2607.05363](https://arxiv.org/abs/2607.05363)） | 规则是固定的；没有测“用户自定义规则”的遵守和泛化 |
| 跨周持久记忆；断开 app 后已学到的内容仍保留（dots） | [dots](https://openai.com/index/introducing-dots)（二手） | PAST-Bench、StateMemBench、InMind、MobileMem（见第 3.2 节） | 记忆测试多是 QA；“记忆 → 多周行动 → 结果”的端到端闭环只在 VibeLife 里隐含存在 |
| 多设备：手机、眼镜、桌面（Muse 上眼镜；nanoMuse 覆盖所有设备） | [Connect 2026](https://about.fb.com/news/2026/09/the-biggest-news-from-connect-2026/)（二手）、[nanoMuse](https://arxiv.org/abs/2610.08699) | 手机记忆（MobileMem）、眼镜记忆（APM-Bench）、桌面（MyPCBench）彼此分离 | 没有跨设备统一的个人环境 |
| 一个用户多个 Bot 共享一台 VM（Grok Bot） | [Grok Bot](https://x.ai/news/designing-grok-bot)（二手） | 未见 | 多 agent 共享个人状态时的协调与冲突，没有基准 |

---

## 5. 研究空白

1. **自主调度的长期环境**：现有开源实现由脚本决定何时唤醒 agent，agent 写的 cron 不会影响时钟推进（[VibeLife task.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/task.py#L471-L492)）。产品却把“无需提示就开始工作”作为核心卖点（[Grok Bot](https://x.ai/news/designing-grok-bot)，二手）。
2. **开源的多周个人 RL 环境与训练报告**：只有 K3 自述在多模拟日环境里做 RL（[§4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）；开源记忆和主动性 RL 都在短程代理任务上（[2607.08716](https://arxiv.org/abs/2607.08716)、[2609.37236](https://arxiv.org/abs/2609.37236)）。VibeLife 的 oracle 轨迹和 rubric 已经具备作为奖励的条件（推论，依据 [harbor/README](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/harbor/README.md)）。
3. **合成人设数据的真实度校验**：只有 SenWorld 用 JSD 与真人数据对齐（[2607.19949](https://arxiv.org/abs/2607.19949)）；MobileMem 的 struct 轨道依赖人工审校，且明说管线不可复现（[struct/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/struct/README.md)）。
4. **真实个人数据的规模**：真实来源只有 83 人（[Fingertip20k](https://github.com/fyzhang1/ExpActivator/blob/3ef8ce5d923de56e56dc17eada833306dd92ea63/samples/user_profile.csv)）、8 人（[MobileMem-Omni](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/README.md)）、1 人（[Activity Frames](https://github.com/nossa-y/activity-frames/blob/a2ce997ef45e9c865d632b8ac601080a758d29d8/research/RESULTS.md)）。缺少隐私保护下的规模化采集协议。
5. **长时间线上的用户模拟器保真度**：UserProxyBench 只在 τ-bench 上测（[2609.38043](https://arxiv.org/abs/2609.38043)）；MIMESIS 用的都是短 gym（[data_preprocess](https://github.com/VietHoang1512/mimesis/tree/58034ff9887cd67914e7acac2a73965fb7cb3782/agent/examples/data_preprocess)）；VibeLife 根本没有交互式用户（[event.yaml](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/event.yaml)）。
6. **信任、打扰成本这类指标的可规模化代理**：LLM judge 会混淆能力与信任，目前只有 30 人研究（[2609.37267](https://arxiv.org/abs/2609.37267)）。
7. **同时惩罚“欠用”和“滥用”个人信息的基准**：现有基准各测一边（[InMind](https://arxiv.org/abs/2607.24368) / [Mirage](https://arxiv.org/abs/2608.04570)）。
8. **跨设备统一的个人环境**：手机、眼镜、桌面三类基准彼此分离（[MobileMem](https://arxiv.org/abs/2608.13606)、[APM-Bench](https://arxiv.org/abs/2609.37559)、[MyPCBench 经 Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）；nanoMuse 的评测套件还在路线图上（[2610.08699](https://arxiv.org/abs/2610.08699)）。
9. **反事实与矛盾处理**：MyPCBench 的 Counterfactual 切片完美率 ≤22%（[表 7](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）；ProEvent 中事件取消处理不好（[2607.17701](https://arxiv.org/abs/2607.17701)）。
10. **关键词式 rubric 的抗刷性**：VibeLife 的部分 stage 检查是对工作区做关键词匹配（[_stage_checks.py](https://github.com/evolvent-ai/VibeLifeBench/blob/cd21b2cb5d18a81b0fcdb4a948889a2148f48958/eval_set/travel/galapagos_no_us_transit/rubrics/_stage_checks.py)）。如果用它做 RL 奖励，需要先做反刷分审计（推论）。

---

## 6. 待核与缺口

- VibeLifeBench 的模型分数（32.5 / 41.2 / 21.1，下降 10–15）只有二手来源，本次搜索没有找到原文表格（[主页](https://vibebench.github.io/VibeLifeBench_homepage/)、[HF](https://huggingface.co/papers/2608.10875)）。
- Proactivity-Gym 的环境细节（服务数、天数、人设数）「无出处，待核」；目前只有摘要和 [二手](https://hyper.ai/en/papers/2609.37267)。
- MyPCBench 的人设（Michael Scott）、任务来源（OpenClaw 社区）和 Opus 4.6 的 55.4% 均来自二手搜索摘要（[二手](https://arxiv.org/pdf/2606.16748)），原文未读。
- UniClawBench 各模型分数只有博客二手来源（[二手](https://agentmarketcap.ai/blog/2026/07/16/uniclawbench-proactive-agent-benchmark)）。
- PAST-Bench 摘要写 7 个模型，仓库只列 5 个 profile；具体增益数字「无出处，待核」（[摘要](https://arxiv.org/abs/2608.04003)、[README](https://github.com/Gen-Verse/PAST-Bench/blob/f8223517ae7491e776b69793d9f11e9d074ab42e/README.md)）。
- MobileMem 排行榜是图片，没有转录（[omni/README](https://github.com/zjunlp/MobileMem/blob/fa5cd13c9c659699df9caf650987ba2bea8ca085/omni/README.md)）。
- 未 clone 的仓库：ContextPilot、UserIDA、Work2Skill、APM-Bench；ProEvent、SenWorld、Setoka、StateMemBench、UserProxyBench 没有仓库，只读了摘要（见第 1 节表中链接）。
- 窗口外的相关前作，本次搜索偶然看到，未读：LifeSim（[arXiv 2603.12152，二手](https://arxiv.org/pdf/2603.12152)）、After Talking with 1,000 Personas（[arXiv 2602.04000，二手](https://arxiv.org/pdf/2602.04000)）。
