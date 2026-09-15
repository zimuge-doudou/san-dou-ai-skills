#!/usr/bin/env python3
"""
图片识别脚本 v2 — 使用xiaomi-token mimo-v2.5（支持text/image/video/audio）
"""
import base64
import sys
import time
import requests
from pathlib import Path
import os

# 优先用xiaomi-token，降级到ollama
XIAOMI_API_KEY = os.environ.get("MIMO_API_KEY", "")
if not XIAOMI_API_KEY:
    print("⚠️ 未设置 MIMO_API_KEY 环境变量", file=sys.stderr)
    sys.exit(1)
OLLAMA_API_KEY = os.environ.get("OLLAMA_API_KEY", "")
XIAOMI_URL = "https://token-plan-cn.xiaomimimo.com/v1/chat/completions"
OLLAMA_URL = "https://ollama.com/v1/chat/completions"

SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}
MAX_IMAGE_SIZE = 10 * 1024 * 1024


def get_mime_type(path: str) -> str:
    ext = Path(path).suffix.lower()
    mime_map = {
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
        ".gif": "image/gif", ".webp": "image/webp", ".bmp": "image/bmp",
    }
    return mime_map.get(ext, "image/jpeg")


def encode_image_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def call_api(base_url, api_key, model, prompt, base64_image, mime_type, timeout=90):
    """调用API"""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": model,
        "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}},
            {"type": "text", "text": prompt}
        ]}],
        "max_tokens": 4000
    }
    resp = requests.post(base_url, headers=headers, json=data, timeout=timeout)
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"]
    raise Exception(f"API {resp.status_code}: {resp.text[:200]}")


def recognize_image(image_path: str, prompt: str = None) -> dict:
    path = Path(image_path)
    if not path.exists():
        return {"error": f"文件不存在: {image_path}"}
    if path.suffix.lower() not in SUPPORTED_FORMATS:
        return {"error": f"不支持的格式: {path.suffix}"}
    if path.stat().st_size > MAX_IMAGE_SIZE:
        return {"error": f"文件过大: {path.stat().st_size/1024/1024:.1f}MB"}

    base64_image = encode_image_base64(image_path)
    mime_type = get_mime_type(image_path)
    if not prompt:
        prompt = "请详细识别这张图片中的所有文字内容和结构，用中文回复。如果是表格，请还原表格结构。"

    # 降级链：mimo-v2.5 → ollama qwen3-vl
    attempts = [
        ("xiaomi-token/mimo-v2.5", XIAOMI_URL, XIAOMI_API_KEY, "mimo-v2.5"),
    ]
    if OLLAMA_API_KEY:
        attempts.append(("ollama/qwen3-vl", OLLAMA_URL, OLLAMA_API_KEY, "qwen3-vl:235b"))

    for name, url, key, model in attempts:
        start = time.time()
        try:
            content = call_api(url, key, model, prompt, base64_image, mime_type)
            return {"success": True, "content": content, "elapsed": time.time()-start, "model": name}
        except Exception as e:
            print(f"⚠️ {name} 失败: {e}", file=sys.stderr)
            continue

    return {"error": "所有模型均失败"}


def main():
    if len(sys.argv) < 2:
        print("用法: python3 qwen_image_recognize.py <图片路径> [提示词]")
        sys.exit(1)
    result = recognize_image(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    if result.get("success"):
        print(result["content"])
    else:
        print(f"❌ 识别失败: {result.get('error')}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
