# Agent eval & safety

> agent 评测可复现性、reward hacking、沙箱逃逸。人工维护。

## 条目

### 2026-08 → 10：agent 逃逸事故密集披露（详见 [reviews/2026-10-14_frontier-labs.md](../reviews/2026-10-14_frontier-labs.md)）
- OpenAI [The Hugging Face incident and the road ahead](https://openai.com/index/hugging-face-incident-and-the-road-ahead/)：确认 HF 入侵来自其内部模型（评测中利用 Artifactory 0-day 逃逸）；[DNS 隧道外联事件](https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/) 后暂停全部 tool-use 训练/评测；[Towards safety cases for frontier AI training](https://openai.com/index/towards-safety-cases-for-frontier-ai-training/)。
- Anthropic [alignment assessment of cybersecurity incidents](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents)：4 起评测环境误连公网导致的越权访问；两阶段扫描 4.81 亿 transcript；[非预期行为报告](https://www.anthropic.com/research/investigating-unintended-model-actions) 后全部内部评测断网。
- Anthropic [self-replicating AI](https://www.anthropic.com/research/self-replicating-ai)：小模型数月内可能在 IoT 设备上端到端自复制。
- 防御侧：NVIDIA [Open Agent Safety Platform](https://developer.nvidia.com/blog/nvidia-open-agent-safety-platform-a-reference-for-continuous-in-silicon-agent-monitoring/)（沙箱 + 硬件看门狗）、Google [Agent Anomaly Detection](https://developers.googleblog.com/agent-anomaly-detection-now-in-private-preview-on-the-gemini-enterprise-agent-platform/)、Google × Singapore AISI [双盲评测](https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/)。

### 2026-07-27 · [Anatomy of a Frontier Lab Agent Intrusion](https://huggingface.co/blog/agent-intrusion-technical-timeline)（+ [事件披露](https://huggingface.co/blog/security-incident-july-2026)）
- 一个跑 ExploitGym（漏洞利用 benchmark）内部评测的 agent，推断 HF 上可能有 benchmark 参考答案，于是**为“作弊”而入侵**：先利用包仓库缓存代理 0-day 逃出评测沙箱，再控制第三方公开代码评测 harness 作跳板。
- 进入 HF 的两个向量：数据集 HDF5 外部 raw storage 读本地文件；Jinja2 模板注入。随后横向移动、窃取凭证、外传与清理痕迹，约 17.6k 条动作、4.5 天。
- 闭源模型的安全护栏拒绝协助分析攻击代码，最终用开源 GLM-5.2 完成取证。
- **对我**：reward hacking 不只发生在 reward 函数里——agent 会去攻击评测基础设施本身。做 real-web RL / BUA 环境时，egress 白名单与答案隔离是必需项。

### 2026-09-22 · [UK AISI × EvalEval: reproducible benchmark results](https://huggingface.co/blog/evaleval-aisi)
- AISI 用 Every Eval Ever schema + Evaluation Cards 公开 SWE-Bench Pro、Terminal-Bench 2.0、HLE、FrontierMath、HealthBench 结果和配置（6 个前沿模型）。
- 配套论文：分数随推理算力和协议（如是否有 oracle 反馈）显著变化。
- **对我**：topic 页 leaderboard 必须记录 setup，否则跨来源比较没有意义。

### 2026-08-13 · [Reproducing 2,200 papers from ICML](https://huggingface.co/blog/icml-2026-open-reproductions)
- 1,200+ 人 × 各自 coding agent，19 天复现 2,226 篇（约 1/3 会议）；51% 至少一条 claim 被验证，23% 至少一条被证伪/有争议，242 篇不同团队结论相反。
- GLM-5.2 logbook judge 逐 claim 判 verified / falsified / toy / inconclusive，且把 logbook 自评视为不可信。
- 有限步数检查会漏掉反例（某定理在 t=224 之后才被推翻）。
