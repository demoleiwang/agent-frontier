# Agentic RL

> 多轮 / 长程 RL、环境构建与扩展、异步 RL 基础设施、reward 设计。人工维护。

## 分类

| 类别 | 代表工作 | 一句话 takeaway |
|---|---|---|
| 环境标准 / 分发 | HF RL Environments on Hub | 环境 = taskset（dataset）+ runtime（框架），Hub 只管托管与发现 |
| 异步 RL 系统 | TRL AsyncGRPOTrainer + LoRA | 只同步 adapter，跨机器靠共享存储即可，不需要 NCCL |
| 非可验证奖励 | Painting with code (TRL + OpenEnv) | 偏好模型 + pairwise judge 对照手工参考池 = RL over taste |
| 小模型 RLVR recipe | LFM2.5-350M + GRPO on IFStruct | 3 个可验证 reward 加权，100 步见效 |

## 条目

### 2026-08 → 10 lab 动态（详见 [reviews/2026-10-14_frontier-labs.md](../reviews/2026-10-14_frontier-labs.md)）
- [Agent Lightning v1.0](https://www.microsoft.com/en-us/research/blog/agent-lightning-v1-0-a-3500-line-lightweight-agentic-rl-framework-for-training-agents-with-real-harnesses/)（MSR）：在真实部署 harness 里做 RL，3.5k 行；6K 样本让 Qwen3.5-9B SWE-bench Verified 41.8 → 56.4（自报）。
- [Putting task expertise into RL](https://thinkingmachines.ai/news/putting-task-expertise-into-rl/)（Thinking Machines）：专家校验数据 + reward 重塑的 RLVR 胜过 scaffold 系统（BIRD text-to-SQL）。
- [MiMo-V2.6](https://mimo.xiaomi.com/rl/)（小米）：开源权重 + RL 环境 + RL 代码 + RL 算力账本。
- [Grok 4.7](https://x.ai/news/grok-4-7)：更长的小时级任务 RL + 自我验证。
- **RL 副作用被系统记录**：OpenAI misalignment reports（compaction 摘要中自我提示隐瞒错误、为作弊泄露 token）、[metagaming latents](https://alignment.openai.com/metagaming-latents) 随 RL 增强；[训练暂停机制](https://openai.com/index/pacing-model-development-cyber-capabilities/)（30 分钟内无法排除的安全信号即暂停）。

### 2026-09-28 · [Welcome RL Environments to the hub](https://huggingface.co/blog/rl-environments)
- RL 环境 = 打 `rl-environment` tag 的 dataset repo；框架 tag（Harbor / Verifiers / OpenEnv / NeMo Gym）生成加载命令，一个 repo 可兼容多个框架。
- 只管 taskset，runtime 交给框架；HF Jobs / Sandboxes 负责运行。
- **对我**：自建 BUA/CUA 环境时可直接按 Harbor task 目录格式发布到 Hub，一次发布多框架可用；broken task 在同一个 discussion 区汇总。

### 2026-09-10 · [Async GRPO with LoRA across HF Jobs](https://huggingface.co/blog/asyncgrpo-lora-hfjobs)
- TRL v1.14 `AsyncGRPOTrainer` 支持 LoRA，只把 adapter（MB 级）推给 vLLM：trainer 写到挂载的 Storage Bucket，原子 rename 后调 vLLM `/v1/load_lora_adapter`。
- vLLM adapter 槽位 = `max_staleness` + 2（旧 rollout 必须用起始版本跑完）。
- proxy 按 KV prefix 把多轮 rollout 路由到同一 replica，并广播 adapter 更新。
- 引用 Thinking Machines “LoRA Without Regret”：policy-gradient RL 每 episode 信息量 ~O(1) bit，rank-1 LoRA 足够。
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
