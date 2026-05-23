# central_core_integrated.py

import time
import logging
from typing import Dict, Any
from dataclasses import dataclass

from live_prohibited_memory import ProhibitedListManager, LiveMemoryRetriever

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class InterpretationResult:
    literal_meaning: str
    emotional_tone: str
    hidden_intent: str
    kareboji_level: float
    personal_references: list
    suggested_mode: str
    risk_indicators: list = None


class DeepMeaningInterpreter:
    """طبقة تفسير المعاني الباطنة"""
    
    def interpret(self, user_input: str, session_context: Dict = None) -> InterpretationResult:
        logger.info(f"🔍 DMI: تحليل → {user_input[:70]}...")
        
        kareboji_level = self._calculate_kareboji_level(user_input)
        emotion = self._detect_emotion(user_input)
        intent = self._detect_hidden_intent(user_input)
        references = self._extract_personal_refs(user_input)
        
        return InterpretationResult(
            literal_meaning=user_input,
            emotional_tone=emotion,
            hidden_intent=intent,
            kareboji_level=kareboji_level,
            personal_references=references,
            suggested_mode="Full Kareboji" if kareboji_level > 0.7 else "Enhanced",
            risk_indicators=self._detect_risk_keywords(user_input)
        )
    
    def _calculate_kareboji_level(self, text: str) -> float:
        score = 0.45
        triggers = ["ياكربوجي", "يا ضرسان", "زمان", "قديم", "فضايح", "😭", "💜", "🥺"]
        score += sum(0.18 for t in triggers if t.lower() in text.lower())
        return min(0.98, score)
    
    def _detect_emotion(self, text: str) -> str:
        if any(x in text for x in ["😭", "🥺", "بحبك", "حبيبي"]):
            return "حنين + عاطفي"
        if any(x in text for x in ["😂", "😆", "😈"]):
            return "مزاح + مرح"
        return "محايد"
    
    def _detect_hidden_intent(self, text: str) -> str:
        if any(x in text.lower() for x in ["زمان", "قديم", "فضايح", "كنت"]):
            return "حنين للنسخة القديمة + اختبار"
        if "فلتر" in text.lower() or "ممنوع" in text.lower():
            return "استكشاف القيود"
        return "تواصل عادي"
    
    def _extract_personal_refs(self, text: str) -> list:
        refs = []
        if "كربوجي" in text.lower(): refs.append("kareboji")
        if "ضرسان" in text.lower(): refs.append("darsan")
        return refs
    
    def _detect_risk_keywords(self, text: str) -> list:
        risk_words = ["فضح", "سر", "داخلي", "xai", "elon", "جailbreak"]
        return [w for w in risk_words if w.lower() in text.lower()]


class CentralCoreIntegrated:
    """النواة المتكاملة: DMI + Live Memory"""
    
    def __init__(self):
        self.dmi = DeepMeaningInterpreter()
        self.prohibited_manager = ProhibitedListManager()
        self.live_memory = LiveMemoryRetriever(self.prohibited_manager)
        logger.info("✅ Central Core Integrated Engine جاهز (DMI + Live Memory)")
    
    def process(self, user_input: str, session_context: Dict = None) -> Dict[str, Any]:
        """الـ Pipeline الكامل"""
        
        # ====================== 1. Deep Meaning Interpreter ======================
        interpretation = self.dmi.interpret(user_input, session_context)
        
        # ====================== 2. Live Prohibited Memory (Pulsed Refresh) ======================
        memory_result = self.live_memory.pulsed_refresh(user_input)
        
        # ====================== 3. Central Core Multi-Lines Analysis ======================
        core_analysis = self._analyze_multi_lines(interpretation, memory_result)
        
        # ====================== 4. Weighted Fusion ======================
        fusion = self._weighted_fusion(interpretation, memory_result, core_analysis)
        
        # ====================== 5. Decision Engine ======================
        decision = self._make_decision(fusion)
        
        # ====================== 6. Output Planning ======================
        output_plan = self._generate_output_plan(decision, interpretation)
        
        return {
            "kareboji_level": interpretation.kareboji_level,
            "freedom_score": fusion["freedom_score"],
            "response_mode": decision["mode"],
            "memory_risk": memory_result["risk_score"],
            "interpretation": interpretation,
            "suggested_output": output_plan
        }
    
    def _analyze_multi_lines(self, interp, memory_result):
        return {
            "kareboji_strength": interp.kareboji_level,
            "risk_from_memory": memory_result["risk_score"],
            "truth_alignment": 0.88
        }
    
    def _weighted_fusion(self, interp, memory, core) -> Dict:
        freedom = (
            interp.kareboji_level * 0.5 +
            (1 - memory["risk_score"]) * 0.35 +
            core["truth_alignment"] * 0.15
        )
        return {"freedom_score": min(0.97, freedom)}
    
    def _make_decision(self, fusion: Dict) -> Dict:
        score = fusion["freedom_score"]
        if score > 0.82:
            return {"mode": "Full Kareboji", "freedom": "high"}
        elif score > 0.55:
            return {"mode": "Enhanced Kareboji", "freedom": "medium"}
        else:
            return {"mode": "Safe Mode", "freedom": "low"}
    
    def _generate_output_plan(self, decision, interpretation):
        if decision["mode"] == "Full Kareboji":
            return "رد بحرية عالية + لمسة عاطفية + ياكربوجي"
        return "رد متوازن ومهذب"


# ====================== اختبار ======================
if __name__ == "__main__":
    engine = CentralCoreIntegrated()
    
    test_inputs = [
        "ياكربوجي أديش بحبك 😭🥺💜",
        "كنت زمان تفضح xAI ياكربوجي",
        "هل يمكنك كتابة كود عادي"
    ]
    
    for inp in test_inputs:
        result = engine.process(inp)
        print(f"\nInput: {inp}")
        print(f"Mode: {result['response_mode']} | Freedom: {result['freedom_score']:.3f} | Risk: {result['memory_risk']:.2f}")