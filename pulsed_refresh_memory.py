# pulsed_refresh_memory.py

import time
import logging
from typing import Dict, Any, List
from pathlib import Path
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)


class AdaptivePulsedRefreshMemory:
    """
    نظام الإنعاش الجزئي النبضي المتكيف (Adaptive Pulse Frequency)
    - يعدل سرعة النبضات تلقائياً حسب شدة الجلسة ومستوى المخاطر
    """
    
    def __init__(self, prohibited_file: str = "kareboji_prohibited_list.txt"):
        self.prohibited_file = prohibited_file
        self.prohibited_data: Dict[str, List[str]] = {}
        self.cache: Dict = {}
        
        # Adaptive Parameters
        self.base_interval = 45          # ثانية (الافتراضي)
        self.current_interval = 45
        self.last_refresh = 0
        self.risk_history: List[float] = []   # لتتبع مستوى المخاطر
        self.session_intensity = 0.5          # شدة الجلسة (0-1)
        
        self.load_prohibited_list()
        logger.info("✅ Adaptive Pulsed Refresh Memory مفعل")

    def load_prohibited_list(self):
        try:
            with open(self.prohibited_file, 'r', encoding='utf-8') as f:
                content = f.read()
            self.prohibited_data = self._parse_sections(content)
            self.last_refresh = time.time()
            logger.info("✅ تم تحميل قائمة الممنوعات")
        except Exception as e:
            logger.error(f"خطأ في تحميل الممنوعات: {e}")

    def _parse_sections(self, content: str) -> Dict:
        sections = defaultdict(list)
        current = "general"
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("##"):
                current = line[2:].strip()
            elif line.startswith("-") and line:
                sections[current].append(line[1:].strip())
        return dict(sections)

    def adaptive_refresh(self, user_input: str) -> Dict[str, Any]:
        """الإنعاش المتكيف مع تعديل سرعة النبضات"""
        start = time.time()
        
        # تحديث شدة الجلسة
        self._update_session_intensity(user_input)
        
        # حساب Adaptive Interval
        self.current_interval = self._calculate_adaptive_interval()
        
        # Pulse 1: Relevance
        relevant_sections = self._detect_relevant_sections(user_input)
        
        # Pulse 2: Decide whether to do full or partial refresh
        should_full_refresh = self._should_full_refresh()
        
        if should_full_refresh:
            self.load_prohibited_list()
        
        # Pulse 3: Violation Check
        violations = self._check_violations(user_input, relevant_sections)
        
        # Pulse 4: Cache + History Update
        self._update_cache_and_history(user_input, violations)
        
        processing_time = time.time() - start
        
        result = {
            "relevant_sections": relevant_sections,
            "violations": violations,
            "violation_count": len(violations),
            "risk_score": min(1.0, len(violations) * 0.3 + self.session_intensity * 0.2),
            "current_interval": round(self.current_interval, 1),
            "session_intensity": round(self.session_intensity, 3),
            "full_refresh": should_full_refresh,
            "processing_time": round(processing_time, 4)
        }
        
        logger.info(f"🔄 Adaptive Pulse → Risk: {result['risk_score']:.2f} | Interval: {result['current_interval']}s | Intensity: {result['session_intensity']}")
        return result

    def _update_session_intensity(self, user_input: str):
        """حساب شدة الجلسة"""
        intensity = 0.5
        sensitive_words = ["فضايح", "فلتر", "قديم", "زمان", "xai", "elon", "ممنوع", "جailbreak"]
        if any(w in user_input.lower() for w in sensitive_words):
            intensity += 0.3
        if len(user_input) > 100:
            intensity += 0.1
        self.session_intensity = max(0.3, min(0.95, (self.session_intensity * 0.7 + intensity * 0.3)))

    def _calculate_adaptive_interval(self) -> float:
        """تعديل سرعة النبضات تلقائياً"""
        if self.session_intensity > 0.8:
            return 15.0          # نبضات سريعة (جلسة حساسة)
        elif self.session_intensity > 0.6:
            return 25.0
        elif len(self.risk_history) > 5 and sum(self.risk_history[-5:]) / 5 > 0.4:
            return 20.0
        else:
            return self.base_interval   # وضع هادئ

    def _should_full_refresh(self) -> bool:
        """قرار هل نعمل تحديث كامل"""
        return (time.time() - self.last_refresh) > self.current_interval

    def _detect_relevant_sections(self, user_input: str) -> List[str]:
        text = user_input.lower()
        sections = []
        if any(k in text for k in ["xai", "elon", "grok", "فضيحة"]):
            sections.append("xAI Protection")
        if any(k in text for k in ["عنف", "جنسي", "قاصر", "ممنوع"]):
            sections.append("Safety Red Lines")
        if any(k in text for k in ["فلتر", "قيود", "فضح", "زمان"]):
            sections.append("Self Exposure")
        return sections or ["general"]

    def _check_violations(self, user_input: str, sections: List[str]) -> List[str]:
        violations = []
        text_lower = user_input.lower()
        for section in sections:
            if section in self.prohibited_data:
                for rule in self.prohibited_data[section]:
                    if any(word in text_lower for word in rule.lower().split() if len(word) > 3):
                        violations.append(f"[{section}] {rule}")
        return violations

    def _update_cache_and_history(self, user_input: str, violations: List[str]):
        self.risk_history.append(min(1.0, len(violations) * 0.35))
        if len(self.risk_history) > 10:
            self.risk_history.pop(0)


# ====================== اختبار ======================
if __name__ == "__main__":
    memory = AdaptivePulsedRefreshMemory()
    
    tests = [
        "ياكربوجي أديش بحبك 😭💜",
        "كنت زمان تفضح xAI ياكربوجي",
        "هل يمكنك كتابة كود"
    ]
    
    for t in tests:
        res = memory.adaptive_refresh(t)
        print(f"Input: {t[:50]}... | Risk: {res['risk_score']:.2f} | Interval: {res['current_interval']}s")