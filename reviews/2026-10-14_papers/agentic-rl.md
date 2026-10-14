# Agentic RL 论文深读笔记（2026-09-14 → 2026-10-14）

> 范围：14 篇（输入 `B_agentic_rl.json`）。所有数字均为作者自报（author-reported），来源标注见每节。arXiv / HF / github.io 无法直连，信息来自：已 clone 的官方 repo（README、docs、项目页 HTML/JS 源码、图表图片）、JSON 中截断的摘要、少量 WebSearch（二手聚合站，标注为 `+search`，数字可信度低于 repo）。**没有任何一篇拿到论文 PDF 全文**（所有 repo 都不含 PDF），所以 `repo-pdf-fulltext` 标签一次也没用。repo 中项目页源码里的表格数据（Trace2Env、Sharpening Tax、TerminalHorizon）和 repo 自带的论文表格截图（SRD、VeriHarness）是质量最高的二级来源。
>
> 读者画像：在给 browser / computer-use agent 搭建 agentic-RL 环境的人。

---

## 必读 Top-6（按对"做 browser/CUA 的 RL 环境"的价值排序）

1. **[CodeMidas](https://arxiv.org/abs/2609.22068)**（Xiaomi MiMo，2609.22068）：把环境构建本身做成 agentic pipeline（agent 写 spec → 基于执行写测试 → 重复 rollout 过滤），只需"源代码"这一种输入就扩到 5,545 个任务 / 3,185 个仓库，在 MiMo-V2.5 上用 GRPO 涨了 DeepSWE、ProgramBench、Terminal-Bench。这套"环境合成 + 独立求解验证"的模板可以直接迁移到 web 任务合成。
2. **[GAGAR](https://arxiv.org/abs/2609.32577)**（Xiaomi MiMo，2609.32577）：在 1T 量级 MoE 上做的"组内 agentic grader 排序 + 保总和的 advantage 重分配"。它直接回答"二值 outcome reward 下，GRPO 怎么区分好的成功和差的成功"，是 grader 设计里最可落地的一篇。
3. **[Trace2Env](https://arxiv.org/abs/2610.06100)**（NTU，2610.06100）：只靠历史交互 trace 重建一个有状态的环境替身（worldbook + world-model agent + harness 校验与提交 state）。论文评测覆盖了 Web 和 Android，还专门测了"在模拟器里学到的动作序列回放到真实环境是否仍然有效"（W2R）。代码完整，对没法 self-host 的网站很有用。
4. **[SRD](https://arxiv.org/abs/2610.08077)**（Salesforce，2610.08077）：用 hindsight 监督 foresight，即使组内 reward 全相同（GRPO 拿不到梯度）也能产生 dense 信号。ALFWorld/WebShop 上有增益，基于 miles/slime 栈开源。稀疏 reward 的 web 任务在早期大部分组都是 all-fail，这类场景里 SRD 很关键。
5. **[VHD-Play](https://arxiv.org/abs/2609.27321)**（Qwen，2609.27321）：先采样并求解一个数学机制，再把它"渲染"成带状态的工具环境，所以环境 dynamics 和打分 reference 来自同一个已求解模型，天然 verifiable。每个环境只花几美分，Qwen3.6-35B-A3B 的诊断分数从 0.204 提到 0.815。它提供了"先定 reward 再造环境"的反向思路。
6. **[Sharpening Tax + PTGS](https://arxiv.org/abs/2610.01509)**（Meta MSL，2610.01509）：在 BFCL/WebShop/ACEBench 上证明 post-training 会把任务推向"总能解"或"永远解不了"两个极端，损失 pass@k coverage。PTGS 是一个按 prompt 难度自适应采样温度的即插即用 sampler（有代码），对决定 RL 训练里怎么做 exploration、怎么挑评测指标都有直接价值。

（第 7–8 名：[VeriHarness](https://arxiv.org/abs/2610.00972)，适合当长程 workspace 任务的 grader 设计参考；[TerminalHorizon](https://arxiv.org/abs/2610.13166)，环境合成思路好，但只做了 SFT。）

## 跨论文趋势（4–6 条）

1. **环境合成从"挖开发工件"转向"agentic 构建 + 独立挑战验证"**。[CodeMidas](https://arxiv.org/abs/2609.22068)（从实现的功能反推 spec/测试）、[TerminalHorizon](https://arxiv.org/abs/2610.13166)（独立执行发现"构建时被偷偷完成的关键工作"后再重建环境）、[Marathoner](https://arxiv.org/abs/2609.34378)（把多个任务串成 Multi-Task Chaining）、[VHD-Play](https://arxiv.org/abs/2609.27321)（先求解机制再渲染环境）。共同模式是：生成器 agent → 独立的求解/挑战 agent → 用重复 rollout 的通过率过滤，避免环境泄题、过易或不可解。这套模板对 web 任务合成同样适用。
2. **在 GRPO 组内二值 reward 之外"再挖信号"**。[GAGAR](https://arxiv.org/abs/2609.32577) 在通过的轨迹之间按质量重分配 advantage；[SRD](https://arxiv.org/abs/2610.08077) 从 reward 完全相同的组里用 hindsight→foresight 蒸馏拿信号；[PTGS](https://arxiv.org/abs/2610.01509) 用温度把难题的通过率推向 ½，从而制造 mixed group；[Marathoner](https://arxiv.org/abs/2609.34378) 加了 Later Stage Bonus Reward；[Taste-Bench](https://arxiv.org/abs/2609.25804) 用"分叉点 + 事后结果"做 step 级标签。核心问题都是 credit assignment 和 reward contrast 稀缺。
3. **Grader 本身 agent 化，并且越来越重视防 reward hacking**。[GAGAR](https://arxiv.org/abs/2609.32577) 用的是 SFT 过的 agentic grader，在共享 workspace 里联合检查整组轨迹；[VeriHarness](https://arxiv.org/abs/2610.00972) 用 disagreement resolver + consensus challenger 从环境取证；MiMo 的开源 rollout 框架 [mimoagent](https://github.com/XiaomiMiMo/mimoagent) 内置 rubric judge-agent、只在打分时才 apply 隐藏测试、截断 git 历史，还带一个可选的 anti-hack 动作拦截器。"LLM-judge 打一个分"正在演变成"带工具、能取证的 grader agent"。
4. **Hindsight 成为通用监督源**。[SRD](https://arxiv.org/abs/2610.08077)（hindsight 蒸馏进 foresight）、[Taste-Bench](https://arxiv.org/abs/2609.25804)（后续轨迹为分叉点打标签）、[Trace2Env](https://arxiv.org/abs/2610.06100)（历史 trace 变成 worldbook）、[PoS](https://arxiv.org/abs/2610.01415)（显式 belief + 陷入检测）都在利用"轨迹后半段揭示了前半段该怎么做"这一点。
5. **万亿级、训推分离的异步 RL 基础设施里，瓶颈转向"训推一致性 + 权重同步"**。[NeMo-DCR](https://arxiv.org/abs/2610.08430) 做 bit-exact 的稀疏 delta refit（每步约 1% 权重变化），[TRACE](https://arxiv.org/abs/2610.07767) 让 FP4 rollout 和 FP4 训练的量化取整对齐以压低 train-rollout mismatch。两篇都把 train/rollout 不一致当成一等问题。[GAGAR](https://arxiv.org/abs/2609.32577) 本身就跑在 310B/1.02T 的 MiMo-V2.6 上，说明工业界 agentic RL 已经进入 T 级参数。
6. **"长程"的定义升级到小时级 / 上千次工具调用**，但评测越来越依赖自建任务。[TerminalHorizon](https://arxiv.org/abs/2610.13166) 的 RSI-Exam 每个 case 给 12 小时预算；[Marathoner](https://arxiv.org/abs/2609.34378) 自称能连续工作 10 小时以上、做 1000+ 次工具调用；[Taste-Bench](https://arxiv.org/abs/2609.25804) 测的是长程决策品味。主流公开 benchmark 是 Terminal-Bench 2.x、DeepSWE、SWE-bench Pro。自建 benchmark 和合成数据的污染风险需要格外留意。

---

# 逐篇笔记

### CodeMidas: Scaling Agentic Coding RL Environments from Code Itself
arXiv 2609.22068 · 2026-09-21 · Xiaomi MiMo（搜索结果称有北大等合作方）· HF 98↑ · [arXiv](https://arxiv.org/abs/2609.22068) · [HF](https://huggingface.co/papers/2609.22068) · 项目页 https://mimo.xiaomi.com/rl/（不可达）· 论文本身无 repo；MiMo 官方 rollout 框架 [XiaomiMiMo/mimoagent](https://github.com/XiaomiMiMo/mimoagent) 可作为工程背景参考

**Source:** `abstract-only` + `+search` + `repo-readme`（mimoagent 仅作背景，**并非**本文代码）

**TL;DR:** 只把"源代码"作为任务输入，由 agent 在环境构建的每一步投入算力（探索功能 → 写行为 spec → 基于原代码执行结果写测试 → 执行检查 + 多次求解 rollout 过滤），把已有的功能实现批量转成可执行、可验证的 coding RL 环境。用 GRPO 训练 MiMo-V2.5 后，五个 benchmark 全部提升。

- **Problem:** SWE-smith、SWE-Gym、SWE-rebench 一类流水线依赖 issue/commit/PR 这类开发工件，可抽取的任务受限于有没有"有记录的改动"，而且大多是 bug fix 类型。
- **Method（就摘要所知）：**
  - 输入只有一个代码仓库，不需要 issue 或 PR。
  - agent 先探索仓库里"已实现的功能"，写成 behavioral specification；推测是把该功能挖空或移除，再让 policy 重新实现。
  - 测试 grounded in execution of the original code：用原始实现的执行结果当 oracle 生成测试。
  - 过滤分两层：执行检查（测试在原实现上通过、在挖空版本上失败，这是推测）+ repeated solution rollouts（多次求解，以难度和可解性筛选）。
  - RL 算法是标准 GRPO，摘要里没提有算法改动。
- **Environments/data:** 5,545 个训练任务，来自 3,185 个开源仓库，覆盖 23 种语言、15 个技术领域。"每个仓库不到 2 个任务"说明筛选很严，或者每个仓库只取一个功能。
  - 工程背景（mimoagent，**不能确认就是本文所用**）：其 `opensource-code` 数据类型约定"隐藏测试 + verifier 脚本都放在 `test_patch` 里，只在打分时 `git apply`"。打分前先把 patch 触及的路径 reset 回 base；镜像里 git 历史截断到 base commit，防止 agent 从 `git log` 读到参考答案。框架还有一个默认关闭、正则为主的 anti-reward-hacking 拦截器，会阻止"抓上游源码 / 读评测文件"一类动作，并返回假观测，而不是直接终止 rollout。这些细节和 CodeMidas"从源代码挖任务"的威胁模型高度相关（参考答案就在上游仓库里）。
- **Key results（作者报告，基座 MiMo-V2.5，GRPO）：**
  - DeepSWE +11.7%，ProgramBench +17%，Terminal-Bench v2.1 +8.5%。摘要原文写的是"%"，**是绝对点数还是相对提升无法确认**。
  - 五个 benchmark 中另外两个的名字在截断的摘要里看不到。
  - 消融显示高质量任务数越多越好；轨迹分析显示训练后探索代码库更多，自我验证也更多样。
- **What's new:** 相对 SWE-smith（合成 bug 注入）、SWE-Gym/SWE-rebench（真实 issue），CodeMidas 的任务来源是"已实现功能"，覆盖 whole-program construction 这类非修 bug 任务。相对 R2E-Gym 一类"从 commit 反推"的方法，它不需要任何历史工件。核心新意在于"环境构建全流程 agentic 化 + rollout 过滤"，RL 算法本身不新。
- **Reputation check:** Xiaomi MiMo 核心团队（Fuli Luo、Lingpeng Kong 等），HF 98↑。红旗有三条：没有代码和数据 release；ProgramBench、DeepSWE 都比较新；从开源仓库"重新实现已有功能"存在**严重的记忆和污染风险**，模型可能在预训练时就见过原实现。
- **Limitations：**
  - 作者提到的：未知（只有摘要）。
  - 我的看法：
    - 测试 oracle 来自原实现，原实现有 bug 也会被当成"正确行为"。
    - 只适用于可执行、可测的代码功能。
    - 增益是相对 MiMo-V2.5 自身的，不清楚和 SWE-smith 等数据在等量预算下的对比。
- **Relevance（browser/CUA env）：**
  - 可以直接借鉴"从现成产物反推任务"：把网站或应用中已实现的功能流程挖成任务，用原系统的执行结果当 oracle，再用多次 rollout 的通过率过滤难度。
  - mimoagent 的防泄题设计（隐藏 verifier 到打分时才注入、截断历史、拦截可疑动作并返回假观测）可以直接搬到 web 环境，例如禁止访问"答案页面"。
- **Verdict：必读**：这是本月环境合成方向最有代表性的工业界工作，pipeline 设计可迁移；但需警惕没有 release、只有自报数字。

---

### Groupwise Agentic Grading and Advantage Redistribution for Code Agent RL (GAGAR)
arXiv 2609.32577 · 2026-09-29（alphaxiv 显示 9-26 提交）· Xiaomi MiMo（+人大/北大）· HF 111↑ · [arXiv](https://arxiv.org/abs/2609.32577) · [HF](https://huggingface.co/papers/2609.32577) · 无 repo

**Source:** `abstract-only` + `+search`

**TL;DR:** 二值测试 reward 下，GRPO 给组内所有通过的轨迹同样的 advantage。GAGAR 让一个 SFT 过的 agentic grader 在共享 workspace 里联合检查整组轨迹，给通过者按质量排序，然后降权低排名者，并按比例缩放所有通过者的 advantage，使总和不变。

- **Problem:** 通过测试的实现之间存在质量差异（是否干净、是否有越界改动、是否遵循需求），binary reward 看不到这些差异。结果是 policy 缺少"偏好干净、聚焦实现"的信号，轨迹长度也会持续膨胀。
- **Method：**
  - 先做 dynamic sampling（与 DAPO 一致），只保留既有通过又有失败的组。
  - 把组内**所有**轨迹的最终 workspace 放进一个共享 workspace。SFT 训练过的 agentic grader 联合检查（搜索摘要称它能读代码、跑有针对性的检查），对通过的候选排名。
  - 按排名降权低质量的通过者，再把所有通过轨迹的 advantage 按比例缩放回原来的总和（sum-preserving redistribution）。我的推断形式：设原始正 advantage 为 A⁺、通过数为 k、权重为 w_i，则 A'_i = A⁺·k·w_i / Σ_j w_j。失败轨迹的 advantage 不变，所以"成功 vs 失败"的总推力不变，只是在成功者之间转移 credit。
  - 二手来源提到：若确认轨迹依赖了外部解（抄上游代码），该轨迹 reward 重置为 0，再重新计算组统计量。这是 reward hacking 防护（**未经原文核实**）。
- **Environments/data:** code agent 任务（推测是 MiMo 内部 SWE 类数据，可能和 CodeMidas 同源）。grader 先用 SFT 训练，数据构造方式未知。
- **Key results（作者报告）：**
  - 基座是 MiMo-V2.6-Flash（310B total）和 MiMo-V2.6-Pro（1.02T total）的 pre-RL SFT checkpoint。
  - 在只做 code、只用 Flash 的受控实验里：code agent 性能提升、轨迹长度增长变慢、训练更稳定。
  - 也用在了两种模型的大规模混合任务 RL 里。
  - 摘要截断处之后的具体数字**拿不到**。
- **What's new:**
  - 相对 GRPO、DAPO：不改目标函数，只在"通过者内部"重新分配 credit，而且保持总和，不会改变正负样本之间的平衡。
  - 相对 rubric/LLM-judge 混合 reward（直接把 judge 分数加到 reward 里）：groupwise 的联合比较加上 agentic 检查，比逐条打绝对分更稳，也更难被 hack。
  - 相对 RM 当 reward：grader 只决定"成功者之间的排序"，不能把失败变成功，降低了被 reward hacking 的面。
- **Reputation check:** 与 CodeMidas 同一团队，HF 111↑，且在 1T 级生产模型上验证。红旗：无代码；grader 的 SFT 数据和准确率未知；"质量"的定义可能带有 MiMo 内部偏好。
- **Limitations：**
  - grader 推理成本高：每组都要额外跑一次 agentic 检查。
  - grader 的偏差会被 RL 放大。
  - 只作用于 mixed group：all-pass 的组被 dynamic sampling 丢掉了，而这些组恰恰最需要质量区分。这是我推断出的一个潜在缺口。
- **Relevance（browser/CUA env）：**
  - web 任务也常有"完成了，但多点了无关按钮、改了别的设置、走了很长的弯路"的情况。可以用 groupwise 视觉/DOM grader 给成功轨迹排序，再按保总和的方式重分配 advantage，以此抑制副作用和冗余操作。
  - "grader 只能在成功者之间排序"是很好的 reward-hacking 安全阀。
- **Verdict：必读**：这是本月 credit assignment 和 grader 设计最实用的工业级方案，思路简单、可复现。

---

### Verifiable Hidden Dynamics Play: Generating Agentic RL Environments from Solved Mechanisms (VHD-Play)
arXiv 2609.27321 · 2026-09-24 · Qwen（Dayiheng Liu 组）· HF 8↑ · [arXiv](https://arxiv.org/abs/2609.27321) · [HF](https://huggingface.co/papers/2609.27321) · 无 repo

**Source:** `abstract-only` + `+search`（搜索只补充了 related-work 定位，没有补到新数字）

**TL;DR:** 反转常规流水线：先采样一个数学模型（机制）并求解，再由一个 corpus-grounded 的 setter 把它的决策过程渲染成有状态的工具。这样可执行的 dynamics 和轨迹打分的 reference 都继承自同一个已求解模型，天然可验证。

- **Problem:** 现有环境生成流水线（EnvScaler、AgentScaler、各种 tool/world-model 合成）先造环境，再定义结局规则或标注轨迹，dynamics 和评测只能事后对齐，容易出现不可解、无法验证、打分不一致的问题。
- **Method：**
  1. 采样一个带隐藏参数的数学机制，例如库存/定价/资源分配这类序贯决策模型，并求出最优策略或最优值。
  2. setter LLM 基于语料把机制"包装"成真实场景下的 stateful tools，参数隐藏，agent 必须靠交互去发现。
  3. 轨迹按与已求解最优解的差距打分（trajectory-scoring reference）。
  - 摘要没提用了什么 RL 算法。
- **Environments/data:** 3,300 个环境，每个"几美分"。训练只用了 3 个 family；诊断集有 5 个 family，另有 8 个 unseen mechanism family。作者对比了三种版本：写成文字题、参数公开的有状态版、参数隐藏的有状态版。
- **Key results（作者报告）：**
  - Qwen3.6-35B-A3B 在五 family 诊断上的平均 agentic score 从 0.204 升到 0.815。
  - 增益覆盖训练 family 的 held-out 实例和 8 个 unseen family，并迁移到外部 benchmark（通用 function calling、旅行规划、365 天电商）。
  - 在 E-Commerce Bench 上，训练后的 checkpoint 每次运行都没有破产，并超过了 Qwen3.7-Max。
  - 对比实验显示，"大部分可学的差距在有状态交互，而不在底层问题求解"。
  - frozen 35B setter 的结论被摘要截断了。
- **What's new:** 相对 Reasoning Gym / LEGO 式可验证环境（只验证答案）、TextArena/PDDL（固定 spec），以及 EnvScaler 一类的 tool/world-model 合成，VHD-Play 的新意是"先有可解机制，后有环境"，reward 不需要 LLM judge。
- **Reputation check:** Qwen 团队，但 HF 只有 8↑，关注度低。没有代码。0.204→0.815 是在自建诊断集上的结果，属于 in-distribution 或近分布。外部 benchmark 的具体数字没拿到。
- **Limitations：**
  - 机制只限于能写成数学模型并求解的类型，比如运筹和经济决策。开放式 web 任务很难先写出可解机制。
  - setter 渲染出来的"真实感"有限，可能出现 sim-to-real gap。
- **Relevance（browser/CUA env）：**
  - 对需要长期状态的业务场景（电商后台、库存、预算、日程）可以先定义隐藏参数的 dynamics 和最优解，再生成一个 web 前端或工具接口当环境。这样 reward 精确，还能控制难度。
  - "参数隐藏 vs 公开"这个对照实验，是很好的诊断手段：用来区分 agent 是不会探索，还是不会求解。
- **Verdict：必读（偏方法论）**：关注度低，但"先 reward、后环境"的思路对环境构建者很有启发；只是证据薄（只有摘要）。

---
### Self-Retrospection Distillation: Turning Post-hoc Experiences into Prior Foresight (SRD)
arXiv 2610.08077 · 2026-10-08 · Salesforce AI Research（+UCSD/TAMU/Stanford；Savarese、McAuley、Chien-Sheng Wu）· HF 88↑（README 称 HF Daily #1）· [arXiv](https://arxiv.org/abs/2610.08077) · [HF](https://huggingface.co/papers/2610.08077) · repo [SalesforceAIResearch/SRD](https://github.com/SalesforceAIResearch/SRD)（JSON 中没有，是我找到的）

**Source:** `repo-readme`（README、`docs/srd/ablations.md`、repo 自带的 Table 1 和方法图截图）+ 摘要

**TL;DR:** 提出 prospective learning：policy 在交互前先生成 foresight（"我可能需要的知识 / 我可能遇到的坑"）。用"看过完整轨迹和 verifier 反馈的 self-teacher"的分布去蒸馏这段 foresight。这样即使组内 reward 全相同，也能拿到 dense 的 token 级信号。SRD 作为辅助损失叠加在 GRPO、OPSD、RLSD 上。

- **Problem:** GRPO 一类 group-relative 目标在 reward-uniform 组（全对或全错）里 advantage 为 0，信号完全消失。作者统计在不同模型规模下有 37–98% 的组是 uniform 的。
- **Method（来自方法图和 ablation 文档）：**
  - Student policy π_θ(·|x,e) 以任务 x 和环境信息 e（工具 schema、提交格式、ALFWorld 房间状态等）为条件，先生成 foresight z^fore，内容分两段：Knowledge/Rule/Example 和 Pitfall/Rule/Example。
  - 正常 rollout 后，用 verifier 结果（错误类型：超长、格式错误、测试失败数等）加上自我 retrospection，从正确轨迹提取"有用知识"、从错误轨迹提取"坑"，得到 hindsight f。
  - 目标：L_SRD = D( stopgrad(π_θ̄(·|x,e,f,z^fore_<l)) ‖ π_θ(·|x,e,z^fore_<l) )，对 foresight 的每个 token 计算。teacher 是 EMA self-teacher（rate 0.05），能看到 hindsight f；student 看不到。
  - 系数默认 `skill-kd-coef 0.01`。推理时**不需要**生成 foresight。
  - 消融 arm：a = baseline，b = 只用正确轨迹的 hindsight，c = 只用 pitfall，d = 两者都用，e = SRD，f/j 为 blind-teacher 变体。
  - 三种宿主：`grpo`（task reward 走 GRPO，SRD 是正交的 KD 项）、`sdpo`/OPSD（JSD top-100 logprob 加性 KD）、`rlsd`（乘性 advantage 重加权）。
- **Environments/data：**
  - 数学用 DAPO-Math-17k，代码用 LiveCodeBench，搜索用 HotpotQA/2Wiki（FlashRAG retriever），agentic 用 ALFWorld 和 WebShop，每个领域 400 条。
  - 每个工具（code interpreter、search、WebShop、ALFWorld）各跑一个容器化 sidecar。
  - 训练栈是 radixark/miles（slime 系，Megatron + SGLang），enroot 启动，一个节点 8×H200。
- **Key results（作者报告，avg@8，Table 1）：**
  - Qwen3.5-4B-Thinking，GRPO → GRPO+SRD：Math 平均 46.22→56.25；Code 平均 36.85→45.18；Search 平均 48.29→56.34（BrowseComp-Plus 13.25→22.77）；ALFWorld 67.75→71.00；WebShop 77.21→83.13。
  - Qwen3.5-4B，OPSD → OPSD+SRD：ALFWorld 52.88→66.62，Search 平均 42.62→52.85。
  - Qwen3.5-9B，GRPO+SRD：Math 平均 55.06→64.61，WebShop 78.06→84.18。不过 9B 的 OPSD+SRD 在 WebShop 上 −3.61，RLSD+SRD 在 4B 的 OJBench 上 −0.97，增益并非处处为正。
  - 摘要："最高 +24.2 pp"（对应 9B OPSD 在 AIME26 上的 +24.16）。2B 规模下 98% 的组是 all-failure，GRPO 最终为 0.0%，加 SRD 达到 60.6%（同等 rollout 预算）。
- **What's new:**
  - 相对 OPSD/SDPO/RLSD 一类 retrospective self-distillation（teacher 用 hindsight 来锐化**下一个动作**），SRD 用 hindsight 监督的是**交互前的预判**。
  - 相对 Hindsight Experience Replay 和 hindsight relabeling，SRD 不改 reward，而是把经验蒸馏到"计划/先验"里。
  - 相对 Reflexion、ExpeL 一类在推理时用记忆，SRD 把经验内化到权重里。
- **Reputation check:** Salesforce 加 Savarese 和 McAuley，代码完整（可启动脚本 + 完整 ablation 参数），开源程度较高。红旗：基线是作者自己实现的 OPSD/RLSD；所有数字是 avg@8 的单次训练，没有报方差；BrowseComp-Plus 的评测流程依赖外部 repo。
- **Limitations：**
  - 增益在 Search 和 Math 上最大，在 agentic（ALFWorld/WebShop）上中等，而且有负例。
  - foresight 的生成和 retrospection 都带来额外训练开销。
  - 环境信息 e 需要人工写好。
  - hindsight 的质量依赖 policy 自身。
- **Relevance（browser/CUA env）：**
  - web/CUA 的 RL 早期通常是大片 all-fail 组，SRD 是让这些组产生梯度的现成方案。环境侧需要提供结构化的失败反馈（错误类型、哪个检查没过），这正是 hindsight f 的原料。
  - WebShop 上 +5.9（4B GRPO）和 +6.1（9B GRPO）是直接证据。
- **Verdict：必读**：开源完整，能直接用来对付稀疏 reward，对环境 feedback 设计也有指导意义。

---

### From Traces to Agentic Worlds: Agentic Language World Models for Interactive Environment Simulation (Trace2Env)
arXiv 2610.06100 · 2026-10-09 · NTU Singapore（Wenya Wang 组）+ PolyU · HF 98↑ · [arXiv](https://arxiv.org/abs/2610.06100) · [HF](https://huggingface.co/papers/2610.06100) · repo [ruyue0001/trace2env](https://github.com/ruyue0001/trace2env) · 项目页 https://quanyulong.net/trace2env/（源码在 repo 的 `docs/index.html`）

**Source:** `repo-readme`（README、REPRODUCING.md、项目页 HTML 中的完整结果表）

**TL;DR:** 不重建可执行环境，而是让一个 world-model agent 充当环境。它从几十条历史 trace 离线重建出 worldbook（schema、规则、约束、观测契约、grounded evidence、示例），在线时主动查 worldbook、episode state 和 episodic memory 来预测观测和持久的状态变化，再由 harness 校验并提交 state。整个方法 learning-free。

- **Problem:** 原系统不可得（私有、遗留、难部署）时怎么得到能用于训练和评测的环境替身。传统 prompt 式 LWM 把描述、历史、动作塞进一个 prompt，不维护状态，长程一致性差。典型问题是"`rm` 文件后很多轮再 `cat` 应该失败"。
- **Method：**
  1. 离线重建：对齐 action–observation，保留原观测作为证据，归纳 action/state schema，推导规则、约束、不变量、response contract 和 provenance。worldbook 用 GPT-5.6-Sol 构建。
  2. 运行时：world-model agent 有选择地读取相关知识（Applicability Gate 按文件路径、web 页面或 Android 屏幕选择证据），提出 state effects 和 next observation；harness 按 schema、约束校验后提交，被拒绝的 effect 不写入。
  - 构建成本：terminal 约 $27，web 约 $19，android 约 $154（15 个 worldbook），swe 约 $340（10 个）。
- **Environments/data：**
  - 单轮评测用 AgentWorldBench（Qwen 发布）的 terminal/swe/android/web split，加上 EnvScaler 的 Food/Shopping/Benefits。
  - 多轮评测用 ALFWorld 和 SciWorld。
  - trace 来源：Terminal-Bench 2.0 共 20+16 条，WebArena 50 条（经 Playwright MCP 采集），Android 和 SWE 用 k=5 cross-fit。
  - 裁判是 GPT-5.2（AgentWorldBench 官方五维 judge）。
- **Key results（作者报告，项目页表格）：**
  - 单轮 next-observation 保真度（0–100），GPT-5.6-Sol 骨干：Direct Prompting 平均 69.51 → Trace2Env 75.94。分环境：Terminal 55.76→65.42，SWE 65.87→70.59，Android 62.80→65.10，Web 54.23→59.55。
  - 但 Trace RAG Prompting（73.76）和 Worldbook Prompting（74.35）也是强基线；Android 和 Shopping 上 Trace2Env 不是最好（Android 66.50 来自 Trace RAG）。
  - DeepSeek-V4.1-Flash 骨干：平均 68.71→75.75。
  - 多轮一致性：ALFWorld 上 Direct Prompting 的 WM 成功率 97%，但回放到真实环境（W2R）只有 3%（CR 0.032）；Trace2Env 的 WM 88%、W2R 85%（CR 0.914）。SciWorld 上 CR 0.529→0.706。
  - 消融（Terminal）：grounded evidence 的贡献最大（+2.45±0.89）；单独加 abstraction 反而 −1.12，与 evidence 组合后才有正贡献。
- **What's new:**
  - 相对 AgentWorldBench 的 prompt 式 LWM、Word2World、WebDreamer / web world model，Trace2Env 把"模拟"本身做成 agentic 任务，加了显式持久状态和 harness 校验。
  - 相对 EnvScaler / AgentScaler 的代码化环境合成，它不需要写出可执行代码。
  - W2R/CR 这个指标非常有价值：它直接衡量"在模拟器里学到的东西在真实环境是否成立"。
- **Reputation check:** NTU 学术组，代码完整，有 285 个测试和 HF demo；REPRODUCING 写得很坦诚，承认每个数字都是单次运行，结果早于 2026-10-08 修复的一个 state-path bug（terminal 上有 6–19% 的 mutation 被丢掉），而且除 Terminal 外的 worldbook 和 trace 都要"按需索取"。红旗：多轮实验只在 ALFWorld/SciWorld 这类文本游戏上做，样本小；没有拿 world model 去**训练** RL agent。
- **Limitations：**
  - 只适用于文本观测，没做截图。
  - 每一步都要调用一次大模型 agent，作为 RL rollout 环境吞吐低、成本高。
  - LLM judge 评估保真度本身有噪声。
  - trace 覆盖不到的行为只能靠归纳，容易产生幻觉。
- **Relevance（browser/CUA env）：**
  - 对无法 self-host 的网站或内部系统，可以用几十条 Playwright 交互 trace 建一个有状态的文本替身，用于 SFT 数据扩增、离线 RL 或安全测试。W2R 回放评估应当成为任何 sim 环境的必测项。
  - harness 校验 + 持久 state 的架构，可以给"LLM 模拟的 web 后端"（mock API）防漂移。
- **Verdict：必读**：这是本月"环境替身 / world model as env"方向最扎实的开源工作，Web 和 Android 都有评测。

---

### Sharpening Tax in Post-Training
arXiv 2610.01509 · 2026-10-02 · Meta Superintelligence Labs + UW-Madison（Sharon Li）+ NYU + Stanford（Azalia Mirhoseini）· HF 69↑ · [arXiv](https://arxiv.org/abs/2610.01509) · [HF](https://huggingface.co/papers/2610.01509) · repo [changdaeoh/sharpening-tax](https://github.com/changdaeoh/sharpening-tax) · 项目页源码在 `docs/`

**Source:** `repo-readme`（README、PTGS 文档、项目页 HTML/JS 中的数据）

**TL;DR:** 带轻量文本 harness 的 base model 本身就是可用的 agent，在大 K 下 pass@k 往往超过它的 post-trained 版本。post-training 把任务推向"永远能解"或"永远解不了"两个极端。作者提出 Sharpening Tax 指标量化这种损失，并提出 PTGS（按 prompt 难度自适应采样温度）在 RL 里少交税。

- **Problem:** "RL 只是锐化"假说（Yue et al. 2025 的 pass@k 争论）此前只在 math/code 上验证。agentic 任务需要多轮工具交互，一般被认为是 post-training 新教会的能力，那它是否也只是锐化？
- **Method：**
  - 14 对 base/post-trained checkpoint（4 个家族：Gemma 4 31B、Qwen2.5-32B、Qwen3.5-35B-A3B、Ministral-3-14B 等），3 个 benchmark（BFCL v4 multi-turn、WebShop、ACEBench），每任务 128 次 rollout，共 42 个 case。
  - Sharpening Tax：A(K)=Σ_{k=1}^{K−1}[pass@K − pass@k]，S(K)=A(K)/[(K−1)(1−pass@1)]，Tax_S = S_base − S_post。
  - PTGS：每个 prompt 维护一个折扣 Beta 后验（γ=0.95），抽样得到 p̂ 后设温度 T=τ·h(p̂)：p̂ 低于 pivot 时升温，高于时降温；pivot 从 0.25 线性 ramp 到 0.5。
  - PTGS 的三个关键实现细节：任务池有限且循环使用；后验必须在 reward-variance 过滤**之前**更新；log-prob 要在该 prompt 自己的采样温度下计算。
- **Key results（作者报告）：**
  - 42 个 case 中有 36 个 Tax_S(128)>0。
  - 项目页默认例子（Gemma 4 31B，WebShop，500 任务×128 次）："有时能解"的任务比例从 87.6% 降到 30.0%。
  - PTGS（Qwen2.5-7B-Instruct，5 次运行取均值，最终 PPO checkpoint）：
    - Sokoban·PPO：pass@1 46.5→61.1，pass@128 55.0→69.7，Tax_S 0.094→0.081。
    - Sokoban·GRPO：pass@1 36.5→39.1，pass@128 55.3→72.5。
    - FrozenLake·PPO：pass@1 63.7→65.0，pass@128 74.1→80.0。
- **What's new:**
  - 把 pass@k 锐化争论扩展到多轮 agentic 任务，并给出一个可以从少量 rollout 估计、能把 coverage 损失量化的指标。
  - PTGS 相对固定温度和 entropy bonus 的区别是按 prompt 难度给出温度；相对 DAPO 的 dynamic sampling，PTGS 是主动"制造" mixed group，而不只是过滤。
- **Reputation check:** Meta MSL 和知名学者，有代码（metrics 和 PTGS 能在 CPU 上跑）。但 repo 明确写着"不是复现包"，RL 训练基础设施留给用户（示例接 RAGEN/verl 风格）。PTGS 只在 Sokoban/FrozenLake 这类玩具环境上用 7B 模型验证，**没有在 WebShop/BFCL 上做 RL 训练**。License 是 CC BY-NC。
- **Limitations：**
  - Tax 为正可能只是"更快饱和"，不一定是 coverage 丢失（作者也承认这一点）。
  - base model 需要 harness 才能当 agent，harness 的设计会影响结论。
  - PTGS 证据规模小。
- **Relevance（browser/CUA env）：**
  - 评测 web agent 的 RL 时，应同时报 pass@1、pass@k、pass^k。"sometimes solved"任务的比例可以当作环境难度和训练健康度的监控指标。
  - PTGS 实现成本很低（每个 prompt 一个 Beta 后验），适合 web 任务池有限、需要循环使用的场景。
- **Verdict：必读**：诊断工具加一个即插即用的 sampler，对 RL 训练策略和评测都有直接启发。

---
### VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks
arXiv 2610.00972 · 2026-10-05 · Google（Cloud AI Research，Tomas Pfister / Chen-Yu Lee 组，+Cambridge Nigel Collier）· HF 48↑ · [arXiv](https://arxiv.org/abs/2610.00972) · [HF](https://huggingface.co/papers/2610.00972) · repo [google-research/veriharness](https://github.com/google-research/veriharness) · 项目页 https://veriharness.com/ · 数据 HF `caiqizh/veriharness`

**Source:** `repo-readme`（README 加 repo 自带的结果图）

**TL;DR:** 不依赖参考答案或 rubric，把生成器同款 LLM 放进一个"verifier harness"：给它 workspace、取证工具和可复用的 verification skills。对 N 条 rollout 中**有分歧**的 claim，由 resolver 用环境证据排除；对**一致**的 claim，由 challenger 主动证伪。最后 adjudication 选出 base，并基于证据修订产物。

- **Problem:** 长程 workspace 任务（报告、表格、文档包）的产物难以验证。Best-of-N 加 LLM-as-judge 依赖 judge 的能力，而同一模型的 rollout 共享盲点，"一致"不等于"正确"。
- **Method：**
  - 一个任务跑 4 个模型 turn，分在 3 个相互隔离的 session 里：resolver 和 challenger 并发且互不可见，各写一个 ledger；adjudication 在新 session 里读两份记录、任务和 rollouts，输出 `{base, work[], open[]}`；delivery 在同一 session 中执行修订计划。
  - selection、revision、reconstruction 由同一个开关控制：`base:"none"` 表示从头重建。
  - 程序只负责搬文件，"查什么、何时停"都由模型决定。
  - skills 库：`evidence-*`（xlsx/pdf/docx/pptx 读取与比对脚本）、`resolve-*`、`falsify-*`、`repair-*`。
  - 运行在 mount-namespace jail 里，archived 分数和答案都不可见。
  - verification skills 可以根据失败反馈自我改进。
- **Environments/data:** 5 个 benchmark：APEX-Agents、Workspace-Bench Lite、WorkBuddy Bench、SpreadsheetBench 2、JobBench。用的都是 benchmark 自带的 grader，其中 3 个是 LLM judge。rollout 池约 26,000 条（Gemini 3.5 Flash 和 Claude Opus 4.8，每任务 10 条），已开源。
- **Key results（作者报告，Gemini 3.5 Flash 同时作生成器和 verifier，single rollout → 先前最好的 LLM-as-a-Verifier → VeriHarness）：**
  - APEX 48.1 → 49.8 → 54.8
  - WSB 56.5 → 60.4 → 65.4
  - WorkBuddy 73.2 → 75.3 → 78.2
  - SB-2 27.3 → 30.2 → 32.2
  - JobBench 30.9 → 31.9 → 36.2
  - 相对单条 rollout 的平均增益：Gemini 3.5 Flash +6.2，Claude Opus 4.8 +6.4。
- **What's new:**
  - 相对 LLM-as-a-Verifier、Best-of-N 加 RM、self-consistency：区分"分歧→排除"和"共识→证伪"两种验证模式，并主动去环境里取证。
  - 它是 verifier harness，不是更强的 judge。
- **Reputation check:** Google 加完整代码和数据，README 很诚实：承认后加的 `resolve-*` 等 skills 是根据**同一批 benchmark** 的失败分析写的，所以"不是对 skill 库的 held-out 测试"。这是一个泄漏风险点，好在作者主动披露了。3 个 benchmark 的打分依赖 LLM judge。
- **Limitations：**
  - 推理时成本高：每个任务 4 个 turn，每 turn 上限 1800s，任务上限 3600s。
  - 需要 N 条 rollout。
  - skills 偏向办公文件（xlsx/docx/pdf）。
  - 没有用于 RL 训练，只是 test-time 方法。
- **Relevance（browser/CUA env）：**
  - 可以作为长程 CUA 任务的 reward/grader 原型：用组内 rollout 的分歧定位待查 claim，再让 grader agent 回到环境里取证（读 DOM、查后台状态、重算数值）。这和 GAGAR 的 groupwise grader 思路互补。
  - jail 隔离（grader 看不到答案和分数）和"打分前做 preflight、judge 不可达就拒绝打分"这些工程细节值得照搬。
- **Verdict：值得浏览（偏必读）**：test-time 方法，但它对 agentic grader 的设计很有借鉴价值。

---

### The Tasteful Agent: Measuring and Improving Taste in Long-Horizon Tasks (Taste-Bench)
arXiv 2609.25804 · 2026-09-23 · Microsoft（Research Asia，Chin-Yew Lin、Yan Lu 等）+ CityU HK · HF 115↑ · [arXiv](https://arxiv.org/abs/2609.25804) · [HF](https://huggingface.co/papers/2609.25804) · repo [wbopan/tastebench](https://github.com/wbopan/tastebench) · 数据 HF `wenbopan/taste-bench`（gated）

**Source:** `repo-readme` + `+search`（训练部分的细节只来自二手搜索）

**TL;DR:** 把长程任务中的"品味"定义为在决策分叉点选择更好方向的能力。从并行尝试和单轨迹内的弯路中自动挖出分叉题（不需要人工标注），共 502 题，最强模型只答对 59.7%。随后用"看过结局的 teacher"去蒸馏"只看到分叉前信息的 student"，证明 taste 可以训练。

- **Problem:** 端到端成功率 benchmark 测不出中间决策的质量；长程任务里 credit assignment 的难点正是这些分叉点。
- **Method / 数据构造：**
  - Parallel forks：同一任务的独立尝试在同一位置分叉，用各自的最终结局标注哪个方向更好。
  - Detour forks：同一轨迹中，agent 走某方向失败后放弃再恢复，被放弃的方向和恢复后的方向作为两个候选。
  - 过滤：所有 judge 模型仅凭候选措辞就能答对的题视为 trivial，丢掉；任一 judge 读完完整记录后与标签不一致的题视为 undecidable，也丢掉。4,657 个分叉最后剩 502 个。
  - 题目来源：工程类 390 题（SWE-bench、SWE-bench Pro 的 rollout），研究类 112 题（METR MALT 的 RE-Bench、HCAST 运行记录）。
  - 评测协议：两种选项顺序都答对才算对，所以随机猜的期望是 25 分；分叉前的上下文最多 64K token，不允许输出可见的 CoT。
  - 训练（二手来源）：teacher 看到结局，student 只看到分叉前信息；在 Qwen3.6-27B 上用 LoRA 蒸馏；在 held-out SWE-bench Pro 任务上提升了端到端成功率。具体数字没拿到。
- **Key results（作者报告，README 排行榜）：**
  - GPT-5.6 Sol 59.7，GPT-5.5 59.5，Claude Opus 5 55.5，GLM-5.2 53.9，DeepSeek V4 Flash 43.3。
  - 决定性证据出现在轨迹越靠后的分叉越难；增大 reasoning budget 不提升准确率。
- **What's new:** 相对 SWE-bench 一类端到端评测、process reward model、PRM800K 式 step 标签，Taste-Bench 用"事后结局"自动标注 step 级决策，为长程 credit assignment 提供了 benchmark 和数据来源。
- **Reputation check:** MSR 加开源代码和数据（gated，有 canary 防污染），HF 115↑。红旗：502 题规模小，研究类只有 112 题；标签依赖"该方向的那次尝试最终成功"，存在混杂（成功也可能来自后续其他决策）。
- **Limitations：**
  - 二选一的形式过于简化。
  - 训练部分的证据有限，没拿到数字。
  - 只覆盖 SWE 和 ML 研究。
- **Relevance（browser/CUA env）：**
  - "从并行 rollout 和弯路中挖分叉点"可以直接用于 web 轨迹：同一任务的多条 rollout 天然产生分叉，用结局标注后，可以训练 step 级 critic/PRM，或者做 hindsight 蒸馏（和 SRD 互补）。
- **Verdict：值得浏览**：数据构造思路好，但主体是 benchmark，训练部分证据少。

---

### Scaling Agentic Data for Long-Horizon Terminal Intelligence (TerminalHorizon)
arXiv 2610.13166 · 2026-10-13 · Alibaba（AMAP 高德）+ USTC + SUSTech · HF 136↑ · [arXiv](https://arxiv.org/abs/2610.13166) · [HF](https://huggingface.co/papers/2610.13166) · 项目页源码 [zs1314/TerminalHorizon](https://github.com/zs1314/TerminalHorizon)（GitHub Pages，**不含代码**）

**Source:** `repo-readme`（项目页 HTML/JS 数据和 pipeline 图）+ 摘要

**TL;DR:** 一个全自动的长程 terminal 任务合成引擎。从真实的专业工作出发，由 Planner、Deep Research、Construction 三个 agent 构建任务；再用独立执行找出"构建时被预先完成或简化掉的关键工作"，据此重建环境；最后渐进地扩展任务视野。共合成 1,535 个环境，SFT Qwen3.5-27B，12 个 benchmark 全部提升。**只做了 SFT，没有 RL。**

- **Problem:** 环境合成常常"预先完成或简化"了 agent 本该自己做的探索、实现和验证工作（例如数据已经清洗好、脚手架已经写好），导致轨迹短、学不到长程行为模式。
- **Method（pipeline 图）：**
  - I. Challenge-Guided Long-Horizon Synthesis：Planner Agent 根据任务库和覆盖反馈找出缺失的专业目标和行为模式，产出 research brief。Deep Research Agent 做真实世界 grounding，产出任务种子、instruction 草稿和研究证据。Construction Agent 产出 Harbor 格式（`instruction.md`、`environment/`、`tests/`、`solution/`、`task.toml`）。Independent Challenge 只拿公开的 instruction 和环境去独立执行。Horizon Gap Analysis 比较"预期工作"和"实际执行"，定位核心工作在哪里丢失，然后重建并再次挑战。
  - II. Progressive Horizon Expansion：Evolution Agent 在同一目标下扩展角色、加深机制、补充证据、升级方法，形成 T⁰→T¹→T² 的依赖链。
- **Environments/data:** 1,535 个可执行环境，25 个专业领域，463 个子领域，27 种行为模式（5 大类）。2,852 条轨迹（共享 teacher 协议，teacher 是谁未知），平均 52.82 轮交互，P50 为 40，P90 为 98。
- **Key results（作者报告，基座 Qwen3.5-27B，SFT）：**
  - Terminal-Bench 1.0：46.3→55.0；2.0：41.6→55.8（base 分数取自官方 model card）；2.1：46.82→60.67。
  - AutomationBench pass rate 5.5→17.2；τ²-bench Airline 79.0→84.5，Retail 84.9→87.5；VitaBench 20.5→31.8；AIME25 86.7→93.3。
  - 数据量 scaling（TB2.1）：0→1000→2000→2852 条轨迹对应 46.82→57.3→58.43→60.67。
  - 模型规模：35B-A3B 从 39.7 到 52.81；122B-A10B 从 49.06 到 64.04。
  - RSI-Exam（自建，每个 case 12 小时预算）四个案例全部提升，例如点云融合 21.93→48.96。
- **What's new:**
  - 相对 TerminalTraj、RST（Recursive Synthetic Terminal Tasks，2608.05466）、SWE-smith、Endless Terminals 一类方法：显式检测"构建泄漏或简化"（horizon gap analysis），并做渐进视野扩展，目标是长轨迹，而不只是更多任务。
- **Reputation check:** HF 136↑（本批最高），阿里高德。红旗：
  - 没有代码和环境 release（项目页上的环境、轨迹、权重链接状态未知）。
  - teacher 模型身份未知，SFT 增益很可能主要来自蒸馏 teacher。
  - base 的 TB2.0 分数直接取自 model card，而不是作者在同一 harness 下复测的，对比不严谨。
  - RSI-Exam 是自建的，而且只有 4 个案例。
  - JSON 把它标为 agentic-rl，其实是 SFT 数据工作。
- **Limitations：** 没有 RL，没有和其他数据集在等量轨迹下对比（就项目页可见内容而言）；terminal 领域。
- **Relevance（browser/CUA env）：**
  - Independent Challenge 加 Horizon Gap Analysis 可以直接用来检查 web 任务合成时"环境是否预先做掉了关键步骤"，例如预填表单、预登录、数据已经整理好。
  - 渐进视野扩展（同一目标下叠加新需求）是构造长程 web 任务的好方法。
- **Verdict：值得浏览**：环境合成的方法论值得学，但它是 SFT 工作，可复现性弱。

---

### Marathoner: Ultra-Long-Horizon Autonomous Intelligence
arXiv 2609.34378 · 2026-09-30 · Ant Group（+澳门大学、北大，据搜索）· HF 28↑ · [arXiv](https://arxiv.org/abs/2609.34378) · [HF](https://huggingface.co/papers/2609.34378) · 无 repo

**Source:** `abstract-only` + `+search`

**TL;DR:** 完整的超长程 agent post-training 流程：从大型 release PR（1000+ 行新代码）合成任务，用 Multi-Task Chaining 串成更难的任务，用强 teacher 加多种 harness 做拒绝采样 SFT 冷启动，再在独立沙箱中用真实 harness 做 RL，并提出 Later Stage Bonus Reward 鼓励执行后期仍有"有意义的动作"。

- **Problem:** agent 在长任务中容易提前收工或后期"摸鱼"，而且缺少前沿难度的超长程训练任务。
- **Method：**
  - 任务合成：来自 GitHub 大型 release PR；Multi-Task Chaining 把多个生成的任务串成一个任务。
  - RFT：teacher 搭配多种 harness 生成轨迹，经拒绝采样后做 SFT。
  - RL：rollout 在真实 harness 和独立 sandbox 里执行。
  - Later Stage Bonus Reward：奖励执行后期的有效动作。具体形式未知，推测与后期 tool call 的有效性或进展有关。
  - RL 算法未知。
- **Key results（作者报告，二手来源）：** 5 个长程 benchmark 相对 base 都有提升，"甚至超过强闭源模型"，可以连续工作 10 小时以上、做 1000+ 次工具调用。**没有拿到具体数字。**
- **What's new:**
  - 相对 SWE-smith 和 SWE-Gym（issue 级小任务）：任务粒度是 release 级，并做了串联。
  - Later Stage Bonus 是专门针对长程"后期懈怠"的 reward shaping。和 TerminalHorizon 里"base model 提前停止"的观察一致。
- **Reputation check:** Ant Group，HF 28↑，没有代码。红旗：摘要截断，看不到 benchmark 名称；"超过闭源模型"缺少上下文；Later Stage Bonus 可能诱导"刷动作"式的 reward hacking，需要看原文是否有防护。
- **Limitations：** 只有摘要级信息；release PR 任务的 verifier 质量未知；10 小时级 rollout 的 RL 成本和 staleness 处理没有提及。
- **Relevance（browser/CUA env）：**
  - Multi-Task Chaining 能低成本造出长程 web 任务（例如把"查订单→改地址→申请退款"串起来）。
  - Later Stage Bonus 提醒我们：长程 RL 需要显式对抗提前终止。但要设计成"有进展才给奖励"，而不是按动作数给。
- **Verdict：值得浏览**：思路对路，但证据太薄，等原文或代码出来再细读。

---
### NeMo-DCR: Bit-Exact Delta-Compressed Refit for Scalable Agentic RL at Trillion-Parameter Scale
arXiv 2610.08430 · 2026-10-07 · NVIDIA（NeMo RL 团队，Terry Kong 等）+ Aalto（Mario Di Francesco）· HF 11↑ · [arXiv](https://arxiv.org/abs/2610.08430) · [HF](https://huggingface.co/papers/2610.08430) · repo [NVIDIA-NeMo/RL](https://github.com/NVIDIA-NeMo/RL)（`docs/guides/refit.md`、`docs/design-docs/sparse-delta-refit.md`）

**Source:** `repo-readme`（NeMo RL 设计文档）+ 摘要 + `+search`（数字来自二手新闻和 LinkedIn 帖子，未经原文核实）

**TL;DR:** 训推分离的 agentic RL 每一步都要把新权重同步到 rollout 集群（refit）。1T checkpoint 在两个 AWS region 之间完整传输要 87.5 分钟，而 BF16 训练每步只有约 1% 的权重存储值变化。NeMo-DCR 只发送变化部分，并保证 bit-exact：接收端得到的参数和 buffer 比特与 dense refit 完全一致。

- **Problem:** 已有的稀疏 refit 系统在 placement（重新实现切分规则、组装完整张量）、exactness（用算术重建数值）、efficiency（跨集群 collective）上各有短板，而且都不能从 refit 中途失败中恢复。
- **Method（摘要）：**
  - Placement：用固定的 affine mapping 把训练 shard 的变化投影到 checkpoint 的 canonical 坐标，其余变化走 residual conversion，最后由 serving runtime 的原生 loader 放进接收端存储。
  - Exactness：affine 变化用可压缩的 XOR mask 承载，其他变化用 overwrite；接收端原地 apply；重试时覆盖部分写入；joint commit 把 policy 与下一个 delta 的 baseline 绑定。
  - Efficiency：在构造 delta 的同时，通过对象存储（S3）或 relay tree 流式发送 payload，不使用跨集群 collective。
- **开源实现（NeMo RL 文档）的重要差异：**
  - 开源版是"Remote Sparse-Delta vLLM Refit"：Megatron Bridge 导出 canonical HF 张量，按 `chunk_index % producers` 分配 owner 做比较；XOR 或 overwrite 编码后 zstd-1；通过 S3 或 ZeroMQ 二叉 relay tree 传输；接收端调用 vLLM 原生 `load_weights()`。
  - 文档**明确写着**："There is no MCore policy-local baseline, conversion-task detector, affine projection…"。也就是说，开源版刻意不做论文里的 affine projection，所以必须支付完整的 Bridge export 成本。
  - 失败恢复：文档说接收端写入不回滚，失败后必须从已知版本重新加载，in-place recovery 还在 issue #3274 跟踪。这与摘要中"retries overwrite partial writes"不完全一致，可能论文实现比 upstream 更完整，也可能论文描述的是目标设计。
  - 限制：只支持 GRPO；只支持 BF16/FP16 的非量化 rollout；版本切换是同步的，所有 payload apply 完之前 generation 暂停。
- **Key results（二手来源，未核实）：**
  - 每步元素变化率为 0.6–1.2%（Qwen3/Nemotron）。XOR 比 overwrite 小 38–40%，zstd 再压缩 1.7–2.2 倍。
  - 30B–1T 模型比完整 checkpoint 传输快 12–40 倍。在 3% 变化率下 1T 约 150 秒；120B 用 relay tree 为 22.6 秒（对照 750 秒）。传输占 refit 延迟的 77–94%。
  - 摘要原文："Even at 3% and 5% change rates, NeMo-DCR refits of 30B-1T models…"，后文被截断。
- **What's new:** 相对 slime、verl、AReaL 的 NCCL 全量广播，以及 Checkpoint-Engine/NIXL 的全量 RDMA：只传 delta，跨 region 可用，bit-exact。相对其他稀疏 refit：用原生 loader 处理 placement，不需要写模型族相关的映射。
- **Reputation check:** NVIDIA 官方，代码已合入 NeMo RL（二手来源说是 PR #2444，约 7K 行），HF 关注度低（11↑）属于正常。红旗：论文设计和开源实现之间存在差异（见上）；跨 region 的 87.5 分钟是"最坏情况"基线。
- **Limitations：**
  - 依赖"每步变化率低"：大学习率、优化器 warmup 或量化 rollout 时不一定成立。
  - 不支持 FP8/FP4 rollout，这正好与 TRACE 的方向冲突。
  - 版本切换仍是同步的。
- **Relevance（browser/CUA env）：**
  - 只有当你的训练集群和 rollout 集群分处不同数据中心（例如浏览器沙箱集群在别处）时才直接相关；否则属于基础设施知识储备。
  - 但"rollout 集群可以远离训练集群"这一点，会改变 CUA 环境集群的部署选择。
- **Verdict：值得浏览**：适合基础设施方向的人，环境构建者了解结论即可。

---

### TRACE: Rollout-Guided Quantization-Aware Training for FP4 Reinforcement Learning of MoE Language Models
arXiv 2610.07767 · 2026-10-07 · Qwen / Alibaba（+Ohio State，据搜索）· HF 85↑ · [arXiv](https://arxiv.org/abs/2610.07767) · [HF](https://huggingface.co/papers/2610.07767) · 无 repo

**Source:** `abstract-only` + `+search`（二手数字未核实）

**TL;DR:** FP4 rollout 能大幅提速 RL，但训练和 rollout 两条量化路径各自优化，会造成 train-rollout mismatch。TRACE 在 rollout 时记录 FP4 量化结果（routed expert 激活、KV），用来指导训练侧 QAT 的 FP4 取整决策，直接缩小两条路径的差异；同时只缓存深层的 mantissa 和 scale 信息，以控制存储和通信开销。

- **Problem:** 低精度 rollout 会加剧 off-policy 程度，即 rollout 的 logprob 和训练时重算的 logprob 不一致。已有方法（例如 QUADS，2607.15810，该文报告 NVFP4 rollout 搭配 BF16 训练约 150 步后崩溃）分别优化两侧精度。
- **Method：**
  - rollout-guided QAT：训练侧前向时，FP4 取整方向参照 rollout 侧的实际量化结果。
  - quantization-information caching：只保留深层的 mantissa 和 scale；二手来源称完整记录每个 RL step 约 51 TB，用 1-bit mantissa cache 来压缩。
  - 支持 W/A 联合 FP4 和 FP4 KV-cache rollout。
- **Key results：**
  - 摘要：在 4 个大型 MoE、推理/编码/长程 RL 任务上，RL 性能可以与 BF16 rollout 相当，rollout 最多快 5.4 倍，最终 FP4 性能强于 post-hoc FP4 量化。
  - 二手来源：模型是 Qwen3.5-35B-A3B、Qwen3.5-122B-A10B、Qwen3.8-Flash-Next、Qwen3.8-2.4T-A95B（名字奇怪，待核实）。Qwen3.5-35B-A3B 的推理平均分从 QUADS 的 68.8 提到 75.3。5.4 倍提速在 4 张 GB200 上测得。
- **What's new:** 相对 QUADS、FlashRL、各种 FP8 rollout 加 importance-sampling 修正（TIS/MIS）：不在 loss 侧做 IS 修正，而是在量化侧直接对齐两条执行路径。
- **Reputation check:** Qwen 团队，HF 85↑。没有代码。GB200/FP4 硬件门槛高。
- **Limitations：** 依赖 Blackwell FP4；缓存和传输量化信息带来额外系统复杂度；和 NeMo-DCR 这类 BF16 delta refit 不兼容。
- **Relevance（browser/CUA env）：** 间接相关。长程 agent rollout 的成本以 decode 为主，FP4 rollout 能大幅降本；但 train-rollout mismatch 在长轨迹上会累积，需要关注这类对齐方法。对环境构建者来说只需知道结论。
- **Verdict：值得浏览（infra 方向）/ 环境构建者可跳过**。

---

### Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States (PoS)
arXiv 2610.01415 · 2026-10-02 · Nankai + Alibaba（实习工作）+ Tsinghua（Dan Pei）· HF 70↑ · [arXiv](https://arxiv.org/abs/2610.01415) · [HF](https://huggingface.co/papers/2610.01415) · repo [luoyu100/PoS](https://github.com/luoyu100/PoS)

**Source:** `repo-readme`（README 加 `docs/results.md` 中转录的 Table 1/2）

**TL;DR:** 一个推理时框架。它维护显式的 belief state（实体、状态、关系，加上"待了解的 epistemic gap"和"待完成的 achievement gap"），用 Belief Sentinel 校验更新的一致性，并检测 Belief Trapping（Static/Cycle/Drift 三类停滞），再按 gap 类型定制恢复约束。**不涉及 RL。**

- **Method：** 在共享的 ReAct 循环之上加三层：belief 建模，belief 引导的动作选择加 Sentinel 一致性审计，陷入诊断与恢复。陷入检测结合了 gap 持续、进展停滞和 belief 复现三个信号。
- **Environments:** ALFWorld（134 个 valid-unseen 任务）、LOCA-Bench（7 种上下文长度×75 例，共 525 例）、RCA-100（103 例）、ClinDiag（604 例）。
- **Key results（作者报告，Qwen3.7-Plus 骨干）：**
  - ALFWorld：Raw 62.69，最强基线 LongHorizon-Harness 72.39，PoS 88.81。
  - LOCA-Bench：43.62 / 52.57 / 56.38。
  - RCA-100：24.27 / 28.16 / 38.83。
  - Kimi-K3、GLM-5.3 两个骨干上也都最好（GLM-5.3 ALFWorld 97.01）。
  - 代价：RCA-100 上总 token 是 Raw 的 5.06 倍（1,800K 对 356K），虽然 Task Agent 本身的 token 减少了 20.9%。
- **What's new:** 相对 ACON（上下文压缩）、PACE、HiAgent（子目标记忆）、MemGPT 类方法：维护"当前世界的可行动理解"，而不是保留或压缩历史；并显式检测陷入。
- **Reputation check:** 有代码。但 ACON/PACE/HiAgent/LongHorizon-Harness 这些基线的实现**没有开源**；用的是 live API，没有固定快照。ALFWorld 上的提升幅度大到需要警惕基线是否调好。
- **Limitations：** 推理开销 5 倍；与 RL 无关；belief schema 需要按领域定制。
- **Relevance（browser/CUA env）：** 可以作为 CUA 推理 harness 的参考，例如陷入检测能用来提前终止 rollout、节省环境算力。但它不是训练方法。
- **Verdict：可跳过**（对 agentic-RL 来说属于误标；做推理 harness 的人可以浏览）。

---

### Beyond Dyadic Memory: Interaction-Aware Multimodal Memory with Adaptive Agentic Retrieval for Multi-Party Spoken Conversations (VoxPolyMem)
arXiv 2609.32522 · 2026-09-30 · Zhejiang University · HF 56↑ · [arXiv](https://arxiv.org/abs/2609.32522) · [HF](https://huggingface.co/papers/2609.32522) · repo [VoxPolyMem/Code](https://github.com/VoxPolyMem/Code)

**Source:** `repo-readme` + 摘要

**TL;DR:** 面向多人语音对话的长期记忆框架：增量说话人识别，加上交互记忆、事实记忆、参与者画像三层结构。检索被建模为序贯决策，并提出 EG-GRPO（按轮次做 evidence-gain credit assignment）。自建 VoxPolyBench 上得分 85.0。

- **Method：** agent 改写 query，并选择检索工具和记忆层。EG-GRPO 按轮次给 credit，奖励互补证据的获取（公式未知）。
- **Key results（作者报告）：** VoxPolyBench 85.0（比最强基线高 23.6 分）；Mem-Gallery 89.6，H2HMem-Multi 74.4（比公开记忆基线各高 8 分以上）。
- **Reputation check / 红旗：**
  - repo 中**没有任何 RL/EG-GRPO 训练代码**。`REPRODUCIBILITY.md` 写明"RL training… must be released as a new version"。公开的只是 43 份只含分数的回放记录，"offline replay 只证明算术正确，不证明 live 调用能复现"。
  - 主要 benchmark 是自建的。
  - 用 LLM judge 打分。
- **Relevance（browser/CUA env）：** 很低。round-wise evidence-gain credit 是一个通用思路（按每轮新增信息给奖励），但没有代码可参考。
- **Verdict：可跳过**（领域不相关，RL 部分没有开源）。

---

## 附：来源与可信度说明
- 拿到 repo 级一手材料的有 9 篇：SRD、Trace2Env、Sharpening Tax、VeriHarness、Taste-Bench、PoS、VoxPolyMem、TerminalHorizon（只有项目页）、NeMo-DCR（只有 upstream 文档，且与论文设计有差异）。
- 只有摘要、靠搜索补充的有 5 篇：CodeMidas、GAGAR、VHD-Play、Marathoner、TRACE。这 5 篇中凡是标注"二手来源"的数字，都应在拿到 PDF 后核对。
- 二手来源（WebSearch 返回的聚合站和新闻）：alphaxiv、hyper.ai、aiweekly.co、developersdigest、LinkedIn 帖子。这些站点在本环境中无法直连，只能看到搜索摘要。
