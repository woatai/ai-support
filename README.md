# AI Support

这是一个面向跨境电商场景的 AI 客服助手项目。项目通过 Streamlit 提供简单的客服工作台界面，通过 FastAPI 提供后端接口，并调用 DeepSeek 大模型生成礼貌、简洁、专业的客服回复。

当前版本已经跑通最小可用闭环：客服人员在页面输入客户问题，前端请求后端 `/chat` 接口，后端调用大模型生成回复并返回给页面展示。

## 项目目标

本项目用于练习和演示 AI 应用开发中的常见能力，包括：

- 使用大模型 API 生成客服回复
- 使用 FastAPI 封装后端服务
- 使用 Streamlit 搭建轻量前端页面
- 通过 Prompt 约束客服回复风格和边界
- 后续接入知识库检索、订单查询、意图分类和转人工建议

典型适用问题包括商品咨询、物流查询、退款售后、优惠券问题、投诉安抚等跨境电商客服高频场景。

## 当前功能

- 前端页面输入客户问题
- 后端提供 `POST /chat` 聊天接口
- 调用 DeepSeek Chat Completions API
- 基于客服系统提示词生成回复
- 对空消息、模型调用失败、返回格式异常做基础错误处理

当前版本只做普通客服回复，不包含 RAG、真实订单查询、用户登录、会话历史保存等能力。

## 技术栈

- Python
- FastAPI
- Uvicorn
- Streamlit
- Requests
- python-dotenv
- DeepSeek API

## 项目结构

```text
ai-support/
  backend/
    main.py          # FastAPI 应用和 /chat 接口
    llm_client.py    # DeepSeek API 调用封装
    prompts.py       # 客服系统提示词
  frontend/
    app.py           # Streamlit 前端页面
  docs/
    README.md
    07_跨境电商AI客服助手项目.md
    知识库_客服话术规范.md
  .env               # 本地模型配置，不建议提交真实密钥
  requirements.txt
  README.md
```

## 快速开始

1. 安装依赖：

```powershell
pip install -r requirements.txt
```

2. 配置环境变量：

在 `.env` 中配置真实的 DeepSeek API Key：

```env
DEEPSEEK_API_KEY=你的真实key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

3. 启动后端服务：

```powershell
uvicorn backend.main:app --reload
```

4. 启动前端页面：

```powershell
streamlit run frontend/app.py
```

默认访问地址：

- 后端接口：http://127.0.0.1:8000
- 前端页面：http://localhost:8501

## 接口示例

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/chat `
  -ContentType "application/json" `
  -Body '{"message":"我的订单什么时候发货？"}'
```

示例返回：

```json
{
  "reply": "您好，请提供订单号，我可以帮您进一步确认发货状态。"
}
```

## 文档入口

- [项目说明与开发路线](./docs/07_跨境电商AI客服助手项目.md)
- [客服话术规范知识库](./docs/知识库_客服话术规范.md)

## 后续规划

- 增加客服意图分类
- 增加更细分的客服场景 Prompt
- 接入知识库检索，支持基于话术规范回答
- 增加模拟订单数据查询
- 增加转人工判断和建议
- 保存会话记录，支持后续复盘和优化
