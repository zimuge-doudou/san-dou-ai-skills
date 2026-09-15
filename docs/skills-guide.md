# 技能指南

本仓库包含 **4 个**技能模块。每个技能是一个独立目录，含 `SKILL.md`（说明）+ 实现文件。

## 目录结构

```
skills/
└── skill_name/
    ├── SKILL.md              # 技能说明（用途、命令、触发条件）
    ├── __init__.py           # 导出入口
    ├── skill_name_impl.py    # 主要实现
    └── config.json           # 可选配置
```

## 技能清单

### skill_auto_image_recognition

图片识别。收到图片时调用视觉模型（小米 MiMo / 通义千问）识别内容并回述。

```python
from skills.skill_auto_image_recognition.mimo_image_recognize import recognize_image
recognize_image("photo.jpg")
```

需要 `MIMO_API_KEY`。含缓存、健康检查与错误处理 mixin。

### skill_browser_use_ai

浏览器自动化。用自然语言描述目标，由 AI 理解页面并执行操作。

```python
from skills.skill_browser_use_ai.browser_use_ai_impl import (
    check_browser_env, get_usage_guide,
)
check_browser_env()   # 先确认环境
print(get_usage_guide())
```

需要 `playwright` 及浏览器内核（`playwright install`）。

### skill_pdf_report

生成 ASCII 版式的报告。三个模板：项目报告、设备清单、审计报告。

```python
from skills.skill_pdf_report.pdf_report import (
    generate_project_report,
    generate_equipment_report,
    generate_audit_report,
)
generate_project_report(data)
```

注意：输出是**纯文本排版的"伪 PDF"**（ASCII 艺术模拟版式），不是真正的 PDF 二进制文件。

### skill_model_router

模型路由。根据消息内容与是否带图，选择模型并支持失败降级。

```python
from skills.skill_model_router import ModelRouter
from skills.skill_model_router.skill_model_router_impl import route, get_fallback, list_models

print(list_models())
decision = route("解释这段代码", has_image=False)
print(get_fallback(decision["model"]))
```

附带模型健康校验与同步检查工具（`model_validator.py` / `model_sync_check.py`）。

## 调用方式

技能支持两种调用：

1. **Python 导入**（推荐）：见上面各示例
2. **命令行**：部分技能有 `main()` 入口，可 `python -m skills.<name>.<impl>`

## 注意事项

- 环境变量名见 README 的配置表；缺密钥时技能会警告并返回占位结果，不会崩溃。
- 技能面向中文场景设计，部分内置文案是中文。
