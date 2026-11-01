# DESIGN.md — AI 编码脚手架设计文档

> 本工程 = **Trellis 骨架（管理层）** + **Matt Pocock Skills（纪律层）** 的融合脚手架。
> Trellis v0.6.17（@mindfoldhq/trellis，AGPL-3.0）提供流程强制与项目管理；
> mattpocock/skills v1.3.1（MIT，中文译版）提供编码纪律。
> 理论依据见「术哥无界」文章《解决 AI 编码两大痛点》第 7 节：两个项目正交互补，可以同时使用。

## 1. 要解决的两个问题

| 痛点 | 层 | 由谁解决 |
|---|---|---|
| AI 写的代码质量失控（不对齐、无测试、架构熵增） | 纪律层 | Matt Pocock Skills：拷问对齐、TDD、双轴评审、深度模块 |
| AI 每次会话失忆（架构、规范、历史全忘） | 管理层 | Trellis：task 状态机、spec 分层、journal 自动记录 |

## 2. 目录结构

```
<project>/
├── .trellis/                    # Trellis 管理层（保留，原样）
│   ├── workflow.md              # 工作流唯一真相源（已改挂 Matt 技能）
│   ├── config.yaml              # 项目配置（journal、hooks、monorepo packages）
│   ├── spec/                    # 分层规范（frontend/backend/guides）
│   ├── tasks/                   # 活跃任务（task.json 状态机 + prd/design/implement.md）
│   ├── workspace/<dev>/         # 每人会话日志（journal-N.md，2000 行轮转）
│   ├── agents/                  # sub-agent 提示词源
│   └── scripts/                 # task.py / get_context.py / add_session.py
├── .claude/
│   ├── skills/                  # 37 个技能 = Matt 31 + Trellis 基建 6
│   │   ├── grill-with-docs/     # ── Matt 纪律层（31 个，中文）
│   │   ├── tdd/  implement/  code-review/  triage/  wayfinder/  ...
│   │   ├── trellis-before-dev/  # ── Trellis 基建（6 个，保留）
│   │   ├── trellis-check/  trellis-session-insight/  ...
│   ├── agents/                  # trellis-implement / trellis-check / trellis-research
│   │                            #   （已注入 TDD 纪律 + 双轴评审）
│   ├── commands/trellis/        # /trellis:continue /trellis:finish-work
│   └── hooks/                   # session-start / workflow-state 注入（框架核心）
├── DESIGN.md                    # 本文档
├── GUIDE.md                     # 使用指南（新手向）
└── scripts/
    ├── new-project.sh           # 从本模板新建项目
    └── apply-matt-rewire.py     # trellis update 后重新应用 Matt 改挂（幂等）
```

## 3. 替换映射表（Trellis 原生 → Matt Pocock）

| Trellis 原生 | 替换为 | 理由 |
|---|---|---|
| `trellis-brainstorm` | **`/grill-with-docs`** | 拷问契约相同（relentless interview、一次一问），Matt 版额外产出 CONTEXT.md 共享语言 + ADR |
| `trellis-update-spec` | **`/domain-modeling`** | 规范回写：挑战术语、边界压测、更新 CONTEXT.md 与 spec |
| `trellis-break-loop` | **`/diagnosing-bugs`** | 反复调试同一问题：六阶段调试纪律循环（反馈循环 → 复现最小化 → 可证伪假设 → 仪器 → 回归测试 → 复盘） |
| implement 环节（文档约定） | **`trellis-implement` agent + `/tdd` 纪律注入** | 保留 Trellis 的约束（禁 git、读 jsonl），注入 Matt 的红绿循环与三反模式 |
| check 环节 | **`trellis-check` agent + `/code-review` 双轴** | 保留 lint/typecheck/test，注入 Standards+Fowler / Spec 双轴评审 |
| （无对应） | `/triage` `/handoff` `/research` 等 | Matt 增益能力，按需使用 |

**保留的 Trellis 基建**（Matt 无对应物，或只覆盖其一部分）：

- `task.py` 状态机（planning → in_progress → archived）与 `tasks/` 目录
- `spec/` 分层规范 + `implement.jsonl` / `check.jsonl` 精确注入
- `workspace/` journal 自动记录（对应 Matt 的 `/handoff`，一个是自动一个是手动，双保险）
- 三个 hooks（session-start、workflow-state 面包屑、sub-agent 上下文注入）
- 六个基建技能：`trellis-before-dev`（inline 平台 spec 加载）、`trellis-check`（lint/typecheck/test 执行器，Matt 的 /code-review 只覆盖其评审维度）、`trellis-session-insight`（历史会话检索，方向与 /handoff 相反）、`trellis-meta`（框架自身管理）、`trellis-channel`（多代理运行时）、`trellis-spec-bootstrap`（代码库 → spec 引导，/to-spec 是对话 → 规格，方向不同）

## 4. 一次典型任务的数据流

```
你：描述需求
  ↓ hook 注入 workflow-state（无任务）→ AI 询问是否建任务
task.py create → status=planning
  ↓ Phase 1（面包屑指示加载 grill-with-docs）
/grill-with-docs 拷问 → prd.md（+复杂任务 design.md/implement.md）+ CONTEXT.md/ADR
  ↓ 你审查产物 → task.py start（status=in_progress）
  ↓ Phase 2（面包屑指示派发子代理）
trellis-implement agent：读 jsonl+prd+design → /tdd 红绿循环实现（禁 git）
trellis-check agent：lint/typecheck/test + 双轴评审（Standards/Spec 分离）
  ↓ Phase 3
/domain-modeling 回写 spec → git commit → /trellis:finish-work 归档
  ↓ task.py archive → journal 自动记录本次会话
```

## 5. 设计取舍

1. **面包屑是融合点**：workflow.md 的 `[workflow-state:*]` 块每轮注入提示词，Matt 技能通过这里被"强制"进入流程——这解决了 Matt 原版"流程靠人记住"的最大短板。
2. **技能用中文译版**（forge-ai mattpocock-skills-zh v1.3.1）：新手可读性优先；要回上游英文版，把 `.claude/skills/` 下同名目录换成官方内容即可。
3. **不删 trellis-research agent**：它与 Matt 的 `/research` 并存——前者是约束化子代理（读 jsonl），后者是轻量后台调研；场景不同。
4. **upstream 升级**：`npx @mindfoldhq/trellis update` 会重刷模板文件（workflow.md、hooks、agents）；Matt 改挂与 TDD/双轴注入可能被覆盖，升级后在新项目目录里重跑 `python3 scripts/apply-matt-rewire.py` 一键恢复（幂等，覆盖 workflow + hooks + commands + agents 五类文件）。

## 6. 已知边界

- Trellis AGPL-3.0：脚手架衍生的 `.trellis/` 部分若分发需遵守 AGPL；公司内部使用不受影响。
- Matt skills 面向 Claude Code；Trellis 17 平台适配里，非 Claude 平台要用 Matt 技能需手动同步 `.claude/skills/` 内容。
