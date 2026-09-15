#!/usr/bin/env python3
"""
model_sync_check.py - 模型调度规则同步检查脚本

检查 MEMORY.md 实时切片与 skill_model_router/SKILL.md 是否一致
每次 session 启动时执行

作者：豆豆
版本：v1.0
更新：2026-04-06
"""

import os
import re
import sys

# 文件路径
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
MEMORY_MD = os.path.join(WORKSPACE, "MEMORY.md")
SKILL_MD = os.path.join(WORKSPACE, "skills/skill_model_router/SKILL.md")

def extract_primary_model(content):
    """提取主模型定义"""
    # 从MEMORY.md提取
    match = re.search(r"当前活跃模型.*?`([^`]+)`", content)
    if match:
        return match.group(1)
    return None

def extract_dispatch_rule(content):
    """提取调度口诀"""
    # 从MEMORY.md提取
    match = re.search(r"调度口诀.*?默认 ([^\n]+)", content)
    if match:
        return "默认 " + match.group(1).strip()
    
    # 从SKILL.md提取
    match = re.search(r"调度口诀.*?默认 ([^\n]+)", content)
    if match:
        return "默认 " + match.group(1).strip()
    return None

def check_sync():
    """检查MEMORY.md和SKILL.md是否一致"""
    # 读取MEMORY.md
    try:
        with open(MEMORY_MD, 'r', encoding='utf-8') as f:
            memory_content = f.read()
    except FileNotFoundError:
        print(f"❌ MEMORY.md 不存在: {MEMORY_MD}")
        return False
    
    # 读取SKILL.md
    try:
        with open(SKILL_MD, 'r', encoding='utf-8') as f:
            skill_content = f.read()
    except FileNotFoundError:
        print(f"❌ SKILL.md 不存在: {SKILL_MD}")
        return False
    
    # 提取主模型定义
    memory_primary = extract_primary_model(memory_content)
    skill_primary = "ollama/glm-5.1:cloud"  # SKILL.md v4.0 固定值
    
    # 提取调度口诀
    memory_rule = extract_dispatch_rule(memory_content)
    skill_rule = "默认 GLM-5，不行换 Omni，还不行上 Pro，最后备胎 M2.7"  # SKILL.md v4.0 固定值
    
    # 检查一致性
    print("=" * 50)
    print("📊 模型调度规则同步检查")
    print("=" * 50)
    
    print(f"\n📁 MEMORY.md:")
    print(f"   主模型: {memory_primary}")
    print(f"   调度口诀: {memory_rule}")
    
    print(f"\n📁 SKILL.md:")
    print(f"   主模型: {skill_primary}")
    print(f"   调度口诀: {skill_rule}")
    
    # 比较结果
    primary_match = memory_primary and memory_primary.replace("bailian/", "") == skill_primary.replace("bailian/", "")
    rule_match = memory_rule and "GLM-5" in memory_rule and "Omni" in memory_rule
    
    print(f"\n📊 检查结果:")
    print(f"   主模型一致性: {'✅ 通过' if primary_match else '❌ 不一致'}")
    print(f"   调度口诀一致性: {'✅ 通过' if rule_match else '❌ 不一致'}")
    
    if primary_match and rule_match:
        print(f"\n✅ 同步检查通过")
        return True
    else:
        print(f"\n❌ 同步检查失败，需要修复 MEMORY.md")
        return False

def main():
    """主函数"""
    success = check_sync()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()