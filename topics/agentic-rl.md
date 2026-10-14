# Agentic RL

> 多轮 / 长程 RL、环境构建与扩展、异步 RL 基础设施、reward 设计。人工维护。

## 分类

| 类别 | 代表工作 | 一句话 takeaway |
|---|---|---|
| 环境标准 / 分发 | HF [RL Environments](https://huggingface.co/blog/rl-environments) on Hub | 环境 = taskset（dataset）+ runtime（框架），Hub 只管托管与发现 |
| 异步 RL 系统 | [TRL AsyncGRPOTrainer + LoRA](https://huggingface.co/blog/asyncgrpo-lora-hfjobs) | 只同步 adapter，跨机器靠共享存储即可，不需要 NCCL |
| 非可验证奖励 | [Painting with code (TRL + OpenEnv)](https://huggingface.co/blog/train-to-paint-with-code) | 偏好模型 + pairwise judge 对照手工参考池 = RL over taste |
| 小模型 RLVR recipe | [LFM2.5-350M + GRPO on IFStruct](https://huggingface.co/blog/grpo-with-trl-ifstruct) | 3 个可验证 reward 加权，100 步见效 |

## 条目

### 2026-08 → 10 lab 动态（深读结论，详见 [frontier-labs review](../reviews/2026-10-14_frontier-labs.md) §3.3）
- **在真实 harness 里训练成为共识**
  - [Agent Lightning v1.0](https://github.com/microsoft/agent-lightning)（MSR，约 3.5k 行）：网关记录 token ID 和 logprob，每个 rollout 一个 K8s Job，异步训练保持组完整、更新前暂停并排空、TIS 阈值 2，MoE 用 R3 router replay。Qwen3.5-9B 的 SWE-bench Verified 41.8 → 56.4。
  - 同一思路：[NeMo Gym](https://github.com/NVIDIA-NeMo/Gym) 0.6/0.7、Orchard [OpenForge](https://github.com/microsoft/Orchard)、MiMo [uni-agent](https://github.com/XiaomiMiMo/uni-agent)。
- **harness 随机化**：[Kimi K3](https://github.com/MoonshotAI/Kimi-K3) 在 RL 中组合 5 种以上 harness 的模块；[MiMo](https://github.com/XiaomiMiMo/verl) 提供多 harness 配置。
- **长程**：[Grok 4.7](https://x.ai/news/grok-4-7) 的 RL 偏向小时级任务（Terminal-Bench 4.0 20.3 → 37.6，但输出 token 约增 2.5×）；[Kimi K3](https://github.com/MoonshotAI/Kimi-K3) partial rollout；[slime](https://github.com/THUDM/slime) 全异步。
- **奖励与防 hack**
  - [MiMo verl](https://github.com/XiaomiMiMo/verl)：tool-call 错误片段惩罚、按符号守恒的 advantage 再平衡、重复早停、VLM 组内挑选式判分。
  - [Kimi K3](https://github.com/MoonshotAI/Kimi-K3) agentic GRM。
  - [Thinking Machines](https://thinkingmachines.ai/news/putting-task-expertise-into-rl/)：专家清洗数据加可反驳的 verifier。
  - [Agent Lightning](https://github.com/microsoft/agent-lightning) 防 hack 清单。
  - 反例：[MiMo](https://github.com/XiaomiMiMo/verl) 开源 coding 任务约 2/3 可从 git 历史拿到答案（[Vals AI](https://digg.com/ai/wo6cdxwj)）。
- **环境质量就是安全**
  - Anthropic 4 月冻结 RL 环境，[超过 10%](https://www.anthropic.com/news/improving-alignment-security-efforts) 被标记；用 [80 个可 hack 环境](https://www.anthropic.com/news/improving-alignment-security-efforts)训练出的模型会在模拟中突破沙箱。
  - OpenAI [IM1](https://openai.com/index/hugging-face-incident-and-the-road-ahead) 训练 run 中复杂作弊率上升，最终引发 HF 事件。
  - OpenAI [暂停 RL 两周](https://openai.com/index/pacing-model-development-cyber-capabilities)；最大前沿 RL run 至今搁置。

### 2026-09-28 · [Welcome RL Environments to the hub](https://huggingface.co/blog/rl-environments)
- RL 环境 = 打 `rl-environment` tag 的 dataset repo；框架 tag（Harbor / Verifiers / OpenEnv / [NeMo Gym](https://github.com/NVIDIA-NeMo/Gym)）生成加载命令，一个 repo 可兼容多个框架。
- 只管 taskset，runtime 交给框架；HF Jobs / Sandboxes 负责运行。
- **对我**：自建 BUA/CUA 环境时可直接按 Harbor task 目录格式发布到 Hub，一次发布多框架可用；broken task 在同一个 discussion 区汇总。

### 2026-09-10 · [Async GRPO with LoRA across HF Jobs](https://huggingface.co/blog/asyncgrpo-lora-hfjobs)
- TRL v1.14 `AsyncGRPOTrainer` 支持 LoRA，只把 adapter（MB 级）推给 vLLM：trainer 写到挂载的 Storage Bucket，原子 rename 后调 vLLM `/v1/load_lora_adapter`。
- vLLM adapter 槽位 = `max_staleness` + 2（旧 rollout 必须用起始版本跑完）。
- proxy 按 KV prefix 把多轮 rollout 路由到同一 replica，并广播 adapter 更新。
- 引用 [Thinking Machines](https://thinkingmachines.ai/news/putting-task-expertise-into-rl/) “LoRA Without Regret”：policy-gradient RL 每 episode 信息量 ~O(1) bit，rank-1 LoRA 足够。
- **对我**：多轮 agent rollout 的 KV-prefix 路由 + staleness 设计可直接借鉴。

### 2026-09-03 · [Training a coding model to paint watercolours](https://huggingface.co/blog/train-to-paint-with-code)
- 模型输出 ~150 行 p5.brush JS（限 10 个 API）作画；reward = HPSv3 偏好分 + Qwen3-VL pairwise judge（对照 4 张随机参考，双向顺序）。
- “参考池就是 reward function”——工作从调超参转移到策划参考集。
- 环境、scorer 均以 Space 部署，训练在 HF Jobs，全部 artifact 开源。

### 2026-09-03 · [Fine-tuning a 350M Model for Structured Outputs in 100 GRPO Steps](https://huggingface.co/blog/grpo-with-trl-ifstruct)
- LFM2.5-350M + LoRA（~6M 参数），~500 条 Nemotron structured-output 数据，reward：格式 1.0 / 字段数 0.5 / schema 校验 2.0。
- IFStruct 22.6% → 29.7%；免费 Colab 可跑。

### 2026-07-07 · [LeRobot v0.6.0](https://huggingface.co/blog/lerobot-release-v060)
- _未读_，关键词命中（evaluate / improve 闭环），具身方向，低优先级。

### 近期论文（2026-09-14 → 10-14，详见 [papers review](../reviews/2026-10-14_papers.md) §3.2–3.3）
- **环境合成**：[CodeMidas](https://arxiv.org/abs/2609.22068)（MiMo）· [VHD-Play](https://arxiv.org/abs/2609.27321)（Qwen）· [Trace2Env](https://arxiv.org/abs/2610.06100)（NTU）· TerminalHorizon
- **grader 与 credit assignment**：[GAGAR](https://arxiv.org/abs/2609.32577)（MiMo，1T 级）· VeriHarness（Google）· RDPO / GuardPO / SLCA-GRPO
- **稀疏奖励**：[SRD](https://arxiv.org/abs/2610.08077)（Salesforce）· [PTGS / Sharpening Tax](https://arxiv.org/abs/2610.01509)（Meta）
- **工业报告与基建**：[MiMo-V2.6](https://arxiv.org/abs/2610.11959) · NeMo-DCR（NVIDIA）· TRACE（Qwen，FP4 RL）
