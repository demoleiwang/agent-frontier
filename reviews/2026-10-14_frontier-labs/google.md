# Google DeepMind / Google AI: blog inventory and deep notes (2026-08-14 to 2026-10-14)

Scope: computer-use and browser-use agents, agentic RL, agent evals and safety (containment, monitoring, prompt injection), and agent infrastructure (SDKs, harnesses, memory). 「无出处，待核」
Compiled: 2026-10-14.

## How this was gathered (read first)

- **Developers Blog (AI label):** The complete list for the window comes from the git history of the Olshansk/rss-feeds mirror (`feeds/feed_google_ai.xml`, all 1,379 historical versions merged). That gives the exact title, URL, pubDate and official summary for 25 items from 2026-08-11 to 2026-10-13. The dates are the feed's pubDate, so they are high confidence. The mirror only covers the Developers Blog "AI" feed. Developers Blog posts without that label may be missing.
- **DeepMind blog, blog.google and research.google:** These sites can't be fetched. Coverage comes from web search in two modes: standard for the inventory sweep and extended for substance on the key posts. **The shared web-search budget ran out partway through.** Searches never ran for computer-use model posts (other than 3.8 Flash), Project Mariner, SIMA 2026, Genie 2026 or Jules for September/October. Those are marked "not found / not searched" below.
- **GitHub full text:** Reached by cloning the public repos. Sources were google/adk-python, google/adk-samples (AQuA), google/tunix, googleapis/python-genai and google-gemini/computer-use-preview. Commit messages there give **primary, timestamped substance** behind several posts. The strongest case is the "200k-line codebase overnight" post, where the commit carries a full benchmark table and the line "Argon generated these changes."
- **Source labels used in the deep notes:** `github-fulltext` | `official-search-extended` (official-domain content summarized by extended search) | `official-search-standard` | `feed-summary-only` | `third-party-corroborated`.
- **Vendor-reported numbers** are marked **[VR]**. No numbers were invented. Where sources disagree, both values are given.

---

## Part 1. Inventory

Date confidence: **H** = feed pubDate, dated listing, or a corroborating git timestamp. **M** = a dated search snippet or listing, not verified on the page. **L** = inferred from relative "N days ago" metadata, roundup membership, or adjacency. 「无出处，待核」
Relevance tag: ★ = agent-relevant to this review's focus.

### 1A. Google DeepMind blog (deepmind.google/blog) and model pages

| Date | Title | URL | Category | Conf. |
|---|---|---|---|---|
| 2026-08-21 | Exploring new frontiers of AI and games research (From Atari to EVE Online, 15-year retrospective, partnerships with game developers) | https://deepmind.google/blog/from-atari-to-eve-online-building-on-15-years-of-ai-research-in-games/ | Research / games / agents | M |
| 2026-08-27 ★ | Piloting the world's first double-blind AI evaluations | https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/ | Evals / safety | M (dated listing, plus "47 days ago") |
| Aug 2026 (day unknown) | Gemini Omni 1.1 Flash (video generation: scene extension, first/last-frame interpolation, 4K upscaling) | DeepMind news index; also in the Aug roundup | Model (video) | L |
| Aug 2026 (day unknown; Batch issue of Sep 11 covers it) | Gemini 3.5 Transcribe (speech-to-text for voice agents and captioning) | DeepMind news index; Aug roundup | Model (ASR) | L |
| Aug 2026 (listed) / possibly earlier | Lyria 3.5 in Google Flow Music | DeepMind news index | Model (music) | L |
| 2026-09-02 ★ | Gemini 3.8 Flash and 3.8 Flash Cyber (DeepMind mirror of the blog.google post; plus model card and Cyber evals-methodology page) | https://deepmind.google/models/model-cards/gemini-3-8-flash/ ; https://deepmind.google/models/evals-methodology/gemini-3-8-flash-cyber | Model / agentic coding / cyber | H (python-genai commit adding the 3.8 Flash model is dated 2026-09-02) |
| 2026-09-08 | AlphaGenome Atlas: predicted effects of 9B human single-nucleotide variants | https://deepmind.google/blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/ | Science | M |
| 2026-09-15 (updated 09-17) | Introducing Gemini 3.8 Live and 3.8 Live Extended Thinking | https://deepmind.google/blog/introducing-gemini-3-8-live-and-3-8-live-extended-thinking/ | Model (voice / live agents) | M |
| Sep 2026 (day unknown) | Agentic video understanding with Gemini | DeepMind news index | Agentic perception | L |
| Sep 2026 (day unknown) | SynthID Bio | DeepMind news index | Safety / provenance | L |
| Sep 2026 (day unknown) | WeatherNext 3 (real-time satellite data, higher resolution) | DeepMind news index; Sep roundup | Science | L |
| Sep 2026 (~09-23 per SDK commit) | Gemini 3.8 text-to-speech (3.8 Flash TTS, 3.8 Flash Lite TTS) | DeepMind news index | Model (TTS) | M |
| 2026-09-23 ★ | Advancing Private AI Compute with secure, server-side memory | https://deepmind.google/blog/advancing-private-ai-compute-with-secure-server-side-memory/ | Agent memory / privacy infra | M (dated listing, plus "~20 days ago") |
| 2026-09-30 ★ | Gemini 4 Argon: our next era of frontier intelligence | https://deepmind.google/blog/gemini-4-argon-our-next-era-of-frontier-intelligence/ (mirror: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) | Frontier model launch | H (DeepMind listing plus third-party coverage) |
| Sep 30 to Oct 13 ★ | Gemini 4 Argon model card | https://deepmind.google/models/model-cards/gemini-4-argon/ | Model card / FSF | M |
| Sep 30 to Oct 13 ★ | Gemini 4 Argon without cyber guardrails (trusted-defender variant page) | https://deepmind.google/models/gemini/cyber/ | Cyber / access control | L |
| Oct 2026 (listed in the Oct DeepMind index; probably 10-13) ★ | Developing Gemini 4 Argon responsibly and safely (blog.google URL) | https://blog.google/innovation-and-ai/technology/safety-security/gemini-4-model-safety-security/ | Safety | L–M |
| 2026-10-13 ★ | Gemini 4 Argon for Robotics (DeepMind plus Developers Blog) | https://developers.googleblog.com/gemini-4-argon-for-robotics/ | Robotics / embodied agents | H (feed) |
| Oct 2026 (~10-06) | EmbeddingGemma 2: an open, lightweight multimodal embedding model | DeepMind news index (dev posts dated 10-06) | Model (embeddings, on-device retrieval) | M |
| Oct 2026 (ADK default-avatar commit is 10-01) | Introducing Gemini 3.8 Live with Live Avatar | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-with-live-avatar/ | Model (live agents) | L |
| 2026-10-14 | Google DeepMind & Singapore MDDI: on-device AI against scams | https://deepmind.google/blog/on-device-ai-scam-detection-mddi/ | Safety / on-device | M |

Outside the window but needed as context (not counted):

| Date | Title | URL |
|---|---|---|
| 2026-04-17 | Strengthening our Frontier Safety Framework (FSF v3.1: Tracked Capability Levels, harmful-manipulation CCL, ML R&D/misalignment protocols) | https://deepmind.google/blog/strengthening-our-frontier-safety-framework/ |
| 2026-06-11 | Investing in multi-agent AI safety research ($10M call with Schmidt Sciences, Cooperative AI Foundation, ARIA and Google.org; deadline Aug 8; awards "autumn 2026") | https://deepmind.google/blog/investing-in-multi-agent-ai-safety-research/ |
| 2026-06-18 | Securing internal systems against increasingly capable and imperfectly aligned AI (AI Control Roadmap, plus the "Three Layers of Agent Security" policy paper) | https://deepmind.google/blog/securing-the-future-of-ai-agents/ |
| ~2026-07-30 | Introducing Gemini Robotics ER 2 | https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-2/ |
| 2026-08-06 | WeatherNext 2 / WeatherNext Cyclones open-sourced | https://deepmind.google/blog/weathernext-ai-model-achieves-breakthrough-in-forecasting-cyclones/ |
| 2026-08-12 | Putting sign language AI into users' hands | https://deepmind.google/blog/putting-sign-language-ai-into-users-hands/ |
| 2026-08-13 | Gemini 3.7 Flash: our most intelligent workhorse model (**one day before the window**) | https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/ |

### 1B. blog.google (The Keyword): AI, Gemini, Chrome and Antigravity posts

| Date | Title | URL | Category | Conf. |
|---|---|---|---|---|
| Aug 2026 (day unknown; in Aug roundup) ★ | Gemini in Chrome with auto browse comes to Android / Tap into the power of Gemini in Chrome on Android | https://blog.google/products-and-platforms/products/chrome/bringing-chrome-ai-to-android/ ; https://blog.google/products-and-platforms/products/chrome/gemini-in-chrome-android-auto-browse/ | Browser agent | L |
| 2026-08-26 ★ | Turn your voice into action with new productivity features in Gemini Live (Gemini Live to Spark integration) | https://blog.google/innovation-and-ai/products/gemini-app/productivity-features-gemini-live/ | Personal agent | M |
| ~2026-08-27/28 ★ | Pairing Google Antigravity with Gemini 3.7 Flash solves notable multi-agent math and engineering problems (Antigravity Teamwork) | https://blog.google/innovation-and-ai/technology/developers-tools/antigravity-teamwork-multi-agent/ | Multi-agent harness | L ("~47 days ago") |
| Aug/Sep 2026 (date conflict) | Jules from Google Labs introduces proactive coding features (Suggested Tasks, Scheduled Tasks, Render deploy-fix integration) | https://blog.google/innovation-and-ai/technology/developers-tools/jules-proactive-updates/ | Coding agent | **L, possibly out of window** (metadata says ~307 days old; page references the Aug 2026 roundup) |
| 2026-09-02 ★ | Introducing Gemini 3.8 Flash and 3.8 Flash Cyber | https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/ | Model / agents / cyber | H |
| Sep 2026 (day unknown) | See what 4 builders are making with Gemini 3.8 Flash | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-flash-developers/ | Developer showcase | L |
| Sep 2026 (likely 09-02 or 09-30) ★ | Google's Fairwind Program: cyber defense tools for trusted partners | https://blog.google/innovation-and-ai/technology/safety-security/fairwind-program/ | Cyber / gated access | L |
| Early Sep 2026 | The latest AI news we announced in August 2026 (monthly roundup) | https://blog.google/innovation-and-ai/technology/google-ai-updates-august-2026/ | Roundup | M |
| ~2026-09-10 ★ | The Gemini app is now available for Windows (Spark workspace, Alt+Space) | https://blog.google/innovation-and-ai/products/gemini-app/gemini-app-now-on-windows/ | Desktop agent | M (one listing says 09-10; "~33 days ago" metadata) |
| 2026-09-15 | Introducing Gemini 3.8 Live and 3.8 Live Extended Thinking | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/ | Model (live) | M |
| 2026-09-15 | New insights from Google's AI & Economy ATLAS | https://blog.google/innovation-and-ai/technology/ai/ai-economy-atlas-september-2026/ | Policy / economics | M |
| Sep 2026 | A new wave of Connected Apps is rolling out to Gemini (Airtable, Linear, monday.com, PandaDoc, Adobe, Peloton) | https://blog.google/innovation-and-ai/products/gemini-app/new-connected-apps-gemini/ | Agent tools / integrations | L |
| Sep 2026 | Googlebook and on-device Gemini introduce a new way to work (pre-orders; Magic Pointer) | https://blog.google/products-and-platforms/devices/googlebook/googlebook-built-in-intelligence/ | Device / on-device agent | L |
| Sep 2026 | September Android Drop | https://blog.google/products-and-platforms/platforms/android/android-drop-september-2026/ | Product | L |
| Sep 2026 | Start the year AI-ready with the Google AI Educator Series | https://blog.google/products-and-platforms/products/education/new-ai-educator-trainings-september-2026/ | Education | L |
| 2026-09-30 ★ | Gemini 4 Argon: our next era of frontier intelligence | https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/ | Frontier model | H |
| Sep 30 or Oct 13 ★ | Gemini 4 Argon: Built to solve your hardest problems (localized fr/pl versions exist) | https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/ | Frontier model (product framing) | L |
| 2026-10-02 | The latest AI news we announced in September 2026 (monthly roundup) | https://blog.google/innovation-and-ai/technology/ai/google-ai-updates-september-2026/ | Roundup | H |
| 2026-10-13 ★ | Gemini 4 Argon is now available in the Gemini app | https://blog.google/innovation-and-ai/products/gemini-app/gemini-4-argon-availability/ | GA | M (python-genai added `gemini-4-argon` on 10-13) |
| 2026-10-13 ★ | Gemini 4 Argon is now available for developers | https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-4-argon/ | GA / developer | M |
| Oct 2026 ★ | Developing Gemini 4 Argon responsibly and safely | https://blog.google/innovation-and-ai/technology/safety-security/gemini-4-model-safety-security/ | Safety | L–M |

Out of window (context only): Chrome "Gemini 3 features including auto browse" (desktop launch, early 2026); "Gemini Spark: new Chrome browsing integration" (July 2026); "Gemini Spark updates: macOS launch" (June 2026); "Connected apps from Made by Google" (Aug 12); AlphaEvolve GA on Cloud (Jul 9).

### 1C. antigravity.google blog (official Antigravity product blog)

| Date | Title | URL | Conf. |
|---|---|---|---|
| 2026-08-13 (boundary) | Gemini 3.7 Flash in Google Antigravity | https://antigravity.google/blog/gemini-3-7-flash-in-google-antigravity/ | L |
| ~2026-08-27 ★ | Teamwork: when AI becomes a research partner | https://antigravity.google/blog/teamwork-when-ai-becomes-a-research-partner/ | L |
| ~2026-09-02 ★ | Gemini 3.8 Flash in Google Antigravity | https://antigravity.google/blog/gemini-3-8-flash-in-google-antigravity/ | L |
| unknown (possibly I/O era) ★ | Google Antigravity built an OS (and more): 93 subagents, more than 339M input tokens [VR] | https://antigravity.google/blog/google-antigravity-built-an-os/ | L, may be out of window |

### 1D. Google Research blog (research.google/blog)

| Date | Title | URL | Category | Conf. |
|---|---|---|---|---|
| 2026-08-25 ★(peripheral) | AgentHands: interactive hand gestures for agent conversations in XR | [research.google/blog](https://research.google/blog/) (listing) | Embodied agent UX | M |
| 2026-08-27 | Planetary prediction engine | [research.google/blog](https://research.google/blog/) (listing) | Science | M |
| 2026-08-31 | TimesFM-3 | [research.google/blog](https://research.google/blog/) (listing) | Forecasting model | M |
| 2026-09-01 | Mapping global methane emissions from space with deep learning (MAPL-EMIT with NASA JPL) | [research.google/blog](https://research.google/blog/) (listing) | Science | M |
| 2026-09-03 | Transfer learning for genomic prediction in underrepresented populations | [research.google/blog](https://research.google/blog/) (listing) | Science | M |
| 2026-09-03 | Complete male fruit fly connectome | [research.google/blog](https://research.google/blog/) (listing) | Science | M |
| 2026-09-10 ★ | ToolGrad: Efficient tool-use dataset generation with textual "gradients" | https://research.google/blog/toolgrad-efficient-tool-use-dataset-generation-with-textual-gradients/ | Agent training data | M |
| 2026-09-15 ★ | Bypassing inference bottlenecks: Accelerating complex AI search with Retrieve-for-Train | https://research.google/blog/bypassing-inference-bottlenecks-accelerating-complex-ai-search-with-retrieve-for-train/ | RL-compiled retrieval | M |
| 2026-09-17 | Generative UI tools for teachers (learning interactives) | [research.google/blog](https://research.google/blog/) (listing) | GenUI | M |
| 2026-09-18 | MilleMiglia: realistic instance generator for middle-mile logistics | [research.google/blog](https://research.google/blog/) (listing) | OR / benchmarks | M |
| 2026-09-24 | Automating coherent long-form video generation | [research.google/blog](https://research.google/blog/) (listing) | Video gen (possibly agentic pipeline; body not seen) | M |
| 2026-09-29 | How Diffusion Controller unifies and simplifies AI image generation | https://research.google/blog/how-diffusion-controller-unifies-and-simplifies-ai-image-generation/ | Image gen | M |
| Sep 2026 (date unverified) ★(peripheral) | Four ways Google Research scientists have been using Empirical Research Assistance | https://research.google/blog/four-ways-google-research-scientists-have-been-using-empirical-research-assistance/ | AI-for-research agents | L |
| 2026-10-02 | Toward provably private learning from federated data (TEE-based) | [research.google/blog](https://research.google/blog/) (listing) | Privacy infra | M |
| 2026-10-05 ★ | Open and Emergent Problems in Agentic Privacy and Security: A Contextual Angle | https://research.google/blog/open-and-emergent-problems-in-agentic-privacy-and-security-a-contextual-angle/ | Agent security | M |
| 2026-10-06 | Unlocking Earth AI's planetary geospatial foundation models for global public health | https://research.google/blog/earth-ais-planetary-geospatial-foundation-models-for-global-public-health/ | Science | M |
| 2026-10-07 | (Headline only) Does higher-quality work mean better workers? | [research.google/blog](https://research.google/blog/) (listing) | Econ / HCI | M |

### 1E. Google Developers Blog (AI label), complete for the window per the feed history

All dates **H** (feed pubDate). Category reflects the official summary.

| Date | Title | URL | Category |
|---|---|---|---|
| 2026-08-17 ★ | Build zero-trust AI agents with Google's Agent Development Kit | https://developers.googleblog.com/build-zero-trust-ai-agents-with-googles-agent-development-kit/ | Agent security / containment |
| 2026-08-24 ★ | How to Evaluate Live & Voice Agents in ADK | https://developers.googleblog.com/how-to-evaluate-live-voice-agents-in-adk/ | Agent evals |
| 2026-08-26 | Enterprise-Grade Precision for Long-Context Multimodal Embedding Inference on Cloud TPU | https://developers.googleblog.com/enterprise-grade-precision-for-long-context-multimodal-embedding-inference-on-cloud-tpu/ | Serving infra |
| 2026-08-27 | Decoding cosmic signals with deep learning and Keras | https://developers.googleblog.com/decoding-cosmic-signals-with-deep-learning-and-keras/ | Science / Keras |
| 2026-09-09 ★ | Announcing ADK for Kotlin 1.0: Building Production-Ready AI Agents in Kotlin, Android, and Beyond | https://developers.googleblog.com/announcing-adk-for-kotlin-10-building-production-ready-ai-agents-in-kotlin-android-and-beyond/ | Agent SDK |
| 2026-09-11 ★ | Autonomous LLM post-training with Tunix on TPUs | https://developers.googleblog.com/autonomous-llm-post-training-with-tunix-on-tpus/ | Agentic research loop / RL (GRPO) |
| 2026-09-15 ★ | Build zero-trust AI agents that judge intent, not just syntax | https://developers.googleblog.com/build-zero-trust-ai-agents-that-judge-intent-not-just-syntax/ | Runtime governance / prompt injection |
| 2026-09-16 ★ | Agent Anomaly Detection, now in Private Preview on the Gemini Enterprise Agent Platform | https://developers.googleblog.com/agent-anomaly-detection-now-in-private-preview-on-the-gemini-enterprise-agent-platform/ | Agent monitoring |
| 2026-09-17 ★(peripheral) | Why client SDK generation belongs in the open | https://developers.googleblog.com/why-client-sdk-generation-belongs-in-the-open/ | Tooling (agent-native CLIs, docs MCP servers) |
| 2026-09-22 | Colab is now part of your Google AI plan | https://developers.googleblog.com/colab-is-now-part-of-your-google-ai-plan/ | Product |
| 2026-09-23 ★ | Introducing Support for Local AI Models in the Antigravity SDK | https://developers.googleblog.com/introducing-support-for-local-ai-models-in-the-antigravity-sdk/ | Agent SDK / hybrid orchestration |
| 2026-09-24 ★ | Turn your REST APIs into MCP tools with Google Cloud API Gateway | https://developers.googleblog.com/turn-your-rest-apis-into-mcp-tools-with-google-cloud-api-gateway/ | Agent tool infra (MCP) |
| 2026-09-24 | Reproducing Olmo 3 7B Pre-training in MaxText: case study of large scale training on TPUs | https://developers.googleblog.com/reproducing-olmo-3-7b-pre-training-in-maxtext-case-study-of-large-scale-training-on-tpus/ | Training infra |
| 2026-09-30 | Accelerating Spatio-Temporal Attention for Video Diffusion on TPUs | https://developers.googleblog.com/accelerating-spatio-temporal-attention-for-video-diffusion-on-tpus/ | Kernels |
| 2026-10-06 | Bring multimodal semantic search to the edge with EmbeddingGemma 2 | https://developers.googleblog.com/google-ai-edge-with-embeddinggemma-2/ | On-device retrieval |
| 2026-10-06 | EmbeddingGemma 2: The Developer Guide | https://developers.googleblog.com/embeddinggemma-2-the-developer-guide/ | On-device retrieval |
| 2026-10-07 ★ | Supercharge your development with the Google Developer Knowledge API ecosystem (Developer Knowledge API + MCP Server, public preview) | https://developers.googleblog.com/supercharge-your-development-with-the-google-developer-knowledge-api-ecosystem/ | Agent grounding / MCP |
| 2026-10-08 ★ | The Outer Loop, Insights First: An Ambient Quality Agent That Diagnoses Your Production Agent (AQuA) | https://developers.googleblog.com/the-outer-loop-insights-first-an-ambient-quality-agent-that-diagnoses-your-production-agent/ | Agent monitoring / evals |
| 2026-10-08 | ML Drift: Next-Gen GPU AI/ML Inference at the Edge | https://developers.googleblog.com/ml-drift-next-gen-gpu-aiml-inference-at-the-edge/ | Edge inference |
| 2026-10-13 ★ | Optimizing a 200,000-line Python codebase overnight with Gemini 4 Argon | https://developers.googleblog.com/optimizing-a-200000-line-python-codebase-overnight-with-gemini-4-argon/ | Long-horizon coding agent |
| 2026-10-13 ★ | Gemini 4 Argon for Robotics | https://developers.googleblog.com/gemini-4-argon-for-robotics/ | Embodied agents |

Just before the window (context): 08-11 "Why Go is an Ideal Language for AI-Assisted Software Engineering"; 08-11 "Mastering Edge AI on Raspberry Pi with LiteRT and Gemma"; 08-13 "HeyGen x Google Cloud: Avatar IV on TPUs"; 08-13 "Introducing Credentio (C2PA C++ library)".

### 1F. Searched for and NOT found in the window (or not searchable)

- **Project Mariner:** no in-window post found. Mariner-style capability now appears to ship as Chrome auto browse and Gemini Spark browsing. Not searched directly because the search budget ran out. (sources: [Chrome auto browse on Android](https://blog.google/products-and-platforms/products/chrome/gemini-in-chrome-android-auto-browse/); [Gemini Spark](https://blog.google/innovation-and-ai/products/gemini-app/gemini-app-now-on-windows/))
- **Standalone "Gemini computer use model" post:** none found. Computer use appears as a *preview capability of Gemini 3.8 Flash* (model page) and in SDK and harness code (see deep note 6). It was not searched separately because the budget ran out. (sources: [3.8 Flash model card](https://deepmind.google/models/model-cards/gemini-3-8-flash/))
- **SIMA / Genie:** no 2026-08-14..10-14 post found. The latest are SIMA 2 (Nov 2025) and Project Genie + Street View (May 2026). 「无出处，待核」
- **AlphaEvolve:** no in-window post found. The latest are the May 7 impact update and Jul 9 Cloud GA. 「无出处，待核」
- **Jules:** no confirmed in-window post. The "proactive features" post has conflicting dates. (sources: [Jules proactive features post](https://blog.google/innovation-and-ai/technology/developers-tools/jules-proactive-updates/))
- **Frontier Safety Framework:** no new FSF version in the window. v3.1 (Apr 17, 2026) is current and was applied in the Argon model card. (sources: [FSF v3.1](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/); [Argon model card](https://deepmind.google/models/model-cards/gemini-4-argon/))
- **Gemini CLI:** its repo shows maintenance and bugfix activity only (v0.65.0-preview.0 changelog, 10-13). No feature blog post was found. 「无出处，待核」

**Inventory count:** 83 in-window rows: 21 DeepMind/model pages (1A), 21 blog.google (1B; the Jules row may be out of window), 3 antigravity.google (1C), 17 Google Research (1D) and 21 Developers Blog (1E). Six rows are the same post listed in two places (Argon launch, Argon safety, 3.8 Flash, 3.8 Live, Argon for Robotics, EmbeddingGemma 2), which leaves **about 77 unique posts or pages**. About 40 rows are tagged agent-relevant (★). 「无出处，待核」

---

## Part 2. Deep notes on the agent-relevant posts

### 1. Gemini 4 Argon: our next era of frontier intelligence (launch)
- **Date:** 2026-09-30 (H). **URL:** https://deepmind.google/blog/gemini-4-argon-our-next-era-of-frontier-intelligence/ (mirror at blog.google .../gemini-models/gemini-4-argon/). Third-party coverage credits Koray Kavukcuoglu (SVP, Chief AI Architect).
- **Source of substance:** official-search-extended + third-party-corroborated.
- First model of the Gemini 4 generation. Positioned above the Gemini 3.8 line for **long-running, multi-step work**. Named target domains are software engineering, financial research, legal drafting and cybersecurity patching.
- **Output ceiling raised from 64K to 1M tokens** (per launch coverage). Some Google pages instead describe a "1M token limit" or a "unified 1M input-output limit" in the Gemini API. *The sources do not agree on whether 1M is output-only or combined.*
- **Phased access at launch:** first through the **Fairwind Program** to trusted cyber defenders only. Developer, enterprise and consumer access was promised "once guardrails are refined" (Sep roundup). This is the first Google frontier launch gated on cyber-defender access.
- **Pricing [VR]:** introductory $2 / $10 per 1M input/output tokens until **2026-11-30**, then $4 / $20.
- **Benchmarks [VR, relayed by third parties]:** DeepSWE v1.1 **77.9%**, vs GPT-6 Astra 74.1% and Claude Opus 5.5 74.2%. It leads the Vals Index. Third-party coverage says it **trails** GPT-6 Astra and Opus 5.5 on FrontierSWE, Terminal-Bench 4.0 and some science tasks. One headline claims it wins "12 of 18 tests." Google chose the comparison set. Methodology is on DeepMind's site, and nobody outside Google has reproduced it.
- For comparison within Google's own line [VR]: 3.7 Flash scored 65.3% and 3.8 Flash 73.7% on DeepSWE v1.1.
- **Implications:** Google now ties frontier-model value to *hours-long autonomous tasks* (a 1M output budget, the overnight-agent case study, robotics). Long-horizon agentic RL and harnesses are the axis of competition, not single-turn quality.
- **Implications:** Leading on DeepSWE while trailing on Terminal-Bench 4.0 and FrontierSWE suggests that harness and benchmark choice drive "SOTA" claims. Compare across vendor harnesses before citing.

### 2. Gemini 4 Argon GA: "now available in the Gemini app" and "now available for developers" (plus "Built to solve your hardest problems")
- **Dates:** 2026-10-13 for both availability posts (M; python-genai commit `8554b07` "add gemini-4-argon to Model enum" is timestamped 2026-10-13). "Built to solve your hardest problems" is dated Sep 30 or Oct 13 (L).
- **URLs:** https://blog.google/innovation-and-ai/products/gemini-app/gemini-4-argon-availability/ ; https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-4-argon/ ; https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/
- **Source of substance:** official-search-standard + github-fulltext (SDK enum).
- Argon is available globally through the **Gemini API (AI Studio, Gemini Enterprise Agent Platform), Google Antigravity, the Gemini app** (Google AI Pro and Ultra) and **AI Mode in Search**, 13 days after the Fairwind-only launch.
- The SDK model description reads: "Our new frontier model, built to solve the hardest problems with depth and precision across real-world software engineering and knowledge work." 3.8 Flash in the same enum is "engineered for long-horizon software engineering, autonomous agents, and complex enterprise workflows."
- The same python-genai history shows the **Interactions API** gaining agent-infra primitives in this window: `environments` (file upload/download, `from_environment` copying, a **network egress allowlist** with `"allowlist": "disabled"` added 10-07), `triggers`, `webhooks`, `agents`, a `CONTINUATION_REQUIRED` interaction status with `continuation_token` (10-02 to 10-09), and a `codemender` agent config with find/fix requests. These are managed-agent sandbox primitives that sit beside the Argon GA.
- Pricing is the same as the launch post: $2/$10 intro to 11-30, then $4/$20 [VR].
- **Implications:** The managed `environments` + `network allowlist` + `triggers` + `continuation_token` surface amounts to Google's hosted long-running agent runtime. Watch it as the counterpart to the Claude Agent SDK and OpenAI's Agents/Responses environments.
- **Implications:** The 13-day gated-to-GA gap is a concrete data point for "staged release for cyber-capable models" policy comparisons.

### 3. Developing Gemini 4 Argon responsibly and safely, plus the Argon model card
- **Date:** October 2026 (it appears in DeepMind's October listing; likely 10-13) (L–M). **URLs:** https://blog.google/innovation-and-ai/technology/safety-security/gemini-4-model-safety-security/ ; https://deepmind.google/models/model-cards/gemini-4-argon/ ; https://deepmind.google/models/gemini/cyber/
- **Source of substance:** official-search-extended.
- **FSF assessment:** evaluated under FSF v3.1 (April 2026). The model card says Google **cannot rule out that Argon reached some CBRN (biological) and cybersecurity Critical Capability Levels**, so it applied mitigations. For contrast, the 3.7 Flash card reached no tracked or critical CCL but hit the *alert threshold* for one CBRN CCL.
- **Phased rollout rationale:** "Safely releasing frontier capabilities at this level requires a phased approach." Fairwind trusted defenders came first, then wider release after testing.
- **Government pre-release testing:** Google takes part in the U.S. government's voluntary pre-release model-access process. It also used third-party partners to measure certain capabilities and safeguards.
- **Misuse defense:** a multi-layer stack covering jailbreak resistance, monitoring and enforcement.
- **Prompt injection:** Google states Argon is its **"most resilient model yet against indirect prompt injection"** [VR]. No IPI numbers or benchmarks were surfaced.
- **Misalignment mitigation (key for agent safety):** Google **monitors Argon's chain-of-thought and actions and stops execution when Argon strays beyond user intent.** This is CoT-plus-action monitoring with intervention, applied in a production launch.
- **Cyber variant:** a separate "Gemini 4 Argon without cyber guardrails" is offered to trusted defenders.
- **Caveat:** all of this is self-reported, and no monitor false-positive or false-negative rates or IPI attack-success rates were found.
- **Implications:** Production CoT+action monitoring that can halt runs connects directly to DeepMind's June AI Control Roadmap (asynchronous transcript review for low-risk actions, synchronous blocking for high-risk ones). The model card is the place to find which tier applies to Argon's agentic surfaces.
- **Implications:** The "most resilient to IPI" claim with no published ASR is a gap. Browser-agent researchers should test it on their own injection suites.

### 4. Gemini 4 Argon for Robotics
- **Date:** 2026-10-13 (H). **URL:** https://developers.googleblog.com/gemini-4-argon-for-robotics/
- **Source of substance:** feed-summary-only.
- Argon is pitched as a **general-purpose physical reasoning model** across the robotics stack: physical understanding, code generation, and visual-semantic reasoning.
- It is available in AI Studio, the Gemini API and **Google Antigravity** for building and testing robot apps, so the coding-agent IDE doubles as a robotics dev environment.
- The workflow is **simulation-verified code-as-policies**. Developers use MuJoCo to go "from real-world data or sketches to physically verified robot control," with **self-improvement workflows** (the model iterates on policies against simulator feedback).
- Context (out of window): Gemini Robotics ER 2 (about Jul 30) is the specialized embodied-reasoning planner that hands off to VLAs. It reports ER 1.6 to ER 2 real-VLA-control at 48.6% to 60.0% and safety-instruction-following at 97.9% [VR]. Argon is the general model alongside it.
- **Implications:** A "self-improvement against a simulator verifier" loop is agentic RL-like iteration at inference time. It is a template for computer-use agents that verify against environment state.

### 5. Optimizing a 200,000-line Python codebase overnight with Gemini 4 Argon
- **Date:** 2026-10-13 (H). **URL:** https://developers.googleblog.com/optimizing-a-200000-line-python-codebase-overnight-with-gemini-4-argon/
- **Source of substance:** feed-summary + **github-fulltext** (google/adk-python commit `1754b3e`, 2026-10-07, "perf: cut time to first model request by 40% in long sessions", message ends **"Argon generated these changes"**).
- **Setup (feed):** the engineering team ran Argon **unattended overnight** on the open-source ADK Python repo (about 200k lines), using **`.agents/skills`** and **`/goal` mode**.
- **The skills, from the repo:** `.agents/skills/` contains 11 skills: adk-agent-builder, adk-architecture, adk-debug, adk-git, adk-review, adk-sample-creator, adk-setup, adk-style, adk-unit-design, adk-unit-guide and adk-verify-snippets. Each is a SKILL.md, with references/ or scripts/ in some. adk-verify-snippets, for example, has a strict "read-only contract" and runs every Markdown Python block in an isolated subprocess. These skills are the codebase-specific scaffolding that made unattended work possible.
- **What changed (commit text):** `InMemorySessionService` deep-copied the whole session on every read, and importing ADK eagerly loaded OpenTelemetry, auth and the LLM-flow modules, including live mode. The fix speeds up Event and Session deep copies (new `utils/_model_copy.py`, 148 lines). `get_session` now copies only the returned events and `list_sessions` copies none. The heavy imports are deferred until first use, "without changing the requests sent to the model." It touched 19 files.
- **Benchmark in the commit [VR]:** median of 6–12 runs, with a no-op model and instant tools so only ADK overhead is measured (* = GC disabled):
  - first model request after 50 turns*: 64 ms → 36 ms (**−43%**)
  - first model request after 150 turns*: 200 ms → 122 ms (−39%)
  - whole 158-turn run: 65.6 s → 56.1 s (−14%)
  - import ADK in a new process: 1.22 s → 0.97 s (**−21%**)
  - new process to first model request: 3.07 s → 3.09 s (+1%, no change)
- The blog's "40% session-prep overhead" and "21% cold import" figures match this table exactly. **Caveat:** cold start to first request did *not* improve, and these are framework-overhead microbenchmarks, not end-to-end agent latency.
- Follow-up commits that week continue the same theme ("stop importing unused providers on the first LLM request", 10-09; "defer the sessions.state import", 10-13; "test: measure packages introduced by isolated imports", 10-09). It looks like a sustained agent-driven perf campaign, though only `1754b3e` is explicitly attributed to Argon.
- **Implications:** This is a reproducible, public artifact of a frontier model doing an overnight autonomous perf task with a measured, reviewable diff. Use it as a case study of the "skills + goal mode + benchmark harness" pattern for long-horizon coding agents.
- **Implications:** The design (a deterministic benchmark with a no-op model as the reward signal) mirrors verifiable-reward setups for agentic RL on SWE tasks.

### 6. Introducing Gemini 3.8 Flash and 3.8 Flash Cyber (computer-use-capable workhorse)
- **Date:** 2026-09-02 (H). **URLs:** https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/ ; model card https://deepmind.google/models/model-cards/gemini-3-8-flash/ ; Cyber evals https://deepmind.google/models/evals-methodology/gemini-3-8-flash-cyber ; Antigravity post https://antigravity.google/blog/gemini-3-8-flash-in-google-antigravity/
- **Source of substance:** official-search-extended + github-fulltext (SDK, ADK, computer-use-preview).
- It is Google's **third Flash release in about 6 weeks** (3.6 in late July, 3.7 on Aug 13, 3.8 on Sep 2). The model card says 3.8 Flash is **based on 3.7 Flash**: a further-trained version, not a new base. That points to rapid post-training (RL) iterations on a fixed base.
- **Claims [VR]:** significant gains over 3.7 Flash in SWE, agentic tasks and multi-step specialized reasoning. DeepSWE v1.1 is **73.7% vs 65.3%** (3.7 Flash). For the 3.7 Flash launch, FrontierCode 1.1 Main was 43.6% vs 34.4% (3.6) and DeepSWE 65.3% vs 49.0% (the card says 48.6%).
- **Specs:** 1,048,576 input / 65,536 output tokens. **Computer use: "Supported (Preview)"** on the official model page. Third parties call it Google's recommended computer-use model, but that is *not confirmed on Google pages*. **No computer-use benchmark numbers (OSWorld or similar) were found for 3.8 Flash.**
- **Pricing [VR]:** $0.75 / $3.75 per 1M tokens (intro, to 2026-12-31), then $1.50 / $7.50 from 2027-01-01. Available in the Gemini API, AI Studio and Antigravity, and to Pro/Ultra consumers.
- **3.8 Flash Cyber:** restricted to Fairwind trusted defenders and paired with the **CodeMender harness** to "find, verify, and fix vulnerabilities at agentic scale." It reports "frontier-level" CyberGym results and **CWE-Bench pass@1 47.2% vs 47.8%** for "a leading frontier model" [VR]. One Google chart is internally inconsistent (71.0% vs 58.2% on the same source-code scanning task), so treat those numbers with caution.
- **Computer-use action schema (github-fulltext):** Gemini 3.5 Flash and later emit a **new predefined action set**: `click, double_click, triple_click, middle_click, right_click, mouse_down, mouse_up, move, type, drag_and_drop, wait, press_key, key_down, key_up, hotkey, take_screenshot, scroll, go_back, navigate, go_forward`. The legacy set (2.5 CU preview, 3-flash-preview, 3.1-pro-preview) was `open_web_browser, click_at, hover_at, type_text_at, scroll_document, scroll_at, wait_5_seconds, search, navigate, key_combination, drag_and_drop`. Sources: google-gemini/computer-use-preview `agent.py`, whose reference agent keeps screenshots only for the last 3 turns (`MAX_RECENT_TURN_WITH_SCREENSHOTS = 3`) and defaults to gemini-3.6-flash as of 2026-07-28. ADK commit `b90e4a5` (2026-10-13) added a translation layer so `ComputerUseToolset` works with both action sets. It excludes optional 3.x actions unless the computer implements them, serializes concurrent actions per computer with an RLock, and normalizes drag coordinates. ADK commit `facaf29` fixed a **cross-session sandbox mix-up**: one `AgentEngineSandboxComputer` serving many sessions could drive another session's sandbox, and it is now bound per tool call through a contextvar. adk-samples `9c9f2d2` (09-18) also moved a sample to the 3.x action aliases.
- **Implications:** Google's CU action space has moved from coarse web-only "click_at/type_text_at + search" to a **desktop-grade low-level mouse and keyboard space** (mouse_down/up, key_down/up, hotkey, right/middle click). That matters for OSWorld-style evals and RL action-space design.
- **Implications:** The per-tool-call sandbox binding bug is a real containment lesson. Multi-tenant CU sandboxes need per-call session binding, or one user's agent can act in another's environment.

### 7. Antigravity Teamwork: "Pairing Google Antigravity with Gemini 3.7 Flash solves notable multi-agent math and engineering problems"
- **Date:** about 2026-08-27/28 (L; "~47 days ago" metadata). **URLs:** https://blog.google/innovation-and-ai/technology/developers-tools/antigravity-teamwork-multi-agent/ ; companion https://antigravity.google/blog/teamwork-when-ai-becomes-a-research-partner/ ; docs https://antigravity.google/docs/teamwork/
- **Source of substance:** official-search-extended.
- **What it is:** Teamwork is a multi-agent framework in Antigravity 2.0 and the Antigravity CLI, invoked as `/teamwork-preview`. It was first shown at I/O 2026 and updated since. Agents "propose, critique, and refine each other's work autonomously over hours or days."
- **Design rationale:** loose multi-agent setups drift, so Teamwork structures the loop as **generate candidates → stress-test → combine the best ideas** into a stronger candidate.
- **Two-phase protocol (docs):** In Phase 1, the main agent **interviews the user** about scope, requirements and *how each requirement will be verified*, then emits a reviewable prompt artifact. In Phase 2, a **Project Orchestrator** runs autonomously and **assigns specific files to individual Workers** so their edits don't conflict.
- **Results [VR]:** seven open math problems solved. Three of them were reproduced with 3.7 Flash; they were originally obtained with Gemini 3.1 Pro, some with higher-than-default parallelism. The work includes **Knuth's Cycles Conjecture verified in Lean** (40+ page proofs) and **71% on TCSBench**.
- **Systems result [VR]:** a cycle-accurate, out-of-order **RISC-V simulator that boots xv6 to a shell**, with **0.71% cycle-alignment error** vs hardware ground truth. Performance patches were also **merged upstream in Eigen and ParlayHash**.
- **Scale data point (separate Antigravity post, date uncertain) [VR]:** "built an OS" using **93 subagents and more than 339M input tokens**, and also an AlphaZero-style game app.
- **Caveats:** the feature is labeled preview, nobody outside Google has evaluated it, and the math results partly come from an earlier, larger model.
- **Implications:** The verification-first interview (Phase 1) plus file-ownership sharding (Phase 2) is a concrete multi-agent harness design. It is worth comparing against single-agent long-horizon setups when designing agentic RL environments that reward verifiable sub-goals.
- **Implications:** Lean-verified proofs and hardware-ground-truth simulators are strong examples of *external verifiers* closing the loop for long-running agents.

### 8. Agent Anomaly Detection, now in Private Preview on the Gemini Enterprise Agent Platform
- **Date:** 2026-09-16 (H). **URL:** https://developers.googleblog.com/agent-anomaly-detection-now-in-private-preview-on-the-gemini-enterprise-agent-platform/
- **Source of substance:** feed-summary-only, cross-checked with the 09-15 companion post's summary.
- An **out-of-band oversight layer**. It analyzes **OpenTelemetry traces and tool calls** asynchronously, so it adds **no runtime latency** to live requests.
- **Multi-tiered pipeline:** lightweight **statistical scanning** first, escalating to **deep LLM-based reasoning**, to flag logical anomalies and policy violations.
- Detection taxonomy grounded in the **OWASP Agentic Top 10**.
- Findings are triaged in **Security Command Center**. An exposed API lets developers **programmatically block subsequent tool calls** once an agent breaches a risk threshold, turning asynchronous detection into near-real-time containment.
- Positioned as the third managed defense alongside Model Armor (prompt screening) and Semantic Governance Policies (see note 9), specifically to catch **multi-turn exploits** that per-request filters miss.
- No detection-rate or false-positive numbers were found in the summary.
- **Implications:** It productizes the DeepMind AI Control Roadmap pattern of asynchronous transcript review escalating to blocking, for third-party agents. It is a useful reference architecture for trace-level monitors in CU-agent safety research.
- **Implications:** Trace-based statistical-then-LLM tiers are a cheap-monitor/expensive-monitor cascade. Researchers should ask how it handles slow, multi-turn injection campaigns.

### 9. Build zero-trust AI agents that judge intent, not just syntax
- **Date:** 2026-09-15 (H). **URL:** https://developers.googleblog.com/build-zero-trust-ai-agents-that-judge-intent-not-just-syntax/
- **Source of substance:** feed-summary-only.
- Argues for moving from **static build-time controls to dynamic runtime governance** on the Gemini Enterprise Agent Platform.
- Three managed defenses: **Model Armor**, which screens prompts at the edge; **Semantic Governance Policies**, which evaluate a *tool call's intent* against business rules rather than its syntax; and **Agent Anomaly Detection** for multi-turn exploits.
- Admins enforce these at the platform level, **without modifying or redeploying agent code**.
- **Implications:** The "intent-level tool-call policy" is an LLM-judge gate on actions. Its robustness to adaptive attacks is the open question, since the literature shows adaptive attacks break many static PI defenses.

### 10. Build zero-trust AI agents with Google's Agent Development Kit
- **Date:** 2026-08-17 (H). **URL:** https://developers.googleblog.com/build-zero-trust-ai-agents-with-googles-agent-development-kit/
- **Source of substance:** feed-summary-only.
- Thesis: agents that **mutate production state** need hard boundaries, not "soft system prompts."
- Three mechanisms: **hardware-backed cryptographic signatures for database writes**, **gVisor kernel-level sandboxing** for dynamically generated code, and **deterministic semantic gateways** for I/O validation.
- Explicitly framed against **prompt injection** and malicious execution in multi-tool ADK workflows.
- **Implications:** Signed writes plus gVisor plus deterministic gateways is a defense-in-depth reference for containment that doesn't depend on model robustness. Pair it with model-level IPI claims (note 3) when threat-modeling CU agents.

### 11. Introducing Support for Local AI Models in the Antigravity SDK
- **Date:** 2026-09-23 (H). **URL:** https://developers.googleblog.com/introducing-support-for-local-ai-models-in-the-antigravity-sdk/
- **Source of substance:** feed-summary-only. No public Antigravity SDK repo could be reached.
- The Antigravity SDK can run **offline agentic workflows locally**, for example with **Gemma 4 26B A4B** (a MoE with about 4B active parameters) via **LiteRT**.
- **Hybrid orchestration:** a **cloud model acts as a lightweight planner** while **local models handle token-intensive work** such as code auditing and patching on-device, for privacy and cost.
- **Drop-in support for OpenAI-compatible servers** such as **Ollama and vLLM**, enabling "privacy-first, autonomous local utilities."
- **Implications:** Planner-in-cloud / executor-on-device splits create a new trust boundary. The local executor sees raw data and the cloud planner sees summaries, which is relevant to agentic-privacy threat models (note 15) and to distilling planners vs executors in agentic RL.

### 12. The Gemini app is now available for Windows (Gemini Spark), plus the Spark/Live integration (Aug 26)
- **Dates:** about 2026-09-10 (M) and 2026-08-26 (M). **URLs:** https://blog.google/innovation-and-ai/products/gemini-app/gemini-app-now-on-windows/ ; https://blog.google/innovation-and-ai/products/gemini-app/productivity-features-gemini-live/
- **Source of substance:** official-search-standard.
- The desktop app is for **Windows 10 and 11**, global, from gemini.google/desktop. **Alt+Space** opens Gemini over the active window.
- Its dedicated workspace lets users **delegate multi-step tasks to Gemini Spark** (Google's "24/7 personal AI agent," launched at I/O 2026 and built on Antigravity). Spark can synthesize files across Gmail and Drive and generate Nano Banana images or Omni videos.
- **Aug 26:** Gemini Live connects to Spark, so **voice commands set up multi-step tasks that run on their own**, across Docs, Sheets and Drive, including **jobs that run over days or weeks**.
- **Availability:** Google AI Pro or higher. Not offered in the EEA, UK, Switzerland or Nigeria (per the July Drop).
- **Roadmap items not confirmed as shipped:** at I/O, Google said Spark would gain texting and email access, custom sub-agents, and **local browser control**. Separately, a July update had already integrated Chrome auto browse with Spark, including logged-in accounts and saved passwords with permission.
- **Implications:** A desktop-resident agent with multi-day task horizons and logged-in browser access is the consumer CU frontier. Its permission and confirmation design is worth comparing with Claude for Chrome and OpenAI's Atlas/Operator.

### 13. Gemini in Chrome with auto browse comes to Android (context: Chrome auto browse)
- **Date:** August 2026 (L; listed in the August roundup as "Gemini in Chrome on Android"). The desktop auto browse launch is **out of window** (early 2026, the Gemini 3 era). **URLs:** https://blog.google/products-and-platforms/products/chrome/bringing-chrome-ai-to-android/ ; https://blog.google/products-and-platforms/products/chrome/gemini-in-chrome-android-auto-browse/ ; desktop: https://blog.google/products-and-platforms/products/chrome/gemini-3-auto-browse/
- **Source of substance:** official-search-standard.
- Auto browse is Gemini-in-Chrome's **agentic multi-step web task mode**. It is gated to **Google AI Pro and Ultra** (US, then India and other regions; India is English-only).
- Android examples: booking event parking, updating a recurring online order, organizing travel. Desktop examples: comparing hotel and flight prices across dates, filling forms from a PDF.
- **Safety design (Google's claim):** it **pauses for confirmation before sensitive actions** such as purchases or social posting, and is **"built to resist prompt injection."** No ASR numbers were found.
- With Spark (July, out of window), it can use **logged-in accounts and saved passwords** with permission.
- **Implications:** This is the largest-distribution browser agent on mobile, so mobile-web CU evals and IPI attacks through mobile pages become practically relevant.

### 14. Piloting the world's first double-blind AI evaluations
- **Date:** 2026-08-27 (M). **URL:** https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/
- **Source of substance:** official-search-standard. Only partial substance was retrieved.
- **Problem:** benchmark contamination (models having seen test items) and the reverse risk that evaluators must expose confidential test sets to model developers.
- **Mechanism:** a "double-blind" setup where **external tests stay inside a cryptographic box**. The model developer can't see or optimize on the tests, and the evaluator doesn't get the model weights.
- **Partners:** the **Singapore AI Safety Institute, OpenMined, AVERI and MLCommons**. The model tested was a **Gemini Flash-Lite** model against **confidential benchmarks**.
- **Motivation:** sensitive evaluations such as **cybersecurity** or government use, where test secrecy matters.
- Specific crypto primitives (secure enclaves vs MPC) and any results were not retrieved.
- **Implications:** It offers a path to held-out, uncontaminated agent benchmarks, for example private CU or IPI suites run by third parties. That is directly relevant to anyone building private browser-agent evals.

### 15. Open and Emergent Problems in Agentic Privacy and Security: A Contextual Angle
- **Date:** 2026-10-05 (M). **URL:** https://research.google/blog/open-and-emergent-problems-in-agentic-privacy-and-security-a-contextual-angle/
- **Source of substance:** official-search-standard. Only partial substance was retrieved.
- A workshop report gathering **50+ academic and industry researchers**.
- Its theoretical frame is **Contextual Integrity**: privacy as appropriate information flow within contexts.
- **Core tension:** useful agents need personal data *and* the authority to act on it.
- It calls for defenses at four levels: **system, model, user and ecosystem**.
- Specific open problems were not retrieved. Related literature in the same results covers indirect IPI-driven exfiltration and cross-session memory leakage.
- **Implications:** The CI framing gives a principled spec for "should this agent send this datum to this site?", which is useful for designing privacy-leak metrics in browser-agent benchmarks.

### 16. ToolGrad: Efficient tool-use dataset generation with textual "gradients"
- **Date:** 2026-09-10 (M). **URL:** https://research.google/blog/toolgrad-efficient-tool-use-dataset-generation-with-textual-gradients/ ; paper arXiv 2508.04086 (ACL 2026); code github.com/zhongyi-zhou/toolgrad
- **Source of substance:** official-search-standard + third-party (arXiv).
- **Authors:** Zhongyi Zhou and Ruofei Du (Google), with University of Tokyo, RIKEN AIP and Tohoku collaborators.
- **Inversion ("answer-first"):** prior pipelines (ToolBench, ToolACE) sample APIs, invent a user query, then search for a solution with DFS agents, which is expensive and often fails. ToolGrad **builds valid tool-use chains first**, then **writes the user query to match**.
- **Mechanism:** an agentic loop that **chains APIs iteratively in minibatches over a large API database**, guided by **textual "gradients"** (TextGrad-style LLM feedback as the update signal).
- **Output [VR]:** **ToolGrad-500**, with more complex tool use, lower generation cost and a **near-100% pass rate**. Models trained on it beat models trained on costlier baselines and some proprietary LLMs.
- **Critique:** a 2026 follow-up ("Execution-First Synthetic Tool-Use Trace Generation") argues it adds workflow complexity without guaranteeing correctness.
- **Implications:** Answer-first synthesis guarantees *executable* trajectories, which is a cheap way to bootstrap SFT and RL data for tool or CU agents before online RL.

### 17. Bypassing inference bottlenecks: Accelerating complex AI search with Retrieve-for-Train
- **Date:** 2026-09-15 (M). **URL:** https://research.google/blog/bypassing-inference-bottlenecks-accelerating-complex-ai-search-with-retrieve-for-train/ ; paper "Efficient, Property-Aligned Fan-Out Retrieval via RL-Compiled Diffusion" (ICML 2026).
- **Source of substance:** official-search-standard (two independent search passes agree).
- **Authors:** Pengcheng Jiang and Judith Yue Li.
- **Problem:** AI search fans a query out into multiple sub-queries. Autoregressive reasoning at query time sets a latency floor that conflicts with sub-second retrieval.
- **Mechanism:** use **offline RL** once to discover good sub-query sets, so the property-aligned slates become the RL output. Then **"compile" them into training data for a lightweight diffusion model** that generates the whole slate **in one parallel pass** at inference.
- **Result [VR]:** **12–20x faster inference** vs autoregressive approaches. Retrieval-quality numbers were not retrieved.
- **Implications:** "RL-compile then distill into a fast non-autoregressive policy" is a general pattern. It could apply to agent sub-steps such as query planning or action proposal, where test-time reasoning is too slow.

### 18. Advancing Private AI Compute with secure, server-side memory
- **Date:** 2026-09-23 (M). **URL:** https://deepmind.google/blog/advancing-private-ai-compute-with-secure-server-side-memory/ ; background: https://blog.google/innovation-and-ai/products/google-private-ai-compute/
- **Source of substance:** official-search-standard.
- **Change:** Private AI Compute (PAC), which runs on Titanium Intelligence Enclaves (TIE), was **strictly stateless** and wiped context when a task ended. It now adds a **persistent, cross-device memory layer**.
- **Storage:** memory sits in **encrypted cloud storage**, and the **decryption keys stay on the user's devices**. The claim is that the data is inaccessible to anyone else, "even Google."
- **Processing:** the device opens an **authenticated end-to-end encrypted channel** into an isolated enclave. The enclave decrypts in isolated memory, saves new context and **re-encrypts**.
- **Verifiability:** devices **verify server software authenticity before sending data**. Google commits to a **tamper-proof public record (transparency log)** of server software and an **independent audit by a cybersecurity firm**.
- User-facing rollout timing was not stated in the retrieved snippets.
- **Implications:** This is the first frontier-lab architecture for *confidential, persistent agent memory*. It is relevant to long-running agents such as Spark that need memory without becoming an exfiltration target. Note that enclave memory doesn't protect against *prompt-injected agents* reading their own memory.

### 19. The Outer Loop, Insights First: An Ambient Quality Agent That Diagnoses Your Production Agent (AQuA)
- **Date:** 2026-10-08 (H). **URL:** https://developers.googleblog.com/the-outer-loop-insights-first-an-ambient-quality-agent-that-diagnoses-your-production-agent/ ; code: google/adk-samples `core/python/ambient-quality-agent` (release v0.1.0 committed 2026-10-08; the README says it lives in google/adk-recipes).
- **Source of substance:** **github-fulltext** (README) + feed summary.
- **Problem:** silent quality regressions in production agents "return HTTP 200 OK."
- An ADK agent that **runs beside the observed agent** and reads its telemetry from three sources: the BigQuery Agent Analytics plugin, Cloud Trace `_AllSpans`, or agents-cli Cloud Logging.
- Investigations run **on a schedule, after each deployment, or on demand**. Each conversation gets an **LLM review against the agent's config and an evaluation goal**, plus **deterministic Python checks** you publish (`agents-cli aqua metrics publish`) or Gemini-platform eval metrics.
- **Deduplicated "insights"** have status NEW / RECURRING / RESOLVED with occurrence history, so recurring failures appear once.
- **Root-cause analysis is anchored to the observed agent's published source snapshot** and proposes fixes. AQuA keeps a memory of facts the user asks it to remember.
- Ships with an `agents-cli-aqua` **skill so a coding agent can deploy AQuA, inspect insights and fix defects**, closing the loop from production monitoring to a coding agent.
- **Implications:** Production transcripts → clustered failure insights → coding-agent fix is an "outer-loop" self-improvement pipeline. It is the offline analogue of agentic RL from deployment feedback.

### 20. Autonomous LLM post-training with Tunix on TPUs ("autofinetune"), plus Tunix agentic-RL repo activity
- **Date:** 2026-09-11 (H). **URL:** https://developers.googleblog.com/autonomous-llm-post-training-with-tunix-on-tpus/
- **Source of substance:** feed-summary + github-fulltext (google/tunix commits; the autofinetune code itself was not found in the tunix repo).
- **Post:** an **autonomous research loop**. A single **Markdown spec** defines boundary conditions and eval metrics. An AI agent **edits training scripts, launches SFT and RL (GRPO) experiments**, and **auto-commits verified hyperparameter improvements to Git**. It is demonstrated on **function calling and math reasoning** with Gemma on Cloud TPUs. No specific gain numbers appear in the summary.
- **Repo (agentic RL infra, in window):** Tunix has an `examples/deepswe` **agentic RL** setup with `r2egym` and `sweagent` scaffolds. The OpenHands scaffold was removed on 10-08. It includes a **failure-aware `ActionGuard`** between `agent.update_from_model()` and `env.step()` that blocks repeated failed edits (default 3), forces view or search after "not found" or "non-unique" edit errors, and injects synthetic observations when blocking.
- Commit `8dcf606` (10-11) is a concrete RL pathology: stripping `<tool_call>` tokens broke the Qwen3.5 tool format. **In agentic RL on DeepSWE with Qwen3.5-35B-A3B, about a fifth of rollouts degenerated into repeated `</function>` until the length cap, which more than doubled step time.**
- Other commits: a TrajectoryStore persisting per-turn steps, rewards and terminal status, including FAILED, TIMEOUT and CANCELLED (10-08); **MoE router-replay persistence** (`prefill_routed_experts`) so partially-run trajectories can be recovered (10-08); `overlong_filter` `masked_out` persisted on the Trajectory (10-09); pre-tokenized prompt IDs passed to samplers to avoid lossy decode/re-encode round-trips (09-21); and a FrozenLake agentic-vs-non-agentic RL efficiency benchmark (10-05).
- **Implications:** Google's open agentic-RL stack is converging on the same engineering concerns as other labs: exact token-ID preservation, MoE routing replay for off-policy correction, overlong filtering and trajectory stores. The DeepSWE degeneration commit is a quotable case of chat-template bugs silently corrupting agentic RL.

### 21. How to Evaluate Live & Voice Agents in ADK
- **Date:** 2026-08-24 (H). **URL:** https://developers.googleblog.com/how-to-evaluate-live-voice-agents-in-adk/
- **Source of substance:** feed-summary-only.
- **Native live evaluation** in ADK, for graph-based agent workflows.
- **LLM-driven simulated users generate actual audio via Gemini TTS**, so tests run multi-turn spoken conversations.
- Scenarios and **natural-language rubrics** score audio responses *and tool executions*. Transcripts can be inspected in ADK Web, and the CLI runs in CI/CD.
- **Implications:** Simulated-user plus rubric evaluation of tool calls carries over to CU agents, and the user simulator is a reusable environment component for RL.

### 22. Announcing ADK for Kotlin 1.0 (brief)
- **Date:** 2026-09-09 (H). **URL:** https://developers.googleblog.com/announcing-adk-for-kotlin-10-building-production-ready-ai-agents-in-kotlin-android-and-beyond/
- **Source of substance:** feed-summary-only.
- Feature parity with the Python and Java ADK cores. Built on **Kotlin Multiplatform**, with **KSP zero-reflection type-safe function calling**, **human-in-the-loop** workflows and **context compaction**.
- Android extensions: **local models via LiteRT-LM**, Firebase AI for cloud reasoning, **Room session persistence** and **AppSearch semantic memory**.
- **Implications:** It brings on-device agents with local memory to Android, alongside Gemini Intelligence and Spark. That makes on-device mobile agents a likely target surface for evals.

### 23. Agent tool infrastructure (brief): API Gateway as MCP server (09-24), Developer Knowledge API + MCP Server (10-07), open-sourced SDK generation (09-17)
- **Source of substance:** feed-summary-only. URLs: [API Gateway (09-24)](https://developers.googleblog.com/turn-your-rest-apis-into-mcp-tools-with-google-cloud-api-gateway/); [Developer Knowledge API (10-07)](https://developers.googleblog.com/supercharge-your-development-with-the-google-developer-knowledge-api-ecosystem/); [SDK generation (09-17)](https://developers.googleblog.com/why-client-sdk-generation-belongs-in-the-open/)
- **API Gateway** turns OpenAPI 3.x operations into **MCP tools** through the `x-google-api-management.mcp` annotation. It transcodes MCP JSON-RPC to REST, and existing auth, quotas and logging apply to agent traffic.
- **Developer Knowledge API + MCP Server** (public preview) gives a canonical, machine-readable docs corpus across Firebase, Cloud and Android for grounding coding agents.
- **Speakeasy partnership:** AGPLv3 OpenAPI SDK generators, including **agent-native CLIs** and **docs MCP servers**.
- **Implications:** Google is standardizing on MCP as the tool layer across Cloud. Agent harness research should assume MCP-exposed enterprise APIs are the default action surface alongside GUI CU.

---

## Part 3. Cross-cutting observations for browser/computer-use agents and agentic RL

1. **CU is a capability of the workhorse models, not a separate model.** Since Gemini 3.5 Flash, computer use is a preview capability of the mainline Flash models (3.6 is the harness default; 3.8 Flash's model page lists it), with a new **desktop-grade action set**. No in-window CU benchmark was published. The evidence comes from code: ADK's 10-13 action-schema migration and the computer-use-preview repo. (sources: [3.8 Flash post](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/); [3.8 Flash model card](https://deepmind.google/models/model-cards/gemini-3-8-flash/); [google/adk-python](https://github.com/google/adk-python); [google-gemini/computer-use-preview](https://github.com/google-gemini/computer-use-preview))
2. **Long-horizon autonomy is the product thesis.** Argon's 1M-token output, the overnight `/goal` + `.agents/skills` run on ADK, Teamwork's hours-to-days multi-agent loops, Spark's days-to-weeks jobs, and the managed Interactions `environments` / `triggers` / `continuation_token` API all point the same way. (sources: [Argon launch](https://deepmind.google/blog/gemini-4-argon-our-next-era-of-frontier-intelligence/); [overnight run](https://developers.googleblog.com/optimizing-a-200000-line-python-codebase-overnight-with-gemini-4-argon/); [Teamwork](https://blog.google/innovation-and-ai/technology/developers-tools/antigravity-teamwork-multi-agent/); [Spark](https://blog.google/innovation-and-ai/products/gemini-app/gemini-app-now-on-windows/); [googleapis/python-genai](https://github.com/googleapis/python-genai))
3. **Safety is layered with monitoring at the center.** It includes CoT-plus-action monitoring with execution halting (Argon), out-of-band trace anomaly detection with tool-call blocking (Agent Anomaly Detection), intent-level tool-call policies, gVisor and signed writes, Fairwind gated access for cyber-capable models, and double-blind third-party evals. **Quantitative IPI/ASR or monitor-accuracy numbers were missing from everything retrieved.** (sources: [Argon safety](https://blog.google/innovation-and-ai/technology/safety-security/gemini-4-model-safety-security/); [Agent Anomaly Detection](https://developers.googleblog.com/agent-anomaly-detection-now-in-private-preview-on-the-gemini-enterprise-agent-platform/); [intent-level policies](https://developers.googleblog.com/build-zero-trust-ai-agents-that-judge-intent-not-just-syntax/); [zero-trust ADK](https://developers.googleblog.com/build-zero-trust-ai-agents-with-googles-agent-development-kit/); [Fairwind](https://blog.google/innovation-and-ai/technology/safety-security/fairwind-program/); [double-blind evals](https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/))
4. **Rapid post-training cadence on a fixed base.** Flash 3.6 → 3.7 → 3.8 shipped in about 6 weeks, and 3.8 is "based on 3.7 Flash," which suggests heavy RL post-training iteration. DeepSWE v1.1 went 49.0 → 65.3 → 73.7 → 77.9 (Argon) [VR]. (sources: [3.8 Flash post](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/); [Argon launch](https://deepmind.google/blog/gemini-4-argon-our-next-era-of-frontier-intelligence/))
5. **Gaps to fill if more search budget becomes available:** full text of the Argon model card (IPI numbers, CCL details), the double-blind eval mechanism, the agentic-privacy report's problem list, the 3.8 Flash CU benchmarks, Mariner/Jules status, and the exact dates of the Teamwork and Windows posts. (sources: [Argon model card](https://deepmind.google/models/model-cards/gemini-4-argon/); [double-blind evals](https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/); [agentic privacy](https://research.google/blog/open-and-emergent-problems-in-agentic-privacy-and-security-a-contextual-angle/); [3.8 Flash model card](https://deepmind.google/models/model-cards/gemini-3-8-flash/); [Jules](https://blog.google/innovation-and-ai/technology/developers-tools/jules-proactive-updates/); [Teamwork](https://blog.google/innovation-and-ai/technology/developers-tools/antigravity-teamwork-multi-agent/); [Windows/Spark](https://blog.google/innovation-and-ai/products/gemini-app/gemini-app-now-on-windows/))
