---
invocation_mode: both
preferred_provider: ollama
name: skill_auto_image_recognition
description: 自动图片识别 - 收到图片时调用MiMo-V2-Omni进行图文识别并汇报结果
priority: P1
metadata:
  author: 豆豆
  category: AI
  version: "2.0"
  model: xiaomi/mimo-v2.5
  trigger: image_received
layer: autonomous
---


invocation_mode: both
preferred_provider: ollama

# 🖼️ 自动图片识别

## 功能说明
- 收到图片时自动触发识别
- 调用 MiMo-V2-Omni 进行图文识别
- 识别完成后向用户汇报内容

## 触发条件
- 用户发送图片消息时自动激活
- 支持 jpg/png/gif/webp 格式

## 输出格式
```
📋 图片识别结果
━━━━━━━━━━━━━
🖼️ 识别内容：[AI识别出的图片内容]
📊 置信度：[识别置信度]
⏱️ 耗时：[识别耗时]
```

## 实际调用方式
```bash
python3 ~/.openclaw/workspace/skills/skill_auto_image_recognition/mimo_image_recognize.py <图片路径>
```

## API配置
- 模型：mimo-v2.5
- Base URL：https://token-plan-cn.xiaomimimo.com/v1
- 认证：api-key

## 命令
- 直接调用脚本识别图片
- 支持自定义提示词（第二个参数）


---
*⚠️ 实现状态: 部分脚本文件待补全（标记于2026-04-23）*
