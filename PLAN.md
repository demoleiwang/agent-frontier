# agent-frontier · 规划

## 定位

个人前沿追踪 repo，只服务自己，不做 `awesome-*` 式公开清单。核心方向：

| 优先级 | Topic | 关注点 |
|---|---|---|
| P0（当前主线） | `personal-agent` | Muse 级个人 agent：自带电脑、常驻、记忆、主动性、多设备、数字人环境 |
| P0（当前主线） | `code-computer-use` | 写代码操作电脑、GUI 与代码 / 命令行的路由 |
| P0（当前焦点） | `env-construction` | 环境形态（真实应用 / mock / 模拟 / 真机）、状态与基础设施、任务合成、verifier 与 rubric、数据准备、隔离 |
| P0（当前焦点） | `office-agent` | 办公套件与企业 SaaS（邮件、日历、IM、工单、CRM / ERP） |
| P0（当前焦点） | `professional-agent` | 工程、科学软件、金融、医疗、法务、数据与 BI |
| P0 | `browser-use-agent` | Web agent / deep research；WebArena、Online-Mind2Web、BrowseComp、WebVoyager |
| P0 | `computer-use-agent` | GUI / desktop / mobile agent；OSWorld、AndroidWorld、ScreenSpot；GUI grounding |
| P0 | `agentic-rl` | 多轮/长程 RL、环境构建与扩展、异步 RL 基础设施、reward 设计 |
| P1 | `gui-agent-search` | agentic search、检索型 agent |
| P1 | `agent-eval-safety` | agent 评测可复现性、reward hacking、沙箱逃逸、安全事件 |
| P2 | `agent-infra` | harness、memory、MCP、tool calling、本地 agent 模型（降权 0.5，避免淹没 P0） |

以后若想公开，可从 `topics/` 拆出 `awesome-browser-use-agent`、`awesome-computer-use-agent`，主 repo 保持个人用途。

## 组织原则

按数据生命周期分层，不按来源分；topic 用 tag 表达，不建目录。

| 层 | 位置 | 产生方式 | 价值 |
|---|---|---|---|
| raw | `data/items/YYYY/MM/YYYY-MM-DD.jsonl` | `fetch.py` 自动抓，按发布日期分文件，id 去重 | 可再生 |
| digest | `digests/{daily,weekly,sources}/`、`README.md` | `render.py` 自动生成 | 可再生 |
| curated | `topics/*.md`、`notes/*.md`、`reviews/*.md` | 人工维护 | **长期价值所在** |

raw item 字段：`id, source, title, url, date, authors, source_tags, tags, excerpt, topics, score, tldr, tldr_source(extract|llm|manual), status, note`。
`status` 依次为 `new → skimmed → read → noted`，即阅读队列；用 `python scripts/mark.py <id> <status> [--tldr ..] [--note ..]` 更新，手写字段不会被自动流程覆盖。

## 分阶段计划

### Phase 1 · HF blog 跑通闭环（✅ 本次完成）

- [x] repo 骨架、`config/sources.yaml`、`config/topics.yaml`
- [x] `fetch.py`：HF blog 走 GitHub 源码仓库 `huggingface/blog`（`_blog.yml` 索引 + 每篇 frontmatter，比 RSS 多出官方 tags 和作者），失败时回退官方 RSS
- [x] `classify.py`：关键词打 topic + 分数（title > 官方 tag > 正文），抽取式 tldr
- [x] `render.py`：daily / weekly / per-source tracker / README（highlights + 阅读队列 + topic 索引）
- [x] 回填 2026-07-01 起 35 篇，13 篇 agent 相关手写中文 tldr，汇总见 [reviews/2026-10-14_hf-blog.md](reviews/2026-10-14_hf-blog.md)
- [x] GitHub Actions 每天 UTC 01:00（新加坡 09:00）自动跑

### Phase 2 · 论文源 + 口碑排序

- [x] `hf-daily-papers`：HF Daily Papers 经 GitHub 镜像接入（主源 Senmo996/hugginggface_daily_paper 带机构标注，备源 joe-nv/hf_paper_watch_dog），带点赞数、机构、代码仓库
- [x] `arxiv-listing`：arXiv cs.AI / cs.CL 经 UNIkeEN/arxiv-daily-server 镜像接入。仅含主分类、非全量，只保留命中关注 topic 的条目，读取 comment 中的录用信息
- [x] 统一 id 为 `arxiv:<id>`，跨源合并信号（`sources` 字段）
- [x] **口碑分 rep**（`config/reputation.yaml`）：HF 点赞（log 缩放）、机构分级、作者关注名单、顶会录用、开源代码，与 topic 相关度分开计算，并给出可读理由
- [x] `requires_any`：泛 RL 词须同时出现 agent 语境，压掉视觉生成类 RL 的误报
- [x] `digests/papers.md`：近 30 天按口碑和相关度排序，含 Must-read 与分 topic 列表；README 增加 Top papers
- [x] 2026-09-14 → 10-14 高口碑论文精读：[reviews/2026-10-14_papers.md](reviews/2026-10-14_papers.md)
- [ ] arXiv 全量（需放行 arxiv.org，或找全量镜像）；Semantic Scholar 引用数作为额外口碑信号（需放行）

### Phase 3 · LLM 精排

- [ ] classify 两级：关键词粗筛命中的才送 LLM，输出 0–1 相关度 + 一句中文 tldr（`tldr_source: llm`）
- [ ] 缓存：按 `id + excerpt hash` 缓存，避免重复花钱
- [ ] `topics.yaml` 增加 `authors:` / `labs:`，命中直接置顶

### Phase 4 · 更多来源 + 推送

- [x] Anthropic news / research / engineering：`scrape` fetcher（listing + sitemap 发现，文章页取真实发布日期，`data/scrape_dates.json` 缓存日期）
- [x] OpenAI（news / research / engineering / developer）、Google Developers AI、Mistral、xAI、Meta AI、UK AISI：经 GitHub 上的 RSS 镜像（Olshansk/rss-feeds）接入。`id_prefix` 合并同一 lab 的多个 feed，`exclude_categories` 去掉客户案例，跨源按 URL 去重
- [x] `digests/labs.md`：各 lab 最近 60 天全部条目（不经 topic 过滤）
- [x] 2026-08-14 → 10-14 前沿 lab 深读汇总：[reviews/2026-10-14_frontier-labs.md](reviews/2026-10-14_frontier-labs.md)，逐篇附录在 [reviews/2026-10-14_frontier-labs/](reviews/2026-10-14_frontier-labs/)
- [x] 办公与专业 agent 的环境构建全景：[reviews/2026-10-14_office-pro-env.md](reviews/2026-10-14_office-pro-env.md)（附录 77 篇精读 + 21 张 lab 卡片），下半年研究提案：[reviews/2026-10-14_research-proposal.md](reviews/2026-10-14_research-proposal.md)
- [ ] DeepMind blog、blog.google、Google Research、Thinking Machines 的官方 RSS（已占位，`enabled: false`；需在可直连的环境验证后打开）
- [ ] Meta（research.meta.ai，镜像 07-27 后停更）、Qwen、DeepSeek、Kimi 等无 RSS 站点：scrape 配置，或监控官方 GitHub 仓库的提交（`git clone` 在本环境可用）
- [ ] Benchmark leaderboard 定期快照（OSWorld-Verified / 2.0、Terminal-Bench 4、DeepSWE、BrowseComp）→ topic 页 SOTA 表
- [ ] daily digest 推送到 Slack / 邮件

## 罗盘网页

- `scripts/build_site.py` 生成 `site/data.json`、`site/index.html`（静态版）和 `site/artifact.html`（发布到 claude.ai 的版本），每天随 daily workflow 自动重建。
- claude.ai 网页会通过查看者的 GitHub 连接器读取 `site/data.json`，所以数据每天自动更新，网页本身不用重发；只有改了 `site/template.html` 才需要重新发布。
- 想用 GitHub Pages：仓库 Settings → Pages → Source 选 “GitHub Actions”，`pages.yml` 会在 main 分支的 `site/` 变化时部署。

## 每周例行（约 20 分钟）

README 分两层：顶部的**研究罗盘**（研究方向雷达、置顶必读、关键信号）来自人工维护的 `config/compass.yaml`；下面的“本周待分拣”、topic 热度、各方向近 14 天的新工作数则每天自动重算。

1. **清空“本周待分拣”**：逐条看完，用 `python scripts/mark.py <id> skimmed --tldr "…"` 标记；值得深读的建 `notes/`，标记为 `noted`
2. **更新罗盘** `config/compass.yaml`：
   - 看 README 中各方向“近 14 天新工作”的数量和条目，判断状态是否改变（空白 → 上升 → 拥挤）；
   - 新发现的研究机会加为新方向，过时的方向删除；
   - 置顶必读控制在 10 条以内，读完的换掉；
   - 关键信号只留仍然成立的，并改 `updated` 日期
3. **沉淀到 topic 页**：把值得长期保留的条目写进 `topics/*.md`；benchmark 有新的 SOTA 时更新表格
4. 每月或遇到大事件时，在 `reviews/` 写一份深度报告；每半年更新一次研究提案（当前：[2026-10-14_research-proposal.md](reviews/2026-10-14_research-proposal.md)），同步 `compass.yaml` 的 `proposals`
5. **方向复盘（M0）**：对照 `config/compass.yaml` 的 `watch` 列表看本周有没有触发信号；更新 `modules` 的状态和下一步；需要修正主方向时，先改 [research-proposal](reviews/2026-10-14_research-proposal.md)，再在 `direction_log` 加一行写明原因和证据
6. 提交前运行 `python scripts/check_evidence.py`：所有论断都要就地附出处 URL（规则见 [CLAUDE.md](CLAUDE.md)）

## 运行

```bash
pip install -r requirements.txt
python scripts/fetch.py --days 14      # 或 --since 2026-07-01 回填
python scripts/classify.py             # --all 重新分类全部
python scripts/render.py
```

## 已知限制

- 本 repo 的云端开发环境网络策略只放行 anthropic.com 和 GitHub（raw 文件、`git clone`）；huggingface.co、openai.com、Google、Meta 等被拦。因此 HF blog 走 `huggingface/blog` 仓库，其他 lab 走 GitHub 上的 RSS 镜像，正文深读靠 lab 的官方 GitHub 仓库加官方域名搜索。GitHub Actions runner 无此限制，可换回官方 RSS。
- RSS 镜像的日期偶有错误，例如 OpenAI 的 *Why we built the Responses API* 被标成 2026-09-22，实为 2025 年旧文。
- HF 社区博客（`huggingface.co/blog/<user>/<slug>`）不在 `huggingface/blog` 仓库里，暂未覆盖。
