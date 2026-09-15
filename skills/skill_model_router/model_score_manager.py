#!/usr/bin/env python3
"""模型评分和降级管理"""

import json
from datetime import datetime
from pathlib import Path


class ModelScoreManager:
    def __init__(self, scores_file=None):
        self.scores_file = Path(scores_file or "~/.openclaw/workspace/memory/model_scores.json").expanduser()
        self.load_scores()
    
    def load_scores(self):
        if self.scores_file.exists():
            with open(self.scores_file) as f:
                self.data = json.load(f)
        else:
            self.data = self._default_scores()
    
    def _default_scores(self):
        return {
            "models": {},
            "thresholds": {
                "upgrade_threshold": 3,
                "downgrade_threshold": 5,
                "low_score_threshold": 60,
                "warning_threshold": 70
            },
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }
    
    def record_score(self, model, score, task_type):
        """记录模型评分"""
        if model not in self.data["models"]:
            self.data["models"][model] = {
                "role": "unknown",
                "total_tasks": 0,
                "avg_score": 0,
                "low_score_count": 0,
                "status": "active"
            }
        
        m = self.data["models"][model]
        m["total_tasks"] += 1
        m["avg_score"] = (m["avg_score"] * (m["total_tasks"] - 1) + score) / m["total_tasks"]
        
        if score < self.data["thresholds"]["low_score_threshold"]:
            m["low_score_count"] += 1
        
        self._check_status(model)
        self.save()
    
    def _check_status(self, model):
        """检查模型状态"""
        m = self.data["models"][model]
        threshold = self.data["thresholds"]["downgrade_threshold"]
        
        if m["low_score_count"] >= threshold:
            m["status"] = "degraded"
        elif m["low_score_count"] >= threshold - 2:
            m["status"] = "warning"
    
    def get_recommendation(self):
        """获取模型推荐"""
        recommendations = []
        for model, data in self.data["models"].items():
            if data["status"] == "degraded":
                recommendations.append(f"⚠️ {model} 已降级，连续{data['low_score_count']}次低分")
            elif data["status"] == "warning":
                recommendations.append(f"🟡 {model} 警告，评分接近降级阈值")
        return recommendations
    
    def save(self):
        self.data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        with open(self.scores_file, "w") as f:
            json.dump(self.data, f, indent=2)


if __name__ == "__main__":
    manager = ModelScoreManager()
    print("📊 模型评分系统已初始化")
    rec = manager.get_recommendation()
    if rec:
        for r in rec:
            print(r)
    else:
        print("✅ 所有模型状态正常")