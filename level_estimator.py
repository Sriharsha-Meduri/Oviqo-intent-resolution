from typing import Dict, Literal

LevelType = Literal["beginner", "intermediate", "advanced", "unknown"]


class LevelEstimator:
    def __init__(self):
        self.beginner_indicators = [
            "what is", "explain", "basics", "introduction", "simple",
            "eli5", "for dummies", "beginner", "start", "first"
        ]
        
        self.advanced_indicators = [
            "derive", "proof", "mathematical", "rigorous", "formal",
            "theoretical", "advanced", "complex", "in-depth", "detailed analysis"
        ]
        
        self.technical_terms = [
            "impedance", "phasor", "laplace", "fourier", "topology",
            "transient", "steady-state", "frequency response"
        ]
    
    def estimate(self, query: str, context: Dict = None) -> Dict[str, any]:
        query_lower = query.lower().strip()
        
        beginner_count = self._count_matches(query_lower, self.beginner_indicators)
        advanced_count = self._count_matches(query_lower, self.advanced_indicators)
        technical_count = self._count_matches(query_lower, self.technical_terms)
        
        if advanced_count > 0:
            return {
                "level": "advanced",
                "confidence": 0.8,
                "reasoning": "Query contains advanced terminology or requests rigorous treatment"
            }
        
        if technical_count > 0:
            return {
                "level": "intermediate",
                "confidence": 0.7,
                "reasoning": "Query uses technical terminology"
            }
        
        if beginner_count > 0:
            return {
                "level": "beginner",
                "confidence": 0.75,
                "reasoning": "Simple explanation request"
            }
        
        if len(query.split()) <= 4:
            return {
                "level": "beginner",
                "confidence": 0.65,
                "reasoning": "Short, direct query suggests introductory level"
            }
        
        return {
            "level": "beginner",
            "confidence": 0.5,
            "reasoning": "Default to beginner level (no clear indicators)"
        }
    
    def _count_matches(self, text: str, keywords: list) -> int:
        count = 0
        for keyword in keywords:
            if keyword in text:
                count += 1
        return count


def estimate_level(query: str, context: Dict = None) -> Dict[str, any]:
    estimator = LevelEstimator()
    return estimator.estimate(query, context)
