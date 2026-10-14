# Office agent

> 办公与企业 SaaS 场景的 agent：办公套件（docx / xlsx / pptx）、邮件、日历、IM、工单、CRM / ERP。人工维护。
> 综述见 [环境构建全景](../reviews/2026-10-14_office-pro-env.md)，逐篇卡片见 [office 笔记](../reviews/2026-10-14_office-pro-env/office.md)，下半年提案见 [research-proposal](../reviews/2026-10-14_research-proposal.md)。

## 分类

| 类别 | 代表工作 | 一句话 takeaway |
|---|---|---|
| mock SaaS + 状态 API | [UI-Mate / CUA-Gym-Hub](https://github.com/Tencent/UI-Mate/blob/main/osworker_bench/CUA-Gym-Hub/README.md)、[HANDBOOK](https://github.com/surge-ai/handbook/blob/main/README.md)、[Thinkingbox](https://github.com/microsoft/thinkingbox/blob/main/README.md) | set / reset / diff 统一接口，按会话隔离，reward 读 state diff |
| agent 合成的业务系统 | [GDPevo](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md)、[SoftwareGym](https://github.com/MrKiing-Jin/SoftwareGym/blob/main/README.md)、[Echoverse](https://github.com/microsoft/Echoverse/blob/main/README.md) | 强制可测试性契约；深度比数量重要（[Echoverse](https://arxiv.org/abs/2607.28074)） |
| 办公文件交付物 | [OmegaUse-OfficeVal](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)、[WorkBuddy Bench](https://github.com/Tencent/workbuddy-bench/blob/main/README.md) | 代码 verifier 加 rubric；语义检查仍是缺口 |
| 真实 SaaS 托管副本 | [OpenAI × Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad) | 伙伴托管、EDGAR 合同合成任务、共写 rubric |
| 用户与偏好 | [MIMESIS](https://github.com/VietHoang1512/mimesis/blob/main/README.md)、[UserProxyBench](https://arxiv.org/abs/2609.38043)、[Project Swap](https://www.anthropic.com/research/project-swap) | 用户模拟器和偏好理解是隐藏变量 |

## Benchmark 速查

| Benchmark | 最强（自报） | 形态 | 出处 | 备注 |
|---|---|---|---|---|
| Thinkingbox | pass@1 65.36%，pass^20 25.25% | MCP mock + 用户模拟 | [arXiv](https://arxiv.org/abs/2608.19741) | 拒绝多余副作用；声明仅限评测 |
| Ironclad 11 工作流 | GPT-6 Astra 55.0%（rubric 部分分） | 真实 SaaS 副本 | [二手](https://fourweekmba.com/ai-openai-says-gpt-6-astra-scored-55-percent-on-11-ironclad-tas/) | 定向训练后的分数 |
| GDPevo | Claude Code + Opus 4.8 base 50.63% → fewshot 67.07% | Docker 业务系统 | [README](https://github.com/Prism-Shadow/GDPevo/blob/main/README.md) | oracle 上限 91.6%（[arXiv](https://arxiv.org/abs/2608.03764)） |
| MyPCBench | rubric 84.3，完美率 58.7 | 个性化桌面 | [Qwen-CUA 报告](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf) | 部分分与完美率分开报 |

## 开放问题

- xlsx 公式、透视表、docx 修订、pptx 版式的语义 verifier 几乎空白，部分任务还要 Office COM（[OfficeVal](https://github.com/baidu-frontier-research/OmegaUse-OfficeVal/blob/main/README.md)）。
- 副作用判分无共识：[Echoverse](https://github.com/microsoft/Echoverse/blob/main/harness/prompts.py) 容忍多余改动，[Thinkingbox](https://arxiv.org/abs/2608.19741) 拒绝。
- 坏 mock 必须 fail closed：练习副本加载失败后 agent 提交了真实政府表单（[Anthropic](https://www.anthropic.com/research/investigating-unintended-model-actions)）。
