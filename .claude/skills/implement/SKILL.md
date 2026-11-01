---
name: implement
description: "基于 spec 或一组 tickets 实现工作内容。"
disable-model-invocation: true
---

根据用户在 spec 或 tickets 中描述的内容实现工作。

如果用户传入 ticket 引用，从 Issue 跟踪器中读取它，并在开始前说明 ticket 标题。如果引用有歧义，先询问用户。

尽可能在预先约定的 seam 处调用 Skill 工具加载 `tdd`。

定期运行类型检查，定期运行单个测试文件，最后运行一次完整测试套件。

完成后，调用 Skill 工具加载 `code-review` 来审查工作。

将你的工作提交到当前分支。
