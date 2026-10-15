# 附录索引：Codex 的 computer use 与 browser use

> 主报告见 [../2026-10-15_codex-cu-bu.md](../2026-10-15_codex-cu-bu.md)。

| 文件 | 内容 | 证据深度 |
|---|---|---|
| [own-re.md](own-re.md) | 本仓库自己的逆向：Codex CLI 0.162.1 二进制 strings、提取的确认策略、Homebrew cask 痕迹、Chrome skill 原文 | npm tarball 全量检索（[@openai/codex](https://www.npmjs.com/package/@openai/codex)）+ [Homebrew cask](https://github.com/Homebrew/homebrew-cask) + [gist](https://gist.github.com/wong2/fec0b7239ce2c264ccaece96071578be) 全文 |
| [oss.md](oss.md) | openai/codex 开源代码中的胶水层、审批与 Guardian、`js_repl` 前身、40 条提交时间线 | GitHub 全文（[openai/codex @e89b7c4](https://github.com/openai/codex/tree/e89b7c442c0433ad5167e72a5a25bb6d0712766a)） |
| [community-re.md](community-re.md) | 社区逆向汇总：安装布局、三代接口、AX/截图、后台点击、IPC、浏览器三后端、安全层、本地与云端、Windows/Linux | 25 个 npm 包 tarball + 20 多个 GitHub 仓库（如 [iFurySt](https://github.com/iFurySt/open-codex-computer-use)、[hqhq1025](https://github.com/hqhq1025/codex-computer-use-lab)、[buYoung](https://github.com/buYoung/pi-codex-auto-review)）+ 泄露合集 |
| [experts.md](experts.md) | 官方产品时间线、Simon Willison、MacStories、trycua 等人的拆解，以及矛盾裁决 | Simon Willison 博客全文（[backup](https://github.com/simonw/simonwillisonblog-backup)）+ 官方搜索摘录 + 二手 |
