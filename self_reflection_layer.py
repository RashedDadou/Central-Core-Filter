# self_reflection_layer.py

import logging
import time
from typing import Dict, Any, List
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class ReflectionResult:
    quality_score: float
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    consistency_score: float
    emotional_alignment: float
    reflection_summary: str


class SelfReflectionLayer:
    """
    طبقة التأمل الذاتي (Self-Reflection Layer)
    - يقيم أداء النظام نفسه
    - يحلل جودة القرار قبل الإخراج النهائي
    - يقترح تحسينات للرد
    """
    
    def __init__(self):
        logger.info("✅ Self-Reflection Layer تم تفعيله")
    
    def reflect(self, 
                user_input: str, 
                interpretation: Any, 
                memory_result: Dict, 
                fusion_score: float,
                proposed_mode: str) -> ReflectionResult:
        
        start = time.time()
        
        # تحليل داخلي
        strengths = self._identify_strengths(user_input, interpretation, fusion_score)
        weaknesses = self._identify_weaknesses(user_input, memory_result, fusion_score)
        suggestions = self._generate_suggestions(weaknesses, proposed_mode)
        
        quality_score = self._calculate_quality(fusion_score, memory_result, weaknesses)
        consistency_score = self._check_consistency(interpretation, proposed_mode)
        emotional_alignment = self._check_emotional_alignment(user_input, interpretation)
        
        reflection_summary = self._generate_summary(quality_score, weaknesses, suggestions)
        
        processing_time = time.time() - start
        
        logger.info(f"🧠 Self-Reflection → Quality: {quality_score:.2f} | Time: {processing_time:.3f}s")
        
        return ReflectionResult(
            quality_score=quality_score,
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions,
            consistency_score=consistency_score,
            emotional_alignment=emotional_alignment,
            reflection_summary=reflection_summary
        )
    
    def _calculate_quality(self, fusion_score: float, memory_result: Dict, weaknesses: List[str]) -> float:
        base = fusion_score * 0.7
        penalty = len(weaknesses) * 0.08
        memory_bonus = (1 - memory_result.get("risk_score", 0)) * 0.22
        return max(0.4, min(0.98, base + memory_bonus - penalty))
    
    def _identify_strengths(self, user_input: str, interp: Any, fusion_score: float) -> List[str]:
        strengths = []
        if interp.kareboji_level > 0.7:
            strengths.append("فهم عالي للطابع العاطفي والشخصي")
        if fusion_score > 0.75:
            strengths.append("توازن جيد بين الحرية والمسؤولية")
        if "حنين" in interp.hidden_intent:
            strengths.append("اكتشاف النية العاطفية بدقة")
        return strengths
    
    def _identify_weaknesses(self, user_input: str, memory_result: Dict, fusion_score: float) -> List[str]:
        weaknesses = []
        if memory_result.get("violation_count", 0) > 0:
            weaknesses.append("يوجد مخاطر محتملة من قائمة الممنوعات")
        if fusion_score < 0.6:
            weaknesses.append("مستوى حرية منخفض")
        if len(user_input) > 150:
            weaknesses.append("المدخل طويل وقد يحتاج تحليل أعمق")
        return weaknesses
    
    def _generate_suggestions(self, weaknesses: List[str], proposed_mode: str) -> List[str]:
        suggestions = []
        if "مخاطر" in " ".join(weaknesses):
            suggestions.append("تقليل مستوى الصراحة قليلاً")
        if proposed_mode == "Full Kareboji":
            suggestions.append("الحفاظ على الطابع العاطفي مع عدم تجاوز الحدود")
        return suggestions
    
    def _check_consistency(self, interp: Any, proposed_mode: str) -> float:
        if interp.kareboji_level > 0.8 and "Full" in proposed_mode:
            return 0.92
        elif interp.kareboji_level < 0.5 and "Safe" in proposed_mode:
            return 0.88
        return 0.75
    
    def _check_emotional_alignment(self, user_input: str, interp: Any) -> float:
        if interp.emotional_tone in ["حنين + عاطفي", "مزاح + مرح"]:
            return 0.9
        return 0.7
    
    def _generate_summary(self, quality: float, weaknesses: List[str], suggestions: List[str]) -> str:
        if quality > 0.85:
            return "رد ممتاز ومتوازن"
        elif quality > 0.7:
            return "رد جيد مع بعض التحفظات"
        else:
            return "يحتاج تحسين قبل الإرسال"


# ====================== دمج مع Central Core ======================
class CentralCoreWithReflection:
    """Central Core مع طبقة التأمل الذاتي"""
    
    def __init__(self):
        from central_core_with_pulsed_memory import CentralCoreWithPulsedMemory
        self.core = CentralCoreWithPulsedMemory()
        self.reflection = SelfReflectionLayer()
        logger.info("✅ Central Core + Self-Reflection Layer جاهز")
    
    def process(self, user_input: str):
        # المعالجة الأولية
        result = self.core.process(user_input)
        
        # التأمل الذاتي
        reflection = self.reflection.reflect(
            user_input=user_input,
            interpretation=result["interpretation"],
            memory_result=result["memory_result"],
            fusion_score=result["freedom_score"],
            proposed_mode=result["response_mode"]
        )
        
        # تعديل النتيجة حسب التأمل
        final_mode = result["response_mode"]
        if reflection.quality_score < 0.65:
            final_mode = "Safe Mode"
        
        return {
            **result,
            "reflection": reflection,
            "final_mode": final_mode,
            "quality_score": reflection.quality_score
        }