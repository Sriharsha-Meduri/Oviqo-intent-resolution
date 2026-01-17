import re
from typing import Dict, Literal

IntentType = Literal["teach_concept", "revise_concept", "test_understanding"]


class IntentDetector:
    def __init__(self):
        self.teach_keywords = [
            "explain", "what is", "how does", "tell me about", 
            "teach me", "learn", "understand", "show me", "describe"
        ]
        
        self.revise_keywords = [
            "revise", "review", "refresh", "recap", "summarize",
            "remind me", "go over", "revisit"
        ]
        
        self.test_keywords = [
            "test", "quiz", "assess", "evaluate", "check my",
            "how well do i", "practice", "exercise", "problem"
        ]
    
    def detect(self, query: str) -> Dict[str, any]:
        query_lower = query.lower().strip()
        
        teach_score = self._count_matches(query_lower, self.teach_keywords)
        revise_score = self._count_matches(query_lower, self.revise_keywords)
        test_score = self._count_matches(query_lower, self.test_keywords)
        
        max_score = max(teach_score, revise_score, test_score)
        
        if max_score == 0:
            if "?" in query:
                return {"intent": "teach_concept", "confidence": 0.7}
            return {"intent": "teach_concept", "confidence": 0.6}
        
        total_score = teach_score + revise_score + test_score
        confidence = min(0.95, 0.7 + (max_score / (total_score + 1)) * 0.25)
        
        if teach_score == max_score:
            intent = "teach_concept"
        elif revise_score == max_score:
            intent = "revise_concept"
        else:
            intent = "test_understanding"
        
        return {"intent": intent, "confidence": round(confidence, 2)}
    
    def _count_matches(self, query: str, keywords: list) -> int:
        count = 0
        for keyword in keywords:
            if keyword in query:
                count += 1
        return count


def detect_intent(query: str) -> Dict[str, any]:
    detector = IntentDetector()
    return detector.detect(query)
