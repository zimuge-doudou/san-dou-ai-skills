#!/usr/bin/env python3
"""
视觉识别自动路由（2026-05-20建立）
当前主模型可能不具备识图能力，此脚本自动选择最优识别方式。
降级链：image工具 → qwen3-vl:235b → 备选
"""

import sys
import os
import json

# 方案1: OpenClaw image工具（如果有视觉能力的主模型）
# 方案2: Ollama qwen3-vl:235b（独立识图模型，不受主模型切换影响）
# 方案3: xiaomi/mimo-v2.5（有视觉能力）

FALLBACK_CHAIN = [
    {
        "name": "独立识图模型",
        "script": os.path.join(os.path.dirname(__file__), "qwen_image_recognize.py"),
        "cmd": "python3 {script} '{path}' '{prompt}'",
        "requires": "OLLAMA_API_KEY",
        "model": "qwen3-vl:235b",
        "reliable": True,
    },
]


def route_recognition(image_path: str, prompt: str = "") -> dict:
    """
    自动路由识图请求到最优方式。
    优先使用独立识图脚本（最稳定，不受主模型切换影响）。
    """
    import subprocess
    
    # 直接用独立识图模型（不受主模型切换影响，最稳定）
    script = FALLBACK_CHAIN[0]["script"]
    if not os.path.exists(script):
        return {"error": f"识图脚本不存在: {script}"}
    
    prompt_arg = prompt or "请详细识别这张图片中的所有内容，用中文回复。"
    cmd = f"python3 {script} '{image_path}' '{prompt_arg}'"
    
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=90
        )
        if result.returncode == 0:
            return {"success": True, "content": result.stdout.strip(), "method": "qwen3-vl:235b"}
        else:
            return {"error": result.stderr.strip()[:500], "method": "qwen3-vl:235b"}
    except subprocess.TimeoutExpired:
        return {"error": "识图超时90秒", "method": "qwen3-vl:235b"}
    except Exception as e:
        return {"error": str(e), "method": "qwen3-vl:235b"}


def check_visual_capability() -> dict:
    """检查当前主模型是否有视觉能力"""
    model = os.environ.get("OPENCLAW_MODEL", "unknown")
    
    # deepseek-v4-pro: text only
    # deepseek-v4-flash: text only
    # kimi-k2.6: text only
    # glm-5.1: text + image
    # qwen3.6-plus: text + image
    # mimo-v2.5: text + image
    
    vision_models = ["glm-5", "qwen", "mimo", "gemini", "gpt-4o", "claude"]
    has_vision = any(vm in model.lower() for vm in vision_models)
    
    return {
        "current_model": model,
        "has_vision": has_vision,
        "recommendation": "use_builtin_image_tool" if has_vision else "use_fallback_script",
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"usage": "python3 vision_router.py <image_path> [prompt]"}, ensure_ascii=False, indent=2))
        # 同时输出能力检查
        capability = check_visual_capability()
        print(json.dumps({"capability": capability}, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    image_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else ""
    
    result = route_recognition(image_path, prompt)
    if result.get("success"):
        print(result["content"])
    else:
        print(f"❌ 识图失败: {result.get('error', '未知错误')}", file=sys.stderr)
        sys.exit(1)
