from typing import Dict, List, Optional
from scene_library import get_scene_info


class SceneSequencer:
    def __init__(self):
        self.session_state = {}
    
    def plan_sequence(self, cri: Dict, quiz_result: str = None, user_state: Optional[Dict] = None) -> Dict:
        concept_id = cri.get("concept_id", "unknown")
        level = cri.get("level", "beginner")
        load_budget = cri.get("load_budget", 3)
        
        personalization_reason = None
        
        if user_state:
            scene_program, personalization_reason = self._get_personalized_sequence(
                cri, user_state, level
            )
        elif quiz_result == "incorrect" and concept_id in self.session_state:
            scene_program = self._get_remediation_sequence()
            personalization_reason = "Remediation sequence triggered by incorrect quiz result"
        else:
            scene_program = self._get_sequence_by_level(level)
            personalization_reason = f"Standard {level}-level sequence"
        
        self.session_state[concept_id] = {
            "last_sequence": scene_program,
            "quiz_result": quiz_result
        }
        
        result = {
            "concept_id": cri.get("concept_id"),
            "concept_name": cri.get("concept_name"),
            "level": level,
            "scene_program": scene_program,
            "load_budget": load_budget
        }
        
        if personalization_reason:
            result["personalization_reason"] = personalization_reason
        
        return result
    
    def _get_sequence_by_level(self, level: str) -> List[str]:
        if level == "beginner":
            return [
                "define_concept",
                "visualize_core",
                "worked_example",
                "mini_quiz"
            ]
        elif level == "intermediate":
            return [
                "define_concept",
                "worked_example",
                "common_mistake",
                "mini_quiz"
            ]
        elif level == "advanced":
            return [
                "worked_example",
                "common_mistake",
                "mini_quiz"
            ]
        else:
            return [
                "define_concept",
                "visualize_core",
                "worked_example",
                "mini_quiz"
            ]
    
    def _get_remediation_sequence(self) -> List[str]:
        return [
            "visualize_core",
            "worked_example",
            "common_mistake",
            "mini_quiz"
        ]
    
    def _get_personalized_sequence(self, cri: Dict, user_state: Dict, level: str) -> tuple:
        concept_id = cri.get("concept_id", "unknown")
        recent_quiz_result = user_state.get("recent_quiz_result")
        concept_mastery = user_state.get("concept_mastery", {})
        
        mastery_level = concept_mastery.get(concept_id, "unknown")
        
        needs_remediation = (
            recent_quiz_result == "incorrect" or 
            mastery_level == "weak"
        )
        
        if needs_remediation:
            base_sequence = self._get_sequence_by_level(level)
            
            if "define_concept" in base_sequence:
                base_sequence.remove("define_concept")
            
            if "common_mistake" not in base_sequence:
                quiz_index = base_sequence.index("mini_quiz") if "mini_quiz" in base_sequence else len(base_sequence)
                base_sequence.insert(quiz_index, "common_mistake")
            
            reason_parts = []
            if recent_quiz_result == "incorrect":
                reason_parts.append("recent quiz failure")
            if mastery_level == "weak":
                reason_parts.append(f"weak mastery of {concept_id}")
            
            reason = f"Personalized sequence: skipped definition, added misconception handling due to {' and '.join(reason_parts)}"
            
            return base_sequence, reason
        else:
            reason = f"Standard {level}-level sequence (user_state provided but no personalization needed)"
            return self._get_sequence_by_level(level), reason
    
    def update_feedback(self, concept_id: str, quiz_result: str):
        if concept_id in self.session_state:
            self.session_state[concept_id]["quiz_result"] = quiz_result
            if quiz_result == "correct":
                self.session_state[concept_id]["status"] = "improving"
            else:
                self.session_state[concept_id]["status"] = "needs_remediation"


def plan_scenes(cri: Dict, quiz_result: str = None, user_state: Optional[Dict] = None) -> Dict:
    sequencer = SceneSequencer()
    return sequencer.plan_sequence(cri, quiz_result, user_state)
