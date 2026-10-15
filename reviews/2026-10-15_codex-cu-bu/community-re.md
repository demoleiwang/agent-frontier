# 社区逆向汇总：Codex（现 ChatGPT 桌面 app）的 computer use 与 browser use

> 2026-10-15 整理。按架构层组织，不按作者组织。
> 来源：25 个 npm 包的 tarball（各自解压、只读，未运行 `npm install`），20 多个 GitHub 仓库（clone 只读），以及几个提示词泄露合集。所有 GitHub 链接都钉在 commit 上。
> 证据等级：
> - 「包代码」：已发布的代码确实这样做；
> - 「作者实测」：作者在仓库文档里自述的 strings、otool、codesign、lsof、抓包、实调结果，本仓库未复现；
> - 「泄露」：提示词或工具 schema 合集，提取方法大多没有说明，未验证；
> - 「推论」：本仓库的推断。

## 0. 主要逆向者与方法

| 来源 | 时间 | 方法 | 覆盖面 |
|---|---|---|---|
| [iFurySt/open-codex-computer-use](https://github.com/iFurySt/open-codex-computer-use/tree/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering) | 2026-04-17 起 | strings、otool、codesign、lsof、crash report、实调 MCP、Ghidra 加原型验证；另写了开源仿制品 | 桌面 CU 最系统的一份，含光标运动、IPC、权限引导 |
| [iFurySt/open-codex-browser-use](https://github.com/iFurySt/open-codex-browser-use/tree/ebfca6587d2446836fbf8722c873fdf98d9a5524/docs) | 2026-04-24 起，10-12 在 ChatGPT 26.1007.30912 上复核 | 用 terser 美化 `browser-client.mjs`（817 KB），解包 `app.asar`，读 Chrome 扩展 1.1.4 快照 | 浏览器侧最系统的一份 |
| [hqhq1025/codex-computer-use-lab](https://github.com/hqhq1025/codex-computer-use-lab/tree/15effbd7c7fdc95b1340da7af239017481ddd6a8) | 2026-07-14 | 钉住版本哈希，做隔离探针，用合成的 AppKit 目标 app 测试 | 线协议、信任边界、策略状态机、威胁模型 |
| [buYoung/pi-codex-auto-review](https://github.com/buYoung/pi-codex-auto-review/tree/83889c6624ffc9363af85f30619da4a57c84fca2/docs) | 2026-10-05 → 10-11 | 在 pi 中复刻 Codex 宿主，实调 `cua_repl` | 最新的 `cua_repl` 合约、审批 `_meta`、浏览器后端 |
| [mcdp-adk/pi-codex-computer-use](https://github.com/mcdp-adk/pi-codex-computer-use/tree/28a90381d2cb706a5316eac239182bec36f34936/docs) | 2026-10 | 在 Windows 上实测 | Windows 版 sky（window2 API） |
| [iola1999/codex-control-chrome-mcp](https://github.com/iola1999/codex-control-chrome-mcp/tree/c701215a63fc5ca6bdc208deb27417cb7da3cb44/docs) | 2026-07 | 读压缩后的 `background.js` 和 `browser-client.mjs`，lsof 探测 socket | Chrome 扩展与 native host |
| [DITlieD/ELAI-archive](https://github.com/DITlieD/ELAI-archive/blob/26bf2bc72d030a2d5ec022f04e1f9603bb285ae1/workflow/reasoning/codex-computer-use-RE-2026-07-12.md) | 2026-07-12 | 解包 Windows MSIX 26.707 | Windows helper |
| [context-labs/whip](https://github.com/context-labs/whip/blob/88764670f1c6e2a57e22463e96cfb0d6021aea33/docs/learnings/other-harnesses/codex-computer-use-plugin.md) | 2026-08-24 | 分析 service 26.823 | XPC、IPC-4、附加 MCP server |
| [syanbo/codex-cu](https://github.com/syanbo/codex-cu) | 2026-09 前后 | 在 ChatGPT 26.930 上实测 skill | 进程链、`getAXState()` diff、审批文件 |
| [elder-plinius/CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S/tree/a4d3da04e63324e794a65500c3e41994fc4ab02e/OPENAI/Codex_Desktop)、[asgeirtj/system_prompts_leaks](https://github.com/asgeirtj/system_prompts_leaks/tree/3c4deaae9bbd6259e3d972f3bdb208ef6fd942f9/OpenAI/Codex) | 2026-06 → 09 | 泄露，方法未说明 | 工具 schema、skill 原文、Guardian prompt |

## 1. 安装布局（macOS）

- **主 app**：现名 `/Applications/ChatGPT.app`，bundle ID 仍为 `com.openai.codex`，Team ID `2DC432GLL2`；旧名 `/Applications/Codex.app`。「包代码」[browserjack@0.3.1](https://www.npmjs.com/package/browserjack/v/0.3.1) `dist/discovery/app.js` L7-8、L124-139
- **app-server 二进制**：`ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex`。「包代码」[codex-computer-use-mcp@0.6.1](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1) `dist/direct-broker.js` L10-13
- **Node 运行时**：`ChatGPT.app/Contents/Resources/cua_node/`（Node `24.21.0-cua.1`），内含 `@oai/cua-repl` 0.1.0、`@oai/cua` 0.2.5、`@oai/sky` 0.7.5、`@oai/browser-desktop` 0.1.1（2026-10 观测）。「作者实测」[buYoung 01-codex-runtime-bridge.md#L33-L37](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/01-codex-runtime-bridge.md#L33-L37)
  - 推论：Simon Willison 看到的 1.7 GB `~/.cache/codex-runtimes/codex-primary-runtime`（Python、Node、LibreOffice 等）是另一套给文档类 skill 用的运行时（[simonwillison.net](https://simonwillison.net/2026/Sep/1/codex-libreoffice/)）。
- **原生服务**：`~/.codex/computer-use/Codex Computer Use.app`，可执行文件 `SkyComputerUseService`，bundle ID `com.openai.sky.CUAService`。客户端在 `Contents/SharedSupport/SkyComputerUseClient.app`，bundle ID 为 `….cli`。app group 为 `2DC432GLL2.com.openai.sky.CUAService`。「包代码」[codex-computer-use-mcp](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1) `direct-broker.js` L14-17；「作者实测」[IF baseline-architecture.md#L9-L14](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/baseline-architecture.md#L9-L14)
- **插件**：
  - app 内置 marketplace：`Resources/plugins/openai-bundled/plugins/{computer-use,chrome,browser,unified-computer-use}`；
  - 安装后缓存：`~/.codex/plugins/cache/openai-bundled/<name>/<ver>/`。
  - 「包代码」[browserjack](https://www.npmjs.com/package/browserjack/v/0.3.1) `app.js` L104-121
- **其他组件**（「作者实测」[synara recon 2026-09-21](https://github.com/Emanuele-web04/synara/blob/a21eb2b43dc16dcc33c55271070d3bdb4a3c1cfb/docs/computer-use-cua/codex-ui-recon-2026-09-21.md#L1-L60)）：
  - `CUALockScreenGuardian.app`；
  - 一个安装器 app；
  - 按 app 区分的说明文件 `AppInstructions/*.md`。
  - 推论：这些对应锁屏 CU，以及按 app 定制的操作提示（依据同上，以及 [chatgpt.rb](https://raw.githubusercontent.com/Homebrew/homebrew-cask/master/Casks/c/chatgpt.rb) 中的 `CodexComputerUseAuthorizationPlugin`）。
- **自更新**：服务 app 用 Sparkle，更新源为 `https://oaisidekickupdates.blob.core.windows.net/mac/cua/alpha/appcast.xml`，`LSUIElement=1`（1.0.750 版）。「作者实测」[IF packaging-and-lifecycle-integration.md#L64-L73](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/packaging-and-lifecycle-integration.md#L64-L73)

## 2. 三代调用接口

### 2.1 第一代（2026-04 起）：MCP server `computer-use`，10 个结构化工具

- 启动方式：`.mcp.json` 只启动 `SkyComputerUseClient mcp`，走 stdio。二进制中还有 HTTP/SSE transport，但没有开放。「作者实测」[IF packaging-and-lifecycle-integration.md#L5-L35](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/packaging-and-lifecycle-integration.md#L5-L35)
- 10 个工具（2026-04 时有 9 个，没有 `select_text`）。工具描述原文见 [codex-computer-use-mcp@0.6.1](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1) `dist/tools.js` L76-112，本仓库已核对；另见 [CL4R1T4S 5.6-Sol_Tools.json#L736](https://github.com/elder-plinius/CL4R1T4S/blob/a4d3da04e63324e794a65500c3e41994fc4ab02e/OPENAI/Codex_Desktop/5.6-Sol_Tools.json#L736)「泄露」，两者一致：
  - `list_apps`："Returns the set of apps that are currently running, as well as any that have been used in the last 14 days"
  - `get_app_state{app}`："get the state of the app's key window and return a screenshot and accessibility tree. This must be called once per assistant turn before interacting with the app"
  - `click{app, element_index?, x?, y?, click_count?, mouse_button?}`："Click an element by index or pixel coordinates from screenshot"
  - `perform_secondary_action{element_index, action}`："Invoke a secondary accessibility action exposed by an element"
  - `set_value{element_index, value}`："Set the value of a settable accessibility element"
  - `select_text{element_index, text, prefix?, suffix?}`："Provide text exactly as it appears in the accessibility tree, including any Markdown formatting"
  - `scroll{element_index, direction, pages?}`
  - `drag{from_x, from_y, to_x, to_y}`：只能用像素坐标
  - `press_key{key}`："This supports xdotool's `key` syntax"
  - `type_text{text}`
- 同一命名空间中还有 `mcp__event_stream`（Record & Replay，最长 30 分钟）。「泄露」[CL4R1T4S 5.6-Sol_Tools.json](https://github.com/elder-plinius/CL4R1T4S/blob/a4d3da04e63324e794a65500c3e41994fc4ab02e/OPENAI/Codex_Desktop/5.6-Sol_Tools.json#L736)
- 2026-08 的 service 26.823 还附带 Messages、ComputerHistory、EventStream 等 MCP server。「作者实测」[whip](https://github.com/context-labs/whip/blob/88764670f1c6e2a57e22463e96cfb0d6021aea33/docs/learnings/other-harnesses/codex-computer-use-plugin.md#L1-L200)

### 2.2 第二代（2026-08 前后）：`node_repl` 加 `@oai/sky`

- 工具为 `js{code, title?, timeout_ms?=30000}`、`js_reset`、`js_add_node_module_dir`、`turn_ended`。「泄露」[asgeirtj gpt-6.1-sol.md#L6807-L6830](https://github.com/asgeirtj/system_prompts_leaks/blob/3c4deaae9bbd6259e3d972f3bdb208ef6fd942f9/OpenAI/Codex/gpt-6.1-sol.md#L6807-L6830)；「作者实测」[MC runtime-behavior.md#L14-L15](https://github.com/mcdp-adk/pi-codex-computer-use/blob/28a90381d2cb706a5316eac239182bec36f34936/docs/runtime-behavior.md#L14-L15)
- 模型的写法：`const {sky} = await import("@oai/sky")`。sky 的方法与第一代的 10 个工具一一对应，另加 `paste`。「包代码」[omo-codex-computer@0.1.7](https://www.npmjs.com/package/omo-codex-computer/v/0.1.7) `src/computer-use-transport.ts` L479-513
- **信任边界**：`cua_node/bin/node_repl` 是 Rust 写的 rmcp 1.5.0 server。模型写的 cell 一律作为不可信的 `vm.SourceTextModule` 运行；`nativePipe`、`createElicitation`、`launchServices` 只开放给白名单模块（`NODE_REPL_TRUSTED_SERVICES={"browser":"@oai/browser-desktop/service","sky":"@oai/sky/service"}`）。「作者实测」[HQ 02-node-repl-trust-boundary.md#L1-L80](https://github.com/hqhq1025/codex-computer-use-lab/blob/15effbd7c7fdc95b1340da7af239017481ddd6a8/docs/02-node-repl-trust-boundary.md#L1-L80)；「包代码」[browserjack](https://www.npmjs.com/package/browserjack/v/0.3.1) `dist/runtime/launch.js` L32-45
  - 推论：模型写的代码不能直接碰屏幕或浏览器，只能调用受信模块暴露的 API。这是“写代码操作电脑”在产品里的安全做法：代码只负责编排，权限留在受信服务里（依据同上）。
- REPL 注入的全局对象：`nodeRepl.write/emitImage/requestMeta/env/rpc/createElicitation/addTurnEndedHandler`；`process` 不可用；不允许顶层 static import。「作者实测」[MC runtime-behavior.md#L26-L35](https://github.com/mcdp-adk/pi-codex-computer-use/blob/28a90381d2cb706a5316eac239182bec36f34936/docs/runtime-behavior.md#L26-L35)

### 2.3 第三代（2026-08-23 起）：`cua_repl`（`unified-computer-use` 插件）

- 启动时 `await import("@oai/cua/tinyskyAlt")` 生成全局 `cua`，入口有 `cua.getState()`、`getTab({mention}|{url})`、`createBrowserTab("iab", url, {visible})`、`createBrowserTab("chrome"|"edge", url, {sessionName})`、`getBrowser({url})`、`getApp()`。
  - 「泄露」[CL4R1T4S GPT-6-Sol_Tools.json L3160-3260](https://github.com/elder-plinius/CL4R1T4S/blob/a4d3da04e63324e794a65500c3e41994fc4ab02e/OPENAI/Codex_Desktop/GPT-6-Sol_Tools.json)
  - 「作者实测」[buYoung 01-codex-runtime-bridge.md#L60-L117](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/01-codex-runtime-bridge.md#L60-L117)
- 由 `CUA_REPL_ENABLED_SURFACES=browser,computer` 选择打开哪些 surface。`enabled_tools` 为 `js`、`js_reset`、`turn_ended`，`output_token_limit` 25000。server instructions 原文："UI automation through cua_repl using the initialized cua API."（「作者实测」同上）
- `js` 带 `readOnlyHint:true`，所以 Codex 不在调用前询问用户，审批改由运行时的 elicitation 逐动作发起（「作者实测」[buYoung#L112-L115](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/01-codex-runtime-bridge.md#L112-L115)）。
- `CUA_REPL_BROWSER_ENV` 有 `codex-app`（默认）、`training`、`cloud`、`orbit` 四种取值，其中 `cloud` 和 `orbit` 会换成面向 CDP 的说明文本。「作者实测」[buYoung 05-browser-use brief](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/briefs/2026-10-05-feat-codex-cua-05-browser-use.md)
  - 推论：同一个 `cua_repl` 运行时被用在产品（codex-app）、RL 训练（training）和云端（cloud / orbit）三处，训练和部署用的是同一套 harness（依据：同上的取值名称；以及 [Agents API](https://openai.com/index/introducing-the-agents-api) 托管同一个 Codex harness，official-search-excerpt）。
- 使用量：buYoung 的日志中 `cua_repl/js` 调用 1,343 次，`node_repl/js` 790 次。「作者实测」[buYoung#L77](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/01-codex-runtime-bridge.md#L77)
- 平台差异：Windows 上 Codex 只对浏览器启用 `cua_repl`。「作者实测」[MC adr/0001](https://github.com/mcdp-adk/pi-codex-computer-use/blob/28a90381d2cb706a5316eac239182bec36f34936/docs/adr/0001-host-the-codex-repl.md#L10)
- 补充：桌面 app 的 Linux 改包脚本用正则改写 `app.asar`，从中能看到 `services.sky='@oai/sky/service'`、`CUA_REPL_ENABLED_SURFACES`、`@oai/cua/tinyskyAlt`、`browserUseTinysky`。「包代码」[ilysenko unified.js#L17-L90](https://github.com/ilysenko/codex-desktop-linux/blob/ac4c7c173768b53492cafbe66f6cd4f4f68a5751/linux-features/computer-use-linux/unified.js#L17-L90)

### 2.4 Responses API 层面

- 抓到的基础请求里没有 Responses 原生的 `computer` tool，CU 走的是 deferred tool discovery → `node_repl` → `@oai/sky` → Unix socket → Sky 服务。「作者实测」[HQ README#L24-L66](https://github.com/hqhq1025/codex-computer-use-lab/blob/15effbd7c7fdc95b1340da7af239017481ddd6a8/README.md#L24-L66)
  - 推论：Codex 产品里的 CU 不使用 API 版的 `computer` tool，和官方示例仓库删掉 native mode 的方向一致（依据同上，以及 [openai-cua-sample-app commit a0f5a76](https://github.com/openai/openai-cua-sample-app/commit/a0f5a7641df9fbe76968ca41245a5eceee6061ce)）。

## 3. 观察：AX 树为主，截图为辅

- **AX 文本树**：每行是“整数索引 + role + 状态 + Value/ID/Secondary Actions”，末尾附 "The focused UI element is N"，另外附一张窗口截图。没有 set-of-marks，编号只存在于文本中。「作者实测」[IF tool-call-samples-2026-04-17.md#L95-L143](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/tool-call-samples-2026-04-17.md#L95-L143)
- **diff**：后续调用只返回 AX 树的变化（"There has been no change in the accessibility tree…"），`disableDiff` 强制返回全量；`getAXStateAndScreenshot()` 是带截图的版本。「作者实测」[buYoung 02-feasibility.json#L189](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/02-feasibility.json#L189)；[syanbo/codex-cu](https://github.com/syanbo/codex-cu)
- **渲染**：strings 中有 `AXManualAccessibility`、`AXEnhancedUserInterface`（强制 Electron 和 Chromium 暴露 AX 树）、`domClassList`、`pruneNonDescriptiveSubtrees`、`flattenLinksIntoMarkdownText`、`retrieveAttributedTextFromWebAreas`。「作者实测」[IF state-rendering-1.0.770.md#L23-L77](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/state-rendering-1.0.770.md#L23-L77)
  - 推论：网页区域的 AX 树会被压成 Markdown 风格的文本，这也是 `select_text` 要求 "including any Markdown formatting" 的原因（依据同上，以及 [tools.js](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1)）。
- **截图**：ScreenCaptureKit 按 point 分辨率截取，存为 JPEG（「作者实测」[whip](https://github.com/context-labs/whip/blob/88764670f1c6e2a57e22463e96cfb0d6021aea33/docs/learnings/other-harnesses/codex-computer-use-plugin.md#L1-L200)）。MCP 路径返回 base64 JPEG，REPL 路径返回 `file://` URL（「包代码」[omo-codex-computer](https://www.npmjs.com/package/omo-codex-computer/v/0.1.7) `src/computer-use-transport.ts` L522-545）。临时文件位于 `$TMPDIR/com.openai.sky.CUAService/`（「包代码」[computer-use-capture@0.2.2](https://www.npmjs.com/package/computer-use-capture/v/0.2.2) `lib/codex-screenshots.mjs` L5）。
- **坐标**：相对窗口的截图像素，150% 缩放下同样适用。「作者实测」[MC runtime-behavior.md#L51](https://github.com/mcdp-adk/pi-codex-computer-use/blob/28a90381d2cb706a5316eac239182bec36f34936/docs/runtime-behavior.md#L51)
- **OCR**：Codex 自身不做 OCR。「包代码」[opencode-codex-computer-use@0.2.0](https://www.npmjs.com/package/opencode-codex-computer-use/v/0.2.0) `src/ocr.ts` 是该插件自己加的
- **AX 树为空的情形**：例如微信几乎不暴露 AX 元素（`AXError.notImplemented`），这时只能用截图加坐标。「作者实测」[syanbo/codex-cu](https://github.com/syanbo/codex-cu)
- **权限引导文案**："Codex uses screenshots to know where to click"。「作者实测」[IF permission-onboarding.md#L50-L110](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/permission-onboarding.md#L50-L110)
  - 推论：截图同时承担两个作用，一是给模型做视觉兜底，二是在 AX 不可用时提供坐标。所以 Screen Recording 和 Accessibility 两项权限都必需（依据同上）。

## 4. 动作：语义动作优先，后台执行，不抢用户的鼠标

- 优先使用 AX 语义动作：AXPress、`set_value`、`perform_secondary_action`（AXShowMenu、Expand 等）。坐标只是补充，`drag` 只能用坐标。动作返回 `void`，模型需要重新读取状态；运行时会等 UI 稳定后再返回。「作者实测」[geohotstan codex-parity.md#L40](https://github.com/geohotstan/dsh-computer-use/blob/0b623103419706a73c40e3c6dcf1ae6584cdaa06/docs/codex-parity.md#L40)；[IF baseline-architecture.md#L320-L334](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/baseline-architecture.md#L320-L334)
- **后台点击**：用 `NSEvent(windowNumber=CGWindowID)` 设置 CGEvent 字段 91/92，调用私有的 `CGEventSetWindowLocation`，再用 `CGEventPostToPid` 直接投递给目标进程。真实鼠标不动，用户可以同时操作。「作者实测」[IF background-click-free-tooling.md#L126-L142](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/background-click-free-tooling.md#L126-L142)
  - trycua 的同类做法：私有 SkyLight `SLEventPostToPid`，yabai 式聚焦（不抬起窗口），`_AXObserverAddNotificationAndCheckRemote` 让被遮挡的 Electron AX 树保持更新（[trycua blog](https://github.com/trycua/cua/blob/b803be65c66a9ad5efeff93f5ff62ffc26b97e3e/blog/inside-macos-window-internals.md)）。
- **软件光标**：一个 overlay 窗口画虚拟光标。运动模型生成 20 条贝塞尔候选路径并优先选不出界的；spring 参数 response 1.4、damping 0.9，Velocity-Verlet 积分，dt = 1/240。「作者实测」[IF software-cursor-motion-reconstruction.md#L281-L319](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/software-cursor-motion-reconstruction.md#L281-L319)；JS 移植见 [cursor-motion@0.2.3](https://www.npmjs.com/package/cursor-motion/v/0.2.3)
  - 多个 agent 并行时，每个 agent 各有一个光标（[openai.com](https://openai.com/index/codex-for-almost-everything/)，official-search-excerpt）。
- **中断**：屏幕上显示 "ChatGPT is using your computer — Esc to cancel"。物理 Esc 键会写入 `<CODEX_HOME>/cache/computer-use/interrupts/<session>/<turn>`，该 turn 的后续请求全部被拒，新 turn 恢复。「作者实测」[MC runtime-behavior.md#L45](https://github.com/mcdp-adk/pi-codex-computer-use/blob/28a90381d2cb706a5316eac239182bec36f34936/docs/runtime-behavior.md#L45)；[opencode-codex-computer-use README](https://www.npmjs.com/package/opencode-codex-computer-use/v/0.2.0)
- **超时**：客户端超时不会取消已被接受的动作；用过期坐标点击可能点中别的元素；坐标点击能穿透到进程外的 WKWebView。「作者实测」[HQ README#L24-L66](https://github.com/hqhq1025/codex-computer-use-lab/blob/15effbd7c7fdc95b1340da7af239017481ddd6a8/README.md#L24-L66)

## 5. 进程间通信与身份校验

- **client 到 service**，演进如下：
  1. 1.0.755：Apple Events `SkCu/SndR`，外部进程调用报 "Sender process is not authenticated"（「作者实测」[IF runtime-and-host-dependencies.md#L283-L306](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/runtime-and-host-dependencies.md#L283-L306)）；
  2. 2026-07：`@oai/sky@0.4.20`，`CodexComputerUseIPC-2`，Unix socket，小端长度前缀，单帧最大 8 MiB，先 ping 再 `request`，信封为 `{requestType, codexTurnMetadata, deadlineUnixMilliseconds, request}`（「作者实测」[HQ 03-sky-native-pipe-protocol.md#L30-L250](https://github.com/hqhq1025/codex-computer-use-lab/blob/15effbd7c7fdc95b1340da7af239017481ddd6a8/docs/03-sky-native-pipe-protocol.md#L30-L250)）；
  3. 2026-08：XPC，`CodexComputerUseIPC-4`（「作者实测」[whip](https://github.com/context-labs/whip/blob/88764670f1c6e2a57e22463e96cfb0d6021aea33/docs/learnings/other-harnesses/codex-computer-use-plugin.md#L1-L200)）；
  4. 2026-10：`~/Library/Group Containers/2DC432GLL2.com.openai.sky.CUAService/IPC/computeruse.sock` 上的 JSON-RPC 2.0（「作者实测」[buYoung#L69](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/01-codex-runtime-bridge.md#L69)）。
  - 推论：协议换代很快，社区桥接工具会频繁失效（依据：上面四个版本）。
- **内部请求类型**：`ListApps`、`AppStart`、`AppModify`、`AppPerformAction`（坐标或 elementID）、`AppGetSkyshot`（即 `get_app_state` 的截图加 AX 树）、`CodexTurnEnded`、`AppUsage`。「作者实测」[IF internal-ipc-surface.md#L20-L140](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/internal-ipc-surface.md#L20-L140)
- **launch constraint**：client 声明 parent 必须由 `team-identifier=2DC432GLL2` 签名，用 node 或 python 拉起会被 SIGKILL（"Launch Constraint Violation"）。社区的绕法是用已签名的 `codex sandbox` 当 parent。「作者实测」[IF runtime-and-host-dependencies.md#L44-L91](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/runtime-and-host-dependencies.md#L44-L91)；「包代码」[claude-codex-computer-use@0.1.2](https://www.npmjs.com/package/claude-codex-computer-use/v/0.1.2) `bin/computer-use-mcp-bridge.mjs` L179-206
- **service 回连 Codex**：通过 `$TMPDIR/codex-ipc/ipc-501.sock`，相关字符串有 `CodexAppServerJSONRPCConnection`、`CodexAppServerAuthProvider`。「作者实测」[IF runtime-and-host-dependencies.md#L112-L145](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/runtime-and-host-dependencies.md#L112-L145)
- **外部宿主的接入方式**：`codex app-server` 走换行分隔的 JSON-RPC，流程为 `initialize` → `thread/start{ephemeral}` → `mcpServer/tool/call`，审批以 `mcpServer/elicitation/request` 回传。「包代码」[pi-codex-computer-use@0.1.0](https://www.npmjs.com/package/pi-codex-computer-use/v/0.1.0) `src/computer-use-backend.ts`
  - “零模型 broker”的做法：`model_provider` 指向 `127.0.0.1:9`，只注入 `computer-use` server。「包代码」[codex-computer-use-mcp](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1) `direct-broker.js` L200-224

## 6. 浏览器

### 6.1 三个后端

- `BROWSER_USE_AVAILABLE_BACKENDS=chrome,iab,mcpapps`。「包代码」[@buyong/pi-codex-computer-use@0.1.2](https://www.npmjs.com/package/@buyong/pi-codex-computer-use/v/0.1.2) `dist/runtime.js` L283（本仓库已核对）
- api.json 中的浏览器类型为 `iab|extension|cdp`。「作者实测」[storybook 中复制的 codex-browser-api.json](https://github.com/storybookjs/storybook/blob/8d01e0376cd807b281940e3f9ab323c46b2063f3/agent-eval/lib/mcp/codex-browser-api.json)
- 选择 API：`get("iab")`、`get("extension")`、`getForUrl()`、`getDefault()`（默认优先 in-app browser）。「泄露」[CL4R1T4S 5.6-Sol_SystemPrompt.md#L1785-L1845](https://github.com/elder-plinius/CL4R1T4S/blob/a4d3da04e63324e794a65500c3e41994fc4ab02e/OPENAI/Codex_Desktop/5.6-Sol_SystemPrompt.md#L1785-L1845)
- 官方 skill 的使用原则：默认用 in-app browser，需要已有登录、profile 或扩展时才用 Chrome（[openai/plugins product-design SKILL.md#L56-L62](https://github.com/openai/plugins/blob/0722921d5542fc593105c27bd52630babd8b8c2a/plugins/product-design/skills/index/SKILL.md#L56-L62)）。

### 6.2 in-app browser（iab）

- 实现：每个对话一个 Electron `<webview>` guest `webContents`，经 `webContents.debugger.sendCommand`（CDP）或 `executeJavaScript` 驱动。数据存在 partition `persist:codex-browser-app`，cookie 和登录会保留。Chromium 版本 155。「作者实测」[IFB iab-architecture.md#L240-L330](https://github.com/iFurySt/open-codex-browser-use/blob/ebfca6587d2446836fbf8722c873fdf98d9a5524/docs/wiki/browser-client/runtime/iab-architecture.md#L240-L330)
  - 这与官方文档“in-app browser 不带用户 profile 的 cookie 和扩展”不矛盾：iab 有自己的独立 profile（[developers.openai.com/codex/app/browser](https://developers.openai.com/codex/app/browser.md)，official-search-excerpt）。
- 本地 socket 有原生插件 `browser-use-peer-authorization.node` 把关，未授权的 `getInfo` 不会得到响应。「作者实测」[IFB iab-architecture.md#L479-L560](https://github.com/iFurySt/open-codex-browser-use/blob/ebfca6587d2446836fbf8722c873fdf98d9a5524/docs/wiki/browser-client/runtime/iab-architecture.md#L479-L560)
- 从外部宿主调用会报 "Browser is not available: iab"，iab 只能在桌面 app 内使用。「作者实测」[buYoung 06-browser-use.json#L39-L48](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/06-browser-use.json#L39-L48)

### 6.3 用户的 Chrome（extension 后端）

- 链路：MV3 扩展（ID `hehggadaopoacecdllhhajmbjkdcmajg`，另有 Edge 用的 `odlomjlbamekndcpllcnffbgeohgkmjh`）→ `chrome.runtime.connectNative("com.openai.codexextension")` → native host（`~/.codex/plugins/cache/openai-bundled/chrome/latest/extension-host/macos/arm64/ChatGPT for Chrome`）→ JSON-RPC → `chrome.debugger.attach(tab, "1.3")` 发 CDP 命令。不开启 remote debugging port。
  - 「作者实测」[IO architecture.md#L9-L16](https://github.com/iola1999/codex-control-chrome-mcp/blob/c701215a63fc5ca6bdc208deb27417cb7da3cb44/docs/architecture.md#L9-L16)
  - 「作者实测」[buYoung 05-browser-use brief](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/briefs/2026-10-05-feat-codex-cua-05-browser-use.md)
- 扩展 1.1.4 的权限：nativeMessaging、debugger、tabs、tabGroups、downloads、history、scripting、storage、`<all_urls>`。「作者实测」[IFB codex-chrome-extension-1.1.4/README.md](https://github.com/iFurySt/open-codex-browser-use/blob/ebfca6587d2446836fbf8722c873fdf98d9a5524/docs/references/codex-chrome-extension-1.1.4/README.md)
- 本地 socket：macOS 为 `/tmp/codex-browser-use/*.sock`；Windows 为 `\\.\pipe\codex-browser-use-<uuid>`，帧格式是 4 字节小端长度加 JSON-RPC。方法有 `getInfo`、`getTabs`、`getUserTabs`、`createTab`、`claimUserTab`、`attach`、`detach`、`executeCdp`、`finalizeTabs`、`nameSession`、`moveMouse`、`ping`，参数都带 `session_id` 和 `turn_id`。「作者实测」[IFB browser-client-reverse-engineering.md](https://github.com/iFurySt/open-codex-browser-use/blob/ebfca6587d2446836fbf8722c873fdf98d9a5524/docs/references/browser-client-reverse-engineering.md)；「包代码」[DB protocol.rs](https://github.com/DeliciousBuding/codex-browser-bridge/blob/c692fb017d79d458927c6a8e350dc2d06224d46e/src/protocol.rs)
- 直连官方 socket 会遇到 EPIPE，client 报 "privileged native pipe bridge is not available; browser-client is not trusted"。26.814 起，浏览器控制移到受信的 `browser-service.mjs`，client 通过 `nodeRepl.rpc("browser")` 调用它。「作者实测」[IO socket-probe.md#L9-L43](https://github.com/iola1999/codex-control-chrome-mcp/blob/c701215a63fc5ca6bdc208deb27417cb7da3cb44/docs/socket-probe.md#L9-L43)；「包代码注释」[browserjack](https://www.npmjs.com/package/browserjack/v/0.3.1) `launch.js` L37-41
- `browser-service.mjs` 读取的开关：`BROWSER_USE_SECURITY_MODE`、`BROWSER_USE_FULL_CDP_ACCESS_ENABLED`、`BROWSER_USE_DISABLE_{TAB,BROWSER}_CAPABILITIES`、`BROWSER_USE_DISABLE_API_MEMBERS`、`BROWSER_USE_AUTOMATIC_OTP_ENABLED`、`BROWSER_USE_AUTOMATED_SAFETY_PRECHECKS_ENABLED`。「作者实测」[buYoung 05-browser-use brief](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/briefs/2026-10-05-feat-codex-cua-05-browser-use.md)

### 6.4 页面怎么被驱动：以 CDP 为主，Playwright 只做选择器

- "primarily through CDP"。Playwright 只是以注入的 selector engine（`window.__codexPlaywrightInjected`）运行在页面里，点击最终变成 CDP 鼠标事件；不支持 `networkidle`。「作者实测」[IFB automation-stack.md#L1-L45](https://github.com/iFurySt/open-codex-browser-use/blob/ebfca6587d2446836fbf8722c873fdf98d9a5524/docs/wiki/browser-client/automation/automation-stack.md#L1-L45)
  - 推论：所谓的 `tab.playwright` 不是一个 Playwright 进程，而是用 CDP 重新实现的 Playwright 子集。所以不能 `evaluate`，并且有 strict mode（依据同上，以及 [wong2 gist L449](https://gist.github.com/wong2/fec0b7239ce2c264ccaece96071578be)）。
- 命令注册表：`cua_*`（click、double_click、drag、get_visible_screenshot、keypress、move、scroll、type）、`dom_cua_*`、`navigate_tab_*`、`playwright_dom_snapshot`、`playwright_locator_*`、`playwright_screenshot`、`browser_user_*`、`finalize_tabs`、`tab_dev_logs`。「作者实测」[IFB browser-client-reverse-engineering.md#L183-L236](https://github.com/iFurySt/open-codex-browser-use/blob/ebfca6587d2446836fbf8722c873fdf98d9a5524/docs/references/browser-client-reverse-engineering.md#L183-L236)
- storybook 的 eval mock 参数：视口 1280×720，截图 JPEG，`domSnapshot` 为 ARIA 风格的文本。「作者实测」[storybook mock#L1-L22](https://github.com/storybookjs/storybook/blob/8d01e0376cd807b281940e3f9ab323c46b2063f3/agent-eval/lib/mcp/codex-browser-client-mock.mjs#L1-L22)
- `getTabContext` 返回页面 innerText，被遮罩的表单控件替换为 `<browser__redacted_form_control/>`。「泄露」[CL4R1T4S GPT-6-Sol_Tools.json L304](https://github.com/elder-plinius/CL4R1T4S/blob/a4d3da04e63324e794a65500c3e41994fc4ab02e/OPENAI/Codex_Desktop/GPT-6-Sol_Tools.json)

### 6.5 浏览器的交互接口：2026-05 有三套并存，到 2026-09 只剩两套

| 时间 | 证据 | Chrome/extension 后端的可用接口 |
|---|---|---|
| 2026-05-09 | [wong2 gist](https://gist.github.com/wong2/fec0b7239ce2c264ccaece96071578be)（本仓库已读全文） | `cua`（坐标加截图）、`dom_cua`（`get_visible_dom()` 返回的 DOM node id）、`playwright`（无 `evaluate`） |
| 2026-08-29 | [executor codex-browser-tools.ts](https://github.com/UsefulSoftwareCo/executor/blob/906bee5efc9b2bfc0d9341cd471a701314136144/packages/plugins/mcp/src/sdk/codex-browser-tools.ts#L1-L30)（本仓库已核对，commit 7cfcfef0） | "the plugin's own API reference marks `ax` unsupported on the `extension`, `iab`, and `cdp` backends"，所以用 `dom_cua` |
| 2026-09-10 | [opencode-codex-control@0.1.0 chrome.ts](https://github.com/aryasaatvik/opencode-codex-control/blob/461e413785f8dc6119f36da3c52d2e8fb81e4098/src/tools/chrome.ts)（本仓库已核对） | "on the `extension` backend `dom_cua` and `cua` are filtered out and only `ax` and `playwright` remain"；`ax.get("state")` 返回 AX 树文本 |
| 2026-10-05 | [buYoung 06-browser-use.json#L23-L30](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/06-browser-use.json#L23-L30) | `cua.createBrowserTab("chrome", …)` 后 `getAXState()` 实测可用 |

- 推论：2026-08 底到 09 初，浏览器交互从“坐标 / DOM-id / Playwright”换成了“AX 编号 / Playwright”，和 `cua_repl`（08-23）及 GPT-6 Astra（09-03）上线的时间吻合。浏览器从此和桌面共用同一套 AX 编号动作词表（`click/typeText/pressKey/scroll/setValue/selectText/performSecondaryAction/drag`）（依据：上表四行，以及 [opencode-codex-control chrome.ts](https://github.com/aryasaatvik/opencode-codex-control/blob/461e413785f8dc6119f36da3c52d2e8fb81e4098/src/tools/chrome.ts) L126-276）。
- 这一推断的反证：iab 后端在 09 月以后是否也已切到 `ax`，没有直接证据。「无出处，待核」

## 7. 安全层（从外到内）

1. **组织与 app 策略**：每个 app 有 allowed、denied by org、forbidden for safety 三种状态。「作者实测」[HQ 13-policy-error-state-machine.md#L36-L75](https://github.com/hqhq1025/codex-computer-use-lab/blob/15effbd7c7fdc95b1340da7af239017481ddd6a8/docs/13-policy-error-state-machine.md#L36-L75)
   - 实测 iTerm2 被拒："Computer Use is not allowed to use the app 'com.googlecode.iterm2' for safety reasons."（「作者实测」[IF tool-call-samples-2026-04-17.md#L202](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/tool-call-samples-2026-04-17.md#L180-L203)，本仓库已核对）。
   - 完整 denylist 未公开，仿制品猜测包括终端、密码管理器、SecurityAgent（[geohotstan SafetyPolicy.swift](https://github.com/geohotstan/dsh-computer-use/blob/0b623103419706a73c40e3c6dcf1ae6584cdaa06/native/Sources/dsh-computer-daemon/SafetyPolicy.swift#L5-L45)，推论）。
2. **按 app 审批**：elicitation 文案为 "Allow Computer Use to use \"Finder\"?"，`_meta` 为 `persist:["session","always"]`、`riskLevel:"low"`、`connector_id:"computer-use"`；永久授权存在 `ComputerUseAppApprovals.json`。「作者实测」[buYoung 02-feasibility.json#L212-L240](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/02-feasibility.json#L212-L240)；[syanbo/codex-cu](https://github.com/syanbo/codex-cu)
3. **URL 与站点策略**：浏览器访问前要经过三道检查：
   - 能力检查；
   - `chatgpt.com/backend-api/aura/site_status`，缓存 24 小时，`feature_status.agent` 为 true 时拦截；
   - 按站点的用户授权，`connector_id: browser-use`、`persist: always`，localhost 免授权。
   - 出处：「作者实测」[IFB policy-and-permissions.md](https://github.com/iFurySt/open-codex-browser-use/blob/ebfca6587d2446836fbf8722c873fdf98d9a5524/docs/wiki/browser-client/security/policy-and-permissions.md)；用户看到的拦截提示见 [openai/codex#47800](https://github.com/openai/codex/issues/47800)。
   - 桌面 CU 操作浏览器窗口时也查 URL（`AuraSiteStatusURLPolicyChecker`），只检查可见 URL；检查器出错时放行（fail open）。「作者实测」[HQ 25-timeout-deadline-url-policy-and-lifecycle.md#L100-L135](https://github.com/hqhq1025/codex-computer-use-lab/blob/15effbd7c7fdc95b1340da7af239017481ddd6a8/docs/25-timeout-deadline-url-policy-and-lifecycle.md#L100-L135)
4. **逐动作审批的类型**：origin 访问（`tool_name:"access_browser_origin"`，`codex_sensitive_action`）、上传、下载、完整 CDP（`riskLevel:high`）、WebMCP、OTP、`browser_auth`、录音。「作者实测」[buYoung 06-browser-use.json#L66-L88](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/06-browser-use.json#L66-L88)
5. **模型侧确认策略与 Guardian 自动审查**：见 [oss.md §5](oss.md) 和 [own-re.md §2.4](own-re.md)。泄露的 Guardian V2 分类器根据“当前动作、前 5 步和后 2 步”输出 high 或 low；风险表把登录和丢失浏览器状态列为 high，在已有 session 中导航列为 medium。「泄露」[CL4R1T4S GPT-6-Astra_Prompts.md#L338-L396](https://github.com/elder-plinius/CL4R1T4S/blob/a4d3da04e63324e794a65500c3e41994fc4ab02e/OPENAI/Codex_Desktop/GPT-6-Astra_Prompts.md#L338-L396)
   - 泄露中的 Node REPL policy 与开源模板几乎相同，这说明该泄露至少部分可信（推论；对照 [node_repl_policy.md](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/prompts/templates/guardian/node_repl_policy.md#L1-L11)）。
6. **威胁模型的作者评估**：CU 服务本身不在沙箱里；锁屏 broker 的 socket 权限为 0666。「作者实测」[HQ 06-security-threat-model.md#L12-L34](https://github.com/hqhq1025/codex-computer-use-lab/blob/15effbd7c7fdc95b1340da7af239017481ddd6a8/docs/06-security-threat-model.md#L12-L34)
7. **TCC 权限**：Accessibility 和 Screen Recording 授给 "Codex Computer Use"，所有宿主共享；Automation 按宿主分别授予。「包代码」[opencode-codex-control](https://www.npmjs.com/package/opencode-codex-control/v/0.1.0) `src/codex/permissions.ts` L20-60

## 8. 本地还是云端

- AX 树和截图都在本机采集（ScreenCaptureKit 和 AX），作为工具结果交给模型；动作在本机执行。「作者实测」[IF baseline-architecture.md#L84-L99](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/baseline-architecture.md#L84-L99)
  - 推论：除了模型推理本身，没有发现屏幕内容另送云端处理的证据（依据同上）。这一点没有抓包证实。
- **会联网的非模型环节**：
  - 站点安全检查 `aura/site_status`（「作者实测」[IFB policy-and-permissions.md](https://github.com/iFurySt/open-codex-browser-use/blob/ebfca6587d2446836fbf8722c873fdf98d9a5524/docs/wiki/browser-client/security/policy-and-permissions.md)）；
  - Sparkle 更新（[IF packaging#L72](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/packaging-and-lifecycle-integration.md#L64-L73)）；
  - sky 自带 `computer-use-telemetry.js` 并依赖 `@statsig/js-client`，是否上传没有确认（[buYoung#L361](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/01-codex-runtime-bridge.md#L361)）。
- **离线可用性**：模型在云端，所以 CU 不能离线使用。去掉路由变量并设 `NODE_REPL_DISABLE_ANALYTICS=1` 后，社区作者轮询未观察到网络连接（不是抓包）。「作者实测」[MC adr/0002](https://github.com/mcdp-adk/pi-codex-computer-use/blob/28a90381d2cb706a5316eac239182bec36f34936/docs/adr/0002-depend-on-codex-files-not-the-running-app.md#L11)
- **云端浏览器（ChatGPT Work / Agents API）是另一条链路**：headless Chrome 跑在 OpenAI 的机器上，经 `connector_openai_browser` 调用（[Simon Willison](https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/)；[oss.md](oss.md)）。

## 9. Windows 与 Linux

- **Windows**：
  - helper 为 `@oai/sky/bin/windows/codex-computer-use(-arm64).exe`，用 UI Automation、Windows.Graphics.Capture、SendInput 实现，走换行分隔的 JSON stdio；每个请求的时间预算头 `x-oai-cua-request-budget-ms` 为 10000；物理 Esc 是 kill switch。「作者实测」[ELAI#L1-L160](https://github.com/DITlieD/ELAI-archive/blob/26bf2bc72d030a2d5ec022f04e1f9603bb285ae1/workflow/reasoning/codex-computer-use-RE-2026-07-12.md#L1-L160)
  - API 是 window2 风格：`list_windows`、`get_window_state({include_screenshot, include_text})`。WinForms 和控制台窗口不出现在列表中。「作者实测」[MC runtime-behavior.md#L21-L52](https://github.com/mcdp-adk/pi-codex-computer-use/blob/28a90381d2cb706a5316eac239182bec36f34936/docs/runtime-behavior.md#L21-L52)
  - 推论：Windows 版是 UIA 树优先（对应 macOS 的 AX），同样不是纯视觉（依据同上）。
- **Linux**：官方 26.901 包里有 Linux 版 `@oai/sky` 二进制，但只暴露像素、没有 AX 编号，官方文档也没有宣称支持。「作者实测」[OS harness-friction.md#L1863-L1868](https://github.com/tanishqkancharla/opensky/blob/54f1d13fe569031c745eebe10ee3f021cf15332f/docs/harness-friction.md#L1863-L1868)

## 10. 社区包清单（详细评级）

| 包 | 做法 | 可信度 |
|---|---|---|
| [browserjack@0.3.1](https://www.npmjs.com/package/browserjack/v/0.3.1) | 用 `codex sandbox` 运行官方 `node_repl`，加 stdio MCP 代理；Chrome/Helium 走 `browser-client.mjs` | 代码扎实，本仓库已核对 |
| [codex-computer-use-mcp@0.6.1](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1) | 零模型 app-server broker，暴露 10 个工具 | 代码扎实，本仓库已核对 |
| [@buyong/pi-codex-computer-use@0.1.2](https://www.npmjs.com/package/@buyong/pi-codex-computer-use/v/0.1.2) | 复刻 Codex 宿主，驱动 `cua_repl` | 代码加最新最细的文档 |
| [opencode-codex-control@0.1.0](https://www.npmjs.com/package/opencode-codex-control/v/0.1.0) | 把 sky 和 browser-client 编译成类型化工具 | 代码，本仓库已核对 |
| [claude-codex-computer-use@0.1.2](https://www.npmjs.com/package/claude-codex-computer-use/v/0.1.2) | 已签名的 `codex sandbox` 当 parent | 代码 |
| [@mcdp-adk/pi-codex-computer-use@0.1.2](https://www.npmjs.com/package/@mcdp-adk/pi-codex-computer-use/v/0.1.2) | Windows 版 `node_repl` 加 sky | 代码加实测文档 |
| [open-computer-use@1.1.0](https://www.npmjs.com/package/open-computer-use/v/1.1.0) | iFurySt 的开源重写，提供三平台二进制 | 不含官方二进制；仓库中的逆向文档最系统 |
| [cursor-motion@0.2.3](https://www.npmjs.com/package/cursor-motion/v/0.2.3) | 光标运动模型的 JS 移植 | 继承 iFurySt 的二手结论 |
| [computer-use-ultra@0.3.0](https://www.npmjs.com/package/computer-use-ultra/v/0.3.0) | 把 AX 动作空间发给外部规划器 | 与 Codex 内部关系弱 |
| [codex-to-claude@1.1.0](https://www.npmjs.com/package/codex-to-claude/v/1.1.0) | 直接拉起 client | 很可能被 launch constraint 杀掉（推论，依据 §5） |
