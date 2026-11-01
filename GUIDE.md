# GUIDE.md — 使用指南（写给从没用过的人）

> 这是一个 **AI 编码脚手架**：用 Claude Code 写代码时，它会逼着 AI 先想清楚再动手、
> 全程 TDD、写完自动双轴评审，并且把每一步都记档——AI 再也不会"失忆"。
> 底层 = Trellis 框架（管流程和记忆）+ Matt Pocock 的 31 个工程技能（管代码纪律）。

## 0. 你需要准备什么

| 依赖 | 检查命令 | 没有怎么办 |
|---|---|---|
| Claude Code | 终端里能跑 `claude` | 按 claude.com/code 安装 |
| Node.js ≥ 18 | `node --version` | 官网装 LTS 版 |
| Python 3 | `python3 --version` | macOS 自带 |

## 1. 三分钟开新项目

```bash
# 从本模板复制出一个新项目（把 my-app 换成你的项目路径）
/Volumes/pipi/AITraining/ai-coding-scaffold/scripts/new-project.sh ~/projects/my-app
cd ~/projects/my-app
git init && git add -A && git commit -m "init: scaffold"   # 建议先提交一次
claude   # 启动 Claude Code
```

进去后对 AI 说第一句话：

```
/setup-matt-pocock-skills
```

它会问你三个问题（都选本地文件就行）：
1. **Issue Tracker 用什么？** → 回答 `local files`（新手推荐，票存在 `.scratch/` 下）
2. **Triage 标签用什么？** → 直接回车用默认
3. **AI 文档放哪？** → 回答 `.trellis/spec/`

完事。环境就绪了。

## 2. 日常怎么用：一个完整例子

场景：你要给应用加一个"导出 Excel"功能。

**第 1 步 — 直接用人话提需求：**

> 我想给订单模块加一个导出 Excel 的功能

AI 会先问你要不要建任务（Trellis 流程），回答"要"。然后它**不会马上写代码**，
而是开始"拷问"你（grill-with-docs）：导出哪些字段？超过 10 万行怎么办？
样式有什么要求？——一次只问一个问题，你答到它懂为止。

**第 2 步 — 看它写的文档：**

拷问结束，它会产出 `prd.md`（需求文档）。复杂任务还有 `design.md`（技术设计）和
`implement.md`（执行清单）。**你审查这些文件**，没问题才让它继续。

**第 3 步 — 它开始写代码（自动 TDD）：**

确认后 AI 派出"实现子代理"：先写失败的测试（红），再写最少代码让测试通过（绿），
一个循环一个循环推进。实现完派出"检查子代理"：跑 lint/测试，并从两个独立视角
评审代码（规范轴 + 需求轴）。

**第 4 步 — 收尾（自动）：**

AI 把这次学到的新知识回写到规范（domain-modeling）、提交代码、归档任务、
把本次会话写进工作日志（journal）。下次开会话，AI 读日志和规范就能"记起"一切。

## 3. 常用命令速查

### 流程内（AI 会自动用，你也可以手动点）

| 命令 | 干什么 |
|---|---|
| `/grill-with-docs` | 拷问需求 + 沉淀术语表和架构决策 |
| `/to-spec` | 把对话写成正式规格文档 |
| `/to-tickets` | 把规格拆成可执行的小票 |
| `/implement` | 按规格实现（内部驱动 TDD） |
| `/tdd` | 红绿循环写代码 |
| `/code-review` | 双轴代码评审 |
| `/domain-modeling` | 维护项目术语表、回写规范 |
| `/diagnosing-bugs` | 调试（六阶段纪律循环） |
| `/triage` | 整理 issue，分类定级 |
| `/handoff` | 把当前会话压缩成交接文档 |

### Trellis 流程命令

| 命令 | 干什么 |
|---|---|
| `/trellis:continue` | 继续当前任务（会告诉你卡在哪一步） |
| `/trellis:finish-work` | 收尾：检查、归档、写日志 |
| `python3 .trellis/scripts/task.py list` | 看所有任务 |
| `python3 .trellis/scripts/task.py current` | 看当前任务状态 |

### 救命命令

| 情况 | 办法 |
|---|---|
| AI 在流程里绕不出来 | 对它说 `no-trellis`（本轮回跳过流程提示） |
| AI 反复修同一个 bug | 说 `/trellis-break-loop` 或 `/diagnosing-bugs` |
| 会话太长要换新会话 | 说 `/handoff`，新会话引用生成的文档继续 |
| 不知道该用哪个技能 | 问 `/ask-matt` |
| 我就是要快速改两行 | 说"这是小改动，不用建任务"，AI 会跳过流程 |

## 4. 新手前三次使用的建议

1. **第一次**：拿一个小需求走完全流程（建任务 → 拷问 → 文档 → 实现 → 评审 → 归档），
   感受"AI 先问后做"的节奏，别跳步骤。
2. **第二次**：故意在拷问环节答得含糊，看 AI 怎么追问——这是这套体系最有价值的部分。
3. **第三次**：试一次 `/handoff` 跨会话接续，体验"AI 记得上周说了什么"。

## 5. 它和你直接用 Claude Code 的区别

| | 裸用 Claude Code | 用本脚手架 |
|---|---|---|
| 需求理解 | AI 猜，猜错返工 | 先拷问对齐再动手 |
| 代码质量 | 看运气 | 强制 TDD + 双轴评审 |
| 下次会话 | 从零开始解释项目 | 读 journal + spec + CONTEXT.md 秒懂 |
| 流程 | 靠你自觉 | 每轮提示注入当前该做什么 |
| 知识沉淀 | 散在聊天记录里 | spec / ADR / journal 全留痕 |

## 6. 原理与定制

想改流程、换技能、接 Linear/GitHub Issues，看 `DESIGN.md` 第 3、5 节。
Trellis 官方文档：`.trellis/workflow.md`（流程唯一真相源，AI 每轮都读它）。
