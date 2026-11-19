# Harbor Invest - FTEC 5510 团队协作规范

本文件是三个人及其 AI 助手的共享约定。AI 在修改代码前必须先阅读本文件和 `docs/integration-contract.md`。如果实现与文档冲突，停止修改并在 PR 中说明冲突，不要自行猜测后大范围重写。

## 1. 项目目标

Harbor Invest 是一个多平台数字资产投资辅助原型，覆盖：

- 跨平台行情比价；
- 自选资产和下单前检查；
- AI 投资教育助手和模拟建议；
- 账户持仓与风险统计。

当前仓库是可交互前端原型，不执行真实交易。真实行情、账户和订单能力必须由受保护的后端接口提供。

## 2. 技术栈

- 前端：原生 HTML、CSS、JavaScript；
- 本地服务器：Python 3.10+ 标准库 `http.server`；
- 图标：仓库内 `lucide.min.js`；
- 当前不使用 npm、React、Vue、打包器、数据库或前端框架；
- AI 后端：Python 3.10+ 标准库，独立运行在 `127.0.0.1:8000`；
- 浏览器访问：静态前端 `127.0.0.1:5510`；
- 浏览器只能请求同源 `/api/*` BFF 接口，不能直接访问 AI 后端或携带服务 Token。

引入新依赖前必须在 PR 中说明原因、安装方式、版本和替代方案。不要静默新增框架。

## 3. 当前仓库结构

```text
5510-UI/
├─ CLAUDE.md
├─ .claude/
│  └─ commands/
├─ docs/
├─ .env.example
├─ .gitignore
├─ README.md
├─ index.html
├─ lucide.min.js
├─ UI.py
└─ start_preview.bat
```

`index.html` 目前同时包含页面、样式、交互和翻译表：

- 页面结构：约 1-664 行；
- 样式：约 665-2607 行；
- 交互与翻译：约 2609-2986 行；
- Lucide 初始化：约 2988 行以后。

修改前先定位实际代码，不要依赖固定行号。

## 4. 三人分工与代码所有权

### A. 前端负责人（Leo）

负责：

- `index.html` 的页面结构、样式、浏览器交互；
- `UI.py` 和 `start_preview.bat`；
- BFF 对前端的同源接口适配；
- 加载、空数据、错误和离线状态；
- README 中与前端运行有关的内容。

### B. AI 后端负责人

负责：

- 画像、AI 对话和风险接口；
- `POST /v1/chat`；
- `PUT/GET /v1/profiles/{user_id}`；
- `GET /v1/risk/{user_id}`；
- 模型、行情和账户适配器的服务端实现；
- 后端测试和接口错误处理。

本仓库只调用其通过 BFF 暴露的接口。除非该负责人明确要求，不要在 `5510-UI` 中复制 AI 后端源码。

### C. 中台/行情/交易负责人

负责：

- 跨平台 `venue + bid + ask + fee + slippage` 行情；
- 账户快照；
- 订单预览和订单提交；
- 风控、余额和成交状态；
- 登录会话与 `user_id` 映射。

当前 AI 后端的单币价接口不能替代跨平台双边报价，也不能替代订单接口。

## 5. 模块边界

### 前端可以负责

- 展示后端返回的结构化数据；
- 维护页面局部交互状态；
- 调用同源 `/api/*`；
- 对输入做基础格式校验；
- 显示加载、空数据、超时和错误；
- 在示例数据上明确标注“原型”“示例”或“模拟”。

### 前端不得负责

- 保存交易所 API Key、DeepSeek Key 或 `AI_MVP_API_TOKEN`；
- 伪造真实成交、余额或实时行情；
- 绕过订单预览直接提交订单；
- 把服务 Token 写入 URL、HTML、JavaScript、localStorage 或日志；
- 直接修改其他团队仓库的代码。

## 6. 浏览器接口约定

浏览器只调用同源路径：

```text
GET  /api/health
GET  /api/profile
PUT  /api/profile
POST /api/assistant/chat
GET  /api/risk
GET  /api/market/venues
GET  /api/market/orderbook
POST /api/orders/preview
POST /api/orders
GET  /api/orders/{id}
GET  /api/account/summary
GET  /api/account/transactions
```

不要把 `http://127.0.0.1:8000/v1/...` 直接写进浏览器代码。

BFF 负责：

1. 从登录会话确定 `user_id`；
2. 在服务端添加 `Authorization: Bearer <AI_MVP_API_TOKEN>`；
3. 转发到 AI 或中台服务；
4. 统一超时、错误码和跨域行为；
5. 过滤后端响应中不应对浏览器暴露的字段。

详细字段见 [接口与合并约定](docs/integration-contract.md)。

## 7. 数据格式

- 金额、数量、价格和比例优先使用十进制字符串，例如 `"68420.10"`；
- 时间使用带时区的 RFC 3339，例如 `"2026-11-19T10:00:00+08:00"`；
- 金额必须包含币种，例如 `currency: "USDT"`；
- 接口错误统一为：

```json
{
  "error": {
    "code": "invalid_request",
    "message": "human-readable message"
  }
}
```

- 不得把 `NaN`、`Infinity` 或浮点误差直接展示给用户；
- 不可用、超时、未配置、空数据和成功空列表必须区分。

## 8. 前端代码规范

### JavaScript

- 使用 `"use strict"` 语义和现代浏览器支持的 ES 语法；
- 使用 `const`，只有确实重新赋值时才用 `let`；
- 缩进 2 个空格，语句使用分号；
- 延续现有代码的双引号风格；
- 使用 `camelCase`；DOM ID 使用 kebab-case；
- 数据写入页面优先使用 `textContent`；
- 未经明确审查，不得将后端文本拼接到 `innerHTML`；
- 一个函数只处理一种职责；
- 网络请求必须集中封装，不能每个按钮各写一套 `fetch`；
- 请求必须处理 loading、成功、空数据、失败和超时。

示例：

```javascript
async function requestJson(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {})
    }
  });

  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    throw new Error(payload?.error?.message || `HTTP ${response.status}`);
  }
  return payload;
}
```

### Python

- 使用 Python 3.10+；
- 缩进 4 个空格；
- 使用类型提示；
- 只使用标准库，除非 PR 中说明并更新依赖；
- 不得在日志中输出 API Key、Token、密码或完整账户数据。

### HTML/CSS

- 保留中英文切换和现有无障碍属性；
- 按钮必须有 `type="button"`，提交按钮除外；
- 交互控件要有可理解的 `aria-label`；
- 保留现有 `da-` 样式命名空间；
- 不进行与功能无关的全文件格式化；
- 不直接编辑 `lucide.min.js`，除非明确升级图标库。

## 9. 常用命令

启动本地页面：

```powershell
python UI.py
```

不自动打开浏览器：

```powershell
python UI.py --no-browser
```

Python 语法检查：

```powershell
python -m py_compile UI.py
```

如果本机有 Node.js，可检查 HTML 中 JavaScript 语法：

```powershell
node -e "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');[...h.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(m=>m[1]).filter(Boolean).forEach(s=>new Function(s));"
```

当前没有 `npm run dev/test/build`。不要虚构这些命令。

## 10. Git 与 Pull Request 强制流程

### 分支

从最新 `main` 创建：

```powershell
git switch main
git pull --rebase origin main
git switch -c feature/<owner>/<feature-name>
```

示例：

```text
feature/leo/assistant-chat
feature/ai/profile-contract
feature/middle/order-preview
docs/integration-contract
```

### 提交前

```powershell
git fetch origin
git rebase origin/main
git diff --check
```

然后运行页面和语法检查，确认没有提交密钥。

### Pull Request

- 一个 PR 只解决一个明确问题；
- PR 描述必须包含变更、测试、风险和回滚方式；
- 至少一名组员 review；
- 发出前使用 AI `/code-review` 自查；
- 修改 `CLAUDE.md`、接口契约或安全规则时必须由组员 review；
- `main` 永远保持可运行；
- 不直接向 `main` force push；
- 合并后删除功能分支。

### Commit message

使用 Conventional Commits：

```text
feat(frontend): connect assistant chat endpoint
fix(frontend): validate empty order quantity
docs: define market quote contract
test(frontend): cover API error rendering
chore: update shared AI review commands
```

## 11. AI 修改规则

AI 在开始工作前必须：

1. 阅读 `CLAUDE.md` 和 `docs/integration-contract.md`；
2. 查看 `git status` 和 `git diff`；
3. 确认修改文件属于当前分工；
4. 先解释假设；
5. 做最小范围修改；
6. 运行可执行的验证；
7. 输出修改文件、测试结果和剩余风险。

AI 不应：

- 为通过 review 而删除测试、降低校验或隐藏错误；
- 未经要求重构整个 `index.html`；
- 同时修改前端、后端和中台的大量无关代码；
- 编造接口已经存在或联调已经通过；
- 提交 `.env`、Token、数据库或用户隐私数据；
- 直接修改 `main` 或强制推送。

## 12. AI Review 重点

优先检查：

1. 是否违反三人模块边界；
2. 是否泄露密钥或服务 Token；
3. 是否直接访问 `8000` 或其他跨域服务；
4. 是否把模拟数据标为真实数据；
5. 是否区分 loading、成功、空数据、失败和超时；
6. 是否产生 `NaN`、重复提交或绕过订单预览；
7. 是否破坏中文/英文切换和四个页面导航；
8. 是否修改了声明中不应修改的文件；
9. 是否缺少测试或回滚说明；
10. 是否引入不必要的依赖或全文件格式化。

## 13. 汇总其他仓库时的规则

其他同学的 AI 将三个仓库汇总时：

- 保留每个模块的独立目录和运行入口；
- 以 `docs/integration-contract.md` 为接口边界；
- 前端保持在 `5510`，AI 后端保持在 `8000`，通过 BFF 连接；
- 不直接复制服务端 Token 到前端；
- 不把三个 `README.md` 简单覆盖为一份，先保留模块说明再增加根目录总览；
- 合并后必须分别运行前端、AI 后端和中台测试，再做一次端到端联调；
- 冲突合并结果必须由人 review。

本仓库是前端模块，不应被其他 AI 强行扩展成完整交易系统。需要新增后端代码时，应由对应负责人创建独立模块并通过 PR 合入。
