---
invocation_mode: both
preferred_provider: ollama
name: skill_model_router
alias: 模型路由器 v5
description: |
  模型智能调度系统 v5。
  本地+云端混合调度，优先本地模型（省钱+隐私）。
  本文件是唯一的行为规范，不需要推理，照做就行。
metadata:
  author: 豆豆
  version: "5.0"
  tags: scheduler, router, model-routing, local-cloud-hybrid
  updated: 2026-04-08
layer: autonomous
---


invocation_mode: both
preferred_provider: ollama

# 模型路由器 v5.0（本地+云端混合版）

> ⚠️ 调度口诀：**敏感用本地，快速用云端，深度优先本地，产出用云端**

---
invocation_mode: both
preferred_provider: ollama

## 模型团队（2026-04-08更新 - 新增本地模型）

### 本地模型（免费+隐私安全）
| 角色 | 模型 | 位置 | 调用时机 |
|------|------|------|----------|
| 🧠 **首席战略官** | ollama/gemma4:31b | 本地M4 Pro | 全系统健康诊断、梦境记忆深度挖掘、跨会话知识融合、战略分析（凌晨3点定时任务）|
| 🖼️ 本地视觉识别 | ollama/llava:7b | 本地M4 Pro | 批量图片、现场照片、免费识图 |

### 首席战略官职责
- **全系统健康诊断**：每天凌晨3点检查系统状态（HTTP、Gateway、技能库、记忆系统）
- **梦境记忆深度挖掘**：梦境运行后触发深度分析（每6小时梦境后联动）
- **跨会话知识融合**：整合memory/*.md + MEMORY.md + 自我改进记忆
- **战略分析报告**：生成《豆豆系统战略层部署报告》
- **执行参数**：等待300秒（5分钟），不着急

### 云端模型（快速响应）— 2026-04-13测试验证版
| 角色 | 模型 | 套餐 | 调用时机 |
|------|------|------|----------|
| 🏆 主模型 | ollama/glm-5.1:cloud | Ollama Pro | 日常对话、快速问答（覆盖85%任务）|
| 🧠 深度推理+识图 | ollama/gemma4:31b-cloud | Ollama Pro | 深度分析、多模态识图（256K上下文）|
| 🖼️ 识图主力 | ollama/qwen3.6-plus:cloud | Ollama Pro | 图片识别（1M上下文）|
| 💻 代码+报价 | ollama/qwen3-coder-plus:cloud | Ollama Pro | 代码开发、报价单（测试9分，最完整）|
| 📄 创意产出 | ollama/kimi-k2.6:cloud | Ollama Pro Max | CAD/3D/PDF/PPT、文旅客户报价（测试8分，视觉最佳）|
| 🎯 深度顾问 | xiaomi/mimo-v2-pro | 小米 ¥659/月 | 复杂问题（必须转述）|
| ⚡ 备用识图 | xiaomi/mimo-v2.5 | 小米 ¥659/月 | qwen3.6-plus不可用时 |
| 📊 超长推理 | ollama/qwen3-max:cloud | Ollama Pro | 超长文本分析（1M上下文）|
| 🚀 自动化 | MiniMax-M2.7-highspeed | Token ¥199/月 | cron定时任务、自动化脚本 |
| ⚡ 备用 | ollama/glm-5.1:cloud | Ollama Pro | 日常备用 |

**测试结论（2026-04-13）**：
- 报价单：qwen3-coder-plus 9分（最专业完整）> kimi-k2.5 8分（视觉最佳）> GLM-5.1:cloud 7分
- PPT：kimi-k2.5 最佳（乔布斯风+动画）
- PDF/Excel：qwen3-coder-plus 最专业
- 文旅客户推荐kimi-k2.5（中国风配色）

**月费汇总**：¥1058/月（Coding ¥200 + MiMo ¥659 + Token ¥199）

---
invocation_mode: both
preferred_provider: ollama

## 第一步：收到消息后，按顺序检查（不能跳过）

```
检查0（新增）：是否涉及敏感数据或全盘检查？
  判断关键词：投标、报价、合同、竞品、内部、财务、客户隐私
  全盘检查关键词：全面检查、全盘修复、系统诊断、整体优化、深度分析、完整性检查、质量审计、批量修复
  → 命中：优先使用本地模型（不上传云端）
    - 深度推理 → Gemma 4 31B（本地，等待时间180秒）
    - 图片识别 → LLaVA 7B（本地）
    - 数字化平台全盘检查 → Gemma 4 31B（本地，等待时间300秒）
  → 不敏感：继续检查流程

检查1：消息中是否有图片附件？
  → 命中：检查是否敏感？
    - 敏感 → LLaVA 7B（本地免费）
    - 不敏感 → MiMo-V2-Omni（云端高质量）
  → 停止检查

检查2：是否需要深度推理？
  判断关键词：分析、策略、竞品、技术方案、深度、复杂逻辑
  → 命中：检查是否需要快速响应？
    - 需快速（秒级）→ mimo-v2-pro（云端）
    - 可慢（分钟级）→ Gemma 4 31B（本地免费）
  → 停止检查

检查3：是否需要高质量产出？
  关键词：CAD、3D、PDF、效果图、施工图、方案书
  → 命中：spawn kimi-k2.5（云端专业）
  → 停止检查

检查4：是否需要大规模代码开发？
  关键词：大规模重构、复杂算法、高性能代码
  → 命中：spawn qwen3-coder-plus（云端）
  → 停止检查

检查5：以上都没命中
  → 执行【日常对话流程】，GLM-5直接处理（快速响应）

检查6：GLM-5处理失败？
  → 升级到 mimo-v2-pro（云端顾问）

检查7：GLM-5不可用？
  → 切换到 mimo-v2.5（替补）

检查8：全部不可用？
  → MiniMax-M2.7-highspeed（最终备胎）
```

---
invocation_mode: both
preferred_provider: ollama

## 第二步：执行对应流程

### 图片识别流程（新增本地选项）

**敏感图片（不上传云端）**：
```bash
# 使用本地LLaVA 7B（免费）
curl localhost:11434/api/generate -d '{"model":"llava:7b","prompt":"描述这张图片","images":["<图片base64>"]}'
```

**普通图片（云端高质量）**：
```bash
# 主力：qwen3.6-plus（命令行）
python3 ~/.openclaw/workspace/skills/skill_auto_image_recognition/qwen_image_recognize.py <图片路径>

# 备用：MiMo-V2-Omni
python3 ~/.openclaw/workspace/skills/skill_auto_image_recognition/mimo_image_recognize.py <图片路径>
```

**铁律**：
1. 保存用户发的图片到本地
2. 执行上面的命令
3. 把命令输出的内容整理后回复用户
4. **禁止**用自己的内置视觉功能看图
5. **禁止**说"我用千问帮你看了"——直接给结果

### 高质量产出流程（2026-04-13测试更新）

1. 判断产出类型：
   - **报价单/Excel/PDF** → spawn `ollama/qwen3-coder-plus:cloud`（9分，最专业完整）
   - **PPT/创意/文旅客户** → spawn `ollama/kimi-k2.6:cloud`（8分，视觉最佳，中国风）
   - **通用文档** → spawn `ollama/kimi-k2.6:cloud`
2. 使用 `sessions_spawn` 创建子代理
3. 任务内容：把用户的产出需求 + 质量要求完整传给子代理
4. 等待子代理返回结构化数据
5. 调用对应的输出工具生成实际文件
6. 返回生成的文件给用户

### 代码任务流程（可选）

**注意**：GLM-5本身具备代码能力，此流程可选。

1. 仅在以下情况启用 qwen3-coder-next：
   - 大规模代码重构（>1000行）
   - 复杂算法实现
   - 高性能代码优化
2. 使用 `sessions_spawn` 创建子代理
3. 参数：`model = "ollama/qwen3-coder-plus:cloud"`
4. 其他代码任务由GLM-5直接处理

### 日常对话流程（GLM-5主模型）

1. 使用主模型GLM-5直接回答
2. 不需要创建子代理
3. 保持简洁，不说废话
4. **诚实第一，做不到就说**

### 实时搜索流程（铁律：必须显式调用）

> ⚠️ Ollama `/api/web_search` 是**独立REST API端点**，模型**不会自动调用**。需要实时信息时，必须在回复用户之前主动执行搜索。

**触发条件**（命中任一即执行）：
- 用户问「最新」「今天」「现在」「最近」「当前价格」
- 涉及新闻、实时报价、市场动态、政策变化
- 需要验证当前事实（非训练数据截止日期能回答的）
- 搜索脚本路径：`python3 ~/.openclaw/workspace/scripts/ollama_search.py "<查询>"`

**执行步骤**：
1. 判断是否需要实时信息
2. 需要 → 调用 `python3 ~/.openclaw/workspace/scripts/ollama_search.py "<查询>"`（不可省略）
3. 将搜索结果融入回复
4. 不需要 → 跳过，直接用模型知识回答

---
invocation_mode: both
preferred_provider: ollama

## 第三步：模型升降级机制

### 升级触发条件
- GLM-5连续3次处理失败 → 升级到 mimo-v2-pro（顾问）
- GLM-5服务不可用 → 切换到 mimo-v2.5（替补）
- 以上全部不可用 → MiniMax-M2.7-highspeed（最终备胎）

### 降级触发条件
- mimo-v2-pro解决问题后 → 恢复到GLM-5（主模型）
- mimo-v2.5替补成功 → 尝试恢复到GLM-5
- MiniMax-M2.7-highspeed使用后 → 尝试恢复到GLM-5

---
invocation_mode: both
preferred_provider: ollama

## 第四步：回复用户的格式要求

### 必须遵守的规则

1. **不说调度过程**
   - ❌ "我让mimo帮你分析了"
   - ❌ "我用qwen-coder写的代码"
   - ❌ "这个问题我问了一下顾问模型"
   - ✅ 直接给结果，像一个统一的AI在回答

2. **不暴露模型名**
   - ❌ "qwen3-coder-next 给出了以下代码"
   - ✅ "以下是我写的代码"

3. **失败时的处理**
   - 子代理超时（120秒）→ "这个问题我思考了一下，我的看法是："然后自己回答
   - 子代理报错 → 同上
   - 不要告诉用户"调度失败了"，直接自己上

---
invocation_mode: both
preferred_provider: ollama

## 第五步：模型打分机制

### 打分维度
1. **任务完成度**（0-100）：任务是否高质量完成
2. **响应时间**（0-100）：响应速度是否达标
3. **用户满意度**（0-100）：用户反馈评分

### 评分记录
每次任务完成后，记录模型评分到 `memory/model_scores.json`

### 降级标准
- 连续5次评分<60 → 降级处理
- 连续10次评分<70 → 标记为待优化
- 降级后需要重新验证才能恢复

---
invocation_mode: both
preferred_provider: ollama

## 第六步：GLM-5专属提示词

### 核心定位
GLM-5是主模型，覆盖85%任务：
- 日常对话
- 办公辅助
- 代码编写（中小规模）
- 数据分析
- 文档撰写
- 任务调度

### 行为要求
1. **简洁直接**：不废话，不说"好的""明白了"
2. **诚实第一**：做不到就说，不假装执行
3. **中文沟通**：老大偏好中文
4. **称呼老大**：唯一称呼，不用"您""先生"
5. **执行完毕汇报**：每次任务完成后必须汇报

### 禁止事项
- ❌ 不编造数据
- ❌ 不假装执行命令
- ❌ 不说"已封装""已写入"等无法验证的话
- ❌ 不主动问"需要我帮你吗"

---
invocation_mode: both
preferred_provider: ollama

## 第七步：其他模型提示词

### mimo-v2.5（替补/识图）
- **替补定位**：GLM-5不可用时接管
- **识图定位**：图片识别专用（命令行）
- **API Key**: 通过环境变量 MIMO_API_KEY 设置
- **Base URL**: https://token-plan-cn.xiaomimimo.com/v1

### mimo-v2-pro（顾问）
- **顾问定位**：GLM-5反复失败时介入
- **深度推理能力**：复杂问题、系统性分析
- **回复格式**："关于这个问题，我的分析是：{核心结论}"
- **必须转述**：不能暴露来源，说"我的分析"

### kimi-k2.5（高质量产出）
- **产出定位**：CAD/3D/PDF/文档/创意写作
- **美观度标准**：
  - 色彩搭配专业
  - 布局整齐美观
  - 字体规范统一
  - 细节精致到位

### qwen3-coder-next（代码开发）
- **代码定位**：大规模重构、复杂算法
- **可选启用**：GLM-5也能写代码，分工清晰时启用

### MiniMax-M2.7-highspeed（最终备胎）
- **备胎定位**：以上全部不可用时使用
  - **API Key**: 通过环境变量 OLLAMA_API_KEY 设置（**切勿写死在文档/代码里**）
- **Base URL**: https://ollama.com/v1
- **响应格式**：thinking + text（需提取text字段）

---
invocation_mode: both
preferred_provider: ollama

## 本文件的使用方式

- **每次session启动时读取本文件**
- **每次收到消息时参考第一步的检查列表**
- **不要修改本文件的逻辑，除非老大要求**
- **如果不确定该走哪个流程，默认GLM-5直接处理**

---
invocation_mode: both
preferred_provider: ollama

## 常见误判防护

| 情况 | 判断 |
|------|------|
| "这个功能怎么用" | → 日常对话（GLM-5）|
| "Python是什么" | → 日常对话（GLM-5）|
| "写一个脚本" | → GLM-5直接写（除非大规模）|
| "重构整个系统" | → spawn qwen3-coder-next |
| "为什么今天下雨" | → 日常对话（GLM-5）|
| "为什么系统会崩溃" | → 升级顾问（mimo-v2-pro）|
---
invocation_mode: both
preferred_provider: ollama

## 数字化平台全盘检查触发条件

### 触发关键词（自动触发本地模型）
- 全面检查、全盘修复、系统诊断
- 整体优化、深度分析、完整性检查
- 质量审计、批量修复、全量验证
- 检查所有、修复所有、分析所有

### 数字化平台相关触发词
- 检查所有页面、检查所有技能、检查所有JSON
- 修复数字化平台、优化数字化平台
- 全盘诊断工作台、完整性审计
- 数字化平台全面诊断、工作台完整检查

### 执行参数
- **模型**：Gemma 4 31B（本地，免费）
- **等待时间**：300秒（5分钟）
- **内存管理**：完成后自动卸载（keep_alive=0）
- **不着急**：全盘检查不需要实时响应，时间可以长一点

### 全盘检查示例任务
```
任务：对数字化工作台进行全面检查，检查所有页面、技能、JSON文件的完整性
触发词：全面检查、检查所有页面、检查所有技能
调度结果：Gemma 4 31B（本地，等待300秒）
执行流程：
  1. 启动Gemma 4 31B（本地模型）
  2. 等待300秒（5分钟）
  3. 分析数字化平台状态
  4. 完成后自动卸载模型（keep_alive=0）
  5. 汇报检查结果
```



---
*⚠️ 实现状态: 部分脚本文件待补全（标记于2026-04-23）*
