# san-dou-ai-skills

三豆（SanDou）AI Agent 系统自用的技能模块集合。

这些技能原本服务于四台机器上的 Agent（豆苗 / 豆豆 / 毛豆 / 刘小豆），
覆盖图像识别、浏览器自动化、PDF 报告与模型路由四件事。开源出来是因为
它们足够通用，也可能对同样在搭 Agent 的人有用。

## 📦 技能列表（4 个）

| 技能 | 能力 | 实测入口 |
|:--|:--|:--|
| `skill_auto_image_recognition` | 收到图片时调用视觉模型识别并回述内容 | `from skills.skill_auto_image_recognition.mimo_image_recognize import recognize_image` |
| `skill_browser_use_ai` | 用自然语言驱动网页操作 | `from skills.skill_browser_use_ai.browser_use_ai_impl import get_usage_guide` |
| `skill_pdf_report` | 生成 ASCII 版式的报告（项目/设备/审计三模板） | `from skills.skill_pdf_report import PdfReport` |
| `skill_model_router` | 按消息类型与是否带图，路由到不同模型 + 降级 | `from skills.skill_model_router import ModelRouter` |

> 每个技能目录下都有 `SKILL.md` 说明用途与命令。**上表中列出的导入路径均已实测可跑。**

## 🚀 快速开始

```bash
git clone https://github.com/zimuge-doudou/san-dou-ai-skills.git
cd san-dou-ai-skills
pip install -r requirements.txt
```

### 示例

```python
# 图片识别（需先设 MIMO_API_KEY 环境变量）
from skills.skill_auto_image_recognition.mimo_image_recognize import recognize_image
result = recognize_image("path/to/image.jpg")
print(result)
```

```python
# PDF 报告
from skills.skill_pdf_report.pdf_report import generate_project_report
generate_project_report(data)   # data 为 dict，含 title / sections / items
```

```python
# 模型路由
from skills.skill_model_router.skill_model_router_impl import route
decision = route("帮我看看这张图", has_image=True)
print(decision)
```

## ⚙️ 配置

技能通过环境变量读取密钥，**不含任何硬编码凭据**：

| 变量 | 用途 |
|:--|:--|
| `MIMO_API_KEY` | 小米 MiMo 视觉模型（图片识别） |
| `QWEN_API_KEY` | 通义千问视觉模型（备选） |

## 📚 文档

- [快速开始](docs/getting-started.md)
- [技能指南](docs/skills-guide.md)
- [贡献指南](CONTRIBUTING.md)

## ⚠️ 说明

- 这些技能来自真实生产环境，代码风格和依赖偏向"能用优先"，不是教科书示例。
- 部分技能面向中文场景（如报告模板）。
- 依赖见 `requirements.txt`；其中 `playwright` 仅浏览器技能需要，装完需 `playwright install`。

## 🤝 贡献

欢迎 PR。请先读 [贡献指南](CONTRIBUTING.md)。

## 📄 许可证

[MIT](LICENSE)
