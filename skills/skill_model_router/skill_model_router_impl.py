#!/usr/bin/env python3
"""模型路由器 v5.0 实际实现 - 基于SKILL.md的7步检查流程"""
import json
import re
from typing import Dict, Optional

# === 模型团队配置（2026-04-13验证版）===
MODELS = {
    "glm-5.1:cloud": {
        "role": "主模型",
        "provider": "ollama_pro",
        "context": "200K",
        "cost": "免费",
        "use": "日常对话、快速问答（覆盖85%任务）",
        "priority": 1
    },
    "gemma4:31b-cloud": {
        "role": "深度推理+识图",
        "provider": "ollama_pro",
        "context": "256K",
        "cost": "免费",
        "use": "深度分析、多模态识图",
        "priority": 2
    },
    "qwen3.6-plus": {
        "role": "识图主力",
        "provider": "bailian_coding",
        "context": "1M",
        "cost": "¥200/月",
        "use": "图片识别",
        "priority": 3
    },
    "qwen3-coder-plus": {
        "role": "代码+报价",
        "provider": "bailian_coding",
        "context": "128K",
        "cost": "¥200/月",
        "use": "代码开发、报价单（9分）",
        "priority": 4
    },
    "kimi-k2.5": {
        "role": "创意产出",
        "provider": "bailian_coding",
        "context": "128K",
        "cost": "¥200/月",
        "use": "CAD/3D/PDF/PPT、文旅报价（8分）",
        "priority": 5
    },
    "mimo-v2-pro": {
        "role": "深度顾问",
        "provider": "xiaomi_mimo",
        "context": "1M",
        "cost": "¥659/月",
        "use": "复杂问题深度推理（100分）",
        "priority": 6
    },
    "mimo-v2.5": {
        "role": "备用识图",
        "provider": "xiaomi_mimo",
        "context": "128K",
        "cost": "¥659/月",
        "use": "qwen3.6-plus不可用时",
        "priority": 7
    },
    "qwen3-max": {
        "role": "超长推理",
        "provider": "bailian_coding",
        "context": "1M",
        "cost": "¥200/月",
        "use": "超长文本分析",
        "priority": 8
    },
    "MiniMax-M2.7-highspeed": {
        "role": "自动化",
        "provider": "ollama_pro",
        "context": "128K",
        "cost": "¥199/月",
        "use": "cron定时任务、自动化脚本",
        "priority": 9
    },
    "glm-5": {
        "role": "备用",
        "provider": "bailian_coding",
        "context": "128K",
        "cost": "¥200/月",
        "use": "日常备用",
        "priority": 10
    }
}

# === 关键词库 ===
SENSITIVE_KW = ["投标", "合同", "竞品", "客户隐私", "投标文件", "商业机密"]  # 去掉'报价'(走产出流)和'内部'(误匹配)
DEEP_CHECK_KW = ["全面检查", "全盘修复", "系统诊断", "整体优化", "深度分析", "完整性检查", "质量审计", "批量修复"]
IMAGE_KW = ["图片", "照片", "截图", "看一下", "识别", "识图"]
DEEP_REASON_KW = ["分析", "策略", "竞品", "技术方案", "深度", "复杂逻辑", "全盘检查"]
OUTPUT_KW = ["CAD", "3D", "PDF", "效果图", "施工图", "方案书", "PPT", "创意", "文旅客户", "报价", "Excel", "成本核算"]
CODE_KW = ["大规模重构", "复杂算法", "高性能代码", "重写整个", "重构系统", "重构整个", "全量重构"]
QUICK_KW = ["快速", "紧急", "马上", "立刻", "急"]

class ModelRouter:
    """模型智能路由器 v5.0"""
    
    def __init__(self):
        self.version = "5.0"
        self.fallback_chain = ["glm-5.1:cloud", "mimo-v2-pro", "mimo-v2.5", "MiniMax-M2.7-highspeed"]
        self.fail_counts = {}  # 模型失败计数
        
    def route(self, message: str, has_image: bool = False, is_automated: bool = False) -> Dict:
        """
        核心路由方法 - 执行SKILL.md的7步检查流程
        返回: {"model": "...", "reason": "...", "method": "direct|spawn|command"}
        """
        msg = message.lower()
        
        # 检查0: 敏感数据或全盘检查
        if self._match(msg, SENSITIVE_KW + DEEP_CHECK_KW):
            if self._match(msg, DEEP_CHECK_KW):
                return {
                    "model": "gemma4:31b-cloud",
                    "reason": "全盘检查任务 → 本地深度推理（免费+隐私）",
                    "method": "spawn",
                    "timeout": 300,
                    "keep_alive": 0
                }
            if self._match(msg, ["投标", "报价", "合同", "竞品"]):
                return {
                    "model": "gemma4:31b-cloud",
                    "reason": "敏感商业数据 → 本地深度推理（隐私保护）",
                    "method": "spawn",
                    "timeout": 180
                }
        
        # 检查1: 图片附件
        if has_image or self._match(msg, IMAGE_KW):
            if self._match(msg, SENSITIVE_KW):
                return {
                    "model": "llava:7b",
                    "reason": "敏感图片 → 本地LLaVA（免费+隐私）",
                    "method": "command",
                    "command": "ollama run llava:7b"
                }
            return {
                "model": "qwen3.6-plus",
                "reason": "图片识别 → qwen3.6-plus（1M上下文，主力识图）",
                "method": "command",
                "command": "python3 ~/.openclaw/workspace/skills/skill_auto_image_recognition/qwen_image_recognize.py"
            }
        
        # 自动化任务
        if is_automated:
            return {
                "model": "MiniMax-M2.7-highspeed",
                "reason": "自动化任务 → MiniMax（Token Plus专用）",
                "method": "direct"
            }
        
        # 检查2: 大规模代码开发（优先于深度推理，避免误判）
        if self._match(msg, CODE_KW):
            return {
                "model": "qwen3-coder-plus",
                "reason": "大规模代码 → qwen3-coder-plus",
                "method": "spawn",
                "timeout": 180
            }
        
        # 检查3: 深度推理
        if self._match(msg, DEEP_REASON_KW):
            if self._match(msg, QUICK_KW):
                return {
                    "model": "mimo-v2-pro",
                    "reason": "深度推理+需快速响应 → mimo-v2-pro（云端100分）",
                    "method": "spawn",
                    "timeout": 120
                }
            return {
                "model": "gemma4:31b-cloud",
                "reason": "深度推理+可慢 → Gemma4:31B本地（免费）",
                "method": "spawn",
                "timeout": 180
            }
        
        # 检查4: 高质量产出
        if self._match(msg, OUTPUT_KW):
            # 报价/Excel/PDF → qwen3-coder-plus(9分)
            if self._match(msg, ["报价", "Excel", "成本", "预算", "清单"]):
                return {
                    "model": "qwen3-coder-plus",
                    "reason": "报价/Excel → qwen3-coder-plus（9分，最专业完整）",
                    "method": "spawn",
                    "timeout": 120
                }
            # PPT/创意/文旅 → kimi-k2.5(8分)
            if self._match(msg, ["PPT", "创意", "文旅", "方案书", "效果图"]):
                return {
                    "model": "kimi-k2.5",
                    "reason": "PPT/创意/文旅 → kimi-k2.5（视觉最佳，中国风）",
                    "method": "spawn",
                    "timeout": 120
                }
            return {
                "model": "kimi-k2.5",
                "reason": "高质量产出 → kimi-k2.5",
                "method": "spawn",
                "timeout": 120
            }
        
        # 检查5: 日常对话 → GLM-5.1主模型
        return {
            "model": "glm-5.1:cloud",
            "reason": "日常对话 → GLM-5.1:cloud主模型（快速响应）",
            "method": "direct"
        }
    
    def get_fallback(self, failed_model: str) -> Optional[Dict]:
        """获取降级模型"""
        try:
            idx = self.fallback_chain.index(failed_model)
            if idx < len(self.fallback_chain) - 1:
                next_model = self.fallback_chain[idx + 1]
                return {
                    "model": next_model,
                    "reason": f"{failed_model}失败 → 降级到{next_model}",
                    "method": "direct"
                }
        except ValueError:
            pass
        return None
    
    def record_failure(self, model: str):
        """记录模型失败"""
        self.fail_counts[model] = self.fail_counts.get(model, 0) + 1
        if self.fail_counts.get(model, 0) >= 5:
            return {"warning": f"{model}连续失败{self.fail_counts[model]}次，建议检查"}
        return None
    
    def get_model_info(self, model_name: str) -> Optional[Dict]:
        """获取模型信息"""
        return MODELS.get(model_name)
    
    def list_models(self) -> Dict:
        """列出所有可用模型"""
        return MODELS
    
    def _match(self, text: str, keywords: list) -> bool:
        """关键词匹配"""
        return any(kw.lower() in text for kw in keywords)


# === 接口函数 ===
def get_info():
    return {"name": "skill_model_router", "version": "5.0", "type": "model_router"}

def route(message: str, has_image: bool = False, is_automated: bool = False) -> Dict:
    router = ModelRouter()
    return router.route(message, has_image, is_automated)

def get_fallback(failed_model: str) -> Optional[Dict]:
    router = ModelRouter()
    return router.get_fallback(failed_model)

def list_models() -> Dict:
    return MODELS

if __name__ == "__main__":
    # 测试路由逻辑
    router = ModelRouter()
    tests = [
        ("帮我写一个报价单", False, False),
        ("识别这张图片", True, False),
        ("全面检查系统", False, False),
        ("重构整个系统", False, False),
        ("你好", False, False),
        ("分析竞品策略", False, False),
        ("做个PPT", False, False),
        ("自动化定时检查", False, True),
    ]
    for msg, img, auto in tests:
        result = router.route(msg, img, auto)
        print(f"输入: {msg[:20]:20s} → 模型: {result['model']:25s} | 原因: {result['reason']}")