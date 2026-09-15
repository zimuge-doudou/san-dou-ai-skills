# 快速开始

## 安装

```bash
git clone https://github.com/zimuge-doudou/san-dou-ai-skills.git
cd san-dou-ai-skills
pip install -r requirements.txt
```

## 配置密钥

技能从环境变量读密钥，不硬编码：

```bash
export MIMO_API_KEY="<your-mimo-api-key>"    # 图片识别（小米 MiMo）
export QWEN_API_KEY="<your-qwen-api-key>"    # 图片识别备选（通义千问）
```

或用 `.env` 文件配合 `python-dotenv`。

## 示例

### 图片识别

```python
from skills.skill_auto_image_recognition.mimo_image_recognize import recognize_image

result = recognize_image("path/to/image.jpg")
print(result)
```

### PDF 报告

```python
from skills.skill_pdf_report.pdf_report import generate_project_report

generate_project_report({
    "title": "项目周报",
    "sections": [{"heading": "进展", "body": "本周完成 X"}],
})
```

### 模型路由

```python
from skills.skill_model_router.skill_model_router_impl import route

decision = route("帮我看看这张图", has_image=True)
print(decision)   # {'model': ..., 'provider': ...}

# 降级
from skills.skill_model_router.skill_model_router_impl import get_fallback
print(get_fallback("some-model"))
```

### 浏览器自动化

```python
from skills.skill_browser_use_ai.browser_use_ai_impl import get_usage_guide

print(get_usage_guide())
```

首次使用浏览器技能需要装浏览器内核：

```bash
playwright install
```

## 下一步

- 浏览[技能指南](skills-guide.md)了解各技能细节
- 阅读[贡献指南](../CONTRIBUTING.md)
