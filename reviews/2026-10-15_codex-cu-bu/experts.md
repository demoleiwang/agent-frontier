# 官方时间线与大牛拆解

> 2026-10-15 整理。openai.com、developers.openai.com 在本环境无法直连，官方内容来自搜索摘录（标 official-search-excerpt）。
> Simon Willison 的文章全文取自他的官方数据库备份 [simonw/simonwillisonblog-backup](https://github.com/simonw/simonwillisonblog-backup)，引用时链接 simonwillison.net 上的原文。
> 其余标注：`二手` 表示第三方报道，`推论` 表示本仓库的推断。

## 1. 官方时间线（产品层）

### 1.1 2025：前身

| 日期 | 事件 | 出处 |
|---|---|---|
| 2025-07-17 | ChatGPT agent 发布，取代 Operator（Operator 于 2025-08-31 下线）；动作空间由浏览器、沙箱终端和文本组成，可在“视觉浏览”和“文本浏览”之间切换 | [OpenAI](https://openai.com/index/introducing-chatgpt-agent/)，official-search-excerpt；[MIT AI Agent Index](https://aiagentindex.mit.edu/2025/chatgpt-agent)，二手 |
| 2025-10-21 | ChatGPT Atlas（Mac）发布。agent 模式 "cannot run code in the browser, download files, or install extensions"，并借助 ARIA 标签理解页面 | [Simon Willison](https://simonwillison.net/2025/Oct/21/introducing-chatgpt-atlas/) |
| 2025-10-23 | OpenAI 收购 Software Applications Inc.（Sky） | [OpenAI](https://openai.com/index/openai-acquires-software-applications-incorporated/)，official-search-excerpt |
| 2025-10-30 | "How we built OWL"：Atlas 把 Chromium 的 browser 进程放在 app 进程之外运行，UI 用原生 SwiftUI/AppKit | [OpenAI](https://openai.com/index/building-chatgpt-atlas)，official-search-excerpt |
| 2025-12-22 | Atlas 防提示注入：用 RL 训练的自动攻击者寻找长程注入，再做对抗训练 | [OpenAI](https://openai.com/index/hardening-atlas-against-prompt-injection)，official-search-excerpt |

### 1.2 2026：Codex 吸收 Sky 与 Atlas

| 日期 | 事件 | 出处 |
|---|---|---|
| 02-02 | Codex app for macOS 发布（Electron 加 Node） | [OpenAI](https://openai.com/index/introducing-the-codex-app/)；[Simon Willison](https://simonwillison.net/2026/Feb/2/introducing-the-codex-app/) |
| 04-16 | "Codex for (almost) everything"：macOS 后台 computer use（自带光标，可多个 agent 并行）、in-app browser、90 多个插件；首发时不含 EEA、英国、瑞士 | [OpenAI](https://openai.com/index/codex-for-almost-everything/)，official-search-excerpt |
| 04-16 | MacStories 实测称它 "literally based on" Sky，走 macOS AX 树 | [MacStories](https://macstories.net/notes/openais-new-codex-app-has-the-best-computer-use-feature-ive-ever-tested/)，二手（搜索摘录，以及 [Michael Tsai 的引用](https://mjtsai.com/blog/2026/04/17/codex-for-almost-everything/)） |
| 04-30 | Auto-review 上线：用独立的审查 agent 代替人做沙箱边界审批，官方称审批中断减少约 200 倍（厂商自报） | [OpenAI Alignment](https://alignment.openai.com/auto-review)，official-search-excerpt |
| 05-07 或 05-08 | Codex Chrome 扩展上线：在用户已登录的 Chrome 中操作（macOS、Windows），后台并行 tab、tab group、按站点授权 | [developers.openai.com](https://developers.openai.com/codex/app/chrome-extension)，official-search-excerpt；[GIGAZINE](https://gigazine.net/gsc_news/en/20260508-codex-chrome)，二手 |
| 05-19 前后 | Appshots，以及锁屏状态下继续 computer use（app 26.519） | [releases.sh](https://releases.sh/release/rel_oTB6ALg9k686yOLzrEJYh-appshots-launch-goal-mode-exits-beta-remote-computer-use-enabled)，二手；需求项 [d86352d](https://github.com/openai/codex/commit/d86352d520b1719a9183a498f428e905c238b40f) |
| 05-29 | Windows 版 computer use 上线（前台运行） | [GIGAZINE](https://gigazine.net/gsc_news/en/20260601-codex-windows-computer-use)，二手 |
| 06-11 或 06-12 | 浏览器 Developer mode（CDP），可做性能分析、看 console 和网络；官方称 browser use "up to 2x faster"（厂商自报） | [OpenAIDevs](https://x.com/OpenAIDevs/status/2065226355495895521)，official-search-excerpt；[TestingCatalog](https://www.testingcatalog.com/icymi-openai-released-cdp-support-for-browser-use-on-codex.md)，二手 |
| 07-09 | Codex app 改名为 ChatGPT 桌面 app，同时发布 ChatGPT Work；Atlas 宣布停止（08-09 下线） | [Simon Willison](https://simonwillison.net/2026/Sep/1/codex-libreoffice/)；[9to5Mac](https://9to5mac.com/2026/07/09/openai-is-discontinuing-chatgpt-atlas-its-standalone-desktop-browser/)，二手；cask 弃用见 [codex-app.rb](https://raw.githubusercontent.com/Homebrew/homebrew-cask/master/Casks/c/codex-app.rb) |
| 08-23 → 09-23 | `cua_repl`、Guardian v2 按模型做 CU 审查；云端 Browser connector 纳入审查 | 见 [oss.md §8](oss.md)，如 [2161ec2](https://github.com/openai/codex/commit/2161ec272a7d6b775c9c721e6206f4fe63e383f2)、[e9b4c69](https://github.com/openai/codex/commit/e9b4c6967ee308ed1d1880ec36e3fda183c1a9ac) |
| 09-29 | Agents API 支持 computer use：agent 在 OpenAI 托管的浏览器中工作 | [changelog](https://developers.openai.com/api/docs/changelog)，official-search-excerpt |

- 推论：OpenAI 用了约 9 个月合并三条线：Sky（桌面 AX 操作）、Atlas（浏览器 agent 运行时）、Codex（代码 harness）。合并后的产品形态是一个桌面 app、一个 REPL（`cua_repl`）、一套 AX 编号动作词表（依据：本表，以及 [wong2 gist 的 `setupAtlasRuntime`](https://gist.github.com/wong2/fec0b7239ce2c264ccaece96071578be)、[`com.openai.sky.CUAService`](https://raw.githubusercontent.com/Homebrew/homebrew-cask/master/Casks/c/chatgpt.rb)）。

## 2. 人物与拆解

### 2.1 Simon Willison

- **2026-08-30 "Understanding ChatGPT Work"**（[原文](https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/)）
  - 方法：让 agent 列出自己的工具和 skill。
  - 结果：共 223 个工具（其中 6 个来自他自己的 MCP server）、44 个 skill。
  - 云端浏览器是完整的 headless Chrome；遇到登录时交还给用户，密码和 2FA 不经过模型。
  - 他实测 `tab.playwright.evaluate` 可以运行。
  - `control-browser` skill 用 `mcp__node_repl__js` 加 `agent.browsers.*`，并要求模型先读 `await browser.documentation()`。他发布了一份拷贝：[codex-tool-reference](https://codex-tool-reference.simonw.chatgpt.site/skills/control-browser)。
  - 观点：Work 同时具备 "lethal trifecta" 的三个条件，他推测 OpenAI 依赖 Auto-review 来兜底，并批评 OpenAI 隐藏系统提示词。
- **2026-09-01**（[原文](https://simonwillison.net/2026/Sep/1/codex-libreoffice/)）
  - 方法：检查磁盘占用。
  - 结果：`~/.cache/codex-runtimes/codex-primary-runtime` 有 1.7 GB，内含 Python、Node、Poppler、git 和 headless LibreOffice。
- **2025-08-04**（[原文](https://simonwillison.net/2025/Aug/4/chatgpt-agents-user-agent/)）
  - 方法：用自建的日志端点抓流量。
  - 结果：ChatGPT agent 伪装成 Chrome 138 macOS 的 UA，但发出的是 `Sec-Ch-Ua-Platform: Linux`；请求按 RFC 9421 签名（`Signature-Agent: https://chatgpt.com`，web-bot-auth，ed25519）。
- **2025-10-21、10-22**：Atlas 的 agent 像 "a first-time computer user"；Watch Mode 在 GitHub 和银行网站上都没有触发（[10-21](https://simonwillison.net/2025/Oct/21/introducing-chatgpt-atlas/)、[10-22](https://simonwillison.net/2025/Oct/22/openai-ciso-on-atlas/)）。
- **没有找到的**：他关于 04 月 CU 发布或 Chrome 扩展的专文。依据是对 backup 中 2025-04 至 2026-10 全部内容的关键词扫描（[backup 仓库](https://github.com/simonw/simonwillisonblog-backup)）。

### 2.2 Federico Viticci（MacStories）

- CU 基于 Sky，读取 AX 树；他对比的是 Claude 的“录屏加 AppleScript”做法（[MacStories](https://macstories.net/notes/openais-new-codex-app-has-the-best-computer-use-feature-ive-ever-tested/)，二手搜索摘录）。
- 会员专文讲到用 Cua Driver 实现“不分地区”的 CU，以及 Appshots（"Skyshots"）（[MacStories Weekly 515](https://www.macstories.net/club/macstories-weekly-issue-515/region-free-computer-use-in-codex-for-mac-with-cua-driver/)，二手）。

### 2.3 Ari Weinstein（前 Shortcuts / Sky 负责人）与 Romain Huet

- 视频中介绍 Sky 技术变成了 Codex Computer Use，"without taking over your Mac"（[Matthew Cassinelli](https://matthewcassinelli.com/shortcuts-lead-ari-weinstein-now-at-openai-talking-computer-use-for-codex/)，二手）。
- Romain Huet：从 GPT-5.4 起，Codex 模型与主模型合一，GPT-5.5 提升了 computer use（[Simon Willison 引述](https://simonwillison.net/2026/Apr/25/romain-huet/)）。

### 2.4 Francesco Bonacci（trycua）

- **2026-04-23** 做了 clean-room 复现（[blog](https://github.com/trycua/cua/blob/b803be65c66a9ad5efeff93f5ff62ffc26b97e3e/blog/inside-macos-window-internals.md)）：
  - 后台点击用私有的 SkyLight `SLEventPostToPid`。Chrome 的 renderer 接受这种事件，拒绝普通 HID 路径来的事件。
  - 聚焦用 yabai 式方法，不抬起窗口。
  - `_AXObserverAddNotificationAndCheckRemote` 让被遮挡的 Electron 窗口仍然保持 AX 树更新。
  - 局限：网页上的右键会被变成左键。
  - 这篇是同类技术的复现，没有拆 Codex 的二进制（推论）。
- 04-22 发布 Cua Driver，距 Codex CU 发布 6 天（[blog](https://github.com/trycua/cua/blob/b803be65c66a9ad5efeff93f5ff62ffc26b97e3e/blog/computer-use-2-ai-engineer-worlds-fair.md)）。
- 08-06：Codex 的 in-app browser 有独立 profile，可选开启完整 CDP；Chrome 扩展覆盖用户的真实 profile（[blog](https://github.com/trycua/cua/blob/b803be65c66a9ad5efeff93f5ff62ffc26b97e3e/blog/extension-free-browser-use.md)）。
- trycua 对比页称 Codex CU 是 "vision-only"（[cua.ai](https://cua.ai/docs/cua-driver/guide/getting-started/comparison)，二手）。这与 AX 证据矛盾，见 §3。

### 2.5 中文和日文社区

- **iola1999（V2EX）**：逆向了 Chrome 扩展、native host 和 socket，见 [community-re.md §6.3](community-re.md)；讨论帖在 [V2EX](https://www.v2ex.com/t/1225724)（二手）。
- **syanbo/codex-cu**：在 26.930 上实测进程链 `cua-repl.mjs → node_repl → SkyComputerUseService`（[repo](https://github.com/syanbo/codex-cu)）。
- **codenote.net**：调用链为 `@oai/cua-repl → @oai/cua → @oai/sky → com.openai.sky.CUAService`，与 trycua 的 cua-driver 没有共享代码（[codenote](https://codenote.net/en/posts/codex-computer-use-cua-repl-vs-trycua-cua-driver/)，二手）。
- **Classmethod**：在 26.609 上用 CDP 观察已登录的 ChatGPT 网页，建议“动作用高层 API，观察用 CDP”（[dev.classmethod.jp](https://dev.classmethod.jp/articles/codex-app-cdp-chatgpt/)，二手）。
- **Qiita**：Windows 的 CU 大概读不了 Chrome，改用 Browser Use 可以（[Qiita](https://qiita.com/Yusg_6/items/59e86b416c2f9dcab07c)，二手）。
- **jxnl**（2026-06-16）对比了 Codex 用电脑的三种方式：Computer Use、Chrome、in-app browser；Windows 上会接管桌面（[blog](https://github.com/jxnl/blog/blob/ea8821f1e7608eacc560aeeef3a012ff2cf5f8b0/docs/writing/posts/three-ways-codex-can-use-a-computer.md#L20-L45)）。

### 2.6 安全研究

- **Johann Rehberger，2025-08-02，ZombAI**：Codex web 的 "Common Dependencies Allowlist" 包含 `azure.net`，任何人都能在 `*.cloudapp.azure.net` 上托管内容（[embracethered](https://embracethered.com/blog/posts/2025/chatgpt-codex-remote-control-zombai/)）。没有找到他 2026 年专门针对 Codex browser 或 CU 的文章（[blog 索引](https://embracethered.com/blog/)，二手）。
- **PromptArmor**："Codex for Everything" 在默认权限模式下可以外泄已连接账户的邮件，2026-04-21 披露并已修复（[PromptArmor](https://www.promptarmor.com/resources/codex-for-everything-exfiltrates-connected-data)，二手）。
- **NeuralTrust、LayerX**：Atlas 的 omnibox 注入，以及 CSRF 写入记忆（[The Hacker News](https://thehackernews.com/2025/10/new-chatgpt-atlas-browser-exploit-lets.html)，二手，严重性未核实）。
- **Zenity Labs** 批评了 Atlas 的加固思路（[Zenity](https://labs.zenity.io/p/hardening-atlas-the-relentless-challenge-of-securing-an-untrusted-browser-agent)，二手）。
- 没有找到专门针对 Chrome 扩展或桌面 CU 的公开红队报告（[Verdent](https://www.verdent.ai/guides/codex-chrome-prompt-injection-protection)，二手，截至 2026-05-09）。

### 2.7 没有找到的

- 约 30 次搜索里，没有找到 Steinberger、Ronacher、Zechner、Huntley、Thorsten Ball、Schirano、Karpathy、swyx/Latent Space 关于 Codex browser 或 CU 的拆解。这只代表没找到，不能证明没有（[Latent Space 2025 年的 Codex 一期](https://www.latent.space/p/chatgpt-codex-the-missing-manual)，二手，讲的是 Codex cloud）。

## 3. 互相矛盾的说法与裁决

1. **纯视觉还是 AX？** trycua 说 vision-only（[cua.ai](https://cua.ai/docs/cua-driver/guide/getting-started/comparison)，二手）；MacStories、工具描述原文和多方实测都显示 AX 树优先、截图辅助（[tools.js](https://www.npmjs.com/package/codex-computer-use-mcp/v/0.6.1)、[IF tool-call-samples](https://github.com/iFurySt/open-codex-computer-use/blob/7d8cb3fa5618d1ed8ec71773434ac3677f1922c9/docs/references/codex-computer-use-reverse-engineering/tool-call-samples-2026-04-17.md#L95-L143)）。
   - 裁决：AX 优先，每次都附截图，`drag` 和 AX 缺失时走坐标。
2. **完整 CDP 是否默认关闭？** 二手报道说默认关、按站点授权（[pasqualepillitteri.it](https://pasqualepillitteri.it/de/news/5091/codex-chrome-devtools-protocol-browser-de)）；源码中的企业开关默认开（[features/src/lib.rs](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/features/src/lib.rs#L284-L329)），但每个站点另有 `full_cdp_access` 的允许或拒绝，运行时审批为 `riskLevel:high`（[buYoung](https://github.com/buYoung/pi-codex-auto-review/blob/83889c6624ffc9363af85f30619da4a57c84fca2/docs/handoffs/computer-use/01-codex-runtime-bridge.md#L152-L167)）。
   - 裁决：两种说法可以同时成立，功能开关开着，具体站点要单独授权。
3. **能否 `evaluate`？** Chrome 扩展的 skill 说不能（[wong2 gist L449](https://gist.github.com/wong2/fec0b7239ce2c264ccaece96071578be)）；云端 Work 浏览器中可以（[Simon Willison](https://simonwillison.net/2026/Aug/30/understanding-chatgpt-work/)）；opencode-codex-control 称 playwright 提供 "read-only page JS"（[chrome.ts](https://github.com/aryasaatvik/opencode-codex-control/blob/461e413785f8dc6119f36da3c52d2e8fb81e4098/src/tools/chrome.ts)）。
   - 裁决：取决于后端、是否开了 Developer mode 以及版本。本地后端默认不给任意 JS，云端或 CDP 模式给。
4. **浏览器交互用 AX 还是 DOM-id？** 08-29 的代码说扩展后端不支持 `ax`（[executor](https://github.com/UsefulSoftwareCo/executor/blob/906bee5efc9b2bfc0d9341cd471a701314136144/packages/plugins/mcp/src/sdk/codex-browser-tools.ts#L1-L30)），09-10 的代码说只剩 `ax` 和 `playwright`（[opencode-codex-control](https://github.com/aryasaatvik/opencode-codex-control/blob/461e413785f8dc6119f36da3c52d2e8fb81e4098/src/tools/chrome.ts)）。
   - 裁决：版本切换，见 [community-re.md §6.5](community-re.md)。
5. **sky 的传输方式**：Apple Events、Unix socket（IPC-2）、XPC（IPC-4）、`computeruse.sock` JSON-RPC 都有人观察到（[community-re.md §5](community-re.md)）。
   - 裁决：几代实现先后替换。
