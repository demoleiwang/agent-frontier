# Professional-domain agent

> 专业领域 agent：工程（CAD / CAE / 仿真）、科学软件、金融、医疗、法务、数据与 BI。人工维护。
> 综述见 [环境构建全景](../reviews/2026-10-14_office-pro-env.md)，逐篇卡片见 [professional 笔记](../reviews/2026-10-14_office-pro-env/professional.md)，下半年提案见 [research-proposal](../reviews/2026-10-14_research-proposal.md)。

## Benchmark 速查

| Benchmark | 领域 | 最强（自报） | 验证 | 出处 |
|---|---|---|---|---|
| DAYJOB | 医疗 / 金融 | 24.7% / 23.9%（中位配置 0.6% / 2.5%） | 专家 binary rubric，全满足才通过 | [arXiv](https://arxiv.org/abs/2610.01306) |
| CADWorld | 机械 CAD（FreeCAD） | 17.5%，专家参考 87.0% | 可执行检查，binary | [arXiv](https://arxiv.org/abs/2609.16251) |
| EngiWorld | 26 款工程软件 | EngiScore 44.3；多软件任务 3.6% | 几何 / 物理引擎重算 | [arXiv](https://arxiv.org/abs/2609.37686) |
| Argo-Bench | 企业运营 / 财务 | 34.8% 的任务得分 ≥95 | 模拟器中结算后果 | [arXiv](https://arxiv.org/abs/2610.02122) |
| SimuVerity | Simulink 工程建模 | 总分 42.86 | 多工况原生仿真 | [README](https://github.com/SimuVerity/SimuVerity/blob/main/README.md) |
| FrontierFinance | 投研 | 前沿模型 49.2% | 11,543 条带来源的 rubric | [arXiv](https://arxiv.org/abs/2608.11683) |
| SWE-bench Science | 科学软件工程 | pass@1 < 50% | held-out tests | [arXiv](https://arxiv.org/abs/2608.19799) |
| NeutronGym | 中子仪器设计 | RL 后 Qwen3-8B 11% → 77% | McStas 分层 ladder | [arXiv](https://arxiv.org/abs/2610.03631) |

## 要点

- 真实专业软件已能装进 VM，瓶颈是商业许可证：用户自带 licence、网页版、只发 recipe（[OSWorld-Science](https://github.com/DiscoAILab/OSWorld-Science/blob/main/configs/snapshots.yaml)）。
- 最可信的 verifier 是让领域引擎重算（[EngiWorld eval.py](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/design-optimization/cli/fenics/task-01/eval.py)、[ScienceIDE](https://github.com/aitofound/ScienceIDE/blob/main/README.md)）。
- 训练需要部分分：NeutronGym 去掉后增益塌缩 60 个点（[arXiv](https://arxiv.org/abs/2610.03631)）。
- GUI 远弱于 CLI：EngiWorld 同一模型 CLI 48.3、GUI 2.0（[README](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)）。
- 专家成本高：CADWorld 约 1,300 人时 / 200 题（[CADWORLD.pdf](https://github.com/Zdong104/CADWORLD/blob/main/CADWORLD.pdf)）；DAYJOB 每题估计 13–17 小时（[arXiv](https://arxiv.org/abs/2610.01306)）。
- 真实仪器：设备侧强制安全上限，6 种故障在动作前被拦下（[Anthropic MHS](https://www.anthropic.com/news/model-hardware-standard-research-preview)）。
