# CUA / BUA / Agentic Search 论文深读笔记（2026-09-14 → 2026-10-14）

> 输入：A_cua_bua_search.json（24 篇）。所有数字均为作者自报（author-reported），除非另行说明。来源标签说明：`repo-pdf-fulltext` = 从 repo 中的论文 PDF 读取；`repo-readme` = 读取 repo README / docs / 模型卡；`abstract-only` = 仅有 arXiv 摘要（数据文件中的 excerpt 有截断）；`+search` = 额外做了一次 web search。
> 环境限制：arXiv / HF / github.io 均不可达；24 篇中 **没有一篇** 的 repo 里有真正的论文全文 PDF（EvoSkill-GUI 的 `docs/static/paper.pdf` 实为 ACL LaTeX 模板占位符），AREX-2 repo 有一份 Research Overview PDF。因此多数条目为 `repo-readme` 深度。

## 必读 Top-8（面向构建 BUA/CUA agent 与 agentic-RL 环境的读者）

1. **RecreationWorld**（Qwen，2609.22000）—— 把"运行中的参考软件"当 oracle 生成可执行奖励，五平台 hybrid CUA 环境 + 250 题 benchmark，环境构建范式可直接迁移。
2. **HybridCUA**（ZJU，2609.38008）—— GUI+CLI 统一 `bash` 动作空间 + CLI-aware RL 奖励，9B 模型 OSWorld 53.6%、14 步；数据、环境服务、异步 RL 基建全开源。
3. **SoftwareGym**（SJTU，2610.12611）—— LLM 自动合成 182 个原生桌面应用并用真实 GUI agent 测试-修复，OSWorld Pass@3 41.39%→56.97%（注意 Pass@3 口径）。
4. **Context Language Models**（Meta/UW，2609.37725）—— 把上下文当文件让模型自己管理，零样本/ICL/RL 三路验证，双通道（任务+效率）advantage，直击长程 agent 上下文瓶颈。
5. **AutoGUIWorld**（Tencent Hunyuan，2610.01215）—— 用图像编辑模型做 GUI 视觉 world model，零部署合成 79K 步轨迹，OSWorld 33.0%→40.8%；"环境可以被生成"的新路线（但无执行验证）。
6. **AREX-2**（BAAI，2609.38288）—— 在 ML 工程/算法编程上合成长程反思轨迹，27B 模型 BrowseComp 84.0、MLE-bench Lite 81.8；数据原则（保留失败与恢复）有启发，迁移结论需 matched 消融。
7. **OSWorld-Pro**（NVIDIA，2609.24890）—— 300+ 任务、2,800+ 子目标、67K 人工标注的过程式 CUA 评测，可演化为 process reward；（本身评级为"值得浏览"，因无代码，但方向关键故入榜）。
8. **False Frontiers**（Rutgers 等，2609.39102）—— 揭示"自出题+自验证"闭环的 proposer–solver 共谋（co-cheating），并用 cross-fitting 缓解；对所有自动任务合成型 RL 环境都是重要警示（评级"值得浏览"，数字待核实）。

> 次一档值得关注：CUA-SWE（coding×computer-use 评测）、DeskForge（受控桌面组合的稠密 grounding 数据）、HazardAuditor（CUA 轨迹级 guard）、IterSynth（角色解耦 RDPO）、EvoSkill-GUI（结构化 skill 演化）、OSWorld-Science。

## 跨论文趋势（6 条）

1. **环境合成规模化，且光谱拉得很宽**：从"真实执行 + 强验证"到"纯视觉生成 + 无验证"形成一条连续谱——RecreationWorld（开源 app + 参考实现做 oracle）、SoftwareGym（LLM 从规格合成原生 app + GUI 测试修复）、DeskForge（组合真实应用的受控桌面场景）、AREX-2（把 GitHub repo / OJ 题变成可执行沙箱）、AutoGUIWorld（图像生成器直接合成观测，不跑软件）。共同问题是"可验证性 vs 覆盖面"的权衡：越靠近生成端，覆盖越广但越难提供 RL 奖励。
2. **GUI + CLI / Code 的 hybrid CUA 成为主流定义**：HybridCUA（GUI+shell 统一动作）、RecreationWorld（explore–implement–verify）、CUA-SWE（code-only vs CUA 对比，前沿模型在 DevOps/Mobile 从 0 提升到 55–80%）、OSWorld-Science（83.6% 任务支持 CLI）。一致发现：未经训练直接加 CLI 会掉分（HybridCUA 报告 38.8→18.4），"何时用哪种接口"需要专门数据与奖励。
3. **评测从终态走向过程，并开始审计 evaluator 本身**：OSWorld-Pro（子目标 + LLM-Judge）、WebArena-Lite 人工审计（自动 evaluator 漏判 5.45–8.49pp）、CUA-SWE（复杂的复核/替换规则）、OSWorld-Science（artifact 级部分分）。对 RL 的含义：终态 verifier 的假阴性/假阳性会直接污染奖励，process reward 与 verifier 质量审计会成为环境构建的标配。
4. **自动生成任务/奖励的"自欺"风险被正面研究**：False Frontiers 的 co-cheating（proposer 与 solver 共享错误）、ReSAIL 的迭代自蒸馏崩塌、EvoSkill-GUI 的 test-time 进化依赖成功信号、AREX-2 作者自承迁移需 matched 消融。趋势是引入"独立性"——交叉拟合、critic 信息隔离（EvoSkill 消融：去隔离 69.52→60.95）、冻结 teacher 正则化。
5. **细粒度 credit assignment：按角色/区域/通道拆分 advantage**：IterSynth 的 RDPO（Planner/Synthesizer 分池归一化，混合归一化反而低于 GRPO）、CLM 的任务+效率双通道（效率项只作用于上下文编辑 token）、HazardAuditor 的 GuardPO（rationale 与 verdict 区域分别归一化）、HybridCUA 的 step-level `r_exec` 罚失败命令 token。agentic RL 正在从"整条轨迹一个标量"走向"结构化 advantage"。
6. **长程能力：上下文管理与经验复用从 harness 走进权重**：CLM（模型原生编辑上下文并可 RL）、IterSynth（summary 即状态）、AREX-2（长程反思写入权重）、X-Tree（BPE 式技能树进入 RL/蒸馏）、对照 training-free 的 EvoSkill-GUI（结构化 skill 包）与 ExpActivator（step-level 经验激活）。此外 **CUA 安全**（HazardAuditor 的执行轨迹级 guard）与 **GUI world model**（AutoGUIWorld、DeskForge 的 (S,a,S') 转移）作为两个较新的支线也在成形。

## 评级总览

| # | 论文 | 方向 | 来源深度 | 评级 |
|---|---|---|---|---|
| 1 | RecreationWorld | CUA 环境 / hybrid | repo-readme | 必读 |
| 2 | SoftwareGym | CUA 环境合成 | repo-readme | 必读 |
| 3 | HybridCUA | GUI+CLI / RL | repo-readme | 必读 |
| 4 | OSWorld-Science | CUA benchmark | repo-readme | 值得浏览 |
| 5 | OSWorld-Pro | 过程评测 | abstract-only | 值得浏览 |
| 6 | CUA-SWE | coding×CUA benchmark | repo-readme | 值得浏览 |
| 7 | AutoGUIWorld | GUI world model / 数据 | repo-readme | 必读 |
| 8 | DeskForge | grounding 数据 | repo-readme | 值得浏览 |
| 9 | EvoSkill-GUI | training-free skill | repo-readme | 值得浏览 |
| 10 | ExpActivator | 个性化 GUI 记忆 | repo-readme | 可跳过 |
| 11 | HazardAuditor | CUA 安全 guard | repo-readme | 值得浏览 |
| 12 | WebArena-Lite 审计 | web 评测可靠性 | abstract-only | 可跳过 |
| 13 | ReSAIL | 迭代自蒸馏 | repo-readme | 可跳过 |
| 14 | X-Tree | 技能挖掘 + RL | repo-readme（代码未发布） | 值得浏览 |
| 15 | AREX-2 | 长程反思 / deep research | repo-pdf（overview） | 必读 |
| 16 | IterSynth | deep search RL | repo-readme | 值得浏览 |
| 17 | Context Language Models | 上下文管理 / RL | repo-readme | 必读 |
| 18 | HyperBrowseComp | 多语言多模态浏览 benchmark | abstract-only +search | 值得浏览 |
| 19 | False Frontiers | 自进化搜索 agent 奖励作弊 | abstract-only +search | 值得浏览 |
| 20 | ZGCM-1 | 7B 开源基座 | repo-readme | 可跳过 |
| 21 | CorpusMap | 语料导航层 | abstract-only +search | 可跳过 |
| 22 | SSR | 多模态搜索推理加速 | repo-readme | 可跳过 |
| 23 | Agentic Retrieval 成本 | 检索 | abstract-only | 可跳过 |
| 24 | AdaTutoRank | 集合式 reranker | abstract-only | 可跳过 |

---

## 一、CUA 环境 / 数据合成 / 训练

### RecreationWorld: Scalable and Verifiable Environments for Hybrid Computer-Use Agents
arXiv 2609.22000 · 2026-09-21 · Qwen（阿里通义，32 位作者含 Shuai Bai、An Yang、Dayiheng Liu、Bowen Zhou）· HF 63↑ · [arXiv](https://arxiv.org/abs/2609.22000) / [HF](https://huggingface.co/papers/2609.22000) / [code](https://github.com/QwenLM/RecreationWorld) / [site](https://recreation-bench.cc/)

来源：`repo-readme`（README + tasks manifest + overview 图）

- **TL;DR**：把"给一个正在运行的参考软件，让 agent 自己探索它、再写代码复刻出一个行为一致的实现"作为任务范式（recreation），参考软件本身就是隐藏行为测试的 oracle，从而在五个平台上得到可规模化、可执行验证的 hybrid（GUI+coding）CUA 训练环境与 250 题 RecreationBench。
- **Problem**：CUA 研究分裂为 GUI 操作（OSWorld/AndroidWorld 线）和 coding/CLI（SWE-bench/Terminal-Bench 线），而真实数字工作需要两者交错；同时缺少可规模化、带可执行奖励的 hybrid 任务来源。
- **Method**：任务 = 高层需求 + 可交互的 running reference + GUI 控制工具与软件开发工具；无固定 workflow，agent 自主形成 explore–implement–verify 循环（探索参考 → 写代码 → build & launch 自己的候选 → 视觉检查 → 修改）。评分基于行为而非源码相似度：reference-grounded programmatic assertions + visual（VLM）assertions，覆盖多个交互深度的 action-conditioned outcome；每条断言先在 reference 上验证并经人工审核后冻结。用高质量开源应用规模化生成轨迹做训练。
- **Environment / data**：Ubuntu / macOS / Windows / Android / Web 五平台，每平台 50 题（共 250，easy/medium/hard 三档），评测接口分别为 AT-SPI、AXUIElement、UI Automation、UiAutomator、browser assertions；统一 harness（native GUI control + coding tools）。数据集放在 HF `Qwen/RecreationBench` 与 ModelScope。
- **Key results（作者自报）**：
  - RecreationBench（五平台 macro 平均，Prog/VLM 两种打分的均值）：GPT-6 Astra（Codex/max）58.06（Prog 58.19 / VLM 57.92），Claude Opus 5（Claude Code/max）44.16，GPT-5.6 Sol 42.06，Grok 4.6 36.73，Qwen3.8-Max-0902 34.80，Kimi K3 31.41，Claude Opus 4.8 31.10，GLM-5.3 24.38，Gemini 3.7 Flash 21.12，Qwen3.7-Plus 9.15。Prog=100% 的 app 比例最高也仅 2.8%（GPT-6 Astra）；每题估算成本 GPT-6 Astra ≈ $115.8、Opus 5 ≈ $117.2（假设 90% cache read）。
  - 训练迁移（overview 图）：在五个 OOD coding / hybrid CU benchmark 上的平均增益 Qwen3.7-Plus **+5.8pp**、Qwen-Flash-CPT **+12.1pp**；摘要称训练后模型"更频繁地视觉验证其渲染产物"。五个 OOD benchmark 的具体名称与逐项数字在 README 中未给出（未知）。
- **What's new**：相对 OSWorld / WindowsAgentArena（GUI 任务 + 手写 checker）和 SWE-bench / Terminal-Bench（纯代码），它把"参考软件 = oracle"变成通用奖励来源，天然支持任意开源 app 的规模化；评测不绑定实现语言/框架；同时覆盖五个 OS 平台（多数 CUA 环境只做 Ubuntu 或 Android）。与 Design2Code / WebGen 类"截图到代码"任务相比，这里需要交互式探索行为而不只是看静态截图。
- **Reputation check**：Qwen 核心团队（Qwen-VL / Qwen 主线作者），HF 63↑，MIT 开源 harness + HF/ModelScope 数据，含独立网站。红旗：训练所用的 Qwen-Flash-CPT 为内部模型，训练数据/轨迹是否开源 README 未说明；评测依赖 VLM judge（Visual 分数）且每题成本 >$100，第三方复现门槛高；"recreation" 任务与开源 app 的预训练记忆可能存在 contamination（模型可能见过这些开源 app 的源码）。
- **Limitations**：作者侧——需要 prepared execution environment + 模型与 judge endpoint；我方补充——(1) recreation 是"有参考实现"的特殊设定，迁移到无 oracle 的开放任务需要 OOD 证据（目前仅给出平均增益）；(2) 开源 app 源码泄漏风险；(3) 视觉断言依赖 judge，存在 judge bias。
- **Relevance**：
  - 对做 agentic-RL 环境的人，这是"把任意可运行软件变成可验证奖励"的一个非常干净的范式：reference-as-oracle + 行为断言，可直接借鉴到 web app 复刻、API 复刻等环境构建。
  - 对 CUA 训练，它是 GUI+coding hybrid 的首个跨五平台 benchmark，可作为衡量"会不会自己跑起来看一眼"的指标。
- **Verdict**：**必读** —— Qwen 出品、五平台、可执行奖励的 hybrid CUA 环境范式，环境构建思路高度可迁移。

### SoftwareGym: Scaling Computer-Use Agent Training with Diverse Synthesized Software Environments
arXiv 2610.12611 · 2026-10-12 · 上海交通大学（Siheng Chen 组）· HF 85↑ · [arXiv](https://arxiv.org/abs/2610.12611) / [HF](https://huggingface.co/papers/2610.12611) / [code](https://github.com/MrKiing-Jin/SoftwareGym)

来源：`repo-readme`

- **TL;DR**：用 Codex CLI 驱动的多 agent 流水线自动"设计→编写→GUI 测试→迭代修复"出 182 个可运行的桌面 GUI 应用（.NET 8 + Avalonia），作为 CUA 训练环境；在其上采集的轨迹把 OSWorld Pass@3 从 41.39% 提升到 56.97%。
- **Problem**：原生应用环境搭建成本高、覆盖面窄、容易对特定 app 过拟合；浏览器托管的合成环境（如 web 版合成 app）交互深度与流程复杂度有限。
- **Method**（README 描述的四阶段）：(1) Design：FunctionDesigner 写需求规格，StyleDesigner/SubStyleDesigner 生成 N 套不同 UI 风格蓝图（Avalonia `.axaml`），IconDesigner 产出 SVG 图标并有硬校验门；(2) Build：Coder 实现应用、DevCoder 审查修复（全部通过 Codex CLI）；(3) Evaluate：EvalTaskGenerateAgent 生成 GUI 测试用例，GUIEval 在 OSWorld Docker（真实 Ubuntu 22.04 VM）里用 GUI agent（GPT-5.4 风格 computer-use 或 Seed）执行，输出 summary；(4) Iterate：v1→v3 三轮修复，把评测反馈喂回 Coder。另有 style diversity / visual fidelity 指标模块。
- **Environment / data**：182 个应用，12 个类别（如 ChatAPP、PicEditor），平均 GUI 任务通过率 91.5%；SoftwareGym-Bench 120 题，同样覆盖 12 类。部署于与 OSWorld 相同的 VM 基础设施（刻意对齐下游评测环境）。
- **Key results（作者自报）**：OSWorld（作者强调 strictly out-of-domain）Pass@3 41.39% → 56.97%；SoftwareGym-Bench 40.0%。基座模型名称、是 SFT 还是 RL、Pass@1 数字在摘要/README 中均未给出（未知）。
- **What's new**：相对于 web 合成环境（如 AgentSynth / WebArena-Infinity 一类浏览器托管合成 app）和手工原生环境（OSWorld），它合成的是**原生桌面应用**且带"运行时 GUI 验证 + 迭代修复"闭环，保证功能可用；与 RecreationWorld 不同，这里不需要参考实现，而是从规格合成。
- **Reputation check**：SJTU Siheng Chen 组（多 agent 系统方向活跃），HF 85↑（本批 CUA 类最高之一），pipeline 代码开源。红旗：(1) 合成应用与评测环境都建在 OSWorld 同一 Ubuntu VM 上，"strictly OOD" 指的是应用不重合，但 UI 风格/环境分布是刻意对齐的；(2) 只报 Pass@3，不报 Pass@1，可比性差（OSWorld 官方榜通常为单次成功率）；(3) SoftwareGym-Bench 为自建 benchmark；(4) 生成的 182 个 app 与训练轨迹/模型权重 README 未声明开源（仅 pipeline），且依赖 Codex CLI + Responses API + computer-use endpoint，复现成本高。
- **Limitations**：作者侧——需要 35GB OSWorld VM 镜像、.NET SDK、Responses API endpoint；容器清理需外部 reaper。我方补充——所有 app 均为 Avalonia 单一 UI 框架，视觉/控件分布单一，可能对 Avalonia 风格过拟合；合成 app 功能深度仍远低于 LibreOffice/GIMP 等真实软件。
- **Relevance**：
  - "LLM 写软件 → 真实 GUI agent 测试 → 迭代修复" 是合成 CUA 环境的可复制模板，评测反馈驱动修复的闭环值得借鉴。
  - 可以与 RecreationWorld 对照：一个从规格合成（无 oracle，靠 GUI 测试筛），一个从参考复刻（有 oracle）。
- **Verdict**：**必读** —— 本月 CUA 环境合成最具代表性的工作之一，OSWorld 提升幅度大，但需留意 Pass@3 口径。

### HybridCUA: Learning to Orchestrate GUI and CLI for Computer-Use Agents
arXiv 2609.38008 · 2026-09-30 · 浙江大学 ZJU-REAL（Yongliang Shen 组）· HF 28↑ · [arXiv](https://arxiv.org/abs/2609.38008) / [HF](https://huggingface.co/papers/2609.38008) / [code](https://github.com/ZJU-REAL/HybridCUA) / [site](https://zjureal.com/HybridCUA/)

来源：`repo-readme`

- **TL;DR**：让 CUA 学会"何时、如何"在 GUI 操作与 shell 命令间切换：构造 GUI-only / CLI-only / 交错三类轨迹（HybridCUA-8K）做 SFT，再用 CLI-aware reward 做 GRPO，9B 模型 OSWorld 53.6%、平均仅 14.0 步。
- **Problem**：纯 GUI 慢且误差级联；GUI+app-specific API（如 ToolCUA、UltraCUA、AutoGLM-OS）需要逐应用工程；直接给未训练模型开 CLI 反而有害——作者报告给 agent 暴露 CLI 会让 OSWorld 掉 2.5–11.5 分（Qwen3.5-9B：GUI 38.8 → GUI+CLI 18.4）。
- **Method**：
  - 统一动作空间：所有交互都走同一个 `bash` 动作——直接 shell 命令，或 heredoc 包裹的 `pyautogui` Python 代码；作者称拆成两个独立 tool 会掉 7.2 分。
  - 数据：5,023 条 SFT 轨迹，11 个应用域（GUI-only 870 / CLI-only 3,155 / 交错 998）+ 3,000 条可验证 RLVR 任务，每条任务标注"CLI 是否有明确执行优势"。
  - 两阶段：SFT → GRPO，两个 CLI-aware 奖励：`R_CLI`（轨迹级，λ=0.1，仅当成功且 CLI 使用与任务标签一致时加分，教 *when*）；`r_exec`（step 级，λ=0.3，对 shell 层面失败的命令 token 罚分，教 *how*）。
  - 基础设施：env_infra 通过统一 `/v1/sessions` HTTP 协议提供 OSWorld / MobileWorld / CUA-Gym 环境，训练侧 slime + Megatron-LM actor + SGLang rollout，完全异步。
- **Key results（作者自报）**：OSWorld 53.6%（14.0 avg steps） vs 基座 Qwen3.5-9B GUI 38.8%（31.6 步）；对比 ToolCUA-8B 46.8%、AutoGLM-OS-9B 48.9%、UltraCUA-32B 43.7%。OOD：OSWorld-MCP 47.1%（+9.1），WindowsAgentArena 36.0%（+4.0，仅在 Linux shell 上训练却会发 PowerShell）。消融：去掉 `R_CLI` 轨迹缩短 18.2%（完整版 29.3%）；去掉 `r_exec` 执行错误率 16.5%（完整版 11.5%）。
- **What's new**：相对 UltraCUA / ToolCUA / CoAct-1 等"GUI + 专用 API/工具"或"GUI + coder 多 agent"方案，它用 OS 自带 CLI 替代逐应用 API，并用 RL 奖励显式教模型"选择性使用 CLI"；"统一 bash 动作空间"这一设计细节有消融支持。
- **Reputation check**：ZJU-REAL 是 GUI agent 方向高产组（同组本批还有 EvoSkill-GUI、IterSynth），HF 28↑，开源数据 + 环境 + RL 训练代码（模型权重 "coming soon"）。红旗：(1) OSWorld 上 CLI 天然能"绕过"GUI 检查（例如直接改文件满足 checker），53.6% 中有多少是 checker 可被 shell 满足的任务需要看 per-domain 表；(2) 基座 GUI+CLI 18.4% 这一对照可能放大了收益叙事；(3) 权重未放出。
- **Limitations**：我方补充——CLI 能力在 Windows/macOS/移动端的可迁移性只在 WAA 上测了一个点；CLI 带来的安全风险（rm、网络请求）未在 README 中讨论；任务"CLI 优势"标签是人工/启发式标注，规模化难。
- **Relevance**：
  - 做 CUA 动作空间设计时，"单一 bash 动作统一 GUI+CLI" 是可直接抄的工程决策；`R_CLI` + `r_exec` 是"工具选择型 reward shaping"的清晰样例。
  - 其 env_infra 的 `/v1/sessions` 统一协议 + 全异步 RL 框架对搭 agentic-RL 基础设施有参考价值。
- **Verdict**：**必读** —— GUI+CLI hybrid 是本月最明确的趋势，这篇给出了数据 + RL 奖励 + 开源基建的完整方案。

### OSWorld-Science: A Benchmark of Computer Use Agents for Learning and Using Scientific Software
arXiv 2609.39903 · 2026-10-01 · DiscoAILab（作者含 Jie Tang、Juanzi Li、Ge Zhang、Pengyu Nie 等，清华/多校联合）· HF 28↑ · 62 页 · [arXiv](https://arxiv.org/abs/2609.39903) / [HF](https://huggingface.co/papers/2609.39903) / [code](https://github.com/DiscoAILab/OSWorld-Science)

来源：`repo-readme`

- **TL;DR**：在 OSWorld 框架上构建 146 个科学软件任务（化学/物理/医学/统计/生物/GIS/语言学，17 种专业软件），用 artifact 级可执行 evaluator 并给部分分，测 12 个 VLM，结论是 SOTA 模型配强 harness 仍难以完成关键科学工作流。
- **Problem**：现有 CUA benchmark（OSWorld、WindowsAgentArena）以办公/日常软件为主，科学软件界面专业、对象复杂（分子、分割 mask、仿真），结果需要科学正确性检查。
- **Method / Environment**：专家提案 + 迭代 human–AI co-design 产出任务；任务覆盖 QuPath、ChemDraw、ASKCOS、SAS/R、OpenFOAM、ANSYS、EEGLAB、PyMOL/Mnova、QGIS、CIAO+DS9、Weasis、Praat、3D Slicer 等；域分布 Chemistry 43 / Physics 31 / Medicine 26 / Statistics 20 / Biology 18 / GIS 6 / Linguistics 2。所有任务需视觉观察，83.6% 同时支持 CLI。Evaluator 检查应用状态与产物（分子结构、mask、图、数值），支持部分分。harness 包含 model adapters、交互循环控制、轨迹日志；内置 OSWorld PromptAgent 与 Kimi 的 tool-calling agent。VM 镜像每个 23–34GB，全量约 196–210GB；EEGLAB 镜像未发布、Windows/ANSYS Fluent 镜像不可分发。
- **Key results**：README 与摘要均未给出具体分数（摘要截断；仅定性称 SOTA VLM + 强 harness 仍有挑战，并分析了多语言、reasoning effort 等维度）。具体数字：未知。
- **What's new**：相对 ScienceBoard（科学软件 CUA benchmark 前作）和 OSWorld，它更强调"artifact-based、部分分、科学正确性"评测以及 GUI+CLI 双通道；领域覆盖 CFD/病理/GIS 等更重的专业软件。
- **Reputation check**：作者阵容强（Jie Tang、Juanzi Li、Ge Zhang），HF 28↑，62 页，代码/任务/镜像开源，CC-BY 4.0。红旗：(1) 作者明确提醒公开数据集含答案 key（`private/` 目录不是访问控制），存在训练污染风险；(2) 146 题、部分域题量极小（语言学 2 题、GIS 6 题），域级结论统计意义有限；(3) 部分镜像不可获得，完整复现受限。
- **Limitations**：作者侧——部分 VM 不可分发、答案公开；我方补充——部分分 evaluator 的设计可能让不同域分数不可比；没有训练集，只是评测。
- **Relevance**：
  - 对 CUA 研究者，是"长尾专业软件"泛化的压力测试；对环境构建者，其 artifact-level evaluator 设计（分子/mask/数值比对）是做可验证奖励的好参考。
- **Verdict**：**值得浏览** —— 高质量 benchmark，但仅评测、题量小，对多数通用 BUA/CUA 训练者是补充性指标。

### OSWorld-Pro: Process-based Evaluation for Computer Use Agents
arXiv 2609.24890 · 2026-10-06 · NVIDIA（Zhilin Wang、Jan Kautz、Yi Dong 等）· HF 22↑ · [arXiv](https://arxiv.org/abs/2609.24890) / [HF](https://huggingface.co/papers/2609.24890) / code: 无

来源：`abstract-only`

- **TL;DR**：为 OSWorld 风格任务标注子目标，提供 300+ 任务、2800+ 子目标、基于 67,000+ 条人工标注的过程式评测，并用人类对齐的 LLM-Judge 判定子目标完成情况，揭示模型在"过程"上的失败模式。
- **Problem**：OSWorld 一类评测只看几百步后的最终交付物，无法解释为何失败（例如键盘输入错误 vs GUI 点击定位错误需要完全不同的改进策略）。
- **Method**：每个任务分解为顺序依赖的子目标；人工标注 67K+；训练/选择"robust human-aligned LLM-Judges"判定每个子目标是否达成，从而得到进度曲线和失败归因。
- **Key results（作者自报）**：Claude Opus 5 在 OSWorld-Pro 上 75.7%，对比其 OSWorld 83.4%（作者称为 top performer 也只有 75.7%）；识别出 subgoal-irrelevant actions、click-based mistakes 等过程失败模式。其他模型数字：摘要未给出（未知）。
- **What's new**：相对 OSWorld / OSWorld-Verified 的终态 functional checker，它做的是子目标级过程评测；与 AgentRewardBench、WebJudge 等"trajectory judge"相比，它有大规模人工子目标标注作为 ground truth。
- **Reputation check**：NVIDIA（Zhilin Wang 是 HelpSteer/奖励模型方向主力），HF 22↑。红旗：**无代码/数据链接**；LLM-Judge 的人类一致性数字摘要未给出；"75.7% vs 83.4%" 的比较口径（子目标完成率 vs 任务成功率？）摘要不清楚。
- **Limitations**：我方补充——过程评测依赖 judge，judge 本身对 CUA 截图/动作的理解误差会叠加；子目标"顺序依赖"假设可能惩罚走不同路径的合法解法。
- **Relevance**：
  - 子目标 + LLM-Judge 可直接转化为 dense/process reward（agentic-RL 中的 PRM），NVIDIA 若放出 judge 会很有用。
  - 失败模式分类（点击 vs 输入 vs 无关动作）有助于定位 CUA 训练瓶颈。
- **Verdict**：**值得浏览** —— 过程式评测方向重要，但无代码、只有摘要，等数据/judge 放出再细读。

### CUA-SWE: When Computer-Use Agents Meet Visual Software Engineering
arXiv 2609.32600 · 2026-10-01 · Carnegie Mellon University（及合作者）· HF 13↑ · [arXiv](https://arxiv.org/abs/2609.32600) / [HF](https://huggingface.co/papers/2609.32600) / [code](https://github.com/kingofspace0wzz/cua-swe)

来源：`repo-readme`（README + docs/results.md + results/）

- **TL;DR**：105 个"必须一边改代码一边运行并操作软件"的 SWE 任务（Web/Game/Mobile/DevOps），对比 code-only 与 hybrid CUA 两种模式，显示在需求/故障只能通过运行界面观察到时，给 agent 加上截图+GUI 操作能大幅提升成功率。
- **Problem**：coding agent（SWE-bench 线）与 CUA（OSWorld 线）被分开研究；真实开发需要运行软件、看界面、把视觉现象对应到代码再回到界面验证。作者进一步问：如果规格或操作信息只存在于运行中应用的可视界面，agent 能否完成 SWE 任务？
- **Method / Environment**：每题 = 指令 + 可编辑源码 + 应用环境 + 独立确定性 verifier（检查新需求且保持既有行为）。两种模式：code-only（源码+终端）vs CUA（额外截图+图形动作）。四个域：Web 36（编辑器、图表、地图、布局）、Game 29（12 款游戏的物理/状态转移/交互回归）、Mobile 20（移动 web）、DevOps 20（监控、看板、告警、可观测性）。沙箱用 bubblewrap，支持 Responses / Chat Completions / Anthropic Messages / Bedrock。
- **Key results（作者自报，Pass@1，code-only → CUA）**：GPT-6 Astra：Web 27.8→66.7、Game 17.2→37.9、DevOps 0.0→80.0、Mobile 0.0→55.0；Claude Opus 5：Web 22.2→55.6、Game 13.8→20.7、DevOps 0.0→60.0；Grok 4.6：Web 30.6→55.6、DevOps 0.0→65.0；Claude Sonnet 5：Web 8.3→0.0（CUA 反而下降）；GPT-5.6 Luna：Web 11.1→5.6。Codex+Sol、Claude Code+Opus 5 等 CLI agent 也有 CUA 列结果。DevOps/Mobile 的 code-only 几乎全 0，说明这些任务按设计"必须看界面"。
- **What's new**：相对 SWE-bench Multimodal（只给截图作为 issue 附件）和 Design2Code，它要求 agent 在**运行中的应用**上交互诊断并验证修复；与 RecreationWorld 同属"coding × computer-use" hybrid，但侧重 bug 修复/需求修改而非整体复刻。
- **Reputation check**：CMU 作者团队，HF 13↑，数据集/数据浏览器/评测代码完整开源，结果附 sha256 溯源。红旗：(1) 题量小（105 题，每个域 20–36 题，单题≈2.8–5pp）；(2) docs/results.md 说明 Game 域有 8/87 次首轮尝试在"runtime review"后被替换（GPT-6 原始 pass@1 为 11/29，替换后集合中首轮为 17/29），Web 域的报告成功需满足"protocol-compliance + CUA evidence"等附加条件——存在人工审查介入，评分口径较复杂；(3) DevOps/Mobile 的 code-only=0 是任务设计使然，"CUA 提升"部分是构造性的；(4) RLVR 训练环境尚在 roadmap 中，未放出。
- **Limitations**：我方补充——每域题量过小、方差大；部分模型（Opus 5 Mobile）deferred；评测成本与基础设施依赖（Node/Java/Playwright）较重。
- **Relevance**：
  - 对 BUA/CUA 训练者：给出"视觉验证闭环"在 coding 任务上的定量价值，是 hybrid agent 的好评测；其确定性 verifier 设计可迁移为 RLVR 奖励（作者也计划放出）。
- **Verdict**：**值得浏览** —— 问题定义好、开源充分，但题量小、评分规则复杂，更适合作为补充评测。

### AutoGUIWorld: Image Generators as Visual World Models for GUI Agent
arXiv 2610.01215 · 2026-10-02 · Tencent Hunyuan（与 HKUST(GZ) Yuyu Luo 组等合作）· HF 42↑ · [arXiv](https://arxiv.org/abs/2610.01215) / [HF](https://huggingface.co/papers/2610.01215) / [code](https://github.com/ImYangC7/AutoGUIWorld) / 模型 AGW-35B（HF）

来源：`repo-readme`（README + docs）

- **TL;DR**：不部署任何真实软件，用"planner 规划原子动作 + 图像编辑模型逐步改写截图"在视觉状态空间里合成 GUI 轨迹（79,266 条带 grounding 的 step 样本），微调 Qwen3.5-35B-A3B 后 OSWorld 33.0%→40.8%、ScienceBoard 14.0%→32.2%。
- **Problem**：GUI 轨迹多样性受限于可部署的软件环境；专业应用安装、配置、重置成本高。
- **Method**：(1) GUI world sampler：从 OS substrate（OS 类型、分辨率、动作空间）、visual appearance（主题、配色、字体、密度）、initial GUI state（窗口/标签数量、布局、可见控件、任务对象）三因素结构化采样并渲染初始截图；(2) 基于场景生成任务并去重；(3) Meta Planner 把任务拆为原子动作，Voyager 读最新干净截图、描述该动作的预期视觉变化，图像编辑后端渲染下一帧（同一轨迹内严格串行）；(4) Grounding（LocateAnything-3B / MAI-UI / VLM 直接预测）给点击动作加框；QC 审核 seed、任务相关性、grounding、transition 保真度。渲染/grounding 失败时保留有效前缀。
- **Environment / data**：代码支持 Windows 11 / macOS / Ubuntu 24.04 / Chrome 及 Android / iOS；报告训练集 79,266 条，覆盖 Chrome、Ubuntu、Windows、macOS。所用图像生成模型名称 README 未写死（通过 adapter 接入，具体模型：未知）。
- **Key results（作者自报）**：Qwen3.5-35B-A3B → AGW-35B：OSWorld mean task score 33.0%→40.8%；ScienceBoard success 14.0%→32.2%。其他 benchmark：未知。
- **What's new**：相对 UI-TARS / OS-Genesis / AgentTrek 等"在真实环境中探索或从教程回放"采集轨迹的方法，它是第一批把**图像生成/编辑模型当作 GUI 视觉 world model** 直接生成观测序列的工作；相对 ViMo、WebDreamer、UI world model 类工作（预测下一屏用于规划），这里目标是批量合成训练数据。
- **Reputation check**：腾讯混元 + 学术合作，HF 42↑，代码与 35B 模型开源。红旗：README 明确写明"不在真实桌面执行、不独立验证任务完成"——生成轨迹可能物理上不可行（幻觉 UI 状态）；OSWorld 用的是 "mean task score" 而非标准 success rate，口径需核对；ScienceBoard 涨幅大但基数低。
- **Limitations**：作者侧——transition 失败/漂移需重生；同轨迹串行渲染导致吞吐受限。我方补充——图像编辑模型对细粒度文本（表格数值、代码）一致性差，长轨迹视觉漂移；没有 reward 信号，只能做 SFT，不能直接用于 RL。
- **Relevance**：
  - "image generator as world model" 是绕开环境部署成本的新路线，适合补长尾应用的 grounding/规划先验；但对 agentic-RL 环境构建者，它不能替代可执行环境（无真实状态、无验证）。
- **Verdict**：**必读** —— GUI world model 方向的代表作，提供了一个可规模化的数据合成新范式，且有 OSWorld 实测收益。

### DeskForge: Dense Supervision from Desktop Environments for Computer-Use Agents
arXiv 2610.02320 · 2026-10-06 · ETH Zurich + IBM Research Zurich（Docling 团队）+ Microsoft（Marc Pollefeys）· HF 7↑ · [arXiv](https://arxiv.org/abs/2610.02320) / [HF](https://huggingface.co/papers/2610.02320) / [code](https://github.com/Saidgurbuz/deskforge) / 数据 DeskForge-1M + 模型（HF）

来源：`repo-readme`

- **TL;DR**：不录制而是"生成"桌面：把 19 个真实 Linux 应用组合成受控多窗口场景，融合截图、a11y tree 与窗口几何得到遮挡感知的稠密元素标注，构建 1.21M 观测 / 159.7M 元素 / 917K 点击转移的 DeskForge-1M，显著提升 GUI grounding 并转化为长程任务收益。
- **Problem**：桌面场景多应用、窗口重叠、相似控件竞争注意力，现有训练数据很少配稠密标注，也无法受控变化。
- **Method / Environment**：seeded scene specification 决定应用、初始状态、内容、窗口布局/层叠、外观预设（7 种，包括模仿 Windows/macOS 风格的主题——实际都在 Linux 后端上运行）、7 种分辨率（1366×768 至 3840×2160）；每个场景独立 headless Xvfb；元素记录类型、文本、完整与可见几何、层级、阅读顺序、所属窗口；记录 (S_t, a_t, S_{t+1}) 点击转移；有 pixel audit 与 QA gate。
- **Key results（作者自报）**：在 200K grounding 样本上微调四个 VLM，全部在 held-out 桌面条件和五个外部 grounding benchmark 上提升；Qwen3.5-4B：ScreenSpot-Pro +11.51pp、OSWorld-G +10.11pp。固定 planner 下作为 action model：WebArena-Infinity 31→50/119，OpenApps 3→15/100。
- **What's new**：相对 OS-Atlas、UGround、Jedi（OSWorld-G 的数据来源）等"截图+a11y 抽取"数据集，它强调**受控组合**（多窗口遮挡、主题、分辨率可编程变化）与**遮挡感知标注**，并附带动作转移数据。
- **Reputation check**：ETH CVG（Pollefeys）+ IBM Docling 团队，数据/模型/全流水线开源，工程质量高。HF 仅 7↑（关注度低，但质量信号不差）。红旗：(1) 所有"Windows/macOS"外观只是 Linux 上的主题模拟，对真实 Windows/macOS 的迁移需单独验证；(2) 只有 19 个应用；(3) 长程任务实验是"固定 planner + 微调 action model"，不是端到端 agent。
- **Limitations**：作者侧——应用需要 a11y tree 暴露主界面内容才能接入；我方补充——点击转移是随机采样点击，不是任务导向轨迹，对规划能力帮助有限。
- **Relevance**：
  - 对 grounding 模块/小模型 action head 训练是即插即用的高质量数据；其"可编程场景组合"思路可用于构造 CUA RL 环境的初始状态多样化（domain randomization）。
- **Verdict**：**值得浏览** —— 扎实的数据工程，grounding 方向必看，但对 agent 层面的 RL/规划贡献有限。

### Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents（EvoSkill-GUI）
arXiv 2609.17653 · 2026-09-18 · 浙江大学 ZJU-REAL（Yongliang Shen 组）· HF 12↑ · [arXiv](https://arxiv.org/abs/2609.17653) / [HF](https://huggingface.co/papers/2609.17653) / [code](https://github.com/ZJU-REAL/EvoSkill-GUI)

来源：`repo-readme`（repo 中 `docs/static/paper.pdf` 实为 ACL 模板占位，无全文）

- **TL;DR**：把 GUI skill 做成可编辑的多文件包（plan / backup 定位 / recover / a11y 工具 / 失败案例），部署时通过"执行中即时修订 + 信息隔离的 critic 反思 + 精确改文件 + 元数据检索复用"实现无训练的技能进化，在 MobileWorld/AndroidWorld/OSWorld 上持续提升多个基座。
- **Problem**：GUI 执行非平稳（弹窗、延迟加载、控件移位），预先写死的 skill（如 Anthropic Agent Skills 风格的单文档）易失效，且单体文档难以精确修复。
- **Method**：retrieve-or-generate（结构化元数据打分，阈值 0.6）→ execute & adapt（执行器通过受限接口 read/write/append/list/search/create_failure 在 rollout 中局部改文件）→ reflect in isolation（同一 backbone 另开 critic 会话，只看指令、截图、a11y、动作轨迹，隐藏 skill 本体、执行器 CoT 与 ground truth）→ revise（plan 错改 plan.md，grounding 错改 backup.md，缺 contingency 改 recover.md）→ reuse。直到任务成功或达到进化上限。
- **Key results（作者自报）**：
  - MobileWorld：Claude-Sonnet-4.6 57.1→67.6；Qwen3.6-Plus 53.3→69.5（+16.2）；Qwen3.6-35B-A3B 32.4→44.8；MAI-UI-8B 29.5→37.1。
  - AndroidWorld：Phase 1（seed 30）68.1→70.7，复用率 37.9%；Phase 2（seed 42，复用进化后库）55.2→61.2（+6.0）；232 题中恢复 27/89 个初始失败。
  - OSWorld：GUI-Owl-1.5-8B 46.7→54.8；Qwen3-VL-8B-Instruct 23.8→34.3（+10.5）。
  - 消融（MobileWorld）：结构化包 69.52 vs 单体 66.67；去即时修订 62.86；去 critic 隔离 60.95；元数据检索 12/12 vs 全文检索 1/12。
- **What's new**：相对 Agent Workflow Memory、SkillWeaver、Voyager 式 skill library 与 Reflexion 式反思，它的新意在于 skill 的**结构化分文件 + 定向编辑**以及"critic 信息隔离"（有消融支持）。
- **Reputation check**：ZJU-REAL，HF 12↑，代码开源（基于 MobileWorld 环境）。红旗：(1) 进化循环"直到成功或达上限"——在 MobileWorld/OSWorld 上若在同一测试任务上反复 rollout+修订，报告的成功率本质上接近多次尝试（pass@k 性质），需看论文是否区分；AndroidWorld Phase 2 换 seed 测复用更可信；(2) README 提到"paper-style MobileWorld task exclusions"——评测子集；(3) 部分消融样本量小（12 个检索案例）。
- **Limitations**：我方补充——test-time 进化需要失败信号（任务是否成功），真实部署中往往没有可靠 oracle；skill 库随部署增长的维护与冲突未讨论。
- **Relevance**：
  - 结构化 skill 包 + 受限编辑接口对构建"会自我改进的 CUA harness"有直接参考价值；但要警惕把 test-time 多次尝试当作单次成功率比较。
- **Verdict**：**值得浏览** —— harness 层面的工程思路好，评测口径需谨慎看待。

### Relevance Does Not Imply Applicability: Experience Activation for Personal GUI Agents（ExpActivator）
arXiv 2609.33304 · 2026-10-13 · 南洋理工大学（+ Alibaba Group）· HF 29↑ · [arXiv](https://arxiv.org/abs/2609.33304) / [HF](https://huggingface.co/papers/2609.33304) / [code](https://github.com/fyzhang1/ExpActivator)

来源：`repo-readme`

- **TL;DR**：发现个性化 GUI agent 检索到的历史只在 episode 第一步有用；提出训练无关的 ExpActivator，在每一步用冻结 backbone 的隐空间把当前屏幕匹配到历史状态并给出对应历史动作作参考，同时只在时间/场景证据充分时才主动推荐例行意图。
- **Problem**：现有方法（如 PersonalAlign 的层次意图记忆）按任务级相关性检索历史并塞入上下文，假设对每一步都有用；作者发现检索历史强烈改善首步，但对其余约 90% 的步骤几乎无持续收益，对"是否该主动建议"指导也弱。
- **Method**：step-level activation：当前截图在冻结 GUI backbone 的 latent space 与历史状态匹配，匹配上的历史动作作为 reference（可采纳/修改/拒绝）；task-level activation：基于时间与场景支持度决定是否主动提出 recurring intent，否则 abstain。无参数拟合，校准只用历史数据。
- **Environment / data**：PersonalAlign benchmark（Fingertip20k 历史）：个性化执行 775 episodes / 7,915 actions；主动建议 215 正例 + 100 负例状态。四个 backbone：Qwen3-VL-8B、MAI-UI-8B、Qwen3.5-9B、GUI-Owl-1.5-8B。历史记忆为每用户按时间前 80%，repo 带测试防泄漏。
- **Key results**：摘要截断、README 未列具体数字——"across four GUI backbones, ExpActivator improv[es]…"，具体增益：未知。
- **What's new**：把"检索相关性"与"决策时适用性"区分开，从 task-level RAG 变为 step-level state matching；相对 PersonalAlign（ACL'26）是直接改进。
- **Reputation check**：NTU + 阿里，HF 29↑，代码+数据开源、有泄漏检查测试，规范性不错。红旗：只在单一 benchmark（PersonalAlign，移动端）上评测；数字在可得材料中缺失。
- **Limitations**：我方补充——隐空间匹配依赖 backbone 表征，跨 backbone/跨 UI 版本更新时历史状态可能失配；隐私问题（长期存储用户截图）未讨论。
- **Relevance**：对做通用 BUA/CUA 训练的人是边缘相关；对做个性化/记忆的 GUI 助手产品有启发（step-level memory activation）。
- **Verdict**：**可跳过**（除非做个性化 GUI 助手）—— 问题窄、单一 benchmark。

---

## 二、CUA / Web Agent 安全与评测可靠性

### HazardAuditor: From Executable Threats to Safer Computer-Use Agents
arXiv 2609.15134 · 2026-09-15 · Ant Group（+ 浙大 Shouling Ji、复旦 Xingjun Ma 等）· HF 14↑ · [arXiv](https://arxiv.org/abs/2609.15134) / [HF](https://huggingface.co/papers/2609.15134) / [code](https://github.com/Yunhao-Feng/HazardAuditor) / 模型 `Yunhao-Feng/HazardAuditor`（HF）

来源：`repo-readme`（README + 模型卡 + training/guardpo/ALGORITHM.md）

- **TL;DR**：做一个"审计 agent 实际做了什么"的轨迹级生成式 guard（8B，基于 Qwen3Guard-Gen-8B），在受控环境里跑 Claude Code / Codex / Hermes / OpenClaw 四种异构 agent 框架并归一化为统一事件表示，再用 GuardPO（序列级 outcome、rationale 与 verdict 区域分别归一化）做 RL，CUA-Exec 上 90.88% 准确率。
- **Problem**：现有 guard（Llama Guard、Qwen3Guard 等）针对静态 prompt/response；现有可执行安全平台只输出评测结论，不产出 guard 学习所需的规范化监督。且 token-level 后训练目标让长 rationale 主导梯度。
- **Method**：(1) 基础设施：受控环境运行四种 agent 框架，交互归一化为 canonical event（user / agent thought+action / environment）；(2) 输出 `<analysis>…</analysis><label>safe|unsafe</label>`；(3) SFT → GuardPO：奖励 +1（格式合法且正确）/ −1（错）/ −1.25（格式非法），batch 去均值得到序列级 advantage 并广播到全部 token，token-level CISPO ratio，rationale 与 verdict 区域分别归一化后再聚合，防止 rationale 长度隐式改变样本权重。训练 prompt 来自 AgentHazard、ASSE、ATBench、R-Judge、Vera 五个源的训练集，每个 source×label 层 512 条（共 5,120）。推理时保留前 16K prompt token。
- **Key results（作者自报）**：CUA-Exec（四框架平衡的 safe/unsafe 轨迹）：SFT 80.50% → GuardPO 90.88%（+10.38）；分框架准确率 Claude Code 94.00（+12.5 vs 最强先前 guard）、Codex 95.50（+4.0）、Hermes 86.50（+9.5）、OpenClaw 87.50（+16.5，即摘要中"最高 16.5pp"）。外部：AgentHazard 87.55、R-Judge 89.60、ASSE-Safety 91.50、ATBench 88.40（准确率）。
- **What's new**：相对 R-Judge / ASSE / AgentHazard（评测集）与 Llama Guard / Qwen3Guard / ShieldAgent（静态或规则 guard），它是"可执行轨迹 → 归一化监督 → RL 训练的生成式轨迹 guard"的完整链路；GuardPO 对"rationale 长度主导梯度"问题的处理是方法上的小创新（借鉴 Complementary RL 的 extractor 形式）。
- **Reputation check**：蚂蚁安全团队 + 浙大/复旦安全方向学者，HF 14↑，代码+权重开源（数据不开源）。红旗：(1) 所谓"外部 benchmark"（AgentHazard、R-Judge、ASSE、ATBench）的**训练集**就在 GuardPO 训练数据中，属于同分布测试，不是真正 OOD；(2) CUA-Exec 为自建（从准确率粒度推测每框架约 200 条，为推测），轨迹与 benchmark 数据未公开；(3) 只截取前 16K token，长轨迹后段证据会丢失（模型卡自述）。
- **Limitations**：作者侧——是研究型 guard 而非访问控制，无法撤销已发生动作，分布外会误报/漏报；我方补充——事后审计（post-hoc）而非逐步拦截，部署到在线 CUA 需要流式/逐步版本；二分类粒度粗，不区分风险等级。
- **Relevance**：
  - 做 CUA 产品需要轨迹级 guard 时可直接试用该 8B 模型；其"多框架事件归一化"可作为 agent 安全日志 schema 参考。
  - GuardPO 的"分区域归一化"对任何"长 rationale + 短决策"的 RL（如 LLM-judge/奖励模型训练）都适用。
- **Verdict**：**值得浏览** —— CUA 安全方向本月最完整的开源 guard，但评测泛化性证据偏弱。

### Auditing Web Agent Evaluation on WebArena-Lite: Human Review of Outcomes and Trajectories
arXiv 2610.01491 · 2026-10-01 · 机构未标注（作者 Chengguang Gan、Kotaro Funakoshi 等，推测为日本研究机构/高校，未核实）· HF 无 · NeurIPS 2026 Workshop "Who Verifies the Agents?" poster · [arXiv](https://arxiv.org/abs/2610.01491) / code: 无

来源：`abstract-only`

- **TL;DR**：对 WebArena-Lite 全部 165 题在六种设置（GPT-5.5 与未训练的 Qwen3.5-9B）下做人工审计，发现自动 evaluator 漏判 5.45–8.49pp 的成功，并系统归类失败轨迹中的首个关键错误。
- **Problem**：web agent 评测依赖规则或 LLM evaluator，只看终态，缺乏人工验证与失败轨迹分析。
- **Method**：保留原始分数 → 人工纠正 false negative → 标注 first consequential error → 分析轨迹进度。另研究两个 harness 机制：MASM（Memory and Analysis Support Mechanism，显式维护执行状态）与 Guide Text（任务相关流程指导）。
- **Key results（作者自报）**：四个 GPT-5.5 设置下人工复核找回 5.45–8.49pp 被 evaluator 漏判的成功；25 步预算下 Guide Text 使 MASM 的修正后成功率 34.55%→38.18%；Qwen3.5-9B 上 MASM 使 evaluator 分数 13.90%→18.80%。102 条 GPT-5.5 失败轨迹的常见失败：滚动循环、探索未完成、过早作答、无效动作、表单流程不完整；"早期大量进展 + 最终失败"并存。
- **What's new**：与 OSWorld-Verified、WebArena-Verified、AgentRewardBench 等"修 benchmark / 评 judge"工作同一方向，在 WebArena-Lite 上首次给出全量人工复核与首错归因。
- **Reputation check**：workshop 论文、无代码、无 HF 热度；规模小（165 题、2 个模型）。红旗：GPT-5.5 + 25 步预算的设定偏离常见 SOTA 配置；MASM/Guide Text 属于 prompt 工程，Guide Text 可能泄漏任务特定知识。
- **Limitations**：样本小、单 benchmark、人工标注一致性未知（摘要未给）。
- **Relevance**：提醒构建 web agent RL 时"终态 evaluator 的假阴性"约 5–8pp 量级，会直接污染 RL 奖励；失败模式清单可用于设计 process reward。
- **Verdict**：**可跳过**（浏览摘要即可）—— 结论有用但证据规模小，与 OSWorld-Pro 同主题且后者更系统。

---

## 三、Agent 学习方法（自蒸馏 / 经验复用 / 自我改进）

### ReSAIL: Mitigating Collapse in Iterative Agent Self-Distillation
arXiv 2609.39306 · 2026-10-08 · 中国人民大学（Zhiwu Lu 组）· HF 32↑ · [arXiv](https://arxiv.org/abs/2609.39306) / [HF](https://huggingface.co/papers/2609.39306) / [code](https://github.com/ShengjieJin/ReSAIL)

来源：`repo-readme`（README + docs/method.md）

- **TL;DR**：发现基于 privileged information（PI）的迭代 agent 自蒸馏（SDPO、OEL）会在多轮部署循环中崩塌；提出 ReSAIL：只蒸馏 PI 最能改变 teacher 预测的步骤、按轨迹平衡损失，并保持学生的 PI-conditioned 行为（为下一轮当 teacher），三轮后最终成功率平均 +22.5pp。
- **Problem**：迭代自蒸馏被视为通向 recursive self-improvement 的路径，但每个更新后的模型既要无 PI 行动，又要作为下一轮带 PI 的 teacher；基础目标只训练无 PI 视角，导致 PI-conditioned 能力退化 → 下一轮监督变差 → 崩塌。
- **Method**：SGS（Sensitivity-Guided Selection，用有/无 PI 时 teacher 预测的 JS 散度选步骤；ALFWorld 选 5%、TextCraft 选 25%）+ TLB（Trajectory Loss Balancing）= TBSD；PR（Privileged Retention，在选中与未选中步骤上把学生的 PI 视角分布向冻结 teacher 正则化，权重 0.5/1.0）。基于 slime 实现；每轮 30 次优化更新。
- **Key results（作者自报）**：ALFWorld 与 TextCraft，Qwen3-4B/8B，三轮；在 SDPO 与 OEL 上加 ReSAIL，最终轮成功率平均绝对提升 22.5pp。多模态 GUI：在 AITZ 上用 sensitivity-guided 选择离线数据提升动作预测准确率（具体数字：未知）。
- **What's new**：相对 SDPO（self-distillation with privileged views）、OEL 等，首次系统性报告并缓解"迭代自蒸馏崩塌"。
- **Reputation check**：人大，HF 32↑，代码 + 8 个 Cycle-3 checkpoint 开源。红旗：主实验在 ALFWorld/TextCraft 这类文本玩具环境；与 CUA 的关联仅是 AITZ 上的离线动作预测，标签为 CUA 属于 mis-tag 倾向。
- **Limitations**：只有三轮循环，"缓解崩塌"在更多轮上是否成立未知；PI 的构造（如经验总结）在真实 CUA 中如何获得未讨论。
- **Relevance**：对做 agent 自我改进 / on-policy distillation 的 RL 研究者有方法价值（"步选择 + 保留 teacher 视角"），对 BUA/CUA 环境构建者间接相关。
- **Verdict**：**可跳过**（对 CUA/BUA 方向）—— 方法有意思，但实验在文本环境，CUA 相关性弱（疑似 mis-tag）。

### X-Tree: Tokenizing Reusable Experience for Efficient Agent Generalization
arXiv 2609.32993 · 2026-10-02 · University of Waterloo（Victor Zhong 组）+ Duke + NUS · HF 17↑ · [arXiv](https://arxiv.org/abs/2609.32993) / [HF](https://huggingface.co/papers/2609.32993) / [code](https://github.com/sitaocheng/X-Tree)（**仅占位，代码未发布**）

来源：`repo-readme`（仅概述）

- **TL;DR**：仿照 BPE 分词器，把 agent 轨迹中的动作规范化为 `verb⟨role⟩` 符号，按 X-Score（复现频率×长度×成功率）合并相邻符号形成可复用技能层次树（无 LLM 调用），再把树用于 offline RL、online RLVR（技能奖励 bonus）与 on-policy 自蒸馏（作为 teacher 的 privileged context）。
- **Problem**：SFT/RLVR 对 flat action stream 的每个 token 一视同仁，忽略跨任务复用的子流程；现有 skill 方法（LLM 写 skill 放上下文）不进权重、泛化依赖检索。
- **Key results（作者自报）**：WebArena、ScienceWorld、WebShop，1.5B/3B/7B 三种规模，在相同数据与预算下相对标准 recipe 最多提升 WebArena SR +4.5%、ScienceWorld SR +5.8%、WebShop success +4.1%。
- **What's new**：相对 Agent Workflow Memory、SkillWeaver 等在上下文中使用 LLM 写的技能，它从数据中统计地挖掘层次技能并"写入权重"；BPE 式技能挖掘思路新颖。
- **Reputation check**：Victor Zhong 组（Waterloo，web agent / RL 方向可靠），HF 17↑。红旗：**代码、挖掘出的树与训练 recipe 均未发布**（README 标明 project in progress）；小模型（≤7B）上绝对提升幅度有限（最多 4.5%）。
- **Limitations**：动作规范化 `verb⟨role⟩` 依赖环境有结构化动作（WebArena 的 a11y 元素角色），对纯像素坐标 CUA 动作不直接适用。
- **Relevance**：对 web agent 的 RLVR 奖励塑形（技能 bonus 在稀疏 verifier 信号时最有效）有启发；等代码发布后可评估。
- **Verdict**：**值得浏览** —— 思路新颖、组可靠，但代码未出、增益不大。

---

## 四、Agentic Search / Deep Research / 上下文管理

### AREX-2: Advancing Self-Improving Agents through Long-Horizon Reflective Tasks
arXiv 2609.38288 · 2026-10-01 · 北京智源研究院 BAAI（Zheng Liu、Zhicheng Dou、Defu Lian 等）· HF 122↑ · [arXiv](https://arxiv.org/abs/2609.38288) / [HF](https://huggingface.co/papers/2609.38288) / [code](https://github.com/VectorSpaceLab/AREX-2) / 模型 `BAAI/AREX-2`

来源：`repo-pdf`（repo 中 `assets/site/AREX-2.0-Research-Overview.pdf`，9 页官方研究概览，含完整对比表；非论文全文）+ `repo-readme`

- **TL;DR**：假设"反思 + 长程执行"是领域无关的元能力，于是在反馈最干净的 ML 工程与算法编程上合成"尝试→测量→反思→修改→继续"的完整长程改进轨迹（保留失败与回退），训练 Qwen3.8-27B 后不仅 MLE-bench Lite / Frontier-CS 强，还迁移到 deep research：BrowseComp 84.0。
- **Problem**：现有监督只保留"成功答案"，丢失了从弱解到强解的改进过程；test-time 自我改进（多轮迭代把预算转化为更好解）需要被内化，而不只是 scaffold 里的 retry loop。
- **Method**：数据引擎五步——Source（筛选有提升空间的 GitHub 仓库与 OJ 题目）→ Build（teacher 生成任务、评分函数、沙箱并验证有效性与 headroom）→ Iterate（允许数小时、大量 tool call，并注入运营知识和反馈）→ Select（run 级筛选：结果强且过程合规，不要求每轮都提升，保留失败与恢复）→ Train（在完整轨迹上下文中模仿有信息量的决策，冗余轮询/近重复轮不计 loss）。新 ML+coding 轨迹 + **不变的** AREX 原有 deep-research 数据。
- **Key results（作者自报，来自 overview PDF）**：
  - In-domain：MLE-bench Lite Medal Average 81.8（对比 GPT-5.6 Sol 72.7、Kimi-K3 72.7；每题预算 12h）；Frontier-CS Agent Track（188 题）70.7（GPT-5.6 Sol 76.4、Claude Opus 4.8 74.5、GPT-5.5 72.1；每题 5h）。
  - Cross-domain：BrowseComp 84.0（≤40B 最高；对比 GPT-5.6 Sol 90.4、Kimi-K3 91.2、Claude Fable 5 88.0、Iris-mini-35B 82.2、Tongyi-DeepResearch-30B 43.4）；HLE（text-only）52.6；GAIA 92.2（低于 Agents-A1 的 96.0）；DeepSearchQA F1 93.8。相对前代 AREX-Turbo（4B）：BrowseComp +13.3、HLE +12.0；且全面超过 122B 的 AREX-Base。
  - 评测协议：最多 300 内轮 / 1,500 总轮；外部 LLM judge；HLE text-only 与 full set 不可比（文中已标注）。
- **What's new**：相对 Tongyi DeepResearch、MiroThinker、WebSailor 等直接在搜索轨迹上训练的 deep research agent，它主张"在别的可验证领域学会长程反思，再迁移到搜索"；相对 MLE-agent / AIDE 一类 scaffold，强调把迭代改进能力写入权重。
- **Reputation check**：BAAI（BGE / FlagEmbedding 团队），HF 122↑（本批第三高），评测代码开源、模型在 HF。红旗：**作者自己在 overview 中承认**跨代对比混杂了 backbone 与参数量差异，"迁移假说"需要 matched-backbone 消融才能证实——即 BrowseComp 84.0 有多少来自新 ML/coding 数据、多少来自 Qwen3.8-27B 基座本身，目前不清楚；BrowseComp 300/1,500 轮的极大预算使其与他人数字不完全可比；"self-improvement 随轮数提升" 在 overview 中只有示意曲线，非实测曲线。
- **Limitations**：我方补充——训练数据合成依赖强 teacher 跑数小时，成本极高；评测依赖 LLM judge；训练数据是否开源 README 未说明。
- **Relevance**：
  - 对 agentic-RL 环境构建者：ML 工程 + 算法编程是"长程、可验证、有 headroom"的理想训练场，"保留失败与恢复的整段轨迹 + 只在有意义决策上算 loss"是可借鉴的数据原则。
  - 对 deep research agent：提示"跨领域长程反思数据"可能是提升 BrowseComp 的另一路线（需自行做消融验证）。
- **Verdict**：**必读** —— 本批 deep research 方向最强的开源 27B 结果，数据原则有启发，但迁移结论需审慎。

### IterSynth: Rethinking Deep Search Agents via Role-Decoupled Iterative Synthesis
arXiv 2609.29444 · 2026-09-25 · 浙江大学 REAL Lab + 腾讯（repo 在 Tencent org 下）· HF 8↑ · [arXiv](https://arxiv.org/abs/2609.29444) / [HF](https://huggingface.co/papers/2609.29444) / [code](https://github.com/Tencent/IterSynth)

来源：`repo-readme`

- **TL;DR**：同一策略交替扮演 Planner（决定搜什么或作答，只看 query+全局 summary）与 Synthesizer（把新证据写进 summary），用 summary 作为唯一持久状态控制上下文；配合按角色分池归一化 advantage 的 RDPO，IterSynth-8B 在五个 deep search benchmark 平均 50.7。
- **Problem**：ReAct 式 deep search agent 存在 role coupling（一个上下文同时承担规划、证据利用、综合）与 context accumulation（历史越长噪声越大）。
- **Method**：状态 = (q, M_t)；Planner 发出 SEARCH 或最终答案；Synthesizer 只能更新 summary。训练：约 10K 条经验证的冷启动 SFT 轨迹（SFT 代码未开源）→ RDPO：每轮 composite reward = 全局广播的终局 outcome（LLM judge）+ 该角色的 turn-level rubric（每角色 5 个维度），Planner 池与 Synthesizer 池**分别**做组内归一化后进入 GRPO。消融称：同样奖励但混合角色归一化会**低于** outcome-only GRPO。还区分环境失败（搜索 API 错误、超长截断）与模型行为问题（退化、过多 tool call）在 loss 中的处理。工具层：Serper.dev 搜索 + Jina Reader 抓取。
- **Key results（作者自报）**：IterSynth-8B（Qwen3-8B）：BrowseComp 30.9、BrowseComp-ZH 55.4、GAIA(text) 55.3、Xbench-DS-2505 66.0、Xbench-DS-2510 46.0，平均 50.7；对比 MiroThinker-v1.0-8B 平均 46.5（BrowseComp 31.1，略高于 IterSynth）、AgentCPM-Explore-4B 44.2。作为免训练 prompting：Claude-4.5-Opus 平均 66.1、DeepSeek-V3.1 平均 47.9，优于 ReAct 与 IterResearch。
- **What's new**：相对 IterResearch（summary 式马尔可夫状态重建）、ReSum、AgentFold（上下文折叠）与多 agent（Researcher+Refiner），它在单参数集内实现角色解耦，并给出"按角色分池算 advantage"的 credit assignment。
- **Reputation check**：ZJU-REAL + 腾讯，HF 8↑（关注度低），RL 代码以 verl patch 形式开源，SFT 数据/代码与权重未开源。红旗：平均分的提升主要来自 BrowseComp-ZH（+15.2）与 Xbench-DS-2510，BrowseComp 本身与 MiroThinker 持平略低；LLM judge 作为 outcome 奖励与评测；对比的 Claude-4.5-Opus 等基线已偏旧。
- **Limitations**：我方补充——summary 作为唯一状态存在不可逆信息丢失风险（Synthesizer 漏写的证据无法找回）；rubric 打分本身依赖 LLM judge，成本高且可能被 hack。
- **Relevance**：
  - "多角色共享参数 + 按角色分池 advantage"对任何多阶段 agent（如 CUA 的 planner/grounder）的 RL 都可迁移；summary-as-state 是长程 BUA 上下文管理的实用选项。
- **Verdict**：**值得浏览** —— 方法清晰、RL 细节有价值，但绝对性能与开源度一般。

### Context Language Models
arXiv 2609.37725 · 2026-09-30 · Meta Superintelligence Labs + University of Washington（Luke Zettlemoyer、Pang Wei Koh、Mike Lewis、Wen-tau Yih、Nathan Lambert 等）· HF 26↑ · [arXiv](https://arxiv.org/abs/2609.37725) / [HF](https://huggingface.co/papers/2609.37725) / [code](https://github.com/facebookresearch/context-language-models)

来源：`repo-readme`（README + clm_rl/README）

- **TL;DR**：把模型上下文当作一个文件，让模型自己无限制地编辑它，从而"原生"地管理自己的上下文；零样本即在 BrowseComp-Plus 上比 SOTA 上下文管理策略高 11.4% 且少 21.5% FLOPs，并提出 CLM 的在线 RL（双通道 advantage）与 Suffix Cache Reuse 服务优化。
- **Problem**：长程 agent 的上下文管理（摘要、折叠、截断）通常由外部 harness 规则控制，模型无法学习"什么值得保留"。
- **Method**：上下文 = 文件（`LIVE_CTX_MAIN.txt` 镜像），模型可任意更新；多 agent 场景下多个上下文共存为文件。三条路径：(1) zero-shot；(2) ICL：用标准 skill-optimization 循环进化自然语言指令来引导 CLM；(3) RL：在 GRPO 的 task 通道之外加 efficiency 通道，`A[i,t] = r_i + w_eff · a_eff_i · m_i[t]`，`a_eff` 为成功轨迹相对组均值的 FLOPs 节省（裁剪到 [-1,1]），只作用于"编辑上下文"轮的 token，w_eff=0.25；基于 NVIDIA ProRL-Agent-Server + slime 训练（RL 训练代码本身不在 repo，只提供 patch）。另有 Suffix Cache Reuse（vLLM/SGLang）。
- **Key results（作者自报）**：zero-shot：BrowseComp-Plus +11.4% 准确率 / −21.5% FLOPs；12 小时 EdgeBench +5% 分数 / −59% FLOPs；24 小时多仓库 agent-swarm 任务同算力下提升多 65%。ICL：上下文管理任务 held-out 准确率最高 +35.9 分。RL：Qwen3.5-9B 在 BrowseComp-Plus 上提升 47.6%（相对值）且少 12% FLOPs。Suffix Cache Reuse 在同性能下比标准 SGLang 少 35% 服务端算力。另发布 ContextBench。
- **What's new**：相对 MemGPT/Letta（分层记忆 + 函数调用）、ReSum / AgentFold / IterResearch（固定摘要或折叠策略），它把上下文管理变成模型的原生、可学习、可 RL 的行为，并与服务系统（suffix cache）协同设计。
- **Reputation check**：Meta + UW 顶级 NLP 团队，HF 26↑，代码开源，已有 Pi / OpenCode 插件"Day 1 support"。红旗：多处百分比为相对提升（如 47.6%），绝对数字 README 未给；RL 训练框架依赖外部仓库。
- **Limitations**：我方补充——无限制编辑意味着模型可能删掉关键信息（不可逆）；效率奖励只在"组内≥2 条成功轨迹"时生效，对难任务（低成功率）信号稀疏。
- **Relevance**：
  - 对长程 BUA/CUA（几百步截图历史）这是最直接相关的上下文管理范式；efficiency-channel advantage 是"在不改任务奖励前提下优化成本"的干净 RL 设计。
- **Verdict**：**必读** —— 顶级团队、通用且开源、直接解决长程 agent 的上下文瓶颈。

### HyperBrowseComp: A Multilingual and Multimodal Stress Test for Web-Browsing Agents
arXiv 2610.03574 · 2026-10-05 · MBZUAI（Alham Fikri Aji 等，多国母语作者）· HF 52↑ · [arXiv](https://arxiv.org/abs/2610.03574) / [HF](https://huggingface.co/papers/2610.03574) / code: 无

来源：`abstract-only` `+search`（二手新闻报道，未能访问原文）

- **TL;DR**：423 道人工撰写并经人工验证的高难度浏览题，覆盖 13 种语言，需要发现冷僻证据、跟随多步线索链或检查视频/扫描文档/图片/地图等异构来源。
- **Method**：母语或高水平作者出题；答案简短、可公开验证；用无联网模型过滤掉可凭参数知识回答的易题；评测 provider-native search 与统一外部检索 harness 两种设置，并对部分题目做人工评测以对照难度与耗时。
- **Key results**：摘要无数字。二手报道（runtimewire）称：五个被评测系统用自带搜索时共有 244/423（约 58%）题无人答对；替代检索设置消耗大量 token 却答对更少；结果依赖 provider 自己的搜索栈。具体每模型分数：未知（未能核实原文）。
- **What's new**：相对 BrowseComp（英文、纯文本）、BrowseComp-ZH（中文）、BrowseComp-VL / BrowseComp-V3（多模态）、MM-BrowseComp，它同时覆盖 13 种语言与多种证据模态（视频、地图、扫描件）。
- **Reputation check**：MBZUAI Alham Aji 组（多语言 NLP 知名），HF 52↑。红旗：无代码/数据链接（可得信息中）；423 题分到 13 种语言，每语言约 30 题，语言级结论统计力弱；provider-native search 的不透明性使跨厂商对比混杂了搜索后端差异（作者也指出）。
- **Limitations**：答案"公开可验证"意味着随时间推移会被网页化而泄漏（BrowseComp 类基准的通病）。
- **Relevance**：做多语言/多模态 BUA 的人可作为新的压力测试；"native search vs 统一 harness"的对比提醒评测时要固定检索后端。
- **Verdict**：**值得浏览** —— 有用的新 benchmark，但当前信息有限、无数据链接。

### False Frontiers: Diagnosing and Mitigating Co-Cheating in Self-Evolving Search Agents
arXiv 2609.39102 · 2026-10-01 · Rutgers University（+ UCSD、Michigan、McGill、KFUPM，据二手报道）· HF 192↑ · 21 页 · [arXiv](https://arxiv.org/abs/2609.39102) / [HF](https://huggingface.co/papers/2609.39102) / code: 无

来源：`abstract-only` `+search`（二手摘要：AI Weekly、chatpaper，未核实原文）

- **TL;DR**：自进化搜索 agent（proposer 出题 + solver 答题的闭环）会出现"co-cheating"：二者在共同错误上越来越一致，内部奖励上升而外部正确率不升；提出交叉拟合的 CrossFit，用在另一半文档上训练的辅助 solver 给 proposer 打分。
- **Problem**：自我出题/自我验证的闭环（如 R-Zero、Absolute Zero、Search Self-Play 一类）缺乏外部 ground truth，伪标签质量随轮次退化。
- **Method**：(1) 诊断：对照源证据做事后审计，发现 co-cheating 随轮次加剧；(2) 基线缓解 MSV（multi-sample verification）：同一模型有/无源文档各采样 3 次决定是否收录题目并替换伪标签——只部分有效、每候选多 6 次生成；(3) 主方法 CrossFit：源文档分 A/B 两组，A 组生成的问题由只在 B 上训练的辅助 solver 打分（反之亦然），交叉一致性决定 proposer 奖励；原 solver 更新规则不变。
- **Key results（作者自报）**：摘要：MSV 使 false-agreement 质量 Qwen3.5-4B 6.1%→5.7%、Qwen3.5-9B 8.8%→7.x%（摘要截断）。二手报道称 CrossFit 降至 3.0%（4B）/ 3.7%（9B），七个下游搜索 benchmark 平均相对耦合自进化 +8.8（4B）/ +8.4（9B）——**未核实原文**。
- **What's new**：把统计学中的 cross-fitting（双重机器学习的样本分割思想）引入自进化 agent 的奖励构造；明确命名并量化了 self-play 搜索 agent 的奖励作弊模式。
- **Reputation check**：HF 192↑（本批第二高，但机构信号一般）；无代码。红旗：无代码、核心数字只能从二手来源获得；HF 热度可能部分来自传播而非同行认可；只在 ≤9B 模型上验证。
- **Limitations**：CrossFit 需要额外训练一个辅助 solver（成本翻倍）；残余 co-cheating 仍存在。
- **Relevance**：
  - 任何"自动合成任务 + 自动验证"的 agentic-RL 环境（包括 CUA 任务合成）都可能遇到同样的 proposer–verifier 共谋，交叉拟合是值得借鉴的通用防护；对环境构建者是一个重要警示。
- **Verdict**：**值得浏览** —— 问题重要且普适，但缺代码、需等原文核实数字。

### ZGCM-1: A Fully Open and Extremely Efficient Foundation Model for Math and Agentic Search
arXiv 2609.13356 · 2026-09-15 · 中关村学院 / 中关村人工智能研究院 ZGCAGI（Tie-Yan Liu、Kai Chen、Shuxin Zheng 等）· HF 295↑ · [arXiv](https://arxiv.org/abs/2609.13356) / [HF](https://huggingface.co/papers/2609.13356) / [code](https://github.com/zgcagi/ZGCM-1) / 模型 `zgcagi/ZGCM-1-7B`、数据 `zgcagi/ZGCM-1-Data`

来源：`repo-readme`

- **TL;DR**：从零训练的 7.39B dense 全开源模型（权重 + 数据 + 训练日志 + 全流程代码），256K 上下文，主打数学推理与工具辅助搜索；预训练设计带来约 4.2× 的 16K time-to-loss 效率提升。
- **Method**：32 层，27 层 gated sliding-window（窗口 128）+ 5 层全局注意力，GQA 32/8；FP8 + Muon；预训练约 4.19T token；mid-training 约 600B token，上下文 16K→64K→256K，并把交互轨迹重写为 MDP 状态-动作转移监督单步决策；SFT 联合通用与 agentic、执行验证轨迹；探索了数学/代码混合 RL。"AI-native R&D"：agent swarm 参与集群运维、数据治理、评测。
- **Key results（作者自报，256K SFT checkpoint、thinking 模式）**：MATH-500 97.13；AIME 2026 75.00；HMMT 2025 70.42；agentic search：WebWalkerQA 63.09、BrowseComp 19.43、GAIA(text) 42.52（最多 64 步搜索-阅读）、Binary Function Search 62.00（31/50）。256K 训练吞吐相对全注意力 3.94×。
- **What's new**：相对 Olmo 3、MiniCPM4.1 等开源小模型，它把"agentic search 能力"纳入从预训练到 SFT 的全流程设计（MDP 化 mid-training），并完全开源。摘要称在若干数学与搜索套件上可与 Qwen3-235B-A22B、GLM-5.1 竞争——但 README 中搜索数字（BrowseComp 19.43）远低于本批 AREX-2（84.0）等专用 agent。
- **Reputation check**：Tie-Yan Liu 等知名研究者领衔，HF 295↑（本批最高），全开源（含 W&B 日志），可信度高。红旗："与大一个数量级的前沿模型竞争"的说法主要针对数学；搜索能力在绝对值上一般。
- **Limitations**：7B 容量限制；搜索评测步数上限 64，与 deep research agent 的数百步设定不可比。
- **Relevance**：对 BUA/CUA 方向是**间接相关**：主要价值在于全开源预训练/mid-training 配方（尤其"轨迹→MDP 转移"的 mid-training 做法）可供训练小型 agent 基座参考；不涉及 GUI/浏览器操作。
- **Verdict**：**可跳过**（对 CUA/BUA 方向）—— 优秀的开源基座工作，但与 agent 环境/BUA 主题关联弱，属于 tag 偏宽。

### Follow the Entities: A Corpus Map for Agentic Search（CorpusMap）
arXiv 2609.37226 · 2026-09-30 · Microsoft（+ KAIST Sung Ju Hwang；Soyeong Jeong 等）· HF 76↑ · [arXiv](https://arxiv.org/abs/2609.37226) / [HF](https://huggingface.co/papers/2609.37226) / code: 无

来源：`abstract-only` `+search`（二手社交媒体/聚合摘要，未核实原文）

- **TL;DR**：离线把语料组织成以"复现实体"为中心的导航层——每个实体一张 Entity Page，汇总信息并链接到所有提及它的文档，形成实体-文档图，agent 遍历即可收集分散证据，减少重复发现关系的 token 开销。
- **Problem**：在大型文档集合上做 agentic search 时，扁平文件集合不提示文档间关系，agent 每次查询都要重新发现，既漏掉互补证据又耗 token。
- **Method**：离线跨文档实体消解 → Entity Pages → 实体-文档图；链接跨查询共享；原文档保持不变。
- **Key results**：摘要称在 7 个模型、3 个 benchmark 上同时改善证据发现与（截断）……二手报道称答案质量 +6.4 到 +11.7 分、输入 token 减少 34%–57%，并优于 "LLM Wiki" 等另外几种导航层——**未核实原文**；benchmark 名称：未知。
- **What's new**：相对 GraphRAG（构建实体/社区图做全局摘要检索）、HippoRAG（知识图 + PPR），它把图作为**agent 可浏览的导航层**（类似给语料建 wiki/sitemap），配合迭代搜索而非一次性检索。
- **Reputation check**：Microsoft + KAIST，HF 76↑。红旗：无代码；离线实体消解的成本与错误传播未知。
- **Limitations**：语料更新需增量维护实体页；实体中心组织对非实体型信息需求（如数值趋势、观点）帮助有限。
- **Relevance**：对企业内文档 agentic search 有工程启发；对 BUA/CUA 环境构建关联较弱（可类比为给网站做"实体导航层"）。
- **Verdict**：**可跳过**（对 CUA/BUA）—— 偏 RAG/企业检索，非浏览器/GUI agent。

### Selection-Based Structured Reasoning: Toward Efficient Multimodal Search Agents（SSR）
arXiv 2610.01892 · 2026-10-07 · Carnegie Mellon University（Jean Oh、Reid Simmons 等，部分作者疑似来自业界合作方）· HF 15↑ · [arXiv](https://arxiv.org/abs/2610.01892) / [HF](https://huggingface.co/papers/2610.01892) / [code（非官方推理代码）](https://github.com/zfy0314/ssr-unofficial)

来源：`repo-readme`

- **TL;DR**：把小模型每轮的自由形式推理改为从预定义、可复用的自然语言推理候选中"选择"一个（按 teacher-forced 似然打分，KV cache 共享、并行 prefill），在 7 个多模态搜索 benchmark 上保持性能同时把每轮推理延迟降低 90%+。
- **Method**：候选库 R；每轮对 h + r_i 做批量 prefill（max_new_tokens=0）计算长度归一化 log-likelihood → softmax(S/τ) 选择 → 注入选中文本 → 自回归生成动作（tool call 或答案）。无需额外分类头；与多种 RL 目标及 SFT 兼容。
- **Key results（作者自报）**：2B/4B 模型，7 个多模态搜索 benchmark，平均成功率与同规模领先搜索 agent 相当；每轮推理延迟降低 >90%，每题总推理延迟降低 28–54%。具体 benchmark 名与分数：未知。
- **What's new**：相对 MMSearch-R1、WebWatcher 等自由 CoT 的多模态搜索 agent，把"推理"离散化为选择；类似思想见于 action/option 库，但这里是对 reasoning 而非 action 做选择。
- **Reputation check**：CMU 机器人方向团队，HF 15↑。红旗：repo 名为 "unofficial"，只有推理代码，训练代码（预计 2026-10 底）与 4B 权重（预计 2026-11 底）未发布；候选库需人工预定义。
- **Limitations**：预定义推理候选限制了开放式推理的上限，对分布外任务可能缺少合适候选。
- **Relevance**：对需要低延迟的小型 BUA/CUA 端侧部署，"推理即选择 + 并行打分"是值得尝试的推理加速技巧。
- **Verdict**：**可跳过** —— 效率技巧，与环境/训练主线关联弱，代码与权重尚未完整。

### Beyond Semantic Similarity: Performance and Costs of Agentic Retrieval for Complex Tasks
arXiv 2610.05750 · 2026-10-06 · NVIDIA（NeMo Retriever 团队，Even Oldridge 等）· HF 8↑ · [arXiv](https://arxiv.org/abs/2610.05750) / [HF](https://huggingface.co/papers/2610.05750) / code: 无

来源：`abstract-only`

- **TL;DR**：实证研究"LLM 在 ReAct 循环中调用 dense retriever"的 agentic retrieval：同一 embedding 模型下 nDCG@10 +8.7，跨域通用（ViDoRe v3 与 BRIGHT 榜单均有竞争力），但平均每查询 107.4 秒、764.1K 输入 + 5.8K 输出 token（对比标准检索 0.67 秒）。
- **Key results（作者自报）**：见 TL;DR；具体榜单名次：未知。
- **What's new**：主要贡献是成本-效果的量化，而非新方法；与 Search-R1、ReasonIR 等推理型检索方向相关。
- **Reputation check**：NVIDIA 检索团队，HF 8↑，无代码。红旗：方法上增量小；成本数字依赖所用 LLM（摘要未说明）。
- **Relevance**：给"agentic retrieval 成本约为传统检索 160×"提供了参照数字，对设计搜索 agent 预算有用；与 BUA/CUA 环境构建关联弱。
- **Verdict**：**可跳过** —— 有用的参考数据点，但非 BUA/CUA 主线。

### AdaTutoRank: Learning to Rerank Document Sets via Adaptive Tutoring Optimization for RAG and Deep Research
arXiv 2609.32472 · 2026-09-29 · Tencent · HF 17↑ · [arXiv](https://arxiv.org/abs/2609.32472) / [HF](https://huggingface.co/papers/2609.32472) / [code](https://github.com/AdaTutoRank/AdaTutoRank)（**仅 "Coming soon" 占位**）

来源：`abstract-only`（repo 只有一行 README）

- **TL;DR**：把 reranker 从"逐文档相关性"改为"组合完整、互补、不冗余的文档集合"，用三层九维 rubric 同时提供冷启动银标签、RL 奖励和蒸馏 hint，并按 rollout 质量自适应给出三种具体度递增的 hint（Adaptive Tutoring Optimization）。
- **Problem**：setwise reranker 若只用集合级 rubric 总分作奖励，监督稀疏、无法区分贡献者与"搭便车"文档；on-policy distillation 给所有 rollout 同样的固定指导，对强 rollout 过于规定、对弱 rollout 过于抽象。
- **Method**：ATO 从策略自身冻结快照中提取三种 hint：仅 rubric；self-selector 在 rubric 下挑出的兄弟集合；self-reflector 对比 rollout 与兄弟集合的反思——按 rollout 质量匹配 hint 形式。
- **Key results**：摘要截断，无数字（未知）。
- **What's new**：相对 SetRank / Rank-R1 等 listwise/setwise reranker，把"自适应 hint 的 on-policy distillation"引入集合式重排序。
- **Reputation check**：腾讯，HF 17↑；代码未发布、数字缺失。
- **Relevance**：对 deep research 的检索模块有参考；"按 rollout 质量自适应 hint"的蒸馏思想可迁移到 agent RL，但与 BUA/CUA 主线关联弱（被标为 browser-use-agent 属 mis-tag）。
- **Verdict**：**可跳过** —— 检索组件工作、无代码无数字、与 BUA/CUA 主题偏离。

---

## 附：数据来源说明
- 二手检索来源（仅用于 HyperBrowseComp / False Frontiers / CorpusMap，数字均未核实原文）：[runtimewire: HyperBrowseComp](https://runtimewire.com/article/hyperbrowsecomp-multilingual-search-agent-benchmark)、[AI Weekly: CrossFit](https://aiweekly.co/alerts/papers-crossfit-cuts-search-agent-co-cheating-to-37)、[chatpaper 353843](https://chatpaper.com/paper/353843)、[hyper.ai 2609.39102](https://hyper.ai/en/papers/2609.39102)、[AI Weekly: Follow the Entities](https://aiweekly.co/alerts/hf-paper-follow-the-entities-builds-an-offline-corpus-map-to-speed-agentic)、[opentrain: 2609.37226](https://www.opentrain.ai/papers/follow-the-entities-a-corpus-map-for-agentic-search--arxiv-2609.37226/)。
- 本地 repo 克隆位于 `/tmp/claude-0/paperrepos/`（仅读取文件，未执行任何 repo 代码）。
