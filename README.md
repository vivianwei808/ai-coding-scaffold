# ai-coding-scaffold

**AI 编码脚手架**：Trellis 流程骨架 + Matt Pocock 工程纪律。开箱即用，复制成新项目，你的 AI 编码从"凭感觉写"变成"先对齐、再 TDD、双轴评审、全程留痕"。

## 它解决什么

用 Claude Code 写代码的两个高频痛点，各由一层解决：

| 痛点 | 解法 |
|---|---|
| AI 写的代码质量失控：不对齐就动手、没测试、架构越写越乱 | **纪律层**：Matt Pocock 31 个工程技能——拷问式对齐、TDD 红绿循环、双轴代码评审、领域建模 |
| AI 每次会话都失忆：架构、规范、上周的决策全忘 | **管理层**：Trellis v0.6.17——任务状态机、分层规范、会话日志自动记录、每轮流程提示注入 |

## 快速开始

```bash
git clone https://github.com/vivianwei808/ai-coding-scaffold.git
cd ai-coding-scaffold

# 从模板复制出一个新项目
./scripts/new-project.sh ~/projects/my-app
cd ~/projects/my-app
git init && git add -A && git commit -m "init: from scaffold"

claude   # 启动 Claude Code
```

进去后说 `/setup-matt-pocock-skills`（三个问题选 local files / 默认即可），然后直接用人话提需求。零基础 walkthrough 见 [GUIDE.md](GUIDE.md)。

## 一次任务的生命周期

```
你说需求 → AI 询问是否建任务（task.py create）
        → /grill-with-docs 拷问对齐：一次一问，产出 prd.md + CONTEXT.md 术语表 + ADR
        → 你审查文档 → task.py start
        → trellis-implement 子代理：/tdd 红绿循环实现（禁 git）
        → trellis-check 子代理：lint/typecheck/test + 双轴评审（规范轴 + 需求轴）
        → /domain-modeling 回写规范 → commit → 归档 → journal 自动记录会话
```

下一场会话，AI 读 journal 和 spec 接着干，不用重新解释项目。

## 技能构成（37 个）

- **Matt Pocock 纪律层 × 31**（中文译版 v1.3.1）：grill-with-docs、to-spec、to-tickets、implement、tdd、code-review、domain-modeling、diagnosing-bugs、wayfinder、triage、research、handoff、teach、wizard……
- **Trellis 基建 × 6**（Matt 无对应物，保留）：before-dev（inline 平台 spec 加载）、check（lint/test 执行器）、session-insight（历史检索）、meta（框架管理）、channel（多代理运行时）、spec-bootstrap（代码库→spec 引导）

原生 trellis-brainstorm / update-spec / break-loop 已分别替换为 grill-with-docs / domain-modeling / diagnosing-bugs，完整替换映射与取舍理由见 [DESIGN.md](DESIGN.md)。

## 目录速览

```
.trellis/          工作流唯一真相源 + 任务/规范/日志（管理层）
.claude/skills/    37 个技能位
.claude/agents/    实现/检查子代理（已注入 TDD 与双轴评审纪律）
scripts/new-project.sh        从本模板建新项目
scripts/apply-matt-rewire.py  trellis update 升级后一键重挂 Matt 引用（幂等）
DESIGN.md          架构设计：替换映射、数据流、取舍
GUIDE.md           零基础使用指南
```

## 升级

```bash
npx @mindfoldhq/trellis update      # 升级 Trellis 模板（会覆盖 workflow/hooks/agents）
python3 scripts/apply-matt-rewire.py  # 重挂 Matt 技能引用与纪律注入，幂等可重复
```

## 依赖

Claude Code、Node.js ≥ 18、Python 3、rsync。Trellis CLI（`npm i -g @mindfoldhq/trellis`）仅 session-insight 与 channel 功能需要。

## 致谢与许可

- [Trellis](https://github.com/mindfoldhq/trellis)（@mindfoldhq/trellis，AGPL-3.0）：`.trellis/` 目录与 trellis-* 模板文件来自它
- [mattpocock/skills](https://github.com/mattpocock/skills)（MIT）：31 个工程技能，采用 [forge-ai](https://github.com/vivianwei808/forge-ai) 维护的中文译版 v1.3.1
- 本仓库自有文件（README / DESIGN / GUIDE / scripts）：使用时请保留署名
