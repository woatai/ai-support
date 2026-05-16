# 项目文档

这里沉淀跨境电商 AI 客服助手的需求、路线和知识库资料。

## 文档目录

- [跨境电商 AI 客服助手项目](./07_跨境电商AI客服助手项目.md)
  - 项目定位
  - 核心流程
  - 功能模块
  - 技术栈
  - 阶段路线
  - 简历与面试表达

- [客服话术规范知识库](./知识库_客服话术规范.md)
  - 客服沟通原则
  - 回复语气规范
  - 上门系统问题口径
  - RAG 切分建议
  - AI 客服系统总约束

## 当前阶段

当前项目处于第一阶段：先完成最小可运行闭环。

目标流程：

```text
用户在 Streamlit 页面输入问题
↓
Streamlit 调用 FastAPI /chat 接口
↓
FastAPI 调用大模型 API
↓
大模型根据客服 Prompt 生成回复
↓
FastAPI 返回 JSON
↓
Streamlit 展示 AI 回复
```

第一阶段暂不实现 RAG、订单查询和转人工规则，先把普通 AI 客服回复跑通。

## 提示词设计说明

当前项目的 LLM 调用链比较简单，适合新手先理解完整闭环：

```text
frontend/app.py 输入客户问题
  -> backend/main.py 接收 /chat 请求
  -> backend/llm_client.py 调用 DeepSeek API
  -> backend/prompts.py 提供客服系统提示词
```

提示词代码主要在 `backend/prompts.py`。当前按职责拆成四块：

```python
DEFAULT_SYSTEM_PROMPT          # 定义 AI 是谁
CUSTOMER_SERVICE_RULES         # 定义客服业务规则和边界
RESPONSE_STYLE_PROMPT          # 定义回复语气、格式和长度
build_customer_service_prompt  # 拼接最终系统提示词
```

这种写法参考了更完整的 Agent 项目里的“提示词分层 + 最终拼接”思想，但本项目没有直接照搬复杂架构。当前不会引入 Agent 表、数据库 Prompt 管理、Workflow 编排等能力，先保持一个轻量、容易看懂、容易调试的版本。

中英文提示词混用通常不会导致 LLM 调用失败，但会影响回复风格的稳定性。因为本项目面向中文客服场景，建议业务相关提示词尽量统一使用中文，比如客服身份、回复规则、兜底话术、转人工规则等。

后续可以按这个顺序扩展：

1. 继续完善 `CUSTOMER_SERVICE_RULES`，把不能编造、需要补充信息、需要转人工的规则写清楚。
2. 拆分物流查询、退款售后、商品咨询、投诉安抚等不同场景的提示词。
3. 再考虑接入 Agent、RAG 知识库、模拟订单查询、转人工判断等更完整的能力。

## 参考项目

- [tgo](https://github.com/tgoai/tgo/tree/main)：本项目仅参考其 LLM/Agent 提示词分层思想，当前仍保持轻量实现。
