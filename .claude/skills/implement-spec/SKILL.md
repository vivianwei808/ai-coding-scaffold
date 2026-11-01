---
name: implement-spec
description: "将 /to-spec 和 /to-tickets 的产出实现为代码。"
disable-model-invocation: true
---

你已经获得一份 spec。该 spec 应关联一组 tickets，用于说明如何实现它。

Issue 跟踪器应该已经提供。如果没有，请告诉用户运行 `/setup-matt-pocock-skills`。

目标是在单一**集成分支**上完整实现整份 spec，并按照 Issue 跟踪器关闭工作的方式解决每个 ticket。

Tickets 不是步骤清单，而是带阻塞关系的**任务图**。因此，始终会存在一组可以立即领取的 tickets，也就是**前沿（frontier）**。

与子 agent 之间的沟通应尽量精简。主要通过**上下文指针**沟通，指向 spec、tickets、研究笔记和之前的 commits。不要重复指针已经提供的信息。

为了获得最大并发度，应尽可能在后台运行**实现子 agent**。

## 步骤

1. 阅读 spec 和 tickets，理解任务图。

2. （可选）使用一个**探索子 agent**完成 tickets 所需的探索，包括相关代码库文件或外部文档。确保探索子 agent 能保存文件。它应将 Markdown 笔记保存在仓库外、所有后续子 agent 都能访问的目录中，让**实现子 agent**专注于实现，而不是重复探索。

3. 创建集成分支。如果 Issue 跟踪器通过 PR 关闭工作，或者用户要求创建 PR，则在步骤 5 第一次合并完成后打开草稿 PR（没有领先于 main 的 commit 时无法创建 PR），并标记它将关闭该 spec 和所有 tickets。

4. 使用**实现子 agent**逐个实现 ticket。每个子 agent 使用独立 worktree 和独立分支，并且：
   - 开始前确认其 worktree 基于集成分支；如果不是，则重置到集成分支；
   - 调用 Skill 工具加载 `tdd` 来实现 ticket；
   - 报告完成前，将集成分支的最新 tip 合并到自己的分支。

5. 每当一个**实现子 agent**完成后，使用一个**合并子 agent**把它的工作合入集成分支。

6. 如果可用 tickets 的**前沿**发生变化，启动更多**实现子 agent**处理新出现的 tickets，以获得最大并发度。

7. 所有 tickets 完成后，在集成分支上调用 Skill 工具加载 `code-review`。使用单一**实现子 agent**修复代码审查提出的全部问题。

8. 如果存在草稿 PR，将它标记为可供审查。否则，按照 Issue 跟踪器关闭工作的方式解决每个 ticket，并报告集成分支。

9. 清理所有**实现子 agent**的 worktrees。
