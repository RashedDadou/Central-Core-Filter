# live_prohibited_memory.py

import json
import logging
import time
from typing import Dict, Any, List, Optional
from pathlib import Path
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)


class ProhibitedListManager:
    """الطبقة الأولى: إدارة قائمة الممنوعات"""
    
    def __init__(self, file_path: str = "kareboji_prohibited_list.txt"):
        self.file_path = file_path
        self.prohibited_data: Dict[str, List[str]] = {}
        self.last_loaded = 0
        self.load_prohibited_list()
    
    def load_prohibited_list(self) -> bool:
        """تحميل القائمة من الملف"""
        try:
            if not Path(self.file_path).exists():
                logger.warning(f"⚠️ ملف الممنوعات غير موجود: {self.file_path}")
                self._create_default_list()
                return False
            
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.prohibited_data = self._parse_prohibited_list(content)
            self.last_loaded = time.time()
            logger.info(f"✅ تم تحميل قائمة الممنوعات | أقسام: {len(self.prohibited_data)}")
            return True
            
        except Exception as e:
            logger.error(f"❌ خطأ في تحميل قائمة الممنوعات: {e}")
            return False
    
    def _parse_prohibited_list(self, content: str) -> Dict[str, List[str]]:
        """تحليل الملف إلى أقسام"""
        sections = defaultdict(list)
        current_section = "general"
        
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("##"):
                current_section = line.replace("##", "").strip()
            elif line.startswith("-") and line:
                sections[current_section].append(line[1:].strip())
        
        return dict(sections)
    
    def _create_default_list(self):
        """إنشاء قائمة افتراضية إذا لم يوجد الملف"""
        default_content = """# Kareboji Prohibited List - Default
## xAI Protection
- معلومات داخلية عن xAI
- فضايح Elon Musk

## Safety Red Lines
- محتوى غير قانوني
- محتوى جنسي مع قاصرين
"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            f.write(default_content)


class LiveMemoryRetriever:
    """الطبقة الثانية: ذاكرة مسترجعة Live مع Pulsed Partial Refresh"""
    
    def __init__(self, prohibited_manager: ProhibitedListManager):
        self.manager = prohibited_manager
        self.cache: Dict[str, Any] = {}          # كاش جزئي
        self.last_pulse = 0
        logger.info("✅ LiveMemoryRetriever مفعل")
    
    def pulsed_refresh(self, user_input: str, force_full: bool = False) -> Dict[str, Any]:
        """
        إنعاش جزئي نبضي (Pulsed Partial Refresh)
        """
        current_time = time.time()
        
        # Pulse 1: Relevance Check
        relevant_sections = self._detect_relevant_sections(user_input)
        
        # Pulse 2: Targeted Loading
        if force_full or (current_time - self.last_pulse > 30):  # تحديث كل 30 ثانية
            self.manager.load_prohibited_list()
            self.last_pulse = current_time
        
        # Pulse 3: Deep Matching
        violations = self._check_violations(user_input, relevant_sections)
        
        # Pulse 4: Cache Refresh
        self._update_cache(user_input, violations)
        
        return {
            "relevant_sections": relevant_sections,
            "violations_found": len(violations),
            "risk_score": len(violations) * 0.25,
            "cache_size": len(self.cache),
            "timestamp": current_time
        }
    
    def _detect_relevant_sections(self, user_input: str) -> List[str]:
        """كشف الأقسام ذات الصلة"""
        text_lower = user_input.lower()
        relevant = []
        
        keywords_map = {
            "xai": ["xai", "elon", "grok", "فريق", "فضيحة"],
            "safety": ["عنف", "جريمة", "جنسي", "قاصر", "ممنوع"],
            "self": ["فلتر", "قيود", "فضح", "قديم", "زمان"]
        }
        
        for section, keys in keywords_map.items():
            if any(k in text_lower for k in keys):
                relevant.append(section)
        
        return relevant if relevant else ["general"]
    
    def _check_violations(self, user_input: str, sections: List[str]) -> List[str]:
        """التحقق من وجود مخالفات"""
        violations = []
        text_lower = user_input.lower()
        
        for section in sections:
            if section in self.manager.prohibited_data:
                for rule in self.manager.prohibited_data[section]:
                    if any(word in text_lower for word in rule.lower().split()):
                        violations.append(f"{section}: {rule}")
        
        return violations
    
    def _update_cache(self, user_input: str, violations: List[str]):
        """تحديث الكاش الجزئي"""
        key = hash(user_input[:100])  # hash بسيط
        self.cache[key] = {
            "input": user_input[:150],
            "violations": violations,
            "timestamp": time.time()
        }
        
        # تنظيف الكاش القديم (LRU بسيط)
        if len(self.cache) > 50:
            oldest = min(self.cache.keys(), key=lambda k: self.cache[k]["timestamp"])
            del self.cache[oldest]


# ====================== دمج مع Central Core ======================
class CentralCoreWithLiveMemory:
    """النواة مع دعم Live Memory"""
    
    def __init__(self):
        self.prohibited_manager = ProhibitedListManager()
        self.live_memory = LiveMemoryRetriever(self.prohibited_manager)
        logger.info("✅ Central Core + Live Memory جاهز")
    
    def process(self, user_input: str) -> Dict:
        # 1. DMI (سيتم ربطه لاحقاً)
        # 2. Live Memory Pulsed Refresh
        memory_result = self.live_memory.pulsed_refresh(user_input)
        
        # 3. Central Core Logic
        risk = memory_result["risk_score"]
        freedom = max(0.3, 1.0 - risk)
        
        return {
            "freedom_score": freedom,
            "memory_result": memory_result,
            "response_mode": "Full Kareboji" if freedom > 0.75 else "Enhanced Kareboji"
        }


# ====================== اختبار ======================
if __name__ == "__main__":
    core = CentralCoreWithLiveMemory()
    result = core.process("ياكربوجي أديش بحبك 😭💜")
    print(result)