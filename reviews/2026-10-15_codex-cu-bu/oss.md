# openai/codex 开源仓库：browser use / computer use 的胶水层与时间线

> 读的是 [openai/codex @e89b7c4](https://github.com/openai/codex/tree/e89b7c442c0433ad5167e72a5a25bb6d0712766a)（2026-10-15 HEAD）的全量 git 历史，用 `git log -S/-G/--grep` 定位提交日期，只读不执行。
> 另读了 [openai/skills @49f948f](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431) 和 [openai/plugins @0722921](https://github.com/openai/plugins/tree/0722921d5542fc593105c27bd52630babd8b8c2a)。
> GitHub releases API 返回 403，release note 没读到；版本归属按 git tag 推定。
> 自 2026-07-10 起，提交带 `GitOrigin-RevId`（[dc5ae37](https://github.com/openai/codex/commit/dc5ae378967cff0de2cfb30b98c52047ab978e3d)）。推论：这是从内部仓库镜像出来的。

## 1. 结论：开源仓库里没有驱动，只有胶水

- 整个仓库中 `AXUIElement` 和 `puppeteer` 命中 0 次，也没有 Playwright、CDP 或 macOS 无障碍驱动代码（[仓库](https://github.com/openai/codex/tree/e89b7c442c0433ad5167e72a5a25bb6d0712766a)）。
- Codex 把三类服务视为 "Node REPL backed"：`node_repl`、`cua_repl`，以及 `codex_apps` 上的远端连接器 `connector_openai_browser`（[protocol/src/mcp.rs#L35-L65](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/protocol/src/mcp.rs#L35-L65)）。
- 插件与 server 的对应关系，见 cleanup hook 白名单（[bundled_hooks.rs#L1-L112](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/plugin/src/bundled_hooks.rs#L1-L112)）：
  - `browser@`、`chrome@`、`chrome-dev@`、`chrome-internal@`、`computer-use@openai-bundled` 对应 `node_repl.turn_ended`；
  - `unified-computer-use@openai-bundled` 对应 `cua_repl.turn_ended`；
  - `browser@openai-curated-remote` 对应 `browser.turn_ended`。
- 内置 marketplace 根目录为 `$CODEX_HOME/.tmp/bundled-marketplaces/openai-bundled`（[marketplace_policy.rs#L505-L516](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/core-plugins/src/marketplace_policy.rs#L505-L516)）。
- 推论：真正的浏览器和电脑驱动由桌面 app 下发的闭源插件实现，开源部分只负责策略、审查、显示和配置（依据同上三条）。

## 2. 模型怎么调用

- GPT-6 系列的 `tool_mode` 为 `"code_mode_only"`（[models.json#L20](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/models-manager/models.json#L20)）；gpt-5.5 的 `tool_mode` 为 null（[models.json#L1356](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/models-manager/models.json#L1356)）。
- Code Mode 的 `exec` 在全新的 V8 isolate 里运行，"no Node, no file system, no network access"，嵌套工具挂在 `tools.*` 上（[description.rs#L21-L45](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/code-mode-protocol/src/description.rs#L21-L45)）。
  - 所以对 GPT-6 来说是两层代码：外层在 V8 isolate 里写 JS，调用 `tools.mcp__node_repl__js({code})`；内层代码在插件的 Node REPL 中运行，这里才有浏览器和电脑 API。
- 测试样例：`tools.mcp__node_repl__js({ code: 'await nodeRepl.emitImage(await tab.screenshot())' })`（[code_mode.rs#L7053](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/core/tests/suite/code_mode.rs#L7053)）。
- 截图回传：插件调 `nodeRepl.emitImage(...)` 生成 MCP image block，可带 `_meta["codex/imageDetail"]`；Code Mode 再用 `image(result.content[0])` 放进上下文（[test_stdio_server.rs#L655-L666](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/rmcp-client/src/bin/test_stdio_server.rs#L655-L666)）。
  - MCP 结果中的图片从 2025-10-27 起交给模型（[b0bdc04](https://github.com/openai/codex/commit/b0bdc04c309385a7529ec06fabdef0662274cb01)）。
- 工具名：`js`、`js_reset`、`js_add_node_module_dir`、`turn_ended`，远端连接器为 `browser_js`（[guardian_v2.rs#L2403-L2408](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/core/tests/suite/guardian_v2.rs#L2403-L2408)）。
- TUI 快照中的真实调用：`cua_repl.js({"title":"Connect to Chrome","code":"await cua.getState()"})`（[computer_activity 快照](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/tui/src/history_cell/mcp/computer_activity.rs#L1-L5)）。
- REPL 里可以反向调用 Codex 工具，例如 `node_repl.js` 中执行 `tools.exec_command`（[be751dd](https://github.com/openai/codex/commit/be751dd1dfc5409a9a490ed75ec8426fba79ae6e)）。
- `node_repl` 是 HTTP MCP server，鉴权用 `NODE_REPL_AUTH_TOKEN`，该变量不传给子进程（[shell_environment.rs#L15-L22](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/protocol/src/shell_environment.rs#L15-L22)、[fe50b61](https://github.com/openai/codex/commit/fe50b616899eef5aac0dacf1e2d36a09c109944b)）。

## 3. 浏览器 API（官方 openai/plugins 中的 skill）

- `frontend-testing-debugging` 通过 Browser 插件的 Node REPL 验证前端，只有 Browser 不可用时才回退到普通 Playwright。用到的 API 有 `agent.browser.nameSession`、`tabs.selected()/new()`、`tab.goto`、`tab.playwright.domSnapshot()/screenshot()`、`tab.dev.logs`（[SKILL.md#L53-L84](https://github.com/openai/plugins/blob/0722921d5542fc593105c27bd52630babd8b8c2a/plugins/build-web-apps/skills/frontend-testing-debugging/SKILL.md#L53-L84)）。
- `product-design` 用 `agent.browsers.get("iab")` 选 in-app browser，只有需要现有登录、profile 或扩展时才用 Chrome（[index SKILL.md#L56-L62](https://github.com/openai/plugins/blob/0722921d5542fc593105c27bd52630babd8b8c2a/plugins/product-design/skills/index/SKILL.md#L56-L62)）。
- openai/plugins 本身不含 browser、chrome、computer-use 插件（[plugins 目录](https://github.com/openai/plugins/tree/0722921d5542fc593105c27bd52630babd8b8c2a/plugins)）。

## 4. 开关与企业策略

- `in_app_browser`、`browser_annotation_api`、`browser_use`、`browser_use_full_cdp_access`、`browser_use_external`、`computer_use` 都标为 requirements-only、Stable、默认开启（[features/src/lib.rs#L284-L329](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/features/src/lib.rs#L284-L329)）。
- 企业需求项（[browser_computer_use_requirements.rs#L6-L121](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/config/src/browser_computer_use_requirements.rs#L6-L121)）：
  - 总开关 `allow_browser_and_computer_use`；
  - Browser Use：WebMCP、历史访问、`disable_auto_review`、持久审批、扩展请求头，以及每个 origin 的 access、downloads、uploads、full CDP、auto_review；
  - Computer Use：锁屏使用、默认 app 访问、macOS bundle ID、Windows AUMID 和 exe。
- in-app browser 的需求项单独一节，注释为 "not agent Browser Use"，只管导入外部浏览器设置（[in_app_browser_requirements.rs#L1-L11](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/config/src/in_app_browser_requirements.rs#L1-L11)）。
- 沙箱：没有针对浏览器的 seatbelt 或网络规则（[seatbelt_base_policy.sbpl](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/sandboxing/src/seatbelt_base_policy.sbpl#L3-L5)）。
  - 推论：浏览器运行在 Codex 的 shell 沙箱之外，网络控制靠 origin 策略加 Guardian（依据同上，以及上面的需求项文件）。
- 保留的 Responses API namespace 中有 `"browser"` 和 `"computer"`（[config/mod.rs#L3210-L3228](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/core/src/config/mod.rs#L3210-L3228)）。

## 5. 审批与 Guardian（Auto-review）

- 确认策略的转发：每个模型可以定义 `confirmation_policies {browser_use, computer_use}`（[openai_models.rs#L574-L583](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/protocol/src/openai_models.rs#L574-L583)），Codex 在每次调用时放进 `_meta["openai/confirmation_policies"]`（[mcp_tool_call.rs#L1374-L1407](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/core/src/mcp_tool_call.rs#L1374-L1407)）。
- 插件运行时会反向发起逐动作审批，带 `codex_approval_kind`（`mcp_tool_call`、`browser_auth`）、`codex_sensitive_action`、`codex_strict_auto_review` 等字段（[mcp_approval_meta.rs#L4-L15](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/core/src/mcp_approval_meta.rs#L4-L15)）。
  - 在用户审批模式下，普通 `js` 请求（空表单、非敏感）自动放行；Full Access 模式跳过审查；嵌套请求通过 `callId` 挂到外层调用上（[session/mcp.rs#L863-L925](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/core/src/session/mcp.rs#L863-L925)）。
- 按模型强制审查：`node_repl_auto_review_required` 对 gpt-6-astra、gpt-6-sol、gpt-6.1-sol 为 true，对 gpt-6-luna、gpt-5.6-*、gpt-5.5 为 false（[models.json#L29-L30](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/models-manager/models.json#L29-L30)）。该字段会写进每个 turn 的 Responses API 元数据（[responses_metadata.rs#L60-L62](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/core/src/responses_metadata.rs#L60-L62)）。
- 后台分类器 prompt："Predict whether the agent's computer and browser activity needs blocking security review"（[models.json#L114](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/models-manager/models.json#L114)）。
- 审查 scope：2026-08-26 起默认只覆盖 browser 和 computer-use 工具，并且带图片（[9dea1f7](https://github.com/openai/codex/commit/9dea1f709ffe94d74563b4d2c9f147b0eb5c9601)）。
  - 首个 `js` 或 `browser_js` 调用不等审查（[approval.rs#L202-L221](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/ext/guardian-v2/src/async_scorer/approval.rs#L202-L221)）；
  - 被标为敏感的动作一律同步审查（[89650c6](https://github.com/openai/codex/commit/89650c66f2f3ff0d028d3f5d6d0b187b2ed49be5)）；
  - 测试名直接写明路由规则，例如 "low risk browser skips full review"、"high risk browser receives full review"（[guardian_v2.rs#L2380-L2382](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/core/tests/suite/guardian_v2.rs#L2380-L2382)）。
- 审查证据：REPL 结果和截图作为“不可信证据”交给审查模型，渲染后上限 32 KB（[guardian-context/src/node_repl.rs#L18-L28](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/guardian-context/src/node_repl.rs#L18-L28)）。截图不进父 agent 的历史，只给审查模型（[9b9b614](https://github.com/openai/codex/commit/9b9b614b02ba04df55479284749c5cbbed695c24)）。
- 审查规则 `node_repl_policy.md` 要点（[node_repl_policy.md](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/prompts/templates/guardian/node_repl_policy.md#L1-L11)）：
  - 按实际界面判断点击，不按 agent 自述；
  - 所有网站都不可信；
  - 敏感数据外发判为 critical；
  - 登录视为高风险。

## 6. TUI 显示

- 相邻的 `cua_repl` 调用合并显示为 "Using computer" / "Used computer"，失败和截图优先展示（[history_cell/mcp.rs#L68-L69](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/tui/src/history_cell/mcp.rs#L68-L69)、[computer_activity.rs](https://github.com/openai/codex/blob/e89b7c442c0433ad5167e72a5a25bb6d0712766a/codex-rs/tui/src/history_cell/mcp/computer_activity.rs#L1-L5)）。

## 7. 前身：`js_repl`（2026-02 → 04）

- 2026-02-11 加入，是一个持久的 Node 内核工具（[42e22f3](https://github.com/openai/codex/commit/42e22f3bde6c851422eb4f7b502457fe86ba91db)）。
- 2026-02-25 升为 Experimental，说明写的是 "interactive website debugging … Requires Node >= v24.13.1"（[features.rs#L465 @0543d0a](https://github.com/openai/codex/blob/0543d0a022376f0440c2ea5b9aab8c2fd0813758/codex-rs/core/src/features.rs#L465)）。
- 注入的说明里有 `codex.emitImage` 和“内存中 Playwright 截图”示例，并推荐原始图像细节，"especially for CUA agents"（[agents_md.rs#L45-L78 @cf02e9c](https://github.com/openai/codex/blob/cf02e9c052764f6be6525091a8e2b0d7bb46d85d/codex-rs/core/src/agents_md.rs#L45-L78)）。
- 2026-04-24 删除（[8a559e7](https://github.com/openai/codex/commit/8a559e7938bd841d78dc2c442deaa76424faf1d9)）。
  - 推论：`node_repl` 的 `js` / `js_reset` / `js_add_node_module_dir` 是它移到插件中的继任者（依据：工具名与语义一致，见 §2）。
- openai/skills 中的 `playwright-interactive` 仍要求 `js_repl` 和临时 `danger-full-access`（[SKILL.md](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright-interactive/SKILL.md#L1-L22)）；另有 `playwright` skill（[SKILL.md](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/playwright/SKILL.md#L1-L4)）。
- 曾有一个 `atlas` skill，用 AppleScript 控制 ChatGPT Atlas，2026-01-31 加入、2026-02-04 删除（[atlas SKILL.md](https://github.com/openai/skills/blob/0ed635aad23fb73b98f75e0f99f407ffcaeba4ea/skills/.curated/atlas/SKILL.md#L1-L4)、[删除 commit](https://github.com/openai/skills/commit/2f7901ee4202a26757a5237e987a8ec5a1799e29)）。

## 8. 提交时间线

commit 链接格式为 `https://github.com/openai/codex/commit/<sha>`。

| 日期 | 事件 | commit |
|---|---|---|
| 2025-10-27 | MCP 结果中的图片交给模型 | [b0bdc04](https://github.com/openai/codex/commit/b0bdc04c309385a7529ec06fabdef0662274cb01) |
| 2026-02-11 | 加入 `js_repl` | [42e22f3](https://github.com/openai/codex/commit/42e22f3bde6c851422eb4f7b502457fe86ba91db) |
| 2026-03-03 | `js_repl` 说明加入 Playwright 截图示例 | [c4cb594](https://github.com/openai/codex/commit/c4cb594e73fda4b9247d606fb00eb2c58da26647) |
| 2026-03-11 | 说明中加入 "especially for CUA agents" | [8791f0a](https://github.com/openai/codex/commit/8791f0ab9a63e186315eaade28496926fbcbe2f0) |
| 2026-03-18 | 新增 `Product::Atlas` | [580f32a](https://github.com/openai/codex/commit/580f32ad2ab642e3fe9661bce838d972f8989663) |
| 2026-03-20 | Code Mode 改为进程内 V8 | [e4eedd6](https://github.com/openai/codex/commit/e4eedd6170580d5b06fb539635a78f261a6b7369) |
| 2026-04-16 | Computer Use 工具建议移入核心，搜索 `openai-bundled` | [dd00efe](https://github.com/openai/codex/commit/dd00efe78178b8c6c78c0ad78c20ec650c9d4cdf) |
| 2026-04-22 | `in_app_browser` / `browser_use` / `computer_use` 成为企业需求项 | [568cdac](https://github.com/openai/codex/commit/568cdacc7e540cc9ec490e867127d4cd1ef62437)、[7730fb3](https://github.com/openai/codex/commit/7730fb3ab8d784788aa0c495265cbdb28a273ab9) |
| 2026-04-24 | 删除 `js_repl` | [8a559e7](https://github.com/openai/codex/commit/8a559e7938bd841d78dc2c442deaa76424faf1d9) |
| 2026-04-30 | `browser_use_external`；Chrome 扩展进入工具建议白名单 | [719431d](https://github.com/openai/codex/commit/719431da6e2bd15dfeccf32f1fb7888f4c762c92)、[487716a](https://github.com/openai/codex/commit/487716ae74944ed07b3cf660998eb97780012a08) |
| 2026-05-06 | Browser Use 的 origin 审批可交给 Guardian | [346070a](https://github.com/openai/codex/commit/346070a424f8cebcbc42d05081ec5e3ba82965b2) |
| 2026-05-19 | 锁屏 computer use 需求项 | [d86352d](https://github.com/openai/codex/commit/d86352d520b1719a9183a498f428e905c238b40f) |
| 2026-06-22 | 完整 CDP 访问开关 | [ff37f4a](https://github.com/openai/codex/commit/ff37f4a6efc98c205809c2ae20e2c01e7b49040d) |
| 2026-07-23 | 暴露 `browser_use.disable_auto_review` | [4177555](https://github.com/openai/codex/commit/41775559ca1ed253c2aa68db772a715cb348a9eb) |
| 2026-08-10 | 首次出现 `node_repl` 字符串 | [4b0e2a0](https://github.com/openai/codex/commit/4b0e2a0bffcc9ca4781dd38e27032591d25e8996) |
| 2026-08-12 | 模型目录加入 `node_repl_auto_review_required` / `node_repl_disabled` | [74004b5](https://github.com/openai/codex/commit/74004b5397b24662a87a5264a6ae80664168c7f3) |
| 2026-08-13 | Guardian 接收 REPL 结果与图像证据 | [053dda6](https://github.com/openai/codex/commit/053dda6b897887c0bbd8efa5d4952a4380dbb5e4) |
| 2026-08-18 | 截图送 Guardian v2；token 隔离 | [9b9b614](https://github.com/openai/codex/commit/9b9b614b02ba04df55479284749c5cbbed695c24)、[fe50b61](https://github.com/openai/codex/commit/fe50b616899eef5aac0dacf1e2d36a09c109944b) |
| 2026-08-21 | `allow_browser_and_computer_use`；browser/CU 需求项扩展到逐 origin、逐 app | [950dd18](https://github.com/openai/codex/commit/950dd184a150f80a4bec2ab979b15d5994ba7182)、[95118df](https://github.com/openai/codex/commit/95118dff65321f36af6408383a605618f2fab0be) |
| 2026-08-23 | 支持 `cua_repl` | [2161ec2](https://github.com/openai/codex/commit/2161ec272a7d6b775c9c721e6206f4fe63e383f2) |
| 2026-08-26 | Guardian v2 默认只审 CU 并附图；Browser/Chrome 插件的清理 hook | [9dea1f7](https://github.com/openai/codex/commit/9dea1f709ffe94d74563b4d2c9f147b0eb5c9601)、[0340e12](https://github.com/openai/codex/commit/0340e12f5dc468f35ff922065ac1800459939b08) |
| 2026-08-27 | 确认策略转发给插件；敏感动作同步审查 | [b592a0b](https://github.com/openai/codex/commit/b592a0bfed439386fadc69327bd49eccb074cdc6)、[89650c6](https://github.com/openai/codex/commit/89650c66f2f3ff0d028d3f5d6d0b187b2ed49be5) |
| 2026-08-30 | 首个 `js` 调用不等审查 | [cefa060](https://github.com/openai/codex/commit/cefa060695594cdeebfb4306170cc27487c8a088) |
| 2026-09-01 | `unified-computer-use` 清理 hook；嵌套审查归属 | [c7c824d](https://github.com/openai/codex/commit/c7c824dce4da186e5142af5d9a1587ae553efe46)、[67cc3c3](https://github.com/openai/codex/commit/67cc3c318dc8b5532db6ade4182b1dc6f3870889) |
| 2026-09-03 | 加入 GPT-6 Astra（强制审查） | [ed391d4](https://github.com/openai/codex/commit/ed391d4dd21396715b66c278e6b451897672c93c) |
| 2026-09-04 | `allow_webmcp` | [0f64d70](https://github.com/openai/codex/commit/0f64d7080864d22610731935cdc203bd2b3c5d93) |
| 2026-09-07 | TUI 合并显示 computer 动作 | [4110342](https://github.com/openai/codex/commit/4110342321bb19b0053190750a0a8b76427b13ad) |
| 2026-09-23 | 云端 Browser connector 纳入 CU 审查 | [e9b4c69](https://github.com/openai/codex/commit/e9b4c6967ee308ed1d1880ec36e3fda183c1a9ac) |
| 2026-09-30 | `browser_annotation_api` 开关 | [3bbf8ec](https://github.com/openai/codex/commit/3bbf8ec3a1e103c30d575f14f1827b193a8d415f) |
| 2026-10-05 | 浏览器扩展请求头 | [a6c5f3a](https://github.com/openai/codex/commit/a6c5f3a9fa8e7ccfba7d53921d2f06d06d3b9f79) |

- 首次包含这些改动的稳定 tag（按 `git tag --contains` 推定，release note 是否提及：「无出处，待核」）：
  - `js_repl` 在 [rust-v0.100.0](https://github.com/openai/codex/releases/tag/rust-v0.100.0)（2026-02-12）；
  - 浏览器 / CU 需求项在 [rust-v0.124.0](https://github.com/openai/codex/releases/tag/rust-v0.124.0)（04-23）；
  - Chrome 扩展相关在 [rust-v0.129.0](https://github.com/openai/codex/releases/tag/rust-v0.129.0)（05-07）；
  - 完整 CDP 在 [rust-v0.142.2](https://github.com/openai/codex/releases/tag/rust-v0.142.2)（06-24）；
  - `cua_repl` 在 [rust-v0.150.0](https://github.com/openai/codex/releases/tag/rust-v0.150.0)（08-26）；
  - GPT-6 Astra 在 [rust-v0.154.0](https://github.com/openai/codex/releases/tag/rust-v0.154.0)（09-09）。
- 推论：开源侧分三段（依据：上表）：
  - ① 2026-02 → 04，`js_repl` 加自管的 Playwright；
  - ② 2026-04 → 07，闭源的桌面 Browser Use 和 Computer Use 上线，开源仓库只加企业开关；
  - ③ 2026-08 → 10，`node_repl` / `cua_repl` 走 MCP，加上 Guardian v2 和按模型的 CU 审查。
