from typing import Dict, List


class GeminiPromptBuilder:
    def __init__(self):
        self.prompt_templates = {
            "define_concept": self._build_define_prompt,
            "visualize_core": self._build_visualize_prompt,
            "worked_example": self._build_example_prompt,
            "common_mistake": self._build_mistake_prompt,
            "mini_quiz": self._build_quiz_prompt
        }
    
    def build_prompts(self, concept_name: str, scene_program: List[str], 
                     misconceptions: List[str] = None) -> List[Dict]:
        prompts = []
        
        for scene_type in scene_program:
            builder_func = self.prompt_templates.get(scene_type)
            if builder_func:
                prompt = builder_func(concept_name, misconceptions)
                prompts.append({
                    "scene_type": scene_type,
                    "instruction": prompt
                })
        
        return prompts
    
    def _build_define_prompt(self, concept: str, misconceptions: List[str] = None) -> str:
        return f"Explain what {concept} is. Provide a clear, concise definition that a student can understand."
    
    def _build_visualize_prompt(self, concept: str, misconceptions: List[str] = None) -> str:
        return f"Create a visual representation of {concept}. Show the main components and how they interact."
    
    def _build_example_prompt(self, concept: str, misconceptions: List[str] = None) -> str:
        return f"Solve a step-by-step example problem involving {concept}. Show all work clearly."
    
    def _build_mistake_prompt(self, concept: str, misconceptions: List[str] = None) -> str:
        if misconceptions and len(misconceptions) > 0:
            mistake = misconceptions[0]
            return f"Address this common misconception about {concept}: '{mistake}'. Explain why it's incorrect and show the right way to think about it."
        return f"Show a common mistake students make with {concept} and explain the correct approach."
    
    def _build_quiz_prompt(self, concept: str, misconceptions: List[str] = None) -> str:
        return f"Create a quick quiz question to check understanding of {concept}. Make it practical and relevant."


def generate_prompts(concept_name: str, scene_program: List[str], 
                    misconceptions: List[str] = None) -> List[Dict]:
    builder = GeminiPromptBuilder()
    return builder.build_prompts(concept_name, scene_program, misconceptions)
