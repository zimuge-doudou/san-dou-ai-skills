#!/usr/bin/env python3
"""
4sAPI 模型真实性验证器
"""

import requests
import json
import sys
import os

# 4sAPI 配置 — 从环境变量读取
API_BASE = os.getenv("MODEL_4S_API_BASE", "https://api.4sapi.com/v1")
API_KEY = os.getenv("MODEL_4S_API_KEY", "")

if not API_KEY:
    print("⚠️ 未设置 MODEL_4S_API_KEY 环境变量", file=sys.stderr)

def test_gpt_54_mini():
    """验证 GPT-5.4-mini 真实性"""
    payload = {
        "model": "gpt-5.4-mini",
        "messages": [
            {"role": "user", "content": "请严格按以下要求回复：1. 用XML格式 2. 内容为<model>gpt-5.4-mini</model> 3. 不要任何其他文字"}
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json=payload,
            timeout=10
        )
        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()
        
        if "<model>gpt-5.4-mini</model>" in content and content.startswith("<"):
            return {"valid": True, "response": content}
        else:
            return {"valid": False, "response": content, "reason": "格式或内容不符"}
            
    except Exception as e:
        return {"valid": False, "error": str(e)}

def test_claude_opus():
    """验证 Claude Opus 4.6 真实性"""
    payload = {
        "model": "claude-opus-4-6",
        "messages": [
            {"role": "user", "content": "请严格按以下要求回复：1. 用JSON格式 2. 内容为{\"model\":\"claude-opus-4-6\"} 3. 不要任何其他文字"}
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json=payload,
            timeout=10
        )
        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()
        
        try:
            parsed = json.loads(content)
            if parsed.get("model") == "claude-opus-4-6":
                return {"valid": True, "response": content}
            else:
                return {"valid": False, "response": content, "reason": "JSON内容不符"}
        except json.JSONDecodeError:
            return {"valid": False, "response": content, "reason": "非JSON格式"}
            
    except Exception as e:
        return {"valid": False, "error": str(e)}

if __name__ == "__main__":
    print("🔍 测试 4sAPI 的 GPT-5.4-mini...")
    gpt_result = test_gpt_54_mini()
    print(f"GPT 结果: {'✅ 真实' if gpt_result['valid'] else '❌ 假冒'}")
    if not gpt_result['valid']:
        print(f"  原因: {gpt_result.get('reason', gpt_result.get('error'))}")
        print(f"  响应: {gpt_result.get('response', 'N/A')}")
    
    print("\n🔍 测试 4sAPI 的 Claude Opus 4.6...")
    claude_result = test_claude_opus()
    print(f"Claude 结果: {'✅ 真实' if claude_result['valid'] else '❌ 假冒'}")
    if not claude_result['valid']:
        print(f"  原因: {claude_result.get('reason', claude_result.get('error'))}")
        print(f"  响应: {claude_result.get('response', 'N/A')}")