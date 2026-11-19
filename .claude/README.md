# 共享 AI 命令

此目录中的命令会提交到仓库，三个人的 AI 助手使用同一套流程。

- `/code-review`：审查当前分支相对 `origin/main` 的改动；
- `/preflight`：提交前运行可用的检查和敏感信息扫描；
- `/commit-message`：根据 staged diff 生成统一格式的提交信息；
- `/pr-description`：生成 Pull Request 描述。

个人本地设置放在 `.claude/settings.local.json`，该文件已被 `.gitignore` 忽略。

修改本目录中的共享命令属于协作约定变更，必须走 PR 并由另一名组员 review。
