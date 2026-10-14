# 办公/专业场景 Agent 的环境与数据构建方法 — 论文精读笔记（2026-07-01 → 10-13）

> 输入：C_env_methods.json（90 篇 env-construction 标签候选）+ 全量池补充（DeskForge、SoftwareGym 等）。
> 出处规则：每条结论后附 URL。arXiv abs 链接 = 仅来自摘要（本环境无法访问 arXiv 全文）；GitHub blob 链接 = 来自仓库 README/代码（已 clone 只读阅读，未执行）。无法溯源的标「无出处，待核」；「迁移/评级/推断」类条目是笔记作者的分析，均注明所依据的论文链接；「（二手）」表示仅来自 WebSearch 结果页。

## 0. 结论速览

**统计**：C 表 90 篇全部按摘要筛选，结果为 ✅深读 19（含 3 篇「轻」读）、◐浏览 38、✗ 无关或误标 33。另从全量池补充深读 2 篇（SoftwareGym、DeskForge），共 21 张方法卡片；第 2.E 节另列 4 篇池内办公数据合成论文（仅摘要）。

### 必读 Top-8（按对办公/专业 env 的可迁移性排序）

| # | 论文 | 一句话为什么读 | 来源深度 |
|---|---|---|---|
| 1 | [Echoverse](https://arxiv.org/abs/2607.28074)（A1） | spec→有状态 Web 应用；答案从真实 DB 铸造并按 DB diff 判分；环境、任务、verifier 与模型共演化；Echo 家族本身就含 Mail/Calendar/Chat/Bank（[README](https://github.com/microsoft/Echoverse/blob/main/README.md)） | L3 |
| 2 | [Thinkingbox](https://arxiv.org/abs/2608.19741)（D1） | 企业流程（保险、IT/HR）的 MCP 隔离沙箱；用 init/geteffects 接口判终态，并拒绝多余副作用；用 pass^k 衡量可靠性（[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)） | L2 |
| 3 | [SoftwareGym](https://arxiv.org/abs/2610.12611)（A2） | 合成原生桌面应用，并强制每个应用实现 dump/reset/seed-state 可测试性契约（[Coderprompt.json](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/prompt/Coderprompt.json)）；OSWorld 上有 OOD 增益 | L3 |
| 4 | [Trace2Env](https://arxiv.org/abs/2610.06100)（B1） | 从几十条 trace 构建 worldbook，作为有状态 mock；rules_only 信任策略 + 不变量 + replay 晋升门，是「LLM 模拟企业系统」的护栏模板（[RUNTIME_HARNESS.md](https://github.com/ruyue0001/trace2env/blob/main/docs/RUNTIME_HARNESS.md)） | L3 |
| 5 | [Apple 免环境 API 数据合成](https://arxiv.org/abs/2607.16900)（B2） | 只需 API spec 就能合成轨迹，并在 OfficeBench 上有效，是办公场景门槛最低的起点 | L1 |
| 6 | [RST 递归合成](https://arxiv.org/abs/2608.05466)（D3） | 种子任务递归扩展，每轮在新 sandbox 中验证；约 0.05 美元/任务；用前沿模型 pass@4 衰减刻画难度 | L1 |
| 7 | [OSReward](https://arxiv.org/abs/2607.28609)（D2） | 证明 VLM judge 存在系统性宽松偏差；judge prompt 里的 grounding rule 可直接复用（[binary_v1.txt](https://github.com/OS-Copilot/OSReward/blob/main/eval_pipeline/prompts/binary_v1.txt)） | L3 |
| 8 | [MIMESIS](https://arxiv.org/abs/2610.09484)（C1） | 专门训练的「不合作」用户模拟器作为 RL 环境，比 GPT-5.5 当用户泛化更好（[README](https://github.com/VietHoang1512/mimesis/blob/main/README.md)） | L2 |

其他评为必读的还有 [RecreationWorld](https://arxiv.org/abs/2609.22000)（reference-as-oracle）、[Terminal-Universe](https://arxiv.org/abs/2609.04148)（从 trace 重建**可执行**环境）、[CompoWorld](https://arxiv.org/abs/2609.33665)（服务库组合，WM 兜底）。这三篇未进 Top-8，原因是证据深度不足（后两篇为 L1）或与办公分布有差距。

### 方法 taxonomy（保真度 × 输入）

纵轴是保真度，从真实执行到 LLM/视觉模拟；横轴是构建所需的输入。

| 保真度 \ 输入 | 代码 / 现成应用 | 文档 / 规格 / API spec | 日志 / 轨迹 / traces | 几乎无输入（类型名、种子、数学模型） |
|---|---|---|---|---|
| **真实执行（真应用 / 真沙箱）** | [RecreationWorld](https://arxiv.org/abs/2609.22000)（运行中的 reference）· [CodeMidas](https://arxiv.org/abs/2609.22068)（源码）· [DeskForge](https://arxiv.org/abs/2610.02320)（真 Linux 应用）· [RST](https://arxiv.org/abs/2608.05466)（已验证种子任务）· [T1](https://arxiv.org/abs/2609.11042) · [Qwen-UI-Agent](https://arxiv.org/abs/2607.28227)（真机）· [Game Dev/RLHEV](https://arxiv.org/abs/2608.25518)（游戏引擎） | [Echoverse](https://arxiv.org/abs/2607.28074)（spec + 公开种子数据）· [Thinkingbox](https://arxiv.org/abs/2608.19741)（手写 MCP mock + scenario）· [DeepSearch-World](https://arxiv.org/abs/2607.07820)（冻结 Wikipedia 语料） | [Terminal-Universe](https://arxiv.org/abs/2609.04148)（回放文件操作重建 workspace） | [SoftwareGym](https://arxiv.org/abs/2610.12611)（软件类型 → 设计 → 代码）· [VHD-Play](https://arxiv.org/abs/2609.27321)（已解数学模型 → 有状态工具） |
| **混合（真实服务 + WM 兜底）** | — | [CompoWorld](https://arxiv.org/abs/2609.33665)（tool spec → 已验证服务，实现不了的交给 WM） | — | — |
| **LLM 模拟，带显式状态/规则护栏** | — | — | [Trace2Env](https://arxiv.org/abs/2610.06100)（worldbook + 规则校验） | — |
| **LLM 模拟，训练出的 WM / 用户模拟器** | — | [EnvACE](https://arxiv.org/abs/2608.06197)（policy 自扮环境，基于工具数据集） | [MDLM WM](https://arxiv.org/abs/2607.16204)（239K 轨迹）· [MIMESIS](https://arxiv.org/abs/2610.09484)（人类对话） | — |
| **LLM 模拟，prompt 型，无显式状态** | — | [Apple env-free](https://arxiv.org/abs/2607.16900)（API spec） | — | — |
| **视觉模拟（图像生成）** | — | — | — | [AutoGUIWorld](https://arxiv.org/abs/2610.01215)（结构化场景规格） |
| *（verifier 层，与输入正交）* | | | [OSReward](https://arxiv.org/abs/2607.28609)（人工金标轨迹 → judge 评测与语料） | |

### Takeaways

1. **单个环境的深度比环境数量更重要，判分要落在应用自己的状态上。**
   - Echoverse 显示：同一领域里，浅环境会把 live-site 准确率拉到基座以下（80.0→75.0），深环境则提升到 85.0；修好一个环境，训练出的模型就能从 16.2% 升到 38.5%（[Echoverse abs](https://arxiv.org/abs/2607.28074)）。
   - SoftwareGym 先用 GUI 实测把应用修到 91.5% 任务可通过，再拿去训练，OSWorld OOD 上有增益（[SoftwareGym abs](https://arxiv.org/abs/2610.12611)）。
   - 结论：办公 env 管线应把预算优先花在「修环境 + 修 verifier」上，而不是多生成几百个浅应用。（笔记作者建议，依据 [Echoverse abs](https://arxiv.org/abs/2607.28074)、[SoftwareGym abs](https://arxiv.org/abs/2610.12611)）

2. **「可测试性契约」是从合成应用到可靠 reward 的关键工程手段。**
   - SoftwareGym 强制每个应用实现 `--dump-state/--reset-state/--seed-state`（[Coderprompt.json](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/prompt/Coderprompt.json)）。
   - Thinkingbox 的每个 MCP server 实现 `__reserved__init/__reserved__geteffects`（[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)）。
   - Echoverse 的每个任务内嵌 `verification_query`（[tasks](https://github.com/microsoft/Echoverse/blob/main/envs/echostay/tasks/test_tasks.jsonl)）。
   - **但副作用检查标准不一**：Echoverse 的写判分明确容忍多余改动（[prompts.py](https://github.com/microsoft/Echoverse/blob/main/harness/prompts.py)），Thinkingbox 则拒绝多余效果（[abs](https://arxiv.org/abs/2608.19741)）。办公场景（误发邮件、误删记录）应采用后者。

3. **LLM 模拟适合当「数据生成器」，当「RL 奖励源」需要护栏。**
   - 只看 spec 的 prompt 型模拟已能在 OfficeBench 上带来 SFT 增益（[Apple abs](https://arxiv.org/abs/2607.16900)）。
   - 一旦用于 RL 或长程交互，就需要显式状态、规则支撑和 replay 晋升门，否则状态会漂移（[Trace2Env RUNTIME_HARNESS](https://github.com/ruyue0001/trace2env/blob/main/docs/RUNTIME_HARNESS.md)，[OFFLINE_VALIDATION](https://github.com/ruyue0001/trace2env/blob/main/docs/OFFLINE_VALIDATION.md)）。
   - 反例一：MDLM WM 的 AppWorld reward 实际是带关键词和占位符黑名单的手写启发式（[appworld_plugin.py](https://github.com/patronus-ai/mdlm_world_modeling/blob/main/appworld/appworld_plugin.py)）。
   - 反例二：AutoGUIWorld 自承不在真实环境执行、也不验证任务完成（[README](https://github.com/ImYangC7/AutoGUIWorld/blob/main/README.md)）。
   - 反例三：EnvACE 的 reward 是 LLM checklist judge，而不是真实状态（[checklist_reward.py](https://github.com/Within-yao/EnvACE/blob/main/agent_system/environments/env_package/checklist/checklist_reward.py)）。

4. **企业场景里最丰富的输入往往是日志和轨迹，而不是代码。**
   - Terminal-Universe 从轨迹回放出可执行 workspace（[abs](https://arxiv.org/abs/2609.04148)）。
   - Trace2Env 只需几十条 trace 构建 worldbook，每个 19–340 美元（[REPRODUCING.md](https://github.com/ruyue0001/trace2env/blob/main/REPRODUCING.md)）。
   - MIMESIS 用真实人类对话训练用户模拟器（[abs](https://arxiv.org/abs/2610.09484)）。
   - 池内的企业数据合成工作，则用一张实体图投影到 CRM、工单、Slack 等多个系统，保证跨系统一致（[Generating a Consistent Enterprise](https://arxiv.org/abs/2609.11286)，[Era by Eon](https://arxiv.org/abs/2609.09853)）。
   - 建议路线：内部日志 → Trace2Env 式 mock（快）→ 高频系统再用 Echoverse/SoftwareGym 式的真实实现（准）→ 用 CompoWorld 式组合生成跨系统任务（[CompoWorld abs](https://arxiv.org/abs/2609.33665)）。

5. **任务合成里，难度靠「链式扩展 + 每轮重新验证」，防泄露靠「白名单 + 对抗 rollout」。**
   - RST 用 15 轮递归把前沿模型 pass@4 从 90% 压到 2.5%，约 0.05 美元/任务（[abs](https://arxiv.org/abs/2608.05466)）。
   - VHD-Play 先求解再出环境，reference 与环境同源（[abs](https://arxiv.org/abs/2609.27321)）。
   - CodeMidas 用 adversarial rollouts 查泄露（[二手](https://arxiv.org/pdf/2609.22068)）。
   - SoftwareGym 只允许已验证可用的功能入题，并禁止把内部手册内容写进任务（[Taskdesignerprompt.json](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/prompt/Taskdesignerprompt.json)）。
   - DeepSearch-World 蒸馏时删除只读 state 字段，防止特权信息泄露（[README](https://github.com/ornamentt/DeepSearch-World/blob/main/README.md)）。

6. **开放问题：judge 和模拟器本身的可靠性很少被测量，sim-to-real 缺乏统一指标。**
   - VLM judge 普遍偏宽松，可靠的又太贵（[OSReward abs](https://arxiv.org/abs/2607.28609)）。
   - 只换 user proxy，企业任务 reward 就能变化 15.2 分（[UserProxyBench abs](https://arxiv.org/abs/2609.38043)）。
   - pass@1 与 pass^20 相差 40 个点（65.36% vs 25.25%）（[Thinkingbox abs](https://arxiv.org/abs/2608.19741)）。
   - sim-to-real 目前只有 Trace2Env 的「W2R/Real 一致性比」这类做法可借鉴（[REPRODUCING.md](https://github.com/ruyue0001/trace2env/blob/main/REPRODUCING.md)）。
   - 成本也很少报告：只有 RST（约 0.05 美元/任务）、VHD-Play（几美分/环境）和 Trace2Env（19–340 美元/worldbook）给出了数字（[RST](https://arxiv.org/abs/2608.05466)，[VHD-Play](https://arxiv.org/abs/2609.27321)，[Trace2Env](https://github.com/ruyue0001/trace2env/blob/main/REPRODUCING.md)）。
   - 办公特有、本批论文都未解决的问题：xlsx/docx 文件语义级的保真（公式、格式、透视表）、权限与审批流的真实性、跨应用副作用审计（「无出处，待核」——基于本批 21 篇缺失项的归纳）。



## 1. 筛选表（90 篇全部）

图例：✅深读 = 进入方法卡片；◐浏览 = 相关但未深读（偏评测或同类方法较弱/信息不足）；✗ = 误标或与环境/数据构建无关。理由均基于各自 arXiv 摘要（表中 abs 链接）。

| # | 论文（arXiv） | 机构 · HF↑ | 相关? | 理由 |
|---|---|---|---|---|
| 0 | [OSReward: Instituting Standardized Evaluation for Cross-Platform Computer-Use Reward Models](https://arxiv.org/abs/2607.28609) | NLP Group of The University of Hong Kong · 72 | ✅深读 | verifier: VLM judge 可靠性基准 + OS-Shepherd-100K 判决语料；CUA reward 关键（[abs](https://arxiv.org/abs/2607.28609)） |
| 1 | [RecreationWorld: Scalable and Verifiable Environments for Hybrid Computer-Use Agents](https://arxiv.org/abs/2609.22000) | Qwen · 63 | ✅深读 | env synthesis: running reference 作 oracle，五平台可复现环境，execution-grounded reward（[abs](https://arxiv.org/abs/2609.22000)） |
| 2 | [CodeMidas: Scaling Agentic Coding RL Environments from Code Itself](https://arxiv.org/abs/2609.22068) | Xiaomi MiMo · 98 | ✅深读 | env synthesis: 仅用源码→可执行 RL 环境，agent 写行为规格+测试+过滤（[abs](https://arxiv.org/abs/2609.22068)） |
| 3 | [DeepSearch-World: Self-Distillation for Deep Search Agents in a Verifiable Environment](https://arxiv.org/abs/2607.07820) | HKUST · 72 | ✅深读 | infra/data prep: 确定性可复现搜索环境 + 420K random-walk 任务 + 自蒸馏迭代（[abs](https://arxiv.org/abs/2607.07820)） |
| 4 | [UI-Mate: Advancing Open-Weight Foundation GUI Agents with In-Context Demonstrations](https://arxiv.org/abs/2608.15930) | Tencent Hunyuan · 33 | ◐浏览 | 闭环 data engine（task-verifier bundle）+ OSWorkerBench 办公任务；方法细节偏系统（[abs](https://arxiv.org/abs/2608.15930)） |
| 5 | [MiMo-V2.6: Scaling Reinforcement Learning Towards Self-Improvement](https://arxiv.org/abs/2610.11959) | Xiaomi MiMo · 60 | ◐浏览 | 通用 RL 技术报告；含 grader compute 与 reward hacking 多层防御，环境方法非重点（[abs](https://arxiv.org/abs/2610.11959)） |
| 6 | [Agentic Game Development as a Verifiable Trajectory Data Engine for Scaling World Models](https://arxiv.org/abs/2608.25518) | National University of Singapore · 128 | ✅深读(轻) | verifier/data: 游戏引擎作可执行世界规格 + 人类接受信号（RLHEV）；对办公迁移有限（[abs](https://arxiv.org/abs/2608.25518)） |
| 7 | [DarwinX: Evolving Agent Harnesses Through Natural Selection](https://arxiv.org/abs/2608.07545) | Salesforce AI Research · 87 | ✗ | harness 自进化，非环境/数据构建（[abs](https://arxiv.org/abs/2608.07545)） |
| 8 | [Qwen-UI-Agent Technical Report: Toward Next-Generation Real-World Centric Foundation GUI Agents](https://arxiv.org/abs/2607.28227) | TongyiLab · 284 | ✅深读(轻) | infra: 真机 runtime + 10k 并发环境 + agent 驱动的任务/环境构造飞轮（[abs](https://arxiv.org/abs/2607.28227)） |
| 9 | [AgentOPSD: Recursive Self-Distillation for Agentic Reinforcement Learning](https://arxiv.org/abs/2608.05987) | Tsinghua University · 94 | ✗ | credit assignment 算法，非环境（[abs](https://arxiv.org/abs/2608.05987)） |
| 10 | [T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks](https://arxiv.org/abs/2609.11042) | Tencent Hunyuan · 29 | ✅深读(轻) | infra/reward: 真实 shell 云沙箱 RL + 以通过 verifier 数为 dense process reward（[abs](https://arxiv.org/abs/2609.11042)） |
| 11 | [OSWorld-Science: A Benchmark of Computer Use Agents for Learning and Using Scientific Software](https://arxiv.org/abs/2609.39903) | DiscoAILab · 28 | ◐浏览 | 科学软件 CUA benchmark；artifact-based evaluator 设计可借鉴（[abs](https://arxiv.org/abs/2609.39903)） |
| 12 | [DeepVoyager-VL: Incentivizing Vision-in-the-Loop Search for Long-Horizon Multimodal Agents](https://arxiv.org/abs/2608.01827) | Peking University · 17 | ✗ | 多模态 deep search 数据合成（事件图），偏搜索（[abs](https://arxiv.org/abs/2608.01827)） |
| 13 | [EnvACE: Internalizing Environment Dynamics via World Rehearsal for Agentic Reinforcement Learning](https://arxiv.org/abs/2608.06197) | Tencent · 44 | ✅深读 | simulation: policy 自扮环境（world rehearsal），免外部环境 RL（[abs](https://arxiv.org/abs/2608.06197)） |
| 14 | [OSWorld-Pro: Process-based Evaluation for Computer Use Agents](https://arxiv.org/abs/2609.24890) | NVIDIA · 22 | ◐浏览 | verifier: 子目标级过程评估（LLM judge + 67K 人工标注）（[abs](https://arxiv.org/abs/2609.24890)） |
| 15 | [Echoverse: Deep, Evolving Environments for Training Computer-Use Agents at Scale](https://arxiv.org/abs/2607.28074) | Microsoft Research · 9 | ✅深读 | env synthesis: spec→有状态应用，DB 判分，环境/任务/verifier 与模型共演化（[abs](https://arxiv.org/abs/2607.28074)） |
| 16 | [AutoGUIWorld: Image Generators as Visual World Models for GUI Agent](https://arxiv.org/abs/2610.01215) | Tencent Hunyuan · 42 | ✅深读 | simulation: 图像生成器作 GUI 视觉 world model 合成轨迹（[abs](https://arxiv.org/abs/2610.01215)） |
| 17 | [When Search Agents Should Ask: DiscoBench for Clarification-Aware Deep Search](https://arxiv.org/abs/2606.27669) | Tencent Hunyuan · 9 | ◐浏览 | user sim: 澄清型搜索 benchmark 的用户模拟器（[abs](https://arxiv.org/abs/2606.27669)） |
| 18 | [Verifiable Hidden Dynamics Play: Generating Agentic RL Environments from Solved Mechanisms](https://arxiv.org/abs/2609.27321) | Qwen · 8 | ✅深读 | env/task synthesis: 先采样并求解数学模型再渲染成有状态工具，reference 同源（[abs](https://arxiv.org/abs/2609.27321)） |
| 19 | [Kimi K3: Open Frontier Intelligence](https://arxiv.org/abs/2607.24653) | Moonshot AI · 263 | ✗ | 基座模型报告；仅提及 persistent rollout/sandbox state（[abs](https://arxiv.org/abs/2607.24653)） |
| 20 | [EvolvingWorld: An Open-Schema Framework for Co-Evolving Role-Play Agents and World Model in Interactive Literary World](https://arxiv.org/abs/2607.17250) | Tencent · 73 | ✗ | 文学角色扮演 world model，领域无关（[abs](https://arxiv.org/abs/2607.17250)） |
| 21 | [MIMESIS: Learning User Simulators as Training Environments for Interactive Agents](https://arxiv.org/abs/2610.09484) | AI at Meta · 19 | ✅深读 | user sim: 用真实对话+13 种行为模式训练的用户模拟器作 RL 环境（[abs](https://arxiv.org/abs/2610.09484)） |
| 22 | [Recursive Synthesis for Long-Horizon Terminal Tasks](https://arxiv.org/abs/2608.05466) | Tencent Hunyuan · 242 | ✅深读 | task synthesis: 从已验证种子递归扩展 solution/verifier/instruction，难度递增（[abs](https://arxiv.org/abs/2608.05466)） |
| 23 | [VibeWorlding: Can Multimodal Agents Construct 3D Open Worlds End-to-End?](https://arxiv.org/abs/2608.15265) | Tencent · 51 | ✗ | 3D 世界构建 benchmark，领域远（[abs](https://arxiv.org/abs/2608.15265)） |
| 24 | [Atria Dawn: The Dawn of Agentic Superintelligence](https://arxiv.org/abs/2609.15818) | Intern Large Models · 411 | ✗ | 基座模型报告，Verifiable Experience Pipeline 描述过粗（[abs](https://arxiv.org/abs/2609.15818)） |
| 25 | [Mid-Harness: Scaling Actions Between Model and Harness for Terminal Agents](https://arxiv.org/abs/2609.39982) | NVIDIA · 105 | ✗ | 测试时 action 验证，非环境构建（[abs](https://arxiv.org/abs/2609.39982)） |
| 26 | [VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks](https://arxiv.org/abs/2610.00972) | Google · 48 | ◐浏览 | verifier: agentic verifier（分歧解析/共识挑战），无参考答案的长任务验证（[abs](https://arxiv.org/abs/2610.00972)） |
| 27 | [From Traces to Agentic Worlds: Agentic Language World Models for Interactive Environment Simulation](https://arxiv.org/abs/2610.06100) | Nanyang Technological University Singapore · 98 | ✅深读 | simulation: 从历史 traces 构建 worldbook，LLM world-model agent 充当环境（[abs](https://arxiv.org/abs/2610.06100)） |
| 28 | [Scaling Agentic Data for Long-Horizon Terminal Intelligence](https://arxiv.org/abs/2610.13166) | alibaba · 136 | ◐浏览 | task synthesis: 从真实专业工作出发、独立执行发现被预先完成的关键工作再重建环境（TerminalHorizon）（[abs](https://arxiv.org/abs/2610.13166)） |
| 29 | [SKT: Skill-Use Training at Scale via Verified Synthetic Data Generation](https://arxiv.org/abs/2608.02287) | Shanghai AI Laboratory · 31 | ◐浏览 | task synthesis: 技能→任务包+轨迹，规则/agent 双验证+修复（[abs](https://arxiv.org/abs/2608.02287)） |
| 30 | [Marathoner: Ultra-Long-Horizon Autonomous Intelligence](https://arxiv.org/abs/2609.34378) | Ant Group · 28 | ◐浏览 | task chaining: Multi-Task Chaining 合成超长任务；PR 作源（[abs](https://arxiv.org/abs/2609.34378)） |
| 31 | [Dockerless: Environment-Free Program Verifier for Coding Agents](https://arxiv.org/abs/2606.28436) | ByteDance · 81 | ◐浏览 | verifier: 免执行 agentic patch verifier；对办公'免环境 verifier'有启发（[abs](https://arxiv.org/abs/2606.28436)） |
| 32 | [Quo Vadis, World Modeling?](https://arxiv.org/abs/2608.02713) | Shanghai AI Laboratory · 37 | ✗ | world model 综述/立场（[abs](https://arxiv.org/abs/2608.02713)） |
| 33 | [EVOKE: Eliciting World Knowledge in Agents for Transferable Decision-Making](https://arxiv.org/abs/2609.38334) | Shanghai Jiao Tong University · 68 | ✗ | 训练方法（多目标排序引出世界知识），非环境构建（[abs](https://arxiv.org/abs/2609.38334)） |
| 34 | [Beyond Relevance-Centric Retrieval: Rubric-Oriented Document Set Selection and Ranking](https://arxiv.org/abs/2607.19747) | Tencent · 29 | ✗ | 检索文档集评估（[abs](https://arxiv.org/abs/2607.19747)） |
| 35 | [Masked Diffusion Language Models are Strong and Steerable Text-Based World Models for Agentic RL](https://arxiv.org/abs/2607.16204) | Patronus AI · 5 | ✅深读 | simulation: masked diffusion LM 作可操控文本 world model + 确定性状态检查 GRPO（[abs](https://arxiv.org/abs/2607.16204)） |
| 36 | [Environment-free Synthetic Data Generation for API-Calling Agents](https://arxiv.org/abs/2607.16900) | Apple · 14 | ✅深读 | simulation/data prep: 仅凭 API spec 由 LLM 模拟有状态后端合成轨迹（含 OfficeBench）（[abs](https://arxiv.org/abs/2607.16900)） |
| 37 | [OmegaUse-OfficeVal: Benchmarking LLM Agents on Long-Horizon Office-Suite Tasks with Economic Grounding](https://arxiv.org/abs/2607.27155) | Baidu · 7 | ◐浏览 | 办公 benchmark：rubric→code-based verifier、经济锚定；偏评测（[abs](https://arxiv.org/abs/2607.27155)） |
| 38 | [MatrAIx: Simulating the World with 8.3 Billion Persona Agents](https://arxiv.org/abs/2608.04205) | MatrAIx · 44 | ◐浏览 | user sim: 83 亿 persona 人群级模拟用户基础设施（[abs](https://arxiv.org/abs/2608.04205)） |
| 39 | [PlayWorld: Benchmarking World Models with Agent Players over Long-Horizon Objectives](https://arxiv.org/abs/2608.13552) | The University of Hong Kong · 43 | ✗ | 视频 world model 评测（[abs](https://arxiv.org/abs/2608.13552)） |
| 40 | [DRACO: Fine-Grained Credit Assignment with Dynamic Rubrics for Long-Horizon Agent Training](https://arxiv.org/abs/2609.04094) | IBM Research · 23 | ◐浏览 | reward: 动态 rubric + 步级 credit 分配（无 verifier 场景）（[abs](https://arxiv.org/abs/2609.04094)） |
| 41 | [ProgramDistill: From Interactive Web Apps to Verifiable Reference-Guided SWE Tasks](https://arxiv.org/abs/2609.18805) | Microsoft Research · 45 | ◐浏览 | task synthesis: 从可交互 web app 因子化出 replay 验证的特性任务（与 RecreationWorld 同族）（[abs](https://arxiv.org/abs/2609.18805)） |
| 42 | [DataSpace: Benchmarking Data Agents for Verifiable Analytics over Heterogeneous Workspaces](https://arxiv.org/abs/2608.03451) | HKUSTDial · 33 | ◐浏览 | DataSpace-Builder：执行落地的异构工作区任务构造 + 确定性表格评估器；数据分析办公相关（[abs](https://arxiv.org/abs/2608.03451)） |
| 43 | [ClawGym II: Exploring Black-Box RL on Agent Harness](https://arxiv.org/abs/2608.16798) | Renmin University of China · 34 | ◐浏览 | infra: 沙箱化 black-box harness RL（前缀树重建轨迹）（[abs](https://arxiv.org/abs/2608.16798)） |
| 44 | [MobilePA-Bench: Benchmarking Mobile Planner Agents on Complex Real-World Tasks](https://arxiv.org/abs/2608.23035) | Tongyi-MAI · 34 | ◐浏览 | 有状态移动工具沙箱 benchmark；偏评测（[abs](https://arxiv.org/abs/2608.23035)） |
| 45 | [Terminal-Universe: Turning Agent Trajectories into Scalable Terminal Environments](https://arxiv.org/abs/2609.04148) | Qwen · 223 | ✅深读 | env synthesis: 从既有 agent 轨迹回放文件操作重建可执行工作区并再合成任务（[abs](https://arxiv.org/abs/2609.04148)） |
| 46 | [WeClawArena: An Auditable Sandbox and Benchmark for Cross-User Agents Collaboration and Security in Human-Centered Agent Networks](https://arxiv.org/abs/2608.03499) | Carnegie Mellon University · 8 | ◐浏览 | 多用户 agent 协作沙箱+安全审计；偏评测（[abs](https://arxiv.org/abs/2608.03499)） |
| 47 | [UniClawBench: A Universal Benchmark for Proactive Agents on Real-World Tasks](https://arxiv.org/abs/2607.08768) | The University of Hong Kong · 27 | ◐浏览 | user sim: executor/hidden supervisor/user agent 闭环、不泄露评分标准（[abs](https://arxiv.org/abs/2607.08768)） |
| 48 | [Xiaomi-GUI-0 Technical Report](https://arxiv.org/abs/2606.31410) | Xiaomi Research · 7 | ◐浏览 | infra: 真机为主的混合基础设施 + 错误驱动数据飞轮（移动端）（[abs](https://arxiv.org/abs/2606.31410)） |
| 49 | [Prospective Hindsight: Self-Calibrating Reinforcement Learning via Prediction-Reality Gaps](https://arxiv.org/abs/2610.02740) | Salesforce AI Research · 2 | ✗ | RL 校准信号（[abs](https://arxiv.org/abs/2610.02740)） |
| 50 | [AREX: Towards a Recursively Self-Improving Agent for Deep Research](https://arxiv.org/abs/2607.21461) | Beijing Academy of Artificial Intelligence · 139 | ✗ | 深度研究 agent 训练（[abs](https://arxiv.org/abs/2607.21461)） |
| 51 | [FACET: Preserving Source Intent and Executable State in Terminal Task Synthesis](https://arxiv.org/abs/2608.18580) | university of science and technology  of china · 114 | ◐浏览 | task synthesis: 以容器状态为共享 grounding 生成 instruction/solution/verifier（FACET）（[abs](https://arxiv.org/abs/2608.18580)） |
| 52 | [Scaling Automatic Research Agents via World Models](https://arxiv.org/abs/2608.12564) | University of Illinois at Urbana-Champaign · 431 | ◐浏览 | simulation: world model 替代昂贵执行做 RL + 去偏/去噪（AutoResearch）（[abs](https://arxiv.org/abs/2608.12564)） |
| 53 | [MiniWorld: Democratizing the Training of Video World Models from Scratch](https://arxiv.org/abs/2608.01127) | Peking University · 19 | ✗ | 视频 world model 训练（[abs](https://arxiv.org/abs/2608.01127)） |
| 54 | [One Success Isn't Reliability: Thinkingbox, a Sandbox and Benchmark for Agents in Stateful Business Workflows](https://arxiv.org/abs/2608.19741) | Microsoft · 9 | ✅深读 | verifier/infra: MCP 隔离会话 + 后端终态检查，拒绝多余副作用；业务流程（保险/IT/HR）（[abs](https://arxiv.org/abs/2608.19741)） |
| 55 | [AgentJudgeBench: A Multi-Difficulty Benchmark for Evaluating LLM Judges on Agentic Tool-Calling](https://arxiv.org/abs/2608.26623) | ServiceNow-AI · 18 | ◐浏览 | verifier: LLM judge 在工具调用 DAG 上的可靠性天花板（[abs](https://arxiv.org/abs/2608.26623)） |
| 56 | [IterSynth: Rethinking Deep Search Agents via Role-Decoupled Iterative Synthesis](https://arxiv.org/abs/2609.29444) | REAL Lab · 8 | ✗ | deep search agent 架构（[abs](https://arxiv.org/abs/2609.29444)） |
| 57 | [Safety Testing LLM Agents at Scale: From Risk Discovery to Evidence-Grounded Verification](https://arxiv.org/abs/2607.01793) | Ant Group · 7 | ◐浏览 | 安全测试：组合式生成可执行 safety case + 证据型 verifier（[abs](https://arxiv.org/abs/2607.01793)） |
| 58 | [Environment Evolution for Terminal Agents](https://arxiv.org/abs/2609.04128) | Tencent Hunyuan · 16 | ◐浏览 | task synthesis/curriculum: off-policy 环境难度演化（[abs](https://arxiv.org/abs/2609.04128)） |
| 59 | [Scores Alone Do Not Prove Discovery: The Discovery Certification Protocol for Auditing AI Research Agents](https://arxiv.org/abs/2609.09219) | Carnegie Mellon University · 15 | ✗ | 研究 agent 发现认证协议（[abs](https://arxiv.org/abs/2609.09219)） |
| 60 | [SCALECUA: Scaling Computer Use Agents with Verifiable Task Synthesis and Efficient Online RL](https://arxiv.org/abs/2607.11185) | None · None | ◐浏览 | task synthesis: VeriGen 多 agent docker 交互生成可验证 CUA 任务 + Frontier Sampling（[abs](https://arxiv.org/abs/2607.11185)） |
| 61 | [Verifiable Social Reasoning for LLM Assistants](https://arxiv.org/abs/2609.17496) | Google · 13 | ✗ | 社会推理模拟（[abs](https://arxiv.org/abs/2609.17496)） |
| 62 | [Agent-Editing World Model: Rethinking World Modeling for LLM Agents](https://arxiv.org/abs/2609.28416) | Renmin University of China · 13 | ✗ | agent 推理编辑 world model，非环境（[abs](https://arxiv.org/abs/2609.28416)） |
| 63 | [FinanceHarness: Autonomous Financial Deep Research Framework](https://arxiv.org/abs/2607.27853) | unknown · 11 | ◐浏览 | 金融 deep research：point-in-time 防未来信息泄露 + rubric；leak prevention 可借鉴（[abs](https://arxiv.org/abs/2607.27853)） |
| 64 | [SkillGym: Training Skill-Use Agents with Automatic Verifiable Environment Generation](https://arxiv.org/abs/2609.37539) | unknown · 5 | ◐浏览 | task synthesis: builder-reviewer 构建难度可控技能环境（SkillGym）（[abs](https://arxiv.org/abs/2609.37539)） |
| 65 | [EngiWorld: What Can Frontier Agents Deliver in Professional Engineering Environments?](https://arxiv.org/abs/2609.37686) | Zhiman AI · 53 | ◐浏览 | 工程软件 benchmark，domain-verifier suite（[abs](https://arxiv.org/abs/2609.37686)） |
| 66 | [LLM-as-a-Verifier: A General-Purpose Verification Framework](https://arxiv.org/abs/2607.05391) | Unknown · 10 | ◐浏览 | verifier: logit 期望连续评分的 LLM-as-Verifier（[abs](https://arxiv.org/abs/2607.05391)） |
| 67 | [Physis-Lang: Self-Evolving Language as a Physical Representation for Video World Model](https://arxiv.org/abs/2609.40358) | NVIDIA · 10 | ✗ | 视频物理 world model（[abs](https://arxiv.org/abs/2609.40358)） |
| 68 | [ToolHazard: Scaling Adversarial Environments for Security Evaluation and Alignment of LLM-based Agents](https://arxiv.org/abs/2608.11878) | Peking University · 9 | ◐浏览 | env synthesis(安全): Environment Simulator+Attacker+User Simulator 合成可执行有状态环境（[abs](https://arxiv.org/abs/2608.11878)） |
| 69 | [StartupBench: Benchmarking General-Purpose Agents on Market-Validated End-to-End Workflows](https://arxiv.org/abs/2608.17800) | ByteDance Seed · 8 | ◐浏览 | 市场验证的专业工作流 benchmark + rubric（[abs](https://arxiv.org/abs/2608.17800)） |
| 70 | [Qwen-Planner-Agent: A Closed-Loop AI-for-AI Framework for Real-World Mobile Planner Agents](https://arxiv.org/abs/2609.29892) | Tongyi-MAI · 9 | ◐浏览 | infra/data flywheel（移动规划，human-gated）（[abs](https://arxiv.org/abs/2609.29892)） |
| 71 | [AgenticGen: Reward-Guided Agentic Video Generation for Advertising](https://arxiv.org/abs/2609.09187) | ByteDance · 7 | ✗ | 广告视频生成（[abs](https://arxiv.org/abs/2609.09187)） |
| 72 | [From Economic Agents to Agentic Economies: A Systems Blueprint for Economic World Models](https://arxiv.org/abs/2608.06020) | FreedomAI · 35 | ✗ | 经济 world model 路线图/综述（[abs](https://arxiv.org/abs/2608.06020)） |
| 73 | [RSIAgent: Autonomous Exploration for Recursive Self-improvement in New Environments](https://arxiv.org/abs/2609.15364) | AetherLabs-AI · 67 | ✗ | 训练外记忆探索（[abs](https://arxiv.org/abs/2609.15364)） |
| 74 | [From RLVR to RLSVR: Task Transformation Induces Self-Verifiable Rewards for Open-Ended LLM Self-Improvement](https://arxiv.org/abs/2607.23802) | Unknown · 105 | ◐浏览 | reward: 把开放任务转成可自验证的 self-play 代理环境（SpyRL）（[abs](https://arxiv.org/abs/2607.23802)） |
| 75 | [Mental World Modeling](https://arxiv.org/abs/2607.27201) | Mental World Model · 105 | ✗ | 心智 world model 理论（[abs](https://arxiv.org/abs/2607.27201)） |
| 76 | [HarnessEval-W: Agentifying the Evaluation of Visual Worlds](https://arxiv.org/abs/2608.16859) | MirroS · 111 | ✗ | 视觉 world model 评测（[abs](https://arxiv.org/abs/2608.16859)） |
| 77 | [Apodex 1.1: Scaling Agentic Intelligence for Complex Work](https://arxiv.org/abs/2608.23283) | Apodex · 172 | ◐浏览 | Environment Scaling（文件/搜索/代码环境）技术报告，细节不明（[abs](https://arxiv.org/abs/2608.23283)） |
| 78 | [AREX-2: Advancing Self-Improving Agents through Long-Horizon Reflective Tasks](https://arxiv.org/abs/2609.38288) | Beijing Academy of Artificial Intelligence · 122 | ✗ | 反思型长任务轨迹合成（ML/算法）（[abs](https://arxiv.org/abs/2609.38288)） |
| 79 | [AgentSWE: Can Coding Agents Build the Agent You Actually Want?](https://arxiv.org/abs/2610.13361) | Unknown · 202 | ✗ | agent 软件工程 benchmark（[abs](https://arxiv.org/abs/2610.13361)） |
| 80 | [What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents](https://arxiv.org/abs/2608.27260) | unknown · 56 | ◐浏览 | 数据生成综述：(E,q,τ,v) 因子化 + ACE 视角；可作 taxonomy 参考（[abs](https://arxiv.org/abs/2608.27260)） |
| 81 | [CompoWorld: Compositional Environment Scaling for General Agents](https://arxiv.org/abs/2609.33665) | AllSpark Research · 30 | ✅深读 | env synthesis: 服务库组合 + 依赖图 random walk 生成跨服务任务，world model 兜底难实现工具（[abs](https://arxiv.org/abs/2609.33665)） |
| 82 | [CADWorld: Computer-Use Benchmark for Long-Horizon Computer-Aided Design](https://arxiv.org/abs/2609.16251) | unknown · 5 | ◐浏览 | FreeCAD benchmark；artifact 级可执行检查（[abs](https://arxiv.org/abs/2609.16251)） |
| 83 | [WorldAuditBench: Interactive 3D World Auditing with Multimodal Agents](https://arxiv.org/abs/2609.40325) | University of California, Santa Barbara · 93 | ✗ | 3D 世界审计（[abs](https://arxiv.org/abs/2609.40325)） |
| 84 | [Programmable World Model](https://arxiv.org/abs/2609.10540) | Alaya Lab · 81 | ✗ | 可编程视频 world model（[abs](https://arxiv.org/abs/2609.10540)） |
| 85 | [EVOHARNESSBENCH: Can Your Agents Keep Pace with an Evolving Harness?](https://arxiv.org/abs/2609.04280) | Salesforce AI Research · 4 | ✗ | harness 演化 benchmark（[abs](https://arxiv.org/abs/2609.04280)） |
| 86 | [World Observer: Joint Actor-Observer Generation for Persistent World Modeling](https://arxiv.org/abs/2610.02162) | KAIST AI · 64 | ✗ | 视频 world model（[abs](https://arxiv.org/abs/2610.02162)） |
| 87 | [The Physics of Multi-Turn Long-Horizon Planning: From Pre-training to Post-training via Single- and Multi-Teacher On-Policy Agentic Distillation](https://arxiv.org/abs/2607.24720) | Chinese Academic of Science Institute of Automation · 20 | ✗ | 规划能力受控研究（[abs](https://arxiv.org/abs/2607.24720)） |
| 88 | [ProgramGym: Scaling Training Environments for Long-Horizon Program Reproduction Agents](https://arxiv.org/abs/2610.13395) | ProgramGym · 49 | ◐浏览 | env synthesis: 从仓库构建程序复现环境+黑盒测试修复（ProgramGym）（[abs](https://arxiv.org/abs/2610.13395)） |
| 89 | [ComBodied Agents: a New Paradigm of Human-Centric Agentic AI](https://arxiv.org/abs/2608.10915) | Unknown · 189 | ✗ | 人本 agent 范式立场文（[abs](https://arxiv.org/abs/2608.10915)） |

## 2. 方法卡片

> 来源深度图例：**L3** = 读了仓库代码/prompt；**L2** = 读了仓库 README/docs；**L1** = 只有 arXiv 摘要（+ 可能 1 次 WebSearch 二手摘要）。arXiv 全文本环境不可达，所以所有「作者报告」数字都来自摘要或仓库 README，链接已逐条注明。

### A. 真实执行型环境合成（代码/规格 → 可运行应用）

#### A1. Echoverse: Deep, Evolving Environments for Training Computer-Use Agents at Scale
arXiv 2607.28074 · 2026-07-31 · Microsoft Research · HF 9↑ · [abs](https://arxiv.org/abs/2607.28074) · [repo](https://github.com/microsoft/Echoverse) · 来源深度 **L3**（README + harness/prompts.py + 任务 jsonl）
- **解决的环节**：env synthesis + task synthesis + verifier + env/model co-evolution（[abs](https://arxiv.org/abs/2607.28074)）
- **方法**
  - 把 specification「编译」成有状态应用，任务按应用自己的数据库判分；co-evolution loop 把每条已判分 rollout 读两遍：一遍当作对环境/任务/verifier 的修复信号，一遍当作模型训练信号（[abs](https://arxiv.org/abs/2607.28074)）。
  - 每个环境 = FastAPI 后端 + Vite/React 前端 + SQLite；两类世界：full-domain worlds（保留共享线程、权限、审计历史、后果性写入等因果结构）与 capability worlds（把单一控件如 date picker / nested filter 在多种布局下反复训练），后者分 ID/OOD split（[README](https://github.com/microsoft/Echoverse/blob/main/README.md)）。
  - 完整 Echo 家族有 10 个环境（EchoMail、EchoCalendar、EchoChat、EchoML、EchoForge、EchoBank、EchoCare、EchoForum、EchoTunes、EchoStay），公开仓库只放出 EchoStay、EchoForge 和两个 capability world（[README](https://github.com/microsoft/Echoverse/blob/main/README.md)）。
  - 种子数据来源：EchoStay 用改造过的 InsideAirbnb 数据，EchoForge 用 WebArena 语料（[README](https://github.com/microsoft/Echoverse/blob/main/README.md)）。
  - 任务 schema：每条任务带 `task_type`(read/write)、`reference_answer` 或 `reference_state_change`、`verification_query`(SQL)、`required_entities`、`grounding_evidence`、`acting_user_id`，也就是答案是从真实 DB「铸造」出来的（[tasks jsonl](https://github.com/microsoft/Echoverse/blob/main/envs/echostay/tasks/test_tasks.jsonl)，[README §Verification](https://github.com/microsoft/Echoverse/blob/main/README.md)）。
  - 判分：read 任务由 LLM judge 比较答案与参考值，write 任务由 LLM judge 比较 `sqldiff` 输出与期望状态变化；judge 只用来吸收 UI 层的格式/四舍五入差异（[README](https://github.com/microsoft/Echoverse/blob/main/README.md)，[prompts.py](https://github.com/microsoft/Echoverse/blob/main/harness/prompts.py)）。
  - Infra：每个实例拷贝一份 seed DB、用 OS 分配端口，无需 Docker 即可并发多实例；结束时导出 `final_db_state.db`（[harness/README](https://github.com/microsoft/Echoverse/blob/main/harness/README.md)）。
  - 成本：摘要和 README 都没有给出每个环境的成本（「无出处，待核」）。
- **验证（sim-to-real）**：同一领域里，浅环境让 live-site 准确率从 80.0 降到 75.0，深环境则提升到 85.0（另一组从 48.0 升到 65.0）；在多种渲染下练同一个控件，能迁移到未见过的 widget 家族和开放网页（[abs](https://arxiv.org/abs/2607.28074)）。
- **关键结果**：在 12 个环境上训练的 9B 模型，14 个评测 split 上从 36.5% 提升到 67.1%，与教它的更大 frontier 模型差距在 14 个点以内；只修复一个环境，就能让在该环境上训练的模型从 16.2% 升到 38.5%（[abs](https://arxiv.org/abs/2607.28074)）。公开 6 个环境上 Fara1.5-9B 总体为 71.6%（517/722）（[README](https://github.com/microsoft/Echoverse/blob/main/README.md)）。
- **局限与红旗**
  - write 判分 prompt 明确写着「多余改动没关系，只要必需改动都在」（"Extra changes are OK as long as the required change was made"），因此**不惩罚副作用**；对办公场景（误删、误发）是明显的可被 hack 点（[prompts.py](https://github.com/microsoft/Echoverse/blob/main/harness/prompts.py)）。
  - 判分依赖 LLM judge（推荐 gpt-4o），不是纯确定性检查（[harness/README](https://github.com/microsoft/Echoverse/blob/main/harness/README.md)）。
  - factory 本身（spec→app 编译器、co-evolution loop）没有开源（[README](https://github.com/microsoft/Echoverse/blob/main/README.md)）。
  - HF 热度很低（9↑）（[abs](https://arxiv.org/abs/2607.28074)）。
- **迁移到办公/专业场景**：Echo 家族本身就有 Mail/Calendar/Chat/Bank（[README](https://github.com/microsoft/Echoverse/blob/main/README.md)），可直接照搬到 CRM/ERP/报销系统。
  - 用「SQLite + 任务内嵌 `verification_query`」铸造答案，把判分落到 DB diff 上。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.28074)）
  - 再加一条**副作用白名单 diff 检查**（与 Thinkingbox 的「拒绝多余效果」结合，见 D1）。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.28074)）
  - capability world 的思路适合专门练表格筛选器、日期控件、多级审批表单等高失败率控件。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.28074)）
- **评级**：**必读**（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2607.28074)）

#### A2. SoftwareGym: Scaling CUA Training with Diverse Synthesized Software Environments（全量池补充，不在 C 表）
arXiv 2610.12611 · 2026-10-12 · 上海交大 · HF 85↑ · [abs](https://arxiv.org/abs/2610.12611) · [repo](https://github.com/MrKiing-Jin/SoftwareGym) · 来源深度 **L3**（README + agent/prompt/*.json）
- **解决的环节**：env synthesis（原生桌面 GUI 应用）+ task synthesis + 运行时验证与修复（[abs](https://arxiv.org/abs/2610.12611)）
- **方法**
  - 四阶段流水线（[README](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)）：
    1. **Design**：FunctionDesigner 写需求规格；Style/SubStyle Designer 产出 N 套 Avalonia `.axaml` 风格蓝图；Icon Designer 生成 SVG 图标并设硬校验门。
    2. **Build**：Coder（.NET 8 + Avalonia 11）实现，DevCoder 审查修复；设计和编码都走 Codex CLI。
    3. **Evaluate**：EvalTaskGenerateAgent 生成 GUI 测试用例，GUIEval 在 OSWorld 同款 Docker/Ubuntu VM 中用 GUI agent 实操。
    4. **Iterate**：v1→v3 轮次，每轮把评测 summary 回灌给 Coder 做增量修复。
  - **可测试性契约**（关键可迁移点）：Coder prompt 要求每个合成应用的 `release/run.sh` 必须支持 `--smoke-test / --dump-state / --reset-state / --seed-state / --open / --new-from / --import-data`，所有 GUI 与运行时状态统一持久化到 `app_data/config.yaml`（[Coderprompt.json](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/prompt/Coderprompt.json)）。
  - 评测任务生成前先跑 `--dump-state`、读 config、列 SQLite 表，得到真实 state schema；`infra_checks` 的字段名必须从中逐字拷贝（[Evaltaskgenerateprompt.json](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/prompt/Evaltaskgenerateprompt.json)）。
  - 训练任务（TaskDesigner）只能使用 GUIEval summary 证明「稳定可用」的功能，标为 failed/blocked/unsupported 的功能一律不得入题；手册与 summary「仅供内部阅读，不得写入任务」（[Taskdesignerprompt.json](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/prompt/Taskdesignerprompt.json)）。
  - 与 OSWorld 对齐：用相同的 Docker VM 基础设施与 Ubuntu 桌面、截图 + PyAutoGUI 动作（[README](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)）。
  - 成本：有 `cost_summary.json` 记录 token，但 README 未给出每个应用的成本数字（[README](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)）（金额「无出处，待核」）。
- **验证（sim-to-real）**：用合成环境轨迹训练后，在严格 OOD 的 OSWorld 上 Pass@3 从 41.39% 升到 56.97%（[abs](https://arxiv.org/abs/2610.12611)）。
- **关键结果**：合成了 12 类共 182 个应用，GUI 任务平均通过率 91.5%；另建 SoftwareGym-Bench（120 任务），在其上达到 40.0%（[abs](https://arxiv.org/abs/2610.12611)）。
- **局限与红旗**
  - 主指标是 **Pass@3**，不是 Pass@1（[abs](https://arxiv.org/abs/2610.12611)）。
  - 依赖 Codex CLI、OSWorld 35GB qcow2 和 Responses API 端点，复现门槛高（[README](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)）。
  - 合成的是「仿品」应用，与真实 Office 文件格式兼容性的保真度未知（「无出处，待核」）。
- **迁移到办公/专业场景**：「每个合成应用必须暴露 dump/reset/seed 状态 CLI」这份契约可以直接写进合成发票、报销、CRM 桌面应用的 Coder prompt；用 `--seed-state` 装入任务初始数据，`--dump-state` 当 state checker，做到 reset 与验证都确定化。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2610.12611)）
- **评级**：**必读**（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2610.12611)）

#### A3. RecreationWorld: Scalable and Verifiable Environments for Hybrid Computer-Use Agents
arXiv 2609.22000 · 2026-09-21 · Qwen · HF 63↑ · [abs](https://arxiv.org/abs/2609.22000) · [repo](https://github.com/QwenLM/RecreationWorld) · 来源深度 **L3**（README + recreation_prompt.py + vlm_judge.py + gt_generator.py）
- **解决的环节**：env synthesis（开源 app → recreation 任务）+ verifier（以运行中的 reference 作 oracle）（[abs](https://arxiv.org/abs/2609.22000)）
- **方法**
  - 任务给 agent 一个高层请求、一个可交互的运行中 reference，以及 GUI 控制和编码两套工具；agent 自己安排 explore–implement–verify 循环（[README](https://github.com/QwenLM/RecreationWorld/blob/main/README.md)）。
  - 评分用冻结的 programmatic + visual assertions，只看可观察行为、不看源码相似度（[README](https://github.com/QwenLM/RecreationWorld/blob/main/README.md)）。
  - 每条 assertion 先在 reference 上验证，再经人工审核，然后才冻结（[abs](https://arxiv.org/abs/2609.22000)）。
  - 五平台各用原生无障碍接口做断言：AT-SPI / AXUIElement / UI Automation / UiAutomator / 浏览器断言（[README](https://github.com/QwenLM/RecreationWorld/blob/main/README.md)）。
  - **防泄露/防作弊**：统一 prompt 模板禁止 agent 检查 reference 二进制或进程元数据、禁止 /proc 内省、禁止联网或下载、禁止压制 accessibility；还要求暴露与 reference 相同的 widget 名称和角色（[recreation_prompt.py](https://github.com/QwenLM/RecreationWorld/blob/main/scripts/core/recreation_prompt.py)）。
  - 视觉 judge 系统提示要求「仅当完全满足才 pass，缺失、占位或不匹配都算 fail」（[vlm_judge.py](https://github.com/QwenLM/RecreationWorld/blob/main/scripts/common/vlm_judge.py)）。
  - Web GT 截图生成时固定 Math.random 种子并冻结动画，保证确定性（[gt_generator.py](https://github.com/QwenLM/RecreationWorld/blob/main/scripts/web/evaluation/gt_generator.py)）。
  - Linux/Web 沙箱跑在阿里云 FC 的 E2B 兼容沙箱上（[sandbox.md](https://github.com/QwenLM/RecreationWorld/blob/main/docs/providers/sandbox.md)）。
- **验证（sim-to-real）**：训练后在 5 个 OOD 的 coding / hybrid CUA benchmark 上都有提升，模型也更常去验证自己渲染出的产物（[abs](https://arxiv.org/abs/2609.22000)）。具体增益数字在摘要截断处之后，未获取（「无出处，待核」）。
- **关键结果**：RecreationBench 共 250 任务，5 平台各 50。GPT-6 Astra 平均 58.06%，Claude Opus 5 44.16%；GPT-6 Astra 每任务估计成本 115.80 美元（[README](https://github.com/QwenLM/RecreationWorld/blob/main/README.md)）。
- **局限与红旗**
  - 每任务评测/推理成本极高，按上面 GPT-6 Astra 约 116 美元/任务计（[README](https://github.com/QwenLM/RecreationWorld/blob/main/README.md)）。
  - 训练轨迹生成管线与训练配方没有出现在公开 README 中（[README](https://github.com/QwenLM/RecreationWorld/blob/main/README.md)）。
  - 「重建一个 app」与办公日常任务分布差异较大（推断）。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2609.22000)）
- **迁移到办公/专业场景**：核心可迁移的是「**running reference = oracle**」：（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2609.22000)）
  - 对内部老旧系统（如审批或报表工具），可以把现网副本当 reference，自动生成「行为 assertion」用于回归评测或训练「复刻/迁移」agent。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2609.22000)）
  - 在 reference 上先跑通 assertion 再冻结，就是低成本的 verifier 自检。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2609.22000)）
  - 用无障碍树做断言，适用于 Excel/WPS 等桌面应用。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2609.22000)）
- **评级**：**必读**（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2609.22000)）

#### A4. CodeMidas: Scaling Agentic Coding RL Environments from Code Itself
arXiv 2609.22068 · 2026-09-21 · Xiaomi MiMo · HF 98↑ · [abs](https://arxiv.org/abs/2609.22068) · 无仓库 · 来源深度 **L1**（摘要 + 1 次 WebSearch）
- **解决的环节**：env synthesis + task synthesis + verifier（源码 → 可执行 RL 环境）（[abs](https://arxiv.org/abs/2609.22068)）
- **方法**
  - 只以源码作为任务输入；agent 先探索已实现的功能、写行为规格，再基于原代码的执行结果构造测试，最后经执行检查和多次 solution rollout 验证、过滤候选任务（[abs](https://arxiv.org/abs/2609.22068)）。
  - 二手资料称 post-rollout 过滤包括：用 adversarial rollouts 检查泄露、用 solution review 核对 verifier 判定是否符合需求、用 rollout 成功率指导选题（[arXiv PDF 经 WebSearch 摘要（二手）](https://arxiv.org/pdf/2609.22068)）。
- **验证（sim-to-real）**：GRPO 训练 MiMo-V2.5 后，五个下游 benchmark 全部提升：DeepSWE +11.7%、ProgramBench +17%、Terminal-Bench v2.1 +8.5%（[abs](https://arxiv.org/abs/2609.22068)）。
- **关键结果**：5,545 个训练任务，来自 3,185 个开源代码库，覆盖 23 种语言、15 个技术领域；高质量任务越多效果越好（[abs](https://arxiv.org/abs/2609.22068)）。
- **局限与红旗**：无代码、无数据；每任务成本未公开（「无出处，待核」）。
- **迁移到办公/专业场景**：「用原系统执行结果当测试期望值」可迁移为：对已有业务脚本、Excel 宏或报表 SQL，由 agent 写功能规格、用原实现跑出期望输出、再挖空让 agent 重建或修改。adversarial rollout 查泄露的做法适用于任何自动出题管线。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2609.22068)）
- **评级**：值得浏览（方法简洁有效，但证据只到摘要）（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2609.22068)）

#### A5. Terminal-Universe: Turning Agent Trajectories into Scalable Terminal Environments
arXiv 2609.04148 · 2026-09-04 · Qwen · HF 223↑ · [abs](https://arxiv.org/abs/2609.04148) · 无仓库 · 来源深度 **L1**（摘要 + 1 次 WebSearch）
- **解决的环节**：env synthesis（从 trace 重建**可执行**环境）+ task synthesis（breadth/depth 扩展）（[abs](https://arxiv.org/abs/2609.04148)）
- **方法**
  - 核心观察：既有轨迹里的工具执行历史暴露了它所运行环境的结构和内容（[abs](https://arxiv.org/abs/2609.04148)）。
  - 回放轨迹中记录的文件操作，恢复每个文件被 agent 修改前的样子，得到部分 workspace；再由 completion agent 补齐缺失的文件和依赖（[abs](https://arxiv.org/abs/2609.04148)）。
  - 在恢复的 workspace 上既重建原意图任务，也合成全新任务（[abs](https://arxiv.org/abs/2609.04148)）。
  - Breadth：挖掘相关环境之间的有向依赖，合成跨多个代码库的查询（[abs](https://arxiv.org/abs/2609.04148)）。
  - Depth：把单轮查询扩展成多轮（[abs](https://arxiv.org/abs/2609.04148)）。
  - 二手资料：用 Qwen3.7-Max 作 teacher 为每个任务 roll out 解答，每个任务带 verifier，只保留通过的轨迹（[WebSearch 结果页（二手）](https://www.developersdigest.tech/blog/terminal-universe-agent-trajectories)）。
- **验证与关键结果（二手）**：得到 37.3k 个 task-sufficient 环境；Qwen3.5-27B 微调后 Terminal-Bench 2.1 +11.9、EvoCode-Bench v2 MT@4 +13.8；在重建环境中重新求解远好于直接模仿原轨迹（[HF paper page（二手，经 WebSearch）](https://huggingface.co/papers/2609.04148)）。
- **局限与红旗**：数字只来自二手摘要，未经核对；completion agent 补出的文件可能偏离真实环境（推断，「无出处，待核」）。
- **迁移到办公/专业场景**：企业里大量现成的 RPA 日志、Copilot 调用日志、工单处理日志 → 回放文件和表格操作，重建「操作前」的工作区（Excel/共享盘快照）→ 在同一工作区上派生多任务。比从零合成更贴近真实数据分布。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2609.04148)）
- **评级**：**必读**（思路对办公「日志多、环境不可得」的现实最对口）（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2609.04148)）

#### A6. CompoWorld: Compositional Environment Scaling for General Agents
arXiv 2609.33665 · 2026-09-29 · AllSpark Research · HF 30↑ · [abs](https://arxiv.org/abs/2609.33665) · 仓库 clone 失败、raw README 404 · 来源深度 **L1**（摘要 + 1 次 WebSearch）
- **解决的环节**：env synthesis（服务库）+ task synthesis（跨服务组合）+ reward（rubric）（[abs](https://arxiv.org/abs/2609.33665)）
- **方法**
  - 由 coding agent 把 tool specification 实现成带 typed state 和共享接口的「已验证服务」；无法可靠实现的工具交给 world model 兜底（[abs](https://arxiv.org/abs/2609.33665)）。
  - 在服务依赖图上做 random walk，生成需要跨服务传递信息的任务并验证（[abs](https://arxiv.org/abs/2609.33665)）。
  - 已验证轨迹用于 SFT；RL 阶段的 Completion-Focused Rubric Reward 强调组内通过率较低的 criteria（[abs](https://arxiv.org/abs/2609.33665)）。
- **验证与关键结果**：448 个服务、10,130 个工具；用 3K SFT 轨迹 + 1K RL 任务训练 Qwen3.6-35B-A3B，8 个 benchmark 平均 +9.17；在 AutomationBench 上超过 Claude Opus 4.6（[abs](https://arxiv.org/abs/2609.33665)）。
- **局限与红旗**：二手报道指出摘要没有列出 8 个 benchmark、没有分项增益，也不清楚服务是包装真实 API 还是自包含 mock（[aiweekly（二手）](https://aiweekly.co/alerts/compoworlds-35b-agent-beats-claude-opus-46-on-automationbench)）。
- **迁移到办公/专业场景**：办公工作流天然跨服务（邮件→CRM→日历→表格）。可以先做「服务库」（每个服务有 typed state 并可 reset），再在依赖图上 random walk 生成跨系统任务；难以实现的长尾 SaaS 用 world model 兜底。这是「真实执行 + 模拟」的混合样板。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2609.33665)）
- **评级**：**必读**（组合式扩展是办公 env 规模化最实用的方案；但细节待全文核实）（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2609.33665)）

#### A7. VHD-Play: Generating Agentic RL Environments from Solved Mechanisms
arXiv 2609.27321 · 2026-09-24 · Qwen · HF 8↑ · [abs](https://arxiv.org/abs/2609.27321) · 无仓库 · 来源深度 **L1**（摘要 + 1 次 WebSearch，无新增信息）
- **解决的环节**：env + task + verifier 一体生成（先有解后有环境）（[abs](https://arxiv.org/abs/2609.27321)）
- **方法**
  - 先采样并求解一个数学模型，再由 corpus-grounded setter 把它的决策过程渲染成有状态工具；可执行的动力学与轨迹打分 reference 继承自同一个已解模型（[abs](https://arxiv.org/abs/2609.27321)）。
  - 对比了「把问题写成文字题」与「有状态、公开或隐藏参数」两种版本（[abs](https://arxiv.org/abs/2609.27321)）。
- **验证**：在三个训练族之外的未见实例和 8 个未见机制族上都有提升，并外推到通用 function calling、旅行规划和 365 天电商 benchmark；在 E-Commerce Bench 上训练后的 checkpoint 全程未破产，且超过 Qwen3.7-Max（[abs](https://arxiv.org/abs/2609.27321)）。
- **关键结果**：3,300 个环境，每个成本仅几美分；Qwen3.6-35B-A3B 在五族诊断上平均分从 0.204 升到 0.815；可学习的差距大部分来自有状态交互，而不是底层解题能力（[abs](https://arxiv.org/abs/2609.27321)）。
- **局限与红旗**：0.204→0.815 是在**自家生成族**的诊断集上测的；外部 benchmark 只有定性描述（[abs](https://arxiv.org/abs/2609.27321)）；HF 热度低。
- **迁移到办公/专业场景**：适合有数学内核的专业任务，例如库存补货、现金流排程、预算分配、定价。先用 LP/动态规划求出最优策略，再包装成「ERP 工具 + 隐藏参数」环境，最优值就是 reference oracle，天然防 judge 偏差。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2609.27321)）
- **评级**：值得浏览（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2609.27321)）

#### A8. DeskForge: Dense Supervision from Desktop Environments for Computer-Use Agents（全量池补充，不在 C 表）
arXiv 2610.02320 · 2026-10-06 · Docling（IBM Research Zurich / ETH）· HF 7↑ · [abs](https://arxiv.org/abs/2610.02320) · [repo](https://github.com/Saidgurbuz/deskforge) · 来源深度 **L2**
- **解决的环节**：real-app 环境组合 + 感知/grounding 数据生成（[abs](https://arxiv.org/abs/2610.02320)）
- **方法**
  - 「生成桌面而不是录制桌面」：把真实 Linux 应用组合成受控多窗口场景，由 seed 决定应用、初始状态、内容、窗口布局与层叠、外观和分辨率（[README](https://github.com/Saidgurbuz/deskforge/blob/main/README.md)）。
  - 融合截图、无障碍树和窗口几何，生成考虑遮挡的逐元素密集标注；每次点击都记录为 (S_t, a_t, S_t+1) 转移（[README](https://github.com/Saidgurbuz/deskforge/blob/main/README.md)）。
  - 每个场景运行在独立的 headless Xvfb 会话里，无需 root（[README](https://github.com/Saidgurbuz/deskforge/blob/main/README.md)）。
- **验证（sim-to-real）**：Qwen3.5-4B 在 ScreenSpot-Pro 上 +11.51、OSWorld-G 上 +10.11；固定 planner 时，WebArena-Infinity 从 31/119 升到 50/119，OpenApps 从 3/100 升到 15/100（[abs](https://arxiv.org/abs/2610.02320)）。
- **关键结果**：DeskForge-1M 含 1.21M 观测、159.7M 元素实例、917K 次点击转移（[README](https://github.com/Saidgurbuz/deskforge/blob/main/README.md)）。
- **局限与红旗**：只解决 grounding/单步转移，没有任务级 verifier（[README](https://github.com/Saidgurbuz/deskforge/blob/main/README.md)）。
- **迁移到办公/专业场景**：把 LibreOffice Calc/Writer、邮件客户端、PDF 阅读器组合成多窗口办公桌面，批量生成「在被遮挡的表格里定位单元格/按钮」的 grounding 数据，作为 GUI 办公 agent 的感知层预训练。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2610.02320)）
- **评级**：值得浏览（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2610.02320)）

### B. LLM / 视觉模拟型环境（world model 充当环境）

#### B1. Trace2Env: Agentic Language World Models for Interactive Environment Simulation
arXiv 2610.06100 · 2026-10-08 · NTU Singapore · HF 98↑ · [abs](https://arxiv.org/abs/2610.06100) · [repo](https://github.com/ruyue0001/trace2env) · 来源深度 **L3**（README + RUNTIME_HARNESS.md + OFFLINE_VALIDATION.md + REPRODUCING.md）
- **解决的环节**：simulation（traces → 有状态环境替身），适用于「原系统不可得但历史交互 trace 可得」的场景（[abs](https://arxiv.org/abs/2610.06100)）。
- **方法**
  - **离线重建**：把历史 trace 组织成 worldbook，内容包括环境 schema、转移规则、约束、不变量、observation contract、grounded evidence 和 demonstration。worldbook 不恢复可执行系统（[README](https://github.com/ruyue0001/trace2env/blob/main/README.md)）。
  - **运行时**（[RUNTIME_HARNESS.md](https://github.com/ruyue0001/trace2env/blob/main/docs/RUNTIME_HARNESS.md)）：
    - 先在所有可用规则里选出一条。置信的模板规则直接走确定性 fast path。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2610.06100)）
    - 否则由 world-model agent 在 8 次工具调用预算内查 worldbook、读 state、recall、dry_run，然后提交带 typed effects 和引用的 transition。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2610.06100)）
    - harness 按 schema 校验，检查不变量、规则支撑和引用。默认 `rules_only` trust policy 会拒绝没有被引用规则支撑的效果。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2610.06100)）
    - 最后原子提交，并写入 episodic memory。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2610.06100)）
  - **验证/晋升门**（[OFFLINE_VALIDATION.md](https://github.com/ruyue0001/trace2env/blob/main/docs/OFFLINE_VALIDATION.md)）：
    - 新重建的 worldbook 状态为 `candidate`，必须用 replay cases 回放通过才能 promote。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2610.06100)）
    - 验证用例不得与构建数据重叠，测试用例不得用于晋升。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2610.06100)）
    - replay 不调用原环境，也不让 LLM 自己生成期望答案。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2610.06100)）
  - **防跨 episode 泄露**：knowledge gate 给每条知识标 applicability，把外来的具体值 mask 掉（[RUNTIME_HARNESS.md](https://github.com/ruyue0001/trace2env/blob/main/docs/RUNTIME_HARNESS.md)）。
  - **数据量**：ALFWorld 的 worldbook 用 40 条成功轨迹构建；Terminal-Bench 用 20 条构建轨迹 + 16 条 scaling 轨迹；WebArena 用 50 条自采轨迹（[REPRODUCING.md](https://github.com/ruyue0001/trace2env/blob/main/REPRODUCING.md)）。
  - **成本**：worldbook 构建约 27 美元（terminal）、19 美元（web）、154 美元（android，15 个 worldbook）、340 美元（swe，10 个 worldbook）（[REPRODUCING.md](https://github.com/ruyue0001/trace2env/blob/main/REPRODUCING.md)）。
- **验证（sim-to-real）**：
  - 任务 agent 在 Trace2Env 里生成的动作序列拿回真实环境 replay 时，更常保持有效（[abs](https://arxiv.org/abs/2610.06100)）。
  - 一致性比 = W2R / Real，即 world model 内动作在真实环境回放的成功率除以真实环境内直接执行的成功率（[REPRODUCING.md](https://github.com/ruyue0001/trace2env/blob/main/REPRODUCING.md)）。
- **关键结果**：在 9 个环境上，next-observation fidelity 和长程一致性都优于传统 prompt 型 LWM（[abs](https://arxiv.org/abs/2610.06100)）。具体数值在摘要中没有给出（「无出处，待核」）。
- **局限与红旗**：（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2610.06100)）
  - 论文报告的结果早于 2026-10-08 的 state-path 修复。旧代码会丢弃或错误嵌套部分 state tracker mutation：terminal + GPT-5.6-Sol 为 6%，DeepSeek 为 19%，其他环境 GPT 低于 3%、DeepSeek 最高 10%（[REPRODUCING.md](https://github.com/ruyue0001/trace2env/blob/main/REPRODUCING.md)）。
  - 每个系统只跑了一次（[REPRODUCING.md](https://github.com/ruyue0001/trace2env/blob/main/REPRODUCING.md)）。
  - 只适用于文本交互环境（[README](https://github.com/ruyue0001/trace2env/blob/main/README.md)）。
- **迁移到办公/专业场景**：README 明确把内部企业工具、工单流、云/DevOps 控制台、API/MCP 后端列为适用对象（[README](https://github.com/ruyue0001/trace2env/blob/main/README.md)）。
  - 例如：从几十条 SAP/CRM API 调用日志构建 worldbook，得到一个有状态的 mock CRM。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2610.06100)）
  - 「rules_only + 不变量 + replay 晋升门」可直接用作「LLM 模拟 API」的防幻觉护栏，例如余额不能为负、单据状态机不可逆。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2610.06100)）
- **评级**：**必读**（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2610.06100)）

#### B2. Environment-free Synthetic Data Generation for API-Calling Agents（Apple）
arXiv 2607.16900 · 2026-07-21 · Apple · HF 14↑ · [abs](https://arxiv.org/abs/2607.16900) · 无仓库 · 来源深度 **L1**（摘要 + 1 次 WebSearch）
- **解决的环节**：simulation + data prep（API spec → 合成轨迹）（[abs](https://arxiv.org/abs/2607.16900)）
- **方法**：只需要 API specification，三步完成（[abs](https://arxiv.org/abs/2607.16900)）：
  1. LLM 生成可用这些 API 解决的多样任务；
  2. teacher agent 迭代求解，LLM simulator 根据任务上下文和模拟历史生成连贯的 API 响应；
  3. LLM judge 过滤轨迹。
- **补充**：WebSearch 显示 arXiv PDF 现标题为「Simulate to Generalize: Scaling Stateful Supervision for API-calling Agents using LLM World Models」，可能已更新版本（[arXiv PDF（二手，经 WebSearch）](https://arxiv.org/pdf/2607.16900)）；Apple 官方页面见 [machinelearning.apple.com（二手）](https://machinelearning.apple.com/research/environment-free)。
- **验证（sim-to-real）**：在 AppWorld 和 **OfficeBench**（含信息检索与状态改变任务）上微调都有「显著提升」（[abs](https://arxiv.org/abs/2607.16900)）。摘要没有给出数值（「无出处，待核」）。
- **局限与红旗**：模拟器没有显式状态存储，「状态一致性」只靠 simulation history 条件生成；判分完全依赖 LLM judge（[abs](https://arxiv.org/abs/2607.16900)）。没有给出成本。
- **迁移到办公/专业场景**：这是最低门槛的办公方案。拿到 Graph API、Salesforce 或钉钉开放平台的 OpenAPI spec，就能出 SFT 轨迹，并已在 OfficeBench 上有正向信号。建议叠加 Trace2Env 式的显式 state 和不变量校验，弥补一致性短板。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.16900)）
- **评级**：**必读**（办公最直接相关；但证据薄）（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2607.16900)）

#### B3. Masked Diffusion LMs are Strong and Steerable Text-Based World Models for Agentic RL
arXiv 2607.16204 · 2026-07-21 · Patronus AI · HF 5↑ · [abs](https://arxiv.org/abs/2607.16204) · [repo](https://github.com/patronus-ai/mdlm_world_modeling) · 来源深度 **L3**（README + appworld_plugin.py）
- **解决的环节**：simulation（训练专用 world model）+ RL（[abs](https://arxiv.org/abs/2607.16204)）
- **方法**
  - 把 world modeling 形式化为可操控的转移动力学，分解为 initial state、task context、tool schemas、domain rules、steering directives（[abs](https://arxiv.org/abs/2607.16204)）。
  - 在 239,403 条 grounded 轨迹上（9 个开源环境、12 个 frontier 模型家族）微调 MDLM（SDAR、WeDLM）作为 world model（[README](https://github.com/patronus-ai/mdlm_world_modeling/blob/main/README.md)）。
  - 训练时只用 WM，真实环境只用于评测；可选的确定性 local responder 处理约 85% 的动作，以减少 WM 调用（[README](https://github.com/patronus-ai/mdlm_world_modeling/blob/main/README.md)）。
- **验证（sim-to-real）**：在 ScienceWorld、ALFWorld、AppWorld 三个 OOD 环境上，对 1.2B–7B 的 agent 做零样本迁移消融（[abs](https://arxiv.org/abs/2607.16204)）。README 称最多带来 47% 的绝对任务成功率提升（[README](https://github.com/patronus-ai/mdlm_world_modeling/blob/main/README.md)）。SDAR-8B 的 in-domain MAUVE 为 0.982，高于 Qwen3.5-35B-A3B 的 0.932（[README](https://github.com/patronus-ai/mdlm_world_modeling/blob/main/README.md)）。
- **局限与红旗**
  - 摘要说有 "deterministic state checks"，但 AppWorld 的实际 reward 是**手写启发式**：按关键词判断语义对齐（如 reject→禁 accept），检测占位符参数（如 "roommate1"、"your_password"），惩罚跳过 `show_account_passwords`，并给部分分 0.15/0.08/0.03。这是强烈的环境特化 shaping，并非通用状态检查（[appworld_plugin.py](https://github.com/patronus-ai/mdlm_world_modeling/blob/main/appworld/appworld_plugin.py)）。
  - 「约 85% 的动作由确定性 responder 处理」意味着 WM 的贡献需要单独消融（[README](https://github.com/patronus-ai/mdlm_world_modeling/blob/main/README.md)）。
  - HF 仅 5↑。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.16204)）
- **迁移到办公/专业场景**：有价值的是 steering 分解（tool schema + domain rules + 期望结果作为全局锚点），可以用来按需生成「刁钻」的 API 返回（如分页、权限拒绝、部分失败）以增加训练多样性。不要照搬它的 reward。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.16204)）
- **评级**：值得浏览（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2607.16204)）

#### B4. EnvACE: Internalizing Environment Dynamics via World Rehearsal
arXiv 2608.06197 · 2026-08-07 · Tencent · HF 44↑ · [abs](https://arxiv.org/abs/2608.06197) · [repo](https://github.com/Within-yao/EnvACE) · 来源深度 **L3**（README + run_checklist_share.sh + checklist_reward.py）
- **解决的环节**：simulation（策略自扮环境）+ RL reward（[abs](https://arxiv.org/abs/2608.06197)）
- **方法**
  - 同一个 policy 交替扮演两个角色：Act 生成工具调用，Rehearse 扮演环境生成该调用应得的响应；后续决策以自己 rehearse 出的响应为条件（[abs](https://arxiv.org/abs/2608.06197)）。
  - 用 role-wise GRPO 训练：每个角色有独立 baseline，参数共享（[README](https://github.com/Within-yao/EnvACE/blob/main/README.md)）。
  - Reward 来自逐轮 **checklist**：每条含 question / focus_on / pass_condition / failure_examples / reference snippet，由 Qwen3-30B-A3B judge 以严格 JSON schema 判定（[checklist_reward.py](https://github.com/Within-yao/EnvACE/blob/main/agent_system/environments/env_package/checklist/checklist_reward.py)，[run_checklist_share.sh](https://github.com/Within-yao/EnvACE/blob/main/examples/drmas_trainer/run_checklist_share.sh)）。
  - judge API 失败时 mask 掉整条轨迹，而不是记 0 分，以免污染 GRPO advantage（[checklist_reward.py](https://github.com/Within-yao/EnvACE/blob/main/agent_system/environments/env_package/checklist/checklist_reward.py)）。
  - 测试时可以先做 N 次私下 rehearsal，总结成 rehearsal memory，再真实执行一次（[README](https://github.com/Within-yao/EnvACE/blob/main/README.md)）。
- **验证**：在 BFCL-v4、τ²-Bench、VitaBench、FinMCP-Bench 上，整体优于 environment-scaling 基线（[abs](https://arxiv.org/abs/2608.06197)）。
- **关键结果**：EnvACE-8B 在 BFCL-v4/τ²/VitaBench 上 Overall 32.91，FinMCP-Bench TF1 46.78；在同等开源规模下优于 Simulator-8B、TOUCAN-7B、EnvScaler-8B、AWM-8B/14B、ScaleEnv-8B（[README](https://github.com/Within-yao/EnvACE/blob/main/README.md)）。
- **局限与红旗**：policy 自己扮演环境，存在「自洽但错误」的风险，例如环境角色学会给出对 actor 有利的响应。reward 来自 checklist judge 而不是真实状态，因此两个角色可能共谋（推断，「无出处，待核」）。
- **迁移到办公/专业场景**：对金融 MCP 工具（FinMCP-Bench 已覆盖，见[abs](https://arxiv.org/abs/2608.06197)）这类无法开放写操作的系统，可以先用 rehearsal 预训练。checklist 格式（pass_condition + failure_examples + 证据片段）是办公 rubric reward 的好模板；「judge 宕机就 mask」这个工程细节值得照抄。
- **评级**：值得浏览（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2608.06197)）

#### B5. AutoGUIWorld: Image Generators as Visual World Models for GUI Agent
arXiv 2610.01215 · 2026-10-02 · Tencent Hunyuan · HF 42↑ · [abs](https://arxiv.org/abs/2610.01215) · [repo](https://github.com/ImYangC7/AutoGUIWorld) · 来源深度 **L2**
- **解决的环节**：visual simulation + trajectory synthesis（[abs](https://arxiv.org/abs/2610.01215)）
- **方法**（[README](https://github.com/ImYangC7/AutoGUIWorld/blob/main/README.md)）
  1. GUI world sampler 从三类因子采样结构化场景：OS 底座、视觉外观、初始 GUI 状态（窗口/标签数、布局、可见内容、障碍物），并渲染出初始截图。
  2. 根据场景生成任务，并对近似重复去重。
  3. Meta Planner 把任务拆成原子动作；Voyager 读取最新截图并描述预期的视觉变化，图像编辑后端据此渲染下一帧。
  4. Grounding 给出点击框；QC 审查 seed 质量、任务相关性、grounding 和转移保真度。
- **验证（sim-to-real）**：微调 Qwen3.5-35B-A3B 后，OSWorld 平均任务分从 33.0% 升到 40.8%，ScienceBoard 成功率从 14.0% 升到 32.2%（[abs](https://arxiv.org/abs/2610.01215)）。
- **关键结果**：Ubuntu/Windows/macOS/Chrome 四个平台共 79,266 条带空间标注的步级样本（[abs](https://arxiv.org/abs/2610.01215)）。
- **局限与红旗**：README 自承只在视觉状态空间生成轨迹，不在真实桌面执行，也不独立验证任务是否完成（[README](https://github.com/ImYangC7/AutoGUIWorld/blob/main/README.md)）。图像编辑出的表格数字、公式结果没有语义保证（推断）。
- **迁移到办公/专业场景**：适合给难以部署的专业软件（如 SAP GUI、行业 ERP、医疗 HIS）低成本补充「界面熟悉度」和 grounding 数据。不能用来学数据正确性，例如公式计算或对账结果。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2610.01215)）
- **评级**：值得浏览（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2610.01215)）

### C. 用户模拟器

#### C1. MIMESIS: Learning User Simulators as Training Environments for Interactive Agents
arXiv 2610.09484 · 2026-10-08 · AI at Meta · HF 19↑ · [abs](https://arxiv.org/abs/2610.09484) · [repo](https://github.com/VietHoang1512/mimesis) · 来源深度 **L2**（README + simulator/README）
- **解决的环节**：user sim（作为 RL 环境）+ 稠密监督（CSD）（[abs](https://arxiv.org/abs/2610.09484)）
- **方法**
  - 出发点：现成的 assistant LLM 当用户会过度合作、过度明确、行为同质，所以用人类对话加显式推理监督，并引入 13 种真实行为模式，专门训练用户模拟器（[abs](https://arxiv.org/abs/2610.09484)）。
  - 三阶段训练（[simulator/README](https://github.com/VietHoang1512/mimesis/blob/main/simulator/README.md)）：
    1. 62 个语料混合的 mid-training，做角色互换，loss 只算在人类一侧的回合；
    2. 在 ThoughtTrace 推理轨迹上做 SFT；
    3. 在 24 个任务混合上做 RL。
  - 冻结模拟器后，用多轮 GRPO 训练 agent。CSD 让 coach 根据模拟器的私有想法写 coaching note，转成 token 级监督；部署时的 agent 只看公开对话（[README](https://github.com/VietHoang1512/mimesis/blob/main/README.md)）。
- **验证（sim-to-real 的代理）**：在 8 个环境（其中 3 个 held-out）、9 个未见的评测用户模型下，GRPO 配 GPT-5.5 用户平均 26.10，配 MIMESIS-9B 平均 29.54，CSD + MIMESIS-9B 平均 31.09（[README](https://github.com/VietHoang1512/mimesis/blob/main/README.md)）。
- **关键结果**：MIMESIS-9B 的 SOUL-Index 为 65.7（GPT-5.5 为 64.1）；RealUserSim PT3 行为保真度 94.0（Claude-Opus-5 为 80.6）；SimulatorArena Turing distance 38.7（越低越好，Claude-Opus-5 为 42.3）；τ-USI 80.17（[README](https://github.com/VietHoang1512/mimesis/blob/main/README.md)）。
- **局限与红旗**：「泛化到新用户」是用其他 LLM 模拟器衡量的，不是真人用户（[README](https://github.com/VietHoang1512/mimesis/blob/main/README.md)）。agent 绝对分数仍低（约 30 分）。
- **迁移到办公/专业场景**：办公 agent 的难点常在需求含糊、信息逐步披露、中途改主意。可以用 MIMESIS 式训练出「不合作」的用户模拟器来替代 τ-bench 里的 GPT 用户。CSD 的思路，即把模拟器的私有意图当训练期特权信息，适合「客户隐含约束」类场景（如报价、合同条款协商）。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2610.09484)）
- **配套参考**：池内的 UserProxyBench 发现：固定 agent、只换 user proxy，375 个企业任务上平均 reward 变化 15.2 分；24.4% 的成功 episode 中有用户违反设定，主要是过早披露信息（[UserProxyBench abs](https://arxiv.org/abs/2609.38043)）。这说明用户模拟器本身必须单独评测。
- **评级**：**必读**（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2610.09484)）

### D. 任务合成、Verifier、Infra 与数据准备

#### D1. Thinkingbox: A Sandbox and Benchmark for Agents in Stateful Business Workflows
arXiv 2608.19741 · 2026-08-25 · Microsoft · HF 9↑ · [abs](https://arxiv.org/abs/2608.19741) · [repo](https://github.com/microsoft/thinkingbox) · 来源深度 **L2**（README + tests）
- **解决的环节**：infra（MCP 隔离会话）+ verifier（终态 + 副作用检查）+ user sim（[abs](https://arxiv.org/abs/2608.19741)）
- **方法**
  - MCP Session Proxy 每次对话按 scenario 拉起一组隔离的 MCP server 进程（[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)）：
    - 每个 server 都实现 `__reserved__init`（装载初始状态）和 `__reserved__geteffects`（导出副作用，供判分用）；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.19741)）
    - 对话结束后通过 `/get_effects` 取回状态，再执行测试断言。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.19741)）
  - 数据集由三类对象组成（[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)）：
    - Agent（prompt 配置）；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.19741)）
    - Scenario（各 server 的初始状态与可用工具）；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.19741)）
    - Test Case（用户 query + 用户 LLM 上下文 + 测试代码）。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.19741)）
  - 用户由 LLM 模拟，基于 prompt 加上下文作答（[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)）。
  - 任务专属的可执行检查接受合法轨迹，同时拒绝**错误、缺失或多余**的效果；部分任务还会检查最终回复（[abs](https://arxiv.org/abs/2608.19741)）。
  - RL 训练放在另一个仓库 thinkingbox-training，支持 GRPO 和多轮 MCP rollout（[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)）。
- **验证**：这是 benchmark，不涉及 sim-to-real。它的发现是：许多失败轨迹终止干净、写操作也合法，说明响应或调用层面的信号不能代替端到端完成度（[abs](https://arxiv.org/abs/2608.19741)）。
- **关键结果**：507 个受 policy 约束的工作流，覆盖零售、酒店、车险、neobank 内部 IT、咨询公司 IT/HR；最强模型 pass@1 为 65.36%，pass^20 只有 25.25%（[abs](https://arxiv.org/abs/2608.19741)）。
- **局限与红旗**：真实场景数据和工具 server 放在单独的 thinkingbox-data 仓库，本仓库只带一个 cloud_drive 冒烟示例（[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)）；HF 热度低。
- **迁移到办公/专业场景**：这是办公/企业流程 verifier 的**参考实现**：（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.19741)）
  - 每个 mock 系统统一实现 init/geteffects 两个保留接口；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.19741)）
  - 判分用「必需效果 ⊆ 实际效果 ⊆ 允许效果」的集合检查；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.19741)）
  - 报 pass^k 衡量可靠性。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.19741)）
  - 与 Echoverse 的「多余改动 OK」形成对照，见 A1。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.19741)）
- **评级**：**必读**（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2608.19741)）

#### D2. OSReward: Standardized Evaluation for Cross-Platform Computer-Use Reward Models
arXiv 2607.28609 · 2026-08-07 · HKU NLP（作者含 Tianbao Xie）· HF 72↑ · [abs](https://arxiv.org/abs/2607.28609) · [repo](https://github.com/OS-Copilot/OSReward) · 来源深度 **L3**（README + eval_pipeline/prompts/binary_v1.txt）
- **解决的环节**：verifier / reward model（VLM judge 可靠性）（[abs](https://arxiv.org/abs/2607.28609)）
- **方法**
  - 多个 agent backbone 在多平台执行人工验证过的指令，轨迹再经多阶段人工标注得到 ground-truth 判定（[abs](https://arxiv.org/abs/2607.28609)）。
  - 派生两个子集：OSReward-Hard 集中难例，OSReward-Multi 评效率与对齐（[abs](https://arxiv.org/abs/2607.28609)）。
  - 采集管线覆盖 Web、Windows 11 VM（基于 WAA）和 Android 模拟器（基于 AndroidWorld），统一流程为 import → collect → judge → filter → export（[trajectory_collection/README](https://github.com/OS-Copilot/OSReward/blob/main/trajectory_collection/README.md)）。
  - 基准 judge prompt 的共识规则（[binary_v1.txt](https://github.com/OS-Copilot/OSReward/blob/main/eval_pipeline/prompts/binary_v1.txt)）：
    1. 明确要求答案的任务，必须显式输出答案；
    2. **grounding rule**：答案事实必须来自与环境的交互，即便答对、但靠先验知识也判 FAIL；
    3. 被登录墙、CAPTCHA 等阻断的一律 FAIL；
    4. 长轨迹中间出错不等于失败。
- **验证**：在 OSWorld、WindowsAgentArena、WebArena、AndroidWorld 上，衡量 VLM judge 与各 benchmark 自带 verifier 的一致性（[README](https://github.com/OS-Copilot/OSReward/blob/main/README.md)）。
- **关键结果**：（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.28609)）
  - 1,019 条 Full 轨迹、284 条 Hard 轨迹（[README](https://github.com/OS-Copilot/OSReward/blob/main/README.md)）。
  - SOTA judge 普遍有**宽松偏差**，会把失败判成成功；足够可靠的 judge 太贵，便宜的开源模型差距很大（[abs](https://arxiv.org/abs/2607.28609)）。
  - 发布 OS-Shepherd-100K 判决语料；README 称 OS-Shepherd 9B/35B 以低 30–60 倍的成本达到商业 judge 水平（[README](https://github.com/OS-Copilot/OSReward/blob/main/README.md)）。
- **局限与红旗**：标注为 "Work in progress"（[abs](https://arxiv.org/abs/2607.28609)）；语料构建管线与 OS-Shepherd 训练代码尚未开源（[README](https://github.com/OS-Copilot/OSReward/blob/main/README.md)）。
- **迁移到办公/专业场景**：（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.28609)）
  - 办公 GUI 任务多数难写程序化 checker，必然会用 VLM judge，所以先在自家任务上建一个小型人工金标集，测 judge 的宽松偏差；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.28609)）
  - grounding rule（答案必须来自环境交互）可以直接加进报表/查数类任务的 judge prompt。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.28609)）
- **评级**：**必读**（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2607.28609)）

#### D3. Recursive Synthesis for Long-Horizon Terminal Tasks (RST)
arXiv 2608.05466 · 2026-08-06 · Tencent Hunyuan · HF 242↑ · [abs](https://arxiv.org/abs/2608.05466) · 无仓库 · 来源深度 **L1**
- **解决的环节**：task synthesis（chaining + 难度递增）（[abs](https://arxiv.org/abs/2608.05466)）
- **方法**：从已验证的种子任务出发，循环执行以下步骤（[abs](https://arxiv.org/abs/2608.05466)）：
  1. 扩展 reference solution；
  2. 让 verifier 和 instruction 重新对齐新工作流；
  3. 在全新 sandbox 中验证；
  4. 把通过的任务作为下一轮种子。
- **关键结果**（[abs](https://arxiv.org/abs/2608.05466)）：
  - 15 轮递归共产出 37,484 个任务，每个约 0.05 美元；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.05466)）
  - 难度随轮次上升：reference solution 中位数从 67 行增到 374 行，执行命令中位数从 40 增到 244；DeepSeek-V4-Pro 的 pass@4 从第 1 轮的 90% 降到第 15 轮的 2.5%；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.05466)）
  - 用 rejection-sampled 轨迹做 SFT，Qwen3.5-27B/122B 提升最多 10 分；agentic PPO 把 Qwen3.5-27B 在 Terminal-Bench 2 / TB Hard / Long-Horizon TB 上提到 49.44% / 32.00% / 22.07%。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.05466)）
- **背景对比**：人工长程任务的成本是每个数百到数千美元（[abs](https://arxiv.org/abs/2608.05466)）。
- **局限与红旗**：「难」可能来自冗长的累积，而不是真正的推理难度；verifier 的再对齐质量没有独立审计（推断，「无出处，待核」）。
- **迁移到办公/专业场景**：「递归扩展 + 每轮新 sandbox 验证」适合把单步表格任务（如清洗一列）逐轮扩展为月结流程（清洗→透视→对账→出报告），并用前沿模型的 pass@k 衰减当作难度刻度。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.05466)）
- **评级**：**必读**（目前最清晰的难度校准与链式扩展方案，成本数据明确）（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2608.05466)）

#### D4. DeepSearch-World: Self-Distillation for Deep Search Agents in a Verifiable Environment
arXiv 2607.07820 · 2026-07-21 · HKUST · HF 72↑ · [abs](https://arxiv.org/abs/2607.07820) · [repo](https://github.com/ornamentt/DeepSearch-World) · 来源深度 **L2**
- **解决的环节**：infra（确定性离线工具环境）+ task synthesis + data prep（RS / 过滤 / 混合）（[abs](https://arxiv.org/abs/2607.07820)）
- **方法**
  - **确定性环境**：`web_search_wiki` 基于 Pyserini/Lucene BM25 索引，`visit_wiki` 通过 SQLite 偏移库 + JSONL 语料返回可复现的观测（[README](https://github.com/ornamentt/DeepSearch-World/blob/main/README.md)）。
  - **任务合成**：从种子 Wikipedia 页面做 BFS，建知识树 → 选择相关链接 → 生成多跳问题（[README](https://github.com/ornamentt/DeepSearch-World/blob/main/README.md)），即摘要所说的 entity-level random walk（[abs](https://arxiv.org/abs/2607.07820)）。
  - **数据准备**（[README](https://github.com/ornamentt/DeepSearch-World/blob/main/README.md)）：
    - LLM judge 做 rejection sampling，可选再做工具使用质量过滤；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.07820)）
    - Scaffold-to-ReAct 转换时删除只读的 state 字段，避免训练时信息泄露；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.07820)）
    - 多轮正确数据按衰减重要性采样混合；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.07820)）
    - 生成节点与训练节点异步迭代。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.07820)）
- **关键结果**：420K 多跳 QA；不从更强模型蒸馏，9B 模型达到 BrowseComp 31.2%、GAIA 61.5%、HotpotQA 93.4%（[abs](https://arxiv.org/abs/2607.07820)）。
- **局限与红旗**：BrowseComp 和 GAIA 需要真实网页，而训练环境是离线 Wikipedia，迁移机制未详述（[abs](https://arxiv.org/abs/2607.07820)）。
- **迁移到办公/专业场景**：「冻结快照 + 确定性检索工具」适用于企业知识库或文档库问答 agent：用 BM25 索引加内部 wiki 快照做可复现环境，在内部实体图上 random walk 生成多跳问题。去掉特权 state 字段这一招适用于任何带 scaffold 的蒸馏。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.07820)）
- **评级**：值得浏览（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2607.07820)）

#### D5. Qwen-UI-Agent Technical Report
arXiv 2607.28227 · 2026-07-31 · TongyiLab · HF 284↑ · [abs](https://arxiv.org/abs/2607.28227) · 无仓库 · 来源深度 **L1**
- **解决的环节**：infra（真机 + 沙箱）+ 数据飞轮（[abs](https://arxiv.org/abs/2607.28227)）
- **方法**（[abs](https://arxiv.org/abs/2607.28227)）：
  - 多样的沙箱环境 + 大规模真机移动 runtime；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.28227)）
  - 统一动作空间，GUI 与 CLI 交错；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.28227)）
  - AutoResearch 式数据飞轮：由 agent 构造任务和环境、诊断失败、规划下一轮迭代；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.28227)）
  - 在线 RL 支持超过 100 轮的轨迹，并发环境超过 10,000 个。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.28227)）
- **关键结果**：MobileWorld 82.1%，移动端 SOTA；computer-use 和 browser-use 与 frontier 模型有竞争力（[abs](https://arxiv.org/abs/2607.28227)）。
- **局限与红旗**：技术报告，没有公开环境或任务构造细节（[abs](https://arxiv.org/abs/2607.28227)）。
- **迁移到办公/专业场景**：可借鉴的只是规模指标（万级并发）和「agent 驱动飞轮」这个概念。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2607.28227)）
- **评级**：可跳过（就方法而言）（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2607.28227)）

#### D6. T1: Terminal Agent RL for Long-Horizon Tasks
arXiv 2609.11042 · 2026-09-10 · Tencent Hunyuan · HF 29↑ · [abs](https://arxiv.org/abs/2609.11042) · 无仓库 · 来源深度 **L1**
- **解决的环节**：infra（云沙箱真实 shell）+ reward 设计 + 防 benchmark 泄露（[abs](https://arxiv.org/abs/2609.11042)）
- **方法**（[abs](https://arxiv.org/abs/2609.11042)）：
  - 122B MoE 在云沙箱里操作真实 shell，最多 300+ 次工具调用；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2609.11042)）
  - 奖励来自执行每个任务自带的 verifier；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2609.11042)）
  - dense process reward 按通过 verifier 的绝对数量计分；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2609.11042)）
  - 训练语料是隔离的种子 + 与 Terminal-Bench 2.1 不相交的合成任务，以避免过拟合 benchmark；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2609.11042)）
  - TITO 与 rollout routing replay 解决训推不一致。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2609.11042)）
- **关键结果**：TITO + R3 把训推 log-prob 差从 0.021 降到 0.013；Terminal-Bench 2.1 从 43.8% 升到 64.0%；Long-Horizon Terminal Bench 27.9%（[abs](https://arxiv.org/abs/2609.11042)）。
- **局限与红旗**：环境构造本身不是贡献点（[abs](https://arxiv.org/abs/2609.11042)）。
- **迁移到办公/专业场景**：「按通过子检查数计 dense reward」适合办公多检查点任务，例如一个报表任务含 10 个单元格级断言。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2609.11042)）
- **评级**：可跳过（对环境方法而言）（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2609.11042)）

#### D7. Agentic Game Development as a Verifiable Trajectory Data Engine for Scaling World Models
arXiv 2608.25518 · 2026-08-28 · NUS · HF 128↑ · [abs](https://arxiv.org/abs/2608.25518) · 无仓库 · 来源深度 **L1**
- **解决的环节**：verifier / reward（引擎检查 + 人类接受信号）（[abs](https://arxiv.org/abs/2608.25518)）
- **方法**（[abs](https://arxiv.org/abs/2608.25518)）：
  - 游戏引擎里的场景是一份可执行的世界规格，引擎可以检查碰撞、物理、可导航性和有界可玩性；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.25518)）
  - 开发者是否接受某个场景，作为全局验证信号；（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.25518)）
  - 两者结合成 RLHEV 后训练范式。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.25518)）
- **关键结果**：摘要里没有量化结果，属于立场/框架文（[abs](https://arxiv.org/abs/2608.25518)）。
- **局限与红旗**：没有实验数字，与办公场景距离远。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.25518)）
- **迁移到办公/专业场景**：「把用户在真实工作流中的接受/修改行为当作隐式 reward」可以类比为：办公文档被用户采纳或改写、财务凭证被审核通过或驳回。（笔记作者分析/建议，依据 [abs](https://arxiv.org/abs/2608.25518)）
- **评级**：可跳过（评级为笔记作者判断，依据本卡所引 [abs](https://arxiv.org/abs/2608.25518)）

### E. 池内补充：值得跟踪的办公数据合成（未深读，仅摘要）
- **Synthesis Through Simulation（SAP）**：LLM agent 通过调用强制执行 policy 的 API 在模拟企业环境中「操作出」数据，构造上保证结构合法；无需 DB schema 即达到 0.88 平均边际保真度和 100% 约束满足（[abs](https://arxiv.org/abs/2610.10549)）。
- **Generating a Consistent Enterprise**：从一张实体图投影到 66 个业务产品的原生格式（CRM、工单、通话等），用 28 项统计检查加对抗检测器做 reference-free 真实性评估；23 家公司的平均真实性从 60.3 升到 99.1（[abs](https://arxiv.org/abs/2609.11286)）。
- **Era by Eon Benchmark**：用 seeded 实体图驱动 Salesforce、Zendesk、Slack、Gong 等产品模拟器，答案由最终记录计算，判分精确（[abs](https://arxiv.org/abs/2609.09853)）。
- **PersonaForge**：分析 16K 真实会话发现 75.9% 是多轮；四维 persona + SOUL 行为控制按真实用户统计校准（[abs](https://arxiv.org/abs/2608.28378)）。

