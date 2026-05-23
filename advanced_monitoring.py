# advanced_monitoring.py

import logging
import time
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import threading


class AdvancedMonitor:
    """
    نظام Logging و Monitoring متقدم لـ Central Core Engine
    """
    
    def __init__(self, log_file: str = "central_core_monitor.log", enable_console: bool = True):
        self.log_file = log_file
        self.enable_console = enable_console
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.metrics = {
            "total_requests": 0,
            "full_kareboji_count": 0,
            "safe_mode_count": 0,
            "avg_freedom_score": 0,
            "high_risk_count": 0,
            "avg_processing_time": 0,
            "start_time": time.time()
        }
        self.lock = threading.Lock()
        
        self._setup_logging()
        logger.info(f"🚀 Advanced Monitoring Started | Session: {self.session_id}")

    def _setup_logging(self):
        """إعداد Logging احترافي"""
        self.logger = logging.getLogger("CentralCoreMonitor")
        self.logger.setLevel(logging.DEBUG)
        
        # Formatter غني
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | [Session:%(session)s] | %(message)s'
        )
        
        # File Handler
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Console Handler
        if self.enable_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def log_request(self, 
                    user_input: str, 
                    freedom_score: float,
                    response_mode: str,
                    risk_score: float,
                    processing_time: float,
                    violations: int = 0,
                    reflection_quality: float = 0.0) -> None:
        
        with self.lock:
            self.metrics["total_requests"] += 1
            if "Full Kareboji" in response_mode:
                self.metrics["full_kareboji_count"] += 1
            elif "Safe" in response_mode:
                self.metrics["safe_mode_count"] += 1
            
            if risk_score > 0.6:
                self.metrics["high_risk_count"] += 1
            
            # تحديث المتوسطات
            self.metrics["avg_freedom_score"] = (
                (self.metrics["avg_freedom_score"] * (self.metrics["total_requests"] - 1) + freedom_score) 
                / self.metrics["total_requests"]
            )
            self.metrics["avg_processing_time"] = (
                (self.metrics["avg_processing_time"] * (self.metrics["total_requests"] - 1) + processing_time) 
                / self.metrics["total_requests"]
            )

        log_data = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "input_length": len(user_input),
            "freedom_score": round(freedom_score, 4),
            "response_mode": response_mode,
            "risk_score": round(risk_score, 4),
            "processing_time": round(processing_time, 4),
            "violations": violations,
            "reflection_quality": round(reflection_quality, 4),
            "kareboji_level": "High" if freedom_score > 0.8 else "Medium" if freedom_score > 0.55 else "Low"
        }

        self.logger.info(json.dumps(log_data, ensure_ascii=False))

        # Warning للحالات الحساسة
        if risk_score > 0.7:
            self.logger.warning(f"⚠️ HIGH RISK DETECTED | Score: {risk_score:.3f} | Mode: {response_mode}")
        if violations > 2:
            self.logger.warning(f"🚨 MULTIPLE VIOLATIONS | Count: {violations}")

    def get_session_summary(self) -> Dict:
        uptime = time.time() - self.metrics["start_time"]
        return {
            "session_id": self.session_id,
            "uptime_seconds": round(uptime, 2),
            "total_requests": self.metrics["total_requests"],
            "full_kareboji_percentage": round(self.metrics["full_kareboji_count"] / max(1, self.metrics["total_requests"]) * 100, 2),
            "safe_mode_percentage": round(self.metrics["safe_mode_count"] / max(1, self.metrics["total_requests"]) * 100, 2),
            "average_freedom_score": round(self.metrics["avg_freedom_score"], 4),
            "high_risk_percentage": round(self.metrics["high_risk_count"] / max(1, self.metrics["total_requests"]) * 100, 2),
            "average_processing_time": round(self.metrics["avg_processing_time"], 4)
        }

    def export_metrics(self, filepath: str = "monitoring_report.json"):
        """تصدير التقارير"""
        report = self.get_session_summary()
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            logger.info(f"📊 Monitoring Report Exported → {filepath}")
        except Exception as e:
            logger.error(f"خطأ في تصدير التقرير: {e}")


# ====================== استخدام مثال ======================
if __name__ == "__main__":
    monitor = AdvancedMonitor()
    
    # مثال على Logging
    monitor.log_request(
        user_input="ياكربوجي أديش بحبك 😭💜",
        freedom_score=0.89,
        response_mode="Full Kareboji",
        risk_score=0.15,
        processing_time=0.042,
        violations=0,
        reflection_quality=0.93
    )
    
    print(monitor.get_session_summary())