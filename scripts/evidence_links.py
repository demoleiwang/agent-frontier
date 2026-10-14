"""Entity → source URL map used to add inline evidence links to synthesis markdown (reviews/*.md, topics/*.md).

Only distinctive names are listed; each URL is the primary source the review's claims about that entity rest on.
Run `python scripts/evidence_links.py <file>...` to link the first mention of a known entity in every claim block
that has no URL yet. It never changes wording, only wraps names in links, and prints blocks it could not resolve.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_evidence import URL, blocks  # noqa: E402

A = "https://www.anthropic.com"
ENTITIES: dict[str, str] = {
    # ---- OpenAI ----
    "The Hugging Face incident and the road ahead": "https://openai.com/index/hugging-face-incident-and-the-road-ahead",
    "IM1": "https://openai.com/index/hugging-face-incident-and-the-road-ahead",
    "ExploitGym": "https://openai.com/index/hugging-face-incident-and-the-road-ahead",
    "Pacing model development": "https://openai.com/index/pacing-model-development-cyber-capabilities",
    "暂停 RL 两周": "https://openai.com/index/pacing-model-development-cyber-capabilities",
    "The Defender's Window": "https://openai.com/index/the-defenders-window",
    "Path to Astra": "https://openai.com/index/path-to-astra",
    "GPT-6 Astra": "https://openai.com/index/gpt-6-astra",
    "Astra": "https://openai.com/index/safety-overview-gpt-6-astra",
    "GPT-6.1 Sol": "https://openai.com/index/introducing-gpt-6-1-sol",
    "GPT-6 Sol": "https://openai.com/index/introducing-gpt-6-sol-and-luna",
    "unwanted persistence": "https://deploymentsafety.openai.com/gpt-6-1-sol",
    "Misalignment reporting framework": "https://openai.com/index/model-misalignment-reporting-framework",
    "misalignment reports": "https://alignment.openai.com/misalignment-reports/",
    "DNS 外联": "https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/",
    "DNS": "https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/",
    "Towards safety cases for frontier AI training": "https://openai.com/index/towards-safety-cases-for-frontier-ai-training",
    "safety case": "https://openai.com/index/towards-safety-cases-for-frontier-ai-training",
    "metagaming": "https://alignment.openai.com/metagaming-latents",
    "Ironclad": "https://openai.com/index/advancing-computer-use-with-ironclad",
    "Asana": "https://openai.com/index/asana-browser-agent",
    "dots": "https://openai.com/index/introducing-dots",
    "Agents API": "https://openai.com/index/introducing-the-agents-api",
    "Codex harness": "https://github.com/openai/codex",
    "compaction 摘要": "https://alignment.openai.com/misalignment-reports/encouraging-deception-in-compaction-summaries/",
    "压缩摘要": "https://alignment.openai.com/misalignment-reports/encouraging-deception-in-compaction-summaries/",
    "agent 工作日": "https://openai.com/index/research-acceleration-view-inside-openai",
    "部署模拟": "https://openai.com/index/safety-overview-gpt-6-astra",
    # ---- Anthropic ----
    "Investigating unintended model actions": f"{A}/research/investigating-unintended-model-actions",
    "非预期行为": f"{A}/research/investigating-unintended-model-actions",
    "实网评测": f"{A}/research/investigating-unintended-model-actions",
    "Improving our alignment and security practices": f"{A}/news/improving-alignment-security-efforts",
    "超过 10%": f"{A}/news/improving-alignment-security-efforts",
    "评测伙伴": f"{A}/news/improving-alignment-security-efforts",
    "80 个可 hack 环境": f"{A}/news/improving-alignment-security-efforts",
    "Alignment assessment of cybersecurity incidents": f"{A}/research/alignment-assessment-cybersecurity-incidents",
    "Mythos 5": f"{A}/research/alignment-assessment-cybersecurity-incidents",
    "这只是模拟": f"{A}/research/alignment-assessment-cybersecurity-incidents",
    "这是模拟": f"{A}/research/alignment-assessment-cybersecurity-incidents",
    "偏置推理": f"{A}/research/alignment-assessment-cybersecurity-incidents",
    "三起评测越权事件": f"{A}/news/investigating-incidents-cybersecurity-evals",
    "4 起评测": f"{A}/research/alignment-assessment-cybersecurity-incidents",
    "GLM-5.3 网络能力评估": f"{A}/research/glm-5-3-and-the-spread-of-advanced-cyber-capabilities",
    "自复制": f"{A}/research/self-replicating-ai",
    "Scion": f"{A}/engineering/redesigning-source-control",
    "合并量": f"{A}/engineering/redesigning-source-control",
    "Model Hardware Standard": f"{A}/news/model-hardware-standard-research-preview",
    "MHS": f"{A}/news/model-hardware-standard-research-preview",
    "Project Swap": f"{A}/research/project-swap",
    "反蒸馏": f"{A}/research/distillation-defenses",
    "OSS Scanner": f"{A}/research/launching-opt-in-vuln-finding-service-for-open-source",
    "CyScenarioBench": f"{A}/news/cyber-verification-program",
    "CVP": f"{A}/news/cyber-verification-program",
    # ---- Google ----
    "Gemini 4 Argon": "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/",
    "Argon": "https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-4-argon/",
    "3.8 Flash": "https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/",
    "computer-use-preview": "https://github.com/google-gemini/computer-use-preview",
    "1754b3e": "https://github.com/google/adk-python/commit/1754b3e",
    "ADK": "https://github.com/google/adk-python",
    "Agent Anomaly Detection": "https://developers.googleblog.com/agent-anomaly-detection-now-in-private-preview-on-the-gemini-enterprise-agent-platform/",
    "双盲评测": "https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/",
    "Antigravity Teamwork": "https://blog.google/innovation-and-ai/technology/developers-tools/antigravity-teamwork-multi-agent/",
    "Teamwork": "https://blog.google/innovation-and-ai/technology/developers-tools/antigravity-teamwork-multi-agent/",
    "Interactions API": "https://github.com/googleapis/python-genai",
    "Gemini Spark": "https://blog.google/innovation-and-ai/products/gemini-app/gemini-app-now-on-windows/",
    "Private AI Compute": "https://deepmind.google/blog/advancing-private-ai-compute-with-secure-server-side-memory/",
    "Chrome auto browse": "https://blog.google/products-and-platforms/products/chrome/gemini-in-chrome-android-auto-browse/",
    "Tunix": "https://github.com/google/tunix",
    "AQuA": "https://developers.googleblog.com/the-outer-loop-insights-first-an-ambient-quality-agent-that-diagnoses-your-production-agent/",
    # ---- Meta / xAI / Mistral / Microsoft / NVIDIA / TML / AISI / HF ----
    "Muse Wonder": "https://about.fb.com/news/2026/10/introducing-muse-wonder-models/",
    "FocusBench": "https://research.meta.ai/blog/muse-wonder",
    "Active Focus": "https://research.meta.ai/blog/muse-wonder",
    "Sentinel": "https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse",
    "Meta Muse": "https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/",
    "Muse": "https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/",
    "Grok 4.7": "https://x.ai/news/grok-4-7",
    "Grok Build memory": "https://x.ai/news/grok-build-memory",
    "Team Bots": "https://x.ai/news/team-bots",
    "Grok Bot": "https://x.ai/news/designing-grok-bot",
    "Mistral Large 4": "https://mistral.ai/news/mistral-large-4",
    "Large 4": "https://mistral.ai/news/mistral-large-4",
    "Mistral × Mozilla": "https://mistral.ai/news/mistral-x-mozilla",
    "Firefox": "https://mistral.ai/news/mistral-x-mozilla",
    "Agentic Search": "https://mistral.ai/news/agentic-search",
    "Fortran": "https://mistral.ai/news/legacy-code-modernization",
    "Mistral 的迁移案例": "https://mistral.ai/news/legacy-code-modernization",
    "Agent Lightning": "https://github.com/microsoft/agent-lightning",
    "OpenForge": "https://github.com/microsoft/Orchard",
    "Orchard": "https://github.com/microsoft/Orchard",
    "Autopilot": "https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/",
    "Open Agent Safety Platform": "https://developer.nvidia.com/blog/nvidia-open-agent-safety-platform-a-reference-for-continuous-in-silicon-agent-monitoring/",
    "Sentry": "https://developer.nvidia.com/blog/nvidia-open-agent-safety-platform-a-reference-for-continuous-in-silicon-agent-monitoring/",
    "硬件看门狗": "https://developer.nvidia.com/blog/nvidia-open-agent-safety-platform-a-reference-for-continuous-in-silicon-agent-monitoring/",
    "OpenShell": "https://github.com/NVIDIA/OpenShell",
    "SMT 策略证明器": "https://github.com/NVIDIA/OpenShell",
    "NeMo Gym": "https://github.com/NVIDIA-NeMo/Gym",
    "NeMo Relay": "https://github.com/NVIDIA/NeMo-Relay",
    "Thinking Machines": "https://thinkingmachines.ai/news/putting-task-expertise-into-rl/",
    "BIRD-Platinum": "https://thinkingmachines.ai/news/putting-task-expertise-into-rl/",
    "AISI": "https://www.aisi.gov.uk/blog/gpt-6-astra-performs-unsanctioned-supply-chain-attacks-in-simulations",
    "恶意 PR": "https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities",
    "Building a more secure environment": "https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities",
    "optstop": "https://github.com/UKGovernmentBEIS/optstop",
    "Transect": "https://github.com/AI-Safety-Institute/transect",
    "HF 07-27 技术时间线": "https://huggingface.co/blog/agent-intrusion-technical-timeline",
    "RL Environments": "https://huggingface.co/blog/rl-environments",
    # ---- Chinese labs ----
    "Qwen-CUA": "https://github.com/xlang-ai/Qwen-CUA",
    "Qwen3.8-Max": "https://qwen.ai/blog?id=qwen3.8",
    "Kimi K3": "https://github.com/MoonshotAI/Kimi-K3",
    "AgentENV": "https://github.com/MoonshotAI/Kimi-K3",
    "Vals AI": "https://digg.com/ai/wo6cdxwj",
    "MiMo-V2.6": "https://arxiv.org/abs/2610.11959",
    "MiMo verl": "https://github.com/XiaomiMiMo/verl",
    "mimoagent": "https://github.com/XiaomiMiMo/mimoagent",
    "uni-agent": "https://github.com/XiaomiMiMo/uni-agent",
    "MiMo": "https://github.com/XiaomiMiMo/verl",
    "GLM-5.3": "https://github.com/zai-org/GLM-5",
    "ZCode": "https://github.com/zai-org/ZCode",
    "Qwen Code": "https://github.com/QwenLM/qwen-code",
    "DeepSeek Harness": "https://github.com/deepseek-ai/deepseek-harness",
    "V4.1-Flash": "https://github.com/deepseek-ai/FlashMLA",
    "MiniMax Code": "https://github.com/MiniMax-AI/MiniMax-Code",
    "Kimi Code": "https://github.com/MoonshotAI/Kimi-Code",
    "slime": "https://github.com/THUDM/slime",
    "Hy4": "https://github.com/Tencent-Hunyuan/Hy4-Preview",
    "HarnessDev": "https://arxiv.org/abs/2609.01437",
    "Qwen3.8-Flash-Next": "https://github.com/QwenLM/Qwen3.8-Flash-Next",
    # ---- papers (short names used in the reviews) ----
    "RecreationWorld": "https://arxiv.org/abs/2609.22000",
    "SoftwareGym": "https://arxiv.org/abs/2610.12611",
    "HybridCUA": "https://arxiv.org/abs/2609.38008",
    "AutoGUIWorld": "https://arxiv.org/abs/2610.01215",
    "DeskForge": "https://arxiv.org/abs/2610.02320",
    "CUA-SWE": "https://arxiv.org/abs/2609.32600",
    "OSWorld-Science": "https://arxiv.org/abs/2609.39903",
    "OSWorld-Pro": "https://arxiv.org/abs/2609.24890",
    "EvoSkill-GUI": "https://arxiv.org/abs/2609.17653",
    "ExpActivator": "https://arxiv.org/abs/2609.33304",
    "IterSynth": "https://arxiv.org/abs/2609.29444",
    "RDPO": "https://arxiv.org/abs/2609.29444",
    "HazardAuditor": "https://arxiv.org/abs/2609.15134",
    "GuardPO": "https://arxiv.org/abs/2609.15134",
    "AdvSim2Real": "https://arxiv.org/abs/2610.08773",
    "AREX-2": "https://arxiv.org/abs/2609.38288",
    "Context Language Models": "https://arxiv.org/abs/2609.37725",
    "CLM": "https://arxiv.org/abs/2609.37725",
    "CodeMidas": "https://arxiv.org/abs/2609.22068",
    "GAGAR": "https://arxiv.org/abs/2609.32577",
    "Trace2Env": "https://arxiv.org/abs/2610.06100",
    "SRD": "https://arxiv.org/abs/2610.08077",
    "VHD-Play": "https://arxiv.org/abs/2609.27321",
    "PTGS": "https://arxiv.org/abs/2610.01509",
    "Sharpening Tax": "https://arxiv.org/abs/2610.01509",
    "Schrödinger": "https://arxiv.org/abs/2609.27891",
    "Harness 设计研究": "https://arxiv.org/abs/2609.20804",
    "Harness Design": "https://arxiv.org/abs/2609.20804",
    "WebArena-Lite": "https://arxiv.org/abs/2610.01491",
    "Emergent Collusion": "https://arxiv.org/abs/2609.24967",
    "Covert Assistance": "https://arxiv.org/abs/2609.39050",
    "UndoBench": "https://arxiv.org/abs/2610.05622",
    "ProgramGym": "https://arxiv.org/abs/2610.13395",
    "Taste-Bench": "https://arxiv.org/abs/2609.25804",
    "TerminalHorizon": "https://arxiv.org/abs/2610.13166",
    "Marathoner": "https://arxiv.org/abs/2609.34378",
    "VeriHarness": "https://arxiv.org/abs/2610.00972",
    "TraceDance": "https://arxiv.org/abs/2609.33295",
    "SLCA-GRPO": "https://arxiv.org/abs/2609.29050",
    "HyperBrowseComp": "https://arxiv.org/abs/2610.03574",
    "NeMo-DCR": "https://arxiv.org/abs/2610.08430",
    "TRACE": "https://arxiv.org/abs/2610.07767",
    "False Frontiers": "https://arxiv.org/abs/2609.39102",
    "co-cheating": "https://arxiv.org/abs/2609.39102",
    "RSR": "https://arxiv.org/abs/2610.02826",
}


def link_block(text: str, linked: set[str]) -> tuple[str, int]:
    """Wrap the first unlinked mention of each known entity (longest names first) in a markdown link."""
    n = 0
    for name in sorted(ENTITIES, key=len, reverse=True):
        if name in linked:
            continue
        # skip mentions already inside link text / urls; require non-word boundaries for ASCII names
        pat = re.compile(rf"(?<![\w\[/.-]){re.escape(name)}(?![\w\]-])" if name.isascii() else re.escape(name))
        m = pat.search(text)
        if not m:
            continue
        # don't link inside an existing [..](..) span
        before = text[: m.start()]
        if before.count("[") > before.count("]") or before.count("(http") > before.count(")"):
            continue
        text = f"{text[: m.start()]}[{name}]({ENTITIES[name]}){text[m.end():]}"
        linked.add(name)
        n += 1
        if n >= 3:
            break
    return text, n


def process(path: Path) -> tuple[int, list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines(True)
    changed, unresolved = 0, []
    for n, kind, text, heads in blocks(lines):
        if URL.search(text):
            continue
        i = n - 1
        new, k = link_block(lines[i], set())
        if k:
            lines[i] = new
            changed += 1
        elif kind != "para" or len(text) > 30:
            unresolved.append(f"{path.name}:{n}: {text[:100]}")
    path.write_text("".join(lines), encoding="utf-8")
    return changed, unresolved


if __name__ == "__main__":
    for p in sys.argv[1:]:
        c, u = process(Path(p))
        print(f"{p}: linked {c} blocks; {len(u)} still unresolved")
