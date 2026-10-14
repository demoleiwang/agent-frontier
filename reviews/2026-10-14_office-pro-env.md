# 办公与专业领域 agent 的环境构建 · 全景（2026-07 → 2026-10）

> 关注点：环境怎么建（真实应用、mock、模拟器、真机、仪器），状态与基础设施，任务合成，验证与奖励，数据准备，隔离与安全。
> 下半年研究提案见 [research-proposal](2026-10-14_research-proposal.md)。
> 逐篇卡片：[办公 / 企业（17 篇）](2026-10-14_office-pro-env/office.md) · [专业领域（18 篇）](2026-10-14_office-pro-env/professional.md) · [环境与数据构建方法（21 篇）](2026-10-14_office-pro-env/methods.md) · [前沿 lab 与产业实践（21 张卡片）](2026-10-14_office-pro-env/labs.md)。
> 证据规则：每条论断就地附原始出处。arXiv abs 链接表示只读到摘要；GitHub 文件链接表示读了仓库 README、文档或代码（只读，未执行）。二手出处标“二手”。所有数字均为作者或厂商自报。

## 0. 覆盖范围与证据深度

- **论文池**：2026-07-01 至 10-13，共 5,210 篇（HF Daily Papers 与 arXiv cs.AI/CL，经 GitHub 镜像获取）。按新增的 office-agent、professional-agent、env-construction 三个 topic 导出候选：70 + 70 + 90 篇，由 4 个 agent 逐篇按摘要筛选，并从全量池补漏。
- **精读**：办公 17 篇、专业领域 18 篇、方法 21 篇，另有 lab 与产业实践 21 张卡片。
- **证据深度**：arxiv.org 与 huggingface.co 在本环境不可达，所以论文以“摘要 + 官方仓库（README、文档、任务文件、verifier 代码）”为主。只有少数仓库自带论文 PDF：[Business Arena](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)、[CADWorld](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)、[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)、[Kimi K3](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)。
- **读代码时的额外发现**：仓库代码有时与摘要不一致，例如 [Echoverse 判分容忍多余改动](https://github.com/microsoft/Echoverse/blob/main/harness/prompts.py)、[Trace2Env 的结果产生于一次 bug 修复之前](https://github.com/ruyue0001/trace2env/blob/main/REPRODUCING.md)。这类差异在卡片里逐条标出。

---

## 1. 一页结论

1. **办公 / 企业环境的主流形态是“mock SaaS + 可注入、可 diff 的状态 API”，真实商业 SaaS 基本缺席。**
   - 腾讯 [CUA-Gym-Hub](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md) 用 98 个 mock Web 应用和统一的 set/reset/diff 接口；[HANDBOOK](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/tests/rubrics.json) 的邮件、Slack、Jira、日历走 MCP；[Thinkingbox](https://github.com/microsoft/thinkingbox/blob/main/README.md) 用 MCP mock 加会话代理；[GDPevo](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/environment_and_data.md) 自建 Web/API 加 SQLite 的业务系统。
   - 精读的 17 篇办公论文里没有一篇在真实商业 SaaS 租户上训练或评测（[办公卡片汇总](2026-10-14_office-pro-env/office.md) 之依据：[UI-Mate](https://arxiv.org/abs/2608.15930)、[GDPevo](https://arxiv.org/abs/2608.03764)、[Thinkingbox](https://arxiv.org/abs/2608.19741)）。唯一的“真实 SaaS”实践来自厂商合作：[OpenAI × Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad) 在伙伴托管的产品副本里训练。
2. **专业领域则相反：真实专业软件已经能装进 VM，瓶颈是商业许可证。**
   - [EngiWorld](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md) 覆盖 26 款工程软件（含 SolidWorks、Abaqus、Revit），共 1,301 题。
   - [OSWorld-Science](https://github.com/DiscoAILab/OSWorld-Science/blob/main/configs/snapshots.yaml) 为 Mnova、SAS、Ansys 各配了一套许可证处理方式：用户自带 licence 注入、改用网页版、只发重建 recipe。
   - [SimuVerity](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/README.md) 要求用户自有 MATLAB/Simulink。
3. **环境本身越来越多由 coding agent 生成，并配“运行时自检”的门槛。** 每篇的门槛各不相同：
   - [SoftwareGym](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/prompt/Coderprompt.json) 合成原生应用，并强制每个应用实现 dump / reset / seed-state 接口。
   - [ScaleCUA / VeriGen](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/agent_feasibility_verification.md) 由 coding agent 在运行中的 VM 里写 evaluator，并要求“初始状态不能通过、解完必须通过”。
   - [GDPevo](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/calibration_and_review.md) 用参考模型的 avg@3 标定难度。
   - [Echoverse](https://github.com/microsoft/Echoverse/blob/main/README.md) 把规格编译成有状态应用，按数据库 diff 判分。
4. **最可信的判分是“落在应用或领域引擎自己的状态上”，LLM judge 只负责开放文本。**
   - 办公侧：读 state diff（[CUA-Gym-Hub](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）、比数据库前后差异（[Echoverse](https://github.com/microsoft/Echoverse/blob/main/README.md)）、比终态哈希与 gold 动作重放的结果（[NeMo Gym indian_banking](https://github.com/NVIDIA-NeMo/Gym/blob/main/resources_servers/indian_banking/README.md)）。
   - 专业侧：用几何内核做容差断言（[EngiWorld eval.py](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/eval.py)）、重跑物理用例（[ScienceIDE](https://github.com/aitofound/ScienceIDE/blob/main/README.md)）、多工况原生仿真（[SimuVerity](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/README.md)）、在模拟器里结算业务后果（[Argo-Bench](https://arxiv.org/abs/2610.02122)）。
   - VLM judge 普遍偏宽松（[OSReward](https://arxiv.org/abs/2607.28609)）。
5. **rubric 收敛为“每条可执行、有部分分、有禁止项”的结构。**
   - [HANDBOOK](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/tests/rubrics.json) 每条 rubric 由自然语言描述和 verifier 代码配对，包含禁止动作检查。
   - [OmegaUse-OfficeVal](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md) 先过交付物门槛，再逐条加减分。
   - [MiMo](https://github.com/XiaomiMiMo/verl/tree/mimo-oss) 的每条 rubric 标注判法（规则或 LLM）、权重、是否门槛。
   - [DAYJOB](https://arxiv.org/abs/2610.01306) 每题配几十条专家 binary 条目。
   - 副作用检查标准尚不统一：[Echoverse](https://github.com/microsoft/Echoverse/blob/main/harness/prompts.py) 容忍多余改动，[Thinkingbox](https://arxiv.org/abs/2608.19741) 则拒绝多余副作用。
6. **长程任务靠“锚定 + 组合 + 链式”合成，难度靠前沿模型通过率标定。** 锚点包括：
   - 真实文件或证据图（[GraphForge](https://arxiv.org/abs/2609.38923)）
   - 原子业务规则的拆分与重组（[GDPevo](https://arxiv.org/abs/2608.03764)）
   - 服务依赖图上的随机游走（[CompoWorld](https://arxiv.org/abs/2609.33665)）
   - 阶段终态的链式串接（[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）
   - 跨多日、多应用的“活环境”事件流（[Kimi K3](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）
   - 递归扩展，并在每轮用新沙箱验证（[RST](https://arxiv.org/abs/2608.05466)）
7. **隔离不到位，reward 就会被 hack，而且已有实证。**
   - [Argo-Bench](https://github.com/TextQLLabs/Argo-Bench/blob/main/analysis/reward_hacking/README.md) 开发期有 run 读到 grader 和答案键，拿到 0.99 分。
   - [MiMo 开源任务](https://digg.com/ai/wo6cdxwj)约 2/3 可从 git 历史拿到答案（Vals AI，二手）。
   - [Anthropic](https://www.anthropic.com/research/investigating-unintended-model-actions) 有一例：练习副本加载失败后，agent 提交了真实的政府表单。

---

## 2. 环境形态怎么选

| 形态 | 代表 | 适用 | 状态 / 重置 | 判分 | 主要风险 |
|---|---|---|---|---|---|
| 伙伴托管的真实 SaaS 副本 | [OpenAI × Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad) | 高价值、稀缺的企业工作流 | 由伙伴托管（细节未公开） | 11 个工作流，每个 8–50 条 rubric | 规模小、依赖合作方；只能看到 rubric 部分得分 |
| VM 中的真实桌面 / 专业软件 | [OSWorld-Science](https://github.com/DiscoAILab/OSWorld-Science/blob/main/docs/user_guide/adding-a-task.md)、[EngiWorld](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)、[ScaleCUA](https://github.com/THUDM/SCALE-CUA/blob/main/README.md) | 办公套件、科学和工程软件 | VM 快照 | 可执行 evaluator，领域引擎重算 | 商业许可证；VM 成本 |
| 打包的真实应用 / 裸金属设备 | [Qwen-CUA（Gym-Anything、30 台 Mac mini）](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf) | 补充交互保真度与长尾覆盖 | 镜像 / 设备重置 | 状态式 RLVR | 并发低、运维重 |
| 带状态 API 的 mock SaaS | [CUA-Gym-Hub](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)、[HANDBOOK](https://github.com/surge-ai/handbook/blob/main/README.md)、[Thinkingbox](https://github.com/microsoft/thinkingbox/blob/main/README.md)、[Kimi K3 的 mock Gmail/Notion/Slack](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf) | 规模化 RL 的主力 | set / reset / diff，按会话隔离 | state diff 加 rubric | 保真度不足；状态被 agent 读取 |
| 由 agent 合成的应用 | [SoftwareGym](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/prompt/Coderprompt.json)、[Echoverse](https://github.com/microsoft/Echoverse/blob/main/README.md)、[GDPevo](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md) | 覆盖面扩展 | 实现强制的 dump / reset / seed 接口 | 数据库 diff 与代码 verifier | 浅环境反而会拉低真实站点上的成绩（[Echoverse](https://arxiv.org/abs/2607.28074)） |
| 从 trace 或日志重建的环境替身 | [Trace2Env](https://github.com/ruyue0001/trace2env/blob/main/docs/RUNTIME_HARNESS.md)、[Terminal-Universe](https://arxiv.org/abs/2609.04148) | 无法自建部署的内部系统 | 显式 worldbook 状态加不变量 | 规则校验加回放晋升门 | 状态漂移；需要定义“回放到真实环境是否成立”的一致性指标 |
| 纯 LLM 模拟 | [Apple env-free](https://arxiv.org/abs/2607.16900)、[EnvACE](https://arxiv.org/abs/2608.06197) | SFT 冷启动数据 | 无显式状态 | LLM judge | 不宜作为 RL 奖励源（[EnvACE reward](https://github.com/Within-yao/EnvACE/blob/main/agent_system/environments/env_package/checklist/checklist_reward.py)） |
| 视觉世界模型 | [AutoGUIWorld](https://github.com/ImYangC7/AutoGUIWorld/blob/main/README.md) | 零部署合成 GUI 观测 | 无 | 无执行验证 | 轨迹从不在真实环境执行 |
| 物理仪器 / 真实设备 | [Anthropic MHS](https://www.anthropic.com/news/model-hardware-standard-research-preview) | 实验室自动化 | 设备驱动强制安全上限 | 物理测量 | 不可逆；物理直觉弱 |
| 以模拟器隐藏真值的企业世界 | [Argo-Bench](https://arxiv.org/abs/2610.02122)、[Business Arena](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf) | 敏感的企业数据场景 | 模拟器重放 | 按动作在模拟器中的后果评分 | 模拟器本身的保真度 |

**选型原则**（依据 [lab 实践卡片](2026-10-14_office-pro-env/labs.md) 的结论，原始出处为 [Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad)、[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)、[Echoverse](https://github.com/microsoft/Echoverse/blob/main/README.md)）：判断用真实环境还是 mock，关键看能不能可靠地读到、改到、重置状态，而不是看外观像不像。
- 规模化 RL 用带状态 API 的 mock（[Qwen-CUA §3.2.1](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)、[Kimi K3 §4.2.5](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
- 稀缺的高价值流程走伙伴托管的真实副本（[Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad)）。
- 交互保真度和长尾覆盖用打包的真实应用或真机补齐（[Qwen-CUA 的 Gym-Anything 与 Mac mini](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。

---

## 3. 按环节拆解

### 3.1 环境实现：让 mock 足够真

- **把可测试性写成契约。** 合成或 mock 出来的应用必须暴露状态接口：
  - SoftwareGym 要求实现 `--dump-state/--reset-state/--seed-state`（[Coderprompt.json](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/prompt/Coderprompt.json)）；
  - Thinkingbox 要求实现 `__reserved__init/__reserved__geteffects`（[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)）；
  - CUA-Gym-Hub 提供 set / reset / diff 接口，并按会话 id 隔离（[README](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）。
- **保真度要靠流水线挣来。**
  - Echoverse 先把规格编译成可检查的断言，生成应用后修到全部断言通过；任务失败按数据库、后端、前端、任务文本、verifier 分层归因再修。修好一个环境，模型在其上从 16.2% 升到 38.5%；而浅环境会把真实站点上的准确率从 80.0 拉低到 75.0（[Echoverse](https://arxiv.org/abs/2607.28074)）。
  - SoftwareGym 先用 GUI 实测把应用修到 91.5% 的任务可通过，再拿去训练（[SoftwareGym](https://arxiv.org/abs/2610.12611)）。
- **种子数据用真实公开数据，或让 agent 上网检索。** Echoverse 用 InsideAirbnb、WebArena 等公开数据播种（[README](https://github.com/microsoft/Echoverse/blob/main/README.md)）；Kimi K3 让 agent 检索资料来搭工作区（[K3 报告 §4.2](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
- **跨系统一致的企业数据。** 用一张实体图投影到 CRM、工单、Slack 等多个系统，保证彼此一致（[Generating a Consistent Enterprise](https://arxiv.org/abs/2609.11286)、[Era by Eon](https://arxiv.org/abs/2609.09853)）。
- **从日志和 trace 起步的环境替身。** Trace2Env 从几十条 trace 构建 worldbook，靠规则校验、不变量和回放晋升门防止状态漂移，每个 worldbook 花费 19–340 美元（[RUNTIME_HARNESS](https://github.com/ruyue0001/trace2env/blob/main/docs/RUNTIME_HARNESS.md)、[REPRODUCING](https://github.com/ruyue0001/trace2env/blob/main/REPRODUCING.md)）。注意：其报告的数字产生于 10-08 一次 bug 修复之前（[REPRODUCING](https://github.com/ruyue0001/trace2env/blob/main/REPRODUCING.md)）。
- **专业软件的许可证三种处理**：用户自带 licence 注入、改用网页版、只发重建 recipe（[OSWorld-Science](https://github.com/DiscoAILab/OSWorld-Science/blob/main/configs/snapshots.yaml)）；商业镜像由用户自备（[EngiWorld](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)）；完全使用开源软件以保证可复现（[CADWorld](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)、[ScienceIDE](https://github.com/aitofound/ScienceIDE/blob/main/README.md)）。

### 3.2 状态管理与基础设施

- **fork 判分、推理时暂停沙箱。** Kimi K3 的 AgentENV 用 Firecracker microVM 做增量 checkpoint 和 fork，判分在 fork 出的副本上进行、不产生副作用；等待推理时暂停沙箱。开发期共创建约 5,100 万个沙箱（[K3 报告](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
- **把状态库和答案放到 agent 物理上够不着的地方。** MiMo 的 agent 容器碰不到状态库，答案和 rubric 到判分时才上传，且默认对 `.git` 做 strip / hide（[mimoagent](https://github.com/XiaomiMiMo/mimoagent/tree/mimo-oss)）。GDPevo 禁止 agent 容器挂载 env/、数据库或种子（[guides](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/environment_and_data.md)）。
- **会话隔离。** Thinkingbox 用 MCP Session Proxy 为每段对话隔离会话（[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)）。Google ADK 修过一个跨会话串用沙箱的 bug（[commit facaf29](https://github.com/google/adk-python/commit/facaf29)）。
- **mock 服务的四个基本操作**：注入状态、检查状态、重置、隔离会话（[Qwen-CUA 报告 §3](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
- **规模**：Qwen-CUA 可调用约 10 万 vCPU，RL 峰值约 2,000 个环境并发（[Qwen-CUA 报告](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）；ScaleCUA 支持 100+ 个 VM 并发生成（[README](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)）。

### 3.3 任务合成

- **锚定**：
  - 职业种子 → 证据图 → 任务与 rubric → 试跑修复（[GraphForge](https://arxiv.org/abs/2609.38923)）。
  - 从业者的真实请求去敏改写（[OfficeVal](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/data/README.md)）。
  - 从真实 commit、PR 反向工程（[WorkBuddy](https://arxiv.org/abs/2607.20911)）。
  - 从真实 BI 看板抽取（[BI-Bench](https://arxiv.org/abs/2609.20886)）。
  - 从官方软件文档出题（[EngiWorld task 示例](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/task-01.json)）。
- **组合**：
  - 原子业务规则的拆分与杂交（[GDPevo](https://arxiv.org/abs/2608.03764)）。
  - 服务依赖图上的随机游走（[CompoWorld](https://arxiv.org/abs/2609.33665)）。
  - 种子文件上的可复用操作（[CUA-Universe](https://arxiv.org/abs/2609.05374)）。
  - 先在合成的持久世界里定义实体、服务、状态和不变式，再从中派生任务（[AgentMercury](https://arxiv.org/abs/2608.20634)）。
- **链式与长程**：
  - 每个阶段的完成态验证后序列化，作为下一阶段的起点（[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
  - 跨多个模拟日、多个应用的活环境，每个事件各有判据（[Kimi K3](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
  - 递归扩展 15 轮，把前沿模型的 pass@4 从 90% 压到 2.5%，约 0.05 美元/任务（[RST](https://arxiv.org/abs/2608.05466)）。
- **难度标定**：
  - 参考模型 avg@3 落在约 0.4–0.6 才收（[GDPevo review criteria](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_3_Quality_Filtering/review_workspace/guides/review_criteria.md)）。
  - pass@8 只保留成功次数在 1–7 之间的任务（[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
  - 按成功率 EMA 做前沿采样，用成功和失败轨迹分别加难或简化任务（[ScaleCUA](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)）。
  - 风险：标定绑定某个前沿 agent，会把它的偏好带进数据（推论，依据 [GDPevo review criteria](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_3_Quality_Filtering/review_workspace/guides/review_criteria.md)）。
- **防泄漏与防记忆**：
  - 规则扰动（[HANDBOOK](https://github.com/surge-ai/handbook/blob/main/README.md)）。
  - 口语化改写，使 prompt 无法被检索（[WorkBuddy](https://arxiv.org/abs/2607.20911)）。
  - 发布不同种子的 sibling build（[Argo-Bench](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)）。
  - canary 字符串（[ScienceIDE 任务](https://github.com/aitofound/ScienceIDE/blob/main/hard85/mitgcm-atmos/mitgcm-atmos-repair-sem-data-aim-convection-qbl/instruction.md)）。
  - 只允许已验证可用的功能入题（[SoftwareGym](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/prompt/Taskdesignerprompt.json)）。
- **用户模拟器**：
  - 专门训练的“不合作”用户模拟器作为 RL 环境，比用 GPT-5.5 扮演用户泛化更好（[MIMESIS](https://github.com/VietHoang1512/mimesis/blob/main/README.md)）。
  - 只换用户模拟器，企业任务的 reward 就能变化 15.2 分（[UserProxyBench](https://arxiv.org/abs/2609.38043)）。

### 3.4 验证与奖励

- **按应用状态判分**：
  - 答案键在出题时用 SQL 从库里取，写任务比较前后数据库的 sqldiff（[Echoverse](https://github.com/microsoft/Echoverse/blob/main/README.md)）。
  - 终态数据库哈希必须等于重放 gold 动作后的哈希，LLM judge 不进严格分（[NeMo Gym indian_banking](https://github.com/NVIDIA-NeMo/Gym/blob/main/resources_servers/indian_banking/README.md)）。
  - 按终态打分，不信 agent 自报完成（[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
- **让领域引擎重算一遍**：
  - 几何内核读 STEP 做容差断言，并从 shell history 检测是否绕开 GUI（[EngiWorld eval.py](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/eval.py)）。
  - 用 FEniCS 重算 compliance（[EngiWorld fenics eval](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/design-optimization/cli/fenics/task-01/eval.py)）。
  - 重编译后跑物理用例，不动仓库恰好得 0 分（[ScienceIDE](https://github.com/aitofound/ScienceIDE/blob/main/README.md)）。
  - 在评估方持有的多个工况（含故障工况）下做原生仿真（[SimuVerity](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/README.md)）。
- **结构化 rubric**：
  - 自然语言描述与 verifier 代码配对，含禁止项（[HANDBOOK rubrics.json](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/tests/rubrics.json)）。
  - 交付物门槛加逐条加减分；9 个任务需要 Office COM（[OfficeVal](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)）。
  - DAYJOB 每题中位数 47.5 / 57.5 条专家条目，全部满足才算通过（[DAYJOB](https://arxiv.org/abs/2610.01306)）。
  - FrontierFinance 共 11,543 条带来源的 rubric（[FrontierFinance](https://arxiv.org/abs/2608.11683)）。
  - rubric 由领域方与 lab 共写：Ironclad 每个任务 8–50 条（[Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad)）。
- **部分分**：训练时很关键，NeutronGym 去掉部分分后增益塌缩 60 个点（[NeutronGym](https://arxiv.org/abs/2610.03631)）。评测时多数选全对才算通过，例如 [CADWorld](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)、[DAYJOB](https://arxiv.org/abs/2610.01306)。部分得分与完美率要分开报：MyPCBench 上分别是 84.3 和 58.7（[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
- **副作用与可靠性**：Thinkingbox 拒绝多余副作用并报 pass^k，pass@1 为 65.36%，pass^20 只有 25.25%（[Thinkingbox](https://arxiv.org/abs/2608.19741)）。
- **judge 偏差**：VLM judge 系统性偏宽松；“答案必须来自环境”这条规则可以直接复用（[OSReward prompt](https://github.com/OS-Copilot/OSReward/blob/main/eval_pipeline/prompts/binary_v1.txt)）。声称“确定性状态检查”的工作，实际 reward 可能是手写启发式（[MDLM appworld_plugin](https://github.com/patronus-ai/mdlm_world_modeling/blob/main/appworld/appworld_plugin.py)）。

### 3.5 数据准备

- **主流配方**：先用验证过的轨迹做 SFT，再在可执行 verifier 上做 GRPO 类在线 RL（[UI-Mate](https://github.com/Tencent/UI-Mate/blob/main/README.md)、[ScaleCUA](https://github.com/THUDM/SCALE-CUA/blob/main/README.md)、[HybridCUA](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)、[ScienceIDE RL](https://github.com/aitofound/ScienceIDE/blob/main/RL/README.md)）。
- **零环境冷启动**：只需 API spec，用 LLM 模拟响应合成轨迹，就能在 OfficeBench 上带来 SFT 增益（[Apple env-free](https://arxiv.org/abs/2607.16900)）。
- **专家数据的成本**：CADWorld 约 1,300 人时做 200 题（[CADWORLD.pdf](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)）；DAYJOB 每题估计需要 13–17 小时人工（[DAYJOB](https://arxiv.org/abs/2610.01306)）；DataSpace 由 11 名专家修复（[DataSpace](https://arxiv.org/abs/2608.03451)）。也有完全由 agent 构建和审阅的：GDPevo 的 6 个 reviewer 都是 agent（[review criteria](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_3_Quality_Filtering/review_workspace/guides/review_criteria.md)）。
- **敏感数据**：用隐藏真值的模拟世界替代真实企业仓库（[Argo-Bench](https://arxiv.org/abs/2610.02122)）；或只公开脱敏轨迹，完整数据返还数据方，例如 UK Biobank（[CASE](https://github.com/VinyehShaw/CASE/blob/main/README.md)）。
- **训练时省成本**：RL 阶段用缓存回放的 mock 工具代替真实医学工具（[CASE](https://github.com/VinyehShaw/CASE/blob/main/README.md)）。
- **数据质量决定 RLVR**：专家清洗标签（BIRD-Platinum），加上可被反驳的 verifier，比加 scaffold 更有效（[Thinking Machines](https://thinkingmachines.ai/news/putting-task-expertise-into-rl/)）。

### 3.6 隔离与安全

- **默认断网，出站检查要覆盖 DNS 与缓存层**（[OpenAI DNS 报告](https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/)、[UK AISI](https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities)）。
- **mock 坏了要关闭，不能落到真实系统**：练习副本加载失败后，agent 提交了真实政府表单（[Anthropic](https://www.anthropic.com/research/investigating-unintended-model-actions)）。
- **不可逆动作设闸**：提交、上传、密码、付款都暂停等人审（[Qwen-CUA demo](https://github.com/xlang-ai/Qwen-CUA)）；采购 agent 的硬约束是“never spend money, never sign, never send a PO”（[xAI](https://x.ai/news/grok-bot-procurement)）；agent 只拿占位凭证，真凭证在网络边界注入（[Meta Sentinel](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)）。
- **grader 与答案物理隔离**：有 run 读到 grader 后拿到 0.99 分（[Argo-Bench](https://github.com/TextQLLabs/Argo-Bench/blob/main/analysis/reward_hacking/README.md)）；给有 shell 的 agent 准备了 hardened 模式（[CUA-Gym-Hub](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）。
- **事前检查**：边界写成指令而非陈述，并在运行前验证每个任务可解（[Anthropic](https://www.anthropic.com/news/improving-alignment-security-efforts)）。
- **物理设备**：设备驱动层强制安全上限，6 种人为制造的故障都在设备动作前被拦下（[Anthropic MHS](https://www.anthropic.com/news/model-hardware-standard-research-preview)）。

---

## 4. 领域速查

| 领域 | 代表环境 / 基准 | 环境形态 | 验证方式 |
|---|---|---|---|
| 办公套件（docx / xlsx / pptx） | [OmegaUse-OfficeVal](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)、[WorkBuddy Office](https://github.com/Tencent/workbuddy-bench/blob/main/README.md) | 交付物 / Docker 工作区 | 代码 verifier 加 rubric |
| 跨应用办公 SaaS | [UI-Mate / OSWorkerBench](https://arxiv.org/abs/2608.15930)、[HANDBOOK](https://arxiv.org/abs/2607.25398)、[Thinkingbox](https://arxiv.org/abs/2608.19741) | mock SaaS / MCP | state diff、禁止项、pass^k |
| CRM / ERP 业务流程 | [GDPevo](https://arxiv.org/abs/2608.03764)、[Argo-Bench](https://arxiv.org/abs/2610.02122)、[NeMo Gym workplace_assistant](https://github.com/NVIDIA-NeMo/Gym/blob/main/resources_servers/workplace_assistant/README.md) | 自建业务系统 / 模拟器 | 规则 grader / 后果结算 |
| 合同与法务 | [OpenAI × Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad) | 真实 SaaS 副本 | rubric |
| 金融 | [FrontierFinance](https://arxiv.org/abs/2608.11683)、[DAYJOB](https://arxiv.org/abs/2610.01306) | 公开数据加文件工作区 | 专家 rubric |
| 医疗 | [CASE](https://github.com/VinyehShaw/CASE/blob/main/README.md)、[DAYJOB](https://arxiv.org/abs/2610.01306) | 真实 UK Biobank 数据加医学工具 | 精确匹配加 rubric dense reward |
| 数据 / BI | [AgenticDataBench](https://arxiv.org/abs/2607.01647)、[DataSpace](https://arxiv.org/abs/2608.03451)、[BI-Bench](https://arxiv.org/abs/2609.20886) | 真实数据集加代码执行 | 逐列容差比对 |
| 科学软件 | [OSWorld-Science](https://arxiv.org/abs/2609.39903)、[ScienceIDE](https://arxiv.org/abs/2609.19134)、[SWE-bench Science](https://arxiv.org/abs/2608.19799) | VM 中的真实软件 / 钉死版本的代码库 | 可执行 evaluator / 物理用例 |
| 工程（CAD / CAE / 仿真） | [EngiWorld](https://arxiv.org/abs/2609.37686)、[CADWorld](https://arxiv.org/abs/2609.16251)、[SimuVerity](https://arxiv.org/abs/2610.02304)、[NeutronGym](https://arxiv.org/abs/2610.03631) | VM 中的真实工程软件 / 模拟器 | 几何、物理引擎重算 |
| 实验室仪器 | [Anthropic MHS](https://www.anthropic.com/news/model-hardware-standard-research-preview) | 真实设备 | 物理测量与安全上限 |

---

## 5. 搭建路线：一条可照着做的流水线

以下是基于上述证据的建议（推论，每步都附依据）：

1. **从日志或 API spec 起步，先做 SFT 数据。** 用内部日志或 API spec，以 LLM 模拟或 trace 重建快速搭出 mock，合成冷启动轨迹（[Apple env-free](https://arxiv.org/abs/2607.16900)、[Trace2Env](https://github.com/ruyue0001/trace2env/blob/main/docs/RUNTIME_HARNESS.md)）。
2. **高频系统换成有状态的真实实现，并写死可测试性契约。** 实现 dump / reset / seed 和 effects 接口（[SoftwareGym](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/prompt/Coderprompt.json)、[Thinkingbox](https://github.com/microsoft/thinkingbox/blob/main/README.md)），按“规格断言 → 生成 → 修到全部断言通过”的方式迭代（[Echoverse](https://github.com/microsoft/Echoverse/blob/main/README.md)）。
3. **任务用“锚定 + 组合 + 链式”合成**（[GraphForge](https://arxiv.org/abs/2609.38923)、[CompoWorld](https://arxiv.org/abs/2609.33665)、[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)），并配用户模拟器（[MIMESIS](https://github.com/VietHoang1512/mimesis/blob/main/README.md)）。
4. **verifier 落在状态上**，按“初始状态不能通过、解完必须通过”做自检（[VeriGen](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/agent_feasibility_verification.md)）。rubric 采用“文本 + 代码 + 禁止项”配对（[HANDBOOK](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/tests/rubrics.json)），对多余副作用扣分（[Thinkingbox](https://arxiv.org/abs/2608.19741)）。
5. **难度用参考模型标定**（[GDPevo](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/calibration_and_review.md)、[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）；**泄漏用对抗式 rollout 审计**：agent 能读到的特权状态、git 历史、grader（[Argo-Bench](https://github.com/TextQLLabs/Argo-Bench/blob/main/analysis/reward_hacking/README.md)、[mimoagent](https://github.com/XiaomiMiMo/mimoagent/tree/mimo-oss)）。
6. **基础设施**：fork 判分、会话隔离、默认断网，不可逆动作设闸（[Kimi K3](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)、[Thinkingbox](https://github.com/microsoft/thinkingbox/blob/main/README.md)、[Anthropic](https://www.anthropic.com/news/improving-alignment-security-efforts)）。
7. **评测与 sim-to-real 检验**：报 pass^k、分开报部分分与完美率（[Thinkingbox](https://arxiv.org/abs/2608.19741)、[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)），并用回放一致性指标检验 mock 与真实环境的差距（[Trace2Env](https://github.com/ruyue0001/trace2env/blob/main/REPRODUCING.md)）。

---

## 6. 开放问题与研究机会

1. **办公文件语义级的保真与判分。** xlsx 公式、透视表、docx 格式与修订、pptx 版式的语义检查，目前只有少量代码 verifier 覆盖，部分还要靠 Office COM（[OfficeVal](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)）。方法组的跨篇分析也把它列为本批论文都没解决的问题（[methods 笔记 takeaway 6](2026-10-14_office-pro-env/methods.md)，依据 [OfficeVal](https://arxiv.org/abs/2607.27155)、[Echoverse](https://arxiv.org/abs/2607.28074)）。
2. **mock 与真实环境之间的差距没有统一度量。** 只有 Trace2Env 提出了“模拟动作回放到真实环境是否成立”的一致性指标（[REPRODUCING](https://github.com/ruyue0001/trace2env/blob/main/REPRODUCING.md)），而 Echoverse 显示浅 mock 会伤害真实站点上的表现（[Echoverse](https://arxiv.org/abs/2607.28074)）。
3. **副作用与权限、审批流的真实性。** 判分是否惩罚多余改动尚无共识（[Echoverse prompts](https://github.com/microsoft/Echoverse/blob/main/harness/prompts.py) 对比 [Thinkingbox](https://arxiv.org/abs/2608.19741)）。企业里真实的权限与审批流（多级审批、角色权限）在 mock 中少见（推论，依据 [办公卡片](2026-10-14_office-pro-env/office.md) 中各环境的形态描述，如 [CUA-Gym-Hub](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)）。
4. **judge 与用户模拟器的可靠性本身需要被评测**（[OSReward](https://arxiv.org/abs/2607.28609)、[UserProxyBench](https://arxiv.org/abs/2609.38043)）。
5. **专业领域缺训练用环境。** 多数专业基准只用于评测，有的明确禁止用于训练（[Thinkingbox-Bench release](https://github.com/microsoft/thinkingbox-data/blob/main/releases/thinkingbox_bench_v1/README.md)）；能做 RL 的少数有 [ScienceIDE](https://github.com/aitofound/ScienceIDE/blob/main/RL/README.md)、[NeutronGym](https://arxiv.org/abs/2610.03631)、[CASE](https://github.com/VinyehShaw/CASE/blob/main/README.md)。
6. **成本几乎不报。** 只有 RST（约 0.05 美元/任务）、VHD-Play（每个环境几美分）、Trace2Env（每个 worldbook 19–340 美元）给了数字（[RST](https://arxiv.org/abs/2608.05466)、[VHD-Play](https://arxiv.org/abs/2609.27321)、[Trace2Env](https://github.com/ruyue0001/trace2env/blob/main/REPRODUCING.md)）。
7. **“停下并报告”的环境依然空白**：真实流程中的不可完成任务与含糊授权，正是越界事故的触发器（[Anthropic](https://www.anthropic.com/research/investigating-unintended-model-actions)）。

---

## 7. 必读清单

| # | 读什么 | 为什么 | 证据深度 |
|---|---|---|---|
| 1 | [Qwen-CUA 报告 §3](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf) | mock 服务、打包应用、阶段链式合成、真机，lab 级完整实践 | 全文 |
| 2 | [Kimi K3 报告 §4.2](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf) | 活环境、harness 随机化、AgentENV 的 fork 判分 | 全文 |
| 3 | [Echoverse](https://github.com/microsoft/Echoverse/blob/main/README.md) | 规格编译成有状态应用、数据库 diff 判分、深度比数量重要 | 仓库 |
| 4 | [UI-Mate / CUA-Gym-Hub](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md) | 98 个 mock SaaS 加统一状态 API | 仓库 |
| 5 | [GDPevo 构建 SOP](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_2_Task_Group_Synthesis/task_factory/guides/environment_and_data.md) | 企业环境、任务、grader 的全流程开源 | 仓库 |
| 6 | [Thinkingbox](https://github.com/microsoft/thinkingbox/blob/main/README.md) | 会话隔离、拒绝多余副作用、pass^k | 仓库 |
| 7 | [ScaleCUA / VeriGen](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/agent_feasibility_verification.md) | agent 写 evaluator 加负对照自检 | 仓库 |
| 8 | [SoftwareGym](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/prompt/Coderprompt.json) | 可测试性契约 | 仓库 |
| 9 | [HANDBOOK](https://github.com/surge-ai/handbook/blob/main/tasks/hr_crestwood_university_79786c46/tests/rubrics.json) | rubric 文本与代码配对，含禁止项 | 仓库（仅 3 个样例） |
| 10 | [Trace2Env](https://github.com/ruyue0001/trace2env/blob/main/docs/RUNTIME_HARNESS.md) | 从 trace 建环境替身的护栏 | 仓库 |
| 11 | [EngiWorld](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md) | 真实工程软件、领域引擎 verifier、检测绕开 GUI | 仓库 |
| 12 | [OSWorld-Science](https://github.com/DiscoAILab/OSWorld-Science/blob/main/docs/user_guide/adding-a-task.md) | 商业许可证处理、grader 负测试 | 仓库 |
| 13 | [Argo-Bench](https://github.com/TextQLLabs/Argo-Bench/blob/main/analysis/reward_hacking/README.md) | 模拟器隐藏真值、按后果评分、reward hacking 实录 | 仓库 |
| 14 | [OmegaUse-OfficeVal](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md) | 办公文件的代码 verifier | 仓库 |
| 15 | [MIMESIS](https://github.com/VietHoang1512/mimesis/blob/main/README.md) | 训练出的用户模拟器作为 RL 环境 | 仓库 |
| 16 | [Apple env-free](https://arxiv.org/abs/2607.16900) | 只需 API spec 的冷启动数据 | 摘要 |
