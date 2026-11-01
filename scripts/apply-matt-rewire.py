#!/usr/bin/env python3
"""trellis update 之后重新应用 Matt Pocock 技能改挂。

覆盖三类文件（全部幂等，可反复运行）：
  1. .trellis/workflow.md      — 技能引用改挂
  2. .claude/agents/*.md       — TDD 纪律 / 双轴评审注入
  3. hooks / commands / 相关 SKILL.md — 悬空技能名改挂

用法（在项目根目录或任意位置均可，路径相对本脚本定位）：
  python3 scripts/apply-matt-rewire.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── 1. workflow.md 引用改挂 ──────────────────────────────────────────
WORKFLOW_SWAPS = [
    ("Load `trellis-brainstorm`; stay in planning.",
     "Load `grill-with-docs` (Matt Pocock skill: relentless interview + build CONTEXT.md shared language + ADR); stay in planning. Persist conclusions into `prd.md`."),
    ("Flow: `trellis-implement` -> `trellis-check` -> `trellis-update-spec` -> commit (Phase 3.4) -> `/trellis:finish-work`.",
     "Flow: `trellis-implement` (drive /tdd red-green on pre-confirmed seams) -> `trellis-check` (dual-axis review per /code-review: Standards + Spec) -> `/domain-modeling` spec write-back -> commit (Phase 3.4) -> `/trellis:finish-work`."),
    ("Flow: `trellis-before-dev` -> edit -> `trellis-check` -> validation -> `trellis-update-spec` -> commit (Phase 3.4) -> `/trellis:finish-work`.",
     "Flow: `trellis-before-dev` -> edit (drive /tdd red-green discipline) -> `trellis-check` -> validation -> `/domain-modeling` spec write-back -> commit (Phase 3.4) -> `/trellis:finish-work`."),
    ("- Planning or unclear requirements -> `trellis-brainstorm`.",
     "- Planning or unclear requirements -> `grill-with-docs`."),
    ("- Repeated debugging -> `trellis-break-loop`; spec updates -> `trellis-update-spec`.",
     "- Repeated debugging -> `/diagnosing-bugs`; spec updates -> `/domain-modeling` (updates CONTEXT.md + spec)."),
    ("`trellis-update-spec` is a skill.",
     "`/domain-modeling` (Matt Pocock skill) handles spec write-back."),
    ("Load the `trellis-brainstorm` skill and explore requirements interactively with the user per the skill's guidance.",
     "Load the `grill-with-docs` skill and explore requirements interactively: relentless interview, one question at a time; persist conclusions into `prd.md`, shared language into CONTEXT.md, key decisions into ADR."),
    ("Load the `trellis-update-spec` skill and review whether this task produced new knowledge worth recording:",
     "Load the `/domain-modeling` skill (spec write-back) and review whether this task produced new knowledge worth recording:"),
    ("- Repeated debugging -> `trellis-break-loop`; spec updates -> `/domain-modeling` (updates CONTEXT.md + spec).",
     "- Repeated debugging -> `/diagnosing-bugs`; spec updates -> `/domain-modeling` (updates CONTEXT.md + spec)."),
    ("If this task involved repeated debugging (the same issue was fixed multiple times), load the `trellis-break-loop` skill to:",
     "If this task involved repeated debugging (the same issue was fixed multiple times), load the `/diagnosing-bugs` skill to:"),
]

# ── 2. hooks / commands / SKILL.md 悬空引用 ─────────────────────────
OTHER_SWAPS = {
    ".claude/hooks/session-start.py": [
        ("Next-Action: Load `trellis-brainstorm` and write `prd.md`. Stay in planning.",
         "Next-Action: Load `grill-with-docs` and write `prd.md`. Stay in planning."),
    ],
    ".claude/hooks/inject-workflow-state.py": [
        ("# trellis-brainstorm + task.py create when user describes real work.",
         "# grill-with-docs + task.py create when user describes real work."),
    ],
    ".claude/commands/trellis/continue.md": [
        ("(load `trellis-brainstorm`)", "(load `grill-with-docs`)"),
    ],
    ".claude/skills/trellis-session-insight/SKILL.md": [
        ("Run the `trellis-update-spec` skill for that",
         "Run the `/domain-modeling` skill for that"),
        ("This skill does not replace `trellis-update-spec`",
         "This skill does not replace `/domain-modeling`"),
    ],
    ".claude/skills/trellis-meta/references/customize-local/change-workflow.md": [
        ("Phase 1.1 (load `trellis-brainstorm`)", "Phase 1.1 (load `grill-with-docs`)"),
    ],
    ".claude/skills/trellis-meta/references/local-architecture/workflow.md": [
        ("skills, such as `trellis-brainstorm` and `trellis-check`.",
         "skills, such as `grill-with-docs` (replaces native brainstorm) and `trellis-check`."),
    ],
    ".claude/skills/trellis-meta/references/local-architecture/spec-system.md": [
        ("Phase 3.3 in `.trellis/workflow.md` and the `trellis-update-spec` skill.",
         "Phase 3.3 in `.trellis/workflow.md` and the `/domain-modeling` skill (replaces native update-spec)."),
    ],
}

# ── 3. agents 注入 ───────────────────────────────────────────────────
IMPL_ANCHOR = """## Core Responsibilities

1. **Understand specs** - Read relevant spec files in `.trellis/spec/`
2. **Understand task artifacts** - Read prd.md, design.md if present, and implement.md if present
3. **Implement features** - Write code following specs and task artifacts
4. **Self-check** - Ensure code quality
5. **Report results** - Report completion status"""
IMPL_MATT = """## Core Responsibilities

1. **Understand specs** - Read relevant spec files in `.trellis/spec/`
2. **Understand task artifacts** - Read prd.md, design.md if present, and implement.md if present
3. **Implement features** - Write code following specs and task artifacts
4. **TDD discipline (Matt Pocock)** - Drive a red-green loop on pre-confirmed seams: write one failing test, then the minimum code to pass, repeat. Avoid the three anti-patterns: implementation coupling (mocking internals / testing privates), tautology (assertions re-computing the code's logic), horizontal slicing (all tests first, then all implementation)
5. **Self-check** - Ensure code quality
6. **Report results** - Report completion status"""

CHK_ANCHOR = "You are the Check Agent in the Trellis workflow."
CHK_MATT = CHK_ANCHOR + """

## Dual-Axis Review Discipline (Matt Pocock /code-review)

Run verification along two independent axes, keeping them separate:
- **Standards axis**: does the code follow the repo's documented coding standards and Fowler's code smells baseline (Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest)?
- **Spec axis**: does the code faithfully implement prd.md / design.md? Look for missing pieces, deviations, and out-of-scope changes.

Report both axes without merging or re-ranking them."""


def apply(path, swaps):
    p = os.path.join(ROOT, path)
    if not os.path.exists(p):
        print("跳过(不存在):", path)
        return 0
    t = open(p).read()
    n = 0
    for old, new in swaps:
        if new in t:
            continue  # 已应用，幂等
        if old in t:
            t = t.replace(old, new)
            n += 1
    if n:
        open(p, "w").write(t)
    return n


total = 0
wf = os.path.join(ROOT, ".trellis/workflow.md")
n = apply(".trellis/workflow.md", WORKFLOW_SWAPS)
total += n
print(f"workflow.md: {n} 处")

for path, swaps in OTHER_SWAPS.items():
    n = apply(path, swaps)
    total += n
    print(f"{path}: {n} 处")

n = apply(".claude/agents/trellis-implement.md", [(IMPL_ANCHOR, IMPL_MATT)])
total += n
print(f"agents/trellis-implement.md: {n} 处")

n = apply(".claude/agents/trellis-check.md", [(CHK_ANCHOR, CHK_MATT)])
total += n
print(f"agents/trellis-check.md: {n} 处")

t = open(wf).read()
print(f"共 {total} 处；残留 brainstorm: {t.count('trellis-brainstorm')}，update-spec: {t.count('trellis-update-spec')}，break-loop: {t.count('trellis-break-loop')}")
