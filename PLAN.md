# agent-frontier · 规划

## 定位

个人前沿追踪 repo，只服务自己，不做 `awesome-*` 式公开清单。核心方向：

| 优先级 | Topic | 关注点 |
|---|---|---|
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
- [ ] DeepMind blog、blog.google、Google Research、Thinking Machines 的官方 RSS（已占位，`enabled: false`；需在可直连的环境验证后打开）
- [ ] Meta（research.meta.ai，镜像 07-27 后停更）、Qwen、DeepSeek、Kimi 等无 RSS 站点：scrape 配置，或监控官方 GitHub 仓库的提交（`git clone` 在本环境可用）
- [ ] Benchmark leaderboard 定期快照（OSWorld-Verified / 2.0、Terminal-Bench 4、DeepSWE、BrowseComp）→ topic 页 SOTA 表
- [ ] daily digest 推送到 Slack / 邮件

## 每周例行（~20 分钟）

1. 打开最新 `digests/weekly/`，把值得留的条目挪进对应 `topics/*.md`，写一句 takeaway
2. benchmark 有新 SOTA 就更新 topic 页的表
3. 深读的论文在 `notes/` 建一篇（模板 `notes/_template.md`），并 `mark.py <id> noted`

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
