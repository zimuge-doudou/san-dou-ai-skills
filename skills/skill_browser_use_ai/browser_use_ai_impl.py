#!/usr/bin/env python3
"""
skill_browser_use_ai - AI自动化浏览器技能实现
使用OpenClaw内置browser工具完成复杂网页操作
"""

import sys
import json
import os
import subprocess
from pathlib import Path

WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', Path.home() / '.openclaw' / 'workspace'))


def check_browser_env():
    """检查浏览器环境是否就绪"""
    results = {
        'playwright': False,
        'browser_use': False,
        'openclaw_browser': True  # OpenClaw内置browser工具
    }
    
    # Check playwright
    try:
        result = subprocess.run(
            ['python3', '-c', 'import playwright; print(playwright.__version__)'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            results['playwright'] = True
            results['playwright_version'] = result.stdout.strip()
    except:
        pass
    
    # Check browser-use
    try:
        result = subprocess.run(
            ['python3', '-c', 'import browser_use; print(browser_use.__version__)'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            results['browser_use'] = True
    except:
        pass
    
    return results


def get_usage_guide():
    """返回使用指南"""
    return """
Browser Use AI 使用方式：

1. OpenClaw内置browser工具（推荐）：
   - 自动处理JS渲染
   - 支持截图、点击、填写等操作
   - 适用于抖音/B站/12306/电商等复杂网站

2. browser-use Python库（高级）：
   - 适合批量自动化任务
   - 需要API Key配置

3. 常见操作指令：
   - "打开抖音搜索XXX" → browser工具自动导航+截图
   - "截取B站视频封面" → browser导航+截图
   - "12306查询车票" → browser自动操作

注意：识图铁律 — 收到图片必须用命令行识别，禁止内置视觉
"""


if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'check':
            results = check_browser_env()
            print(json.dumps(results, indent=2, ensure_ascii=False))
        elif cmd == 'guide':
            print(get_usage_guide())
        else:
            print(f"未知命令: {cmd}")
    else:
        print(get_usage_guide())