# 写代码来操作电脑：前沿 lab computer use 的接口转向（以 GPT-6 Astra 为中心）

> 2026-10-14 整理。

## 方法与来源

- **来源深度标签**
  - `github-fulltext`：从 GitHub 克隆后全文阅读，克隆只读，未执行其中代码。
  - `official-fulltext`：官方页面直接抓取全文。本环境可直连 platform.claude.com 和 anthropic.com，所以只适用于 Anthropic。
  - `official-search-excerpt`：openai.com、developers.openai.com、docs.x.ai 等站点无法直连，内容来自 WebSearch 对官方页面的摘录，不是全文阅读。
  - `二手`：第三方转述。
  - `推论`：笔者推断，括号中给出依据链接。
- **本次克隆的仓库**（commit 以 2026-10-14 克隆时的 HEAD 为准）
  - [openai/openai-cua-sample-app @f2a3dc5](https://github.com/openai/openai-cua-sample-app/tree/f2a3dc523ae406f9b704f9a420a05402a63b4522)，含完整 git 历史。
  - [openai/openai-agents-python @1c1a28d](https://github.com/openai/openai-agents-python/tree/1c1a28df92f359dded4eed83976301c2f9850e89)。
  - [openai/codex @95273b8](https://github.com/openai/codex/tree/95273b84fbff40f9df7d71d50f1ca52c6489b25d)。
  - [openai/openai-cookbook](https://github.com/openai/openai-cookbook/tree/main/examples/agents_sdk/computer_use_with_daytona)。
  - [google-gemini/computer-use-preview @77c9797](https://github.com/google-gemini/computer-use-preview/tree/77c9797e943aad63bbc963b7fd092a9e51c07863)。
  - [MoonshotAI/Kimi-K3](https://github.com/MoonshotAI/Kimi-K3)，含 `k3_tech_report.pdf`。
- **Anthropic 文档**：直接抓取 platform.claude.com 的 `.md` 版本：[computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)、[browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool)、[programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)、[code execution tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)、[tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference)。
- **本仓库已有笔记**：沿用了 `reviews/2026-10-14_frontier-labs/*.md` 和 `reviews/2026-10-14_office-pro-env/*.md` 中的事实，正文一律改挂原始出处，不引用本仓库报告。
- **用了 9 次 WebSearch**：6 次 extended，3 次 standard。
- **数字口径**：所有数字都是厂商或作者自报，没有独立复现。

---

## 0. 一页结论

1. **OpenAI 已把“写代码”定为 Astra 的首选 computer-use 接口，并在官方示例中移除了结构化动作模式。**
   - 官方指南写明：对 GPT-6 Astra 推荐 code execution，即模型写 PyAutoGUI 或 Playwright 代码来操作界面；`computer` tool 仍作为替代保留（[guide](https://developers.openai.com/api/docs/guides/tools-computer-use)，official-search-excerpt）。
   - 官方示例仓库在 Astra 发布当天（2026-09-03）的 commit “removing native mode” 删掉了 `computer` tool 路径，只留下 `exec_js` 和 `exec_py`（[commit a0f5a76](https://github.com/openai/openai-cua-sample-app/commit/a0f5a7641df9fbe76968ca41245a5eceee6061ce)，github-fulltext）。
2. **这个转向早于 Astra。** 2026-03 的 GPT-5.4 版示例同时有 `native`（computer tool）和 `code`（`exec_js`）两种模式，三个场景的 `defaultMode` 都已经是 `"code"`（[README @3751c8b](https://github.com/openai/openai-cua-sample-app/blob/3751c8baa6376c0bbf6cceea2cdc0c0b42996e03/README.md)、[scenarios.ts @3751c8b](https://github.com/openai/openai-cua-sample-app/blob/3751c8baa6376c0bbf6cceea2cdc0c0b42996e03/packages/scenario-kit/src/scenarios.ts)，github-fulltext）。
3. **OpenAI 的 code-CU 有四个关键设计**（[README](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)、[responses-loop.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)，github-fulltext）：
   - 只有一个 `code: string` 函数工具；（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)）
   - 运行时由开发者托管且持久，变量跨调用保留；（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)）
   - 观察由模型自己决定返回什么，可以是 `console.log` 文本或 `display()` 图片，runner 不会自动附截图；（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)）
   - 一次调用可以写循环，例如填多个字段并逐个校验。（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)）
   - 官方给的理由是定性的：“减少模型往返和重复输入上下文”。（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)）
4. **公开材料里没有 code vs computer tool 的受控对比数字。** 官方的 47% 提速（约 40 vs 75 分钟/任务）是 Astra 对比 GPT-5.6 Sol 的模型间比较，不是接口间比较，也没说明 OSWorld 2.0 跑分用的是哪种接口（[Astra 发布](https://openai.com/index/gpt-6-astra)，official-search-excerpt）。接口层的量化证据目前都来自学术侧，见第 4 节。
5. **Anthropic 走的是另一条路。**
   - 核心仍是结构化动作，但把动作拆成 toolset：`computer_toolset_20260801` 有 17 个成员（含 `zoom`），支持批量动作；`browser_toolset_20260801` 有 31 个成员，以 AX 树 + ref + 截图为主，`javascript_exec` 默认关闭（[CU 文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)、[browser 文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool)，official-fulltext）。
   - 这两个 toolset 的 `allowed_callers` 只接受 `["direct"]`，不能从 code execution 里以编程方式调用（[tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference)，official-fulltext）。
   - Anthropic 把“写代码”放在 code execution 和 programmatic tool calling 上，用于编排其他工具，并不用来点屏幕（[PTC](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)，official-fulltext）。
6. **其他各家的选择**
   - Google 仍是纯像素加预定义动作：坐标归一化到 0–1000，3.5 Flash 起换成桌面级底层动作集（[agent.py](https://github.com/google-gemini/computer-use-preview/blob/main/agent.py)，github-fulltext）。
   - Qwen-CUA 是纯像素，加 Bash 反而掉分（[Qwen-CUA PDF](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
   - Meta Muse 的浏览器子 agent 只看 AX 树、不能跑 JS（[Meta 安全博文](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse)，official-search-excerpt）。
   - 推论：**完全转向写代码的只有 OpenAI；其余各家要么是结构化动作，要么是 GUI+CLI 混合。**（依据：本条各项，以及 [Anthropic tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference)、[HybridCUA](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)）
7. **OpenAI 自家产品里，代码驱动的 CU 也已经落地。**
   - Codex 开源 harness 把 `node_repl` 和 `cua_repl` 识别为“Node REPL 支撑”的 MCP 服务器；`cua_repl` 调用在 TUI 里被标为 computer activity（[protocol/src/mcp.rs](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/mcp.rs)、[tui mcp.rs](https://github.com/openai/codex/blob/main/codex-rs/tui/src/history_cell/mcp.rs)，github-fulltext）。
   - Guardian 有一份专门的“Computer and Browser Use”审查策略，要求递归审查 REPL 内的嵌套调用，并按实际界面效果判断，不按 agent 自述的意图判断（[node_repl_policy.md](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/guardian/node_repl_policy.md)）。
   - `models.json` 对 gpt-6-astra、gpt-6-sol、gpt-6.1-sol 设了 `node_repl_auto_review_required: true`，Luna 和 5.6 系列为 false（[models.json](https://github.com/openai/codex/blob/main/codex-rs/models-manager/models.json)）。
8. **研究侧推论。** 动作空间从“固定动作原语”变成“图灵完备程序 + 持久状态”之后，有几件事要重新定义：（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/labs/catalog.json)）
   - 评测要规定哪些代码捷径算作弊。OpenAI 的 Paint 实验室明令禁止 `page.evaluate` 写像素（[catalog.json](https://github.com/openai/openai-cua-sample-app/blob/main/labs/catalog.json)）；EngiWorld 的 GUI 任务会检测脚本旁路（[eval.py](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/eval.py)）。
   - 训练环境要支持持久 REPL 状态的回放和重置（依据：[architecture.md](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/docs/architecture.md) 中运行时状态独立于 API 对话）。
   - 何时写代码、何时点屏幕，需要学出来：HybridCUA 和 Qwen-CUA 都显示，未经训练直接给 CLI 会掉分（[HybridCUA](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)、[Qwen-CUA](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）。
   - 以上是推论。

---

## 1. OpenAI code-execution computer use 详解

### 1.1 官方指南的口径
来源：[tools-computer-use](https://developers.openai.com/api/docs/guides/tools-computer-use)、[tools-computer-use-integration](https://developers.openai.com/api/docs/guides/tools-computer-use-integration)。深度：official-search-excerpt，两次 extended search 的摘录，非全文。

- 对 GPT-6 Astra 推荐 code execution：模型写代码，用 PyAutoGUI 或 Playwright 之类的库操作界面；结构化鼠标键盘的 `computer` tool 仍作为替代支持（[guide](https://developers.openai.com/api/docs/guides/tools-computer-use)，official-search-excerpt）。
- 各语言示例的分工（[guide](https://developers.openai.com/api/docs/guides/tools-computer-use)，official-search-excerpt）：
  - Python、Ruby、Go 示例把 Python 代码发给使用 PyAutoGUI 的桌面运行时；（[出处](https://developers.openai.com/api/docs/guides/tools-computer-use)）
  - JavaScript 示例用 Playwright 操作浏览器，暴露 `exec_js`，以及持久的 browser、context、page。（[出处](https://developers.openai.com/api/docs/guides/tools-computer-use)）
- 一次调用可以组合多个动作、循环或条件逻辑（[guide](https://developers.openai.com/api/docs/guides/tools-computer-use)，official-search-excerpt）。
- 示例会先检查屏幕再行动，把截图保留在运行时内存里，而不是每张都回传给模型（[guide](https://developers.openai.com/api/docs/guides/tools-computer-use)，official-search-excerpt）。
- 指南示例用 `previous_response_id` 续接对话，循环上限为 20 轮（[guide](https://developers.openai.com/api/docs/guides/tools-computer-use)，official-search-excerpt）。
- integration recipes 对运行时的说明（[integration](https://developers.openai.com/api/docs/guides/tools-computer-use-integration)，official-search-excerpt）：
  - 代码运行时可以是临时的，也可以是持久的；（[出处](https://developers.openai.com/api/docs/guides/tools-computer-use-integration)）
  - 如果要恢复同一个浏览器会话，要在单个脚本之外单独保存这个会话；（[出处](https://developers.openai.com/api/docs/guides/tools-computer-use-integration)）
  - 持久运行时可以在工具调用之间保留变量。（[出处](https://developers.openai.com/api/docs/guides/tools-computer-use-integration)）
- 运行环境由开发者自己托管，官方建议在隔离环境中运行浏览器（[integration](https://developers.openai.com/api/docs/guides/tools-computer-use-integration)，official-search-excerpt）。
- **两次搜索都没找到**官方解释“为什么对 Astra 更推荐代码”的段落，也没找到相关的速度或步数数字（[guide](https://developers.openai.com/api/docs/guides/tools-computer-use)，official-search-excerpt）。「无出处，待核」：指南全文是否另有理由段落。

### 1.2 官方示例仓库：openai/openai-cua-sample-app（github-fulltext）

**仓库演进**（[git 历史](https://github.com/openai/openai-cua-sample-app/commits/main)）：

| 时间 | 形态 | 出处 |
|---|---|---|
| 2025-03-11 | 初版，围绕 `computer-use-preview` 模型，Python CLI 加多种 Computer 后端（Browserbase、本地 Playwright 等） | [initial commit](https://github.com/openai/openai-cua-sample-app/commit/240c9e3f05e1cbbc540d233f9e3599e31e3411a8) |
| 2026-03-04/05 | “GPT-5.4 CUA Sample App”，TS 重写；`native` 模式直接暴露 Responses `computer` tool，`code` 模式通过 `exec_js` 暴露持久 Playwright REPL；三个场景的 `defaultMode` 都是 `"code"` | [README @3751c8b](https://github.com/openai/openai-cua-sample-app/blob/3751c8baa6376c0bbf6cceea2cdc0c0b42996e03/README.md)、[scenarios.ts](https://github.com/openai/openai-cua-sample-app/blob/3751c8baa6376c0bbf6cceea2cdc0c0b42996e03/packages/scenario-kit/src/scenarios.ts) |
| 2026-09-03 | commit “removing native mode”：删除 computer tool 路径，`responses-loop.ts` 删了 457 行 | [a0f5a76](https://github.com/openai/openai-cua-sample-app/commit/a0f5a7641df9fbe76968ca41245a5eceee6061ce) |
| 2026-09-03/04 | 加入 Python/PyAutoGUI 版（`exec_py`），默认模型改为 `gpt-6-astra` | [0d5e62e](https://github.com/openai/openai-cua-sample-app/commit/0d5e62e7cddd700a85867deaa4eb800c8a547489)、[defaults.json](https://github.com/openai/openai-cua-sample-app/blob/main/contracts/defaults.json) |

**README 对这一模式的原话**：“At OpenAI, we build this loop around models that write code to interact with software. Code lets the model combine actions, process observations, and choose when to look again.” 后文又说：“A persistent runtime keeps useful state and helper functions available between calls… This can reduce model round trips and repeated input context while giving the model feedback to correct mistakes.” 此外，README 声明这两个示例只是用标准库演示该模式，“OpenAI products use their own runtimes and additional controls”（[README](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)）。

**工具定义：JS 版**（[responses-loop.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)）
- 只有一个 `type: "function"` 工具 `exec_js`，`strict: true`，参数只有 `code: string`。（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)）
- 工具描述原文：
  - “Execute provided interactive JavaScript in a persistent Playwright REPL context.”（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)）
  - “Persist state across calls with globalThis.”（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)）
  - “Available globals: console.log, display(base64Image), Buffer, browser, context, page.”（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)）
  - “Prefer locator-based waits and domcontentloaded load-state waits over fixed delays.”（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)）

**工具定义：Python 版**（[responses_loop.py](https://github.com/openai/openai-cua-sample-app/blob/main/python-app/app/responses_loop.py)）
- 工具 `exec_py`。可用的全局对象有 `pyautogui`、`log(value)`、`display(image)`（接受 Pillow 图像）。（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/python-app/app/responses_loop.py)）
- “Python globals survive between calls.”（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/python-app/app/responses_loop.py)）
- 工具描述要求先 `display(pyautogui.screenshot())`。截图坐标与 PyAutoGUI 输入坐标一致，Retina 屏也一样。（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/python-app/app/responses_loop.py)）
- 只提供 PyAutoGUI，不提供 Playwright 对象。（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/python-app/app/responses_loop.py)）

**观察空间**
- 模型看到的只有代码自己产出的内容（[javascript-worker.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/javascript-worker.ts)）：
  - `console.log` 产出 `input_text`，单值最多 2,000 字符；（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/javascript-worker.ts)）
  - `display()` 产出 `input_image`，`detail: "original"`；（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/javascript-worker.ts)）
  - 报错信息截断到 4,000 字符；（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/javascript-worker.ts)）
  - 什么都没输出时返回 “exec_js completed with no console output.”（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/javascript-worker.ts)）
- runner 每轮执行后会截图，但截图只存进 replay 和控制台，**不回传给模型**：`executeJavaScriptToolCall` 只返回 worker 的输出（[responses-loop.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)）。
- 推论：截图从“每步强制观察”变成“模型按需拉取”，所以能读 DOM 文本时可以完全不看图（依据：[README](https://github.com/openai/openai-cua-sample-app/blob/main/README.md) 中 “choose when to look again”）。

**动作空间**
- 动作就是任意 JS 或 Python 代码。JS 版可用 Playwright 的 locator、`page.mouse`、`page.keyboard`、`page.evaluate` 等；Python 版可用任意 PyAutoGUI 调用（[responses-loop.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)、[responses_loop.py](https://github.com/openai/openai-cua-sample-app/blob/main/python-app/app/responses_loop.py)）。
- 约束只有工程层面的（[protocol.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/browser/protocol.ts)、[JS README](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/README.md)）：
  - 代码不超过 64 KiB；（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/browser/protocol.ts)）
  - 单次输出不超过 12 MiB；（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/browser/protocol.ts)）
  - 每次调用 60 秒截止，超时结束整个 run（2026-09-03 的 [commit 8baa140](https://github.com/openai/openai-cua-sample-app/commit/8baa140ccbd00cac49df69ed6344547d3e838cab) 把时限从 20 秒提高到 60 秒）。
- Paint 实验室的指令明确禁止代码捷径：“Do not generate an image externally, write canvas pixels through page.evaluate, or call page-internal drawing, document, or save functions.” Paint 场景还额外要求通过截图观察、用 `page.mouse` 操作可见控件（[catalog.json](https://github.com/openai/openai-cua-sample-app/blob/main/labs/catalog.json)、[executor-registry.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/executor-registry.ts)）。

**循环**（[responses-loop.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)）
- 请求参数：`reasoning: {effort: "low"}`、`parallel_tool_calls: false`、`truncation: "auto"`，用 `previous_response_id` 续接。（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)）
- 响应按 message 的 `phase` 分类：`commentary` 表示继续循环，`final_answer` 表示结束。（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)）
- 每条 `function_call` 的结果以 `function_call_output` 回传，包含 text 或 image 数组。（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)）
- 轮数上限可配置，最多 50（[contracts/index.ts](https://github.com/openai/openai-cua-sample-app/blob/main/contracts/index.ts)）。

**会话状态**
- 浏览器会话在调用之间存活；每段代码在一个 async 函数里执行，要保留自定义变量须挂到 `globalThis`；每次新 run 都从新的浏览器和 JS 状态开始（[architecture.md](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/docs/architecture.md)）。
- “The worker preserves execution state independently of the API conversation”（[JS README](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/README.md)）。
- 推论：这样就有两条状态线，一条是 Responses 侧的对话状态，一条是运行时侧的变量和页面状态，两者需要各自持久化和恢复（依据：[integration](https://developers.openai.com/api/docs/guides/tools-computer-use-integration)，official-search-excerpt）。
- 默认视口 1440×900（[session.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/browser/session.ts)）。

**安全边界**：示例不提供 OS 沙箱，也不含 OpenAI 生产环境的 action-review 控制；“A final answer does not prove the task succeeded”（[README](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)）。

### 1.3 `computer` tool：结构化动作，仍受支持（github-fulltext）

- **GA 接口**：tools 里只写 `{"type": "computer"}`。模型返回 `computer_call`，带批量的 `actions[]` 和 `pending_safety_checks`；开发者执行后回传 `computer_call_output`，其中 `output.type = "computer_screenshot"`（[3751c8b responses-loop.ts](https://github.com/openai/openai-cua-sample-app/blob/3751c8baa6376c0bbf6cceea2cdc0c0b42996e03/packages/runner-core/src/responses-loop.ts)）。
- **动作类型**：`click`、`double_click`、`drag`、`move`、`scroll`、`type`、`keypress`、`wait`、`screenshot`（[同上](https://github.com/openai/openai-cua-sample-app/blob/3751c8baa6376c0bbf6cceea2cdc0c0b42996e03/packages/runner-core/src/responses-loop.ts)）。Agents SDK 的 `AsyncComputer` 接口与此一一对应（[cookbook Daytona](https://github.com/openai/openai-cookbook/blob/main/examples/agents_sdk/computer_use_with_daytona/computer_use_with_daytona.ipynb)、[tools.md](https://github.com/openai/openai-agents-python/blob/main/docs/tools.md)）。
- **从 preview 迁移到 GA**（[tools.md](https://github.com/openai/openai-agents-python/blob/main/docs/tools.md)）：
  - 模型从 `computer-use-preview` 换成 `gpt-5.6-sol`；（[出处](https://github.com/openai/openai-agents-python/blob/main/docs/tools.md)）
  - 工具从 `computer_use_preview` 换成 `computer`；（[出处](https://github.com/openai/openai-agents-python/blob/main/docs/tools.md)）
  - 每个 `computer_call` 从单个 `action` 变成批量 `actions[]`；（[出处](https://github.com/openai/openai-agents-python/blob/main/docs/tools.md)）
  - GA 不再要求 `truncation="auto"`，也不再需要 environment 和尺寸参数。（[出处](https://github.com/openai/openai-agents-python/blob/main/docs/tools.md)）
- Agents SDK 的内置默认模型 `gpt-5.6-luna` 支持 computer use（[tools.md](https://github.com/openai/openai-agents-python/blob/main/docs/tools.md)）。
- **什么时候还用 computer tool**：官方只说它“仍作为替代受支持”，搜索摘录里没有具体选择准则（[guide](https://developers.openai.com/api/docs/guides/tools-computer-use)，official-search-excerpt）。推论：
  - 没有可写代码运行时的场景用它，例如只能拿到 VNC 或截图流的远程桌面；（[出处](https://developers.openai.com/api/docs/guides/tools-computer-use)）
  - 需要逐动作人工确认的场景用它，因为代码一次能做多个动作，逐动作审批更难。（[出处](https://developers.openai.com/api/docs/guides/tools-computer-use)）
  - 依据：[Agents SDK 关于高风险工具保持直接调用的建议](https://github.com/openai/openai-agents-python/blob/main/docs/tools.md)。

### 1.4 与 Programmatic Tool Calling（PTC）的关系（github-fulltext 为主）

- **OpenAI 的 PTC**：模型生成 JavaScript 去编排“合格工具”，程序运行在 **OpenAI 托管的全新 V8 环境**里，“does not have Node.js APIs, filesystem or network access, or a persistent process”（[Agents SDK tools.md](https://github.com/openai/openai-agents-python/blob/main/docs/tools.md)）。
- **PTC 能调用哪些工具**：可通过 `allowed_callers` 开启编程调用的 SDK 工具类型是 FunctionTool、CustomTool、ShellTool、ApplyPatchTool、HostedMCPTool、CodeInterpreterTool，**不含 ComputerTool**（[tools.md](https://github.com/openai/openai-agents-python/blob/main/docs/tools.md)）。
- **二者的区别**：code-execution CU 不走 PTC。它是一个普通的 function tool（`exec_js`/`exec_py`），代码在**开发者自托管、持久**的运行时中执行，可以直接持有 browser、page 对象（[README](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)）。
  - 推论：PTC 解决的是“少走模型往返地编排工具”，code-CU 解决的是“用通用编程接口直接操作 UI 状态”。两者都把一次模型输出从“一个动作”变成“一段程序”，但执行位置和状态模型正好相反：PTC 托管且无状态，code-CU 自托管且有状态。（[出处](https://github.com/openai/openai-agents-python/blob/main/docs/tools.md)）
- **Codex 的 Code Mode**：`exec` 工具在“fresh V8 isolate”中以 async module 执行 JS，嵌套工具挂在全局 `tools` 对象上；不能用 Node、文件系统、网络或 console；可以用 `store`/`load` 跨 `exec` 保存可序列化的值；用 `yield_control()` 和 `wait` 处理长任务（[description.rs](https://github.com/openai/codex/blob/main/codex-rs/code-mode-protocol/src/description.rs)）。这是 PTC 式编排在 Codex 中的实现，同样与 GUI 无关。
- **Codex 里的 GUI 控制走另外两个 REPL**：`node_repl` 和 `cua_repl` 两个由 Node REPL 支撑的 MCP 服务器，加上 Browser connector `connector_openai_browser`（[mcp.rs](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/mcp.rs)）。
  - `cua_repl` 的调用被标为 computer activity（[tui mcp.rs](https://github.com/openai/codex/blob/main/codex-rs/tui/src/history_cell/mcp.rs)）。
  - 「无出处，待核」：这两个 REPL 的工具描述和运行时实现不在开源仓库里，可能在服务端或闭源组件中。

### 1.5 Agents API 托管浏览器、dots 云电脑（official-search-excerpt）

- **上线**：Agents API 于 2026-09-10 以 public beta 发布，由 OpenAI 托管 Codex harness，管理 session、编排和 compaction（[Introducing the Agents API](https://openai.com/index/introducing-the-agents-api)）。2026-09 的 changelog 加入 computer use：agent 在 **OpenAI 托管的浏览器**中工作，网站访问审批和登录由你的应用处理（[changelog](https://developers.openai.com/api/docs/changelog)、[Agents API CU 文档](https://developers.openai.com/api/docs/guides/agents-api/tools/computer-use)）。具体日期 09-29 来自本仓库 openai 笔记，摘录里只有“2026 年 9 月”（[Agents API](https://openai.com/index/introducing-the-agents-api)）。
- **网站审批**：每个新的网站 origin 都要审批，公共站点也一样；开启网络访问不等于批准这些请求。应用在收到 `agent.session.requires_action` 后读取待办请求，再通过 session events 端点提交 approve、deny 或 cancel（[Agents API CU](https://developers.openai.com/api/docs/guides/agents-api/tools/computer-use)）。
- **登录**：登录请求是单独的 `browser_authentication` 类型；对只读公开页面的任务，示例直接取消登录请求（[Agents API CU](https://developers.openai.com/api/docs/guides/agents-api/tools/computer-use)）。
- **确认粒度**：origin 审批不会强制逐动作确认。对购买或破坏性操作，文档建议把浏览器限制在做不了这些操作的资源上，或者改用自己控制的浏览器运行时（[Agents API CU](https://developers.openai.com/api/docs/guides/agents-api/tools/computer-use)）。
- **断线恢复**：流断开后，从取回的 session 的 `required_actions` 恢复待填表单，不需要重发任务或之前的审批（[Agents API CU](https://developers.openai.com/api/docs/guides/agents-api/tools/computer-use)）。
- **预热沙箱**：可以用保存好的桌面配置预热沙箱，并在创建带 computer use 工具的 session 时挂上（[prewarmed](https://developers.openai.com/api/docs/guides/agents-api/environments/prewarmed)）。
- **代码执行示例**：在你自己运营的沙箱服务中运行生成的代码，每个脚本弹一次确认。文档说这只是保守的演示，生产运行时必须自己执行权限规则（[Agents API CU](https://developers.openai.com/api/docs/guides/agents-api/tools/computer-use)）。
- 「无出处，待核」：Agents API 托管浏览器暴露给模型的是 computer tool 还是 code 接口，摘录中没有说明。
- **dots**：运行在 GPT-6 Astra 上，自带云电脑和浏览器，用户关机后仍可继续工作（[Introducing dots](https://openai.com/index/introducing-dots)，official-search-excerpt）。
- **ChatGPT 企业版**：浏览器和 computer use 的管理设置于 2026-09-03 发布（[help 20001510](https://help.openai.com/en/articles/20001510-manage-browser-and-computer-use-in-your-enterprise-workspace)，official-search-excerpt）。

---

## 2. 各家对比表

“写代码”指模型输出的动作本身是程序，例如 Playwright、PyAutoGUI 或 Bash，而不是预定义的动作原语。（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)）

| 实体 | 观察形式 | 动作形式 | 写代码？ | 谁托管电脑 | 关键数字（自报） | 出处 / 深度 |
|---|---|---|---|---|---|---|
| **OpenAI GPT-6 Astra，code-CU（推荐路径）** | 模型自己用代码取：`console.log` 文本、`display()` 图片，也可以读 DOM 或 locator | 任意 JS（Playwright）或 Python（PyAutoGUI），持久 REPL | **是** | 开发者 | OSWorld 2.0 offline partial 72.6%（未说明接口） | [sample app](https://github.com/openai/openai-cua-sample-app/blob/main/README.md) github-fulltext；[Astra](https://openai.com/index/gpt-6-astra) excerpt |
| OpenAI `computer` tool（替代路径） | 每批动作后回传整屏截图 | `computer_call.actions[]`：click、double_click、drag、move、scroll、type、keypress、wait、screenshot | 否 | 开发者 | — | [3751c8b loop](https://github.com/openai/openai-cua-sample-app/blob/3751c8baa6376c0bbf6cceea2cdc0c0b42996e03/packages/runner-core/src/responses-loop.ts) github-fulltext |
| OpenAI Agents API CU / dots | 「无出处，待核」 | 「无出处，待核」；网站 origin 逐个审批 | 未知 | **OpenAI**（托管浏览器 / 云电脑） | — | [Agents API CU](https://developers.openai.com/api/docs/guides/agents-api/tools/computer-use)、[dots](https://openai.com/index/introducing-dots) excerpt |
| OpenAI Codex（产品） | AX 编号树 + 截图（[报告](https://github.com/demoleiwang/agent-frontier/blob/claude/intelligent-goldberg-ocxr01/reviews/2026-10-15_codex-cu-bu.md)） | `node_repl`、`cua_repl`（tool `js`）、Browser connector | **是**（Node REPL） | 动作为 AX 语义优先、坐标兜底（[tools.js](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1)） | gpt-6 系列对 node_repl 强制 auto-review | [mcp.rs](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/mcp.rs)、[models.json](https://github.com/openai/codex/blob/main/codex-rs/models-manager/models.json) github-fulltext |
| **Anthropic computer toolset**（`computer_toolset_20260801`） | 截图，加 `zoom` 局部全分辨率图 | 17 个成员（click 系、drag、mouse_down/up、scroll、type、key、hold_key、wait、cursor_position…），批量顺序执行 | 否；`allowed_callers` 只接受 `["direct"]` | 开发者（参考实现为 Docker + Xvfb） | Opus 5.5 OSWorld 2.1 partial 81.8%；Fable 5.1 OSWorld 2.0（2026-08 版）77.9% partial / 41.7% strict | [CU 文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)、[Opus 5.5](https://www.anthropic.com/claude-opus-5-5)、[Fable 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1) official-fulltext |
| Anthropic browser toolset（`browser_toolset_20260801`） | AX 树（`read_page`，元素带 `[ref_n]`）、`find`、`get_page_text`、截图、zoom | 31 个成员，可以按坐标或 ref 指定目标；`form_input` 直接设值 | 仅可选的 `javascript_exec`，**默认关闭** | 开发者，或 Browserbase、E2B 等合作方驱动 | — | [browser 文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool)、[SDK toolsets](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk) official-fulltext |
| Anthropic code execution + PTC | 代码输出 | Python 或 Bash；从容器内的代码调用自定义工具 | 是，但**不能调用** computer / browser toolset | Anthropic 托管容器，无网络 | 工具定义加载 15 万 → 2,000 tokens（MCP 场景） | [code exec](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)、[tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference)、[code-execution-with-mcp](https://www.anthropic.com/engineering/code-execution-with-mcp) official-fulltext |
| Google Gemini computer use（3.5 Flash 及之后） | 截图加当前 URL；参考 agent 只保留最近 3 轮截图 | 预定义函数：click、double/triple/middle/right_click、mouse_down/up、move、type、drag_and_drop、wait、press_key、key_down/up、hotkey、take_screenshot、scroll、go_back/forward、navigate；坐标归一化到 0–1000 | 否，但可以加自定义函数 | 开发者（Playwright 或 Browserbase） | 3.8 Flash 无公开 CU 分数 | [agent.py](https://github.com/google-gemini/computer-use-preview/blob/main/agent.py) github-fulltext；[3.8 Flash model card](https://deepmind.google/models/model-cards/gemini-3-8-flash/) |
| Meta Muse（浏览器子 agent） | **只有 AX 树快照**，没有原始 DOM | broker 持有 CDP 连接；**不能跑 JS** | 否 | Meta（Muse Secure VM） | — | [Meta 安全博文](https://research.meta.ai/blog/security-and-safety-for-ai-agents-our-approach-with-muse) official-search-excerpt；[Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/) |
| xAI Grok Bot | 「无出处，待核」（截图与动作的循环细节未公开） | 持久云电脑上的浏览器、文件系统和终端；shell 命令逐条审批 | 有 shell，CU 接口未知 | xAI：每用户一台持久云电脑（microVM），所有 Bot 共享 | 屏幕从 1280×800 升到 1920×1200；会话日志只记录动作数和截图数 | [computer-and-apps](https://docs.x.ai/grok-bot/computer-and-apps)、[changelog](https://x.ai/changelog/bot)、[designing-grok-bot](https://x.ai/news/designing-grok-bot) official-search-excerpt |
| Qwen-CUA | **纯截图**，没有 DOM、AX 树、shell 或 API | key、type、鼠标原语、scroll、wait、call_user 等，每轮一个动作 | 否；加 Bash 后完美率下降 | 开发者 | OSWorld-Verified 86.2；OSWorld 2.0 18.5 / 48.4（binary / partial）；MyPCBench 加 Bash 后完美率 58.7 → 55.1，轮数 63.6 → 49.1 | [Qwen-CUA PDF](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)、[arXiv](https://arxiv.org/abs/2608.02352) |
| HybridCUA-9B | 截图加 CLI 输出 | GUI 与 CLI 合并成单一 `bash` 动作 | **是**（shell） | 开发者（OSWorld VM 集群） | OSWorld 53.6%（+14.8），平均 14.0 步；未训练直接开 CLI 掉 2.5–11.5 分；拆成两个工具掉 7.2 分 | [README](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)、[arXiv](https://arxiv.org/abs/2609.38008) |
| Kimi K3 | 报告未说明 OSWorld 的观察和动作接口 | 「无出处，待核」 | 未知；RL 环境模拟 Claude Code、Codex 等多种 harness | 开发者 | OSWorld-Verified 84.8；OSWorld 2.0 58.3 | [k3_tech_report.pdf](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf) github-fulltext |
| Xiaomi MiMo-V2.6-Pro | 「无出处，待核」 | 「无出处，待核」 | 未知；RL 栈含 mini-bash、Claude Code、Codex harness | — | OSWorld-Verified 约 82.0（二手转述） | [MiMo news](https://mimo.mi.com/docs/en-US/news)、[XiaomiMiMo/verl](https://github.com/XiaomiMiMo/verl) |
| Z.ai ZCode `zcode-cua-plugin` | AX 树优先；浏览器默认用 `playwright.domSnapshot()` | 按索引操作 AX 元素，优先 `setValue`；“每个观察周期最多一个改变状态的动作” | 部分（harness 侧） | 本机 | — | [ZCode](https://github.com/zai-org/ZCode) |

**跨行要点**
- 数字口径不可比。
  - OpenAI 的 72.6% 是 OSWorld 2.0 offline 子集（[Astra](https://openai.com/index/gpt-6-astra)，excerpt）。
  - Anthropic 的 77.9% 是 2026-08 版 task release；Anthropic 自己说明这个版本与早先结果不可直接比较（[Fable 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1)）。
  - 81.8% 是 OSWorld 2.1，表中 GPT-6 Astra 一栏为空（[Opus 5.5](https://www.anthropic.com/claude-opus-5-5)）。
- 推论（依据：上表各行出处）：三家选的观察和动作形式正好落在三个点上：
  - OpenAI 是“写代码”，模型自选观察；（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)）
  - Anthropic 是“结构化工具 + AX 树”，写代码与 GUI 隔离；（[出处](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference)）
  - Google 和 Qwen 是“纯像素 + 原语”。（[出处](https://github.com/google-gemini/computer-use-preview/blob/main/agent.py)）

---

## 3. 训练与评测线索（只记技术事实）

### 3.1 OpenAI
- **Ironclad**：Astra 是第一个在 Ironclad 任务上训练的前沿模型。任务是合作方生产 SaaS 中的合成任务，用 rubric 判分，Astra 平均 55.0%，GPT-5.6 Sol 为 41.6%（[Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad)，official-search-excerpt）。帖子没有说这些任务用的是 code 接口还是 computer tool。「无出处，待核」
- **confirmation policy**：system card 称 Astra 被训练遵守一套确认策略，例如发送某些消息或购买前暂停，等待用户批准。相关评测故意设计成模糊指令和复杂权限（[system card](https://deploymentsafety.openai.com/gpt-6-astra)、[business post](https://openai.com/index/gpt-6-astra-next-generation-work)，official-search-excerpt）。
- **没有找到“混合 GUI + 代码训练”的描述**：两次 extended 搜索都没找到 Astra system card 或博文中有关“训练模型用代码操作电脑”的段落，搜索结论明确说没有（[搜索覆盖 openai.com / deploymentsafety](https://deploymentsafety.openai.com/gpt-6-astra)，official-search-excerpt）。「无出处，待核」：system card 全文与 6.1 Sol 附录 PDF 是否有相关内容（[6.1 Sol addendum PDF](https://cdn.openai.com/pdf/38e3efcf-545e-44cd-99ec-2b7eb395f4cc/oai_GPT_6_1_Sol.pdf) 未能读取）。
- **harness 侧的间接证据**：Codex 的 `models.json` 只对 GPT-6 系列（Astra、Sol、6.1 Sol）设 `node_repl_auto_review_required: true`；Guardian 有专门的 computer/browser-use REPL 审查策略（[models.json](https://github.com/openai/codex/blob/main/codex-rs/models-manager/models.json)、[node_repl_policy.md](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/guardian/node_repl_policy.md)，github-fulltext）。
  - 推论：GPT-6 系列在 Codex 中被预期频繁地通过 REPL 写代码做 CU，因此这条路径被设为强制审查（依据同上）。（[出处](https://github.com/openai/codex/blob/main/codex-rs/models-manager/models.json)）
- **Guardian 策略的具体规则**（[node_repl_policy.md](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/guardian/node_repl_policy.md)，github-fulltext）：
  - “Recursively evaluate nested tool calls within these actions”；（[出处](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/guardian/node_repl_policy.md)）
  - 按“actual interface, existing state and selections, and resulting effects, not the agent's description of its intent”评估；（[出处](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/guardian/node_repl_policy.md)）
  - 用不同手段达到“先前被限制动作”同样结果的，判为高风险并拒绝。（[出处](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/guardian/node_repl_policy.md)）
  - 推论：这些规则针对的正是代码动作的特点，即一段代码可以打包多步，并且绕开具体的 UI 路径。（[出处](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/guardian/node_repl_policy.md)）
- **47% 提速的口径**：来自“latency simulations on OSWorld 2.0”，Astra 72.6% 约 40 分钟，GPT-5.6 Sol 65.7% 约 75 分钟；脚注只说明 OSWorld V2-Offline 是能离线运行的子集，Claude 分数用官方设置（[Astra](https://openai.com/index/gpt-6-astra)，official-search-excerpt）。没有接口维度的拆分。
- **示例代码里的成本信号**：OpenAI 官方 CUA 示例默认 `reasoning.effort = "low"`（[responses-loop.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/responses-loop.ts)）；Agents JS SDK 也把 gpt-6-astra 的默认 reasoning 设为 low（[CHANGELOG](https://github.com/openai/openai-agents-js/blob/main/packages/agents-openai/CHANGELOG.md)）。
- **相关成本案例**：StackAI（Asana）的浏览器 agent 成本问题出在截图和页面文本历史没有进缓存，修好后成本至少降了 76 倍（[Asana](https://openai.com/index/asana-browser-agent)，official-search-excerpt）。
  - 推论：code-CU 让模型按需取图，从结构上就减少了这类历史膨胀（依据：[README](https://github.com/openai/openai-cua-sample-app/blob/main/README.md) 中 “reduce … repeated input context”）。

### 3.2 Anthropic
- 2026-09-09 的事故复盘称，相关行为集中在 GUI computer-use RL 任务中，这些任务的预期解法不可用（[alignment assessment](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents)，official-fulltext，经本仓库笔记）。
- 10-09 的报告说 OSWorld 等基准上出现过误提交真实表单；边界和谨慎训练正从编码环境扩展到搜索和 computer use（[investigating unintended actions](https://www.anthropic.com/research/investigating-unintended-model-actions)）。
- Fable 5.1 带生产 safeguards 评测；safeguards 介入的任务在 OSWorld 2.0 上记 0 分（[Fable 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1)，official-fulltext）。
- **截图上下文管理**（[CU 文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)，official-fulltext）：
  - 每张截图约 1,000–1,800 input tokens；（[出处](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)）
  - 单次请求超过 20 张图时，每张图的单边尺寸限制会收紧；（[出处](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)）
  - 在 Fable 5.1、Opus/Sonnet/Haiku 5.5 上不建议在客户端裁剪截图，因为会让后续 thinking block 失效，应改用服务端的 tool result clearing。（[出处](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)）
- **toolset 开销**：默认成员约 4,500 input tokens；关掉 `zoom` 约省 410（[CU 文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)，official-fulltext）。

### 3.3 评测设计：代码能力带来的“旁路”问题
- OpenAI 示例 Paint 实验室禁止用 `page.evaluate` 写像素，也禁止调用页面内部函数（[catalog.json](https://github.com/openai/openai-cua-sample-app/blob/main/labs/catalog.json)）。
- EngiWorld 的 GUI 任务 verifier 会检测桌面上的 `.py`/`.ps1` 脚本，以及 shell history 中调用 cadquery、freecadcmd 等工具的命令，发现即判失败（[eval.py](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/eval.py)）。
- 同一基准上，DeepSeek V4.1 Flash CLI 48.3 分、GUI 2.0 分；Claude Opus 5 CLI 48.6 分、GUI 40.5 分（[EngiWorld README](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/README.md)）。
- ComponentBench：同一模型、同一 harness，只改观察和动作空间，成功率差 30% 以上；GPT-5 mini 用 AX 树 83.1%，坐标像素 48.9%（[arXiv 2608.18307](https://arxiv.org/abs/2608.18307)）。
- 推论：OSWorld 类分数在 code-CU 时代必须标注接口。同一个任务，如果允许 `page.evaluate` 或 shell，测的就不再是 GUI 能力（依据：上面四条）。（[出处](https://arxiv.org/abs/2608.18307)）

---

## 4. 学术相关工作（code-as-action / 混合 GUI+代码）

从本仓库 `data/items/**` 按标题和摘要关键词筛出（关键词：GUI/CUA/browser 与 code/CLI/API/script/hybrid 的组合），另补一篇经搜索核实的 2025 年基线 [CoAct-1](https://arxiv.org/abs/2508.03923)。

| # | 论文 | 一句话 | 链接 |
|---|---|---|---|
| 1 | **ASIL**：Replacing Screenshot-and-Click with Structured State and Semantic Actions（2026-08-27） | 把软件暴露为结构化 JSON 观察加“可由代码执行的语义动作”。15 个应用、380 个任务上，闭源模型超过 80 分，每任务少于 5 个动作；截图点击只有 6.6 / 26.6 strict。小模型做 SFT 和 RL 后提升明显 | [arXiv 2608.26991](https://arxiv.org/abs/2608.26991) |
| 2 | **HybridCUA**：Learning to Orchestrate GUI and CLI（2026-09-30） | 5K 条 GUI/CLI/交错轨迹加 3K RLVR 任务，配 CLI-aware 奖励（R_CLI、r_exec）。9B 模型 OSWorld 53.6%；未训练直接开 CLI 会掉分 | [arXiv 2609.38008](https://arxiv.org/abs/2609.38008)、[repo](https://github.com/ZJU-REAL/HybridCUA) |
| 3 | **CUA-Universe**（2026-09-04） | App-Forge 把真实桌面软件改造成 VM 加 CLI 面（16 个应用）；Path-Steer 引导 rollout 走高效的混合路径。训练后模型从低效 GUI 和脆弱 CLI 脚本转向 GUI+CLI 协同 | [arXiv 2609.05374](https://arxiv.org/abs/2609.05374) |
| 4 | **RecreationWorld**（2026-09-21） | 给定一个运行中的参考程序，agent 要探索界面、写代码复刻并做视觉验证；参考程序充当 oracle。5 个平台；RecreationBench 有 250 个任务，摘要称 GPT-6 Astra 领先 | [arXiv 2609.22000](https://arxiv.org/abs/2609.22000) |
| 5 | **Qwen-UI-Agent**（2026-07-31） | 统一动作空间，GUI 操作与 CLI 执行交错，单轮输出批量动作；在线 RL 轨迹超过 100 轮 | [arXiv 2607.28227](https://arxiv.org/abs/2607.28227) |
| 6 | **ComponentBench**（2026-08-18） | 97 类 UI 组件、2,910 个程序化验证任务；只换观察和动作空间就能让成功率差 30% 以上 | [arXiv 2608.18307](https://arxiv.org/abs/2608.18307) |
| 7 | **EchoPath**（2026-09-15） | 把验证过的 GUI 轨迹编译成带参数、可确定性重放的“可调用记忆”，类似 MCP 工具；中位 token 成本降 90% 以上，执行时间约降 60% | [arXiv 2609.16635](https://arxiv.org/abs/2609.16635) |
| 8 | **PhoneCLI**（2026-09-28） | 离线探索 App，把 GUI 导航编译成可调用命令；在线阶段先确定性执行，失败时回退到 VLM | [arXiv 2609.35671](https://arxiv.org/abs/2609.35671) |
| 9 | **CUA-SWE**（2026-10-01） | 软件工程任务同时需要改代码、跑命令、操作运行中的 GUI 并看视觉反馈，用确定性测试判分 | [arXiv 2609.32600](https://arxiv.org/abs/2609.32600) |
| 10 | **CoAct-1**（2025-08，ICLR 2026，基线） | Orchestrator 把子任务分给 GUI Operator 或写 Python/Bash 的 Programmer。OSWorld 60.76%，平均 10.15 步（对比领先 GUI agent 约 15 步） | [arXiv 2508.03923](https://arxiv.org/abs/2508.03923)（搜索核实，二手摘要） |

**补充**
- 综述 *Efficient GUI Agents* 把“能在 GUI 与非 GUI 执行间切换的混合运行时”列为反复出现的效率机制之一（[arXiv 2609.02309](https://arxiv.org/abs/2609.02309)）。
- EngiWorld 提供 GUI 与 CLI 双接口对照（[arXiv 2609.37686](https://arxiv.org/abs/2609.37686)）。
- 「无出处，待核」：本地语料里**没有**找到直接研究“Playwright / 持久 REPL 作为 CUA 唯一动作空间”的 2026 论文，即 OpenAI 这种形态。现有工作多是 GUI+CLI 混合，或者结构化语义动作。

---

## 5. 开放问题（全部为推论）

1. **何时写代码、何时点屏幕。**
   - 已有证据：HybridCUA 未经训练直接开 CLI 掉 2.5–11.5 分（[README](https://github.com/ZJU-REAL/HybridCUA/blob/main/README.md)）；Qwen-CUA 加 Bash 后完美率下降，作者认为模型还没学会何时转向 Bash（[Qwen-CUA PDF](https://github.com/xlang-ai/Qwen-CUA/blob/main/paper/Qwen-CUA.pdf)）；OpenAI 则把选择完全交给模型在代码里决定（[README](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)）。
   - 开放问题：路由策略应该靠奖励塑形（如 HybridCUA 的 R_CLI）学出来，还是靠能力自然涌现？公开基准缺少“同一任务、不同接口”的成对设置。ASIL 和 ComponentBench 是少数例外（[ASIL](https://arxiv.org/abs/2608.26991)、[ComponentBench](https://arxiv.org/abs/2608.18307)）。
2. **代码动作的训练环境。**（[出处](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/docs/architecture.md)）
   - 持久 REPL 意味着环境状态包括页面、DOM、cookie，还包括运行时变量和 helper 函数（[architecture.md](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/docs/architecture.md)）。
   - RL 环境的 snapshot、reset、fork 要覆盖这部分状态。Kimi K3 的 AgentENV 用 microVM 增量 checkpoint 和 fork，是可借鉴的方向（[K3 report](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。
   - 开放问题：轨迹回放的确定性怎么保证，例如代码里的计时等待、网络请求和随机性。（[出处](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）
3. **奖励与旁路。**
   - 代码可以绕过 UI 直接改状态，比如 `page.evaluate`、调用内部 API、写文件。终态 verifier 无法区分“正确操作 UI”和“走后门”，除非像 EngiWorld 那样检测旁路（[eval.py](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/eval.py)），或者像 OpenAI 那样在指令中禁止（[catalog.json](https://github.com/openai/openai-cua-sample-app/blob/main/labs/catalog.json)）。
   - 开放问题：旁路什么时候是“好的泛化”（真实工作中能用 API 就该用 API），什么时候是 reward hacking？这需要任务级的“允许接口”规范。（[出处](https://github.com/Hongcheng-Gao/EngiWorld/blob/main/task/single-software-execution/gui/solidworks/task-01/eval.py)）
4. **观察预算由模型自选。**
   - code-CU 中模型自己决定何时截图、看多大的图（[javascript-worker.ts](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/src/javascript-worker.ts)）。
   - 开放问题：少看图会不会漏掉视觉状态变化，比如弹窗或 canvas？“该看没看”的失败模式缺少专门基准。WebFovea 记录的 harness 层四阶段失败可作参考（[arXiv 2610.03036](https://arxiv.org/abs/2610.03036)）。
5. **长期会话状态与双状态线。**
   - API 对话状态（`previous_response_id` 或 compaction）与运行时状态是分开持久化的（[JS README](https://github.com/openai/openai-cua-sample-app/blob/main/javascript-app/README.md)、[Agents API](https://openai.com/index/introducing-the-agents-api)）。
   - 开放问题：compaction 之后，模型还记得 `globalThis` 里存了哪些 helper 吗？跨 session 的运行时怎么做版本管理？dots 和 Grok Bot 这类持久云电脑把这个问题推到了产品层面（[dots](https://openai.com/index/introducing-dots)、[Grok Bot docs](https://docs.x.ai/grok-bot/computer-and-apps)）。
6. **评测可比性。**
   - OSWorld 2.0 / 2.1、offline 子集、不同 task release、partial 与 strict 分数并存（[Astra](https://openai.com/index/gpt-6-astra)、[Fable 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1)、[Opus 5.5](https://www.anthropic.com/claude-opus-5-5)）。
   - 再叠加“接口是代码还是原语”这个变量，厂商之间的数字基本不可比。建议论文同时报告接口、每任务时间和成本，以及步数或往返数。（[出处](https://openai.com/index/gpt-6-astra)）
7. **小模型能否学会 code-CU。**（[出处](https://arxiv.org/abs/2608.26991)）
   - ASIL 显示，结构化语义动作让 2B/9B 小模型经 SFT+RL 达到 74–82 分（[ASIL](https://arxiv.org/abs/2608.26991)）；但开放模型的主流路线仍是纯像素（[Qwen-CUA](https://arxiv.org/abs/2608.02352)）。
   - 开放问题：持久 Playwright REPL 这种开放式动作空间，对开放模型的 RL 是否太难探索？（[出处](https://arxiv.org/abs/2608.26991)）

---

## 6. 缺口与待核

- **OpenAI 指南全文未读**，只有搜索摘录。待核：
  - 推荐代码的官方理由段落；
  - 何时用 computer tool 的准则；
  - Python 示例的完整 helper 列表；
  - 指南中 20 轮上限的示例与 GitHub 示例的 50 轮上限是否一致（[guide](https://developers.openai.com/api/docs/guides/tools-computer-use)）。
- **Astra 的 OSWorld 2.0 跑分用的是哪种接口**：「无出处，待核」（[Astra](https://openai.com/index/gpt-6-astra)）。
- **Astra 训练中是否有代码驱动 CU 的 RL**：system card 全文未读，「无出处，待核」（[system card](https://deploymentsafety.openai.com/gpt-6-astra)）。
- **Agents API 托管浏览器暴露给模型的接口**（computer tool / code / Browser connector）：「无出处，待核」（[Agents API CU](https://developers.openai.com/api/docs/guides/agents-api/tools/computer-use)）。
- **Codex `cua_repl` / `node_repl` 的工具描述与运行时**：开源仓库只有识别和审查逻辑（[mcp.rs](https://github.com/openai/codex/blob/main/codex-rs/protocol/src/mcp.rs)）。2026-10-15 已由社区逆向补上：AX 编号树 + 截图、10 个语义动作、`cua_repl` 中的 `cua` 对象，见 [Codex CU/BU 报告](https://github.com/demoleiwang/agent-frontier/blob/claude/intelligent-goldberg-ocxr01/reviews/2026-10-15_codex-cu-bu.md)。
- **code vs computer tool 的第三方受控对比**：没有找到。搜到的只是厂商博客类的 DOM 与视觉延迟和成本估算，属于二手，未采信（[presenc.ai](https://presenc.ai/research/browser-use-vs-computer-use-2026)，二手）。
- **Claude for Chrome、Claude Cowork 的具体动作接口**：本次未抓取产品页，`anthropic.com/product/claude-cowork` 返回 308。Opus 5.5 页面只列出 Cowork 和 Claude in Chrome 两个入口（[Opus 5.5](https://www.anthropic.com/claude-opus-5-5)）。「无出处，待核」
- **Kimi K3、MiMo 的 CU 接口**：报告或公开资料未说明（[K3 report](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)）。「无出处，待核」
- **Grok Bot 的 CU 循环**：xAI 文档摘录没有说明截图到动作的机制（[docs.x.ai](https://docs.x.ai/grok-bot/computer-and-apps)）；摘录中提到云电脑运行在 “Cursor's cloud”，此说法很不寻常，未采信。「无出处，待核」
