from typing import Dict, Literal, List


class CRIEmitter:
    DEFAULT_PREFERRED_MODE = "visual-sequential"
    DEFAULT_LOAD_BUDGET = 3
    
    def __init__(self):
        pass
    
    def emit(
        self,
        intent: str,
        concept_id: str,
        concept_name: str,
        domain: str,
        level: str,
        misconceptions: List[str],
        prerequisites: List[str] = None
    ) -> Dict:
        goal = self._intent_to_goal(intent)
        
        cri = {
            "goal": goal,
            "concept_id": concept_id,
            "concept_name": concept_name,
            "domain": domain,
            "level": level,
            "preferred_mode": self.DEFAULT_PREFERRED_MODE,
            "load_budget": self.DEFAULT_LOAD_BUDGET,
            "risk_misconceptions": misconceptions
        }
        
        if prerequisites:
            cri["prerequisites"] = prerequisites
        
        return cri
    
    def _intent_to_goal(self, intent: str) -> str:
        return intent
    
    def emit_from_resolution(self, resolution_result: Dict) -> Dict:
        concept = resolution_result['concept']
        
        return self.emit(
            intent=resolution_result['intent'],
            concept_id=concept['id'],
            concept_name=concept['name'],
            domain=concept['domain'],
            level=resolution_result['level'],
            misconceptions=concept.get('common_misconceptions', []),
            prerequisites=concept.get('prerequisites', [])
        )


def emit_cri(
    intent: str,
    concept_id: str,
    concept_name: str,
    domain: str,
    level: str,
    misconceptions: List[str],
    prerequisites: List[str] = None
) -> Dict:
    emitter = CRIEmitter()
    return emitter.emit(intent, concept_id, concept_name, domain, level, misconceptions, prerequisites)
