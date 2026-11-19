---
description: 根据当前分支改动生成 Pull Request 描述
argument-hint: "[可选：目标分支，默认 origin/main]"
---

读取：

1. `CLAUDE.md`
2. `docs/integration-contract.md`
3. `git status --short`
4. `git diff <target>...HEAD`
5. 相关测试结果

如果没有提供参数，目标分支为 `origin/main`。

只报告可以从 diff 和测试中验证的内容。生成以下 Markdown：

```markdown
## Summary

## Changed

## Contract / API Impact

## Tests

## Screenshots or Manual Checks

## Risks

## Rollback
```

要求：

- 不把“实现完成”写成“已联调成功”；
- 明确哪些测试实际运行、哪些未运行；
- 如果接口字段变化，链接 `docs/integration-contract.md`；
- 如果涉及页面，列出人工检查的页面；
- 如果没有风险，也必须说明为什么；
- 不生成虚假的测试输出或截图。
