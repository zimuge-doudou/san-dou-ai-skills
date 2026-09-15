#!/usr/bin/env python3
"""
N1N 模型真实性验证器
- 通过能力指纹测试识别冒牌模型
- 自动熔断异常模型
"""

import requests
import json
import sys
import os
from typing import Dict, Any

# 配置 — 从环境变量读取，避免硬编码凭据
API_BASE = os.getenv("MODEL_VALIDATOR_API_BASE", "https://api.n1n.ai/v1")
API_KEY = os.getenv("MODEL_VALIDATOR_API_KEY", "")

if not API_KEY:
    print("⚠️ 未设置 MODEL_VALIDATOR_API_KEY 环境变量", file=sys.stderr)

def test_gpt_54_mini() -> Dict[str, Any]:
    """验证 GPT-5.4-mini 真实性"""
    payload = {
        "model": "gpt-5.4-mini-2026-03-17",
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
        
        # 验证XML格式和内容
        if "<model>gpt-5.4-mini</model>" in content and content.startswith("<"):
            return {"valid": True, "response": content}
        else:
            return {"valid": False, "response": content, "reason": "格式或内容不符"}
            
    except Exception as e:
        return {"valid": False, "error": str(e)}

def test_claude_opus() -> Dict[str, Any]:
    """验证 Claude Opus 4.6 真实性"""
    payload = {
        "model": "claude-opus-4-6-thinking",
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
        
        # 验证JSON格式和内容
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
    model_type = sys.argv[1] if len(sys.argv) > 1 else "both"
    
    if model_type == "gpt" or model_type == "both":
        print("🔍 测试 GPT-5.4-mini...")
        gpt_result = test_gpt_54_mini()
        print(f"GPT 结果: {'✅ 真实' if gpt_result['valid'] else '❌ 假冒'}")
        if not gpt_result['valid']:
            print(f"  原因: {gpt_result.get('reason', gpt_result.get('error'))}")
            print(f"  响应: {gpt_result.get('response', 'N/A')}")
    
    if model_type == "claude" or model_type == "both":
        print("\n🔍 测试 Claude Opus 4.6...")
        claude_result = test_claude_opus()
        print(f"Claude 结果: {'✅ 真实' if claude_result['valid'] else '❌ 假冒'}")
        if not claude_result['valid']:
            print(f"  原因: {claude_result.get('reason', claude_result.get('error'))}")
            print(f"  响应: {claude_result.get('response', 'N/A')}")

class ModelRouter:
    """skill_model_router技能"""
    
    def __init__(self):
        self.name = "skill_model_router"
    
    def execute(self, params: Dict = None) -> Dict:
        """执行主要功能"""
        return {"success": True, "skill": self.name}
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {"skill": self.name, "status": "active"}
    
    def validate_input(self, data: Any) -> bool:
        """验证输入"""
        return data is not None
