---
description: 提交前运行团队预检查和敏感信息扫描
---

按以下顺序执行，不要修改业务代码：

1. 阅读 `CLAUDE.md`；
2. 运行 `git status --short`；
3. 运行 `git diff --check`；
4. 运行 `python -m py_compile UI.py`；
5. 如果存在 Node.js，检查 `index.html` 中所有内联 JavaScript 的语法；
6. 检查 staged 和 working tree 是否包含 `.env`、真实 Key、Bearer Token、数据库或用户隐私文件；
7. 检查浏览器代码是否直接访问 `127.0.0.1:8000` 或 `/v1/*`；
8. 检查 README 中是否有不存在的 `npm` 命令；
9. 启动 `python UI.py --no-browser`，请求主页，确认 HTTP 200；
10. 停止启动的本地服务器。

输出：

- 已执行的检查；
- 通过项；
- 失败项；
- 因环境缺失而跳过的检查；
- 是否可以创建 commit。

不得声称未实际运行的检查已通过。
