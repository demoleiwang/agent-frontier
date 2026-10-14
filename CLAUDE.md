# agent-frontier · 工作约定

个人前沿追踪仓库：Muse 级个人 agent 的练习场与训练（主线）、写代码操作电脑、办公 / 专业领域 agent 及其环境构建、computer/browser-use agent、agentic RL、agent 评测与安全。结构与流程见 [PLAN.md](PLAN.md)；主方向与模块拆解见 `config/compass.yaml` 和 `reviews/*research-proposal.md`。
- 本仓库对安全话题只在影响设计时顺带记录，不作为主线。

## 证据规则（必须遵守）

- **所有论断都要就地附出处 URL**，特别是 `reviews/`、`topics/`、`notes/` 下的 md，以及 `config/compass.yaml`（README 顶部由它渲染）。
  - 最小单位是一个列表项、一行表格或一段文字；数字、比较、趋势判断都算论断。
  - 用最具体的原始出处：arXiv abs、官方博文、GitHub 文件或 commit。不要用我们自己的报告代替原始出处。
  - 只来自搜索摘要或二手聚合站的，链接那个页面并标“二手”；推论标“推论”，并链接所依据的证据。
  - 找不到出处的，删掉或标 `「无出处，待核」`。不编造 URL 或数字。
- 逐篇附录（`reviews/<报告名>/` 下）中，卡片标题或卡片开头给出原文 URL 时，卡片内条目可以继承这个出处；综合性文件必须就地引用。
- 提交前运行 `python scripts/check_evidence.py`（`-v` 列出缺出处的行），确保 0 条缺失。
- `scripts/evidence_links.py` 维护“名称 → 原始出处”词典，可以批量给已知实体加链接。批量加完后必须人工核对是否挂错（同名多篇时容易错）。

## 其他约定

- `README.md`、`digests/` 由 `scripts/render.py` 生成，不手改；要改 README 顶部内容，改 `config/compass.yaml`。
- 数字一律视为厂商或作者自报，除非注明已独立复现。
- 本云端环境只能直连 anthropic.com 和 GitHub（raw 文件、`git clone`）；其他站点经 GitHub 镜像或官方域名搜索获取，笔记中要标注来源深度。
