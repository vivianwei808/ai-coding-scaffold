#!/usr/bin/env python3
"""trellis update 之后重新应用 Matt Pocock 技能改挂（workflow.md + agents）。"""
import sys

WF = "/Volumes/pipi/AITraining/ai-coding-scaffold/.trellis/workflow.md"

SWAPS = [
    ("Load `trellis-brainstorm`; stay in planning.",
     "Load `grill-with-docs` (Matt Pocock skill: relentless interview + build CONTEXT.md shared language + ADR); stay in planning. Persist conclusions into `prd.md`."),
    ("Flow: `trellis-implement` -> `trellis-check` -> `trellis-update-spec` -> commit (Phase 3.4) -> `/trellis:finish-work`.",
     "Flow: `trellis-implement` (drive /tdd red-green on pre-confirmed seams) -> `trellis-check` (dual-axis review per /code-review: Standards + Spec) -> `/domain-modeling` spec write-back -> commit (Phase 3.4) -> `/trellis:finish-work`."),
    ("Flow: `trellis-before-dev` -> edit -> `trellis-check` -> validation -> `trellis-update-spec` -> commit (Phase 3.4) -> `/trellis:finish-work`.",
     "Flow: `trellis-before-dev` -> edit (drive /tdd red-green discipline) -> `trellis-check` -> validation -> `/domain-modeling` spec write-back -> commit (Phase 3.4) -> `/trellis:finish-work`."),
    ("- Planning or unclear requirements -> `trellis-brainstorm`.",
     "- Planning or unclear requirements -> `grill-with-docs`."),
    ("- Repeated debugging -> `trellis-break-loop`; spec updates -> `trellis-update-spec`.",
     "- Repeated debugging -> `trellis-break-loop`; spec updates -> `/domain-modeling` (updates CONTEXT.md + spec)."),
    ("`trellis-update-spec` is a skill.",
     "`/domain-modeling` (Matt Pocock skill) handles spec write-back."),
    ("Load the `trellis-brainstorm` skill and explore requirements interactively with the user per the skill's guidance.",
     "Load the `grill-with-docs` skill and explore requirements interactively: relentless interview, one question at a time; persist conclusions into `prd.md`, shared language into CONTEXT.md, key decisions into ADR."),
    ("Load the `trellis-update-spec` skill and review whether this task produced new knowledge worth recording:",
     "Load the `/domain-modeling` skill (spec write-back) and review whether this task produced new knowledge worth recording:"),
]

p = sys.argv[1] if len(sys.argv) > 1 else WF
t = open(p).read()
n = 0
for old, new in SWAPS:
    if new in t:
        continue
    if old in t:
        t = t.replace(old, new)
        n += 1
open(p, "w").write(t)
print(f"重挂 {n} 处；残留 trellis-brainstorm: {t.count('trellis-brainstorm')}，trellis-update-spec: {t.count('trellis-update-spec')}")
