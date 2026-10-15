# Codex 是怎么操作电脑和浏览器的：官方源码、社区逆向与自己动手（截至 2026-10-15）

> 这份报告回答六个问题：
> 1. Codex（2026-07 起改名为 ChatGPT 桌面 app）的 computer use 和 browser use，看的是 AX 树还是截图？
> 2. 动作是怎么执行的？
> 3. 模型通过什么接口调用？
> 4. 哪些在本地、哪些在云端，能不能离线？
> 5. 为什么这样选？
> 6. 往哪里走？
>
> 逐项证据在附录：[自己动手的逆向](2026-10-15_codex-cu-bu/own-re.md) · [openai/codex 开源代码与时间线](2026-10-15_codex-cu-bu/oss.md) · [社区逆向汇总](2026-10-15_codex-cu-bu/community-re.md) · [官方时间线与大牛拆解](2026-10-15_codex-cu-bu/experts.md)。前一份报告的背景见 [写代码操作电脑](2026-10-14_personal-agent/code-computer-use.md)。
>
> 证据深度：
> - 开源代码、npm 包、社区仓库是逐文件读的；
> - Codex CLI 二进制是本仓库自己下载后检索的；
> - 桌面 app 本体和 Chrome 扩展无法下载（下载域名被拦），这部分靠社区逆向，标「作者实测」或「泄露」；
> - openai.com 只能看搜索摘录。
>
> 所有数字均为厂商或作者自报。

---

## 0. 一页结论

1. **桌面 computer use 以 AX 树为主、截图为辅，不是纯视觉。**
   - `get_app_state` 的官方工具描述是 "return a screenshot and accessibility tree"（[tools.js](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1)，本仓库已核对）。
   - AX 树渲染成带整数编号的文本，没有 set-of-marks（[iFurySt 实测样例](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/tool-call-samples-2026-04-17.md#L95-L143)）。
   - 动作优先按编号走 AX 语义（AXPress、`set_value`、secondary action），坐标是兜底，`drag` 只能用坐标（[tools.js](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1)）。
   - 后续读取只返回 AX 的 diff（[buYoung 实测](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/02-feasibility.json#L189)）。
   - Windows 版对应 UI Automation 树（[ELAI](https://github.com/DITlieD/ELAI-archive/blob/26bf2bc72d030a2d5ec022f04e1f9603bb285ae1/workflow/reasoning/codex-computer-use-RE-2026-07-12.md#L1-L160)）。
   - Linux 预览版只有像素（[opensky](https://github.com/tanishqkancharla/opensky/blob/54f1d13fe569031c745eebe10ee3f021cf15332f/docs/harness-friction.md#L1863-L1868)）。
2. **浏览器底层全部是 CDP。上层先有三套接口，现已收敛为两套**（[iFurySt automation-stack](https://github.com/iFurySt/open-codex-browser-use/blob/ebfca6587d2446836fbf8722c873fdf98d9a5524/docs/wiki/browser-client/automation/automation-stack.md#L1-L45)）。
   - in-app browser 是 Electron `<webview>`，经 `webContents.debugger` 驱动（[iFurySt](https://github.com/iFurySt/open-codex-browser-use/blob/ebfca6587d2446836fbf8722c873fdf98d9a5524/docs/wiki/browser-client/runtime/iab-architecture.md#L240-L330)）。
   - 用户的 Chrome 经 MV3 扩展加 native messaging，由扩展内的 `chrome.debugger` 发 CDP，不开调试端口（[iola1999](https://github.com/iola1999/codex-control-chrome-mcp/blob/c701215a63fc5ca6bdc208deb27417cb7da3cb44/docs/architecture.md#L9-L16)）。
   - 2026-05 的 skill 给出三套接口（[wong2 gist](https://gist.github.com/wong2/fec0b7239ce2c264ccaece96071578be)，本仓库已读全文）：
     - `cua`：坐标加截图，与 API `computer` tool 的动作集相同（[gist](https://gist.github.com/wong2/fec0b7239ce2c264ccaece96071578be)）；
     - `dom_cua`：可交互元素的 DOM node id（[gist](https://gist.github.com/wong2/fec0b7239ce2c264ccaece96071578be)）；
     - 受限的 `playwright`：用 CDP 重实现的选择器子集，不能 `evaluate`（[gist](https://gist.github.com/wong2/fec0b7239ce2c264ccaece96071578be)）。
   - 2026-09 起 Chrome 后端只剩 `ax`（AX 树编号）和 `playwright`（[opencode-codex-control](https://github.com/aryasaatvik/opencode-codex-control/blob/461e413785f8dc6119f36da3c52d2e8fb81e4098/src/tools/chrome.ts)；与 08-29 的 [executor](https://github.com/UsefulSoftwareCo/executor/blob/906bee5efc9b2bfc0d9341cd471a701314136144/packages/plugins/mcp/src/sdk/codex-browser-tools.ts#L1-L30) 对照）。
   - 推论：浏览器与桌面统一到同一套 AX 编号动作词表（依据：[chrome.ts](https://github.com/aryasaatvik/opencode-codex-control/blob/461e413785f8dc6119f36da3c52d2e8fb81e4098/src/tools/chrome.ts)、[tools.js](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1)）。
3. **模型不调用结构化的 CU 工具，而是写 JS。代码分两层，权限留在受信服务里。**
   - GPT-6 系列 `tool_mode: "code_mode_only"`，外层在无 Node、无网络的 V8 isolate 中运行（[models.json](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/models-manager/models.json#L20)、[description.rs](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/code-mode-protocol/src/description.rs#L21-L45)）。
   - 外层再调用 `cua_repl.js` 或 `node_repl.js`，内层是持久的 Node REPL（[mcp.rs](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/protocol/src/mcp.rs#L35-L65)）。
   - REPL 中模型写的 cell 一律不可信，只有白名单模块（`@oai/sky/service`、`@oai/browser-desktop/service`）能碰原生管道（[hqhq1025](https://github.com/hqhq1025/codex-computer-use-lab/blob/15effbd7c7fdc95b1340da7af239017481ddd6a8/docs/02-node-repl-trust-boundary.md#L1-L80)）。
   - 抓包显示请求里没有 Responses 原生的 `computer` tool（[hqhq1025 README](https://github.com/hqhq1025/codex-computer-use-lab/blob/15effbd7c7fdc95b1340da7af239017481ddd6a8/README.md#L24-L66)）。
4. **三代接口，9 个月里换了三次。**
   - 2026-04：独立 MCP server `computer-use`，10 个结构化工具（[iFurySt](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/packaging-and-lifecycle-integration.md#L5-L35)）。
   - 2026-08 前后：`node_repl` 中 `import("@oai/sky")`（[mcdp-adk](https://github.com/mcdp-adk/pi-codex-computer-use/blob/28a90381d2cb706a5316eac239182bec36f34936/docs/runtime-behavior.md#L14-L35)）。
   - 2026-08-23 起：统一的 `cua_repl`，同一个 `cua` 对象既开 app 也开浏览器 tab（[commit 2161ec2](https://github.com/openai/codex/commit/2161ec272a7d6b775c9c721e6206f4fe63e383f2)、[CL4R1T4S 泄露](https://github.com/elder-plinius/CL4R1T4S/blob/a4d3da04e63324e794a65500c3e41994fc4ab02e/OPENAI/Codex_Desktop/GPT-6-Sol_Tools.json)）。
5. **观察和执行都在本地，模型在云端，所以不能离线。**
   - AX 树和截图由本机的 Sky 服务用 AX API 和 ScreenCaptureKit 采集，作为工具结果交给云端模型（[iFurySt](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/baseline-architecture.md#L84-L99)）。
   - 动作用 `CGEventPostToPid` 直接投递给目标进程，不抢用户的鼠标（[iFurySt](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/background-click-free-tooling.md#L126-L142)）。
   - 会联网的非模型环节：站点安全查询 `chatgpt.com/backend-api/aura/site_status`（[iFurySt](https://github.com/iFurySt/open-codex-browser-use/blob/ebfca6587d2446836fbf8722c873fdf98d9a5524/docs/wiki/browser-client/security/policy-and-permissions.md)）、Sparkle 自更新、可能的遥测。
   - 另有一条完全在云端的链路：ChatGPT Work 和 Agents API 用 OpenAI 托管的 headless Chrome（[Simon Willison](https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/)）。
6. **这套东西来自收购与合并。**
   - 桌面 CU 的服务 bundle ID 是 `com.openai.sky.CUAService`，来自 2025-10 收购的 Sky（[Homebrew cask](https://raw.githubusercontent.com/Homebrew/homebrew-cask/master/Casks/c/chatgpt.rb)、[收购公告](https://openai.com/index/openai-acquires-software-applications-incorporated/)，official-search-excerpt）。
   - 浏览器客户端的入口函数原名 `setupAtlasRuntime`，来自 Atlas（[wong2 gist](https://gist.github.com/wong2/fec0b7239ce2c264ccaece96071578be)）。
   - Atlas 已于 2026-08 下线，功能并入桌面 app（[9to5Mac](https://9to5mac.com/2026/07/09/openai-is-discontinuing-chatgpt-atlas-its-standalone-desktop-browser/)，二手）。
7. **安全是多层叠加，而且 OpenAI 自己的审查模型专门盯 CU**（[guardian node_repl_policy.md](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/prompts/templates/guardian/node_repl_policy.md#L1-L11)）。
   - 从外到内依次是：app 黑名单（iTerm2 实测被拒）→ 按 app 或站点的用户授权 → 站点安全查询 → 模型侧四档确认策略 → Guardian 自动审查（GPT-6 系列强制，带截图）（[13-policy-error-state-machine.md](https://github.com/hqhq1025/codex-computer-use-lab/blob/15effbd7c7fdc95b1340da7af239017481ddd6a8/docs/13-policy-error-state-machine.md#L36-L75)）。
   - 出处：[iFurySt](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/tool-call-samples-2026-04-17.md#L180-L203)、[models.json](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/models-manager/models.json#L29-L30)、[node_repl_policy.md](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/prompts/templates/guardian/node_repl_policy.md#L1-L11)。
8. **研究侧推论：OpenAI 押注“代码编排 + 语义动作 + 同一套 harness 训练和部署”**（依据见下两条）。
   - `cua_repl` 的浏览器说明有 `training` 变体（[buYoung](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/briefs/2026-10-05-feat-codex-cua-05-browser-use.md)）。
   - 推论：RL 训练用的就是产品里这个 REPL 和 API。对我们的 M6（动手层）而言，练习场应该提供“持久 REPL + 受信 API + AX 编号”，而不是只给像素动作（依据同上，以及 [hqhq1025 信任边界](https://github.com/hqhq1025/codex-computer-use-lab/blob/15effbd7c7fdc95b1340da7af239017481ddd6a8/docs/02-node-repl-trust-boundary.md#L1-L80)）。

---

## 1. 全景：一次 computer use 调用经过哪些层

下图依据：[oss.md §1–2](https://github.com/demoleiwang/agent-frontier/blob/claude/intelligent-goldberg-ocxr01/reviews/2026-10-15_codex-cu-bu/oss.md)、[community-re.md §2–6](https://github.com/demoleiwang/agent-frontier/blob/claude/intelligent-goldberg-ocxr01/reviews/2026-10-15_codex-cu-bu/community-re.md)。

```
GPT-6 (云端, Responses API; 无原生 computer tool)
   │  写 JS
   ▼
Codex Code Mode `exec`  —— V8 isolate, 无 Node/FS/网络
   │  tools.mcp__cua_repl__js({title, code})        (旧: mcp__node_repl__js / mcp__computer_use__*)
   ▼
cua_repl / node_repl  —— 桌面 app 自带 Node 24 (cua_node/), Rust rmcp MCP server, 持久 REPL
   │  模型代码 = 不可信 vm 模块; 只有白名单服务能碰 nativePipe / elicitation
   ├──► @oai/sky/service ──(Unix socket / XPC / computeruse.sock, length-prefixed JSON-RPC)──►
   │        SkyComputerUseService (Swift, com.openai.sky.CUAService, Team 2DC432GLL2)
   │          观察: AX 树(编号+diff) + ScreenCaptureKit 截图(JPEG)
   │          动作: AXPress/SetValue/SecondaryAction 优先; CGEventPostToPid 后台点击; 软件光标 overlay
   │          Windows: codex-computer-use.exe = UIA + Windows.Graphics.Capture + SendInput
   └──► @oai/browser-desktop/service (browser-service.mjs) ──(/tmp/codex-browser-use/*.sock)──►
            iab:    Electron <webview> + webContents.debugger (CDP), partition persist:codex-browser-app
            chrome: MV3 扩展 + native host com.openai.codexextension + chrome.debugger (CDP)
            (云端) connector_openai_browser on codex_apps → OpenAI 托管 headless Chrome
   审批: elicitation (按 app / 按 origin / CDP / 上传下载) → Codex 核心 → 用户 或 Guardian 自动审查
```

---

## 2. 桌面 computer use 的技术细节

### 2.1 观察

- **AX 树**：每个元素一行，格式为“编号 role 状态 Value/ID/Secondary Actions”，末尾标出焦点元素（[iFurySt](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/tool-call-samples-2026-04-17.md#L95-L143)）。
- **让 Electron 和 Chromium 吐出 AX 树**：strings 中有 `AXManualAccessibility`、`AXEnhancedUserInterface`；网页区域会被压成 Markdown 风格文本（`flattenLinksIntoMarkdownText`）（[iFurySt state-rendering](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/state-rendering-1.0.770.md#L23-L77)）。
- **diff**：每个 turn 第一次 `get_app_state` 必须调用（"This must be called once per assistant turn"），之后只返回变化，`disableDiff` 返回全量（[tools.js](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1)、[buYoung](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/02-feasibility.json#L189)）。
- **截图**：ScreenCaptureKit 按 point 分辨率截取，存为 JPEG，坐标相对窗口（[whip](https://github.com/context-labs/whip/blob/88764670f1c6e2a57e22463e96cfb0d6021aea33/docs/learnings/other-harnesses/codex-computer-use-plugin.md#L1-L200)、[mcdp-adk](https://github.com/mcdp-adk/pi-codex-computer-use/blob/28a90381d2cb706a5316eac239182bec36f34936/docs/runtime-behavior.md#L51)）。
  - 截图给模型做视觉兜底，也在 AX 缺失时提供坐标。例如微信几乎不暴露 AX 元素（[syanbo/codex-cu](https://github.com/syanbo/codex-cu)）。
- **没有 OCR，也没有 set-of-marks**（[opencode-codex-computer-use ocr.ts](https://www.npmjs.com/package/opencode-codex-computer-use/v/0.2.0) 是第三方自己加的）。

### 2.2 动作

- 10 个工具：`list_apps`、`get_app_state`、`click`（编号或坐标）、`perform_secondary_action`、`set_value`、`select_text`、`scroll`（按元素翻页）、`drag`（坐标）、`press_key`（xdotool 语法）、`type_text`（[tools.js](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1)）。
- 后台执行：`CGEventPostToPid` 加私有的 `CGEventSetWindowLocation`，真实光标不动（[iFurySt](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/background-click-free-tooling.md#L126-L142)）。trycua 复现的同类做法是 SkyLight `SLEventPostToPid` 加 yabai 式聚焦（[trycua](https://github.com/trycua/cua/blob/b803be65c66a9ad5efeff93f5ff62ffc26b97e3e/blog/inside-macos-window-internals.md)）。
- 软件光标：每个 agent 一个，有 20 条贝塞尔候选路径加 spring 动画（[iFurySt](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/software-cursor-motion-reconstruction.md#L281-L319)）。
  - 推论：光标主要是给用户看的，表明 agent 在哪里操作，实际事件并不经过它（依据：[software-cursor-overlay.md](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/software-cursor-overlay.md)、[background-click](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/background-click-free-tooling.md#L126-L142)）。
- 中断：物理 Esc 会写一个标记文件，终止当前 turn（[mcdp-adk](https://github.com/mcdp-adk/pi-codex-computer-use/blob/28a90381d2cb706a5316eac239182bec36f34936/docs/runtime-behavior.md#L45)）。
- 锁屏继续工作：靠 `CodexComputerUseAuthorizationPlugin` 和 `CUALockScreenGuardian.app`（[cask](https://raw.githubusercontent.com/Homebrew/homebrew-cask/master/Casks/c/chatgpt.rb)、[synara](https://github.com/Emanuele-web04/synara/blob/a21eb2b43dc16dcc33c55271070d3bdb4a3c1cfb/docs/computer-use-cua/codex-ui-recon-2026-09-21.md#L1-L60)）。具体机制：「无出处，待核」。

### 2.3 进程与身份

- Sky 服务是一个独立的 LSUIElement app，用 Sparkle 自更新，没有 client 时自行退出（[iFurySt](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/packaging-and-lifecycle-integration.md#L64-L73)）。
- client 有 parent launch constraint，要求父进程由 OpenAI 签名；service 端做 sender 授权（[iFurySt](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/runtime-and-host-dependencies.md#L44-L91)）。
- TCC 的 Accessibility 和 Screen Recording 都授给 "Codex Computer Use" 这一个 app（[opencode-codex-control](https://www.npmjs.com/package/opencode-codex-control/v/0.1.0)）。
  - 推论：把高危权限集中到一个独立签名的服务，宿主（Codex、REPL）不持有权限，这样可以单独审计、单独更新（依据：[runtime-and-host-dependencies.md](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/runtime-and-host-dependencies.md#L44-L91)、[permissions.ts](https://www.npmjs.com/package/opencode-codex-control/v/0.1.0)）。

---

## 3. 浏览器的技术细节

### 3.1 三个后端，怎么选

- 后端有 `chrome`、`iab`、`mcpapps`，另有云端的 `connector_openai_browser`（[@buyong runtime.js](https://www.npmjs.com/package/@buyong/pi-codex-computer-use/v/0.1.2)、[mcp.rs](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/protocol/src/mcp.rs#L35-L65)）。
- 官方 skill 的规则：默认用 iab，需要用户已有的登录、profile 或扩展时才用 Chrome（[openai/plugins](https://github.com/openai/plugins/blob/0722921d5542fc593105c27bd52630babd8b8c2a/plugins/product-design/skills/index/SKILL.md#L56-L62)）。
  - 浏览器能做的事优先交给浏览器，不交给 Computer Use："Prefer this method … over alternatives (such as Computer Use)"（[@buyong runtime.js L276-290](https://www.npmjs.com/package/@buyong/pi-codex-computer-use/v/0.1.2)）。
- 推论：路由顺序是 iab → 用户 Chrome → 桌面 CU，从隔离、便宜到真实、昂贵（依据：[product-design SKILL.md](https://github.com/openai/plugins/blob/0722921d5542fc593105c27bd52630babd8b8c2a/plugins/product-design/skills/index/SKILL.md#L56-L62)、[@buyong runtime.js](https://www.npmjs.com/package/@buyong/pi-codex-computer-use/v/0.1.2)）。

### 3.2 驱动方式

- 全部经过 CDP："primarily through CDP"。Playwright 只是注入页面的 selector engine，点击最终变成 CDP 鼠标事件（[iFurySt automation-stack](https://github.com/iFurySt/open-codex-browser-use/blob/ebfca6587d2446836fbf8722c873fdf98d9a5524/docs/wiki/browser-client/automation/automation-stack.md#L1-L45)）。
- 观察的选择："Prefer Playwright where possible, but if it is not clear how to best use it, prefer vision"；"collect the cheapest state check that answers the next question"（[wong2 gist](https://gist.github.com/wong2/fec0b7239ce2c264ccaece96071578be)）。
- 用户上下文：`browser.user.openTabs()`、`claimTab()`、`history()`；每个 turn 必须以 `tabs.finalize({keep})` 收尾，留下的 tab 放进 "✅ Codex" tab group（[wong2 gist](https://gist.github.com/wong2/fec0b7239ce2c264ccaece96071578be)）。
- Developer mode（完整 CDP）需要单独开启和授权，官方称速度最多提升 2 倍（[OpenAIDevs](https://x.com/OpenAIDevs/status/2065226355495895521)，official-search-excerpt）。

### 3.3 接口的演进（关键趋势）

| 时间 | Chrome 后端的交互接口 | 出处 |
|---|---|---|
| 2026-05 | `cua`（坐标）+ `dom_cua`（DOM id）+ `playwright` | [wong2 gist](https://gist.github.com/wong2/fec0b7239ce2c264ccaece96071578be) |
| 2026-08-29 | 不支持 `ax`，用 `dom_cua` | [executor](https://github.com/UsefulSoftwareCo/executor/blob/906bee5efc9b2bfc0d9341cd471a701314136144/packages/plugins/mcp/src/sdk/codex-browser-tools.ts#L1-L30) |
| 2026-09-10 | 只剩 `ax` + `playwright` | [opencode-codex-control](https://github.com/aryasaatvik/opencode-codex-control/blob/461e413785f8dc6119f36da3c52d2e8fb81e4098/src/tools/chrome.ts) |
| 2026-10-05 | `cua.createBrowserTab("chrome")` 后 `getAXState()` 可用 | [buYoung](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/06-browser-use.json#L23-L30) |

- 推论：浏览器从“多种表示并存、由模型挑选”收敛为“与桌面同构的 AX 编号表示”。好处是动作词表统一、训练数据可以共享；代价是放弃了直接的像素坐标接口（依据：[chrome.ts](https://github.com/aryasaatvik/opencode-codex-control/blob/461e413785f8dc6119f36da3c52d2e8fb81e4098/src/tools/chrome.ts)、[gist](https://gist.github.com/wong2/fec0b7239ce2c264ccaece96071578be)）。

---

## 4. 本地、云端与离线

| 环节 | 位置 | 出处 |
|---|---|---|
| 模型推理 | 云端 | [models.json](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/models-manager/models.json#L20) |
| AX 树、截图采集 | 本机（Sky 服务；浏览器为 CDP） | [iFurySt](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/baseline-architecture.md#L84-L99) |
| 动作执行 | 本机 | [iFurySt](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/background-click-free-tooling.md#L126-L142) |
| REPL 和 Code Mode | 本机 | [description.rs](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/code-mode-protocol/src/description.rs#L21-L45) |
| Guardian 自动审查 | 云端（另一次模型调用，带截图） | [9b9b614](https://github.com/openai/codex/commit/9b9b614b02ba04df55479284749c5cbbed695c24) |
| 站点安全查询 | 云端 `aura/site_status`，缓存 24 小时 | [iFurySt](https://github.com/iFurySt/open-codex-browser-use/blob/ebfca6587d2446836fbf8722c873fdf98d9a5524/docs/wiki/browser-client/security/policy-and-permissions.md) |
| ChatGPT Work 和 Agents API 的浏览器 | 全云端（托管 headless Chrome） | [Simon Willison](https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/) |

- 结论：桌面版不能离线。屏幕数据在本机采集，但会作为工具结果（截图和 AX 文本）发给云端模型，开启自动审查时还会发给审查模型（依据：[9b9b614](https://github.com/openai/codex/commit/9b9b614b02ba04df55479284749c5cbbed695c24)、[baseline-architecture.md](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/baseline-architecture.md#L84-L99)）。
- 站点检查器出错时放行（fail open）（[hqhq1025](https://github.com/hqhq1025/codex-computer-use-lab/blob/15effbd7c7fdc95b1340da7af239017481ddd6a8/docs/25-timeout-deadline-url-policy-and-lifecycle.md#L100-L135)）。

---

## 5. 技术选择：和其他家对比

| | Codex（OpenAI 产品） | OpenAI API 示例 | Claude API | Google Gemini CU |
|---|---|---|---|---|
| 观察 | AX 编号树 + 截图，diff（[tools.js](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1)） | 模型自己决定输出什么（`display()`）（[README](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)） | computer 为截图 + 坐标；browser 为 AX 树 + ref + 截图（[CU 文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)、[browser 文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool)） | 纯像素，坐标归一化到 0–1000（[agent.py](https://github.com/google-gemini/computer-use-preview/blob/main/agent.py)） |
| 动作接口 | 在 REPL 中写 JS 调用受信 API（[CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S/blob/a4d3da04e63324e794a65500c3e41994fc4ab02e/OPENAI/Codex_Desktop/GPT-6-Sol_Tools.json)） | 单个 `code` 工具，用 Playwright 或 PyAutoGUI（[commit a0f5a76](https://github.com/openai/openai-cua-sample-app/commit/a0f5a7641df9fbe76968ca41245a5eceee6061ce)） | 结构化 toolset，不能从 code execution 调用（[tool reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference)） | 预定义动作（[agent.py](https://github.com/google-gemini/computer-use-preview/blob/main/agent.py)） |
| 浏览器 | CDP；iab、扩展、云端（[iFurySt](https://github.com/iFurySt/open-codex-browser-use/blob/ebfca6587d2446836fbf8722c873fdf98d9a5524/docs/wiki/browser-client/automation/automation-stack.md#L1-L45)） | Playwright（[README](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)） | browser toolset，`javascript_exec` 默认关闭（[browser 文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool)） | 浏览器截图（[agent.py](https://github.com/google-gemini/computer-use-preview/blob/main/agent.py)） |
| 后台、多 agent | 是，`CGEventPostToPid` + 软件光标（[iFurySt](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/background-click-free-tooling.md#L126-L142)） | 不适用（容器或 VM）（[README](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)） | 由开发者自己决定（[CU 文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)） | 不适用（[agent.py](https://github.com/google-gemini/computer-use-preview/blob/main/agent.py)） |

- MacStories 的对比：Codex 走 AX，Claude 走录屏加 AppleScript（[MacStories](https://macstories.net/notes/openais-new-codex-app-has-the-best-computer-use-feature-ive-ever-tested/)，二手）。
- 推论：OpenAI 在产品和 API 两条线上都选了“写代码”，但产品里的代码调用的是 AX 语义 API，不是 PyAutoGUI 式的像素操作。“写代码”和“AX 语义”是两个独立的维度，此前本仓库的笔记把两者混为一谈（依据：[tools.js](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1)、[commit a0f5a76](https://github.com/openai/openai-cua-sample-app/commit/a0f5a7641df9fbe76968ca41245a5eceee6061ce)；对照 [code-computer-use.md](2026-10-14_personal-agent/code-computer-use.md)）。

---

## 6. 技术方向与思路（推论）

以下各条都是推论，依据见各条链接（总依据：[community-re.md](https://github.com/demoleiwang/agent-frontier/blob/claude/intelligent-goldberg-ocxr01/reviews/2026-10-15_codex-cu-bu/community-re.md)）。

1. **统一动作词表。** 桌面 app、浏览器 tab、Windows 窗口共用一组 AX 语义动作：click、setValue、selectText、secondaryAction、scroll、drag、pressKey、typeText（[tools.js](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1)、[opencode-codex-control](https://github.com/aryasaatvik/opencode-codex-control/blob/461e413785f8dc6119f36da3c52d2e8fb81e4098/src/tools/chrome.ts)）。目的应是让一个模型、一套训练数据覆盖所有 surface。
2. **代码负责编排，权限留在受信服务。** 模型能写循环、能保存变量，但碰不到原生能力。安全审查递归检查 REPL 内的嵌套调用，并按实际界面效果判断（[hqhq1025](https://github.com/hqhq1025/codex-computer-use-lab/blob/15effbd7c7fdc95b1340da7af239017481ddd6a8/docs/02-node-repl-trust-boundary.md#L1-L80)、[node_repl_policy.md](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/prompts/templates/guardian/node_repl_policy.md#L1-L11)）。
3. **确认策略跟着模型走。** 11 KB 的四档策略挂在 `models.json` 的模型条目上，随调用传给插件（[models.json](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/models-manager/models.json#L124-L126)、[mcp_tool_call.rs](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/core/src/mcp_tool_call.rs#L1374-L1407)）。这意味着模型训练时已经学过这套策略，并与运行时约定一致。
4. **训练与部署同一个 harness。** `CUA_REPL_BROWSER_ENV=training`，加上 Agents API 托管同一个 Codex harness（[buYoung](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/briefs/2026-10-05-feat-codex-cua-05-browser-use.md)、[Agents API](https://openai.com/index/introducing-the-agents-api)，official-search-excerpt）。
5. **路由顺序：接口 → 隔离浏览器 → 用户浏览器 → 桌面。** 浏览器能做的事不交给 CU（[@buyong runtime.js](https://www.npmjs.com/package/@buyong/pi-codex-computer-use/v/0.1.2)、[openai/plugins](https://github.com/openai/plugins/blob/0722921d5542fc593105c27bd52630babd8b8c2a/plugins/product-design/skills/index/SKILL.md#L56-L62)）。
6. **下一步可能的方向：**
   - 浏览器标注 API（`browser_annotation_api`，09-30 加入）（[3bbf8ec](https://github.com/openai/codex/commit/3bbf8ec3a1e103c30d575f14f1827b193a8d415f)）；
   - WebMCP，即网站直接向 agent 暴露工具（[0f64d70](https://github.com/openai/codex/commit/0f64d7080864d22610731935cdc203bd2b3c5d93)）；
   - Record & Replay（`mcp__event_stream`）（[CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S/blob/a4d3da04e63324e794a65500c3e41994fc4ab02e/OPENAI/Codex_Desktop/5.6-Sol_Tools.json#L736)）；
   - 推论：从“看屏幕”走向“网站或 app 主动提供结构化接口”，从“每次重新摸索”走向“录一次、重放多次”（依据：[0f64d70](https://github.com/openai/codex/commit/0f64d7080864d22610731935cdc203bd2b3c5d93)、[5.6-Sol_Tools.json](https://github.com/elder-plinius/CL4R1T4S/blob/a4d3da04e63324e794a65500c3e41994fc4ab02e/OPENAI/Codex_Desktop/5.6-Sol_Tools.json#L736)）。

### 6.1 对本仓库 M6（动手层）的启示

以下也是推论。

- 练习场的动手层应同时提供三样东西：持久 REPL（变量跨调用保留）、受信 API（AX 编号语义动作 + 截图）、在 REPL 中可用的接口调用（依据：[sample-app README](https://github.com/openai/openai-cua-sample-app/blob/main/README.md)、[hqhq1025](https://github.com/hqhq1025/codex-computer-use-lab/blob/15effbd7c7fdc95b1340da7af239017481ddd6a8/docs/02-node-repl-trust-boundary.md#L1-L80)）。
- 环境存档时要包括 REPL 状态和 AX 快照，判分时要区分“语义动作”和“坐标动作”（依据：[community-re.md §3–4](https://github.com/demoleiwang/agent-frontier/blob/claude/intelligent-goldberg-ocxr01/reviews/2026-10-15_codex-cu-bu/community-re.md)）。
- 可以直接复用社区成果作为 baseline harness：
  - [iFurySt/open-codex-computer-use](https://github.com/iFurySt/open-codex-computer-use) 提供跨平台的同构工具；
  - [opensky](https://github.com/tanishqkancharla/opensky) 提供兼容 sky 的 API。
  - 用这些可以在开源模型上复现 Codex 式的接口，再和纯像素接口做受控对比。这一对比正是 compass 的 watch 项所等的信号（[compass watch](https://github.com/demoleiwang/agent-frontier/blob/claude/inspiring-lovelace-umqw6v/config/compass.yaml)）。

---

## 7. 缺口与待核

- 桌面 app 本体（`app.asar`、`cua_node/node_modules/@oai/*`、`browser-client.mjs` 原文）：本环境无法下载 `persistent.oaistatic.com`（[cask url](https://raw.githubusercontent.com/Homebrew/homebrew-cask/master/Casks/c/chatgpt.rb)）。「无出处，待核」
- `cua_repl` 的 `js` 工具描述全文（约 2,952 字符）：只有字数，没有原文（[buYoung](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/01-codex-runtime-bridge.md#L117)）。「无出处，待核」
- 截图的官方分辨率和缩放上限：「无出处，待核」
- iab 在 09 月以后是否也已切到 `ax`：「无出处，待核」
- 锁屏 CU 的授权插件机制：「无出处，待核」
- 遥测是否上传、屏幕数据是否另送云端：没有抓包证据。「无出处，待核」
- 有没有 “AX 语义 vs 像素 vs DOM” 的官方受控对比数字：没有找到。「无出处，待核」

## 8. 持续跟踪清单

以下是建议的跟踪方式。

- **openai/codex 的这些路径**：`codex-rs/plugin/src/bundled_hooks.rs`、`codex-rs/models-manager/models.json`、`codex-rs/config/src/browser_computer_use_requirements.rs`、`codex-rs/features/src/lib.rs`、`codex-rs/prompts/templates/guardian/`（[仓库](https://github.com/openai/codex/commits/main)）。
- **npm `@openai/codex` 新版本**：重跑 [own-re.md](2026-10-15_codex-cu-bu/own-re.md) 的 strings 检索，重点看新出现的插件 ID 和 feature key（[npm](https://www.npmjs.com/package/@openai/codex)）。
- **社区逆向仓库**：[iFurySt/open-codex-computer-use](https://github.com/iFurySt/open-codex-computer-use/commits/main)、[iFurySt/open-codex-browser-use](https://github.com/iFurySt/open-codex-browser-use/commits/main)、[hqhq1025/codex-computer-use-lab](https://github.com/hqhq1025/codex-computer-use-lab/commits/main)、[buYoung/pi-codex-auto-review](https://github.com/buYoung/pi-codex-auto-review/commits/main)。
- **泄露合集中的 Codex 目录**：[CL4R1T4S/OPENAI/Codex_Desktop](https://github.com/elder-plinius/CL4R1T4S/tree/main/OPENAI/Codex_Desktop)、[system_prompts_leaks/OpenAI/Codex](https://github.com/asgeirtj/system_prompts_leaks/tree/main/OpenAI/Codex)。
- **Homebrew `chatgpt` cask 的 zap 清单**：新增的路径往往意味着新组件（[cask 历史](https://github.com/Homebrew/homebrew-cask/commits/master/Casks/c/chatgpt.rb)）。
