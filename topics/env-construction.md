# Environment construction

> agent 训练与评测环境怎么建：环境形态、状态与基础设施、任务合成、verifier 与 rubric、数据准备、隔离。人工维护。
> 综述见 [环境构建全景](../reviews/2026-10-14_office-pro-env.md)，方法卡片见 [methods 笔记](../reviews/2026-10-14_office-pro-env/methods.md)，lab 实践见 [labs 笔记](../reviews/2026-10-14_office-pro-env/labs.md)。

## 环境形态（保真度 × 可扩展性）

| 形态 | 代表 | 适用 |
|---|---|---|
| 真实 SaaS 托管副本 | [Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad) | 稀缺高价值流程 |
| VM 中的真实软件 | [OSWorld-Science](https://github.com/DiscoAILab/OSWorld-Science/blob/main/README.md)、[EngiWorld](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md) | 办公套件、专业软件 |
| 带状态 API 的 mock | [CUA-Gym-Hub](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)、[Kimi K3](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf) | 规模化 RL |
| agent 合成应用 | [Echoverse](https://github.com/microsoft/Echoverse/blob/main/README.md)、[SoftwareGym](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md) | 覆盖面扩展 |
| trace 重建替身 | [Trace2Env](https://github.com/ruyue0001/trace2env/blob/main/docs/RUNTIME_HARNESS.md) | 不能自建的内部系统 |
| 纯 LLM 模拟 | [Apple env-free](https://arxiv.org/abs/2607.16900) | SFT 冷启动，不宜做 RL 奖励 |
| 物理仪器 | [Anthropic MHS](https://www.anthropic.com/news/model-hardware-standard-research-preview) | 实验室自动化 |

## 可照抄的规则

- 可测试性写成契约：dump / reset / seed（[SoftwareGym](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/agent/prompt/Coderprompt.json)）。
- verifier 负对照：初始状态不能通过、解完必须通过（[VeriGen](https://github.com/THUDM/SCALE-CUA/blob/main/VeriGen/docs/architecture/agent_feasibility_verification.md)）。
- 难度标定：参考模型 avg@3 落在约 0.4–0.6（[GDPevo](https://github.com/Prism-Shadow/GDPevo/blob/main/data_construction/Stage_3_Quality_Filtering/review_workspace/guides/review_criteria.md)）；pass@8 只留 1–7 次成功（[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
- 长程任务：阶段终态序列化后串接（[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）；递归扩展并逐轮验证（[RST](https://arxiv.org/abs/2608.05466)）。
- 判分在 fork 上做，答案晚上传，状态库对 agent 不可见（[K3](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)、[MiMo](https://github.com/XiaomiMiMo/verl/blob/mimo-oss/recipes/general/general_agent/environment.py)）。
- `.git` 默认 strip，运行时 antihack guard（[mimoagent](https://github.com/XiaomiMiMo/mimoagent/blob/mimo-oss/src/mimoagent/environments/datasets/base.py)）。
- 默认断网并覆盖 DNS，mock 失败时关闭（[OpenAI DNS](https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/)、[Anthropic](https://www.anthropic.com/research/investigating-unintended-model-actions)）。

## 环境质量的警示

- 超过 10% 的生产 RL 环境被标记为有问题（[Anthropic](https://www.anthropic.com/news/improving-alignment-security-efforts)）。
- MiMo 开源任务约 2/3 可从 git 历史拿到答案（[Vals AI，二手](https://digg.com/ai/wo6cdxwj)）。
- Argo-Bench 开发期有 run 读到 grader 拿到 0.99（[reward_hacking](https://github.com/TextQLLabs/Argo-Bench/blob/main/analysis/reward_hacking/README.md)）。
