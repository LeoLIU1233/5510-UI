---
description: 按团队规范审查当前分支相对 origin/main 的改动
argument-hint: "[可选：目标分支，默认 origin/main]"
---

请审查当前工作区。

目标比较分支：

```text
$ARGUMENTS
```

如果没有提供参数，使用 `origin/main`。

先读取：

1. `CLAUDE.md`
2. `docs/integration-contract.md`
3. `git status --short`
4. `git diff <target>...HEAD`
5. 相关测试和运行命令

只报告本次分支引入的问题。按严重程度输出：

- Critical：密钥泄露、资金/订单错误、鉴权绕过、数据损坏；
- High：直接跨域调用、伪造成功、状态判断错误、主要功能回归；
- Medium：loading/empty/error 状态缺失、字段契约不一致、可维护性问题；
- Low：命名、重复代码、文档小错误。

每条发现必须包含：

- 文件与行号；
- 具体问题；
- 可能的用户影响；
- 最小修复建议。

额外重点检查：

- 浏览器是否直接访问 8000；
- 前端是否包含 `AI_MVP_API_TOKEN` 或 API Key；
- 是否把模拟报价标成实时；
- 是否区分成功、空数据、超时和失败；
- 是否绕过订单预览直接提交；
- 是否修改三人分工外的模块；
- 是否进行无关的大范围格式化。

不要修改代码。最后给出：

1. 是否建议合并；
2. 必须修复项；
3. 建议补测项；
4. 尚未验证的内容。
