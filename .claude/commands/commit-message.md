---
description: 根据暂存改动生成团队统一的 Conventional Commit 信息
---

读取：

1. `git status --short`
2. `git diff --cached --stat`
3. `git diff --cached`
4. `CLAUDE.md` 中的提交规范

只根据已经 staged 的改动生成一条提交信息，不要修改文件。

格式：

```text
<type>(<scope>): <short summary>
```

允许的类型：

- feat
- fix
- docs
- test
- refactor
- chore

常用 scope：

- frontend
- bff
- integration
- docs

要求：

- 使用英文；
- 不超过 72 个字符；
- 说明用户可见变化；
- 不使用 `update files`、`changes`、`misc` 等模糊描述；
- 如果 staged diff 同时包含多个无关功能，先提示拆分提交，不要强行生成一条信息。

最后只输出建议的 commit message。
