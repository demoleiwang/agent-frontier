# Chinese frontier labs: agent-relevant releases, 2026-08-14 to 2026-10-14 (deep notes)

Compiled 2026-10-14. Scope: computer-use / GUI / browser agents, agentic RL (environments, RL infra, reward design), agent evals and safety, and agent infra (coding-agent harnesses).

## How this was sourced (read first)

- **Primary text read in full.** I could not reach lab sites, huggingface.co or arxiv.org. Instead I made blobless `git clone`s of official GitHub repos (no checkout, no code executed) and read the READMEs, configs, docs and commit history with `git show`. Several repos ship the full technical-report PDF, and I extracted those with `pdftotext`:
  - Qwen-CUA report (24 pp)
  - Kimi K3 report
  - Qwen3.8-Flash-Next architecture report

  Benchmark charts that exist only as images (GLM-5.3, GLM-5.3-Flash and the Hy4 appendix) were downscaled and read visually.
- **Dates.** Repo commit timestamps give an upper bound on dates. They are used as the date when they match README "News" lines.
- **Source-of-substance labels used below:**
  - `github-fulltext`: the substance comes from official repo files or report PDFs that I read in full.
  - `official-search-extended`: the substance comes from official pages (docs.z.ai, api-docs.deepseek.com, qwen.ai, arXiv) as quoted in extended web-search results. I did not read those pages directly.
  - `third-party-corroborated`: the substance comes only from secondary coverage. I note agreement or conflict between sources.
- **Vendor numbers.** All benchmark numbers are **vendor-reported** unless marked otherwise. Harness, effort and turn limits are given where the source states them.
- **Date confidence:** H = official repo or README dated entry; M = official page quoted via search, or several consistent secondary sources; L = secondary sources that conflict.

---

## 0. Cross-lab takeaways for GUI/CUA and agentic-RL research

1. **Qwen-CUA is the most detailed open recipe for pixel-only computer use in this period.** It covers:
   - a 20-screenshot active window with 10-step block folding, which keeps the KV-cache prefix stable;
   - training slices made with the same fold operator, each inheriting the terminal reward;
   - SAPO with asymmetric gate temperatures;
   - a pass@8 task filter (keep 0<c<8);
   - about 100k vCPUs, about 40k verifiable tasks, 512 H200s, and about 61k GPU-hours per RL run.

   Results: 86.2 on OSWorld-Verified (Max: 87.6) and 18.5/48.4 binary/partial on OSWorld 2.0. Weights went open on 2026-08-26. OSWorld-Verified is near saturation (Kimi K3 84.8, Qwen3.8-Max about 86.1, MiMo-V2.6-Pro about 82.0). The real headroom is in long-horizon work (OSWorld 2.0 binary is about 20%), personalization (MyPCBench) and prompt-injection robustness (RedTeamCUA ASR is 16.4 for Qwen-CUA vs 0.7 for Opus 4.8).
2. **Harness diversity has become an explicit RL design axis.**
   - Kimi K3 trains in a "unified white-box RL environment" that composes harness modules (tools, system prompts, context management, skills, memories, subagents) to imitate Kimi Code, Claude Code, Codex, OpenClaw and Hermes.
   - Xiaomi's open RL stack ships Claude Code, Codex, mini-bash and MiMo-code harness configs plus a `group_advantage_by_harness` flag.
   - ByteDance Seed's HarnessDev evaluates models on the harness they *build*.
   - Hy4 and Kimi report scores per harness.
3. **The most concrete open RL artifacts in the window are the reward-design and credit-assignment code** in Xiaomi's `XiaomiMiMo/verl` fork (2026-09-21):
   - segment-level tool-call-error penalties (`monitor/mask/adv_reduction/adv_set/adv_signed`);
   - a sign-aware mass-conserving advantage rebalance;
   - an n-gram repetition early-stop;
   - an experimental "deep-failure mask";
   - infra-failure vs wrong-answer separation;
   - a VLM group-pick grader for web design that picks only "clearly better" and "clearly worse" screenshots inside a group of 16.

   Third-party caveat (Vals AI): about two-thirds of the released coding tasks leak the fix through git history.
4. **Every lab now ships an open-source coding-agent harness, and computer use is being bolted onto them.**
   - DeepSeek Harness (`dsh`, MIT, 2026-08-13) is "everything is a plugin". It added computer-use and browser-use provider packages on 2026-09-12/13.
   - ZCode (Z.ai, Apache-2.0, 2026-09-21) added an accessibility-first `zcode-cua-plugin` in v3.15.1 (2026-10-10).
   - Qwen Code shipped a versioned CUA SDK/driver (2026-08-23) and moved computer use to a bundled skill (2026-08-24).
   - MiniMax Code published its source snapshot (MIT) on 2026-09-18.
   - Kimi Code replaced kimi-cli.

   The harness-side CUA designs are AX-tree/DOM-first. The model-side CUA research (Qwen-CUA) is pixel-only. That contrast is worth tracking.
5. **Cyber capability is now reported as an emergent byproduct of agentic RL, with gating attached.**
   - GLM-5.3: "cyber capability developed faster than we expected". It is SOTA on CyberGym, more than doubles GLM-5.2 on exploitation, and launched without a public API at first.
   - Kimi K3: two-tier cyber eval. It solves 14/36 expert exploit tasks; joint UK AISI + NIST CAISI testing gave 0/41 arbitrary-code-execution on end-to-end exploit completion.
   - MiMo-V2.6 includes an ARVO vulnerability-reproduction RL environment.
6. **Long-context efficiency for agents is the dominant architecture theme.**
   - GLM-5.3-Flash: sparse+linear hybrid plus mHC.
   - Qwen3.8-Flash-Next: GDN + Qwen Sparse Attention, Gated Residual and n-gram embeddings.
   - DeepSeek V4.1-Flash: KV-cache compression. FlashMLA shows a 528 B/token FP8 cache (288 B/token FP4 extra cache).
   - Kimi K3: KDA + Gated MLA, with an external KV pool for 1M-context RL.
   - Hy4: Gated DSA + IndexCache + identity Hyper-Connections.

---

## 1. Inventory (in window unless flagged)

| Lab | Item | Date (conf.) | Official URL(s) | Repo | Agent-relevant? |
|---|---|---|---|---|---|
| Z.ai | GLM-5.3 (API/coding plan launch; open weights about 2 weeks later) | API 2026-08-14 (M); weights/README 2026-08-27 (H) | https://z.ai/blog/glm-5.3 ; https://docs.z.ai/guides/llm/glm-5.3 | https://github.com/zai-org/GLM-5 | Yes (coding agents, cyber) |
| Z.ai | GLM-5.3-Flash (+ FlashX API tier) | 2026-08-26 (H) | https://z.ai/blog/glm-5.3-flash ; https://docs.z.ai/guides/vlm/glm-5.3-flash | zai-org/GLM-5 (GLM-V repo points there) | Yes |
| Z.ai | GLM-V repo frozen ("no longer maintained", redirect to GLM-5) | 2026-09-02 (H) | — | https://github.com/zai-org/GLM-V | Minor |
| Z.ai/THUDM | slime v0.3.2 → v0.4.0 (RL framework behind GLM-5.x) | v0.3.2 2026-08-28; v0.4.0 2026-10-09 (H) | https://thudm.github.io/slime/ | https://github.com/THUDM/slime | Yes (RL infra) |
| Z.ai | ZCode open-sourced (desktop/web/TUI coding agent); v3.14.3; v3.15.1 adds CUA plugin | 2026-09-21 / 09-23 / 10-10 (H) | — | https://github.com/zai-org/ZCode | Yes (harness, CUA) |
| Alibaba Qwen | Qwen-CUA report (arXiv 2608.02352) | 2026-08-03 (H) **pre-window context** | https://arxiv.org/abs/2608.02352 | https://github.com/xlang-ai/Qwen-CUA | Yes (core) |
| Alibaba Qwen | Qwen-CUA weights released | 2026-08-26 (H) | https://huggingface.co/xlangai/Qwen-CUA | xlang-ai/Qwen-CUA | Yes (core) |
| Alibaba Qwen | Qwen3.8-Max blog "A New Bar for Coding and Cowork" | Aug 2026 (L: sources say 08-02/03 or later); open 2.4T-A95B weights 2026-08-12 (H) | https://qwen.ai/blog?id=qwen3.8 | https://github.com/QwenLM/Qwen3.8 | Yes |
| Alibaba Qwen | Qwen3.8-27B open weights (Apache-2.0 per secondary sources) | 2026-08-14 (H) | HF collection Qwen/qwen38 | QwenLM/Qwen3.8 | Yes |
| Alibaba Qwen | Qwen3.8-Flash-Next (Qwen4 architecture preview) + tech report | 2026-08-26 (H) | https://qwen.ai/blog?id=qwen3.8-flash-next | https://github.com/QwenLM/Qwen3.8-Flash-Next | Partly (efficiency; agent evals in blog only) |
| Alibaba Qwen | Qwen3.8-Max-0902 snapshot | 2026-09-02 (M) | qwen.ai (via search) | — | Yes |
| Alibaba Qwen | Qwen3.8-Omni-Flash (+ arXiv 2609.25611 "Towards Native Omni-Modal Agents") | 2026-09-18 (M; OpenRouter lists 09-21) | qwen.ai (via search) | — (no open weights) | Yes (multimodal agents) |
| Alibaba Qwen | Qwen-Image-2.1 / -Turbo | 2026-09-20 / 10-09 (H) | https://qwen.ai/blog?id=qwen-image-2.1 | https://github.com/QwenLM/Qwen-Image-2.1 | No |
| Alibaba Qwen | Qwen Code: versioned Computer-Use SDK/driver; CUA moved to bundled skill; harness-invariance eval doc | 2026-08-23 / 08-24 / 10-14 (H) | https://qwenlm.github.io/qwen-code-docs/ | https://github.com/QwenLM/qwen-code | Yes (harness, CUA) |
| DeepSeek | V4-Pro-0813 GA + **DeepSeek Harness v0.1** (MIT) | 2026-08-13 (M) **one day before window** | https://api-docs.deepseek.com/news/news260813/ | https://github.com/deepseek-ai/deepseek-harness | Yes (harness) |
| DeepSeek | V4-Flash-Vision-Exp | 2026-08-21 (L) | (API) | — | Partly (multimodal agent) |
| DeepSeek | **V4.1-Flash** (+ arXiv 2609.19969 "Pushing the Limits of KV Cache Compression") | 2026-09-10 (H via FlashMLA news + M changelog) | https://api-docs.deepseek.com/updates/ | FlashMLA/DeepGEMM (no model repo found) | Yes (agent prefill efficiency) |
| DeepSeek | FlashMLA V4.1 kernels; Ascend 950 kernels; DeepGEMM releases; TileKernels v2.0/v2.1 | 09-10, 09-30, 10-14 (H) | — | deepseek-ai/FlashMLA, /DeepGEMM, /TileKernels | Infra |
| DeepSeek | Harness adds computer-use / browser-use packages; release 0.2.1-alpha.2 | 2026-09-12/13; 10-09 (H) | https://deepseek-harness.github.io/deepseek-harness/ | deepseek-ai/deepseek-harness | Yes |
| Moonshot | Kimi K3 (open 2.8T) + full tech report | 2026-07-27 (H) **pre-window context** | https://www.kimi.com/blog/kimi-k3 | https://github.com/MoonshotAI/Kimi-K3 | Yes (core) |
| Moonshot | Kimi K2.8 Preview (Kimi Code / app; `kimi-for-coding`) | 2026-09-11 (M) | (kimi.com; via search) | — | Yes |
| Moonshot | kimi-cli deprecated → Kimi Code CLI migration | 2026-09-01 / 09-22 (H) | https://moonshotai.github.io/kimi-code/en/ | MoonshotAI/kimi-cli, MoonshotAI/Kimi-Code | Harness |
| MiniMax | MiniMax-M3 (428B-A23B, MSA) | 2026-06-01 (H) **pre-window context** | https://platform.minimax.io | https://github.com/MiniMax-AI/MiniMax-M3 | Context |
| MiniMax | MiniMax Code CLI source snapshot open (MIT) | 2026-09-18 (H) | https://agent.minimax.io/docs/cli/quick-start | https://github.com/MiniMax-AI/MiniMax-Code | Yes (harness) |
| MiniMax | M3.1-Flash-Preview inside MiniMax Code (no card) | 2026-09-27 (M/L) | (X post via search) | — | Yes (weakly documented) |
| Xiaomi | **MiMo-V2.6 Pro / Flash / Distill-Qwen-9B + open RL environments + RL code** (arXiv 2610.11959) | 2026-09-21/22 (H for code; M for release notes) | https://mimo.mi.com/docs/en-US/news (via search) | https://github.com/XiaomiMiMo/verl , /mimoagent , /uni-agent | Yes (core) |
| StepFun | Step 5 Preview (600B-A27B, API-only; weights promised 10-15) | 2026-09-18 to 09-20 (L) | (stepfun; via search) | none found | Partly |
| ByteDance Seed | HarnessDev (arXiv 2609.01437) | 2026-09-01 (M) | https://arxiv.org/abs/2609.01437 ; project page self-developing-agents.github.io (unverified) | none found | Yes (harness eval) |
| ByteDance | UI-TARS-desktop agent-server security hardening (no new UI-TARS model) | 2026-09-24, 10-08 (H) | — | https://github.com/bytedance/UI-TARS-desktop | Minor (CUA safety ops) |
| Tencent Hunyuan | Hy4 preview (770B-A49B, Apache-2.0) | 2026-08-28 (H) | (tencent; via search) | https://github.com/Tencent-Hunyuan/Hy4-Preview | Yes (agent evals) |

Searched for and **not found in the window**:
- No new UI-TARS model; the bytedance/UI-TARS repo was last updated 2025-09.
- No Seed 2.x agent model (Seed 2.1 was June; SeedRealtime was 08-05).
- No MiniMax-M3.1 model card.
- No StepFun GitHub repo for Step 5.
- No DeepSeek model repo for V4.1 (only the kernel repos).
- No Tencent CUA-specific release; Hy3 was July.

---

## 2. Deep notes

### Z.ai / Zhipu

#### 2.1 GLM-5.3 — "every gain comes from post-training"
- **Date:** API/Coding-Plan launch 2026-08-14 (M, docs.z.ai via search). Open weights and README update 2026-08-27 (H, commit `153ca46 "update GLM-5.3"`).
- **URLs:** https://z.ai/blog/glm-5.3 · https://docs.z.ai/guides/llm/glm-5.3 · https://github.com/zai-org/GLM-5
- **Source:** github-fulltext (README + benchmark chart image). Cyber disclosure details are official-search-extended or third-party-corroborated.
- **Substance:**
  - Same base model as GLM-5.2 (744B-A40B, DSA-based). README: "GLM-5.3 uses the same base model as GLM-5.2 — every gain comes from post-training." Weights are FP8 and BF16.
  - Coding: "+50% over GLM-5.2 on our in-house Z.ai Code Bench". Claims open-source SOTA on Terminal Bench 3.0 and Agents' Last Exam.
  - Emergent cyber, quoted: "As we scaled post-training, cyber capability developed faster than we expected. GLM-5.3 is state of the art on CyberGym … its gains are largest further up the exploitation chain, where it more than doubles GLM-5.2 on exploitation benchmarks."
  - Search-sourced cyber context (M/L): Z.ai added vulnerability-discovery environments to post-training, and capability moved toward full exploit chains. CyberGym is 84.5 vs 77.2 for GLM-5.2. Z.ai reports 2,436 vulnerabilities across 269 projects (1,097 medium-to-high) with a "Security Disclosure Ledger". Access at launch was limited to the GLM Coding Plan and ZCode, with no public API; weights followed about 2 weeks later "pending safety evaluation".
  - Vendor chart (`resources/bench_53_2.png`), GLM-5.3 / GLM-5.2 / Kimi K3 / Fable 5 / GPT-5.6 Sol:

    | Benchmark | GLM-5.3 | GLM-5.2 | Kimi K3 | Fable 5 | GPT-5.6 Sol |
    |---|---|---|---|---|---|
    | Terminal Bench 3.0 | 28.3 | 4.6 | 17.4 | 33.7 | 34.6 |
    | DeepSWE | 66.9 | 46.2 | 67.5 | 69.7 | 72.7 |
    | Agents' Last Exam (CLI) | 28.5 | 23.8 | 27.6 | 23.8 | 28.6 |
    | AutomationBench | 48.2 | 26.2 | 46.7 | 46.2 | 45.8 |
    | HLE w/ tools | 62.5 | 54.7 | 59.8 | 63.9 | 64.5 |
    | GDPval-AA v2 (Elo) | 1769 | 1508 | 1682 | 1743 | 1730 |

    The chart gives no harness or effort details.
  - Inference: `reasoning_effort` ∈ {low, high, max}, default max ("For benchmark and leaderboard reproduction, keep the default max"). The chat template defaults `clear_thinking=false`, so thinking is preserved across turns for agents.
  - RL framework: slime (see 2.3). Fine-tuning is supported via slime v0.3.0+ and ms-swift v4.4.0+.
- **What is new vs GLM-5.2:** no architecture change. The jump on Terminal Bench 3.0 (4.6 → 28.3) and AutomationBench (26.2 → 48.2) is attributed purely to post-training.
- **Caveats:**
  - All numbers are vendor-reported; Z.ai Code Bench is in-house.
  - Sources disagree on total parameters (743B vs 753B); the README says 744B-A40B.
- **Implications:**
  - This is a clean "post-training-only" data point. Long-horizon terminal/automation and cyber gains came from environment and RL scaling on a fixed base. Use it as a reference when attributing CUA/agent gains to RL vs pretraining.
  - Emergent offensive capability from vulnerability-discovery environments argues for building gating/eval (exploit-chain tiers) into any agentic-RL environment suite that includes security tasks.

#### 2.2 GLM-5.3-Flash — first hybrid sparse+linear attention GLM, plus mHC
- **Date:** 2026-08-26 (H: GLM-5 commit `f6adb53`; GLM-V README "2026/08/26: We released GLM-5.3-Flash, our first open-source natively multimodal model").
- **URLs:** https://z.ai/blog/glm-5.3-flash · https://docs.z.ai/guides/vlm/glm-5.3-flash
- **Source:** github-fulltext (README + chart). The efficiency ratios are official-search-extended.
- **Substance:**
  - New base model: 320B-A18B, FP8 and BF16. It is the first natively multimodal GLM-5 model, trained on a 30T-token multimodal pre-training corpus.
  - Architecture: "For the first time in the GLM series, we introduce a hybrid architecture combining sparse and linear attention." Docs (via search): linear attention handles local dependencies through state modelling, while sparse attention retrieves global context through a lightweight indexer. Attention compute is 3.01× lower and KV cache 4.44× lower vs GLM-5.3.
  - Adopts **Manifold-Constrained Hyper-Connections (mHC)** "to further improve scaling efficiency".
  - Claims it beats GLM-5.2 "at one-tenth the price", approaching Claude Opus 4.8 on coding/agentic benchmarks.
  - Vendor chart (`bench_53.png`), GLM-5.3-Flash vs GLM-5.2 / DeepSeek-V4-Vision-Exp / Claude Opus 4.8 / GPT-5.6 Terra / Gemini 3.7 Flash:
    - Terminal Bench 2.1: 84.3 vs 81.0 / 83.9 / 85.0 / 87.4 / 85.8
    - DeepSWE v1.1: 63.4 vs 46.2 / 59.3 / 58.0 / 69.6 / 65.3
    - Agents' Last Exam: 26.3 vs 20.4 / 27.3 / 27.0 / 28.0
    - AutomationBench v1.0.6: 48.8 vs 26.2 / 38.8 / 41.0 / 37.2 / 52.3
    - HLE w/ tools: 55.3 vs 54.7 / 55.1 / 57.9
    - GDPval-AA v2: 1773 vs 1504 / 1675 / 1582 / 1571 / 1527
  - Serving: SGLang, vLLM, TokenSpeed, Transformers (`glm5_next`), KTransformers, Unsloth and vLLM-Ascend.
- **Caveats:**
  - No OSWorld or GUI numbers are given, even though it is natively multimodal.
  - FlashX (an API tier) is not documented in the repo.
- **Implications:**
  - An 18B-active, natively multimodal open model with hybrid attention is a candidate base for open CUA RL on a cost budget. The cheaper long-context KV directly lowers the cost of screenshot-heavy trajectories.
  - Z.ai has not published GUI-agent evals for it; this is an open gap to measure.

#### 2.3 slime (THUDM) v0.3.2 → v0.4.0 — RL infra behind GLM-5.x
- **Date:** v0.3.2 2026-08-28; v0.4.0 2026-10-09 (H).
- **Repo:** https://github.com/THUDM/slime
- **Source:** github-fulltext (README + commit log).
- **Substance:**
  - README: "slime is the RL framework behind GLM-5.3-Flash, GLM-5.3, GLM-5.2, GLM-5.1, GLM-5, GLM-4.7…". It is Megatron training plus SGLang rollout, connected through one Data Buffer.
  - In-window features:
    - streaming external rollouts (09-03);
    - aborting timed-out SGLang requests through router workers (09-03, agent tail latency);
    - distributed fully-async rollout plus **straw** (persistent prompt tasks, rollout continuations and training batches on JuiceFS) (09-28);
    - legacy async entrypoint removed (09-18);
    - Ascend NPU, MUSA and Biren SUPA backends;
    - forced UE8M0 FP8 scales (08-26).
  - New agentic RL example: `examples/coding_agent_rl`, "Qwen3.8-27B coding-agent RL on Xiaomi MiMo SWE data, using sunabako sandboxes, official test rewards, and token-correct trajectories". The sunabako agent E2E was added 2026-10-10.
  - Other agentic examples: multi_agent, search-r1, fully_async. The ecosystem section lists Alibaba Accio's **Dressage** (Paddock/Sandbox/Proxy layers, black-box agents, token-level trajectory capture).
- **Implications:**
  - Cross-lab reuse is visible: Zhipu's RL framework ships a recipe on Xiaomi's released SWE RL data and a Qwen model. Open RL environment data is becoming shared infrastructure.
  - "Token-correct trajectories" plus fully-async rollout with persistent continuations is the pattern needed for long CUA episodes.

#### 2.4 ZCode open-source (Apache-2.0) and its Computer-Use plugin
- **Date:** open-sourced 2026-09-21; v3.14.3 2026-09-23; v3.15.1 2026-10-10 (H).
- **Repo:** https://github.com/zai-org/ZCode
- **Source:** github-fulltext.
- **Substance:**
  - An "AI programming workbench" with a desktop (Electron) app, web UI and terminal agent. The agent CLI and runtime live in `apps/zcode-cli/`.
  - Plugin packages include `browser-use-plugin`, `zcode-cua-plugin`, `android-emulator-plugin`, `ios-simulator-plugin`, `dynamic-workflow`, plus document, pdf, presentations and spreadsheets plugins.
  - **`zcode-cua-plugin` (first appears in v3.15.1, 2026-10-10):** "Read or operate the UI of native apps." Design rules:
    - "Accessibility first": act on AX-tree elements by index; prefer `setValue` over typing; keyboard is the fallback.
    - Strategy options are `auto | a11y | event`.
    - "Main agent only. Never delegate Computer Use to a subagent."
    - AppleScript/osascript/shell UI automation is forbidden unless the user asks.
    - Every call bootstraps a fresh JS worker (`node_repl`); UI state persists host-side.
  - **Browser use:** backends are `iab` (in-app browser), `extension` and `cdp` (headless Chromium). The default observation is `playwright.domSnapshot()` (a compact AI/ARIA tree, not outerHTML). Rules include "At most one state-changing action per observation cycle" and "judge an action by whether its expected effect appeared".
  - GLM-5.3 launched first on ZCode and the Coding Plan (see 2.1).
- **Implications:**
  - Z.ai's production CUA path is AX-tree/DOM-first, not pixel-first, which is the opposite of Qwen-CUA. If you RL a GUI policy for these harnesses, the observation space is the AX tree plus optional screenshots.
  - The "one state-changing action per observation" and "verify effect, not tab list" rules are harness-level reward-hacking and false-success mitigations worth copying into CUA eval scaffolds.

### Alibaba Qwen

#### 2.5 Qwen-CUA: Native Computer Use for (almost) Everything (key context)
- **Date:** report dated 2026-08-03 (arXiv 2608.02352). Repo initial release 2026-07-31. **Weights released 2026-08-26** (commit "Mark model weights as available"). (H)
- **URLs:** https://github.com/xlang-ai/Qwen-CUA · https://huggingface.co/xlangai/Qwen-CUA · https://arxiv.org/abs/2608.02352
- **Source:** github-fulltext (full 24-page PDF in `paper/`, README, demo README).
- **Substance:**
  - **Interface:**
    - The backbone is a 397B-A17B Qwen MoE; Qwen-CUA-Max is >1T.
    - Observation is screenshots only. There is no DOM, accessibility tree, shell or task API.
    - Action space (App. A): key, key down/up, type, mouse move, left/right/middle/double/triple click, left-click drag, left mouse down/up, scroll, hscroll, screenshot, wait, terminate, call_user.
    - The demo uses a normalized 0..999 coordinate grid.
  - **Context management:**
    - Up to 20 active screenshots. When the active window exceeds 20, the folded prefix advances by **10 at once**.
    - Folded screenshots become a fixed text placeholder (`<image collapsed>`); their reasoning and actions stay in context.
    - Because the boundary moves only every 10 steps, steps 21–30 share a prefix, which improves KV-cache reuse. The deterministic folding needs no summarizer.
  - **Training-time trajectory slicing:**
    - Uses the same fold operator, slicing every 10 turn-pairs under a 144K-token cap.
    - Each slice inherits the full episode reward. The loss covers only active model-generated reasoning and tool-call tokens.
    - The result is denser reuse of sparse terminal rewards without step-level reward design.
  - **Infrastructure and data:**
    - Alibaba Cloud ECS fleet with access to about 100k vCPUs and tens of thousands of concurrent environments. During RL, up to 2,000 environments are active at >75% utilization.
    - Environments: controllable mock web services (state injection, inspection, reset, session isolation) plus broad desktop apps (Gym-Anything-style packaged apps, including professional/scientific software).
    - About 40k verifiable tasks in three classes: environment-operation tasks from feature taxonomies; user-interactive tasks with a simulated user holding bounded knowledge (OSWorld 2.0-style); and long-horizon tasks built by **phase-state chaining**, where each phase's verified end state is serialized to initialize the next.
    - Human trajectories in personalized desktops and pro software (CAD, Blender), with model-generated step rationales filtered for consistency.
  - **RL algorithm:**
    - RLVR with state-based rewards r∈[0,1]; partial credit is allowed when meaningful.
    - SAPO: a smooth sigmoid gate instead of clipping, with τ_pos=1.0 and τ_neg=1.05. Negative-advantage tokens decay faster, which the authors found important for long multimodal trajectories and the MoE backbone.
    - Group size G=16 from 20 oversampled rollouts; invalid ones (timeouts, malformed calls) are dropped. There is no variance filtering inside groups.
    - Outer batch 128 prompts, mini-batch 32, lr 1e-6 constant, 1 epoch per batch, 1,000 updates.
    - Max 100 turns per episode in training; 2,048 tokens per turn.
  - **Compute:**
    - 512 H200 (32 nodes training, 32 rollout). Training TP2/EP8/CP4/PP8; rollout SGLang TP8.
    - Async dispatch ratio 2.35, with a staleness cap of 4 optimizer steps.
    - About 5 days and about 61,440 H200 GPU-hours per full 1,000-update run.
    - In the final run, held-out score rose from 0.734 to 0.770 at update 800, which was selected.
  - **Iteration ("self-improvement cycles"):**
    - Each run's model exposes failed SFT queries and weak domains. Teacher policies re-roll those queries, new human data is added, and every SFT run restarts **from the same mid-training checkpoint** rather than from the last agent checkpoint.
    - The RL pool is then recalibrated with 8 trial rollouts per query, keeping only 0 < successes < 8.
    - Four iterations are reported before the final model. The authors warn the curves are "not controlled convergence or scaling".
  - **Results** (pure CU setting; comparison models run by the authors: Qwen3.7 non-thinking, GPT-5.5 xhigh, Opus 4.8 max):
    - OSWorld-Verified 86.2 (359/360 tasks executed, 100-step limit). Qwen3.7 73.3, GPT-5.5 78.7, Opus 4.8 83.4. Max: 87.6.
    - OSWorld 2.0 binary/partial 18.5/48.4 (Max 21.2/53.3), vs Opus 20.3/54.8 and GPT-5.5 13.9/47.5.
    - MyPCBench perfect-task rate 58.7 (rubric 84.3; 1280×800, 200-turn limit, no Bash).
    - MacAgentBench 69.2 pass@1 (30 bare-metal Mac minis; 12 clock tasks scored 0 by the evaluator although they look correct, and the official score is retained).
    - Gym-Anything 46.3 (1,295 tasks from 97 envs, 1600×900, 150 steps; Claude Sonnet 4.6 as VLM verifier).
    - ScienceBoard 64.5. WebArena 64.16.
  - **Efficiency and caveats:**
    - OSWorld-Verified uses about 3.6k output tokens per task (14.2 steps), vs Opus 4.8 at 83.3 with 21.8k tokens.
    - On OSWorld 2.0, Qwen-CUA averages 218.9 turns vs 105.7 for Opus and 83.5 for GPT-5.5, because it emits a single action per turn while the proprietary APIs batch actions.
  - **Safety and hybrid use:**
    - RedTeamCUA task success/ASR is 74.0/16.4 (Qwen3.7 70.5/36.6, GPT-5.5 75.7/15.6, Opus 4.8 80.7/0.7). The authors note residual risk and that Rocket.Chat ASR is confounded by execution failures.
    - Adding Bash on MyPCBench cut turns from 63.6 to 49.1 but lowered perfect-task rate from 58.7 to 55.1. The authors' reading: the model has not learned when to route to Bash.
    - The demo's safety gates pause password entry, uploads, downloads, form submission and cross-origin navigation for operator review. Private, loopback and credential-bearing URLs are blocked, and custom-URL runs are marked "unverified".
- **Implications:**
  - Fold-and-slice with block-aligned prefixes is a ready-to-copy recipe for making long CUA RL feasible: train–inference consistent, cache-friendly, and with no summarizer model. The pass@8 band filter plus restarting SFT from a fixed mid-train checkpoint is a concrete, reproducible "iterate the data, not the weights" loop.
  - Open problems are named explicitly: (a) interface turn-efficiency (single-action turns); (b) learned routing between GUI and Bash/tools, where naive hybrid use hurts accuracy; (c) prompt-injection robustness, where an 16.4 vs 0.7 ASR gap to Opus remains. Each is a natural RL-environment target.

#### 2.6 Qwen3.8 family (Max / 2.4T-A95B open / 27B / Max-0902)
- **Dates:**
  - Blog "Qwen3.8-Max: A New Bar for Coding and Cowork": August 2026 (L on exact day).
  - Qwen3.8-2.4T-A95B open weights 2026-08-12 (H, README News).
  - Qwen3.8-27B 2026-08-14 (H).
  - README updated 2026-08-17 (H).
  - Max-0902 snapshot 2026-09-02 (M).
- **URLs:** https://qwen.ai/blog?id=qwen3.8 · https://github.com/QwenLM/Qwen3.8 · https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B
- **Source:** github-fulltext (README: features, dates, deployment). Benchmarks are official-search-extended (Qwen tables quoted by DataCamp, CellCog, openlm.ai, DataLearner); they are not in the GitHub README, which defers to HF model cards.
- **Substance:**
  - README: "For the first time, Qwen3.8 brings a Qwen-Max-class model to open release. Built on the architectural foundation of Qwen3.5" (Gated DeltaNet + sparse MoE hybrid).
  - Feature bullets: "Agent Execution: stronger autonomous planning and better handling of environment feedback"; "Downstream Compatibility: broader support for popular harnesses"; `reasoning_effort` plus `preserve_thinking`.
  - The Qwen3.5 lineage notes, which still apply: RL "scaled across million-agent environments with progressively complex task distributions" and "asynchronous RL frameworks supporting massive-scale agent scaffolds and environment orchestration".
  - Deployment flags use `--tool-call-parser qwen3_coder` and a 262,144 context. Product surfaces are Qoder, QwenWork ("one-stop AI working platform"), QwenCloud (OpenAI- and Anthropic-compatible) and Qwen Code.
  - Agent evals (vendor; via search):

    | Benchmark | Qwen3.8-Max | Qwen3.8-Max-0902 | Comparisons |
    |---|---|---|---|
    | Terminal-Bench 2.1 | 86.6 | — | GPT-5.6 Sol 88.8; Opus 4.8 / Fable 5 84.6 |
    | SWE-bench Pro | 67.7 | — | Fable 5 80.0 |
    | CoWorkBench (in-house) | 74.8 | 76.1 | Opus 4.8 72.3; Fable 5 75.9; Opus 5 79.6 |
    | JobBench | 53.4 | — | — |
    | Toolathlon-Verified | 72.5 | 73.3 | Opus 5 77.6 |
    | OSWorld-Verified | 86.1 | — | Fable 5 85.0; GPT-5.6 Sol 83.2 |
    | TerminalBench 3.0 | 11.3 | 29.0 | — |

    Qwen states it reports the higher score across two harnesses and that the model performs best with Claude Code.
  - "Self-improvement" (via DataCamp, attribution to the 0902 snapshot unclear): a research-reproduction demo where the model reproduced a paper's 6 main findings, then ran hypothesis → code → GPU run → analysis loops over 4 rounds and 18 ideas.
  - Third-party test (Hy4 appendix, Tencent's own testing): Qwen3.8-Max scores Toolathlon-Verified 72.5/69.1, SWE-bench Pro 67.7/61.6* and Terminal-Bench 2.1 86.6/85.8*.
- **Caveats:**
  - Secondary sources report that the open 2.4T checkpoint lacks image input and non-thinking mode, so OSWorld 86.1 (screenshot-based) likely applies only to the hosted model. This is unverified, since HF model cards were unreachable.
  - The 2.4T license is reportedly a custom Qwen3.8-Max license.
  - Several benchmarks are in-house (CoWorkBench).
- **Implications:**
  - The Qwen line now reports OSWorld-Verified ≈86 from both the general Max model and specialized Qwen-CUA. On that benchmark, general-model RL has caught up with the specialist. Differentiation must come from OSWorld 2.0, MyPCBench and safety.
  - CoWorkBench and "cowork" positioning (QwenWork) signals that the eval target is shifting from SWE to office/knowledge-work agents. Watch for a public release of CoWorkBench.

#### 2.7 Qwen3.8-Flash-Next (Qwen4 architecture preview)
- **Date:** 2026-08-26 (H). Tech report dated 2026-08-26.
- **URLs:** https://github.com/QwenLM/Qwen3.8-Flash-Next (README + `tech_report.pdf`) · https://qwen.ai/blog?id=qwen3.8-flash-next
- **Source:** github-fulltext for the architecture. Agent benchmarks are third-party-corroborated (blog not reachable).
- **Substance:**
  - 125B main model + 51B n-gram embedding tables held off-accelerator and prefetched from host memory; 6B active per token. "Early preview of the architecture used in Qwen4", playing the role Qwen3-Next played for Qwen3.5.
  - **GDN + QSA hybrid:** one full-attention layer in every four. At continued-pretraining time, those full-attention layers are replaced by Qwen Sparse Attention, which scores micro-blocks with a compressed lightweight indexer. At 1M context, kernel-level speedups are 7.6× (prefill) and 4.9× (decode) vs dense.
  - **Gated Residual:** a 4-branch residual stream with elementwise gate reads/writes. **Muon** optimizer, with a refitted scaling law. FlashQLA kernels give 2–3× forward and about 2× backward speedups over FLA Triton.
  - Base model leads the 397B-A17B Qwen3.7-Plus on 8 of 14 pretraining benchmarks and trails by ≤2.6 points on the rest, at 1/3 the active parameters, 1/3 the tokens and about 1/9 the FLOPs. Example: SWEBench-Pretrain 50.99 vs 49.24.
  - The report itself has no agent or RL content.
  - Vendor agent numbers (via secondary sources): DeepSWE 1.1 58.7, SWE-bench Pro 62.5, CoWorkBench 73.9, Toolathlon-Verified 73.5, AndroidWorld 84.5. A third-party table gives OSWorld 2.0 19.4.
  - Powers QwenWork "Standard" mode.
- **Caveats:** the agent numbers come only from secondary relays of the blog.
- **Implications:**
  - AndroidWorld 84.5 and OSWorld 2.0 ≈19 on a 6B-active model, if confirmed, suggest that cheap open bases for mobile/desktop GUI RL are now viable.
  - Host-offloaded n-gram tables and 1M-context sparse attention matter for the RL rollout cost of long multimodal agent traces.

#### 2.8 Qwen3.8-Omni-Flash ("Towards Native Omni-Modal Agents")
- **Date:** 2026-09-18 (M). Tech report arXiv 2609.25611.
- **Source:** official-search-extended (paper excerpts via search). No open weights.
- **Substance:**
  - Built on the Flash-Next sparse backbone; 1M context; on QwenCloud, Model Studio and Qwen Studio.
  - Multimodal agent table (paper Table 6): WildClawBench-MM 71.0 and AgenticVBench 36.8 (both with Claude Code), UniClawBench 69.6 (OpenClaw), OmniGAIA 74.0 (no harness). Gemini 3.8 Flash leads AgenticVBench and OmniGAIA.
  - Average of 29 evals is >25% over Qwen3.5-Omni-Plus.
  - No OSWorld score was found.
- **Implications:** this is an early signal of audio/video-in-the-loop agent benchmarks (AgenticVBench) run inside general coding harnesses. Relevant if GUI agents start consuming screen recordings rather than stills (compare Kimi Code's video input).

#### 2.9 Qwen Code: CUA SDK and a harness-invariance eval
- **Dates:** CUA SDK/driver and release pipeline 2026-08-23; "replace built-in tools with bundled skill" 2026-08-24; CUA hardening 08-28 to 09-02 (Windows UIAccess, Node REPL); eval doc 2026-10-14 (H).
- **Repo:** https://github.com/QwenLM/qwen-code
- **Source:** github-fulltext.
- **Substance:**
  - The README feature table lists "Computer Use (desktop automation)" alongside SubAgents, Agent Teams, Dynamic Workflows, Auto-Memory/Skills, Sandbox, Daemon `qwen serve` (HTTP+SSE, ACP) and "Agent Arena (multi-model head-to-head on same task)".
  - Computer use is shipped as a skill backed by a separately versioned `cua-driver` SDK, not as built-in tools.
  - **Harness-version invariance study:** seven Qwen Code versions (0.0.14 → 0.22.0), all on Qwen 3.7 Max.
    - Setup: SWE-bench Verified 500 tasks, 3 trials each; temp 1, top_p 0.95; reasoning_effort high, adaptive interleaved thinking; 1M context; max 500 iterations; 7,200 s timeout.
    - Average score ranges 76.40–77.80% (1.4 pp spread); pass^3 is 65.8–69.2%.
- **Implications:**
  - A useful null result: across a year of harness feature growth, SWE-bench Verified did not move. Harness gains may only show on longer-horizon or different-distribution tasks, which supports evaluating harnesses on long-horizon suites (Terminal-Bench 3/4, OSWorld 2.0) rather than SWE-V.
  - The CUA-as-skill pattern matches ZCode, DeepSeek Harness and Claude Code. It is converging on a common harness abstraction for GUI control.

### DeepSeek

#### 2.10 V4-Pro-0813 GA and DeepSeek Harness v0.1 (boundary: 2026-08-13)
- **Date:** 2026-08-13 (M: api-docs.deepseek.com/news/news260813 via search; the harness repo has internal history from 2026-06-10).
- **URLs:** https://api-docs.deepseek.com/news/news260813/ · https://github.com/deepseek-ai/deepseek-harness · docs https://deepseek-harness.github.io/deepseek-harness/
- **Source:** github-fulltext for the harness. Model facts are official-search-extended.
- **Substance:**
  - V4-Pro leaves preview with the 0813 build. Reasoning effort is low/high/max. Native OpenAI Responses API support was added, "optimized for Codex". Terminal-Bench 2.1 is 87.9 on DeepSeek's harness vs 72.1 for the April preview (vendor).
  - Harness (`dsh`, MIT):
    - "Everything-is-a-plugin", built on the Cordis meta-framework (paper: arXiv 2608.25512, "A Programming Paradigm for Spatiotemporal Composability"). Developer preview with "COMPATIBILITY-BREAKING CHANGES".
    - Run with `npx @deepseek-ai/dsh web`. There is also a Python SDK and a `jsonrpc-agent` variant for benchmarks.
    - Package families include `guard` (repeat-tool-call reminder, per-tool timeout policy), `compaction` (auto-condense, tool-output pruner, image offload), `sandbox` (Linux bwrap→Landlock, macOS Seatbelt, Windows restricted token; read-only / workspace-write / danger-full-access with one-time escalation), plus subagent, workflow, goal, plan, schedule, mcp, lsp, ssh and ptc-runtime.
  - **Computer-use and browser-use provider groups were added 2026-09-12 and 09-13 (in window).** Experimental providers are Cua Driver MCP/native (desktop) and Playwright MCP, Chrome DevTools MCP and Stagehand (browser).
  - Release 0.2.1-alpha.2 is from 2026-10-09; the repo has about 21k commits.
  - SAFETY.md: "has not undergone a security audit… Sandboxing, approval prompts, and permission controls can reduce risk, but they do not guarantee isolation."
- **Implications:**
  - DeepSeek's first open agent runtime reuses third-party CUA drivers (Cua) rather than shipping a GUI model. Its in-repo `benchmarks/` cover runtime properties (long-session browser, conversation fold, agent continuation), not task success.
  - Loop-hygiene guards (repeat-call reminders, timeouts) at the harness level are cheap mitigations for the stuck-loop failure mode seen in agent RL. Hy4's appendix notes DeepSeek-V4-Pro-0803 "frequently gets stuck in a repetitive loop" on ProgramBench.

#### 2.11 DeepSeek-V4.1-Flash: causal encoder-decoder for KV-cache compression
- **Date:** 2026-09-10 (H: FlashMLA README "2026.09.10 Release of DeepSeek v4.1's Attention Kernels"; DeepGEMM "Public Release 26/09" the same day; M: DeepSeek changelog). NVIDIA lists HF 09/10.
- **URLs:** https://api-docs.deepseek.com/updates/ · arXiv 2609.19969 ("DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression") · https://github.com/deepseek-ai/FlashMLA
- **Source:** github-fulltext for the kernel and KV-format facts. Architecture and benchmarks are third-party-corroborated (Baseten, NVIDIA model card, MindStudio, HelixML; not read directly).
- **Substance:**
  - Architecture (third-party, consistent across Baseten and others):
    - 552B multimodal MoE with a **causal encoder-decoder** split: 40 layers = 20-layer causal encoder + 20-layer decoder.
    - The decoder's KV cache is projected from the encoder output, so **prefill runs only the encoder (about 8B active)** while decode runs the full model (about 16B active).
    - Also cited: CSA2 attention, FP4 KV caching, a 196B "Engram" memory, 1M context, MIT license.
  - KV size: secondary sources say about 890 B/token global KV, about 1/4 of V4-Flash (some say 1/8).
  - Primary kernel docs (FlashMLA README) give the cache layouts:
    - V4.1 main cache: **528 bytes/token** (512 B FP8 e4m3 for all 512 dims including RoPE, plus 16 B e8m0 scales per 32 values).
    - V4.1-FP4 "extra" cache: **288 bytes/token** (256 B e2m1 + 32 B e4m3 scales per 16 values), valid only alongside the V4.1 main cache.
    - Token-level sparse attention (DSA lineage) via `indices` of top-k tokens.
  - Kernels: fused Q-RoPE + attention + O-RoPE + cast-to-FP8 (the Q-norm is "only used in V4, not V4.1"). Reported up to 1,460 TFLOPS prefill and 950 TFLOPS decode on B200.
  - The 2026-09-30 release drops Hopper and V3/V3.2/V4.0 support and adds Ascend 950 kernels (410 TFLOPS prefill at 95% of peak; 360 TFLOPS decode).
  - API: callers switch to `deepseek-flash`; old V4-Flash names are routed to V4.1-Flash. Native vision.
  - Vendor agent numbers (via NVIDIA card / search):
    - Terminal-Bench 2.1 90.6 (V4-Pro-0813 87.9; V4-Flash-0731 82.7). Terminal-Bench 3.0 30.0; 4.0 31.2.
    - DeepSWE v1.1 74.2 (V4-Pro 62.7).
    - The NVIDIA card shows harness sensitivity: Terminal-Bench 2.1 ranges 84.1–90.6 and DeepSWE 65.6–74.2 across harnesses.
- **Caveats:**
  - Neither the 890 B/token figure nor the encoder-decoder layer split appears in any primary file I could read. The FlashMLA formats (528/288 B) are primary, and how they combine into "890" is not documented.
  - No DeepSeek model repo was found for V4.1.
- **Implications:**
  - Cheap prefill (encoder-only) directly targets the agent workload shape: huge, mostly re-read contexts with short decodes per tool call. For CUA/agent RL this lowers rollout cost of long histories and favours cache-reuse-friendly context policies like Qwen-CUA's block folding.
  - The 6.5-point Terminal-Bench 2.1 spread across harnesses (84.1–90.6) reinforces that agent evals must fix the harness when comparing models.

#### 2.12 DeepSeek-V4-Flash-Vision-Exp
- **Date:** 2026-08-21 (L).
- **Source:** third-party-corroborated only.
- **Substance:**
  - Multimodal V4-Flash variant on the API (`deepseek-v4-flash-vision-exp`), 1M context.
  - Parameter counts conflict (284B-A13B vs 305B), as does open-weight status (MIT on HF vs API-only).
  - DeepSeek reportedly claims it is close to Opus 4.8 on "agent-oriented multimodal tests". GLM-5.3-Flash's chart uses it as a baseline ("DeepSeek-V4-Vision-Exp": Terminal Bench 2.1 83.9, DeepSWE 59.3).
- **Implication:** DeepSeek is moving to native vision ahead of V4.1, a prerequisite for screenshot-based CUA. No GUI benchmark was found.

### Moonshot (Kimi)

#### 2.13 Kimi K3: open 2.8T agentic model and tech report (pre-window context, 2026-07-27)
- **Date:** repo initial commit 2026-07-27; report updated 07-28 and 08-06 (H).
- **URLs:** https://github.com/MoonshotAI/Kimi-K3 (README + `k3_tech_report.pdf`) · https://www.kimi.com/blog/kimi-k3
- **Source:** github-fulltext (README + full report).
- **Substance:**
  - **Architecture:**
    - 2.8T total / 104B active; 93 layers (69 KDA + 24 Gated MLA); Attention Residuals.
    - Stable LatentMoE with 16 of 896 experts plus 2 shared; MoonViT-V2 vision (401M); 1M context.
    - MXFP4 weights / MXFP8 activations with QAT from SFT onward. Claims about 2.5× scaling efficiency over K2.
  - **Post-training:** SFT → RL experts → Multi-Teacher On-Policy Distillation (MOPD).
    - RL trains one expert per domain (general; general agents; coding agents) × effort level {low, high, max}, giving 9 teachers. These are distilled with a per-token clipped log-ratio OPD reward; top-k distillation showed no advantage.
  - **RL details:**
    - **Partial rollout**: the generation phase pauses once a fraction λ of N×K trajectories finish, and unfinished ones resume next iteration. Per-token regularization tolerates the staleness.
    - **Reasoning-effort RL**: reward is overridden to −1 if total tokens exceed τ·b0(x). For agents, the count includes tool-call arguments. τ is annealed from max to high to low.
    - **Agentic GRM** for non-verifiable tasks: the judge must read the outcome, write a rubric, score candidates and record them in a "scorepad". Tournament binary comparisons are used, and a candidate auto-loses if its length exceeds σ·ℓ0, which counters verbosity hacking.
  - **Environments (§4.2):**
    - **Unified white-box RL environment**: the harness is a set of configurable modules (tools, system prompts, context management, skills, memories, subagents), instantiating Kimi Code, Claude Code, Codex, OpenClaw, Hermes "as well as entirely new ones". Configurations are randomized per task group so the model does not overfit to one harness.
    - **Knowledge-graph-guided task synthesis**: an agent-expanded DAG of concepts that drives web retrieval and task generation.
    - Visual-reasoning tasks with a Python sandbox (crop, zoom, transform).
    - **Kernel tasks**: reward is 0 above an error threshold, 0.5 for matching the expert implementation, and rises toward 1 near the roofline. A hacking detector targets CUDA-graph replay, input caching and precision reduction.
    - **Personal-assistant "living" environments**: mock Gmail, Notion, Slack and Canvas; multi-day event streams; up to thousands of tool calls and millions of tokens per rollout; per-event graders.
    - **Autonomous Execution Tasks**: verifier-in-the-loop with public diagnostic verifiers plus hidden held-out verifiers and limited submission budgets, for example black-box system replication and tax auditing.
    - **Web-dev**: run under diverse scaffolds. Reward is zeroed if the build fails or the artifact is faked; model judges inspect code or interact with the artifact.
  - **Infrastructure:**
    - Co-located RL within "a few hundred GPUs" per 1M-context experiment.
    - External CPU-DRAM KV pool with write-back of idle prefixes; KDA states are offloaded together with the MLA KV.
    - A rollout **auto-throttling** scheduler driven by KV utilization.
    - **AgentENV**: Firecracker microVM sandboxes with incremental checkpoint/resume (133 ms / 49 ms), pause while waiting on inference (up to 98% of sandbox lifetime), **fork** for side-effect-free reward judging, snapshots, and sub-second launch via OverlayBD. 51,219,741 sandboxes across 1,505,678 images were created during K3 development.
  - **Agentic results** (max effort; agentic top-p 1.0):
    - OSWorld-Verified 84.8 (Fable 5 85.0; GPT-5.6 Sol 83.0; Opus 4.8 83.4).
    - OSWorld 2.0 58.3 (Fable 5 66.1; Sol 62.6). The metric is not stated, but the numbers look like the partial-credit metric (Opus 4.8 55.7 here vs 54.8 partial in Qwen-CUA's table).
    - SaaS-Bench 60.1; BrowseComp 91.2 (compaction at 300K; 90.4 with the full 1M and no management); Toolathlon-Verified 76.5; MCPMark-Verified 94.5; MCP-Atlas 84.2 (500 tasks, 100 turns, Gemini 3.1 Pro judge); AutomationBench 30.8; Agents' Last Exam 28.3; Terminal-Bench 2.1 88.3 (Kimi Code harness).
  - **Cyber eval (§6.2.2):**
    - Tier 1: about 70% of reviewed findings confirmed; 16 new vulnerabilities across 6 projects, including a Linux remote heap OOB write and a Dirty-COW-class RDMA local privilege escalation.
    - Tier 2 (36 tasks): 14/36 solved vs GLM-5.2 8/36.
    - UK AISI + NIST CAISI: ExploitBench 32% vs 24%; 0/41 arbitrary code execution on end-to-end exploits.
- **Implications:**
  - AgentENV's **fork** primitive (judge a copy of the final state without side effects) and pause-during-inference are directly applicable to CUA RL, where VMs dominate cost.
  - Harness randomization during RL is the strongest published argument that agent policies overfit to harness conventions. CUA training should likewise randomize action schemas, context policies and system prompts.

#### 2.14 Kimi K2.8 Preview
- **Date:** 2026-09-11 (M).
- **Source:** third-party-corroborated (llm-stats, KuCoin, Pandaily, magicshot).
- **Substance:**
  - A mid-tier coding/agent model between K2.7 Code and K3, rolled out across Kimi Code and Work under the existing `kimi-for-coding` ID.
  - 1M context (up from 262,144 on K2.7 Code); thinking effort low/high/max.
  - Moonshot claims coding/agent performance "close to K3". No public benchmarks, pricing or weights at launch, and sources conflict on modalities.
  - Related harness change (H): `MoonshotAI/kimi-cli` added a deprecation-aware update with one-key migration to Kimi Code (2026-09-01) and short-circuited entry points to the Kimi Code installer (2026-09-22). `MoonshotAI/Kimi-Code` (MIT; video input; subagents `coder`/`explore`/`plan`; marketplace plugins; a "Kimi Browser Extension", renamed 2026-09-15) is the active harness.
- **Implication:** model iterations are now shipped behind a stable harness model ID. External researchers cannot pin versions, which complicates longitudinal agent evals.

### MiniMax

#### 2.15 MiniMax-M3 (pre-window context) and M3.1-Flash-Preview
- **Dates:** M3 2026-06-01 (H; README last edited 07-11). M3.1-Flash-Preview 2026-09-27 (M/L).
- **URLs:** https://github.com/MiniMax-AI/MiniMax-M3 · tech report arXiv 2606.13392 · https://github.com/MiniMax-AI/MSA
- **Source:** github-fulltext for M3. M3.1 is third-party-corroborated plus a quoted MiniMax X post.
- **Substance:**
  - M3: about 428B total / 23B active; native multimodal from the first step (text, image, video); 1M context.
  - **MiniMax Sparse Attention (MSA)**: 9× prefill and 15× decode speedups vs M2 at 1M, with per-token compute cut to 1/20.
  - Thinking modes are enabled, adaptive and disabled. Positioned for "coding & cowork" long-horizon agentic benchmarks; the benchmark figure is image-only.
  - M3.1-Flash-Preview: shipped only inside MiniMax Code on the subscription "M Plan" (formerly Token Plan). 1M context; five effort levels (low/medium/high/xhigh/max). No model card, benchmarks or weights. M3.1 had been shown at WAIC on 2026-07-17.
- **Implication:** there is no new primary technical content from MiniMax in the window. M3's MSA plus native video makes it a plausible long-video/GUI base, but no CUA evals have been published.

#### 2.16 MiniMax Code: open-source CLI source snapshot
- **Date:** source imported 2026-09-18 (H; the repo was an issue tracker from 06-01). Active through 10-13.
- **Repo:** https://github.com/MiniMax-AI/MiniMax-Code
- **Source:** github-fulltext.
- **Substance:**
  - `mcode` terminal agent with BYOK support for openai-completions, openai-responses and anthropic-messages formats.
  - Packages: agent-core, agent-runtime, agent-tools, **browser-core**, local-runtime(-v2), protocol, tui.
  - First-party code is MIT. `third_party/sandbox-runtime` (Apache-2.0) is retained, and Pi-derived terminal code keeps its original declarations.
  - LICENSE-STATUS notes that on 2026-09-12 review found the original root license "had been copied from Sandbox Runtime and contained Anthropic's attribution" and corrected it.
  - Recent fixes: forced compaction recovery for oversized requests; per-turn reminder trimming (budget thresholds, time, session ID).
- **Implication:** another open harness, built on reused components (Pi, sandbox-runtime). It is useful as a cross-harness eval target, but not a research artifact.

### Xiaomi MiMo

#### 2.17 MiMo-V2.6 (Pro / Flash / Distill-Qwen-9B) with open RL environments, RL code and compute disclosure
- **Date:** RL code commit 2026-09-21 (H). Release notes 2026-09-22 (M). Technical report "MiMo-V2.6: Scaling Reinforcement Learning Towards Self-Improvement" is arXiv 2610.11959; the PDF is also on HF `XiaomiMiMo/MiMo-V2.6-Pro-RL`.
- **URLs:**
  - https://github.com/XiaomiMiMo/verl (RL code)
  - https://github.com/XiaomiMiMo/mimoagent (rollout framework)
  - https://github.com/XiaomiMiMo/uni-agent (gateway + TransferQueue capture)
  - data: https://huggingface.co/datasets/XiaomiMiMo/MiMo-V2.6-RL-oss
  - images: https://hub.docker.com/r/xiaomimimo/mimo-v2.6-rl-oss
  - news: https://mimo.mi.com/docs/en-US/news
- **Source:** github-fulltext for the RL stack (README, configs, algorithm code docstrings, grader prompts, commit messages). Model and benchmark facts are official-search-extended / third-party-corroborated.
- **Substance:**
  - **Models (via search):** Pro is about 1.02T / 42B active; Flash 309B / 15B active; both about 1M context, MIT. A 9B distilled Qwen-based model is released as the reproduction training model.
  - **Five open RL environments** (README table):

    | Domain | Task family | Verifier |
    |---|---|---|
    | Code | Software engineering | executable tests |
    | Cyber | Vulnerability reproduction (ARVO) | rule checks |
    | General | Knowledge work | rubric-based judging |
    | Visual | Web development | visual grading |
    | Music | Symbolic composition | rule checks |

    Secondary sources count about 7k tasks (one audit: 7,780 tasks / 4,688 distinct environments).
  - **Harness plurality:** configs include `mini-bash`, `mini-claude-code`, `mini-codex`, `mini-mimocode` and a `mix-four-whitebox` mix. Commit text: "Multi-harness agentic rollout and recipes: mimoagent SWE, mini-swe-agent, the Claude Code and Codex Responses harnesses, and the uni-agent blackbox path". `algorithm.group_advantage_by_harness` exists (false in the code recipe). mimoagent supports "10+ black-box coding CLIs (Claude Code, Codex, OpenCode, …)" and K8s, Docker, CubeSandbox and Modal backends.
  - **Code-RL recipe** (`recipes/code/config/train.yaml`):
    - GRPO advantage without std normalization; n=16; train batch 32 prompts.
    - Prompt 8,192 + response up to **253,952 tokens** (262,144 max).
    - temp 1.0, top_p 0.95, top_k 20.
    - clip 0.2/0.2 (dual-clip c=3); `loss_agg_mode: prompt-mean`; lr 1e-6 constant; no KL.
    - SGLang FP8 KV.
    - Trajectory timeout 7,200 s; agent idle timeout 720 s; `trajectory_selection: longest`.

    A third-party analysis notes the open recipe is a simplified PPO-clip port, not the exact internal stack.
  - **Credit assignment and reward-shaping channels** (`verl/trainer/config/algorithm.py`):
    - `tool_call_error_penalty` acts on tokens of *model-attributable* tool-call errors. Strategies are `monitor | mask | adv_reduction | adv_set | adv_signed`.
    - `adv_signed` is a "sign-aware, per-sign mass-conserving penalty": marked tokens of negative samples are multiplied by κ≥1, marked tokens of positive samples go to 0, and both sides are rebalanced over the batch (`signed_min_scale` 0.5 / `signed_max_scale` 2.0).
    - `repetition_penalty` ports a "dirty_repetition" rule (an n-gram of 300 tokens repeated ≥15 times within an 8,300-token window), with an experimental `early_stop` mode that masks tokens before the first hit and applies `adv_signed` on the hit spans.
    - `deep_failure_mask` (explicitly "a biased estimator… used only to test where deep-turn entropy growth comes from") drops failing trajectories' tokens from turn k = ceil(α·median successful turns).
    - Infra failures are split from wrong answers, and group metrics are filter-independent.
  - **Visual (web-dev) grader:** a VLM "group pick" prompt that sees all rollout screenshots for one query in random order.
    - It names only those that are *clearly* better or worse (0..n each), or "no clear difference". It is told not to force a ranking or judge functionality.
    - It lists objective defects: blank renders, truncation, overlapping, placeholder images, crude SVG doodles, unreadable contrast.
    - Plus a separate query-fit judge and an `eval_rubric`. This matches the report's "groupwise grading" of the 16 attempts.
  - **Compute disclosure** (via search): each RL step samples 1,568 prompts × G=16 ≈ 25,088 trajectories (2.7–3.7B tokens). "30 RL steps across ≈750,000 trajectories in under six days" per model is consistent (30 × 25,088 ≈ 752k). A self-hosted MiMo-V2.6-SFT model serves as grader during RL. A $3.47M flagship RL cost is cited by third parties without an official source.
  - **Vendor benchmarks** (via search):
    - Pro: DeepSWE v1.1 71.9, Terminal-Bench 2.1 89.9, OSWorld-Verified 82.0, Toolathlon-Verified about 76.9, SEC-Bench Pro 66.3, Terminal-Bench 4.0 34.9.
    - Flash: DeepSWE 67.9, Terminal-Bench 2.1 87.6, CyberGym 95.1 (Pro 94.0), ExploitBench 25.3 (Pro 47.9).
- **Caveats:**
  - **Vals AI** (third-party): "In two-thirds of the coding tasks, the answer is still in the task's Git history, and MiMo finds it." This is an environment-leakage / reward-hacking flaw in the released tasks.
  - Self-grading with an SFT model is a recognized hacking surface.
  - Benchmarks need independent replication.
- **Implications:**
  - This is the richest *open* agentic-RL reward-engineering codebase of the window. The token-level tool-call-error and repetition channels and the signed rebalance are directly portable to CUA RL, where malformed actions and loops dominate failure modes.
  - The git-history leak is a cautionary pattern for anyone building environments from real repos (or replayable GUI states). Scrub privileged state the agent can read, and audit with exploit-seeking agents before training.

### StepFun

#### 2.18 Step 5 Preview
- **Date:** 2026-09-18/20 (L; AA lists 09-18, StepFun materials 09-20). Open weights promised for 2026-10-15 and not yet out as of 10-14.
- **Source:** third-party-corroborated (no official repo found; `stepfun-ai/Step-5*` probes returned 404). The last open StepFun repos are Step-3.5-Flash (2026-04) and GELab-Zero (GUI agent, 2026-05).
- **Substance:**
  - Sparse MoE, 600B total / 27B active; 1M context; 64K max output; text, image and video input.
  - StepFun-reported: GPQA-D 93.5, HLE w/ tools 59.4, Terminal-Bench 2.1 85.0, DeepSWE v1.1 67.7, Toolathlon-Verified 74.1, ProgramBench 80.5, StepCodeBench 49.0, Terminal-Bench v4 33.3.
  - Independent: Vals AI Terminal-Bench v4 31.8; Vals Index 49.35 (30/45); Finance Agent v2 50.67; Vibe Code Bench 70.40.
  - No OSWorld or GUI numbers found, despite StepFun's earlier GUI-agent work (GELab-Zero).
- **Implication:** check on 10-15 whether the weights and a tech report ship with GUI-agent evals. There is no primary substance yet.

### ByteDance Seed

#### 2.19 HarnessDev: can LLMs create and evolve their own agent harness?
- **Date:** arXiv 2609.01437, submitted 2026-09-01 (M).
- **Source:** official-search-extended (arXiv abstract and figures via search) plus third-party notes. No code repo found.
- **Substance:**
  - The evaluation unit moves from task outputs to the **runnable harness** the model writes.
  - **Creation** phase: start from a minimal seed harness that scores 0, plus a few cases, and build a full execution system. **Evolution** phase: hand back the harness and improve it on downstream execution feedback (for example SWE-bench Pro and Terminal-Bench 2.1).
  - Scope: 6 creator LLMs, 4 domains, 5 downstream benchmarks, 2,207 unique downstream instances (one source says 2,027).
  - Findings:
    - Generated harnesses lag human-engineered ones in code, search and research. One write-up reports BrowseComp 52.6 (best model-built) vs 92.2 (reference), and Terminal-Bench 2.1 68.8 vs 88.8.
    - Evolution gains are unstable and runtime-model-dependent: only 34 of 64 changes generalize. All 9 evolution runs improved on their feedback set, but 4 went negative on held-out tasks; the agent's own feedback agreed with held-out performance only 53.1% of the time.
  - Related same-period work cited alongside: HarnessCompass (arXiv 2608.01918), Harness-Zero (2609.24974), AutoSaddler (2608.23041), JIT-Agent (2608.25593).
- **Implications:**
  - Self-improving harness loops overfit their feedback set much as RL overfits its reward. Held-out gating is mandatory, which mirrors Qwen-CUA's held-out checkpoint selection and Kimi's hidden verifiers.
  - Harness quality is a large, separately measurable factor (BrowseComp 52.6 vs 92.2 with a fixed model). GUI-agent comparisons need harness-controlled baselines.

#### 2.20 UI-TARS / UI-TARS-desktop
- **Date:** 2026-09-24 and 10-08 commits (H). No new UI-TARS model; `bytedance/UI-TARS` was last updated 2025-09-05.
- **Repo:** https://github.com/bytedance/UI-TARS-desktop
- **Source:** github-fulltext (commit log).
- **Substance:** 8 in-window commits, all agent-server security hardening:
  - validate the Host header against DNS rebinding;
  - require a token once the server leaves loopback;
  - block request-body injection into agent constructor options;
  - stop HTML previews escaping the iframe sandbox;
  - answer disallowed origins with 403;
  - document remote-access settings.
- **Implication:** these are useful as a checklist of attack surfaces for locally hosted CUA agent servers (rebinding, unauthenticated remote control, option injection). There is no new GUI-model research from Seed in the window.

### Tencent Hunyuan

#### 2.21 Hy4 preview (770B-A49B, Apache-2.0)
- **Date:** 2026-08-28 (H: repo init and README).
- **URLs:** https://github.com/Tencent-Hunyuan/Hy4-Preview · https://huggingface.co/tencent/Hy4-preview
- **Source:** github-fulltext (README; benchmark appendix image read visually).
- **Substance:**
  - **Architecture:**
    - 78 layers (1 dense + 77 MoE); 256 routed experts + 1 shared, top-8; hidden 6,144; 1 MTP layer (10B, 0.7B active).
    - **Gated DSA** with **IndexCache** cross-layer index reuse (indexer 32 heads × 128, top-k 2,048).
    - **iHC (identity Hyper-Connections)** with 4 residual streams. Context 1M; vocabulary 120,832.
  - **Training emphasis:** data built with in-house experts (SWE, game dev, finance, security). Co-designed with CodeBuddy and WorkBuddy.
  - **Blind evaluation:** 163 experts × 203 engineering tasks. Hy4 averages 2.99 vs GLM-5.3 2.92 and Kimi K3 2.94 (win/tie/loss 46.8/12.8/40.4 and 51.2/7.9/40.9).
  - **Appendix (vendor; \* = Tencent's own runs of competitors).** Hy4 / Hy3 shown first:

    | Benchmark | Hy4 | Hy3 | Competitors |
    |---|---|---|---|
    | SWE-bench Pro | 65.7 | 57.9 | — |
    | DeepSWE | 64.3 | 28.0 | — |
    | SWE-Marathon | 31.9 | 5.0 | — |
    | Terminal-Bench 2.1 | 85.4 | 70.8 | — |
    | CyberGym | 78.4 | — | GLM-5.3 84.5/83.0* |
    | PostTrainBench v1.1 | 35.6 | — | — |
    | WideSearch | 83.9 | — | — |
    | Toolathlon-Verified | 74.1 | — | GLM-5.3 73.0/73.8*; Kimi K3 76.5/74.7*; Qwen3.8-Max 72.5/69.1* |
    | MCP-Atlas | 83.7 | — | — |
    | APEX-Agents | 37.1 | — | — |
    | JobBench | 61.7 | — | — |
    | Agents' Last Exam (CLI) | 22.8 | — | — |
    | AutomationBench | 32.1 | — | GLM-5.3 48.2/49.4* |
    | GDPval-AA v2 | 1678 | — | GLM-5.3 1763; Opus 5 1831 |

    No OSWorld or GUI benchmarks are reported.
  - **Harness and anti-hacking setup notes** (valuable):
    - Terminal-Bench 2.1 runs in Claude Code with up to 500 turns, 12 h per trial, 16 CPU / 32 GB.
    - SWE-Atlas has a network allowlist "to prevent hacking behaviors". NL2Repo uses a 1,000-turn budget "with anti-hacking prompt constraints and tool-call monitoring". ProgramBench uses a 2,000-turn budget, and DeepSeek-V4-Pro-0803 was swapped to mini-swe-agent because it "frequently gets stuck in a repetitive loop".
    - Toolathlon uses an internal reimplementation of some MCP tools, a 2 h timeout and a 100-step budget.
    - "Certain Hy3 benchmark scores may differ … following updates to the evaluation harness, judge model, and anti-hacking mechanisms."
  - **Known limitations** (README): "spending longer than necessary reasoning", "a tendency to over-verify its own work".
- **Implications:**
  - The appendix is a rare cross-lab table where one lab re-runs all Chinese competitors under fixed harnesses. It is useful for calibrating vendor-reported numbers, which often differ by 1–6 points from the competitor's own claims (for example GLM-5.3 Toolathlon 73.0 claimed vs 73.8*).
  - Anti-hacking controls (network allowlists, tool-call monitoring) are now routine in agent evals. GUI-agent evals need equivalents, such as blocking web lookups of answer states.

---

## 3. Gaps and items to verify when sites are reachable

- **Qwen:**
  - Qwen3.8-Max blog: the exact date and the full agent table (Toolathlon, CoWorkBench, OSWorld, any GUI/Android numbers).
  - Whether the open 2.4T checkpoint lacks vision.
  - Qwen3.8-Flash-Next blog agent table (AndroidWorld 84.5, OSWorld 2.0 19.4 are unconfirmed).
- **DeepSeek:**
  - V4.1-Flash arXiv 2609.19969: the encoder/decoder split, the 890 B/token claim, and agent-harness results.
  - V4-Flash-Vision-Exp: weights status.
- **Xiaomi:** MiMo-V2.6 arXiv 2610.11959 §7 (RL recipe), the self-grader design and the compute log. Also check whether Xiaomi responds to the Vals AI git-history leak.
- **StepFun:** whether Step 5 weights and report ship on 2026-10-15.
- **Z.ai:**
  - GLM-5.3 blog: cyber environment design, disclosure-ledger details, trusted-access program.
  - GLM-5.3-Flash/FlashX docs.
- **ByteDance Seed:** whether HarnessDev code is released (project page self-developing-agents.github.io).
- **Moonshot:** a K2.8 official blog or benchmarks, and whether weights are planned.
