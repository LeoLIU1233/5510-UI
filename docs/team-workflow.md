# 三人起步与合并手册

## 1. 分工边界

| 角色 | 主要目录/接口 | 交付物 |
| --- | --- | --- |
| 前端负责人 | `index.html`、`UI.py`、`start_preview.bat`、前端 BFF 适配 | 四个页面、交互、加载/错误状态 |
| AI 后端负责人 | `ai_mvp/`、AI API、测试 | 画像、聊天、风险、模拟建议 |
| 中台/交易负责人 | 行情、账户、订单、风控服务 | 双边报价、账户快照、订单预览和提交 |

共享：`CLAUDE.md`、`docs/integration-contract.md`、根 README 和合并后的运行手册。

## 2. 第一次协作

1. 三个人分别同步各自仓库；
2. 确认本文件中的接口名称和字段；
3. 每个人创建功能分支；
4. 先完成一个最小垂直切片：`health -> profile -> chat`；
5. 再完成行情和风险；
6. 最后完成订单预览和提交；
7. 每个切片都发 PR，并运行 `/code-review`。

## 3. 推荐的前三个 PR

### PR 1：共享契约

- 负责人：前端或协调人；
- 内容：`CLAUDE.md`、`.claude/`、`.gitignore`、`.env.example`、接口契约；
- 验收：其他两人确认职责和接口没有歧义。

### PR 2：AI 对话垂直切片

- 负责人：前端 + AI 后端；
- 内容：BFF `/api/assistant/chat`，画像写入，前端显示 reply；
- 验收：无 Token 泄露，成功/失败/超时状态可用。

### PR 3：行情与风险

- 负责人：中台 + 前端 + AI；
- 内容：跨平台报价、来源时间、账户风险和部分状态；
- 验收：比价表不再使用无来源静态数据。

## 4. 每次开工步骤

```powershell
git switch main
git pull --rebase origin main
git switch -c feature/<owner>/<feature-name>
```

然后：

1. 让 AI 先读 `CLAUDE.md` 和接口契约；
2. 说明本次只改哪些文件；
3. 先实现最小改动；
4. 运行启动和测试；
5. 使用 `/preflight`；
6. 使用 `/code-review`；
7. 使用 `/commit-message`；
8. 使用 `/pr-description`；
9. 再次人工检查高风险内容；
10. 发 PR，另一人 review，合并后删除分支。

## 5. AI 合并其他仓库的提示词

可以把下面这段直接交给负责汇总的同学的 AI：

```text
你要把三个仓库合并成一个团队 monorepo。先不要修改业务逻辑。

1. 阅读每个仓库的 CLAUDE.md、README 和接口文档。
2. 以 docs/integration-contract.md 作为跨模块契约。
3. 保留 frontend、ai-backend、middle-office 的独立运行入口。
4. 不要覆盖彼此 README；根 README 只增加总览和启动顺序。
5. 不提交 .env、Token、数据库、缓存或用户数据。
6. 先用 dry-run 或只读检查列出文件冲突和接口冲突。
7. 输出冲突清单、拟合并目录和需要人工决定的问题。
8. 得到确认后再实际移动或合并文件。
9. 分别运行各模块测试，再按 health -> profile -> chat -> quote -> risk -> order 顺序联调。
10. 明确区分“代码已合并”“模块测试通过”“端到端联调通过”。
```

## 6. 合并后目录示例

```text
5510-team/
├─ CLAUDE.md
├─ README.md
├─ docs/
├─ .claude/
├─ frontend/
│  ├─ index.html
│  ├─ UI.py
│  └─ start_preview.bat
├─ ai-backend/
│  ├─ ai_mvp/
│  ├─ tests/
│  └─ README.md
└─ middle-office/
   ├─ src/
   ├─ tests/
   └─ README.md
```

## 7. Review 分工

- 前端 PR：至少一名非前端成员检查接口使用和业务语义；
- AI 后端 PR：前端检查响应字段是否可渲染，中台检查数据边界；
- 中台/订单 PR：前端检查状态流，AI 负责人检查用户身份和风险字段；
- 文档或共享 AI 规则：必须由另一名组员 review；
- 任何人不得只依赖自己的 AI review 后直接合并。

## 8. 完成定义

一个功能只有同时满足以下条件才算完成：

- 代码已合并到 `main`；
- 启动命令有效；
- 相关测试通过；
- 接口契约已更新；
- 页面有 loading、成功、空数据和失败状态；
- 没有密钥或隐私数据进入 Git；
- PR 中记录了实际验证结果；
- 回滚方式明确。
