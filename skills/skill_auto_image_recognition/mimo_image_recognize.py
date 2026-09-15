#!/usr/bin/env python3
"""
MiMo-V2-Omni 图片识别脚本
统一使用小米MiMo全模态模型进行图像识别
"""

import base64
import json
import os
import sys
import time
import requests
from pathlib import Path

# 配置 — 从环境变量读取API密钥
API_KEY = os.getenv("MIMO_API_KEY", "")
if not API_KEY:
    print("⚠️ 未设置 MIMO_API_KEY 环境变量", file=sys.stderr)
BASE_URL = "https://token-plan-cn.xiaomimimo.com/v1"
MODEL = "mimo-v2.5"

SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB


def get_mime_type(path: str) -> str:
    """根据扩展名获取MIME类型"""
    ext = Path(path).suffix.lower()
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
    }
    return mime_map.get(ext, "image/jpeg")


def encode_image_base64(image_path: str) -> str:
    """将图片编码为Base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def recognize_image(image_path: str, prompt: str = None) -> dict:
    """
    调用MiMo-V2-Omni识别图片

    Args:
        image_path: 图片文件路径
        prompt: 自定义提示词（可选）

    Returns:
        识别结果字典
    """
    path = Path(image_path)

    # 验证文件
    if not path.exists():
        return {"error": f"文件不存在: {image_path}"}

    if path.suffix.lower() not in SUPPORTED_FORMATS:
        return {"error": f"不支持的格式: {path.suffix}，支持: {SUPPORTED_FORMATS}"}

    if path.stat().st_size > MAX_IMAGE_SIZE:
        return {"error": f"文件过大: {path.stat().st_size / 1024 / 1024:.1f}MB，最大10MB"}

    # 编码图片
    base64_image = encode_image_base64(image_path)
    mime_type = get_mime_type(image_path)

    # 默认提示词
    if not prompt:
        prompt = "请详细识别这张图片中的所有文字内容和结构，用中文回复。如果是表格，请还原表格结构。"

    # 构建请求
    url = f"{BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "max_tokens": 4000
    }

    # 发送请求
    start_time = time.time()
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        elapsed = time.time() - start_time

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return {
                "success": True,
                "content": content,
                "elapsed": elapsed,
                "model": MODEL,
                "image": str(path.name)
            }
        else:
            return {
                "error": f"API错误: {response.status_code}",
                "detail": response.text[:200],
                "elapsed": elapsed
            }

    except requests.exceptions.Timeout:
        return {"error": "API请求超时（60秒）"}
    except Exception as e:
        return {"error": f"请求异常: {str(e)}"}


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 mimo_image_recognize.py <图片路径> [提示词]")
        print("示例: python3 mimo_image_recognize.py photo.jpg")
        print("      python3 mimo_image_recognize.py photo.jpg '识别表格内容'")
        sys.exit(1)

    image_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else None

    result = recognize_image(image_path, prompt)

    if result.get("success"):
        print(result["content"])
    else:
        print(f"❌ 识别失败: {result.get('error', '未知错误')}")
        if "detail" in result:
            print(f"详情: {result['detail']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
