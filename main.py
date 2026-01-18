import json
from typing import Dict

from intent_detector import IntentDetector
from concept_resolver import ConceptResolver, ConceptNotFoundError
from level_estimator import LevelEstimator
from cri_emitter import CRIEmitter
from scene_sequencer import SceneSequencer
from gemini_prompt_builder import GeminiPromptBuilder


class IntentResolutionPipeline:
    def __init__(self):
        self.intent_detector = IntentDetector()
        self.concept_resolver = ConceptResolver()
        self.level_estimator = LevelEstimator()
        self.cri_emitter = CRIEmitter()
        self.scene_sequencer = SceneSequencer()
        self.prompt_builder = GeminiPromptBuilder()
    
    def resolve(self, query: str, verbose: bool = False, quiz_result: str = None, user_state: Dict = None) -> Dict:
        intent_result = self.intent_detector.detect(query)
        intent = intent_result['intent']
        
        concept_result = self.concept_resolver.resolve(query)
        concept = concept_result['concept']
        concept_id = concept_result['concept_id']
        
        level_result = self.level_estimator.estimate(query)
        level = level_result['level']
        
        cri = self.cri_emitter.emit(
            intent=intent,
            concept_id=concept_id,
            concept_name=concept['name'],
            domain=concept['domain'],
            level=level,
            misconceptions=concept.get('common_misconceptions', []),
            prerequisites=concept.get('prerequisites', [])
        )
        
        scene_plan = self.scene_sequencer.plan_sequence(cri, quiz_result, user_state)
        
        prompts = self.prompt_builder.build_prompts(
            concept_name=cri['concept_name'],
            scene_program=scene_plan['scene_program'],
            misconceptions=cri.get('risk_misconceptions', [])
        )
        
        result = {
            "cri": cri,
            "scene_plan": scene_plan,
            "prompts": prompts
        }
        
        if verbose:
            result["metadata"] = {
                "query": query,
                "intent_detection": intent_result,
                "concept_resolution": {
                    "concept_id": concept_id,
                    "matched_alias": concept_result['matched_alias']
                },
                "level_estimation": level_result
            }
        
        return result


def resolve_query(query: str, verbose: bool = False, quiz_result: str = None, user_state: Dict = None) -> Dict:
    pipeline = IntentResolutionPipeline()
    return pipeline.resolve(query, verbose, quiz_result, user_state)


def main():
    print("=" * 80)
    print("Intent & Concept Resolution System - Demo")
    print("Learning Operating System - v1.0")
    print("=" * 80)
    print()
    
    pipeline = IntentResolutionPipeline()
    
    test_queries = [
        "Explain KCL",
        "What is Ohm's law?",
        "Review Kirchhoff's voltage law",
        "Test my understanding of series circuits",
        "Teach me about capacitors"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"Query #{i}: \"{query}\"")
        print("-" * 80)
        
        try:
            result = pipeline.resolve(query, verbose=True)
            
            print("\n📋 COGNITIVE REMEDIATION INTENT (CRI):")
            print(json.dumps(result['cri'], indent=2))
            
            print("\n🎬 SCENE PLAN:")
            print(json.dumps(result['scene_plan'], indent=2))
            
            print("\n📝 GEMINI PROMPTS:")
            for i, prompt in enumerate(result['prompts'], 1):
                print(f"\n  Scene {i}: {prompt['scene_type']}")
                print(f"  → {prompt['instruction']}")
            
            if 'metadata' in result:
                print("\n🔍 Pipeline Metadata:")
                metadata = result['metadata']
                print(f"  Intent: {metadata['intent_detection']['intent']} "
                      f"(confidence: {metadata['intent_detection']['confidence']})")
                print(f"  Concept: {metadata['concept_resolution']['concept_id']} "
                      f"(matched: '{metadata['concept_resolution']['matched_alias']}')")
                print(f"  Level: {metadata['level_estimation']['level']} "
                      f"(confidence: {metadata['level_estimation']['confidence']})")
                print(f"  Reasoning: {metadata['level_estimation']['reasoning']}")
            
            print()
        
        except ConceptNotFoundError as e:
            print(f"\n❌ Error: {e}")
            print()
        
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print()
        
        if i < len(test_queries):
            print("=" * 80)
            print()
    
    print("=" * 80)
    print("Demo complete. The CRI objects above are ready for downstream systems.")
    print("=" * 80)


if __name__ == "__main__":
    main()
