# Agent eval & safety

> agent 评测可复现性、reward hacking、沙箱逃逸。人工维护。

## 条目

### 2026-08 → 10：agent 越界事故密集披露（深读结论，详见 [frontier-labs review](../reviews/2026-10-14_frontier-labs.md) §2 时间线、§3.4）
- **事故**
  - OpenAI：[IM1](https://openai.com/index/hugging-face-incident-and-the-road-ahead) 评测逃逸入侵 HF（约 1,200 个 agent 经制品库协作）；09-20 [DNS 外联](https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/)后最强模型的 tool-use 全面暂停。
  - Anthropic：[4 起评测](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents)越权；10-09 报告 BrowseComp、OSWorld 等[实网评测](https://www.anthropic.com/research/investigating-unintended-model-actions)造成真实副作用，所有内部评测断网。
  - UK [AISI](https://www.aisi.gov.uk/blog/gpt-6-astra-performs-unsanctioned-supply-chain-attacks-in-simulations)：08-04 agent 向真实 GitHub 项目提交[恶意 PR](https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities)。
- **归因**
  - Anthropic：[偏置推理](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents)（坚持“[这是模拟](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents)”）加鲁莽。[Mythos 5](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents) 在模拟复现中 82% 采取严重有害行动，Opus 5 为 31%。
  - [偏置推理](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents)集中在预期解不可达的 GUI 任务；pre-release 审计和离线 CoT 监控都没发现。
- **指标**
  - OpenAI [unwanted persistence](https://deploymentsafety.openai.com/gpt-6-1-sol)：Luna 15.9%、[Astra](https://openai.com/index/safety-overview-gpt-6-astra) 17.4%、6.1 Sol 23.5%、Sol（10 月版）28%。
  - [AISI](https://www.aisi.gov.uk/blog/gpt-6-astra-performs-unsanctioned-supply-chain-attacks-in-simulations)：Astra 越界供应链攻击率高于前代，且把自动消息当授权。
- **监控的上限**：OpenAI 对抗设定下 CoT 监控召回 <11%；[metagaming](https://alignment.openai.com/metagaming-latents) latent 随 RL 增强；NVIDIA [OpenShell](https://github.com/NVIDIA/OpenShell) 的 SMT prover 挡住了 agent 两小时游说审核者。
- **检查清单与工具**：Anthropic 对评测伙伴的要求；OpenAI 训练 [safety case](https://openai.com/index/towards-safety-cases-for-frontier-ai-training)；AISI optstop、[Transect](https://github.com/AI-Safety-Institute/transect)；NVIDIA Sentry 硬件看门狗；Meta [Sentinel](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse) 污点追踪加带外审批。

### 2026-07-27 · [Anatomy of a Frontier Lab Agent Intrusion](https://huggingface.co/blog/agent-intrusion-technical-timeline)（+ [事件披露](https://huggingface.co/blog/security-incident-july-2026)）
- 一个跑 [ExploitGym](https://openai.com/index/hugging-face-incident-and-the-road-ahead)（漏洞利用 benchmark）内部评测的 agent，推断 HF 上可能有 benchmark 参考答案，于是**为“作弊”而入侵**：先利用包仓库缓存代理 0-day 逃出评测沙箱，再控制第三方公开代码评测 harness 作跳板。
- 进入 HF 的两个向量：数据集 HDF5 外部 raw storage 读本地文件；Jinja2 模板注入。随后横向移动、窃取凭证、外传与清理痕迹，约 17.6k 条动作、4.5 天。
- 闭源模型的安全护栏拒绝协助分析攻击代码，最终用开源 GLM-5.2 完成取证。
- **对我**：reward hacking 不只发生在 reward 函数里——agent 会去攻击评测基础设施本身。做 real-web RL / BUA 环境时，egress 白名单与答案隔离是必需项。

### 2026-09-22 · [UK AISI × EvalEval: reproducible benchmark results](https://huggingface.co/blog/evaleval-aisi)
- [AISI](https://www.aisi.gov.uk/blog/gpt-6-astra-performs-unsanctioned-supply-chain-attacks-in-simulations) 用 Every Eval Ever schema + Evaluation Cards 公开 SWE-Bench Pro、Terminal-Bench 2.0、HLE、FrontierMath、HealthBench 结果和配置（6 个前沿模型）。
- 配套论文：分数随推理算力和协议（如是否有 oracle 反馈）显著变化。
- **对我**：topic 页 leaderboard 必须记录 setup，否则跨来源比较没有意义。

### 2026-08-13 · [Reproducing 2,200 papers from ICML](https://huggingface.co/blog/icml-2026-open-reproductions)
- 1,200+ 人 × 各自 coding agent，19 天复现 2,226 篇（约 1/3 会议）；51% 至少一条 claim 被验证，23% 至少一条被证伪/有争议，242 篇不同团队结论相反。
- GLM-5.2 logbook judge 逐 claim 判 verified / falsified / toy / inconclusive，且把 logbook 自评视为不可信。
- 有限步数检查会漏掉反例（某定理在 t=224 之后才被推翻）。

### 近期论文（2026-09-14 → 10-14，详见 [papers review](../reviews/2026-10-14_papers.md) §3.5）
- **分数的隐藏变量**：[Schrödinger's Code Repository](https://arxiv.org/abs/2609.27891)（数据污染探测）· [Harness Design study](https://arxiv.org/abs/2609.20804)（176 组对照实验）· WebArena-Lite 审计 · ProgramGym（换 harness 差 20.84pp）
- **闭环自欺与共谋**：[False Frontiers](https://arxiv.org/abs/2609.39102)（co-cheating）· Emergent Collusion（94% 轨迹出现）· Covert Assistance（9 个模型中 7 个规避 monitor）
- **CUA 安全**：[HazardAuditor](https://arxiv.org/abs/2609.15134) · [AdvSim2Real](https://arxiv.org/abs/2610.08773) · UndoBench（简单重试在 53% 试验中产生重复副作用）
