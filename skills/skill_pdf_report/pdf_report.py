#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF报告生成器 - 生成纯文本格式的"伪PDF"报告
支持模板：项目报告、设备清单、审计报告
"""

import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

# ─── 常量 ───
REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
LINE_WIDTH = 72
DOUBLE_LINE = "═" * LINE_WIDTH
SINGLE_LINE = "─" * LINE_WIDTH
THIN_LINE = "·" * LINE_WIDTH

# ─── 模板定义 ───
TEMPLATES = {
    "项目报告": {
        "title": "项目进度报告",
        "fields": ["项目名称", "负责人", "状态", "进度", "备注"],
        "sections": ["项目概况", "进度详情", "存在问题", "下一步计划"],
    },
    "设备清单": {
        "title": "设备清单报告",
        "fields": ["设备名称", "型号", "数量", "状态", "存放位置"],
        "sections": ["设备统计", "设备明细", "状态汇总"],
    },
    "审计报告": {
        "title": "系统审计报告",
        "fields": ["检查项", "检查结果", "风险等级", "建议措施"],
        "sections": ["审计概览", "检查详情", "风险汇总", "整改建议"],
    },
}


def center_text(text, width=LINE_WIDTH):
    """居中文本"""
    return text.center(width)


def right_text(text, width=LINE_WIDTH):
    """右对齐文本"""
    return text.rjust(width)


def format_table(headers, rows, col_widths=None):
    """格式化表格"""
    if not col_widths:
        all_rows = [headers] + rows
        col_widths = []
        for i in range(len(headers)):
            max_w = max(len(str(r[i])) if i < len(r) else 0 for r in all_rows)
            col_widths.append(max(max_w, len(headers[i])) + 2)

    lines = []
    # 表头
    header_line = "│"
    for h, w in zip(headers, col_widths):
        header_line += f" {h:<{w-1}}│"
    lines.append(header_line)

    # 分隔线
    sep = "├"
    for w in col_widths:
        sep += "─" * w + "┼"
    lines.append(sep.rstrip("┼") + "┤")

    # 数据行
    for row in rows:
        row_line = "│"
        for i, w in enumerate(col_widths):
            val = str(row[i]) if i < len(row) else ""
            row_line += f" {val:<{w-1}}│"
        lines.append(row_line)

    # 底线
    bottom = "└"
    for w in col_widths:
        bottom += "─" * w + "┴"
    lines.append(bottom.rstrip("┴") + "┘")

    # 顶线
    top = "┌"
    for w in col_widths:
        top += "─" * w + "┬"
    lines.insert(0, top.rstrip("┬") + "┐")

    return "\n".join(lines)


def generate_project_report(data):
    """生成项目报告"""
    lines = []
    lines.append(DOUBLE_LINE)
    lines.append(center_text("📋 项目进度报告"))
    lines.append(DOUBLE_LINE)
    lines.append(f"  生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"  报告编号：RPT-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    lines.append(SINGLE_LINE)

    # 项目概况
    lines.append("")
    lines.append("  【一、项目概况】")
    lines.append(THIN_LINE)
    project_name = data.get("项目名称", "未命名项目")
    manager = data.get("负责人", "未指定")
    status = data.get("状态", "进行中")
    progress = data.get("进度", 0)
    lines.append(f"  项目名称：{project_name}")
    lines.append(f"  负责人  ：{manager}")
    lines.append(f"  当前状态：{status}")
    lines.append(f"  整体进度：{'█' * (progress // 5)}{'░' * (20 - progress // 5)} {progress}%")
    lines.append("")

    # 进度详情
    lines.append("  【二、进度详情】")
    lines.append(THIN_LINE)
    items = data.get("进度详情", [])
    if items:
        headers = ["阶段", "状态", "完成度", "负责人"]
        rows = []
        for item in items:
            p = item.get("完成度", 0)
            bar = f"{'█' * (p // 10)}{'░' * (10 - p // 10)} {p}%"
            rows.append([
                item.get("阶段", ""),
                item.get("状态", ""),
                bar,
                item.get("负责人", ""),
            ])
        lines.append(format_table(headers, rows))
    else:
        lines.append("  （暂无进度详情）")
    lines.append("")

    # 存在问题
    lines.append("  【三、存在问题】")
    lines.append(THIN_LINE)
    problems = data.get("存在问题", [])
    if problems:
        for i, p in enumerate(problems, 1):
            desc = p if isinstance(p, str) else p.get("描述", str(p))
            level = "" if isinstance(p, str) else f" [{p.get('严重程度', '一般')}]"
            lines.append(f"  {i}. {desc}{level}")
    else:
        lines.append("  ✓ 暂无问题")
    lines.append("")

    # 下一步计划
    lines.append("  【四、下一步计划】")
    lines.append(THIN_LINE)
    plans = data.get("下一步计划", [])
    if plans:
        for i, p in enumerate(plans, 1):
            desc = p if isinstance(p, str) else p.get("描述", str(p))
            deadline = "" if isinstance(p, str) else f" (截止：{p.get('截止日期', '待定')})"
            lines.append(f"  {i}. {desc}{deadline}")
    else:
        lines.append("  （暂无计划）")

    # 页脚
    lines.append("")
    lines.append(DOUBLE_LINE)
    lines.append(center_text("— 报告结束 —"))
    lines.append(center_text(f"豆豆AI 自动生成 | {datetime.now().strftime('%Y-%m-%d')}"))
    lines.append(DOUBLE_LINE)

    return "\n".join(lines)


def generate_equipment_report(data):
    """生成设备清单报告"""
    lines = []
    lines.append(DOUBLE_LINE)
    lines.append(center_text("🔧 设备清单报告"))
    lines.append(DOUBLE_LINE)
    lines.append(f"  生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"  报告编号：EQP-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    lines.append(SINGLE_LINE)

    # 设备统计
    lines.append("")
    lines.append("  【一、设备统计】")
    lines.append(THIN_LINE)
    items = data.get("设备列表", data.get("设备", []))
    total = len(items)
    total_qty = sum(item.get("数量", 1) for item in items)
    status_count = {}
    for item in items:
        s = item.get("状态", "未知")
        status_count[s] = status_count.get(s, 0) + 1
    lines.append(f"  设备种类：{total} 种")
    lines.append(f"  设备总量：{total_qty} 台/件")
    for s, c in status_count.items():
        lines.append(f"  {s}：{c} 种")
    lines.append("")

    # 设备明细
    lines.append("  【二、设备明细】")
    lines.append(THIN_LINE)
    if items:
        headers = ["序号", "设备名称", "型号", "数量", "状态", "位置"]
        rows = []
        for i, item in enumerate(items, 1):
            rows.append([
                str(i),
                item.get("设备名称", item.get("名称", "")),
                item.get("型号", "-"),
                str(item.get("数量", 1)),
                item.get("状态", "未知"),
                item.get("存放位置", item.get("位置", "-")),
            ])
        lines.append(format_table(headers, rows))
    else:
        lines.append("  （暂无设备数据）")
    lines.append("")

    # 状态汇总
    lines.append("  【三、状态汇总】")
    lines.append(THIN_LINE)
    if status_count:
        for s, c in sorted(status_count.items()):
            pct = round(c / total * 100) if total else 0
            bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
            lines.append(f"  {s:<8} {bar} {c}种 ({pct}%)")
    else:
        lines.append("  （无状态数据）")

    # 页脚
    lines.append("")
    lines.append(DOUBLE_LINE)
    lines.append(center_text("— 报告结束 —"))
    lines.append(center_text(f"豆豆AI 自动生成 | {datetime.now().strftime('%Y-%m-%d')}"))
    lines.append(DOUBLE_LINE)

    return "\n".join(lines)


def generate_audit_report(data):
    """生成审计报告"""
    lines = []
    lines.append(DOUBLE_LINE)
    lines.append(center_text("🔍 系统审计报告"))
    lines.append(DOUBLE_LINE)
    lines.append(f"  生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"  报告编号：AUD-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    audit_scope = data.get("审计范围", "全系统")
    lines.append(f"  审计范围：{audit_scope}")
    lines.append(SINGLE_LINE)

    # 审计概览
    lines.append("")
    lines.append("  【一、审计概览】")
    lines.append(THIN_LINE)
    items = data.get("检查项", data.get("检查详情", []))
    total_checks = len(items)
    pass_count = sum(1 for i in items if i.get("检查结果", "").lower() in ("通过", "pass", "正常"))
    fail_count = sum(1 for i in items if i.get("检查结果", "").lower() in ("不通过", "fail", "异常"))
    warn_count = total_checks - pass_count - fail_count
    lines.append(f"  检查项目：{total_checks} 项")
    lines.append(f"  通过    ：{pass_count} 项 ✓")
    lines.append(f"  不通过  ：{fail_count} 项 ✗")
    lines.append(f"  待确认  ：{warn_count} 项 ?")
    if total_checks:
        score = round(pass_count / total_checks * 100)
        lines.append(f"  合规率  ：{'█' * (score // 5)}{'░' * (20 - score // 5)} {score}%")
    lines.append("")

    # 检查详情
    lines.append("  【二、检查详情】")
    lines.append(THIN_LINE)
    if items:
        headers = ["序号", "检查项", "结果", "风险等级"]
        rows = []
        for i, item in enumerate(items, 1):
            result = item.get("检查结果", "待检")
            icon = "✓" if result.lower() in ("通过", "pass", "正常") else ("✗" if result.lower() in ("不通过", "fail", "异常") else "?")
            rows.append([
                str(i),
                item.get("检查项", item.get("项目", "")),
                f"{icon} {result}",
                item.get("风险等级", "-"),
            ])
        lines.append(format_table(headers, rows))
    else:
        lines.append("  （暂无检查数据）")
    lines.append("")

    # 风险汇总
    lines.append("  【三、风险汇总】")
    lines.append(THIN_LINE)
    risk_count = {}
    for item in items:
        r = item.get("风险等级", "未知")
        risk_count[r] = risk_count.get(r, 0) + 1
    if risk_count:
        for r, c in sorted(risk_count.items()):
            lines.append(f"  {r}：{c} 项")
    else:
        lines.append("  （无风险数据）")
    lines.append("")

    # 整改建议
    lines.append("  【四、整改建议】")
    lines.append(THIN_LINE)
    suggestions = data.get("整改建议", data.get("建议", []))
    if suggestions:
        for i, s in enumerate(suggestions, 1):
            desc = s if isinstance(s, str) else s.get("建议", s.get("描述", str(s)))
            priority = "" if isinstance(s, str) else f" [优先级：{s.get('优先级', '中')}]"
            lines.append(f"  {i}. {desc}{priority}")
    elif fail_count > 0:
        lines.append("  ⚠ 存在不通过项，请及时整改")
    else:
        lines.append("  ✓ 所有检查项通过，暂无整改建议")

    # 页脚
    lines.append("")
    lines.append(DOUBLE_LINE)
    lines.append(center_text("— 报告结束 —"))
    lines.append(center_text(f"豆豆AI 自动生成 | {datetime.now().strftime('%Y-%m-%d')}"))
    lines.append(DOUBLE_LINE)

    return "\n".join(lines)


def load_data(json_path):
    """加载JSON数据"""
    if not os.path.exists(json_path):
        print(f"错误：文件不存在 - {json_path}")
        sys.exit(1)
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"错误：JSON格式无效 - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"错误：读取文件失败 - {e}")
        sys.exit(1)


def detect_template(data):
    """自动检测模板类型"""
    keys = set(data.keys())
    if "设备列表" in keys or "设备" in keys:
        return "设备清单"
    if "检查项" in keys or "检查详情" in keys or "审计范围" in keys:
        return "审计报告"
    if "项目名称" in keys or "进度详情" in keys:
        return "项目报告"
    return None


def save_report(content, template_name):
    """保存报告文件"""
    os.makedirs(REPORT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{template_name}_{timestamp}.txt"
    filepath = os.path.join(REPORT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath


def cmd_generate(args):
    """生成报告"""
    if not args:
        print("用法：generate <data_json> [--template=项目报告|设备清单|审计报告]")
        sys.exit(1)

    json_path = args[0]
    template = None

    for arg in args[1:]:
        if arg.startswith("--template="):
            template = arg.split("=", 1)[1]

    data = load_data(json_path)

    if not template:
        template = detect_template(data)
        if not template:
            print("错误：无法自动检测模板类型，请使用 --template= 指定")
            print("可用模板：项目报告、设备清单、审计报告")
            sys.exit(1)
        print(f"自动检测模板：{template}")

    generators = {
        "项目报告": generate_project_report,
        "设备清单": generate_equipment_report,
        "审计报告": generate_audit_report,
    }

    if template not in generators:
        print(f"错误：未知模板 '{template}'")
        print(f"可用模板：{', '.join(TEMPLATES.keys())}")
        sys.exit(1)

    content = generators[template](data)
    filepath = save_report(content, template)
    print(f"✓ 报告已生成：{filepath}")
    return filepath


def cmd_templates():
    """列出可用模板"""
    print("可用报告模板：")
    print(SINGLE_LINE)
    for name, info in TEMPLATES.items():
        print(f"  📄 {name}")
        print(f"     标题：{info['title']}")
        print(f"     字段：{', '.join(info['fields'])}")
        print(f"     章节：{', '.join(info['sections'])}")
        print()


def cmd_preview(args):
    """预览报告内容"""
    if not args:
        print("用法：preview <data_json> [--template=项目报告|设备清单|审计报告]")
        sys.exit(1)

    json_path = args[0]
    template = None

    for arg in args[1:]:
        if arg.startswith("--template="):
            template = arg.split("=", 1)[1]

    data = load_data(json_path)

    if not template:
        template = detect_template(data)
        if not template:
            print("错误：无法自动检测模板类型，请使用 --template= 指定")
            sys.exit(1)

    generators = {
        "项目报告": generate_project_report,
        "设备清单": generate_equipment_report,
        "审计报告": generate_audit_report,
    }

    if template not in generators:
        print(f"错误：未知模板 '{template}'")
        sys.exit(1)

    content = generators[template](data)
    print(content)


def main():
    if len(sys.argv) < 2:
        print("PDF报告生成器 - 用法：")
        print("  python pdf_report.py generate <data.json> [--template=项目报告|设备清单|审计报告]")
        print("  python pdf_report.py templates")
        print("  python pdf_report.py preview <data.json> [--template=...]")
        sys.exit(0)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "generate":
        cmd_generate(args)
    elif command == "templates":
        cmd_templates()
    elif command == "preview":
        cmd_preview(args)
    else:
        print(f"错误：未知命令 '{command}'")
        print("可用命令：generate, templates, preview")
        sys.exit(1)


if __name__ == "__main__":
    main()


class PdfReport:
    """skill_pdf_report技能"""
    
    def __init__(self):
        self.name = "skill_pdf_report"
    
    def execute(self, params: Dict = None) -> Dict:
        """执行主要功能"""
        return {"success": True, "skill": self.name}
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {"skill": self.name, "status": "active"}
    
    def validate_input(self, data: Any) -> bool:
        """验证输入"""
        return data is not None
