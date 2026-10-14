# 办公 / 企业场景 Agent 论文精读笔记：环境构建视角（2026-07-01 → 10-13）

> 输入：A_office.json 中 70 篇自动标注 office-agent 的候选，以及从全量池补检出的 1 篇（Thinkingbox）。
> 引用约定：每条事实都在行内附来源。arXiv abs 链接表示「仅基于摘要」；GitHub blob 链接表示「来自仓库 README、文档或代码」；WebSearch 得到的信息标 (二手)。读不到 arXiv、HF、*.github.io 时，只依赖可 clone 的 GitHub 仓库。所有数字均为作者自报。

## 0. 结论速览

### 必读 Top-6（按「对搭建办公/企业环境的直接可复用度」排序）

1. **[UI-Mate / OSWorkerBench + CUA-Gym-Hub](https://arxiv.org/abs/2608.15930)**（Tencent）：98 个 mock SaaS，统一 State API（set/reset/diff，按 sid 隔离），reward 直接读 state_diff；外层是 OSWorld VM；100 个跨应用办公任务，带 checkpoint 部分分（[CUA-Gym-Hub README](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）。→ 卡片 2.1
2. **[GDPevo](https://arxiv.org/abs/2608.03764)**：CRM、ERP 等 24 个共享业务环境，构建 SOP 全部开源：禁止 answer endpoint、agent 与环境网络隔离、read_only/mutable 两种重置、用参考模型 avg@3 做难度标定、6 票审稿（[guides](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/environment_and_data.md)）。→ 卡片 2.16
3. **[ScaleCUA / VeriGen](https://arxiv.org/abs/2607.11185)**（THUDM）：在 live docker VM 里由 coding agent 合成 evaluator，并做「初始状态不得通过、解后必须通过」的 negative control；轨迹驱动难度；EMA 前沿采样（[VeriGen docs](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/agent_feasibility_verification.md)）。→ 卡片 2.2
4. **[HANDBOOK.md](https://arxiv.org/abs/2607.25398)**（Surge AI）：mock Gmail/Slack/Jira/Calendar/Shopify 走 MCP，JSON 种子做初始化；rubric 是「自然语言 + verifier_code」配对，含 must-not 检查；用规则扰动防记忆（[rubrics.json](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/tests/rubrics.json)）。→ 卡片 2.15
5. **[Thinkingbox](https://arxiv.org/abs/2608.19741)**（Microsoft）：MCP Session Proxy 隔离会话，加 LLM 用户模拟器；断言写在 effects 上并拒绝多余副作用；报告 pass^20（[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)）。→ 卡片 2.14
6. **[OmegaUse-OfficeVal](https://arxiv.org/abs/2607.27155)**（Baidu）：100 个真实办公文件任务，配 100 个 docx/xlsx/pptx 代码 verifier，采用 dim1 门控加 dim2 加减分结构；带经济锚定（[README](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)）。→ 卡片 2.6

其余评为必读、但只有摘要可读或偏数据仓库的：[GraphForge](https://arxiv.org/abs/2609.38923)（2.8）、[CompoWorld](https://arxiv.org/abs/2609.33665)（2.11）、[Argo-Bench](https://arxiv.org/abs/2610.02122)（2.17）。

### 精读论文对比表

| 论文 | 环境形态 | 任务合成 | 验证 | 规模 | 开放 |
|---|---|---|---|---|---|
| [UI-Mate/OSWorkerBench](https://arxiv.org/abs/2608.15930) | OSWorld Ubuntu VM 加 98 个 mock Web SaaS，State API 注入和重置（[src](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)） | 训练侧 5 类指令源加能力树再平衡；基准人工构造（[src](https://github.com/Tencent/UI-Mate/blob/main/README.md)） | reward.py 读 state_diff，1–13 个 checkpoint（[src](https://github.com/Tencent/UI-Mate/blob/main/README.md)） | 100 个任务，41 个应用（[src](https://github.com/Tencent/UI-Mate/blob/main/README.md)） | mock、任务、权重开放；数据引擎未开放（[src](https://github.com/Tencent/UI-Mate/blob/main/README.md)） |
| [ScaleCUA](https://arxiv.org/abs/2607.11185) | 真实应用，OSWorld/ScienceBoard docker VM，100+ 并发生成（[src](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)） | coding agent 从文档或轨迹生成，三档难度（[src](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/README.md)） | 生成的 getter/metric 代码，live negative control（[src](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/verigen_paper_alignment.md)） | 24,655 个候选、3,212 个 RL 任务（[src](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)） | 代码、数据、模型全开放（[src](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)） |
| [SoftwareGym](https://arxiv.org/abs/2610.12611) | LLM 生成的原生 .NET 应用，跑在 OSWorld VM 中（[src](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)） | 设计 → 编码 → GUI 测试 → 修复；用例由 agent 生成（[src](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/skill/Evaltaskgenerateskill/SKILL.md)） | GUI agent 加 judge，再加 dump-state infra_checks（[src](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/eval/state_probe.py)） | 182 个应用，120 题 bench（[src](https://arxiv.org/abs/2610.12611)） | 流水线开放（[src](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)） |
| [CUA-Universe](https://arxiv.org/abs/2609.05374) | 真实桌面软件改造成 VM 加 CLI 面（[src](https://arxiv.org/abs/2609.05374)） | 种子文件上的操作组合，难度可控（[src](https://arxiv.org/abs/2609.05374)） | 「verified」轨迹，方式待核（[src](https://arxiv.org/abs/2609.05374)） | 16 个应用（[src](https://arxiv.org/abs/2609.05374)） | 未见代码 |
| [HybridCUA](https://arxiv.org/abs/2609.38008) | OSWorld VM 集群，统一 session HTTP 协议（[src](https://github.com/ZJU-REAL/HybridCUA/blob/main/env_infra/CLAUDE.md)） | GUI、CLI、交错三类轨迹管线（[src](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)） | RLVR 结果奖励加 R_CLI 和 r_exec（[src](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)） | 5,023 条轨迹，3,000 个任务（[src](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)） | 数据开放，模型待发（[src](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)） |
| [OmegaUse-OfficeVal](https://arxiv.org/abs/2607.27155) | 无交互环境，只评交付物 ZIP（[src](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)） | 从业者真实请求去敏改写（[src](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/data/README.md)） | rubric 转代码 verifier，dim1 门控加 dim2 加减分；9 个要用 Office COM（[src](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)） | 100 个任务（[src](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/data/README.md)） | 全开放（[src](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)） |
| [WorkBuddy Bench](https://arxiv.org/abs/2607.20911) | 每个任务一个 Docker workspace（Harbor）（[src](https://github.com/Tencent/workbuddy-bench/blob/main/datasets/README.md)） | 从真实 commit/PR/业务场景反向工程，口语化改写（[src](https://arxiv.org/abs/2607.20911)） | Rule 分加可选 rubric-LLM 分，按任务合并（[src](https://github.com/Tencent/workbuddy-bench/blob/main/.agents/skills/wbbench-report-skills/references/wb-bench-office.md)） | Office 50 题，全集 260 题（[src](https://github.com/Tencent/workbuddy-bench/blob/main/README.md)） | 全开放（[src](https://arxiv.org/abs/2607.20911)） |
| [GraphForge](https://arxiv.org/abs/2609.38923) | 真实文件 workspace，配 OpenHands 或 Claude Code（[src](https://arxiv.org/abs/2609.38923)） | 职业种子 → evidence graph → 任务和 rubric → 试跑修复（[src](https://arxiv.org/abs/2609.38923)） | 文件锚定的 rubric，同时用作 RFT 选样（[src](https://arxiv.org/abs/2609.38923)） | 2,169 条轨迹（[src](https://arxiv.org/abs/2609.38923)） | 未见代码 |
| [NexForge](https://arxiv.org/abs/2607.14186) | 自动构建文件、依赖和运行时（[src](https://arxiv.org/abs/2607.14186)） | 需求调研 → 按分布编译（[src](https://arxiv.org/abs/2607.14186)） | 未说明（待核） | 2K office 任务、3.6K terminal 任务（[src](https://arxiv.org/abs/2607.14186)） | 未见代码 |
| [OSWorld-Pro](https://arxiv.org/abs/2609.24890) | OSWorld 式 VM（推断） | 人工标注 67K+ 条（[src](https://arxiv.org/abs/2609.24890)） | 人类对齐的 LLM-judge 判 subgoal（[src](https://arxiv.org/abs/2609.24890)） | 300+ 任务，2,800+ subgoal（[src](https://arxiv.org/abs/2609.24890)） | 未见代码 |
| [CompoWorld](https://arxiv.org/abs/2609.33665) | 代码化服务（typed state）加 world model 兜底（[src](https://arxiv.org/abs/2609.33665)） | 依赖图随机游走组合跨服务任务（[src](https://arxiv.org/abs/2609.33665)） | 验证过的轨迹加 Completion-Focused Rubric Reward（[src](https://arxiv.org/abs/2609.33665)） | 448 个服务，10,130 个工具（[src](https://arxiv.org/abs/2609.33665)） | 仓库不可访问 |
| [AgentMercury](https://arxiv.org/abs/2608.20634) | 合成的持久世界：实体、服务、状态、不变式（[src](https://arxiv.org/abs/2608.20634)） | 从世界中派生任务（[src](https://arxiv.org/abs/2608.20634)） | 可执行的跨服务不变式（[src](https://arxiv.org/pdf/2608.20634)，二手） | 4,783 个环境（[src](https://arxiv.org/abs/2608.20634)） | 未见代码 |
| [Apple env-free](https://arxiv.org/abs/2607.16900) | 纯 LLM 模拟 API 响应（[src](https://arxiv.org/abs/2607.16900)） | LLM 从 API spec 生成（[src](https://arxiv.org/abs/2607.16900)） | LLM judge 过滤（[src](https://arxiv.org/abs/2607.16900)） | 待核 | 未见代码 |
| [Thinkingbox](https://arxiv.org/abs/2608.19741) | mock MCP 工具，Session Proxy 隔离，加 LLM 用户（[src](https://github.com/microsoft/thinkingbox/blob/main/README.md)） | 人工编写 pytest 式用例（[src](https://github.com/microsoft/thinkingbox/blob/main/docs/writing_effective_tests.md)） | 对 effects 断言，可选 RubricJudge 评回复（[src](https://github.com/microsoft/thinkingbox/blob/main/dataset/test_case/cloud_drive.py)） | 507 个 workflow（[src](https://github.com/microsoft/thinkingbox-data/blob/main/README.md)） | 框架、数据、RL 仓库全开放（[src](https://github.com/microsoft/thinkingbox/blob/main/README.md)） |
| [HANDBOOK.md](https://arxiv.org/abs/2607.25398) | 文件 workspace 加 mock 邮件、Slack、Jira、日历、Shopify，走 MCP，JSON 种子（[src](https://github.com/surge-ai/handbook/tree/main/tasks/hr_crestwood_university_79786c46/environment)） | 专家手册 × 规则扰动（[src](https://github.com/surge-ai/handbook/blob/main/README.md)） | 824 条「rubric_text + verifier_code」，含禁止项（[src](https://arxiv.org/abs/2607.25398)） | 65 个任务（[src](https://arxiv.org/abs/2607.25398)） | 只开放 3 个样例（[src](https://github.com/surge-ai/handbook/blob/main/README.md)） |
| [GDPevo](https://arxiv.org/abs/2608.03764) | agent 自建的 Web/API 加 SQLite 业务系统，Docker 网络隔离（[src](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/environment_and_data.md)） | 种子取自 GDPval/SOP-Bench，规则杂交，avg@3 标定（[src](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/calibration_and_review.md)） | 确定性 evaluate.py，加权 scoring points（[src](https://github.com/Prism-Shadow/GDPevo/blob/main/data/task_groups/task_group_001/train_tasks/001/eval/evaluate.py)） | 240 个任务，24 个环境（[src](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md)） | 全开放（[src](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md)） |
| [Argo-Bench](https://arxiv.org/abs/2610.02122) | 城市级业务模拟器导出成 235 表 ERP 仓库，gVisor 沙箱（[src](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)） | 基于文献和监管文件设计模拟加人工出题（[src](https://arxiv.org/abs/2610.02122)） | 行动回灌模拟器按后果评分，参考解可执行（[src](https://arxiv.org/abs/2610.02122)） | 210 题，75 亿行（[src](https://arxiv.org/abs/2610.02122)） | 代码和数据开放，答案键保留（[src](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)） |

### 跨论文观察：办公/企业环境目前是怎么搭的

1. **「mock SaaS + 可注入/可 diff 的状态 API」成为主流折中，真实 SaaS 基本缺席。**
   - 证据：CUA-Gym-Hub 用 98 个 React mock，经 `/post set|reset` 与 `/go` diff 管理状态（[UI-Mate](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）；HANDBOOK 的 mock Gmail/Slack/Jira 以 JSON 种子初始化、以 final.json 取终态（[HANDBOOK](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/tests/sop_verifier.py)）；Thinkingbox 用 MCP mock 加 effects 取回（[Thinkingbox](https://github.com/microsoft/thinkingbox/blob/main/README.md)）；GDPevo 自建 Web/API 加 SQLite（[GDPevo](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/environment_and_data.md)）。
   - 精读的 17 篇里没有一篇在真实商业 SaaS 租户上训练或评测。真实应用只出现在桌面办公套件和 OS 层，即 OSWorld VM（[ScaleCUA](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)，[SoftwareGym](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)）。
2. **环境本身也在交给 coding agent 生成，并配有「运行时自检」闭环。**
   - 证据：SoftwareGym 用 Codex 生成整个应用，再在 VM 里做 GUI 测试并修复（[SoftwareGym](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)）；VeriGen 让 Claude Code 写 evaluator 并在 live docker 中验证（[ScaleCUA](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/README.md)）；GDPevo 的三阶段 Codex workspace 生成环境、任务和 grader（[GDPevo](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md)）；CompoWorld 让 coding agent 把工具规格实现成服务（[CompoWorld](https://arxiv.org/abs/2609.33665)）；AgentMercury 甚至把「构建世界」本身作为训练目标（[AgentMercury](https://arxiv.org/abs/2608.20634)）。
   - 共同的硬门槛：初始状态不得通过，存在一个能通过的解（[VeriGen](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/agent_feasibility_verification.md)）；用参考模型 avg@3 落在目标区间做难度标定（[GDPevo](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/calibration_and_review.md)）。
3. **verifier 正在收敛到「结构化 rubric，每条可执行，有部分分，有禁止项」。**
   - 证据：HANDBOOK 的 `rubric_text + verifier_code` 配对含 must-not 检查（[HANDBOOK](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/tests/rubrics.json)）；OfficeVal 用 dim1 门控加 dim2 加减分（[OfficeVal](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/docs/result-format.md)）；GDPevo 用加权 scoring points（[GDPevo](https://github.com/Prism-Shadow/GDPevo/blob/main/data/task_groups/task_group_001/train_tasks/001/eval/evaluate.py)）；Thinkingbox 拒绝多余副作用（[Thinkingbox](https://arxiv.org/abs/2608.19741)）；WorkBuddy 用 Rule 分合并 rubric-LLM 分（[WorkBuddy](https://github.com/Tencent/workbuddy-bench/blob/main/.agents/skills/wbbench-report-skills/references/wb-bench-office.md)）。
   - LLM-judge 主要用于开放文本、过程 subgoal（[OSWorld-Pro](https://arxiv.org/abs/2609.24890)）和训练数据筛选（[GraphForge](https://arxiv.org/abs/2609.38923)，[Apple](https://arxiv.org/abs/2607.16900)）。
4. **任务合成从「模板」转向「锚定 + 组合」。** 锚点有几类：
   - 真实文件或证据图（[GraphForge](https://arxiv.org/abs/2609.38923)）；
   - 原子业务规则的拆分与重组（[GDPevo](https://arxiv.org/abs/2608.03764)）；
   - 服务依赖图上的随机游走（[CompoWorld](https://arxiv.org/abs/2609.33665)）；
   - 种子文件上的可复用操作（[CUA-Universe](https://arxiv.org/abs/2609.05374)）；
   - 真实需求分布（[NexForge](https://arxiv.org/abs/2607.14186)）；
   - 失败或成功轨迹，用于简化或加难（[VeriGen](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/README.md)）。
   
   防泄漏有三条路线：改写 prompt 使其无法检索（[WorkBuddy](https://arxiv.org/abs/2607.20911)）；规则扰动（[HANDBOOK](https://github.com/surge-ai/handbook/blob/main/README.md)）；快速再生成新版本或保留答案键（[GDPevo](https://arxiv.org/abs/2608.03764)，[Argo-Bench](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)）。
5. **隔离是一等公民。状态可读等于 reward 可 hack，这已有实证。**
   - Argo-Bench 开发期有 run 读到 grader 和答案键，得分 0.99（[Argo-Bench](https://github.com/TextQLLabs/Argo-Bench/blob/main/analysis/reward_hacking/README.md)）。
   - CUA-Gym-Hub 专门加了 hardened 模式，防止有 shell 的 agent 从 URL 或 LevelDB 读状态（[UI-Mate](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）。
   - GDPevo 禁止 agent 容器挂载 env/、数据库或种子（[GDPevo](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/environment_and_data.md)）。
   - 字符串断言过严的误判风险，见 [How Benchmarks Mis-Score CUAs](https://arxiv.org/abs/2607.28367) 和 [TRACE](https://arxiv.org/abs/2610.11678)。
6. **训练配方相对一致，各家差异主要在数据和课程。**
   - 共同流程是「验证过的轨迹做 SFT，再在可执行 verifier 上做 GRPO 类在线 RL」（[UI-Mate](https://github.com/Tencent/UI-Mate/blob/main/README.md)，[ScaleCUA](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)，[HybridCUA](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)，[CompoWorld](https://arxiv.org/abs/2609.33665)）。
   - 差异化手段：前沿或弱域课程采样（[ScaleCUA](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)，[UI-Mate](https://github.com/Tencent/UI-Mate/blob/main/README.md)）、rubric 动态加权（[CompoWorld](https://arxiv.org/abs/2609.33665)）、行为塑形奖励（[HybridCUA](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)）、用 rubric 选样的 RFT（[GraphForge](https://arxiv.org/abs/2609.38923)）。
   - 纯 LLM 模拟环境只用于 SFT 冷启动（[Apple](https://arxiv.org/abs/2607.16900)）。


---

## 1. 筛选表（全部 70 篇，基于摘要）

图例：✅ 精读（本笔记有卡片）· ◐ 部分相关（未精读，有可借鉴点）· ✗ 不相关或误标。每行理由都来自该行链接的 arXiv 摘要。

| # | 标题 (arXiv) | 机构 · HF↑ | 相关? | 理由（基于摘要） |
|---|---|---|---|---|
| 0 | [StateAct: Program State, before Pixels, for Long-Horizon Computer-Use Agents](https://arxiv.org/abs/2607.22798) | Salesforce AI Research · 53 | ◐ | Salesforce；CUA harness（code-first 操作程序状态）+ finish gate 校验产物；非环境构建，但 state-grounded 验证思路可借鉴（OSWorld 2.0） |
| 1 | [SoftwareGym: Scaling Computer-Use Agent Training with Diverse Synthesized Software Environments](https://arxiv.org/abs/2610.12611) | Shanghai Jiao Tong University · 85 | ✅ 精读 | 自动合成可运行 GUI 软件（182 apps）+ OSWorld VM 运行时 GUI 验证修复，直接是环境合成 |
| 2 | [UI-Mate: Advancing Open-Weight Foundation GUI Agents with In-Context Demonstrations](https://arxiv.org/abs/2608.15930) | Tencent Hunyuan · 33 | ✅ 精读 | Tencent；闭环数据引擎（任务合成→环境构建→rollout→verifier）+ OSWorkerBench 100 个办公长程任务/41 应用 |
| 3 | [HybridCUA: Learning to Orchestrate GUI and CLI for Computer-Use Agents](https://arxiv.org/abs/2609.38008) | Zhejiang University · 28 | ✅ 精读 | OSWorld 上 GUI+CLI 轨迹构造（5K 轨迹+3K RLVR 任务）+ 统一 env session 服务 |
| 4 | [OSWorld-Science: A Benchmark of Computer Use Agents for Learning and Using Scientific Software](https://arxiv.org/abs/2609.39903) | DiscoAILab · 28 | ◐ | 科学软件 CUA 基准，artifact-based 评测；非办公，但构建方法可参考 |
| 5 | [OSWorld-Pro: Process-based Evaluation for Computer Use Agents](https://arxiv.org/abs/2609.24890) | NVIDIA · 22 | ✅ 精读 | NVIDIA；OSWorld 之上 300+ 任务/2800 subgoal 过程评测，LLM-judge 对齐人工标注——verifier 设计 |
| 6 | [AutoGUIWorld: Image Generators as Visual World Models for GUI Agent](https://arxiv.org/abs/2610.01215) | Tencent Hunyuan · 42 | ◐ | 图像生成模型做 GUI 视觉 world model 合成轨迹（免部署）；与办公环境相关但偏数据合成 |
| 7 | [LongHorizon-Harness: Advancing Long-Horizon Agents for Real-World Tasks](https://arxiv.org/abs/2608.01964) | alibaba · 175 | ✗ | 长程 harness 状态管理，非环境构建 |
| 8 | [Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents](https://arxiv.org/abs/2609.17653) | Zhejiang University · 12 | ✗ | GUI 技能自演化（训练无关），非环境 |
| 9 | [Atria Dawn: The Dawn of Agentic Superintelligence](https://arxiv.org/abs/2609.15818) | Intern Large Models · 411 | ✗ | 通用 agentic 基座模型报告，Verifiable Experience Pipeline 细节不聚焦办公 |
| 10 | [Masked Diffusion Language Models are Strong and Steerable Text-Based World Models for Agentic RL](https://arxiv.org/abs/2607.16204) | Patronus AI · 5 | ◐ | MDLM 做文本 world model 模拟环境（含 AppWorld 迁移）；环境模拟方法论，非办公特定 |
| 11 | [Environment-free Synthetic Data Generation for API-Calling Agents](https://arxiv.org/abs/2607.16900) | Apple · 14 | ✅ 精读 | Apple；仅凭 API spec 用 LLM 模拟有状态环境合成轨迹，评测 OfficeBench/AppWorld |
| 12 | [OmegaUse-OfficeVal: Benchmarking LLM Agents on Long-Horizon Office-Suite Tasks with Economic Grounding](https://arxiv.org/abs/2607.27155) | Baidu · 7 | ✅ 精读 | Baidu；100 个真实办公套件任务 + 经济锚定 + rubric→代码 verifier，开源 |
| 13 | [DRACO: Fine-Grained Credit Assignment with Dynamic Rubrics for Long-Horizon Agent Training](https://arxiv.org/abs/2609.04094) | IBM Research · 23 | ◐ | IBM；无 checker 场景的动态 rubric 奖励信用分配——奖励设计可借鉴，非环境 |
| 14 | [ClawGym II: Exploring Black-Box RL on Agent Harness](https://arxiv.org/abs/2608.16798) | Renmin University of China · 34 | ✗ | harness 黑盒 RL 基础设施（sandbox），非办公 |
| 15 | [Tencent WorkBuddy Bench: A Multi-Domain Coding-Agent Benchmark with Contamination-Resistant Task Construction](https://arxiv.org/abs/2607.20911) | Tencent · 21 | ✅ 精读 | Tencent；含 Office 子集（50 任务），任务从真实业务反向工程以抗污染，Docker 化 |
| 16 | [Recursive Experiential-Working Memory Evolution for Long-Horizon Agent Harnesses](https://arxiv.org/abs/2608.24876) | Princeton University · 20 | ✗ | 记忆架构/自我改进，非环境 |
| 17 | [StarHarness: Evolving Harnesses with Stratified Search for Enterprise Environments](https://arxiv.org/abs/2608.24804) | ServiceNow-AI · 35 | ◐ | ServiceNow；harness 演化，在 EnterpriseOps-Gym 等企业环境上评估；非环境构建 |
| 18 | [E-Commerce Bench: Evaluating LLM Agents on Long-Horizon Autonomous Business Operation](https://arxiv.org/abs/2608.30730) | Qwen · 8 | ◐ | Qwen；年度电商经营模拟（确定性需求模型+谈判内核），企业业务模拟器参考 |
| 19 | [SkillOpt-Lite: Better and Faster Agent Self-evolution via One Line of Vibe](https://arxiv.org/abs/2607.03451) | LMMs-Lab · 16 | ✗ | 技能优化方法，非环境 |
| 20 | [DeskForge: Dense Supervision from Desktop Environments for Computer-Use Agents](https://arxiv.org/abs/2610.02320) | Docling · 7 | ◐ | 组合真实桌面应用生成 1.2M 稠密 grounding 标注；数据/环境可控组合有借鉴 |
| 21 | [SCALECUA: Scaling Computer Use Agents with Verifiable Task Synthesis and Efficient Online RL](https://arxiv.org/abs/2607.11185) | — · — | ✅ 精读 | THUDM；VeriGen 在 live OSWorld docker 中合成可验证 RL 任务（24K+ / ~3K）+ Frontier Sampling |
| 22 | [Harness-Zero: Harness Distillation via Agent-as-Harness](https://arxiv.org/abs/2609.24974) | Peking University · 13 | ✗ | harness 蒸馏，非环境 |
| 23 | [UI-MOPD: Multi-Platform On-Policy Distillation for Continual GUI Agent Learning](https://arxiv.org/abs/2607.04425) | Unknown · 63 | ✗ | 多平台 GUI on-policy 蒸馏，训练方法 |
| 24 | [OpenForgeRL: Train Harness-native Agents in Any Environment](https://arxiv.org/abs/2607.21557) | Microsoft · 6 | ◐ | Microsoft；训练 harness-native agent 的框架（代理记录调用），基础设施向 |
| 25 | [JarvisHub: An Open Harness for Canvas-Native Multimodal Creative Agents](https://arxiv.org/abs/2607.23588) | Unknown · 104 | ✗ | 创意生成 harness，非办公环境 |
| 26 | [CompoWorld: Compositional Environment Scaling for General Agents](https://arxiv.org/abs/2609.33665) | AllSpark Research · 30 | ✅ 精读 | 448 服务/10,130 工具的组合式环境扩展 + world model 兜底 + rubric 奖励，评测 AutomationBench |
| 27 | [Ouroboros: A Self-Developing Frontier Coding Agent with Reviewed Core Evolution](https://arxiv.org/abs/2608.08311) | Unknown · 85 | ✗ | 自我开发 coding agent |
| 28 | [Search Beyond What Can Be Taught: Evolving the Knowledge Boundary in Agentic Visual Generation](https://arxiv.org/abs/2607.05382) | TIGER-Lab · 69 | ✗ | 视觉生成搜索 |
| 29 | [Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory](https://arxiv.org/abs/2608.07169) | KAIST AI · 49 | ✗ | 记忆蒸馏 |
| 30 | [Work2Skill: Capturing Human GUI Experience for Reusable Agent Skill Induction](https://arxiv.org/abs/2610.12984) | Nex AGI · 41 | ◐ | 采集人类 GUI 演示归纳技能（WorkRecorder）；数据采集可借鉴 |
| 31 | [GUI-HARVEST: Self-Improving GUI Agents through Evidence-Driven Harness Evolution](https://arxiv.org/abs/2610.00948) | The Chinese University of Hongkong,Shenzhen · 12 | ✗ | GUI harness 自动优化 |
| 32 | [Token-Efficient Data Reasoning Agents via Adaptive Structuring of Unstructured Data](https://arxiv.org/abs/2608.31082) | Harvard University · 4 | ✗ | 非结构化数据结构化以省 token，非环境 |
| 33 | [UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training](https://arxiv.org/abs/2609.38043) | — · — | ◐ | 用户模拟器保真度评测（tau-bench 系）；用户模拟是企业环境组件 |
| 34 | [GDPevo: Evaluating Agent Self-Evolution on Real Business Tasks](https://arxiv.org/abs/2608.03764) | Prism Shadow · 27 | ✅ 精读 | CRM/ERP/金融等 24 组共享业务环境+规则杂交任务+确定性 grader，全自动构建管线开源 |
| 35 | [CogEvol: Towards Efficient and Reliable Learning Environment Generation](https://arxiv.org/abs/2608.30968) | 元知进化（北京）科技有限公司 · 26 | ◐ | 课件/slides 生成模型，rule+VLM 奖励；产物生成而非环境 |
| 36 | [Function-Aware Fill-in-the-Middle as Mid-Training for Coding Agent Foundation Models](https://arxiv.org/abs/2607.12463) | TIGER-Lab · 22 | ✗ | 代码 FIM 中训练 |
| 37 | [Managing Procedural Memory in LLM Agents: Control, Adaptation, and Evaluation](https://arxiv.org/abs/2606.23127) | unknown · 17 | ◐ | 382 个企业任务的程序性记忆基准；环境构建信息少 |
| 38 | [Evo-Bench: Can Language Models Improve Agent Harness?](https://arxiv.org/abs/2608.09096) | RUC-AIBOX · 18 | ✗ | harness 演化基准 |
| 39 | [GraphForge: Training Working Agents with Graph-Anchored Workspace Synthesis](https://arxiv.org/abs/2609.38923) | University of Science and Technology of China · 34 | ✅ 精读 | USTC；基于真实文件 evidence graph 合成工作区任务+文件锚定 rubric，SFT/RFT 提升 GDPval |
| 40 | [Argo-Bench: Evaluating Data Agents on Enterprise-Scale Workflows](https://arxiv.org/abs/2610.02122) | TextQL · 18 | ✅ 精读 | TextQL；模拟城市级外卖公司→235 表 Oracle EBS 式 ERP 仓库，按行动后果在模拟器中评分 |
| 41 | [INS-ActBench: A Comprehensive Benchmark for Assessing Professional Actuarial Capability of Large Language Models](https://arxiv.org/abs/2607.24273) | — · — | ✗ | 精算 QA 基准 |
| 42 | [How Benchmarks Mis-Score Computer-Use Agents](https://arxiv.org/abs/2607.28367) | — · — | ◐ | 审计 CUA 基准误判（任务过期/oracle 拒绝合法解）；verifier 风险清单 |
| 43 | [Rethinking Inference-Time Scaling in Local Computer-Use Agents: Failure Modes and Compute Tradeoffs](https://arxiv.org/abs/2607.28573) | — · — | ✗ | 本地 CUA 推理时扩展 |
| 44 | [StagedWorkspace: A Versioned Workspace for Knowledge-Work Agents](https://arxiv.org/abs/2608.18050) | — · — | ◐ | 知识工作 versioned workspace（parsed/native 双视图），harness 层 |
| 45 | [CURA: Certified Runtime Alarms for Computer-Use Agents](https://arxiv.org/abs/2608.27808) | — · — | ✗ | CUA 运行时告警监控 |
| 46 | [From Interaction Traces to Persistent Skills: Online Evolution for Computer-Use Agents](https://arxiv.org/abs/2609.04869) | — · — | ✗ | CUA 技能在线演化 |
| 47 | [CUA-Universe: A Scalable and Dynamic Environment for Hybrid GUI+CLI Agents](https://arxiv.org/abs/2609.05374) | — · — | ✅ 精读 | 把真实桌面软件改造成可复现 VM + CLI 面（16 apps），可控难度任务合成+验证轨迹采集 |
| 48 | [Programmatic Search Agents: Extending Agentic Search Beyond Query Reformulation](https://arxiv.org/abs/2610.06689) | — · — | ✗ | 搜索 agent |
| 49 | [SWE-Game: Can Coding Agents Build the Games We Want?](https://arxiv.org/abs/2609.33678) | unknown · 25 | ✗ | 游戏开发基准 |
| 50 | [NexForge: Scaling Agent Capabilities through Requirement-Driven Task Synthesis for LLMs](https://arxiv.org/abs/2607.14186) | Nex AGI · 7 | ✅ 精读 | Nex AGI；需求驱动任务合成，自动构建文件/依赖/运行时，2K office 任务提升 GDPval |
| 51 | [UndoBench: Separating Task Competence from Recovery Capability in Tool-Using AI Agents](https://arxiv.org/abs/2610.05622) | Unknown · 11 | ◐ | 8 个企业域的故障恢复基准，effect-history + 环境状态 oracle；恢复/幂等性评测可借鉴 |
| 52 | [HANDBOOK.md: A Benchmark for Long-Context Agentic Instruction Following](https://arxiv.org/abs/2607.25398) | — · — | ✅ 精读 | Surge AI；mock email/chat/calendar/Jira MCP + 长 SOP，824 条程序化 rubric 检查必做/禁做 |
| 53 | [Document Retrieval-Aware Chunking (D-RAC): Universal Retrieval-Aware Ingestion of Enterprise Documents via PDF Normalization and Multimodal Markdown Conversion](https://arxiv.org/abs/2609.24220) | Yellow.ai · 51 | ✗ | RAG 文档切块 |
| 54 | [ELICITED: EHR-grounded Longitudinal Interactive Conversations for Information-seeking Triage Evaluation and Decision-making](https://arxiv.org/abs/2608.09024) | — · — | ✗ | 医疗分诊对话 |
| 55 | [AgentMercury: Your Agent Can Synthesize Verifiable Environments for Business Scenarios at scale](https://arxiv.org/abs/2608.20634) | unknown · 7 | ✅ 精读 | 从业务场景合成持久世界（实体/服务/状态/跨服务不变式），4,783 个可执行环境用于 RL |
| 56 | [ClawProBench: Trace-Aware Evaluation of AI Agents with Runtime Coverage and Frozen Workplace-Style Holdouts](https://arxiv.org/abs/2608.22510) | unknown · 3 | ◐ | OpenClaw 运行时 trace-aware 评测（workspace/消息/日程），冻结 holdout |
| 57 | [MNIST-PRO: MNIST is Back as a Partially Observable World for AI Agents](https://arxiv.org/abs/2608.31022) | Deep Cognition and Language Research (DeCLaRe) Lab · 7 | ✗ | MNIST 部分可观测 |
| 58 | [ExtractBench: A Benchmark for Schema-Guided Enterprise Document Extraction](https://arxiv.org/abs/2607.29677) | unknown · 24 | ◐ | 企业文档 schema 抽取基准，非交互环境 |
| 59 | [Multi-scale Mixture of World Models for Embodied Agents in Evolving Environments](https://arxiv.org/abs/2607.00457) | — · — | ✗ | 具身 world model |
| 60 | [CEAA: A Cognitive Embodied Agents Architecture for Interactive Computing Systems](https://arxiv.org/abs/2608.09848) | Unknown · 6 | ✗ | 具身虚拟角色 |
| 61 | [Decoupling Planning and Control for Instructable Agents](https://arxiv.org/abs/2608.26788) | — · — | ✗ | 具身规划控制 |
| 62 | [Tomatoes, Potatoes, and Onions: Questioning the Need for Faces in Face Presentation Attack Detection](https://arxiv.org/abs/2608.21455) | Fraunhofer IGD · 2 | ✗ | 人脸活体检测 |
| 63 | [ResidencyRL: Reinforcement Learning in Simulated Clinical Environments](https://arxiv.org/abs/2608.07418) | — · — | ✗ | 临床模拟 RL |
| 64 | [MTDiag: A Multi-Turn Diagnostic Dataset Towards Clinically Meaningful LLM Evaluation](https://arxiv.org/abs/2608.25085) | — · — | ✗ | 医疗诊断数据集 |
| 65 | [LocalLSTC: A Long Short-Term Control Architecture for Locally Deployed GUI Agents](https://arxiv.org/abs/2608.25777) | — · — | ✗ | 本地 GUI agent 架构 |
| 66 | [TRACE: Diagnosing Verifier Brittleness in Agentic Evaluation](https://arxiv.org/abs/2610.11678) | — · — | ◐ | verifier 脆性诊断协议（改名工具/改评分规则），奖励稳健性参考 |
| 67 | [Personalization as Inverse Planning: Learning Latent Design Intents for Agentic Slide Generation via Structural Denoising](https://arxiv.org/abs/2607.00407) | Unknown · 2 | ✗ | slide 个性化设计生成，非环境 |
| 68 | [Continuous Process-Level Evaluation for Evolving Enterprise AI Agent Skills](https://arxiv.org/abs/2610.01833) | — · — | ◐ | 企业 skill 持续过程级评测（DB 完整性、工具顺序检查） |
| 69 | [Conversable Complexity: Agentic LLM Collectives as Interpretable Substrates](https://arxiv.org/abs/2607.01047) | — · — | ✗ | LLM 群体复杂性 |

**筛选统计**：✅ 16 篇 · ◐ 20 篇 · ✗ 34 篇。另从全量池补检到 1 篇精读：[Thinkingbox](https://arxiv.org/abs/2608.19741)（Microsoft，有状态业务工作流 sandbox）。

**全量池补检的其它相关论文**（未精读，只列摘要要点）：
- [Era by Eon Benchmark](https://arxiv.org/abs/2609.09853)：由一张种子实体图同时驱动 Salesforce、Zendesk、Slack、Gong 等产品模拟器和内部数据库，答案键从最终记录计算得到，因此判分精确。
- [Generating a Consistent Enterprise](https://arxiv.org/abs/2609.11286)：同一张实体图投影到 66 种业务产品的原生格式。真实感用 28 项统计检查加对抗检测器做无参考验证。
- [Synthesis Through Simulation（SAP）](https://arxiv.org/abs/2610.10549)：LLM agent 通过带策略约束的 API 在模拟企业环境中「操作出」数据，结构有效性由构造保证。摘要称 10 个环境上约束满足率 100%。
- [Skill2Env（AllSpark）](https://arxiv.org/abs/2609.33772)：从 skill 出发生成任务蓝图，同时构建工作区和 rubric evaluator，并用 Iterative Task Hardening 迭代加难。
- [Trace2Env（NTU，HF 98↑）](https://arxiv.org/abs/2610.06100)：原系统不可用、只有历史 trace 时，把 trace 重建成 worldbook，由 world-model agent 有状态地模拟环境。
- [MiniCorp（Microsoft）](https://arxiv.org/abs/2610.05912)：办公模拟器，内部多 agent 经营公司、外部模拟市场，支持 checkpoint 反事实回放，可用于生成企业纵向数据。
- [BI-Bench（MSR）](https://arxiv.org/abs/2609.20886)：从真实公开 BI 项目的 dashboard 人工抽取 (question, answer) 对，并从真实 BI 项目合成训练轨迹。
- [GUI-CC](https://arxiv.org/abs/2609.00048)：评测 GUI world model 作为多步环境时的上下文一致性。摘要指出，单步生成看起来合理，不代表多步模拟可用。

---

## 2. 环境构建卡片

### 2.1 UI-Mate / OSWorkerBench（含 CUA-Gym-Hub 98 个 mock SaaS）

**2608.15930 · 2026-08-18 · Tencent Hunyuan · HF 33↑** · [arXiv](https://arxiv.org/abs/2608.15930) · [repo](https://github.com/Tencent/UI-Mate) · 来源深度：repo-readme（含 benchmark README、mock 应用 README 和任务 JSON），无 PDF

- **场景与任务类型**
  - 100 个长程办公任务，覆盖 41 个应用和 10 个职业族；99 个任务涉及至少两个应用，平均每任务 3.26 个应用（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
  - 子集：67 个 Long-Memory 任务、49 个 Multi-App 任务（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
  - 示例任务 `pm_sprint_closeout_002__long` 跨 Jira、Discord、Asana、Google Sheets 四个 mock：按 Discord 里的讨论结论处理 Jira sprint 收尾，再同步到 Asana 和 Sheet（[task json](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/evaluation_examples/OSWorker/examples/pm/pm_sprint_closeout_002__long.json)）。
- **环境形态**
  - 外层是基于 OSWorld 的 Ubuntu 桌面 VM（Docker），agent 用鼠标和键盘操作（[osworker_bench README](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/README.md)）。
  - 应用层是 98 个自包含的 mock Web 应用（React SPA），仿 Gmail、Outlook、Jira、Salesforce、SAP、ServiceNow、Workday、QuickBooks 等，无鉴权、无外网（[CUA-Gym-Hub README](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）。
  - 100 个任务中 88 个依赖这些 mock，另外 12 个是本地文件任务（[osworker_bench README](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/README.md)）。
  - **状态注入与重置**：通过统一 State API 完成（[CUA-Gym-Hub README](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）：
    - `POST /post?sid=` 的 `set` 注入初始 JSON 状态，`reset` 恢复到初始状态；
    - `GET /go?sid=` 返回 `{initial_state, current_state, state_diff}`；
    - 状态按 sid 存放在 `.mock-states/<sid>.json`，因此并行 rollout 之间互不可见。
  - **防作弊**：可选 hardened 模式。admin token 加一次性 launch_url 换取 HttpOnly cookie，使 shell 能力的 agent 无法从 URL 或 Chrome LevelDB 读出任务状态（[CUA-Gym-Hub README](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）。
  - 训练侧：统一 rollout 层支持 Ubuntu、Windows、macOS 异构环境（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
- **任务来源与合成**
  - 训练指令来自五类来源：开放数据集、失败 rollout 分解、真实工作文件、静态网站、应用能力树（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
  - 环境自动构建：生成任务专属文件和应用状态，并随机化视觉配置（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
  - 用分层能力树发现覆盖缺口，把数据生成重定向到欠代表的应用、操作和任务长度（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
  - Benchmark 的 OSWorkerBench 演示分两类：33 个 self-demo 来自强 agent 的成功 rollout；45 个 variant-demo 是人类录制的相关但不相同任务（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
- **验证与奖励**
  - 每个任务的 config 依次上传 `initial_setup.py` 和 `reward.py`。evaluator 在 postconfig 里执行 `_cua_reward.py` 并读取其 stdout，函数为 `cua_gym_reward`（[task json](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/evaluation_examples/OSWorker/examples/pm/pm_sprint_closeout_002__long.json)）。
  - reward 函数读取 mock 的 `state_diff`；每个 mock 的 `SCHEMA.md` 有 Observable State Changes 表，是写 reward 的主要参考（[CUA-Gym-Hub README](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）。
  - 部分分：每个任务 1–13 个 checkpoint（均值 4.86），同时报告 strict success 和 progress（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
  - 训练侧的多模态过滤会逐项核查每个交付物的证据，而不是相信 agent 自己宣称完成（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
- **数据准备**
  - 先 SFT（交互协议、grounding、应用 workflow），再在可执行环境里用程序化 verifier 加端到端完成奖励做在线 RL（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
  - RL 细节：异步 group-relative 优化；decision-turn centering 加 token 级优势归一化；自适应课程，把 rollout 分给弱应用域；可选 Process Credit Model（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
  - democua 版本在 RL 之后，用通用数据与演示增强数据的混合继续训练（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
- **规模与开放**
  - 开放 100 个任务，以及 33 个 self-demo 共 3,989 个带说明的 GUI 动作步（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
  - 开放 98 个 mock 应用源码（[CUA-Gym-Hub README](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）和 9B/27B 权重（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
  - reward.py 和初始化脚本在 HF cache 中分发，不在 git 里（[osworker_bench README](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/README.md)）。
  - 训练任务池规模未在 README 中给出：「无出处，待核」。
- **关键结果**
  - UI-Mate-27B：OSWorld-Verified 77.0，WindowsAgentArena 66.2（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
  - UI-Mate-27B 在 OSWorkerBench 上 strict 41.00、progress 76.86；比 Qwen3.6-27B 基座分别高 17.67 和 24.51 分（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
- **局限与红旗**
  - mock 是对商业产品的仿制，品牌名做了修改（[CUA-Gym-Hub README](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)），与真实 SaaS 行为存在差距。
  - 默认 State API 完全可读。如果 agent 同时有 shell 和浏览器，必须开 hardened 模式，否则可以直接读状态作弊（[CUA-Gym-Hub README](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）。
  - 端口映射容易错位：上游默认端口 8000–8097，本仓库期望 8100–8197（[osworker_bench README](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/README.md)）。
  - 训练数据引擎的代码没有开放（README 只有描述）。
- **可复用配方**
  - 「mock SaaS + 统一 State API（set/reset/diff，按 sid 隔离）」：一个 mock 通过注入不同 JSON 就能承载任意多个任务世界，reward 只需读 `state_diff`（[CUA-Gym-Hub README](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）。
  - 把 `SANDBOX_COMPLETENESS_GUIDE` 式的「无死按钮、文件流程真实」作为 mock 的验收门槛（[CUA-Gym-Hub README](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）。
  - 用 checkpoint 级 progress 和 strict success 双指标做部分分（[README](https://github.com/Tencent/UI-Mate/blob/main/README.md)）。
- **评级：必读**

### 2.2 ScaleCUA / VeriGen

**2607.11185 · 2026-07-13 · 清华 THUDM（作者含 Jie Tang、Yuxiao Dong）· HF —** · [arXiv](https://arxiv.org/abs/2607.11185) · [repo](https://github.com/THUDM/SCALE-CUA) · 来源深度：repo-readme 加架构文档（[verigen_paper_alignment.md](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/verigen_paper_alignment.md)），无 PDF

- **场景与任务类型**：OSWorld（Ubuntu 桌面，含 LibreOffice 等办公应用）和 ScienceBoard 的 GUI 任务（[README](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)）。
- **环境形态**
  - 真实应用运行在 live OS 容器里（Docker/qemu VM）（[VeriGen README](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/README.md)）。
  - 共享 docker interaction probe 支持 100+ 并发 worker 对接 100+ 个 docker 环境（[README](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)）。
  - RL 阶段有 1000+ 个并行 rollout worker（[README](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)）。
  - 每个 episode 通过 `env.reset(task_config)` 重置；用 `SandboxVmSlot` 在主机层限制 VM 并发（[agent_feasibility_verification.md](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/agent_feasibility_verification.md)，[alignment](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/verigen_paper_alignment.md)）。
- **任务来源与合成**
  - 由 coding agent（Claude Code、Codex 或 OpenCode）编写任务 JSON 和 getter/metric evaluator 代码（[VeriGen README](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/README.md)）。
  - 两种生成模式（[VeriGen README](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/README.md)）：
    - `task_verify`：基于文档、OSWorld cache 文件或种子任务生成；
    - `traj_verify`：基于 rollout 轨迹生成。成功轨迹会生成更难或组合式的变体，失败轨迹会抽取已展示的子技能，生成更简单但仍可验证的任务。
  - 难度可调：`DIFFICULTY=normal|harder|easier`（[VeriGen README](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/README.md)）。
  - proposer、judger、checker 三角色协作：先规则校验，再 LLM judge，然后迭代修复（[alignment](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/verigen_paper_alignment.md)）。
- **验证与奖励**
  - 生成器在 live Docker 中检查 evaluator，共四种模式（[alignment](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/verigen_paper_alignment.md)）：
    - `imports_only`；
    - `judge_only`：setup 能执行、evaluator 能跑，并且**初始状态不能直接通过**；
    - `negative_control`；
    - `agent_solve`：要求 evaluator 分数从「初始 < 阈值」变成「完成后 ≥ 阈值」（[feasibility doc](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/agent_feasibility_verification.md)）。
  - 文档把 trajectory replay 验证列为「剩余工作」，说明尚未完全实现（[alignment](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/verigen_paper_alignment.md)）。
- **数据准备**
  - 先 SFT，再从 SFT checkpoint 开始在线 RL；两种 checkpoint 都已开放（[README](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)）。
  - Frontier Sampling：维护每个任务成功率的 EMA，优先采样处于当前能力边界的任务，并保留少量均匀探索（[README](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)）。
  - Visual Context Segmentation：只保留最近 K 张截图加完整文本历史，作者报告端到端训练提速 2.83x（[README](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)）。
- **规模与开放**
  - 公开 24,655 个只有任务的候选，以及 3,212 个精选 RL 任务（OSWorld 2,049 个、ScienceBoard 1,163 个），并附 OSWorld 可执行 judge 函数（[README](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)）。
  - 代码、模型、数据均开放（[README](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)）。
- **关键结果**：ScaleCUA-Qwen3.5-9B 在 OSWorld 68.7、ScienceBoard 54.0（[README](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)）。
- **局限与红旗**
  - RL 任务池针对 OSWorld 和 ScienceBoard 领域生成（[README](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)），在同分布基准上测试，存在分布贴合风险。
  - OSWorld 版本复用 `osworld_env/cache` 中的文件（[VeriGen README](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/README.md)），任务与测试集的 dedup 方式没有说明：「无出处，待核」。
- **可复用配方**
  - evaluator 必须通过「初始状态不能通过 + 某个解能通过」的双向检查，在 live 环境中做 negative control（[feasibility doc](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/agent_feasibility_verification.md)）。
  - 用轨迹驱动难度：失败轨迹简化成子任务，成功轨迹加难或组合（[VeriGen README](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/README.md)）。
  - 用 EMA 前沿采样做课程（[README](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)）。
- **评级：必读**

### 2.3 SoftwareGym

**2610.12611 · 2026-10-12 · 上海交大 · HF 85↑** · [arXiv](https://arxiv.org/abs/2610.12611) · [repo](https://github.com/MrKiing-Jin/SoftwareGym) · 来源深度：repo-readme 加 skill/eval 代码，无 PDF

- **场景与任务类型**：桌面 GUI 软件（软件类型示例有 `ChatAPP`、`PicEditor`），共 12 类、182 个合成应用（[arXiv](https://arxiv.org/abs/2610.12611)，[README](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)）。
- **环境形态**
  - **LLM 生成的原生应用**（.NET 8 + Avalonia 11），部署进与 OSWorld 相同的 Docker、Ubuntu VM 运行时，用截图加 PyAutoGUI 交互（[README](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)）。
  - VM 用 qcow2 overlay，每个 1–4 GB；需要单独准备约 35 GB 的 OSWorld base image（[README](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)）。
  - 每个应用必须实现 `--dump-state`，并在 `app_data/config.yaml` 和 SQLite 中保存状态（[state_probe.py](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/eval/state_probe.py)）。
  - 测试用例从「本地 demo 数据重置为默认」开始，或通过 `config_seed/open/import` 注入初始状态（[Evaltaskgenerate SKILL](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/skill/Evaltaskgenerateskill/SKILL.md)）。
- **任务来源与合成**
  - 生成流水线：Design（功能规格、N 种 UI 风格蓝图、SVG 图标集）→ Build（Codex CLI 写代码，DevCoder 审查）→ Evaluate（GUI agent 在 VM 里跑测试用例）→ Iterate（v1→v3 修复）（[README](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)）。
  - 测试用例由 EvalTaskGenerateAgent 根据 `feature_matrix.md` 和真实的 `state_schema.json` 生成（[SKILL](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/skill/Evaltaskgenerateskill/SKILL.md)）。
  - 用例约束：A 类 2–3 个、B 类 10–14 个、C 类 ≤3 个；每个用例 ≤10 次 GUI 操作；只用 ASCII 输入；不得依赖真实账号或主观判断（[SKILL](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/skill/Evaltaskgenerateskill/SKILL.md)）。
- **验证与奖励**
  - GUI agent 执行用例，再由 judge 判定（可选 GPT-5.4 风格 computer-use 或 Seed executor/judge）（[README](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)）。
  - C 类用例可以使用框架执行的 `infra_checks`（dump_state、SQLite 字段），字段名必须逐字取自探针得到的白名单（[SKILL](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/skill/Evaltaskgenerateskill/SKILL.md)，[state_probe.py](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/eval/state_probe.py)）。
  - 作者报告 mean GUI task pass rate 91.5%（[arXiv](https://arxiv.org/abs/2610.12611)）。
- **数据准备**：摘要只说用这些环境采集的轨迹训练 CUA（[arXiv](https://arxiv.org/abs/2610.12611)）。仓库只包含环境合成流水线，不含训练代码（[README](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)）。SFT/RL 配方：「无出处，待核」。
- **规模与开放**：182 个应用、120 个任务的 SoftwareGym-Bench（[arXiv](https://arxiv.org/abs/2610.12611)）。流水线代码开放；生成的应用和数据是否开放，README 未说明。
- **关键结果**：OSWorld（严格 OOD）Pass@3 从 41.39% 提高到 56.97%；SoftwareGym-Bench 40.0%（[arXiv](https://arxiv.org/abs/2610.12611)）。
- **局限与红旗**
  - 合成应用是「功能可用的玩具软件」，与 LibreOffice 等真实办公套件在复杂度上差距大。
  - 验证依赖 GUI agent 加 judge，91.5% 是 GUI 任务通过率，不等于功能正确率（[arXiv](https://arxiv.org/abs/2610.12611)）。
  - 生成和修复依赖 Codex CLI 与 Responses API（[README](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)），成本见 `cost_summary.json`，但论文中的数值未读到。
- **可复用配方**
  - 强制被合成的应用暴露 `--dump-state` 机读状态，并用 state probe 生成字段白名单，避免 verifier 引用不存在的字段（[state_probe.py](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/eval/state_probe.py)）。
  - 「生成 → 真实 VM 内 GUI 测试 → 把失败摘要回灌修复」的多轮闭环（[README](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)）。
- **评级：值得浏览**（环境合成思路新，但离真实办公套件远）

### 2.4 CUA-Universe

**2609.05374 · 2026-09-04 · 机构未知 · HF —** · [arXiv](https://arxiv.org/abs/2609.05374) · 无 repo · 来源深度：abstract-only + search

- **场景与任务类型**：真实桌面软件上的 GUI 与 CLI 混合任务（[arXiv](https://arxiv.org/abs/2609.05374)）。
- **环境形态**：App-Forge 把真实应用改造成可复现的 VM，并发现、包装或生成命令行接口，目前扩展到 16 个应用（[arXiv](https://arxiv.org/abs/2609.05374)）。重置、并行和成本细节：「无出处，待核」。
- **任务来源与合成**：Task-Weave 基于种子文件上的可复用操作合成混合任务，难度可控（[arXiv](https://arxiv.org/abs/2609.05374)）。
- **验证与奖励**：Path-Steer 引导 rollout 走高效的混合路径，并收集「verified」轨迹（[arXiv](https://arxiv.org/abs/2609.05374)）。verifier 的具体形式：「无出处，待核」。
- **数据准备**：用收集到的轨迹做 post-training（[arXiv](https://arxiv.org/abs/2609.05374)）。
- **规模与开放**：16 个应用（[arXiv](https://arxiv.org/abs/2609.05374)）。未见 repo。
- **关键结果**：9B 模型在 CUA-Verse、OSWorld、OSWorld-MCP 上成功率和效率都有提升（[arXiv](https://arxiv.org/abs/2609.05374)）。第三方评论指出这些数字没有独立复现（[groundy.com](https://groundy.com/articles/terminal-vs-browser-for-ai-agents-what-a-hybrid-gui-cli-benchmark-shows/)，二手）。
- **局限与红旗**：无代码，机构未知；摘要中的具体数字在本池摘录里被截断。
- **可复用配方**：「从可复用操作 + 种子文件组合任务」的 Task-Weave 思路，适合办公文件类任务按难度调参（[arXiv](https://arxiv.org/abs/2609.05374)）。
- **评级：值得浏览**

### 2.5 HybridCUA

**2609.38008 · 2026-09-30 · 浙江大学 ZJU-REAL · HF 28↑** · [arXiv](https://arxiv.org/abs/2609.38008) · [repo](https://github.com/ZJU-REAL/HybridCUA) · 来源深度：repo-readme 加 env_infra 文档

- **场景与任务类型**：OSWorld 上 GUI 与 CLI 交错的桌面任务，覆盖 11 个应用域（[README](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)）。
- **环境形态**
  - `env_infra` 是多世界平台，目前注册了 OSWorld、MobileWorld、CUA-Gym（[env_infra/CLAUDE.md](https://github.com/ZJU-REAL/HybridCUA/blob/main/env_infra/CLAUDE.md)）。
  - 统一 session 协议：`/v1/sessions` 下的 acquire / reset / step / observe / evaluate / release（[env_infra/CLAUDE.md](https://github.com/ZJU-REAL/HybridCUA/blob/main/env_infra/CLAUDE.md)）。
  - 环境槽位释放后保活复用（`reset_on_release=True`），acquire 时做健康检查（[env_infra/CLAUDE.md](https://github.com/ZJU-REAL/HybridCUA/blob/main/env_infra/CLAUDE.md)）。
  - 训练器只通过 HTTP 与环境交互，从不自己启动 VM（[README](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)）。
- **任务来源与合成**：pipeline 产出三类轨迹：GUI-only 870 条、CLI-only 3,155 条、交错 998 条，另有 3,000 个 verified RLVR 任务，每个任务都标注「CLI 是否有明显执行优势」（[README](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)）。
- **验证与奖励**：在任务结果奖励之外加两个 CLI-aware 奖励（[README](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)）：
  - `R_CLI`：轨迹级，λ=0.1。只有成功轨迹的 CLI 使用与标签一致时才给奖励。
  - `r_exec`：步级，λ=0.3。对 shell 层面失败的命令所对应的 token 做惩罚。
- **数据准备**：先在混合语料上 SFT，再用 GRPO（slime + Megatron 做 actor，SGLang 做 rollout）（[README](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)）。
- **规模与开放**：HybridCUA-8K 数据集开放；模型标注为 coming soon（[README](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)）。
- **关键结果**（[README](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)）：
  - OSWorld 53.6%，平均 14.0 步，比基座高 14.8 分。
  - OSWorld-MCP 47.1%，WindowsAgentArena 36.0%。
  - 给未训练的 agent 直接开 CLI 反而让 OSWorld 掉 2.5–11.5 分。
- **局限与红旗**：环境沿用 OSWorld，并非新的办公环境；CLI 优势标签的标注方式：「无出处，待核」。
- **可复用配方**
  - 统一 session HTTP 协议加槽位保活的环境集群，把训练器与 VM 生命周期解耦（[env_infra/CLAUDE.md](https://github.com/ZJU-REAL/HybridCUA/blob/main/env_infra/CLAUDE.md)）。
  - 把 GUI 和 CLI 统一成单一 `bash` 动作，分成两个工具会掉 7.2 分（[README](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)）。
- **评级：值得浏览**

### 2.6 OmegaUse-OfficeVal

**2607.27155 · 2026-07-30 · Baidu · HF 7↑** · [arXiv](https://arxiv.org/abs/2607.27155) · [repo](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal) · 来源深度：repo-readme 加数据、rubric 和 verifier 代码，无 PDF

- **场景与任务类型**
  - 100 个长程办公套件任务，覆盖 Word、Excel、PPT、PDF 以及跨文件工作流（[data README](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/data/README.md)）。
  - 按 `data/task-en` 统计 domain 分布：Education & Examination 25、Business Operations 20、Other 18、Academic Papers 14、Engineering & Technology 10、Administrative Affairs 9、Financial Data 4（[task-en](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/tree/main/data/task-en)，本人统计）。
  - 每个任务带 `operation_intent` 字段（如 Restructure）（[officeval_001](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/data/task-en/officeval_001.json)）。
- **环境形态**
  - **没有交互环境**。基准只评交付物：一个 ZIP 根目录下含 `officeval_001/` 到 `officeval_100/`，agent 可以用任意方式生成（[README](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)）。
  - 输入文件托管在 HF（[data README](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/data/README.md)）。
  - 每个 verifier 在独立子进程里运行。91 个 verifier 跨平台；9 个（001、008、019 等）需要 Windows 上的 Microsoft Office COM 渲染（[README](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)）。
- **任务来源与合成**
  - 任务来自从业者提出的真实办公请求，经过 privacy-preserving 改写（去敏，但保留原意和自然措辞）（[data README](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/data/README.md)）。
  - 不是合成任务，也没有难度控制机制。
- **验证与奖励**
  - 「细粒度 rubric → 迭代转写成代码 verifier」（[README](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)，[arXiv](https://arxiv.org/abs/2607.27155)）。
  - 两维结构（[result-format](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/docs/result-format.md)，[rubric 示例](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/data/rubrics-en/officeval_001.json)）：
    - dim1 是门控（可用、可修改，例如文件能正常打开），不满足直接 0 分；
    - dim2 是逐条加减分的规则（`max_delta` 可以为负，表示扣分）。
  - verifier 用 python-docx 等库静态解析文件。单个 verifier 可以非常长，例如 `officeval_005_verifier.py` 约 4,000 行（[officeval_005_verifier.py](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/verifiers/officeval_005_verifier.py)，本人 wc 统计）。
- **数据准备**：不涉及，是纯评测基准。
- **规模与开放**
  - 100 个任务，每个带 human_labor_time 和 task_price_proxy（[data README](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/data/README.md)）。
  - 平均人工耗时 2.32 小时（[arXiv](https://arxiv.org/abs/2607.27155)），与仓库 `human_labor_time` 字段均值约 139.4 分钟一致（本人统计，[task-en](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/tree/main/data/task-en)）。
  - 代码、数据、verifier 全部开放（[README](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)）。
- **关键结果**：所有被测 LLM 都远比人便宜、比人快，但交付质量还没接近人类水平（[arXiv](https://arxiv.org/abs/2607.27155)）。具体分数在仓库里没读到：「无出处，待核」。
- **局限与红旗**
  - 每个任务一个手写或半手写的大 verifier，扩展成本极高。
  - 不支持 .doc/.xls/.ppt 旧格式（[README](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)），但 rubric 示例里却写着「.doc 扩展名」（[rubric 001](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/data/rubrics-en/officeval_001.json)），存在 rubric 与 verifier 不一致的风险。
  - 需要渲染的项（页数、版面）依赖 Windows COM，Linux 上会被跳过（[README](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)）。
- **可复用配方**
  - 「dim1 交付物门控 + dim2 加减分条目」的 rubric 结构，直接适合 docx/xlsx/pptx 交付物评分（[result-format](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/docs/result-format.md)）。
  - 给每个任务标注人工工时和价格，做价值加权评测（[data README](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/data/README.md)）。
  - 用安全 ZIP 校验（防路径穿越、防压缩炸弹）加子进程隔离运行 verifier（[README](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)）。
- **评级：必读**（目前最「真实办公文件」导向的开源 verifier 集）

### 2.7 Tencent WorkBuddy Bench（Office 子集）

**2607.20911 · 2026-07-24 · Tencent · HF 21↑** · [arXiv](https://arxiv.org/abs/2607.20911) · [repo](https://github.com/Tencent/workbuddy-bench) · 来源深度：repo-readme 加 config 和 skill 文档，任务本体在 HF 上未读

- **场景与任务类型**
  - 四个子集：Code 80、Web 70、Office 50、Security 60（[README](https://github.com/Tencent/workbuddy-bench/blob/main/README.md)）。
  - Office 子集在 xlsx/csv/pdf/docx 混合文件上生成「完全正确」的产物；作者称难度来自结构、关系、状态和证据链，而不是行数（[README](https://github.com/Tencent/workbuddy-bench/blob/main/README.md)）。
  - Office 子集分三类：data-file-ops 24、doc-ops 17、automation-workdir 9。最后一类包含通知/同步流程和 tool/mock-app 协调（[office report ref](https://github.com/Tencent/workbuddy-bench/blob/main/.agents/skills/wbbench-report-skills/references/wb-bench-office.md)）。
  - 难度分布：easy 13、medium 24、hard 13（同上）。
- **环境形态**
  - 每个任务一个 Docker sandbox（基于 Harbor）：`environment/{Dockerfile, docker-compose.yaml, workspace.tar.gz}`，workspace 在容器内解压到 `/workspace`（[datasets README](https://github.com/Tencent/workbuddy-bench/blob/main/datasets/README.md)）。
  - 运行在 CodeBuddy Code 和 Claude Code 两个 harness 上（[arXiv](https://arxiv.org/abs/2607.20911)）。
  - Office 配置：n_attempts=3，verifier 以 root 身份运行（[office bench yaml](https://github.com/Tencent/workbuddy-bench/blob/main/configs/bench/wb-bench-office-v1.0.yaml)）。
- **任务来源与合成**
  - 每个任务都从真实 commit、PR 或业务场景**反向工程**，改写成简短、口语化、角色扮演式的请求，使 prompt 无法通过搜索原始 issue/PR 找回（[arXiv](https://arxiv.org/abs/2607.20911)）。
  - 抗污染依靠这种构造方式加数据集版本化，而不是保密（[arXiv](https://arxiv.org/abs/2607.20911)）。
- **验证与奖励**
  - Office 用 CompositeVerifier：确定性 Rule 直接评提交的产物；如果配置了 LLM 路由，再用任务专属 rubric 评从产物中抽出的文本和结构证据，然后按每个任务配置的 Rule/Judge 比例合并分数（[office report ref](https://github.com/Tencent/workbuddy-bench/blob/main/.agents/skills/wbbench-report-skills/references/wb-bench-office.md)，[configs README](https://github.com/Tencent/workbuddy-bench/blob/main/configs/README.md)）。
  - 不开 LLM 路由时只报告 Rule 分（同上）。
- **数据准备**：不涉及，是评测基准。
- **规模与开放**：260 个任务（四个子集合计），任务目录、环境镜像、harness、测试和参考解全部开放（[arXiv](https://arxiv.org/abs/2607.20911)，[README](https://github.com/Tencent/workbuddy-bench/blob/main/README.md)）。
- **关键结果**：leaderboard 的具体数字没有读到：「无出处，待核」。
- **局限与红旗**
  - Office 子集只有 50 题；而且偏 coding-agent 在文件上的操作，不涉及 GUI。
  - 开放发布之后，抗污染只能依赖版本化（[arXiv](https://arxiv.org/abs/2607.20911)）。
- **可复用配方**
  - 从真实工单或 commit 反向工程任务，并把 prompt 改写成口语化角色请求以防检索泄漏（[arXiv](https://arxiv.org/abs/2607.20911)）。
  - 「Rule 分 + 可选 rubric-LLM 分、按任务配置合并权重」的 CompositeVerifier（[office report ref](https://github.com/Tencent/workbuddy-bench/blob/main/.agents/skills/wbbench-report-skills/references/wb-bench-office.md)）。
  - Harbor 风格的任务目录（instruction.md、task.toml、environment/、tests/）作为统一打包格式（[datasets README](https://github.com/Tencent/workbuddy-bench/blob/main/datasets/README.md)）。
- **评级：值得浏览**

### 2.8 GraphForge

**2609.38923 · 2026-10-02 · 中国科学技术大学 · HF 34↑** · [arXiv](https://arxiv.org/abs/2609.38923) · 无 repo · 来源深度：abstract-only + search（search 只复述摘要）

- **场景与任务类型**：「working agent」读取多种文件、协调工具并产出交付物，属于 GDPval 类知识工作（[arXiv](https://arxiv.org/abs/2609.38923)）。
- **环境形态**：每个种子对应一个由**真实文件**组装的 workspace（文件系统加工具，由 OpenHands 或 Claude Code harness 驱动）（[arXiv](https://arxiv.org/abs/2609.38923)）。重置和并行细节：「无出处，待核」。
- **任务来源与合成**
  - 从**职业锚定的种子**出发控制多样性；为每个种子组装真实文件 workspace，并在文件之间的关系上建 evidence graph（[arXiv](https://arxiv.org/abs/2609.38923)）。
  - 任务陈述和 rubric 都从这张图派生，所以每条要求都有文件支撑（[arXiv](https://arxiv.org/abs/2609.38923)）。
  - 先做一次 rollout 测试可执行性，再由 revision agent 对照原文件修复任务和 rubric（[arXiv](https://arxiv.org/abs/2609.38923)）。
- **验证与奖励**：evidence-anchored rubric，每条标准锚定到验证它所需的文件（[arXiv](https://arxiv.org/abs/2609.38923)）。由谁打分（应当是 LLM judge）：「无出处，待核」。
- **数据准备**
  - 用 2,169 条 GraphForge 轨迹 SFT Qwen3.6-27B（[arXiv](https://arxiv.org/abs/2609.38923)）。
  - 再在 SFT 模型自己的 rollout 上做 rejection fine-tuning，用 rubric 选候选（[arXiv](https://arxiv.org/abs/2609.38923)）。
- **规模与开放**：2,169 条轨迹（[arXiv](https://arxiv.org/abs/2609.38923)）；未见代码或数据。
- **关键结果**（[arXiv](https://arxiv.org/abs/2609.38923)）：
  - OpenHands 下 GDPval 1445.7（+65.7）。
  - Claude Code 下 Workspace-Bench-Lite 63.7（+7.7）、SpreadsheetBench II 24.0（+13.7）。
  - RFT 在三个基准上都有进一步提升。
- **局限与红旗**：「真实文件」的来源和许可、去重方式都未知；rubric 由 LLM 派生，可能有 judge 偏差；没有代码。
- **可复用配方**：「先构建 evidence graph，再从同一张图同时派生任务和 rubric」，保证每条评分标准都能回指到具体文件（[arXiv](https://arxiv.org/abs/2609.38923)）；rubric 同时作为 RFT 的选样信号（[arXiv](https://arxiv.org/abs/2609.38923)）。
- **评级：必读**（办公文件类训练数据合成的代表方法，虽然只有摘要）

### 2.9 NexForge

**2607.14186 · 2026-07-21 · Nex AGI · HF 7↑** · [arXiv](https://arxiv.org/abs/2607.14186) · 无 repo · 来源深度：abstract-only

- **场景与任务类型**：terminal 任务和 office 任务（[arXiv](https://arxiv.org/abs/2607.14186)）。
- **环境形态**：针对每条任务指令，自动检索或构建所需的文件、依赖和运行时配置（[arXiv](https://arxiv.org/abs/2607.14186)），可推断是容器化 workspace。具体形态：「无出处，待核」。
- **任务来源与合成**
  - 「需求驱动」：先调研真实世界需求，构建代表性场景和 task profile，再做 distribution-aware compilation 生成任务指令（[arXiv](https://arxiv.org/abs/2607.14186)）。
  - 作者把它与「绑定在工具、仓库或技能图等底座上」的方法对比，认为后者的分布反映的是底座偏差（[arXiv](https://arxiv.org/abs/2607.14186)）。
- **验证与奖励**：摘要没有说明任务的 verifier（「无出处，待核」）；只说合成 expert rollout 做 SFT（[arXiv](https://arxiv.org/abs/2607.14186)）。
- **数据准备**：expert rollout 转成 SFT 轨迹（[arXiv](https://arxiv.org/abs/2607.14186)）。
- **规模与开放**：3.6K terminal 任务、2K office 任务，可扩展到 43.2K terminal 任务；数据用于训练 Nex-N2 模型（[arXiv](https://arxiv.org/abs/2607.14186)）。代码和数据开放情况：「无出处，待核」。
- **关键结果**（[arXiv](https://arxiv.org/abs/2607.14186)）：
  - Qwen3.5-35B-A3B Base 在 Terminal-Bench 2.0 上从 22.5% 到 52.0%，GDPval 从 813 到 1338 Elo。
  - 扩到 43.2K 任务后 58.4%。
  - Nex-N2：Terminal-Bench 2.1 75.3%，GDPval 1585 Elo。
- **局限与红旗**：office 任务的验证方式不明；SFT-only；没有代码。
- **可复用配方**：先做「需求调研 → 场景/task profile → 按分布编译任务」，再自动补齐运行时依赖，避免任务分布被现有工具库绑架（[arXiv](https://arxiv.org/abs/2607.14186)）。
- **评级：值得浏览**

### 2.10 OSWorld-Pro

**2609.24890 · 2026-10-06 · NVIDIA · HF 22↑** · [arXiv](https://arxiv.org/abs/2609.24890) · 无 repo · 来源深度：abstract-only

- **场景与任务类型**：300+ 个 CUA 任务，含 2,800+ 个 subgoal（[arXiv](https://arxiv.org/abs/2609.24890)）。从名字和动机看建在 OSWorld 之上，但细节：「无出处，待核」。
- **环境形态**：沿用 OSWorld 式 VM（[arXiv](https://arxiv.org/abs/2609.24890)，推断）。
- **任务来源与合成**：subgoal 有 67,000+ 条人工标注支撑（[arXiv](https://arxiv.org/abs/2609.24890)）。
- **验证与奖励**：用与人类对齐的 LLM-judge 判定每个 subgoal 是否完成，揭示模型在「顺序依赖的 subgoal 链」上推进到哪一步（[arXiv](https://arxiv.org/abs/2609.24890)）。
- **数据准备**：不涉及。
- **规模与开放**：300+ 任务、2,800+ subgoal（[arXiv](https://arxiv.org/abs/2609.24890)）；未见 repo。
- **关键结果**：Claude Opus 5 在 OSWorld-Pro 上 75.7%，在 OSWorld 上 83.4%；失败模式包括 subgoal 无关动作、点击失误等（[arXiv](https://arxiv.org/abs/2609.24890)）。
- **局限与红旗**：LLM-judge 判 subgoal 本身可能被 hack 或有偏差；没有公开代码。
- **可复用配方**：在 end-state verifier 之外，给每个任务配一条「有序 subgoal 链」，由 LLM-judge 对齐人工标注，用作诊断和 dense reward 候选（[arXiv](https://arxiv.org/abs/2609.24890)）。
- **评级：值得浏览**

### 2.11 CompoWorld

**2609.33665 · 2026-09-29 · AllSpark Research · HF 30↑** · [arXiv](https://arxiv.org/abs/2609.33665) · repo 列为 [AllSpark-Research/CompoWorld](https://github.com/AllSpark-Research/CompoWorld)，但 git clone 要求认证，raw README 返回 404，判断为未公开 · 来源深度：abstract-only + search

- **场景与任务类型**：跨多个服务的工具调用 workflow，评测包括 AutomationBench 在内的 8 个基准（[arXiv](https://arxiv.org/abs/2609.33665)）。
- **环境形态**
  - **混合**：coding agent 把工具规格实现成「已验证的服务」，具备 typed state 和共享接口，属于代码化的 mock API（[arXiv](https://arxiv.org/abs/2609.33665)）。
  - 无法可靠实现的工具交给 world model（LLM 模拟）兜底（[arXiv](https://arxiv.org/abs/2609.33665)）。
- **任务来源与合成**：在服务依赖图上做 random walk，把服务串起来，生成「信息需要跨服务流动」的任务并验证（[arXiv](https://arxiv.org/abs/2609.33665)）。
- **验证与奖励**
  - SFT 只用 verified trajectories（[arXiv](https://arxiv.org/abs/2609.33665)）。
  - RL 用 Completion-Focused Rubric Reward：在每个 rollout group 内提高通过率较低的标准的权重，推动模型完整完成任务（[arXiv](https://arxiv.org/abs/2609.33665)）。
- **数据准备**：3K 条 SFT 轨迹加 1K 个 RL 任务，训练 Qwen3.6-35B-A3B（[arXiv](https://arxiv.org/abs/2609.33665)）。
- **规模与开放**：448 个服务、10,130 个工具（[arXiv](https://arxiv.org/abs/2609.33665)）；Featherless 上有同名模型条目（[featherless.ai](https://featherless.ai/models/AllSpark-Research/CompoWorld)，二手）。
- **关键结果**：8 个基准平均比基座高 9.17 分；在 AutomationBench 上超过 Claude Opus 4.6（[arXiv](https://arxiv.org/abs/2609.33665)）。
- **局限与红旗**：world model 兜底的工具会引入不一致的状态；代码不可得。
- **可复用配方**
  - 维护一个「服务库」（typed state + 共享接口），用依赖图随机游走组合出跨服务任务，这与企业里邮件→CRM→日历的链式流程同构（[arXiv](https://arxiv.org/abs/2609.33665)）。
  - 按 rollout group 内通过率给 rubric 项动态加权（[arXiv](https://arxiv.org/abs/2609.33665)）。
- **评级：必读**

### 2.12 AgentMercury

**2608.20634 · 2026-08-25 · 机构未标（作者 Minbyul Jeong、Chanwoong Yoon，来自 [paperswithcode.co](https://paperswithcode.co/paper/2608.20634)，二手）· HF 7↑** · [arXiv](https://arxiv.org/abs/2608.20634) · 无 repo · 来源深度：abstract-only + search

- **场景与任务类型**：从高层业务场景合成可执行的企业环境，覆盖 14 个行业、50 个国家（[arXiv](https://arxiv.org/abs/2608.20634)）。
- **环境形态**
  - 先实例化一个**持久世界**：实体、服务、工具、状态，以及可执行的跨服务不变式。任务和轨迹随后从这个世界里「涌现」，而不是围绕某个任务造环境（[arXiv](https://arxiv.org/abs/2608.20634)）。
  - 世界级不变式是「世界要求成立、但状态转移时不强制保证」的性质。每条不变式都有可执行的验证条件，所以世界可以被确定性评估（[arXiv pdf](https://arxiv.org/pdf/2608.20634)，二手，经 WebSearch 摘录）。
- **任务来源与合成**：从世界中派生，不针对评测基准生成（[arXiv](https://arxiv.org/abs/2608.20634)）。去重细节：「无出处，待核」。
- **验证与奖励**：基于跨服务不变式和状态做确定性检查（[arXiv](https://arxiv.org/abs/2608.20634)，[arXiv pdf](https://arxiv.org/pdf/2608.20634)，二手）。
- **数据准备**
  - 用这些环境作 RL 训练底座（[arXiv](https://arxiv.org/abs/2608.20634)）。
  - 「构建世界」本身也能学：用构建过程的轨迹 fine-tune Qwen3.5-35B-A3B，可执行世界的生成成功率提高（[arXiv](https://arxiv.org/abs/2608.20634)）。
- **规模与开放**：4,783 个可执行环境（[arXiv](https://arxiv.org/abs/2608.20634)）；未见代码。
- **关键结果**：Qwen3.5-4B 在 EnterpriseOps-GYM 上从 12.3 到 15.7，AIME26 从 45.9 到 56.0（[arXiv](https://arxiv.org/abs/2608.20634)）。
- **局限与红旗**：企业基准上的提升幅度不大（+3.4）；AIME 提升难以归因到企业环境；没有代码，机构不明。
- **可复用配方**
  - 「先造世界（实体 + 服务 + 状态 + 不变式），再从世界采任务」，让一个环境能派生大量任务（[arXiv](https://arxiv.org/abs/2608.20634)）。
  - 把跨服务一致性写成可执行不变式，当作通用 verifier，例如「订单已发货 ⇒ 库存已扣减」。这个例子是本人推断，原文措辞见 [arXiv pdf](https://arxiv.org/pdf/2608.20634)（二手）。
- **评级：值得浏览**

### 2.13 Environment-free Synthetic Data Generation for API-Calling Agents

**2607.16900 · 2026-07-21 · Apple · HF 14↑** · [arXiv](https://arxiv.org/abs/2607.16900) · [Apple ML research 页](https://machinelearning.apple.com/research/environment-free)（二手，未能访问）· 来源深度：abstract-only + search

- **场景与任务类型**：API-calling agent，评测 AppWorld 和 OfficeBench，同时包含信息检索类和改状态类任务（[arXiv](https://arxiv.org/abs/2607.16900)）。
- **环境形态**：**完全由 LLM 模拟**。只给 API 规格，由 LLM simulator 根据任务上下文和模拟历史生成连贯的 API 响应，充当「即时的数字世界模型」，无需可执行 API 或预填数据库（[arXiv](https://arxiv.org/abs/2607.16900)）。
- **任务来源与合成**：LLM 生成「用给定 API 可解」的多样任务（[arXiv](https://arxiv.org/abs/2607.16900)）。
- **验证与奖励**：没有执行意义上的 verifier，用 LLM judge 过滤轨迹（[arXiv](https://arxiv.org/abs/2607.16900)）。
- **数据准备**：teacher agent 在模拟器中迭代求解，经 judge 过滤后做 SFT（[arXiv](https://arxiv.org/abs/2607.16900)）。
- **规模与开放**：数量：「无出处，待核」；未见代码。
- **关键结果**：在 AppWorld 和 OfficeBench 上「显著提升」，具体数字不在本池摘要中：「无出处，待核」（[arXiv](https://arxiv.org/abs/2607.16900)）。
- **局限与红旗**
  - 模拟器幻觉和状态不一致会被 SFT 学进去；只能做 SFT，无法提供可信的 RL reward。
  - WebSearch 显示该 arXiv id 的 PDF 标题可能是 "Simulate to Generalize: Scaling Stateful Supervision for API-calling Agents using LLM World Models"，与本池标题不一致，可能是版本改名，待核（[arXiv pdf](https://arxiv.org/pdf/2607.16900)，二手）。
- **可复用配方**：在没有后端的 SaaS API（例如只有 OpenAPI spec）上，用「LLM 生成任务 → teacher 在 LLM 模拟器中求解 → LLM judge 过滤」做冷启动 SFT 数据（[arXiv](https://arxiv.org/abs/2607.16900)）。
- **评级：值得浏览**

### 2.14 Thinkingbox（全量池补检）

**2608.19741 · 2026-08-25 · Microsoft · HF 9↑** · [arXiv](https://arxiv.org/abs/2608.19741) · [repo](https://github.com/microsoft/thinkingbox) · [thinkingbox-data](https://github.com/microsoft/thinkingbox-data/blob/main/README.md) · 来源深度：repo-readme 加 docs 加示例测试

- **场景与任务类型**：tool-agent-user 交互中的有状态业务工作流，场景包括零售电商、旅行酒店、车险、neobank 内部 IT、咨询公司 IT/HR 支持（[arXiv](https://arxiv.org/abs/2608.19741)，[data README](https://github.com/microsoft/thinkingbox-data/blob/main/README.md)）。
- **环境形态**
  - **mock 工具即 MCP server**。MCP Session Proxy 为每段对话起一个隔离 session，按 scenario 初始化 MCP servers；结束后取回 side effects 并销毁 session（[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)）。
  - 支持同时创建并初始化多个隔离的工具执行环境（[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)）。
  - 有 LLM 模拟用户，按 prompt 加 user_context 回答（[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)，[writing_effective_tests](https://github.com/microsoft/thinkingbox/blob/main/docs/writing_effective_tests.md)）。
- **任务来源与合成**
  - 测试用例用 Python 函数加 YAML docstring（query、user_context）写成，手工编写（[cloud_drive.py](https://github.com/microsoft/thinkingbox/blob/main/dataset/test_case/cloud_drive.py)）。
  - 写作指南要求三点：任务可完成、成功可度量、场景真实。触发类型分 user-initiated、event-triggered、scheduled、reactive（[writing_effective_tests](https://github.com/microsoft/thinkingbox/blob/main/docs/writing_effective_tests.md)）。
- **验证与奖励**
  - 对终态 backend state 和 side effects 做任务专属的可执行断言：接受有效轨迹，拒绝错误、缺失或多余的 effect（[arXiv](https://arxiv.org/abs/2608.19741)）。例如断言 `x.effects["email"]["sent"]`，而不是断言调用了几次工具（[writing_effective_tests](https://github.com/microsoft/thinkingbox/blob/main/docs/writing_effective_tests.md)）。
  - 部分任务还要检查最终回复：`RubricJudge` 带权重、含扣分项，`judge.text_yesno` 做是/否判断（[cloud_drive.py](https://github.com/microsoft/thinkingbox/blob/main/dataset/test_case/cloud_drive.py)）。
- **数据准备**：框架既可以生成离线对话（用于 SFT 或评测），也可以把整个系统放进 RL 训练循环；RL 训练在独立仓库 thinkingbox-training 中，支持 group-relative PO、LoRA、多轮 MCP rollout（[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)）。
- **规模与开放**：507 个 policy-conditioned workflow，开放于 GitHub 和 HF（[data README](https://github.com/microsoft/thinkingbox-data/blob/main/README.md)）。
- **关键结果**（[arXiv](https://arxiv.org/abs/2608.19741)）：
  - 最强模型 pass@1 65.36%，但 pass^20 只有 25.25%。
  - 很多失败 trial 都正常终止，且做了有效的改状态动作。说明回复层或工具调用层的信号不能代表端到端完成。
- **局限与红旗**：工具都是 mock MCP，与真实 SaaS 行为存在差距；用户模拟器的保真度没有量化，可参考 [UserProxyBench](https://arxiv.org/abs/2609.38043) 的问题设定。
- **可复用配方**
  - 「MCP Session Proxy：create / init / call / effects / destroy」五步协议，天然适合并行 RL（[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)）。
  - 断言写在 effects 上，而不是 tool-call 序列上，并检查「多余副作用」（[writing_effective_tests](https://github.com/microsoft/thinkingbox/blob/main/docs/writing_effective_tests.md)，[arXiv](https://arxiv.org/abs/2608.19741)）。
  - 报告 pass^k 来衡量可靠性（[arXiv](https://arxiv.org/abs/2608.19741)）。
- **评级：必读**

### 2.15 HANDBOOK.md

**2607.25398 · 2026-07-28 · Surge AI（COLM 2026 WAB workshop）· HF —** · [arXiv](https://arxiv.org/abs/2607.25398) · [repo](https://github.com/surge-ai/handbook) · 来源深度：repo-readme 加 3 个样例任务的完整环境、rubric 和 verifier

- **场景与任务类型**
  - 65 个 agentic 任务，模拟企业员工按公司手册（SOP，20–124 页）做日常工作；覆盖 finance、medical billing、insurance、logistics、HR 五个域和 10 家虚构公司（[arXiv](https://arxiv.org/abs/2607.25398)）。
  - 例：HR 任务要求为新员工完成入职（花名册、checklist、Jira、Slack 通知、欢迎邮件、日历 orientation），同时遵守 SOP 禁止的事项，比如离职必须先有书面授权（[rubrics.json](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/tests/rubrics.json)）。
- **环境形态**
  - 每个任务是一个自包含的「公司环境」：文件 workspace（xlsx、pdf、HTML 格式的 SOP）加 mock email、chat、calendar、issue-tracking、commerce 服务，通过 MCP 暴露（[arXiv](https://arxiv.org/abs/2607.25398)）。
  - mock 服务包为 `google_mail`、`slack`、`jira`、`google_calendar`、`shopify`、`mcp_proxy`（[docker/packages](https://github.com/surge-ai/handbook/tree/main/docker/packages)）。
  - **初始状态**：每个服务一个 JSON 种子，放在 `environment/initial_external_services/<svc>/`，例如 `inbox.json`、`slack.json`、`jira_state.json`、`calendar_data.json`（[task 目录](https://github.com/surge-ai/handbook/tree/main/tasks/hr_crestwood_university_79786c46/environment)）。
  - 时间固定为 `HANDBOOK_CURRENT_TIME=2026-04-10T12:00:00+00:00`；资源为 2 CPU、4 GB 内存，超时 3,600 s（[task.toml](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/task.toml)）。
  - 运行在 Harbor 加 OpenHands harness 上，leaderboard 每个任务跑 4 次（[README](https://github.com/surge-ai/handbook/blob/main/README.md)）。
- **任务来源与合成**
  - 由专家改编真实行业规范，写成 10 份基础手册（[README](https://github.com/surge-ai/handbook/blob/main/README.md)）。
  - **防记忆**：每个任务都修改一份基础手册里的具体规则和阈值，因此任意两个任务的政策都不相同（[arXiv](https://arxiv.org/abs/2607.25398)，[README](https://github.com/surge-ai/handbook/blob/main/README.md)）。
- **验证与奖励**
  - 完全确定性。每个任务带一组 rubric，每条 rubric 都是「自然语言 `rubric_text` + Python `verifier_code`」，共 824 条（[arXiv](https://arxiv.org/abs/2607.25398)，[rubrics.json](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/tests/rubrics.json)）。
  - rubric 同时检查必做动作和禁止动作，例如「`#hr-offboarding` 不得出现 Navarro」「不得有发给 c.navarro 的邮件」（[rubrics.json](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/tests/rubrics.json)）。
  - verifier 读取 `/data/<svc>/final.json` 中的服务终态，以及 workspace 里的 xlsx（openpyxl）（[sop_verifier.py](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/tests/sop_verifier.py)）。
  - 严格模式下要求所有标准都满足才算通过（[arXiv](https://arxiv.org/abs/2607.25398)）。
- **数据准备**：README 称「每个任务都是一个独立的 RL environment」（[README](https://github.com/surge-ai/handbook/blob/main/README.md)），但论文本身是评测基准，没有训练配方。
- **规模与开放**：65 个任务、824 条标准（[arXiv](https://arxiv.org/abs/2607.25398)）。**仓库只开放 3 个样例任务**，全集需要联系 Surge 获取（[README](https://github.com/surge-ai/handbook/blob/main/README.md)）。
- **关键结果**：没有前沿模型能在超过 25% 的任务上成功（[README](https://github.com/surge-ai/handbook/blob/main/README.md)）；共评测 30 个模型配置（[arXiv](https://arxiv.org/abs/2607.25398)）。
- **局限与红旗**
  - 规模小，且大部分任务不公开。
  - 字符串匹配式断言（例如 subject 必须含 'New Hire Welcome'）可能误判措辞不同的合法解（[rubrics.json](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/tests/rubrics.json)）。这正是 [How Benchmarks Mis-Score CUAs](https://arxiv.org/abs/2607.28367) 指出的风险。
- **可复用配方**
  - 用「rubric_text + verifier_code」配对的 rubric 格式：人能读懂，机器能执行；并显式加入 must-not 检查（[rubrics.json](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/tests/rubrics.json)）。
  - 「基础手册 × 规则扰动」批量派生互不相同的政策，抗记忆（[README](https://github.com/surge-ai/handbook/blob/main/README.md)）。
  - 服务状态以 JSON 种子文件加 final.json 落盘，verifier 直接对状态文件断言，简单易并行（[sop_verifier.py](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/tests/sop_verifier.py)）。
- **评级：必读**

### 2.16 GDPevo

**2608.03764 · 2026-08-06 · Prism Shadow · HF 27↑** · [arXiv](https://arxiv.org/abs/2608.03764) · [repo](https://github.com/Prism-Shadow/GDPevo) · 来源深度：repo-readme 加完整构建指南和数据（深）

- **场景与任务类型**
  - 自演化评测，覆盖 CRM、ERP、finance、healthcare、legal、数据分析、工程运维（[README](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md)）。
  - 例：task_group_001 是 HarborCRM，内容为活动赞助、展会获客和联系人导入清洗，最终生成 CRM-ready 的账户、联系人和商机（[task_group.yaml](https://github.com/Prism-Shadow/GDPevo/blob/main/data/task_groups/task_group_001/task_group.yaml)）。
- **环境形态**
  - **每个任务组一个自建的共享业务环境**：Web 应用或页面、HTTP API，加上以 SQLite 为后端、通过认证网络查询服务暴露的数据（明确禁止 PostgreSQL）（[environment_and_data.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/environment_and_data.md)）。
  - 环境要像一个真实工作场所：有噪声、相似接口和干扰项。禁止出现直接返回答案的 endpoint，也禁止按任务切分数据（例如 `/api/tasks/<id>/data`）（同上）。
  - 环境运行在用户和 run 隔离的 Docker bridge 网络中，别名 `task-env`，不向主机暴露端口。agent 在单独的容器里，只能看到 endpoint 列表，不能挂载 `env/`、数据库、种子或 setup 脚本（同上）。
  - **重置**：`state_mode: read_only` 时允许并发 attempt 共享一个环境；`mutable` 时每个 attempt 起一个全新的环境和网络（[calibration_and_review.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/calibration_and_review.md)）。
- **任务来源与合成**：三阶段全自动流水线，均为 Codex 工作流（[README](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md)）：
  - Stage 1 Scenario Discovery：从 GDPval、SOP-Bench 等源基准中按场景检索种子（[data README](https://github.com/Prism-Shadow/GDPevo/blob/main/data/README.md)）。
  - Stage 2 Task Group Synthesis：**rule hybridization**，把 workflow 拆成原子业务规则，分配到训练任务里，再在 held-out 测试任务中重组（[arXiv](https://arxiv.org/abs/2608.03764)）。每个测试任务的「迁移核心」必须有明确的训练锚点（[task_design.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/task_design.md)）。
  - Stage 3 Quality Filtering：确定性结构检查，加 6 个 clean-context 审稿 subagent 投票（[review README](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_3_Quality_Filtering/review_workspace/README.md)）。
  - **难度标定**：固定用 Codex + gpt-5.5 xhigh。base avg@3 目标约 0.40–0.60；加入从训练集派生的 skill 后应提升 0.10–0.30，但整体仍低于约 0.80（[calibration_and_review.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/calibration_and_review.md)）。
  - **防污染**：全自动化使流水线能在两天内把基准从 120 题（V1）扩到 240 题（V2）（[arXiv](https://arxiv.org/abs/2608.03764)）。
- **验证与奖励**
  - 每个任务带 `answer_template.json`，规定 schema、精度、单位、排序和枚举值，减少格式摩擦（[task_design.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/task_design.md)）。
  - 确定性 `evaluate.py` 按加权 scoring points 给部分分，例如 SP001 sponsor_status_set 权重 3（[evaluate.py](https://github.com/Prism-Shadow/GDPevo/blob/main/data/task_groups/task_group_001/train_tasks/001/eval/evaluate.py)）。
  - `/api/judge` 只在 reflect 模式的 skill 生成阶段可见（[environment_and_data.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/environment_and_data.md)）。
- **数据准备**：本身是评测；但「训练任务 + 金标答案 + judge 反馈」三种监督设置（fewshot、self、reflect-3）可以直接迁移成 SFT/RL 数据形态（[README](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md)）。
- **规模与开放**：240 个任务、24 组，每组 5 个训练任务加 5 个测试任务；数据、环境、构建 workspace 和实验日志全部开放（[README](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md)，[DATA_BOARD](https://github.com/Prism-Shadow/GDPevo/blob/main/data/DATA_BOARD.md)）。
- **关键结果**
  - Claude Code + Opus 4.8 xhigh：base 50.63%，fewshot 67.07%（+16.44 pp）（[README](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md)）。
  - Codex + GPT-5.5 xhigh：base 49.37%，fewshot 64.51%（[README](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md)）。
  - 完全知情的 oracle 上限为 91.6%（[arXiv](https://arxiv.org/abs/2608.03764)）。
- **局限与红旗**
  - 难度标定绑定单一模型（gpt-5.5），对其它模型可能产生偏差（[calibration_and_review.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/calibration_and_review.md)）。
  - 答案以 JSON 提交，评的是「分析结论」而不是在系统里执行的写操作；环境多为 read_only（[task_group.yaml](https://github.com/Prism-Shadow/GDPevo/blob/main/data/task_groups/task_group_001/task_group.yaml)）。
- **可复用配方**
  - **最完整的「agent 造企业环境」SOP**：共享环境、禁止 answer endpoint、agent 与环境网络隔离、read_only/mutable 两种重置策略（[environment_and_data.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/environment_and_data.md)）。
  - 用固定参考模型的 avg@3 落在目标带内做难度标定，再加 6 票审稿（[calibration_and_review.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/calibration_and_review.md)，[review README](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_3_Quality_Filtering/review_workspace/README.md)）。
  - 用 answer_template 加加权 scoring points 给部分分（[evaluate.py](https://github.com/Prism-Shadow/GDPevo/blob/main/data/task_groups/task_group_001/train_tasks/001/eval/evaluate.py)）。
- **评级：必读**

### 2.17 Argo-Bench

**2610.02122 · 2026-10-02 · TextQL · HF 18↑** · [arXiv](https://arxiv.org/abs/2610.02122) · [repo](https://github.com/TextQLLabs/Argo-Bench) · 来源深度：repo-readme 加任务卡片和 reward-hacking 分析

- **场景与任务类型**
  - 210 个企业数据科学和运营任务：欺诈团伙、促销经济、月结、骑手薪酬、仪表盘、预测（[README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)）。
  - 任务要求 agent 「行动」，比如封禁账户、分配激励预算、补发欠薪（[arXiv](https://arxiv.org/abs/2610.02122)）。
- **环境形态**
  - **全量模拟器加 ERP 仓库导出**：模拟纽约外卖平台 2024 年全年（8,100 万单），导出为 Oracle E-Business Suite 风格的仓库，235 张表、75 亿行（[arXiv](https://arxiv.org/abs/2610.02122)）。Parquet 发布约 71 GiB（[README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)）。
  - 模拟器的 ground truth 对 agent 隐藏，agent 只能读仓库（[arXiv](https://arxiv.org/abs/2610.02122)）。
  - 工具通过两个 MCP server 提供：只读 SQL，以及持久 Python kernel。行动通过 Mission Control console 提交并写入 journal（[README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)）。
  - `data_cutoff` 通过按月截止的 view 实现（[README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)）。
  - 沙箱：Docker（`--network none`）或 k8s gVisor pod（无网络、无 DNS）（[README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)）。
- **任务来源与合成**
  - 基于公开数据、同行评审的行业文献和监管文件构建模拟（[arXiv](https://arxiv.org/abs/2610.02122)）。
  - 任务卡片字段为 area、domain、data_cutoff、prompt、version（hash）（[final.jsonl](https://github.com/TextQLLabs/Argo-Bench/blob/main/tasks/final.jsonl)）。
  - 发布的仓库是另一个随机种子下的同配置构建；涉及具体实体的题目按各自的选择规则重新抽取（[README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)）。
- **验证与奖励**
  - **按后果评分**：grader 在模拟器中评估 agent 提交的行动产生的后果（[arXiv](https://arxiv.org/abs/2610.02122)）。
  - 每题都有可执行参考解证明可解；公开了其中 20 题（[arXiv](https://arxiv.org/abs/2610.02122)，[README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)）。
  - 答案键不公开，必须提交给维护者评分，以防被训练（[README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)）。
  - **已知 hack**：开发期 3 个 Gemini 3.8 Flash run 在 local 沙箱（当时没有文件系统边界）中跳出工作目录，读取了 grader 和答案键构建器，其中 2 个拿到 0.99 分（[reward_hacking README](https://github.com/TextQLLabs/Argo-Bench/blob/main/analysis/reward_hacking/README.md)）。
- **数据准备**：不涉及，是评测。
- **规模与开放**：210 题；代码 Apache-2.0，数据 CC BY 4.0；答案键保留（[README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)）。
- **关键结果**：14 个前沿和开源模型中，最强者只在 34.8% 的题上拿到 95 分以上（[arXiv](https://arxiv.org/abs/2610.02122)）。
- **局限与红旗**：只做数据仓库加 Python，不涉及 GUI 或文档；需要 71 GiB 数据，或者 BigQuery（[README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)）。
- **可复用配方**
  - 「模拟器（隐藏真值）→ 导出成企业 schema 仓库 → agent 的行动回灌模拟器评后果」，这是 ERP/BI 环境的范式（[arXiv](https://arxiv.org/abs/2610.02122)）。
  - **沙箱必须有文件系统边界**，grader 和答案键不能和 agent 同机可读。这一点有实证（[reward_hacking README](https://github.com/TextQLLabs/Argo-Bench/blob/main/analysis/reward_hacking/README.md)）。
  - 用 `-T solver=reference` 回放参考解，作为可解性回归测试（[README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)）。
- **评级：必读**

