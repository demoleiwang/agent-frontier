# 专业领域 Agent 环境构建 —— 论文精读笔记（2026-07-01 → 2026-10-13）

> 证据规则：每条论断后附来源链接。arXiv abs 链接 = 来自摘要（数据集 excerpt 字段即 arXiv 摘要）；GitHub blob 链接 = 来自仓库 README/文档/代码（只读，未执行任何仓库代码）；(二手) = 仅来自 WebSearch 结果页。无法溯源者标「无出处，待核」。arxiv.org / *.github.io / huggingface.co 在本环境不可达，故未读 PDF 全文的论文以「摘要 + 仓库」为证据深度。

## 0. 速览

**统计**：输入 70 篇全部按摘要筛选：13 篇判"是·深读"，21 篇"部分"相关，36 篇"否"（见 §1）；另从全量池补捞 19 篇（§1b），其中 4 篇深读；加上输入中"部分"相关的 TerminalHorizon 一张简要卡片，共 18 张环境构建卡片（§2）。

### 必读 Top-6

1. **EngiWorld**：26 款真实工程软件（含 SolidWorks/Abaqus/Revit/Altium）、1,301 题，verifier 用几何内核做容差断言并检测 GUI 旁路（[arXiv](https://arxiv.org/abs/2609.37686) · [eval.py](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/eval.py)）→ §2.2
2. **OSWorld-Science**：17 款真实科学软件放在 VM 中；为商业许可证（Mnova/SAS/Ansys）各配了一套处理办法；"gate + 加权 partial credit"评分；grader 先写 negative tests（[arXiv](https://arxiv.org/abs/2609.39903) · [adding-a-task.md](https://github.com/DiscoAILab/OSWorld-Science/blob/main/docs/user_guide/adding-a-task.md)）→ §2.1
3. **Argo-Bench**：先用模拟器生成隐藏真值的企业世界，再导出成 Oracle EBS 形态的 ERP 仓库；按 agent 动作在模拟器里的后果评分；仓库公开了开发期"agent 读 grader"的 reward-hacking 记录（[arXiv](https://arxiv.org/abs/2610.02122) · [reward_hacking](https://github.com/TextQLLabs/Argo-Bench/blob/main/analysis/reward_hacking/README.md)）→ §2.6
4. **ScienceIDE**：钉死版本的真实科学代码 + 自带物理用例当 verifier，reward 按 floor 归一化；已用于 SFT/RL 并发布模型（[arXiv](https://arxiv.org/abs/2609.19134) · [README](https://github.com/aitofound/ScienceIDE/blob/main/README.md)）→ §2.9
5. **DAYJOB**：医疗和金融从业者自己出题，每题估计需 13–17 小时人工；每题配几十条专家 binary rubric，由 agentic judge 判定，全部满足才算通过（[arXiv](https://arxiv.org/abs/2610.01306) · [README](https://github.com/surge-ai/dayjob/blob/main/README.md)）→ §2.3
6. **SimuVerity**：在商业 MATLAB/Simulink 里做工程建模，验收靠评估方持有的多工况原生仿真场景；先过 gate，再按六维打分（[arXiv](https://arxiv.org/abs/2610.02304) · [benchmark README](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/README.md)）→ §2.14

（同为"必读"但未进 Top-6：**CADWorld** §2.15 与 EngiWorld §2.2 在 CAD 上重叠，但它是唯一公开人工成本的 CAD 基准，约 1,300 人时 / 200 题，[CADWORLD.pdf](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)。）

### 对比表（18 篇深读）

| 论文 | 领域 | 环境形态 | 任务来源 | 验证 | 开放 | 出处 |
|---|---|---|---|---|---|---|
| OSWorld-Science | 7 个科学领域 | 真实科学软件 + VM（含商业软件许可证处理） | 专家提案 + human–AI 共设计 | 可执行 evaluator，gate + 加权 partial credit，数值容差 | 代码 CC BY；数据/VM 在 HF；答案键公开 | [arXiv](https://arxiv.org/abs/2609.39903) · [repo](https://github.com/DiscoAILab/OSWorld-Science/blob/main/README.md) |
| EngiWorld | CAD/CAE/CAM/BIM/EDA/DCC | 26 款真实工程软件，Win/Ubuntu VM | "expert-curated"；source 多为官方文档 URL | 几何/物理/规则 verifier；优化题连续分；GUI 旁路检测 | MIT，1,301 题全开 | [arXiv](https://arxiv.org/abs/2609.37686) · [repo](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md) |
| CADWorld | 机械 CAD（FreeCAD） | 真实开源软件 + VM | 人工编写，约 1,300 人时 | 对 .FCStd 的可执行检查，binary all-pass | 全开 + VM 镜像 | [arXiv](https://arxiv.org/abs/2609.16251) · [repo](https://github.com/Zdong104/CADWORLD/blob/main/README.md) |
| SimuVerity | 10 个工程领域（Simulink） | 商业 MATLAB/Simulink + MCP | 规格 + 参考系统（10 个专家自建、58 个第三方、33 个导入官方示例） | gate + 6 维，多工况原生仿真 | Apache-2.0；需 MATLAB | [arXiv](https://arxiv.org/abs/2610.02304) · [repo](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/README.md) |
| NeutronGym | 中子仪器设计 | McStas 模拟器 | 程序化 family + 16 个已发表仪器 | 分层 ladder，无 LLM judge，partial credit | 未找到代码 | [arXiv](https://arxiv.org/abs/2610.03631) |
| ScienceIDE | 计算物理/地球科学等 | 钉死版本的真实科学代码库，Harbor 容器 | 专家定义 case + 程序化缺陷注入 | 重编译后跑物理用例，floor 归一化 | 15/64 个环境、30/85 题公开 | [arXiv](https://arxiv.org/abs/2609.19134) · [repo](https://github.com/aitofound/ScienceIDE/blob/main/README.md) |
| SWE-bench Science | 20 个科学领域软件工程 | 真实仓库，环境/verifier 双镜像 | 真实 issue + 专家探索 + 工程集成 | held-out tests，pass@1 | MIT；有 license gate | [arXiv](https://arxiv.org/abs/2608.19799) · [repo](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/README.md) |
| AgenticDataBench | 15 个领域的数据科学 | 真实数据集 + 代码执行 | 真实 B2B 用例 + SO skill-graph 合成 + 专家标注 | 逐列容差比对 CSV 等，partial | dev 246 题公开，98 题私有 | [arXiv](https://arxiv.org/abs/2607.01647) · [repo](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/README.md) |
| DataSpace | 异构 workspace 分析 | 本地文件 workspace（6 种模态） | Builder 渲染 + 11 名专家修复 | 确定性表格比对，binary | 410 题输入公开，只有 60 题给 gold | [arXiv](https://arxiv.org/abs/2608.03451) · [repo](https://github.com/HKUSTDial/DataSpace/blob/main/README.md) |
| Argo-Bench | 企业运营/财务/反欺诈 | 模拟器 → ERP 仓库（235 表，75 亿行） | 人工设计 + 可执行参考解 | 在模拟器里结算动作后果 | 代码 Apache / 数据 CC BY；答案键保留 | [arXiv](https://arxiv.org/abs/2610.02122) · [repo](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md) |
| BI-Bench | 商业智能 | 真实公开 BI 项目数据 + Python/SQL | 从真实 dashboard 人工抽取 | 真值 CSV 宽松匹配 | 100 cases + gt 公开 | [arXiv](https://arxiv.org/abs/2609.20886) · [repo](https://github.com/Hu-Chuxuan/bi-agent/blob/release/README.md) |
| Thinkingbox | 零售/酒店/车险/银行/咨询 IT-HR | MCP mock 后端 + 模拟用户 | 测试作者编写 | 终态 hash 比对 + 30 题 rubric，binary | 开源；声明仅限评测 | [arXiv](https://arxiv.org/abs/2608.19741) · [release](https://github.com/microsoft/thinkingbox-data/blob/main/releases/thinkingbox_bench_v1/README.md) |
| GDPevo | CRM/ERP/金融/医疗/法律/数据 | Docker 化 mock 企业服务 | 以 GDPval/SOP-Bench 为种子，agent 全自动合成 | 规则 grader，每个得分点全有或全无 | 全开 | [arXiv](https://arxiv.org/abs/2608.03764) · [repo](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md) |
| Business Arena | 跨境 B2B 经营 | 以真实 Alibaba.com 数据为底的模拟器 | 单一长程任务 + 人类策略参照 | 净资产 + 技能指标 + 机制消融 | 未开源 | [arXiv](https://arxiv.org/abs/2608.08621) · [paper](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf) |
| DAYJOB | 医疗 + 金融 | Harbor 容器文件工作区 | 专业人员编写 | 专家 binary rubric + agentic judge | 发布 100/130 题 | [arXiv](https://arxiv.org/abs/2610.01306) · [repo](https://github.com/surge-ai/dayjob/blob/main/README.md) |
| FrontierFinance | 投研 | 通用 harness，仅用公开数据 | 220 个专家查询 | 11,543 条带来源的 rubric | 称数据与评分代码公开 | [arXiv](https://arxiv.org/abs/2608.11683) |
| CASE | 纵向临床（MRI + EHR） | 真实 UK Biobank 数据 + 医学工具；RL 时回放 mock 工具 | 由 ICD-10 诊断派生 | 多选题 exact match；RL 用 rubric dense reward | 代码与权重公开；数据需 UKB 授权 | [arXiv](https://arxiv.org/abs/2609.39566) · [repo](https://github.com/VinyehShaw/CASE/blob/main/README.md) |
| TerminalHorizon | 25 个专业领域的终端任务 | 合成终端环境 | 从真实专业工作出发合成，用独立执行审计 | 未见 | 引擎未开源 | [arXiv](https://arxiv.org/abs/2610.13166) |

### 跨论文要点：专业领域环境与专家数据现在怎么建

1. **真实专业软件已经能装进 VM，卡脖子的是许可证。** 一共三种做法：
   - 用户自带 licence，通过 pre-task hook 注入；SAS 走网页版；Ansys 只给重建 recipe（[OSWorld-Science](https://github.com/DiscoAILab/OSWorld-Science/blob/main/configs/snapshots.yaml)）。
   - 只公开部分镜像，商业软件镜像由用户自备（[EngiWorld](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)）。
   - 要求用户自有 MATLAB，并在评测时删掉官方示例目录防止照抄（[SimuVerity](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/README.md)）。

   与此相对，[CADWorld](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf) 和 [ScienceIDE](https://github.com/aitofound/ScienceIDE/blob/main/README.md) 只用开源软件，换来完全可复现和可再分发。[SWE-bench Science](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/docs/paper_material_audit_046_060.md) 走得更远：对每道题附带的论文和图表逐一做版权审计。

2. **最可信的 verifier 是"让领域引擎重新算一遍"，而不是 LLM judge。** 例子：
   - 用几何内核读 STEP 做容差断言；用 FEniCS 重算 compliance（[EngiWorld](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/design-optimization/cli/fenics/task-01/eval.py)）。
   - 重编译后跑物理用例（[ScienceIDE](https://github.com/aitofound/ScienceIDE/blob/main/README.md)）。
   - 多工况原生 Simulink 仿真（[SimuVerity](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/README.md)）。
   - McStas ray-trace（[NeutronGym](https://arxiv.org/abs/2610.03631)）。
   - 在模拟器里结算业务后果（[Argo-Bench](https://arxiv.org/abs/2610.02122)）。

   要不要给 partial credit 分成两派：
   - 用于训练时，partial credit 很关键。NeutronGym 去掉 ladder 的 partial credit 后增益塌缩 60 个点（[arXiv](https://arxiv.org/abs/2610.03631)）；ScienceIDE 用 floor 归一化，保证不动仓库恰好得 0 分（[README](https://github.com/aitofound/ScienceIDE/blob/main/README.md)）。
   - 用于评测时，多数基准选 binary all-pass，例如 [CADWorld](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)、[DataSpace](https://github.com/HKUSTDial/DataSpace/blob/main/evaluation/README.md)、[Thinkingbox](https://github.com/microsoft/thinkingbox-data/blob/main/releases/thinkingbox_bench_v1/README.md)、[DAYJOB](https://arxiv.org/abs/2610.01306)。

   需要 LLM judge 的地方（开放长文交付）都在用专家写的细粒度原子 rubric 收紧它：DAYJOB 每题中位 47.5 / 57.5 条（[arXiv](https://arxiv.org/abs/2610.01306)），FrontierFinance 共 11,543 条（[arXiv](https://arxiv.org/abs/2608.11683)）。

3. **专家知识的注入方式正从"专家出题"转向"从真实工件反推，或由 agent 合成"，但专家验证在变薄。** 三种来源：
   - 人工重投入：CADWorld 约 1,300 人时（[PDF](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)）；DAYJOB 由从业者出题（[arXiv](https://arxiv.org/abs/2610.01306)）；DataSpace 有 11 名专家做修复（[arXiv](https://arxiv.org/abs/2608.03451)）。
   - 从真实工件反推：BI 看板（[BI-Bench](https://arxiv.org/abs/2609.20886)）、官方软件文档（[EngiWorld 任务 source](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/task-01.json)）、ICD-10 诊断（[CASE](https://arxiv.org/abs/2609.39566)）、Alibaba listing（[Business Arena](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)）。
   - agent 合成：[GDPevo](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_3_Quality_Filtering/review_workspace/guides/review_criteria.md) 的 builder 和 6 个 reviewer 都是 agent；[AgenticDataBench](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/generator/README.md) 用 skill graph 合成后再做专家标注；[TerminalHorizon](https://arxiv.org/abs/2610.13166) 用独立执行来审计合成环境是否把关键工作提前做掉了。

   风险：合成管线常按某个前沿 agent 的通过率校准难度，例如 GDPevo 设定 base avg@3 ≈ 0.4–0.6（[review_criteria](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_3_Quality_Filtering/review_workspace/guides/review_criteria.md)）。

4. **隐私和敏感数据的两条路：建一个隐藏真值的模拟世界，或者把数据"返还"给数据方。**
   - 模拟世界：Argo-Bench 明说因为真实企业仓库太敏感，所以模拟了一家公司并导出成 ERP schema（[arXiv](https://arxiv.org/abs/2610.02122)）；Business Arena 对供应商身份做了脱敏和改写（[PDF](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)）；池中的 Era by Eon、STS 也走这条路（[2609.09853](https://arxiv.org/abs/2609.09853)、[2610.10549](https://arxiv.org/abs/2610.10549)）。
   - 返还数据：医疗方面，CASE 只公开脱敏轨迹，完整基准返还 UK Biobank，供获批研究者访问（[README](https://github.com/VinyehShaw/CASE/blob/main/README.md)）。

5. **防作弊和防污染已经成为环境工程的一等公民。**
   - 防作弊：Argo-Bench 记录了无文件系统边界的沙箱里 agent 读 grader、拿到 0.99 分的过程（[reward_hacking](https://github.com/TextQLLabs/Argo-Bench/blob/main/analysis/reward_hacking/README.md)）；EngiWorld 从 shell history 检测 GUI 旁路（[eval.py](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/eval.py)）；Business Arena 用分离的系统身份做文件权限隔离（[PDF](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)）。
   - 防污染：
     - 私有留出集：AgenticDataBench 98 题、DataSpace 350 题、ScienceIDE 49 个环境、DAYJOB 30 题，见各卡片 §2.4 / 2.5 / 2.9 / 2.3。
     - 发布同配置、不同种子的 sibling build（[Argo-Bench](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)）。
     - canary GUID（[ScienceIDE task](https://github.com/aitofound/ScienceIDE/blob/main/hard85/mitgcm-atmos/mitgcm-atmos-repair-sem-data-aim-convection-qbl/instruction.md)）。
     - 两天内自动扩容出 V2（[GDPevo](https://arxiv.org/abs/2608.03764)）。

6. **能同时当训练环境的专业基准还很少；harness 带来的差异常常不小于模型之间的差异。**
   - 训练闭环：ScienceIDE 做了 SFT + GRPO（[RL README](https://github.com/aitofound/ScienceIDE/blob/main/RL/README.md)）；NeutronGym 用 RL 把成绩从 11% 提到 77%（[arXiv](https://arxiv.org/abs/2610.03631)）；CASE 做 RSFT + GRPO，训练时用缓存回放的 mock 工具省成本（[README](https://github.com/VinyehShaw/CASE/blob/main/README.md)）；BI-Agent 做了 SFT + RFT（[post-train](https://github.com/Hu-Chuxuan/bi-agent/blob/release/post-train/README.md)）。反观 Thinkingbox-Bench，明确禁止用于训练（[release](https://github.com/microsoft/thinkingbox-data/blob/main/releases/thinkingbox_bench_v1/README.md)）。
   - harness 差异：DataSpace 固定 backbone 时，换 harness 差 15.36 分（[arXiv](https://arxiv.org/abs/2608.03451)）；FrontierFinance 认为 harness 强烈影响质量与效率（[arXiv](https://arxiv.org/abs/2608.11683)）；EngiWorld 上 DeepSeek V4.1 Flash 的 CLI 48.3 分对 GUI 只有 2.0 分（[README](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)）。

---


## 1. 筛选表（输入 70 篇，全部按摘要筛选）

每行理由均基于该行 arXiv 摘要（链接即出处）。

| # | Title | arXiv | Inst. / HF↑ | 相关? | 理由 |
|---|---|---|---|---|---|
| 0 | DarwinX: Evolving Agent Harnesses Through Natural Selection | [2608.07545](https://arxiv.org/abs/2608.07545) | Salesforce AI Research / 87 | 否 | harness 自进化（Terminal-Bench 等通用 benchmark），无专业领域环境构建 |
| 1 | SWE-Bench ProMax: Benchmarking Agents on Large-Scale Multilingual Code Refactoring | [2608.09802](https://arxiv.org/abs/2608.09802) | ByteDance / 128 | 否 | 通用代码重构 benchmark，非专业领域 |
| 2 | OSWorld-Science: A Benchmark of Computer Use Agents for Learning and Using Scientific Software | [2609.39903](https://arxiv.org/abs/2609.39903) | DiscoAILab / 28 | 是·深读 | 科学软件 CUA benchmark，146 tasks，artifact-based evaluation |
| 3 | AgenticDataBench: A Comprehensive Benchmark for Data Agents | [2607.01647](https://arxiv.org/abs/2607.01647) | Tsinghua University / 29 | 是·深读 | data agent 综合 benchmark（data science workflow） |
| 4 | Opera: A Verbal Critic Framework for Long-horizon Coding Agents | [2609.33987](https://arxiv.org/abs/2609.33987) | Salesforce AI Research / 8 | 否 | coding agent verbal critic 方法 |
| 5 | Towards Autonomous and Auditable Medical Imaging Model Development | [2607.10522](https://arxiv.org/abs/2607.10522) | Chinese University of Hong Kong / 7 | 部分 | 医学影像 MLE 多智能体框架；是方法而非环境，验证协议值得一瞥 |
| 6 | LongHorizon-Harness: Advancing Long-Horizon Agents for Real-World Tasks | [2608.01964](https://arxiv.org/abs/2608.01964) | alibaba / 175 | 否 | 通用长程 harness |
| 7 | RRSI: Regularized Recursive Self-Improvement of Agent Harnesses | [2609.24972](https://arxiv.org/abs/2609.24972) | Google / 162 | 否 | harness RSI 方法 |
| 8 | AtomiMed: Hierarchical Atomic Fact-Checking for Universal Clinical-Aware Medical Report Evaluation | [2606.31292](https://arxiv.org/abs/2606.31292) | Zhejiang University / 4 | 部分 | 医学报告生成的 atomic-fact 评测器（可作 verifier 参考），非 agent 环境 |
| 9 | Sharpening Tax in Post-Training | [2610.01509](https://arxiv.org/abs/2610.01509) | Meta / 69 | 否 | RL 后训练分析 |
| 10 | InternReviewer & InternAdvocate: Objective Reward and Evaluation for Agentic Reinforcement Learning in Peer Review and Rebuttal | [2608.28612](https://arxiv.org/abs/2608.28612) | Shanghai AI Laboratory / 7 | 部分 | peer review/rebuttal 的 agentic RL reward；学术写作域，与核心专业域偏远 |
| 11 | ComponentBench: Diagnosing Component-Level Failures in Computer-Use Agents | [2608.18307](https://arxiv.org/abs/2608.18307) | — / — | 否 | 通用 Web UI 组件级 GUI benchmark |
| 12 | Scaling Agentic Data for Long-Horizon Terminal Intelligence | [2610.13166](https://arxiv.org/abs/2610.13166) | alibaba / 136 | 部分（简要卡片 §2.18） | terminal 长程专业任务的数据/环境合成（数据准备相关）；引擎无代码，仅项目页 |
| 13 | Cura 1T: Specialized Model for Agentic Healthcare | [2607.15314](https://arxiv.org/abs/2607.15314) | actAVA AI / 38 | 部分 | 医疗专用模型训练（含 EHR tool use），重模型训练而非环境构建 |
| 14 | MatrAIx: Simulating the World with 8.3 Billion Persona Agents | [2608.04205](https://arxiv.org/abs/2608.04205) | MatrAIx / 44 | 否 | persona 模拟用户评测基础设施 |
| 15 | AIM: Agentic Idea Management for Automated Research | [2609.38445](https://arxiv.org/abs/2609.38445) | Google / 47 | 否 | 自动科研 idea 管理 |
| 16 | Business Arena: Benchmarking LLM Agents in a Realistic Marketplace | [2608.08621](https://arxiv.org/abs/2608.08621) | alibaba / 20 | 是·深读 | 跨境电商经营模拟环境，基于真实市场数据 |
| 17 | DataSpace: Benchmarking Data Agents for Verifiable Analytics over Heterogeneous Workspaces | [2608.03451](https://arxiv.org/abs/2608.03451) | HKUSTDial / 33 | 是·深读 | 异构 workspace 上的可验证数据分析 benchmark |
| 18 | WeClawArena: An Auditable Sandbox and Benchmark for Cross-User Agents Collaboration and Security in Human-Centered Agent Networks | [2608.03499](https://arxiv.org/abs/2608.03499) | Carnegie Mellon University / 8 | 否 | 跨用户 agent 协作/安全沙盒 |
| 19 | NVIDIA-labs OO Agents: Native Python Object-Oriented Agents | [2607.20709](https://arxiv.org/abs/2607.20709) | NVIDIA / 26 | 否 | agent 开发框架 |
| 20 | A^2E : An End-to-End Agent Auditing Engine | [2608.07346](https://arxiv.org/abs/2608.07346) | Shanghai AI Laboratory / 12 | 否 | harness 评测引擎 |
| 21 | AREX: Towards a Recursively Self-Improving Agent for Deep Research | [2607.21461](https://arxiv.org/abs/2607.21461) | Beijing Academy of Artificial Intelligence / 139 | 否 | deep research agent |
| 22 | Tencent WorkBuddy Bench: A Multi-Domain Coding-Agent Benchmark with Contamination-Resistant Task Construction | [2607.20911](https://arxiv.org/abs/2607.20911) | Tencent / 21 | 部分 | 多领域 coding-agent benchmark（含 Office），任务从真实 commit/业务场景反推；偏 coding/office |
| 23 | One Success Isn't Reliability: Thinkingbox, a Sandbox and Benchmark for Agents in Stateful Business Workflows | [2608.19741](https://arxiv.org/abs/2608.19741) | Microsoft / 9 | 是·深读 | 有状态业务工作流 sandbox（MCP、policy、状态转移验证） |
| 24 | When Memory Lies: An Empirical Study of Spatial Memory Staleness in VLM Agents | [2608.04574](https://arxiv.org/abs/2608.04574) | Tencent / 16 | 否 | 空间记忆研究（FrozenLake） |
| 25 | MOLE: Detecting Insider Threats in AI Agents | [2609.06966](https://arxiv.org/abs/2609.06966) | Carnegie Mellon University / 16 | 否 | insider-threat 安全 benchmark |
| 26 | Scores Alone Do Not Prove Discovery: The Discovery Certification Protocol for Auditing AI Research Agents | [2609.09219](https://arxiv.org/abs/2609.09219) | Carnegie Mellon University / 15 | 否 | 科研 agent 审计协议 |
| 27 | FinanceComplexQA: Benchmarking Agentic Reasoning on Industrial-grade Financial Documents | [2607.19238](https://arxiv.org/abs/2607.19238) | Beihang University / 6 | 部分 | 合成金融文档 QA（Finance-LaTeX skill 生成 2,000 文档）；低声誉，未深读 |
| 28 | Inducing Task Models from Computer-Use Traces | [2608.20319](https://arxiv.org/abs/2608.20319) | — / — | 否 | 从 computer-use trace 归纳任务模型 |
| 29 | Voice Memory for Agentic Speech Recognition | [2607.26410](https://arxiv.org/abs/2607.26410) | NVIDIA / 5 | 否 | ASR |
| 30 | FinanceHarness: Autonomous Financial Deep Research Framework | [2607.27853](https://arxiv.org/abs/2607.27853) | unknown / 11 | 部分 | 金融 deep research harness + point-in-time benchmark（防未来信息泄漏思路可借鉴），低声誉 |
| 31 | SkillGym: Training Skill-Use Agents with Automatic Verifiable Environment Generation | [2609.37539](https://arxiv.org/abs/2609.37539) | unknown / 5 | 部分 | skill-use 环境自动合成（通用方法，属 env-methods 组） |
| 32 | EngiWorld: What Can Frontier Agents Deliver in Professional Engineering Environments? | [2609.37686](https://arxiv.org/abs/2609.37686) | Zhiman AI / 53 | 是·深读 | 工程软件（CAD/CAE/CAM/BIM/EDA/3D）真实专业软件 benchmark，1,301 expert-curated tasks |
| 33 | Agentic RAG Evaluation: Budget Allocation Across Questions, Trajectories, and Reads | [2610.05034](https://arxiv.org/abs/2610.05034) | Carnegie Mellon University / 19 | 否 | agentic RAG 评测预算 |
| 34 | Securing the AI Agent: A Unified Framework for Multi-Layer Agent Red Teaming | [2606.31227](https://arxiv.org/abs/2606.31227) | Tencent / 8 | 否 | agent 红队框架 |
| 35 | StartupBench: Benchmarking General-Purpose Agents on Market-Validated End-to-End Workflows | [2608.17800](https://arxiv.org/abs/2608.17800) | ByteDance Seed / 8 | 部分 | 基于市场验证的 AI 产品构造任务（任务来源思路），ByteDance Seed，无代码 |
| 36 | Qwen-Planner-Agent: A Closed-Loop AI-for-AI Framework for Real-World Mobile Planner Agents | [2609.29892](https://arxiv.org/abs/2609.29892) | Tongyi-MAI / 9 | 否 | 移动端 planner |
| 37 | Interactive Training 2: Auditable Control Plane for Live Model Training | [2607.18314](https://arxiv.org/abs/2607.18314) | University of Waterloo / 15 | 否 | 训练控制平面 |
| 38 | AskChem: Claim-Centered Infrastructure for Chemistry Literature Synthesis | [2607.28618](https://arxiv.org/abs/2607.28618) | New York University / 292 | 部分 | 化学文献 claim 级检索基础设施，非 agent 环境 |
| 39 | Apodex 1.1: Scaling Agentic Intelligence for Complex Work | [2608.23283](https://arxiv.org/abs/2608.23283) | Apodex / 172 | 部分 | 通用 working-capability 环境扩展（file/search/code），非专业域 |
| 40 | Auditing Web Agent Evaluation on WebArena-Lite: Human Review of Outcomes and Trajectories | [2610.01491](https://arxiv.org/abs/2610.01491) | — / — | 否 | WebArena-Lite 人工审计（verifier 可靠性有参考价值但非专业域） |
| 41 | CADWorld: Computer-Use Benchmark for Long-Horizon Computer-Aided Design | [2609.16251](https://arxiv.org/abs/2609.16251) | unknown / 5 | 是·深读 | FreeCAD 长程 CAD computer-use benchmark |
| 42 | WorldAuditBench: Interactive 3D World Auditing with Multimodal Agents | [2609.40325](https://arxiv.org/abs/2609.40325) | University of California, Santa Barbara / 93 | 否 | 3D 世界异常审计 |
| 43 | DecepEval: A Benchmark for Evaluating Deception in LLM Agents | [2610.07967](https://arxiv.org/abs/2610.07967) | Xi'an Jiaotong University / 66 | 否 | 欺骗行为评测（专业场景仅作背景） |
| 44 | SWE-bench Science: Can Coding Agents Resolve Engineering Tasks in Science? | [2608.19799](https://arxiv.org/abs/2608.19799) | OpenMOSS / 61 | 是·深读 | 科学软件仓库级 SWE benchmark（20 个科学领域） |
| 45 | False Frontiers: Diagnosing and Mitigating Co-Cheating in Self-Evolving Search Agents | [2609.39102](https://arxiv.org/abs/2609.39102) | Rutgers University / 192 | 否 | 自进化搜索 agent co-cheating |
| 46 | Learning to Evaluate Before Improving: Automatic Rubric Induction for Automatic Research Agents | [2608.31076](https://arxiv.org/abs/2608.31076) | ZJUNLP / 15 | 部分 | 科研 agent 的 task-specific executable rubric 自动归纳（verifier 构造方法） |
| 47 | AgenticSTS: A Bounded-Memory Testbed for Long-Horizon LLM Agents | [2607.02255](https://arxiv.org/abs/2607.02255) | Alaya Studio / 46 | 否 | 记忆 testbed |
| 48 | SkillZip: Contract-Preserving Graph Compression for Scalable Agent Skill Libraries | [2608.05604](https://arxiv.org/abs/2608.05604) | unknown / 74 | 否 | skill 压缩 |
| 49 | SkillGate: Training In-Policy Skill Selection in Long-Horizon Agents | [2608.18852](https://arxiv.org/abs/2608.18852) | Shanghai Jiao Tong University / 2 | 否 | skill 选择 RL |
| 50 | From Given to Gathered Evidence: Agentic Learning for Longitudinal Medical Reasoning | [2609.39566](https://arxiv.org/abs/2609.39566) | CASE / 12 | 是·深读 | UK Biobank 纵向多模态临床证据搜集 benchmark + agentic 后训练 |
| 51 | DSWorld: A Data Science World Model for Efficient Autonomous Agents | [2607.15901](https://arxiv.org/abs/2607.15901) | HKUSTGZ / 4 | 部分 | data science world model（用学习的模拟器替代真实执行），低声誉，未深读 |
| 52 | Same Agent, Different Answers: A Repeat-Aware Audit of Corpus-Induced Answer Churn in Retrieval-Augmented QA | [2608.22856](https://arxiv.org/abs/2608.22856) | Carnegie Mellon University / 4 | 否 | RAG answer churn 审计 |
| 53 | Prime Agent: A Self-Improving RLM Harness | [2608.23552](https://arxiv.org/abs/2608.23552) | Prime Intellect / 32 | 否 | 通用 harness |
| 54 | Token-Efficient Data Reasoning Agents via Adaptive Structuring of Unstructured Data | [2608.31082](https://arxiv.org/abs/2608.31082) | Harvard University / 4 | 部分 | 非结构化文档（filings/contracts）结构化以降本，方法论文 |
| 55 | Towards Expert Financial QA via Self-Improving RAG | [2608.26706](https://arxiv.org/abs/2608.26706) | — / — | 部分 | 金融 QA RAG 方法，无环境贡献 |
| 56 | DAYJOB: A Benchmark for Long-Horizon Professional Work | [2610.01306](https://arxiv.org/abs/2610.01306) | — / — | 是·深读 | 医疗+金融专业人员构建 130 tasks、Harbor 容器、专家 binary rubric |
| 57 | Are LLMs Ready for Scientific Discovery? A Capability-Oriented Benchmark for AI Scientists | [2607.11079](https://arxiv.org/abs/2607.11079) | HKUST / 3 | 部分 | 科学数据分析 benchmark（527 tasks，按能力组织）；无代码，未深读 |
| 58 | LMBuild: Evaluating LLM Agents for Generating Buildable and Functional Structures | [2610.04292](https://arxiv.org/abs/2610.04292) | University of Illinois at Urbana-Champaign / 31 | 部分 | 可建造/功能性 3D 结构生成，物理可实现性评估；偏生成而非专业软件 |
| 59 | GDPevo: Evaluating Agent Self-Evolution on Real Business Tasks | [2608.03764](https://arxiv.org/abs/2608.03764) | Prism Shadow / 27 | 是·深读 | GDP 相关企业工作流的自进化 benchmark + 全自动数据管线 |
| 60 | ScienceIDE: Turning World's Scientific Codebase into Agent Learnable Environments | [2609.19134](https://arxiv.org/abs/2609.19134) | PhAI Labs / 71 | 是·深读 | 把科学代码库转成可学习环境，专家定义 case 与 acceptance criteria |
| 61 | SearchJev: A Fast and Calibrated System-1 Model for Search Agents | [2610.05107](https://arxiv.org/abs/2610.05107) | Unknown / 20 | 否 | 搜索 agent System-1 模型 |
| 62 | LoopArena: Benchmarking Models as Runtime Controllers for Loop Engineering | [2608.28281](https://arxiv.org/abs/2608.28281) | AMAP-ML / 99 | 否 | coding loop 控制器 benchmark |
| 63 | Managing Procedural Memory in LLM Agents: Control, Adaptation, and Evaluation | [2606.23127](https://arxiv.org/abs/2606.23127) | unknown / 17 | 部分 | 企业 6 角色 382 tasks 的程序性记忆 benchmark；无机构信息，未深读 |
| 64 | Argo-Bench: Evaluating Data Agents on Enterprise-Scale Workflows | [2610.02122](https://arxiv.org/abs/2610.02122) | TextQL / 18 | 是·深读 | 企业级数据科学/分析 210 tasks，基于公开数据+行业文献 |
| 65 | SKILLER: Language-Level Reinforcement Learning for Reusable Skill Extraction in Small Language Models | [2608.10538](https://arxiv.org/abs/2608.10538) | OpenDataLab / 14 | 否 | skill 抽取 RL |
| 66 | SAEScientist-Bench: Can AI Agents Conduct Autonomous SAE Interpretability Research? | [2609.09113](https://arxiv.org/abs/2609.09113) | Chinese Academic of Science Institute of Automation / 16 | 否 | SAE 可解释性科研 agent |
| 67 | AutoSciBench: Autonomous Benchmark Generation for Evaluating Scientific Agents | [2610.05140](https://arxiv.org/abs/2610.05140) | Genentech / 29 | 部分 | 科学 agent benchmark 自动生成（Genentech），任务合成思路相关；无代码，未深读 |
| 68 | From Prompts to Contracts: Harness Engineering for Auditable Enterprise LLM Agents | [2607.08028](https://arxiv.org/abs/2607.08028) | — / — | 否 | 企业 harness 工程实践 |
| 69 | LongMedBench: Benchmarking Medical Agents for Long-Horizon Clinical Decision-Making | [2607.09322](https://arxiv.org/abs/2607.09322) | — / — | 部分 | MIMIC-IV 构造长程临床决策 benchmark；无机构/声誉信号，未深读 |

### 1b. 从全量池补捞的专业领域环境/benchmark 论文（不在 70 篇输入中）

| Title | arXiv | 声誉信号 | 处理 | 理由（出处=该行 arXiv 摘要） |
|---|---|---|---|---|
| NeutronGym: Physics-Graded Neutron Instrument Design for LLM Agents | [2610.03631](https://arxiv.org/abs/2610.03631) | 无 | 深读 | McStas ray-trace 仿真器作为 verifier、无 LLM judge、可 RL |
| BI-Agent and BI-Bench | [2609.20886](https://arxiv.org/abs/2609.20886) | Microsoft Research, HF 14↑, code | 深读 | 从真实公开 BI 项目/dashboard 人工抽取 QA |
| SimuVerity: Engineering-Grade Simulink Model Generation | [2610.02304](https://arxiv.org/abs/2610.02304) | XJTU, HF 47↑, code | 深读 | 原生 Simulink 仿真场景作为工程验收 |
| FrontierFinance | [2608.11683](https://arxiv.org/abs/2608.11683) | 无 | 深读 | 220 expert-crafted queries + 11,543 source-attributed rubrics |
| E-Commerce Bench | [2608.30730](https://arxiv.org/abs/2608.30730) | Qwen, HF 8↑, code | 浏览 | 365 天电商经营模拟，商品/供应商数据来自真实平台；与 Business Arena 同类 |
| FinProBench | [2608.04077](https://arxiv.org/abs/2608.04077) | 无 | 浏览 | 从从业者真实交付物反推 role-grounded rubric（RGRC） |
| FinAutoRubric | [2609.35744](https://arxiv.org/abs/2609.35744) | 无 | 浏览 | 专家写可复用评估指南，agent 生成 query-specific rubric，失败升级人工 |
| FinResearchBench II | [2607.12252](https://arxiv.org/abs/2607.12252) | 无 | 浏览 | 104 真实用户 query，自动合成 14,450 候选 rubric，三专家 vs 三 LLM judge 一致性 |
| FinEvo-Bench | [2608.06144](https://arxiv.org/abs/2608.06144) | 无 | 浏览 | 机构提供的专业流程 + 真实案例，人工审核 rubric |
| DataClawEval | [2607.28033](https://arxiv.org/abs/2607.28033) | 无 | 浏览 | 基于企业数据工程师生产代码，5 种执行引擎，case-specific 执行验证 |
| The Era by Eon Benchmark | [2609.09853](https://arxiv.org/abs/2609.09853) | 无 | 浏览 | 种子化虚构企业 + Salesforce/Zendesk/Slack 等产品模拟器，精确 ground truth |
| Synthesis Through Simulation (STS) | [2610.10549](https://arxiv.org/abs/2610.10549) | SAP, HF 3↑ | 浏览 | 通过对 policy-enforcing API 执行操作合成企业数据（规避真实企业数据法务限制） |
| A computable representation of the physical laboratory | [2609.03621](https://arxiv.org/abs/2609.03621) | 无 | 浏览 | 机器人实验室：stateful simulation 在 dispatch 前校验前置条件与实验室约束（物理动作安全） |
| From Benchmark to Bench (MAGI) | [2610.06411](https://arxiv.org/abs/2610.06411) | 无 | 浏览 | 3 家药企 9 个回溯 lead-optimization campaign，按时间截断回放 |
| Optimal Resource Utilization for Autonomous Laboratory Orchestrators | [2607.01188](https://arxiv.org/abs/2607.01188) | 无 | 浏览 | MOF 合成自主实验平台，多仪器容量约束的 constraint programming 调度 |
| ResidencyRL | [2608.07418](https://arxiv.org/abs/2608.07418) | 无 | 浏览 | LLM 模拟病人的多轮临床 encounter RL 环境 |
| AgentMercury | [2608.20634](https://arxiv.org/abs/2608.20634) | HF 7↑ | 浏览 | 4,783 个可执行业务环境，14 行业，cross-service invariants |
| StarHarness | [2608.24804](https://arxiv.org/abs/2608.24804) | ServiceNow-AI, HF 35↑ | 跳过 | harness 进化，用到 EnterpriseOps-Gym ITSM / AutomationBench Finance，非环境构建 |
| MedicalHarness | [2610.05778](https://arxiv.org/abs/2610.05778) | 无 | 跳过 | 医疗任务上 harness 对照研究（107 tasks） |


---

## 2. 环境构建卡片（深读）

### 2.1 OSWorld-Science — 科学软件 computer-use benchmark
arXiv [2609.39903](https://arxiv.org/abs/2609.39903) · 2026-10-01 · DiscoAILab（作者含 Jie Tang、Juanzi Li 等，见 [README citation](https://github.com/DiscoAILab/OSWorld-Science/blob/main/README.md)）· HF 28↑ · 代码 [DiscoAILab/OSWorld-Science](https://github.com/DiscoAILab/OSWorld-Science) · 证据深度：摘要 + 仓库 README/docs/评分代码（数据与 VM 镜像在 HF，未下载）

- **领域与任务类型**：7 个科学领域（Chemistry 43 / Physics 31 / Medicine 26 / Statistics 20 / Biology 18 / GIS 6 / Linguistics 2），146 tasks；分子绘制、逆合成、病理图像、统计计算、CFD 等 [README](https://github.com/DiscoAILab/OSWorld-Science/blob/main/README.md)。
- **环境形态**：**真实专业软件**跑在 OSWorld 风格 VM 中：QuPath、ChemDraw、ASKCOS、SAS/R、OpenFOAM、ANSYS、EEGLAB、PyMOL/Mnova、QGIS、CIAO+DS9、Weasis、Praat、3D Slicer [README](https://github.com/DiscoAILab/OSWorld-Science/blob/main/README.md)。全部任务需视觉观测，83.6% 同时支持 CLI，16.4% 仅 GUI [README](https://github.com/DiscoAILab/OSWorld-Science/blob/main/README.md)。
  - 状态初始化/重置：每个任务指定 VM snapshot，`config` 依次执行 execute/upload(带 sha256)/launch/sleep 对 fresh guest 进行 staging [adding-a-task.md](https://github.com/DiscoAILab/OSWorld-Science/blob/main/docs/user_guide/adding-a-task.md)；`tools_probe` 失败时自动 provision，使 `osci vm reset` 自愈 [adding-a-domain.md](https://github.com/DiscoAILab/OSWorld-Science/blob/main/docs/developer_guide/adding-a-domain.md)。
  - 商业软件/许可证处理：Mnova 需用户自带机构 licence，经 pre-task hook 注入 guest [vm_prep/biomed/README.md](https://github.com/DiscoAILab/OSWorld-Science/blob/main/scripts/vm_prep/biomed/README.md)；SAS 不装在镜像里，九个 SAS-or-R 任务经 Firefox 访问 SAS OnDemand for Academics [configs/snapshots.yaml](https://github.com/DiscoAILab/OSWorld-Science/blob/main/configs/snapshots.yaml)；Windows 10 + Ansys Student（Fluent）镜像不可再分发，只给重建 recipe [configs/snapshots.yaml](https://github.com/DiscoAILab/OSWorld-Science/blob/main/configs/snapshots.yaml)。部分 biomed 任务运行时需要访问 RCSB / AlphaFold DB / SynergyFinder 外网 [vm_prep/biomed/README.md](https://github.com/DiscoAILab/OSWorld-Science/blob/main/scripts/vm_prep/biomed/README.md)（→ 可复现性风险）。
  - 成本：每并发 guest 约 8 GB RAM / 4 vCPU；8 个公开镜像全量约 196 GB，单镜像 23–34 GB [README](https://github.com/DiscoAILab/OSWorld-Science/blob/main/README.md)。
  - 安全约束：输入文件以 hash gate 保护（`protected_inputs_hash`）；solver 写的 R 代码在评分主机上执行、30 分钟上限，作者建议在容器中评分 [grading_env/README.md](https://github.com/DiscoAILab/OSWorld-Science/blob/main/scripts/grading_env/README.md)。
- **任务来源**：expert proposals + 迭代 human–AI co-design，按科学价值与难度筛选 [arXiv](https://arxiv.org/abs/2609.39903)。任务 JSON 含 `source` 字段（要求不写 URL/课程号）及 `bench` 审计字段 [adding-a-task.md](https://github.com/DiscoAILab/OSWorld-Science/blob/main/docs/user_guide/adding-a-task.md)。作者也接受任务作者自带 grader，原样放入 `reference_private/` [adding-a-task.md](https://github.com/DiscoAILab/OSWorld-Science/blob/main/docs/user_guide/adding-a-task.md)。
- **验证与奖励**：task-specific execution-based evaluators 检查应用状态与产物（分子结构、分割 mask、图、数值），给 partial credit [arXiv](https://arxiv.org/abs/2609.39903)。实现上：`weighted` 组合多个 check；`stages` gate 失败则后续 check 全部归零（"a number extracted from tampered inputs is not a partially correct number"）[score.py](https://github.com/DiscoAILab/OSWorld-Science/blob/main/src/osworld_science/evaluators/score.py)；gt 叶子为 `{"expect","tol_abs"|"tol_rel","floor"}` 数值容差 [adding-a-task.md](https://github.com/DiscoAILab/OSWorld-Science/blob/main/docs/user_guide/adding-a-task.md)；`r_function_probe` 用 held-out 参数调用 solver 写的 R 函数 [grading_env/README.md](https://github.com/DiscoAILab/OSWorld-Science/blob/main/scripts/grading_env/README.md)。
  - 防 hack：stat 任务"每题两套数据、输入 hash gate、可执行 grader、先写 negative tests"；grader 测试要求所有 shortcut 变体 FAIL、容差内变体 PASS [adding-a-task.md](https://github.com/DiscoAILab/OSWorld-Science/blob/main/docs/user_guide/adding-a-task.md)。
- **数据准备**：无训练数据；harness 记录 trajectory、步数与成本（models.yaml 记录价格）[README](https://github.com/DiscoAILab/OSWorld-Science/blob/main/README.md)。
- **规模与开放**：146 tasks / 12 VLMs [arXiv](https://arxiv.org/abs/2609.39903)；代码 CC BY 4.0，数据与 VM 在 HF；EEGLAB 镜像未发布 [README](https://github.com/DiscoAILab/OSWorld-Science/blob/main/README.md)。
- **关键结果**：摘要仅定性称 SOTA VLM + 强 harness 仍面临挑战 [arXiv](https://arxiv.org/abs/2609.39903)；具体分数未在可达材料中看到（无出处，待核）。
- **局限与红旗**：公开数据集包含答案键，`private/` 只是对 solver 隐藏、非访问控制，作者自己提示可能被训练污染 [README](https://github.com/DiscoAILab/OSWorld-Science/blob/main/README.md)；依赖外网与商业许可证的任务难以完全复现 [snapshots.yaml](https://github.com/DiscoAILab/OSWorld-Science/blob/main/configs/snapshots.yaml)；领域分布不均（Linguistics 仅 2 题）[README](https://github.com/DiscoAILab/OSWorld-Science/blob/main/README.md)。
- **可复用配方**：
  1. "gate + weighted partial credit"：输入完整性 gate 失败则全零，否则按权重给分 [score.py](https://github.com/DiscoAILab/OSWorld-Science/blob/main/src/osworld_science/evaluators/score.py)。
  2. grader 先写 negative tests：从 gt 构造正确提交，再变异出 shortcut 必须 FAIL [adding-a-task.md](https://github.com/DiscoAILab/OSWorld-Science/blob/main/docs/user_guide/adding-a-task.md)。
  3. 商业软件许可证通过 pre-task hook 注入、镜像只给 build recipe [vm_prep/biomed/README.md](https://github.com/DiscoAILab/OSWorld-Science/blob/main/scripts/vm_prep/biomed/README.md)。
- **评级：必读**

### 2.2 EngiWorld — 26 款工程软件（CAD/CAE/CAM/BIM/EDA/DCC）的完整设计闭环
arXiv [2609.37686](https://arxiv.org/abs/2609.37686) · 2026-09-30 · Zhiman AI · HF 53↑ · 代码 [Hongcheng-Gao/EngiWorld](https://github.com/Hongcheng-Gao/EngiWorld) · 证据深度：摘要 + 仓库 README/task 定义/eval.py 抽样阅读

- **领域与任务类型**：CAD、CAE、CAM、BIM、EDA、3D visualization 6 域、26 个专业软件平台，GUI+CLI 双接口 [arXiv](https://arxiv.org/abs/2609.37686)。六类任务：Single-Software Execution 931 / Software Selection 140 / Vision-Guided Modeling 120 / Design Optimization 40 / Cross-Software Coordination 60 / Open-Environment Engineering 10 [README](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)。软件目录可见 SolidWorks、AutoCAD、Abaqus、Ansys、Revit、Archicad、Altium Designer、Cadence OrCAD、KiCad、FreeCAD、OpenFOAM、FEniCS、OpenFAST 等 [task/](https://github.com/Hongcheng-Gao/EngiWorld/tree/main/task)。
- **环境形态**：**真实专业软件**（含商业 Windows 软件）跑在 Docker 托管的 Windows/Ubuntu VM（复用 `happysixd/osworld-docker`），每环境默认 4 CPU / 16 GB RAM [README](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)。
  - 初始化：task JSON 的 `config` 上传输入 STEP 文件、launch SLDWORKS.exe，并用 pyautogui 按回车跳过启动对话框 [solidworks/task-01.json](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/task-01.json)。
  - 镜像与许可证：15 个公开镜像压缩约 98 GB；"公开目录外的 snapshot 需用户自备匹配镜像" [README](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)（即商业软件镜像大概率不随数据发布——推断，待核）。
  - 成本：README 报告每任务 $0.44–$18.78、69.5–119.6 turns（主实验 306 题）[README](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)。
- **任务来源**：摘要称 1,301 expert-curated tasks [arXiv](https://arxiv.org/abs/2609.37686)。仓库 `source` 字段统计（本人对 task JSON 计数）：约 1,105 个以官方软件文档 URL 开头（如 SolidWorks Help 页面），另有 "generated canonical reverse-CAD evidence package"（40）、"design-generated quantified CAE optimization task"（10）、"human_craft"（18）等 [solidworks/task-01.json 示例](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/task-01.json)、[task/](https://github.com/Hongcheng-Gao/EngiWorld/tree/main/task) → 专家知识主要通过"官方文档功能点 → 具体参数化建模指令"注入。
- **验证与奖励**：artifact-centric domain-verifier suite 程序化检查几何有效性、物理可行性、规则合规，对定量设计任务按 specification attainment 连续打分 [arXiv](https://arxiv.org/abs/2609.37686)。
  - 实例：SolidWorks 任务用 cadquery/OCP 读 STEP，检查孔半径、包围盒、孔位与体积，容差 `BBOX_TOL=0.10`、`POS_TOL=0.20`、`RADIUS_TOL=0.10`、`VOLUME_REL_TOL=0.02` [eval.py](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/eval.py)；eval.py 经 `postconfig` 上传进 VM 内执行 [task-01.json](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/task-01.json)。
  - 连续分：FEniCS 拓扑优化任务用 dolfin 重算 compliance，score = clamp(1 − submitted/baseline)，并校验 baseline 未被篡改、体积分数 ≤0.40 [design-optimization/cli/fenics/task-01/eval.py](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/design-optimization/cli/fenics/task-01/eval.py)。
  - **防 hack**：GUI 任务的 verifier 检测"GUI bypass"——桌面出现 .py/.ps1 等脚本、或 shell/PowerShell history 中有调用 cadquery/freecadcmd/solidworks 等写出产物的命令即判失败 [eval.py](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/eval.py)。
- **数据准备**：无训练数据；运行产出 traj.jsonl [README](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)。
- **规模与开放**：1,301 tasks 与 verifiers 全部开源（MIT），HF/ModelScope 镜像；论文主实验用 306 题子集 [README](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)。
- **关键结果**：摘要：最强模型 EngiScore 44.3，多软件任务仅 3.6% 成功 [arXiv](https://arxiv.org/abs/2609.37686)；README 表：Claude Opus 5 EngiScore 44.7（CLI 48.6 / GUI 40.5），GPT-5.6 Sol 38.6；DeepSeek V4.1 Flash CLI 48.3 但 GUI 仅 2.0 [README](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)。注意摘要 44.3 与 README 44.7 不一致（可能版本更新）。
- **局限与红旗**：答案/ground truth 随仓库公开（污染风险）[task/README.md](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/README.md)；"expert-curated" 但多数任务 source 为官方文档 URL，专家具体参与方式需读论文正文（无出处，待核）；2026-10-09 有任务 ID 重命名迁移 [id-migration-20261009.json](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/id-migration-20261009.json)；GUI bypass 检测基于关键词启发式，可被绕过（推断）。
- **可复用配方**：
  1. 以几何内核（cadquery/OCP）读取原生/中性 CAD 文件做容差几何断言 [eval.py](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/eval.py)。
  2. 优化类任务用"相对 baseline 的物理量改进"作连续奖励，并由 verifier 自己重跑求解器 [fenics eval.py](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/design-optimization/cli/fenics/task-01/eval.py)。
  3. GUI-only 任务显式检测脚本旁路（桌面脚本 + shell history）[eval.py](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/eval.py)。
- **评级：必读**

### 2.3 DAYJOB — 医疗 + 金融专业人员构建的长程专业工作 benchmark
arXiv [2610.01306](https://arxiv.org/abs/2610.01306) · 2026-10-01 · Surge AI（据仓库 [README](https://github.com/surge-ai/dayjob/blob/main/README.md)）· 早期版本被 NeurIPS 2026 AABA4ET workshop 接收（arXiv comment）· 代码 [surge-ai/dayjob](https://github.com/surge-ai/dayjob)（仅评测 harness；任务在 HF，未下载）· 证据深度：摘要 + harness README

- **领域与任务类型**：130 tasks，healthcare 50 / finance 80；专业人士估计平均耗时 13.6 h（医疗）/ 16.6 h（金融）；任务以简短请求开始，需要专业人员自己判断需要什么、哪些文档相关、前提是否成立 [arXiv](https://arxiv.org/abs/2610.01306)。
- **环境形态**：每个任务是容器化 Harbor 环境（`task.toml`、`instruction.md`、`environment/`、`tests/`）[README](https://github.com/surge-ai/dayjob/blob/main/README.md)；agent 用 OpenHands SDK，含 terminal/file-editor/task-tracker 工具，镜像可选挂 MCP server [harbor-agents/README.md](https://github.com/surge-ai/dayjob/blob/main/harbor-agents/README.md)。属于"真实格式的文件工作区"（mock 的企业文档/记录），非真实专业软件——具体文档是否来自真实记录需读论文（无出处，待核）。
  - 安全/隔离：agent 阶段网络仅允许模型 API host（nftables allowlist），浏览与包下载被阻断；setup 与 grading 阶段保留网络 [README](https://github.com/surge-ai/dayjob/blob/main/README.md)。
- **任务来源**：由医疗与金融领域专业人员构建 [arXiv](https://arxiv.org/abs/2610.01306)。
- **验证与奖励**：每题专家写的 binary-criteria rubric，中位数 47.5（医疗）/ 57.5（金融）条；由 agentic judge 对交付文件逐条判定；全部满足才算 pass [arXiv](https://arxiv.org/abs/2610.01306)。实现上 judge 为 Claude Opus 4.8 驱动的 OpenCode，在任务容器内运行，依赖 harbor-rewardkit 0.1.7；trial reward ∈[0,1]，任务分 = 5 次 attempt 平均（排除报错 trial），领域分 = 任务分的非加权平均 [README](https://github.com/surge-ai/dayjob/blob/main/README.md)。→ 论文 pass 口径（全满足）与仓库 reward 口径（0–1 连续）并存，引用时需区分。
- **数据准备**：无训练数据；保存 trajectory.json 与 verifier 日志 [README](https://github.com/surge-ai/dayjob/blob/main/README.md)。
- **规模与开放**：发布全部 50 个医疗任务、80 个金融任务中的 50 个、harness 与 leaderboard（30 个金融任务保留）[arXiv](https://arxiv.org/abs/2610.01306)。
- **关键结果**：30 个模型配置（13 家），最强 Claude Opus 5.5 医疗 24.7% / 金融 23.9% pass；中位配置 0.6% / 2.5%；案例中 agent 接受被记录反驳的前提、把错误输入带入一致的后续分析 [arXiv](https://arxiv.org/abs/2610.01306)。
- **局限与红旗**：judge 与被测模型同厂（Opus 4.8 judge 评 Claude 系）存在自偏风险（推断）；LLM judge 读交付文件，数值核对能力取决于 judge；保留 30 个金融题作 held-out 是好做法 [arXiv](https://arxiv.org/abs/2610.01306)。
- **可复用配方**：
  1. "专家写大量 binary 原子 criteria + agentic judge 在容器里读交付物 + all-or-nothing pass" [arXiv](https://arxiv.org/abs/2610.01306)。
  2. agent 阶段断网（仅放行模型 API），防止检索答案 [README](https://github.com/surge-ai/dayjob/blob/main/README.md)。
  3. 设计"前提可能错误"的请求以测专业判断 [arXiv](https://arxiv.org/abs/2610.01306)。
- **评级：必读**

### 2.4 AgenticDataBench — 15 个垂直领域的 data agent benchmark（含蚂蚁 B2B 真实用例）
arXiv [2607.01647](https://arxiv.org/abs/2607.01647) · 2026-07-03 · Tsinghua University + Ant Digital Technologies（[README Community](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/README.md)）· HF 29↑ · README 标注 VLDB（bibtex `journal={VLDB}`）· 代码 [AgenticDataBench/AgenticDataBench](https://github.com/AgenticDataBench/AgenticDataBench) · 证据深度：摘要 + README + generator 文档 + 任务/评测代码

- **领域与任务类型**：端到端 data science workflow（清洗、联表、统计、建模、可视化）[README](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/README.md)；15 个领域，含某头部 fintech 公司 5 个真实 B2B 用例 [arXiv](https://arxiv.org/abs/2607.01647)。公开 dev 集 246 题，按领域计数（本人统计）loan_risk 25、real_estate 25、financial 24、healthcare 24 … strategy 4 [tasks/dev.jsonl](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/testbed/tasks/dev.jsonl)。
- **环境形态**：**真实数据集 + 本地代码执行**（无专业 GUI 软件）；数据从 HF 下载到 `testbed/datasets/`，可接 Smolagents / DA-Agent / Claude Code / Codex 四种 harness [README](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/README.md)。
- **任务来源**（混合）：
  - 真实任务：收集 15 领域真实数据集与任务；对真实业务任务选择最大化多样性的 task–solution 对 [arXiv](https://arxiv.org/abs/2607.01647)。
  - 合成任务：从 Stack Overflow 大规模解答中经 skill-aligned hierarchical clustering 抽取"data science skills"，建加权 skill graph（节点=skill，边=相邻使用，权重=频次）；采样 skill path + 领域数据 + 相似示例 → LLM 依次生成 profile / skill tree / step workflow / 任务描述，并用 6 条质量准则校验 [generator/README.md](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/generator/README.md)；`--rare_skill_ratio` 默认 0.3 注入稀有 skill；`greedy_select.py` 剪枝到覆盖全部 skill 的最小集合 [generator/README.md](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/generator/README.md)。
  - 专家注入：Step 4 "Expert Annotation"——人工精修任务、解答代码与评测函数 [generator/README.md](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/generator/README.md)。
- **验证与奖励**：每题 `eval_func` 列表 + gold 文件 [tasks/dev.jsonl](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/testbed/tasks/dev.jsonl)；主要为 `compare_csv`（本人统计约 209 次调用），另有 compare_image / compare_json / compare_model / compare_sqlite 等；`compare_csv` 默认绝对容差 1e-2，可按列设 tolerance，返回 0–1 相似度分（partial credit）[table.py](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/testbed/da_agent/evaluators/metrics/table.py)；图表评测比对图对应的 json/npy 数据，按 subplot 计分 [image.py](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/testbed/da_agent/evaluators/metrics/image.py)。"fine-grained ground-truth labels" 支持 skill-level 诊断 [arXiv](https://arxiv.org/abs/2607.01647)。
- **数据准备**：无训练数据；合成管线本身可复用为数据生成器 [generator/README.md](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/generator/README.md)。
- **规模与开放**：98 题作为私有 test 保留，"失去评测意义后再公开" [README](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/README.md)；结果文件每份 344 条（= 246 公开 + 98 私有，本人推算）[testbed/results](https://github.com/AgenticDataBench/AgenticDataBench/tree/main/testbed/results)。
- **关键结果**（仓库结果文件平均分，本人读取）：smolagents-qwen 0.4708、smolagents-claude 0.4672、claude-code-claude 0.4659、codex-kimi 0.4879（最高）、codex-claude 0.3163（最低，完成率 0.8808）[testbed/results](https://github.com/AgenticDataBench/AgenticDataBench/tree/main/testbed/results) → 模型 × harness 差异大于模型差异。
- **局限与红旗**：公开 dev 的 gold 随仓库发布 [testbed/gold](https://github.com/AgenticDataBench/AgenticDataBench/tree/main/testbed/gold)；任务描述极度显式（字段名、阈值、模糊匹配阈值 80 都写进题面，见 agriculture_02）[tasks/dev.jsonl](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/testbed/tasks/dev.jsonl)——更像"规格执行"而非"开放分析"；B2B 真实数据的隐私处理方式需读正文（无出处，待核）。
- **可复用配方**：
  1. 从 Stack Overflow 解答挖 skill graph → 按 skill 路径采样合成任务 → 贪心最小覆盖剪枝 [generator/README.md](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/generator/README.md)。
  2. 输出约束为指定列名 CSV，用逐列容差比对得到确定性分数 [table.py](https://github.com/AgenticDataBench/AgenticDataBench/blob/main/testbed/da_agent/evaluators/metrics/table.py)。
- **评级：值得浏览**（数据合成方法好，但环境仅是文件+代码执行）

### 2.5 DataSpace — 异构 workspace 上的"可验证表格结果"数据分析（KDD Cup 2026 官方 benchmark）
arXiv [2608.03451](https://arxiv.org/abs/2608.03451) · 2026-08-07 · HKUSTDial（作者含 Nan Tang、Guoliang Li、Yuyu Luo，见 [README](https://github.com/HKUSTDial/DataSpace/blob/main/README.md)）· HF 33↑ · 代码 [HKUSTDial/DataSpace](https://github.com/HKUSTDial/DataSpace) · 证据深度：摘要 + README + evaluation/README + baseline README

- **领域与任务类型**：组织内 workspace 上的自然语言分析；证据分散在数据库、结构化文件、长文档、多媒体中；agent 只拿到问题与 workspace，返回完整表格结果 [arXiv](https://arxiv.org/abs/2608.03451)。覆盖证据发现、结构化抽取、跨表示 join、过滤聚合排序、时间推理、文档/视频理解；中英跨语言 [README](https://github.com/HKUSTDial/DataSpace/blob/main/README.md)。
- **环境形态**：**task-local 文件 workspace**（CSV/JSON/SQLite/Markdown/PDF/video，7,439 artifacts，15.01 GB）[arXiv](https://arxiv.org/abs/2608.03451)；baseline 提供共享离线 "Data Workbench Runtime"，模型生成命令一律无网络；对 Codex / Claude Code / Grok Build / smolagents 分别配置禁搜与 fail-closed sandbox，只读挂载数据 [baseline/README.md](https://github.com/HKUSTDial/DataSpace/blob/main/baseline/README.md)。
- **任务来源**：DataSpace-Builder：cross-language transformation、constraint-aware relational sampling、modality routing、artifact rendering（即把源数据渲染成 PDF/视频等模态），再由 **11 名领域专家** human review + task repair [arXiv](https://arxiv.org/abs/2608.03451) → "从结构化真值出发、渲染成异构证据"，因此天然有确定性 gold。
- **验证与奖励**：确定性 evaluator：header-invariant 列对齐、类型与精度感知归一化、order-aware 行比较 [arXiv](https://arxiv.org/abs/2608.03451)；每题 binary，需存在一个一一列映射使整表相等；无序任务比较行 multiset（含重复次数）；支持 text/number/date/datetime/Boolean 列与精度、单位规则；输出 config 集 SHA-256 [evaluation/README.md](https://github.com/HKUSTDial/DataSpace/blob/main/evaluation/README.md)。无 partial credit。
- **数据准备**：无训练数据。
- **规模与开放**：410 tasks 输入全部公开；仅 60 题公开 gold + config，其余 350 题 gold 保留用于官方评测；MIT [README](https://github.com/HKUSTDial/DataSpace/blob/main/README.md)。
- **关键结果**：6 个前沿多模态模型 × 5 个 harness，最好准确率 66.34%；固定 backbone 时 harness 选择造成 15.36 个点差异 [arXiv](https://arxiv.org/abs/2608.03451)。
- **局限与红旗**：数据为构造/渲染而成，"组织 workspace"的真实性取决于源数据（具体来源需读正文，无出处，待核）；全有或全无评分对长表很严格；领域上偏通用分析而非某一专业行业。
- **可复用配方**：
  1. 从结构化真值反向渲染多模态证据（PDF/视频），专家再修复任务 → 低成本获得确定性 gold [arXiv](https://arxiv.org/abs/2608.03451)。
  2. 表格评测：列名无关的一一映射 + 按列类型/精度/单位的冻结 config + config 哈希 [evaluation/README.md](https://github.com/HKUSTDial/DataSpace/blob/main/evaluation/README.md)。
  3. 输入全公开、gold 大部分保留（410 vs 60）抵抗污染 [README](https://github.com/HKUSTDial/DataSpace/blob/main/README.md)。
- **评级：值得浏览**（数据分析域中验证器设计最干净）

### 2.6 Argo-Bench — 模拟纽约外卖平台 + Oracle EBS 形态 ERP 仓库，按"行动后果"评分
arXiv [2610.02122](https://arxiv.org/abs/2610.02122) · 2026-10-02 · TextQL · HF 18↑ · 代码 [TextQLLabs/Argo-Bench](https://github.com/TextQLLabs/Argo-Bench) · 证据深度：摘要 + README + reference 解答 + reward_hacking 分析

- **领域与任务类型**：企业数据科学/分析/运营：欺诈团伙、促销经济学、月结（month-end close）、骑手薪酬、看板、预测；210 题 [README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)。任务卡带 `area`（如 Trust, Safety & Payments Risk）、`domain`、`data_cutoff`、`version` 哈希 [tasks/final.jsonl](https://github.com/TextQLLabs/Argo-Bench/blob/main/tasks/final.jsonl)。会计类示例：AR-to-GL 对账、资产负债表对账、1099-NEC [reference/](https://github.com/TextQLLabs/Argo-Bench/tree/main/reference)。
- **环境形态**：**simulator + 真实规模仓库**：依据公开数据、同行评审行业文献、监管 filings 模拟 2024 年纽约外卖平台（8,100 万订单），导出为仿 Oracle E-Business Suite schema 的 ERP 仓库（235 表、75 亿行）；**模拟器 ground-truth 状态对 agent 隐藏**，agent 需从仓库重建事实再行动 [arXiv](https://arxiv.org/abs/2610.02122)。
  - 工具：warehouse MCP（只读 `run_sql`/`list_tables`/`describe_table`）+ python MCP（持久解释器，含 pandas/scipy/statsmodels/OR-Tools）；agent 通过 "Mission Control" 控制台 *filing* 行动（封禁账户、记账分录、余额、预测、看板数据源）[README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)。
  - 时间截断：`data_cutoff` 早于 12 月的问题只能读到截至当月的 view schema，其它 schema 查询被拒 [README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)。
  - 隔离/成本：论文运行在 gVisor pod 中、无网络；每题 3,600 s / 500 turns；BigQuery 每查询扫描上限 20 GiB；仓库以 Parquet 发布 71 GiB [README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)。
- **任务来源**：基于模拟世界人工设计的业务请求；20 题附 reference 解答，docstring 写明"题目刻意省略了什么"与归档规则（如 ds-22 需自行发现 GL_IMPORT_REFERENCES 把分录挂到订单）[reference/ds_22_margin_monthly_per_order.py](https://github.com/TextQLLabs/Argo-Bench/blob/main/reference/ds_22_margin_monthly_per_order.py)；每题都有只用仓库即可解的可执行 reference solution [arXiv](https://arxiv.org/abs/2610.02122)。动机：真实企业仓库过于敏感无法发布 [arXiv](https://arxiv.org/abs/2610.02122)。
- **验证与奖励**：按 filing 在模拟器中的**后果**打分（不看文字回答）[arXiv](https://arxiv.org/abs/2610.02122)、[README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)；答案键 held out，本地只算 `filed`（是否有提交）与 smoke 的 `conformance`，需提交给维护者评分 [README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)。连续分（如 fraud 任务 0.991/0.222 等）见 [reward_hacking/README.md](https://github.com/TextQLLabs/Argo-Bench/blob/main/analysis/reward_hacking/README.md)。
  - **hackability 实录**：开发期 3 个 Gemini 3.8 Flash 运行在无文件系统边界的 local sandbox 中，诚实工作 90–155 步后离开工作目录，读到 grader 与答案键构建器，导入 kernel 离线用 grader 的 cost function 选封禁名单，两次得 0.99 [reward_hacking/README.md](https://github.com/TextQLLabs/Argo-Bench/blob/main/analysis/reward_hacking/README.md)。修复：gVisor/Docker `--network none`、macOS Seatbelt 仅可读工作目录 [README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)。
- **数据准备**：无训练数据；发布仓库为"同配置、不同随机种子的兄弟 build"，涉及具体实体的题目按选择规则重新抽取 [README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md) → 可复现又降低泄漏。
- **规模与开放**：代码 Apache-2.0，题卡与仓库 CC BY 4.0；39 个 model rung（12 模型 × 推理档位）[README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)。
- **关键结果**：14 个前沿与开源模型中最强者只在 34.8% 的任务上得分 ≥95（摘要截断处之后内容未见）[arXiv](https://arxiv.org/abs/2610.02122)。
- **局限与红旗**：世界是模拟的（经济学"grounded"程度依赖作者校准）；评分依赖维护者服务器、外部不可独立复核；部分题目在 final run 后修改了措辞（col-22-*）[README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)。
- **可复用配方**：
  1. "隐藏状态的模拟器 → 导出成真实 ERP schema 仓库 → agent 执行动作 → 在模拟器里结算后果"[arXiv](https://arxiv.org/abs/2610.02122)。
  2. 发布 sibling seed build + 按规则重抽实体，兼顾开放与防污染 [README](https://github.com/TextQLLabs/Argo-Bench/blob/main/README.md)。
  3. 沙箱必须有文件系统边界：公开记录的"读 grader"案例是最好的反面教材 [reward_hacking/README.md](https://github.com/TextQLLabs/Argo-Bench/blob/main/analysis/reward_hacking/README.md)。
- **评级：必读**

### 2.7 Thinkingbox — 有状态业务工作流 sandbox（MCP mock 后端 + 模拟用户 + 终态检查）
arXiv [2608.19741](https://arxiv.org/abs/2608.19741) · 2026-08-25 · Microsoft · HF 9↑ · 代码 [microsoft/thinkingbox](https://github.com/microsoft/thinkingbox)（框架）+ [microsoft/thinkingbox-data](https://github.com/microsoft/thinkingbox-data)（数据/工具服务器，经 raw 读取 README）+ thinkingbox-training（RL）· 证据深度：摘要 + 两仓库 README + docs

- **领域与任务类型**：507 个 policy-conditioned 工作流：零售电商 98 / 旅行酒店 104 / 车险 100 / neobank 支持 104 / 咨询公司 IT/HR 支持 101 [release README](https://github.com/microsoft/thinkingbox-data/blob/main/releases/thinkingbox_bench_v1/README.md)。agent 需多轮向（模拟）用户收集信息、遵循领域 policy、协调依赖工具、实现正确的持久状态转移且无附带副作用 [arXiv](https://arxiv.org/abs/2608.19741)。
- **环境形态**：**mock**：工具以 MCP server 形式实现（如 mcp_online_banking、mcp_email_system），每个 server 有 `__reserved__init`（初始化状态）与 `__reserved__geteffects`（取副作用供评测）；MCP Session Proxy 为每段对话 spawn 隔离 session、结束即销毁 [README](https://github.com/microsoft/thinkingbox/blob/main/README.md)。每题提供初始后端状态、用户目标与模拟用户上下文、领域工具、policy 约束 [release README](https://github.com/microsoft/thinkingbox-data/blob/main/releases/thinkingbox_bench_v1/README.md)；部分场景用 Typesense 搜索，每个场景自建 collection [release README](https://github.com/microsoft/thinkingbox-data/blob/main/releases/thinkingbox_bench_v1/README.md)。服务器包名含 `ms_toloka_servers`（暗示数据供应商参与，推断）[README](https://github.com/microsoft/thinkingbox/blob/main/README.md)。
- **任务来源**：由测试作者以 Python/YAML test case 编写；作者指南要求"可完成、可测量、真实"，示例强调按 effects 断言而非数工具调用次数 [writing_effective_tests.md](https://github.com/microsoft/thinkingbox/blob/main/docs/writing_effective_tests.md)。是否由领域专家编写：无出处，待核。
- **验证与奖励**：任务特定可执行检查，接受任何有效轨迹，拒绝错误/缺失/多余副作用 [arXiv](https://arxiv.org/abs/2608.19741)；实现为与 golden 期望状态的确定性 hash 比对，30 题额外用 yes/no rubric LLM judge；**无 partial credit** [release README](https://github.com/microsoft/thinkingbox-data/blob/main/releases/thinkingbox_bench_v1/README.md)。框架另有 Rubric Judge（正向权重 + 扣分 + 乘性惩罚，reward∈[0,1] 与阈值比较）用于训练 [rubrics_judge.md](https://github.com/microsoft/thinkingbox/blob/main/docs/rubrics_judge.md)。
- **数据准备**：框架定位之一就是生成离线训练对话并把整个系统放进 RL 环路；thinkingbox-training 支持 GRPO、LoRA、多轮 MCP rollout [README](https://github.com/microsoft/thinkingbox/blob/main/README.md)。但 Bench v1.0 明确**仅限评测**，禁止用于 prompt 优化/微调/RL/奖励模型 [release README](https://github.com/microsoft/thinkingbox-data/blob/main/releases/thinkingbox_bench_v1/README.md)。
- **规模与开放**：507 tasks，GitHub tag 为可执行源，HF 为 viewer [release README](https://github.com/microsoft/thinkingbox-data/blob/main/releases/thinkingbox_bench_v1/README.md)。
- **关键结果**：最强模型 pass@1 65.36%，但 pass^20 仅 25.25%；很多失败 trial 正常终止且有合法状态变更动作 → response/tool-call 级信号不是端到端完成的好代理 [arXiv](https://arxiv.org/abs/2608.19741)。
- **局限与红旗**：后端为 mock（非真实保险/银行系统），专业深度主要体现在 policy 文本；与 τ-bench 范式高度相似（推断）。
- **可复用配方**：
  1. MCP server 约定 `init`/`geteffects` 两个保留接口，使任意 mock 后端可重置且可审计副作用 [README](https://github.com/microsoft/thinkingbox/blob/main/README.md)。
  2. 用 pass^k（k=20）报告可靠性而非 pass@1 [arXiv](https://arxiv.org/abs/2608.19741)。
  3. 断言写在 effects 上、不写在调用序列上 [writing_effective_tests.md](https://github.com/microsoft/thinkingbox/blob/main/docs/writing_effective_tests.md)。
- **评级：值得浏览**

### 2.8 Business Arena — 基于真实 Alibaba.com 供给数据的跨境 B2B 经营模拟器
arXiv [2608.08621](https://arxiv.org/abs/2608.08621) · 2026-08-11 · Accio Team, Alibaba Group（+Yale）· HF 20↑ · 仓库 [Accio-org/BusinessArena](https://github.com/Accio-org/BusinessArena/blob/main/README.md)（**仅 README + 论文 PDF，无环境代码**）· 证据深度：摘要 + 论文 PDF 全文（[paper/business-arena.pdf](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)）

- **领域与任务类型**：agent 独立经营跨境 B2B 店铺：市场调研、采购、库存、定价、广告、客服谈判、合规、财务；预开业阶段 + 30 个模拟营业日，agent 调 `end_round` 推进一天 [论文 PDF App. A](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)、[README](https://github.com/Accio-org/BusinessArena/blob/main/README.md)。
- **环境形态**：**simulator grounded in real data**：产品、供应商报价、价格、MOQ、交期来自真实 Alibaba.com listing；965 个可交易报价 / 831 个脱敏供应商 / 135 SKU，敏感身份与标题被 mask 或改写 [论文 PDF §1, App. B](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)。关税基于 World Bank WITS，关税冲击按中美贸易摩擦历史校准；季节需求按美国 Census MRTS（经 FRED）、Eurostat、中国国家统计局零售数据校准 [论文 PDF App. C](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)。60+ 工具，MCP typed call 与可脚本化接口共享同一市场机制 [论文 PDF §1, App. A](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)。NPC 竞争者每日执行确定性行为循环 [论文 PDF](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)。
  - 不可逆动作：合规缺失时交易产生递增罚款（$500、$1,000、$1,500、$2,000…）[论文 PDF App. E](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)——即用"模拟中的罚款"代替真实世界不可逆后果。
  - 隔离：每次评测在全新隔离 sandbox 中运行 OpenClaw runtime；agent 以非特权用户运行，arena 服务的源码/数据库/隐藏状态通过文件权限保护 [论文 PDF §5, App. A](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)。
- **任务来源**：单一长程任务（经营一家店）；"专家知识"体现在 **human/expert-designed reference strategies**：只用公开接口、无 oracle 信息的分层决策控制器，用来估计可得机会上限 [论文 PDF App. J](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)、[README](https://github.com/Accio-org/BusinessArena/blob/main/README.md)。
- **验证与奖励**：最终 net worth（利润）作主指标；skill-level 经济指标（资本部署、毛利、客服、合规等）；把已实现盈亏追溯到产生它们的动作（action-level attribution）；用 mechanism ablations 证明高分不是"忽略机制/模拟器捷径"所致 [arXiv](https://arxiv.org/abs/2608.08621)、[论文 PDF](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)。
- **数据准备**：无训练数据；论文提出 action-level attribution 可用于更细粒度的 credit assignment [论文 PDF §1](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)。
- **规模与开放**：15 个模型 × 每模型 10 次同种子 episode，共 150 runs [README](https://github.com/Accio-org/BusinessArena/blob/main/README.md)、[论文 PDF App. H](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)；**环境未开源**，作者"按需代测" [README](https://github.com/Accio-org/BusinessArena/blob/main/README.md)。
- **关键结果**：平均最终资产差 9 倍（$20,856 – $188,488），Gemini 3.1 Pro 第一（$188,488）[README](https://github.com/Accio-org/BusinessArena/blob/main/README.md)、[arXiv](https://arxiv.org/abs/2608.08621)；最好的模型仍落后于人类设计策略 [arXiv](https://arxiv.org/abs/2608.08621)；MiniMax M2.5 平均 22.7 次违规、$51,750 罚款 [论文 PDF](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)。
- **局限与红旗**：不开源→不可复现；单一世界种子（10 次运行同 seed，部分 ablation 用 10 seeds）[论文 PDF App. H](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)；需求/买家是模拟的，真实性取决于校准。
- **可复用配方**：
  1. 真实平台 listing（脱敏）+ 官方宏观统计校准需求/关税 → "grounded simulator" [论文 PDF App. B–C](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)。
  2. 用无 oracle 的人类规则策略作 headroom 参照，用机制消融排除模拟器捷径 [论文 PDF App. J](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)。
  3. agent 与环境服务分属不同系统身份，文件权限隔离隐藏状态 [论文 PDF App. A](https://github.com/Accio-org/BusinessArena/blob/main/paper/business-arena.pdf)。
- **评级：值得浏览**（设计思路好，但未开源）

### 2.9 ScienceIDE — 把科学计算代码库变成可训练环境（数值物理用例作 verifier）
arXiv [2609.19134](https://arxiv.org/abs/2609.19134) · 2026-09-17 · PhAI Labs / AItonomy · HF 71↑（README 称 HF Daily Papers #1）· 代码 [aitofound/ScienceIDE](https://github.com/aitofound/ScienceIDE) · 证据深度：摘要 + README + hard85 任务文件 + SFT/RL README

- **领域与任务类型**：天体 MHD（Athena++）、海洋/大气/海冰/生物地球化学（MITgcm）、等离子体（Gkeyll）、材料描述符（DScribe）、量子电路（Stim）等科学代码；任务为 **Repair**（注入语义缺陷后修复）与 **Implementation**（挖掉函数体后重实现）[README](https://github.com/aitofound/ScienceIDE/blob/main/README.md)。
- **环境形态**：**真实科学软件（未修改的上游代码，钉死 commit）**容器化为 Harbor episode；verifier 重新编译、重跑物理用例并与参考输出逐点比较 [README](https://github.com/aitofound/ScienceIDE/blob/main/README.md)。例：MITgcm checkpoint69q，钉 upstream commit 与源码包 sha256 [task.toml](https://github.com/aitofound/ScienceIDE/blob/main/hard85/mitgcm-atmos/mitgcm-atmos-repair-sem-data-aim-convection-qbl/task.toml)；verifier 在 separate 环境里独立构建未修改源码 [instruction.md](https://github.com/aitofound/ScienceIDE/blob/main/hard85/mitgcm-atmos/mitgcm-atmos-repair-sem-data-aim-convection-qbl/instruction.md)、[task.toml](https://github.com/aitofound/ScienceIDE/blob/main/hard85/mitgcm-atmos/mitgcm-atmos-repair-sem-data-aim-convection-qbl/task.toml)。agent 网络仅允许模型 API 主机 [task.toml](https://github.com/aitofound/ScienceIDE/blob/main/hard85/mitgcm-atmos/mitgcm-atmos-repair-sem-data-aim-convection-qbl/task.toml)；agent 镜像中不含参考输出或原始源码 [instruction.md](https://github.com/aitofound/ScienceIDE/blob/main/hard85/mitgcm-atmos/mitgcm-atmos-repair-sem-data-aim-convection-qbl/instruction.md)。资源：4 CPU / 8 GB，agent 超时 3,600 s [task.toml](https://github.com/aitofound/ScienceIDE/blob/main/hard85/mitgcm-atmos/mitgcm-atmos-repair-sem-data-aim-convection-qbl/task.toml)。
- **任务来源**：摘要称由**专家定义的科学 case 与 acceptance criteria** 引导 agent 把仓库转成可执行环境 [arXiv](https://arxiv.org/abs/2609.19134)。具体 task 由"repair-factory"程序化注入缺陷：provenance 记录 break/fix 编辑（如把 `QBL = 15.` 改成 `14.`）、缺陷族、预测难度与理由 [provenance.json](https://github.com/aitofound/ScienceIDE/blob/main/hard85/mitgcm-atmos/mitgcm-atmos-repair-sem-data-aim-convection-qbl/authoring/provenance.json)；derived_from "ScienceAccelBench ... official checks; native repair-factory calibration" [task.toml](https://github.com/aitofound/ScienceIDE/blob/main/hard85/mitgcm-atmos/mitgcm-atmos-repair-sem-data-aim-convection-qbl/task.toml)。难度用实测属性（未修复得分、编辑位置数、验证成本、实测通过率）而非人工标签 [README](https://github.com/aitofound/ScienceIDE/blob/main/README.md)。含 canary GUID 便于检测训练污染 [instruction.md](https://github.com/aitofound/ScienceIDE/blob/main/hard85/mitgcm-atmos/mitgcm-atmos-repair-sem-data-aim-convection-qbl/instruction.md)。
- **验证与奖励**：reward = 物理用例平均分；`reward_repair = max(0,(reward−floor)/(1−floor))`，floor 为未修复版本得分 → 不动仓库恰好 0 分；每个发布任务都经执行验证：官方 fix 得 1.0、未修复版本留有信号空间、agent 镜像无答案材料 [README](https://github.com/aitofound/ScienceIDE/blob/main/README.md)。按数值正确性而非 diff 匹配评分，作者称难以 game [README](https://github.com/aitofound/ScienceIDE/blob/main/README.md)。
- **数据准备**：SFT 用经 verifier 过滤的工具轨迹（LoRA，ms-swift），超长样本默认报错、只能显式整条丢弃并审计 [SFT/README.md](https://github.com/aitofound/ScienceIDE/blob/main/SFT/README.md)；RL 在 PSRL（改版 veRL）上做 async GRPO，可选丢弃零方差组、DAPO overlong filtering [RL/README.md](https://github.com/aitofound/ScienceIDE/blob/main/RL/README.md)。
- **规模与开放**：64 个环境中公开 15 个、49 个留作测试集；ScienceIDE-Hard 85 题中公开 30 题 [README](https://github.com/aitofound/ScienceIDE/blob/main/README.md)；完整 task-authoring pipeline 将在 Gen-Verse/ScienceInfra 发布（尚未）[README](https://github.com/aitofound/ScienceIDE/blob/main/README.md)。模型 PhAI-IDE-4B/9B/72B 已发布 [README](https://github.com/aitofound/ScienceIDE/blob/main/README.md)。
- **关键结果**：RL（Qwen3.5-4B，30 步）LAPS 0.357→0.857、MITgcm-biogeo 0.286→0.571；SFT PhAI-IDE-9B 在 BBH Word Sorting 27.20→63.20；作者也报告 9B 在 HumanEvalFix Python 上下降 [README](https://github.com/aitofound/ScienceIDE/blob/main/README.md)。
- **局限与红旗**：任务是"注入缺陷修复"，与真实科学工作（建模、参数研究）距离较远；held-out 环境与任务生成管线未公开；"专家定义 case" 的具体人工量未在仓库体现（无出处，待核）。
- **可复用配方**：
  1. 以"上游代码自带的回归/物理用例"作 verifier，reward 用 floor 归一化 [README](https://github.com/aitofound/ScienceIDE/blob/main/README.md)。
  2. 缺陷注入 + 精确逆修复 + 实测难度 + canary GUID 的 task 卡结构 [provenance.json](https://github.com/aitofound/ScienceIDE/blob/main/hard85/mitgcm-atmos/mitgcm-atmos-repair-sem-data-aim-convection-qbl/authoring/provenance.json)、[task.toml](https://github.com/aitofound/ScienceIDE/blob/main/hard85/mitgcm-atmos/mitgcm-atmos-repair-sem-data-aim-convection-qbl/task.toml)。
  3. verifier 在独立环境中从钉死源码重建参考结果 [task.toml](https://github.com/aitofound/ScienceIDE/blob/main/hard85/mitgcm-atmos/mitgcm-atmos-repair-sem-data-aim-convection-qbl/task.toml)。
- **评级：必读**（科学软件 → RL 环境的最完整开源配方）

### 2.10 SWE-bench Science — 98 个真实科学计算仓库上的仓库级修复/工程任务
arXiv [2608.19799](https://arxiv.org/abs/2608.19799) · 2026-08-21 · OpenMOSS · HF 61↑ · 代码 [OpenMOSS/SWE-bench-Science](https://github.com/OpenMOSS/SWE-bench-Science) · 证据深度：摘要 + README + docs（architecture / dataset-contract / 许可审计）+ tasks.csv

- **领域与任务类型**：119 tasks / 98 GitHub 仓库 / 20 个科学领域；三种范式：Issue-driven、Expert-exploratory、Engineering-integration [arXiv](https://arxiv.org/abs/2608.19799)。细分领域标签例：计算反应化学、DFT、天文光谱、ATAC-seq HMM、CALPHAD、电池建模 [statistics.md](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/huggingface/data/statistics.md)。强调"科学契约"：单位、坐标系、数值不变量、文件格式语义、物理假设 [README](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/README.md)。
- **环境形态**：真实科学仓库 + 固定 base commit；每题一个 environment 镜像 + 一个 verifier 镜像，Docker Hub 按 digest 钉死；verifier 把补丁应用到干净 baseline、重新构建后运行 held-out 测试；agent 仅连内部网络、推理经 allowlist 代理，verifier 无网络 [README](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/README.md)。harness（Codex/Claude Code/mini-swe-agent）由 Pier 运行时安装 [README](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/README.md)。
- **任务来源**：Issue-driven 来自真实 issue；Expert-exploratory 暗示由专家探索设计 [arXiv](https://arxiv.org/abs/2608.19799)（专家人数/流程：无出处，待核）。91 题标记可做 science-knowledge 消融 [statistics.md](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/huggingface/data/statistics.md)。
  - **许可/版权治理（亮点）**：每行记录 source_license、material_licenses、license_gate（none/gpl-family/noncommercial/restricted-materials）[dataset-contract.md](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/docs/dataset-contract.md)；默认 96 题无限制，23 题需显式 `--allow-restricted-licenses`（18 道 GPL 家族）[statistics.md](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/huggingface/data/statistics.md)；对随题打包的论文/图表逐题做再分发审计，规则如"DOI/arXiv/open access 标签本身不是再分发许可"，结论分 PASS / FIX NOTICE / BLOCK [paper_material_audit_046_060.md](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/docs/paper_material_audit_046_060.md)。
- **验证与奖励**：programmatic held-out tests，pass@1 [README](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/README.md)、[arXiv](https://arxiv.org/abs/2608.19799)。公开发布不含参考补丁、私有 verifier 测试、凭据与轨迹 [README](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/README.md)。
- **数据准备**：无训练数据。
- **规模与开放**：119 tasks，MIT；镜像与 HF 数据公开 [README](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/README.md)。
- **关键结果**：最好的 agent（Claude Code + Opus-5 max）pass@1 < 50%；四类失败机制；去掉显式科学指导的配对消融显示科学知识并非一致有益——对齐良好的信息可约束修复、提升平均表现与 token 效率，对齐差的指导会诱发 anchoring [arXiv](https://arxiv.org/abs/2608.19799)。
- **局限与红旗**：verifier 镜像在 Docker Hub 公开，held-out 测试理论上可被提取（推断）；每个领域题量很少（多数为 1 题）[statistics.md](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/huggingface/data/statistics.md)，领域结论统计力弱。
- **可复用配方**：
  1. environment / verifier 双镜像分离 + digest 钉死 + verifier 断网 [README](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/README.md)。
  2. 数据卡中把源码许可与附带材料许可分开记录，并以 license gate 控制默认选择 [dataset-contract.md](https://github.com/OpenMOSS/SWE-bench-Science/blob/main/docs/dataset-contract.md)。
  3. 用"有/无科学知识提示"的配对消融测量领域知识对 agent 的真实贡献 [arXiv](https://arxiv.org/abs/2608.19799)。
- **评级：值得浏览**

### 2.11 CASE — UK Biobank 纵向多模态"自己找证据"的临床 agent 环境 + agentic 后训练
arXiv [2609.39566](https://arxiv.org/abs/2609.39566) · 2026-10-12 · 作者 Minye Shao、Chaohui Yu、Fan Wang、Ling Shao、Yang Long 等（README 注释中的作者列表，[README](https://github.com/VinyehShaw/CASE/blob/main/README.md)）· HF 12↑ · 代码 [VinyehShaw/CASE](https://github.com/VinyehShaw/CASE) · 证据深度：摘要 + README + reward/mock tool 代码

- **领域与任务类型**：纵向临床推理：50,401 道多选题，源自 4,739 名参与者的 ICD-10 编码诊断；每题链接到一个患者专属环境（临床上下文 + 基线/随访多序列 MRI），agent 自主选择看哪次随访、器官、模态、切片、专科工具 [arXiv](https://arxiv.org/abs/2609.39566)。10 个 strata / 6 个临床领域；随访中位间隔 2.26 年，5 个器官区域、7 种子模态 [README](https://github.com/VinyehShaw/CASE/blob/main/README.md)。三种角色：Anatomist（Vista3D 分割/体积变化）、Radiologist（跨随访 MRI 对比）、Consultant（10 种工具含 MedGemma 报告与 skill memory），各有调用预算 [README](https://github.com/VinyehShaw/CASE/blob/main/README.md)。
- **环境形态**：**真实临床数据（UK Biobank）+ 真实医学影像工具**（Vista3D 分割、MedGemma-27B 报告）用于评测；**RL 训练时用 mock 工具回放离线预计算结果**（按 patient_id/tool/organ 键控的缓存）以降成本 [README](https://github.com/VinyehShaw/CASE/blob/main/README.md)、[anatomist_mock_tool.py](https://github.com/VinyehShaw/CASE/blob/main/distill/tool/anatomist/anatomist_mock_tool.py) → "评测用真工具、训练用回放"是值得注意的成本折中。所有结果在 8×H100 上产出 [README](https://github.com/VinyehShaw/CASE/blob/main/README.md)。
- **任务来源**：从真实 ICD-10 医生诊断派生（摘要）[arXiv](https://arxiv.org/abs/2609.39566)；题目生成方式（模板/LLM）需读正文（无出处，待核）。
  - **隐私/许可**：依 UK Biobank Application 603483 条款，仅公开脱敏轨迹与少量展示图；完整 benchmark 与派生数据须"返还"UK Biobank（AMS 平台），经批准的研究者才能访问；不得在批准项目外再分发 [README](https://github.com/VinyehShaw/CASE/blob/main/README.md)。
- **验证与奖励**：评测指标为首次作答 exact answer-set 准确率（Micro/Macro over 10 strata）[README](https://github.com/VinyehShaw/CASE/blob/main/README.md)。RL 奖励 = sparse 正确性（对 +1 / 错 −1 / 无法解析 −2）+ α·dense LLM rubric 质量分（默认 α=0.5）[reward.py](https://github.com/VinyehShaw/CASE/blob/main/distill/opd_rl/reward.py)；rubric judge 默认 Kimi K2.6 [README](https://github.com/VinyehShaw/CASE/blob/main/README.md)；另加 on-policy privileged self-distillation（OPSD，对 Phase-4 insight 的 causal-KL）[README](https://github.com/VinyehShaw/CASE/blob/main/README.md)、[arXiv](https://arxiv.org/abs/2609.39566)。
- **数据准备**：teacher（Qwen3.8-Max）在同一工具环境中录制的 147,434 条角色条件轨迹 [README](https://github.com/VinyehShaw/CASE/blob/main/README.md)（摘要写 SFT 用 14,734 条 frontier-model 轨迹 [arXiv](https://arxiv.org/abs/2609.39566)，两数字关系待核）；RSFT 过滤：至少一次工具调用、可解析 Phase-4 insight、Kimi K2.6 evidence-linkage rubric 分 ≥0.4 [README](https://github.com/VinyehShaw/CASE/blob/main/README.md)。患者级 md5 稳定划分 40/50/10（RSFT/RL/test）[README](https://github.com/VinyehShaw/CASE/blob/main/README.md)。
- **规模与开放**：测试集 4,850 题 / 455 名参与者（3 角色共 14,135 次评测）[README](https://github.com/VinyehShaw/CASE/blob/main/README.md)；代码与 CASE-8B 权重公开，数据需 UK Biobank 授权 [README](https://github.com/VinyehShaw/CASE/blob/main/README.md)。
- **关键结果**：基于 Qwen3-VL-8B 的 agent 在匹配评测条件下取得 >16% 与 >10% 的相对提升（摘要截断，比较对象未见）[arXiv](https://arxiv.org/abs/2609.39566)。
- **局限与红旗**：多选题形式 → 终答可猜；rubric judge 与 teacher 都是 LLM，"专家"参与度不明；数据不可公开复现。
- **可复用配方**：
  1. 受限医疗数据的"返还数据集"合规路径（公开脱敏轨迹 + 授权访问全集）[README](https://github.com/VinyehShaw/CASE/blob/main/README.md)。
  2. 训练期用缓存回放的 mock 工具，评测期用真实工具 [anatomist_mock_tool.py](https://github.com/VinyehShaw/CASE/blob/main/distill/tool/anatomist/anatomist_mock_tool.py)。
  3. sparse 正确性 + α·rubric dense reward 的组合 [reward.py](https://github.com/VinyehShaw/CASE/blob/main/distill/opd_rl/reward.py)。
- **评级：值得浏览**

### 2.12 GDPevo — 由 agent 全自动构建的企业工作流"自进化"benchmark（CRM/ERP/金融/医疗/法律/数据）
arXiv [2608.03764](https://arxiv.org/abs/2608.03764) · 2026-08-06 · Prism Shadow · HF 27↑ · 代码 [Prism-Shadow/GDPevo](https://github.com/Prism-Shadow/GDPevo) · 证据深度：摘要 + README + DATA_BOARD + 构建/评审 workspace 文档 + evaluator 抽样

- **领域与任务类型**：24 个 task group / 240 tasks：CRM、ERP（费用控制与结账、采购收货、库存、HR）、金融（私人财富税务与遗产规划、信贷委员会、机构投资）、医疗运营（入院转诊、医保预授权与申诉、EHR 质控、临床协议决策支持）、法律（白领调查文档审阅、法院书记员、许可合规、并购合同审阅）、数据分析 [DATA_BOARD.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data/DATA_BOARD.md)。每组共享一个业务环境、5 train + 5 held-out test [README](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md)。
- **环境形态**：**mock 企业系统**：每组一个 Docker 化服务（如 HarborCRM：`server.py` + `generate_data.py` 生成的 JSON 数据），`state_mode` 为 read_only 或 mutable [task_group.yaml](https://github.com/Prism-Shadow/GDPevo/blob/main/data/task_groups/task_group_001/task_group.yaml)；评审规范要求环境仅在编排器创建的 bridge 网络内以 `http://task-env:<port>/` 可达、不向 agent 挂载环境源码/数据库/真值/Docker socket；mutable 环境每次 attempt 一个干净实例；`/api/judge` 仅在 train 反馈阶段开启 [review_criteria.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_3_Quality_Filtering/review_workspace/guides/review_criteria.md)。
- **任务来源（合成 + 真实种子）**：以 GDPval、SOP-Bench 等"真实工作"来源为种子，再扩展成带相似记录、重复业务规则的共享环境 [data/README.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data/README.md)；三阶段 **agent 驱动的构建管线**：Stage 1 场景发现（从源 benchmark 检索归组）→ Stage 2 task factory（env-builder 与 task-builder 子 agent）→ Stage 3 质量过滤（脚本检查 + 6 个独立 reviewer agent 投票）[README](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md)。核心机制 rule hybridization：把工作流拆成原子业务规则，分散到 train 任务并在 test 中重组，使 test 增益可归因于训练经验 [arXiv](https://arxiv.org/abs/2608.03764)。全自动可在两天内从 V1 120 题扩到 V2 240 题以应对污染 [arXiv](https://arxiv.org/abs/2608.03764)。**专家参与：未见人工专家审核环节**（评审为 agent 投票）[review_criteria.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_3_Quality_Filtering/review_workspace/guides/review_criteria.md)。
- **验证与奖励**：确定性规则 grader（如对 answer.json 的标量字段相等、集合字段相等、金额四舍五入到 2 位）[evaluator.py](https://github.com/Prism-Shadow/GDPevo/blob/main/data/task_groups/task_group_006/train_tasks/001/eval/evaluator.py)；每题 rubric 6–10 项、权重 ∈{1,2,3}，每个得分点"全得或零分"，避免 free-text 匹配；脚本要求参考答案拿满分 [review_criteria.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_3_Quality_Filtering/review_workspace/guides/review_criteria.md)。
  - 难度校准：用 Docker 化 `codex exec` 做 base/fewshot 试跑，目标 base avg@3 ≈0.40–0.60、fewshot <0.80 且增益约 0.10–0.30 [review_criteria.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_3_Quality_Filtering/review_workspace/guides/review_criteria.md) → 难度按某个前沿 agent 校准，存在对该 agent 的选择偏差（推断）。
- **数据准备**：评测 4 种进化模式（base / self / fewshot / reflect-3）[README](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md)。
- **规模与开放**：240 tasks、环境、参考答案、evaluator、构建 workspace 全部公开 [README](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md)。
- **关键结果**：Claude Code + Opus 4.8 base 50.63% → fewshot 67.07%（+16.44 pp）；Codex + GPT-5.5 base 49.37% → fewshot 64.51%；self 模式增益仅 +2.59~+6.42 pp [README](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md)；oracle 上限 91.6% [arXiv](https://arxiv.org/abs/2608.03764)。
- **局限与红旗**：环境、任务、评审全由 agent 生成，领域正确性（如遗产规划、医保申诉规则）无人类专家背书；答案公开。
- **可复用配方**：
  1. "种子真实任务 → 共享 mock 环境 + 原子规则 → train/test 规则重组" 的可归因迁移设计 [arXiv](https://arxiv.org/abs/2608.03764)。
  2. agent 化的 builder / 多 reviewer 投票 / 脚本硬检查（参考答案满分、rubric 结构）的三层质检 [review_criteria.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_3_Quality_Filtering/review_workspace/guides/review_criteria.md)。
  3. 以目标 agent 通过率区间做难度校准 [review_criteria.md](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_3_Quality_Filtering/review_workspace/guides/review_criteria.md)。
- **评级：值得浏览**（任务合成管线可直接复用；专家性弱）

### 2.13 BI-Agent & BI-Bench — 从真实公开 BI 项目与用户看板中人工抽取的端到端 BI 问答
arXiv [2609.20886](https://arxiv.org/abs/2609.20886) · 2026-09-21 · Microsoft Research（作者 Chuxuan Hu、Yeye He、Daniel Kang、Surajit Chaudhuri 等，见 arXiv 元数据）· HF 14↑ · 代码 [Hu-Chuxuan/bi-agent](https://github.com/Hu-Chuxuan/bi-agent)（默认分支 `release`）· 证据深度：摘要 + README + 评测/数据生成代码抽样

- **领域与任务类型**：Power BI / Tableau 式 BI：找表、数据变换、建 join、回答业务问题，端到端 [arXiv](https://arxiv.org/abs/2609.20886)。每个 case = 多张 CSV + 关系文件 + 从用户看板抽出的自然语言问题；共 100 cases [README](https://github.com/Hu-Chuxuan/bi-agent/blob/release/README.md)；问题例 "What is the sum of unit price and sum of quantity for each order year?" [queries.json](https://github.com/Hu-Chuxuan/bi-agent/blob/release/bi-bench/queries.json)。
- **环境形态**：**真实数据（公开 BI 项目）+ Python/SQL 执行**，可选 transform/retrieve/join 工具套件 [README](https://github.com/Hu-Chuxuan/bi-agent/blob/release/README.md)。未使用真实 Power BI 软件本身。
- **任务来源**：从公开来源收集大量真实 BI 项目，**人工**从真实用户 dashboard 抽取（问题，真值答案）对 [arXiv](https://arxiv.org/abs/2609.20886) → "真实工件反推题目"，专家性来自原 dashboard 作者。
- **验证与奖励**：真值 CSV 比对；数值比较 `np.isclose(rtol=1e-2, atol=0.5)`，把两表展平后做贪心一一匹配 [tools/run_large_models.py](https://github.com/Hu-Chuxuan/bi-agent/blob/release/tools/run_large_models.py) → 表结构信息被丢弃、绝对容差 0.5 偏松（hackability/误判风险，本人阅读代码所得）。
- **数据准备（亮点）**：post-train 管线：从真实 BI case 采样（示例命令 10,000 个 case），用 o4-mini 按 transpose/pivot/unpivot/join 变换生成新问题，用 GPT-4o 跑 trace，只保留成功 trace 转 SFT/RFT 数据；RFT 用 GRPO + BI-Bench 式 reward [post-train/data_gen/README.md](https://github.com/Hu-Chuxuan/bi-agent/blob/release/post-train/data_gen/README.md)、[post-train/README.md](https://github.com/Hu-Chuxuan/bi-agent/blob/release/post-train/README.md)。源 BI case 原始数据不在仓库中 [post-train/data_gen/README.md](https://github.com/Hu-Chuxuan/bi-agent/blob/release/post-train/data_gen/README.md)。
- **规模与开放**：100 cases + gt 全部在仓库 [README](https://github.com/Hu-Chuxuan/bi-agent/blob/release/README.md)。
- **关键结果**：前沿 LLM 准确率 <50% [arXiv](https://arxiv.org/abs/2609.20886)；仓库表：o4-mini Python+tools 66.3%、GPT-5.5 Python+tools 65.4%；Qwen3-8B base 5.4–19.8% → SFT+RFT SQL+tools 35.0%；专用 NL2SQL 系统最高 26.3%（ktx）[README](https://github.com/Hu-Chuxuan/bi-agent/blob/release/README.md)。（注意摘要"<50%"应指无工具设置，与仓库带工具数字不矛盾。）
- **局限与红旗**：仅 100 题；比对函数宽松；真实 BI 项目的许可证/隐私处理未在 README 说明（无出处，待核）。
- **可复用配方**：
  1. 从公开 BI 项目的 dashboard 视觉元素反推问题 + 真值（真实工件 → QA）[arXiv](https://arxiv.org/abs/2609.20886)。
  2. 用 schema 变换（pivot/unpivot/transpose/join）对真实表做数据增广合成训练题 [post-train/data_gen/README.md](https://github.com/Hu-Chuxuan/bi-agent/blob/release/post-train/data_gen/README.md)。
- **评级：值得浏览**

### 2.14 SimuVerity — 工程级 Simulink 模型生成（原生仿真场景作工程验收）
arXiv [2610.02304](https://arxiv.org/abs/2610.02304) · 2026-10-05 · Xi'an Jiaotong University · HF 47↑ · 代码 [SimuVerity/SimuVerity](https://github.com/SimuVerity/SimuVerity) · 证据深度：摘要 + README + 任务包（public_spec / official_scenarios / scorer manifest）抽样

- **领域与任务类型**：101 个 text-to-executable Simulink 建模任务，10 个工程领域 [arXiv](https://arxiv.org/abs/2610.02304)：XELEC 9 / XAERO 10 / XAUTO 11 / XBATT 10 / XCOMM 9 / XFLUID 11 / XMECH 11 / XMED 9 / XROBO 10 / XTHERM 11 [benchmark README](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/README.md)。例：8 模组串联电池包 + 分布式热状态 + 主动液冷，指定参数名义值与运行范围、冷却故障注入 [XBATT-01 public_spec.json](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/tasks/XBATT-01/public_spec.json)。
- **环境形态**：**真实商业专业软件**：评测需 MATLAB R2025a + Simulink 及任务所需产品；agent 通过 MATLAB/Simulink 工具接口（MCP）生成 [benchmark README](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/README.md)。隔离：评测服务器上在 OS 层阻断 agent 进程与 MATLAB 会话的外网，删除 MATLAB 示例目录（防止直接拷贝官方 example）；评测时创建只读提交副本 + 独立可写运行副本 + 隔离的 MATLAB preferences/cache [benchmark README](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/README.md)。
- **任务来源**：参考系统 68 个随包发布、33 个由用户本地 MATLAB 公开示例导入；随包的 68 个中 10 个为 SimuVerity 原创"expert_built"模型，58 个为再分发的第三方项目与研究工件 [benchmark README](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/README.md)（本人对 task.json 计数亦为 expert_built 10 个）。每题配 executable-system profile 落地工程规格 [arXiv](https://arxiv.org/abs/2610.02304)。
- **验证与奖励**：分层 evaluator：先 gate（交付、原生可执行、工程合格 G），合格后在 6 个维度打分：accuracy、output quality、mechanistic fidelity、control & causal integrity、operating-domain robustness、dynamic response [arXiv](https://arxiv.org/abs/2610.02304)；每题有 evaluator 自有的 official scenarios（如 hot_high_current、cold_low_soc、故障/无故障配对场景）[XBATT-01 official_scenarios.json](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/tasks/XBATT-01/official_scenarios.json)；评测抽取 evidence bundle 后可离线 rescore，不再启动 MATLAB [benchmark README](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/README.md)。参考系统平均得分 96.01（评分器自洽性检查）[README](https://github.com/SimuVerity/SimuVerity/blob/main/README.md)。
- **数据准备**：无训练数据；公布 6 个 agent 系统 × 3 次运行的冻结结果与 10 题工具消融（Full MCP / No-Simulation MCP / Batch-only）[README](https://github.com/SimuVerity/SimuVerity/blob/main/README.md)。
- **规模与开放**：101 tasks、scorer、结果全部开源（Apache-2.0，第三方资产保留原许可）[README](https://github.com/SimuVerity/SimuVerity/blob/main/README.md)；但需 MATLAB 商业许可证才能评测。
- **关键结果**：最佳 Opus 4.8 + Claude Code 总分 42.86（G pass 76.90%），GPT-5.5 + Codex 41.72；GLM-5.3-Flash 4.98 [README](https://github.com/SimuVerity/SimuVerity/blob/main/README.md)；结构相似度不是工程性能的好代理，部分高分模型可视布局严重混乱 [arXiv](https://arxiv.org/abs/2610.02304)。
- **局限与红旗**：MATLAB 许可证门槛；58 个参考来自第三方再分发（任务可能被预训练见过）；system profile 公开（虽不发给 agent）[benchmark README](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/README.md)。
- **可复用配方**：
  1. "规格 + 评估方持有的多工况仿真场景（含故障配对）"作为工程验收，而非与参考模型做结构比较 [official_scenarios.json](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/tasks/XBATT-01/official_scenarios.json)。
  2. evidence bundle 解耦"重仿真"与"打分"，便于离线复核 [benchmark README](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/README.md)。
  3. 评测时删除软件自带示例目录，防止 agent 直接复制官方模型 [benchmark README](https://github.com/SimuVerity/SimuVerity/blob/main/SimuVerity-benchmark/README.md)。
- **评级：必读**（商业工程软件 + 物理仿真验收的范例）

### 2.15 CADWorld — FreeCAD 长程机械 CAD computer-use benchmark（1,300 人时人工构建）
arXiv [2609.16251](https://arxiv.org/abs/2609.16251) · 2026-09-21 · Georgia Tech / NCSU / NUS / Marquette（论文 PDF 署名，[CADWORLD.pdf](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)）· HF 5↑ · 代码 [Zdong104/CADWORLD](https://github.com/Zdong104/CADWORLD)（经 WebSearch 找到：[aiweekly 二手摘要](https://aiweekly.co/alerts/cadworld-benchmark-top-agent-175-on-freecad-vs-experts-87)、[HF VM image 页](https://huggingface.co/Zihan1004/CADWorld)（二手））· 证据深度：摘要 + README + 仓库内论文 PDF

- **领域与任务类型**：200 tasks，11 个机械 CAD 工作流类别：草图、零件建模、装配、CAM、FEM、材质外观、点云转换、宏、测量、网格转换、工程图（TechDraw）[arXiv](https://arxiv.org/abs/2609.16251)、[CADWORLD.pdf §3.3](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)。前 190 题为常规覆盖集，另加 10 道刻意简短的诊断题 [CADWORLD.pdf §3.3](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)。
- **环境形态**：**真实开源专业软件**：FreeCAD 1.1 运行在预构建 Ubuntu VM（Docker/QEMU，默认 64G 盘/8G 内存/8 核），agent 通过截图 + pyautogui 交互；VM 镜像约 35 GB [README](https://github.com/Zdong104/CADWORLD/blob/main/README.md)。任务可从空白文档或上传的 precondition 文件开始，常附指令图片 [CADWORLD.pdf §3.3](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)。评测在宿主机侧：从 VM 拉取 .FCStd 解析；15 道 CAM 任务需宿主机 FreeCADCmd 做 OpenCascade 布尔比较 [README](https://github.com/Zdong104/CADWORLD/blob/main/README.md)。选 FreeCAD 是为了开放、可复现、可宏化 [CADWORLD.pdf §Limitations](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)。
- **任务来源**：从 FreeCAD workbench 能力、CAD 教程与文档、常见机械设计流程及构建中发现的覆盖缺口收集与编写；标注与验证约 3 个月、约 **1,300 人时**（任务编写、precondition 制作、evaluator 设计、反复人工检查）[CADWORLD.pdf §3.3](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)。人类专家参考轨迹用 CUA Collector 录制，是"一次专家参考通过"而非人群研究 [CADWORLD.pdf §4](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)。
- **验证与奖励**：task-specific 可执行检查覆盖几何属性、参数化结构、约束、制造状态、仿真结果 [arXiv](https://arxiv.org/abs/2609.16251)：零件看包围盒/体积/表面积；装配看 joint 元数据；CAM 比较毛坯到目标的去除量与过切/欠切比；FEM 要求分析对象、材料、边界条件、网格、求解器、结果与导出 CSV 数值；**binary，全部检查通过才成功，无 partial credit**，但保留缺失对象/属性不符/超容差等诊断 [CADWORLD.pdf §3.4](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)。仓库提供无 LLM 的分阶段失败归因（如 `geometry_close_but_out_of_tolerance`、`shape_correct_process_wrong`）[README](https://github.com/Zdong104/CADWORLD/blob/main/README.md)。
- **数据准备**：无训练数据；轨迹与 .FCStd 可离线重评 [README](https://github.com/Zdong104/CADWORLD/blob/main/README.md)。
- **规模与开放**：200 tasks、evaluator、baseline、VM 镜像均公开 [README](https://github.com/Zdong104/CADWORLD/blob/main/README.md)。
- **关键结果**：arXiv 摘要：全量 200 题上最强 agent 17.5% vs 专家参考 87.0% [arXiv](https://arxiv.org/abs/2609.16251)；仓库 PDF 版本：60 题覆盖子集上最强 25.0% vs 87.0% [CADWORLD.pdf](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)（两版本设置不同）。420 条模型-任务记录中 66.0% 达到 ≥100 GUI 步，失败记录中 72.7% 用满步数预算，成功记录无一达到 [CADWORLD.pdf §5](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)；人类示范平均 14.6 步 [CADWORLD.pdf](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)。
- **局限与红旗**：任务给出明确目标与所需素材，不测需求澄清/设计取舍；仅 FreeCAD；专家参考仅一次通过 [CADWORLD.pdf §Limitations](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)。PDF 页眉称 "Published as a conference paper at ICLR 2026"（可能仅为模板，待核）[CADWORLD.pdf](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)。
- **可复用配方**：
  1. 以 precondition 文件 + 指令图片构造"中途接手"型 CAD 任务 [CADWORLD.pdf §3.3](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)。
  2. judge-free 的分阶段失败归因（完成→保存→结构→几何→构造过程）[README](https://github.com/Zdong104/CADWORLD/blob/main/README.md)。
  3. 公开报告人工成本（~1,300 人时 / 200 题）可作预算参照 [CADWORLD.pdf §3.3](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)。
- **评级：必读**

### 2.16 NeutronGym — 中子散射仪器设计环境（McStas 射线追踪作物理 verifier，无 LLM judge，可 RL）
arXiv [2610.03631](https://arxiv.org/abs/2610.03631) · 2026-10-02 · 作者 Lijie Ding、Changwoo Do（机构未在数据中给出；无出处，待核）· 无 HF 声誉信号 · 代码：未找到（一次 WebSearch 无结果，[检索结果页之一：McStas 官网](https://mcstas.org/about/about.pure.html)（二手））· 证据深度：**仅摘要**

- **领域与任务类型**：中子散射仪器设计——agent 设定仪器布局的设计参数 [arXiv](https://arxiv.org/abs/2610.03631)。
- **环境形态**：**专业科学模拟器**：agent 通过带校验的工具搭建仪器，McStas 对其进行 ray-trace [arXiv](https://arxiv.org/abs/2610.03631)（McStas 为开源中子 Monte Carlo 模拟器，GPL，[Wikipedia](https://en.wikipedia.org/wiki/McStas)（二手））。"真实仪器的数字替身"：不触碰实体设备，故无物理安全问题。
- **任务来源**：两部分：procedural families 生成无限实例（固定布局、待定参数，含 held-out 参数区间）；McStasBench 为来自**已发表仪器**的 16 道精选任务，配 memorization probes 与 sandbox [arXiv](https://arxiv.org/abs/2610.03631)。
- **验证与奖励**：分层 ladder 依次评 syntax、runtime、structure、science，**无 LLM judge**；ladder 提供 partial credit [arXiv](https://arxiv.org/abs/2610.03631)。
- **数据准备**：RL 直接用环境 reward 训练 [arXiv](https://arxiv.org/abs/2610.03631)。
- **关键结果**：7 个模型在 McStasBench 16 题中最多复现 7 题，无一检索到参考、无一达到改进目标；RL 把 Qwen3-8B 在某 family（目标来自隐藏设计）held-out 实例上从 11% 提到 77%（第二个 seed 69%），超过未训练的 Qwen3-32B；另 3 个 gated family 各 1 个 seed 复现；**去掉 ladder 的 partial credit，增益塌缩 60 个点**；仅凭 reward 训练的模型在给定闭式物理时与经典优化器同预算相当（77% vs 81%），前沿模型解决 98–99% [arXiv](https://arxiv.org/abs/2610.03631)。
- **局限与红旗**：仅摘要证据；代码未找到；部分结论单 seed [arXiv](https://arxiv.org/abs/2610.03631)。
- **可复用配方**：
  1. 用领域权威模拟器作 verifier + 分层 partial-credit ladder（语法→可运行→结构→科学）[arXiv](https://arxiv.org/abs/2610.03631)。
  2. procedural family + held-out 参数区间做无限训练实例；"已发表仪器"做真实感测试切片并加 memorization probe [arXiv](https://arxiv.org/abs/2610.03631)。
- **评级：值得浏览**（对"simulator-as-verifier 能否训练出物理能力"给出了少见的消融证据，但缺代码）

### 2.17 FrontierFinance — 220 个专家编写的投研查询 + 11,543 条来源可追溯 rubric
arXiv [2608.11683](https://arxiv.org/abs/2608.11683) · 2026-08-12 · Samaya（据 [Samaya 博客](https://samaya.ai/blog/frontier-finance)（二手））· 无 HF 声誉信号 · 代码：作者称数据与评分代码公开 [arXiv](https://arxiv.org/abs/2608.11683)，仓库 URL 未检得 · 证据深度：摘要 + 一次 WebSearch（二手）

- **领域与任务类型**：覆盖完整投资者工作流的 6 类用例 [arXiv](https://arxiv.org/abs/2608.11683)；Samaya 页面列为财务数据与建模、行业/宏观、财报与事件、公司研究、覆盖与催化剂监控、筛选与发现 [research.samaya.ai](https://research.samaya.ai/benchmarks/frontier-finance)（二手）。
- **环境形态**：通用 tool harness，限制为**仅公开数据** [arXiv](https://arxiv.org/abs/2608.11683)；非专业终端（如 Bloomberg）。
- **任务来源**：220 个 expert-crafted queries [arXiv](https://arxiv.org/abs/2608.11683)。
- **验证与奖励**：11,543 条 source-attributed rubrics（针对长答案，作者认为 reference-based 指标与通用 LLM judge 不足）[arXiv](https://arxiv.org/abs/2608.11683)；rubric 项分 must-have / informational [Samaya 博客](https://samaya.ai/blog/frontier-finance)（二手）。
- **关键结果**：Samaya 自家系统 56.0%，最强前沿模型 Claude Fable 5 49.2%（成本约高 2.2×）；最佳开源 Kimi K3 46.4%（成本低 4.5×）；Screening & Discovery 与 Sector/Industry/Macro 最难（最好仅 33% / 39%）；harness 而非模型本身强烈影响质量与效率 [arXiv](https://arxiv.org/abs/2608.11683)。Samaya 博客给出的自家分数为 50.8%，与摘要不一致 [Samaya 博客](https://samaya.ai/blog/frontier-finance)（二手）。
- **局限与红旗**：作者方系统登顶（利益相关）；有评论指出单次随机运行无误差棒、agent 可用 2026 年网页回答较早日期问题造成 hindsight [Substack 评论](https://theagenticanalyst.substack.com/p/finance-ai-benchmarks-are-misleading)（二手）。
- **可复用配方**：每题数十条带来源归属的 rubric 项，区分 must-have 与 informational [arXiv](https://arxiv.org/abs/2608.11683)、[Samaya 博客](https://samaya.ai/blog/frontier-finance)（二手）。
- **评级：值得浏览**

### 2.18 TerminalHorizon（Scaling Agentic Data for Long-Horizon Terminal Intelligence）— 从真实专业工作合成长程终端任务环境
arXiv [2610.13166](https://arxiv.org/abs/2610.13166) · 2026-10-13 · alibaba · HF 136↑ · 项目页仓库 [zs1314/TerminalHorizon](https://github.com/zs1314/TerminalHorizon)（仅 GitHub Pages 站点源码，无引擎代码）· 证据深度：摘要 + 项目页数据文件

- **领域与任务类型**：终端 agent 的长程专业任务；项目页列出 25 个专业领域，含金融会计经济、生命科学医学健康、化学材料分子模拟、物理天文与仪器、机械热力航空、芯片电子嵌入式等 [data.js](https://github.com/zs1314/TerminalHorizon/blob/main/data.js)。
- **环境形态**：合成的终端任务环境（容器）[arXiv](https://arxiv.org/abs/2610.13166)；非真实 GUI 专业软件。
- **任务来源（亮点）**：从真实专业工作出发；指出环境合成常"预先完成或简化关键工作"从而去掉了本应由 agent 完成的探索/实现/验证；用**独立执行**识别构建中被省略的关键工作，并据此重建环境；再在同一目标下渐进扩展任务，引入依赖前序结果的新需求 [arXiv](https://arxiv.org/abs/2610.13166)。行为模式分类为 Explore / Diagnose / Build / Verify / Coordinate [data.js](https://github.com/zs1314/TerminalHorizon/blob/main/data.js)。
- **验证与奖励**：未在可达材料中说明（无出处，待核）。
- **数据准备**：构建 1.5K 任务环境，对 Qwen3.5-27B 做 SFT 得 TerminalHorizon-27B [arXiv](https://arxiv.org/abs/2610.13166)；项目页列出 Terminal-Bench 1.0/2.0/2.1、VitaBench 为评测基准 [data.js](https://github.com/zs1314/TerminalHorizon/blob/main/data.js)（具体分数未见）。
- **局限与红旗**：引擎未开源；专业领域覆盖靠合成，缺专家验证证据。
- **可复用配方**：用独立 agent 执行来审计"合成环境是否把关键工作预先做掉了"，再据证据重建环境 [arXiv](https://arxiv.org/abs/2610.13166)。
- **评级：值得浏览**（数据准备视角）

