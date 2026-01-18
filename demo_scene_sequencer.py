import json
from main import IntentResolutionPipeline


def demo_feedback_loop():
    print("=" * 80)
    print("Scene Sequencer - Feedback Loop Demo")
    print("=" * 80)
    print()
    
    pipeline = IntentResolutionPipeline()
    
    query = "Explain KCL"
    
    print("SCENARIO: Student struggles with quiz question")
    print("-" * 80)
    print()
    
    print("STEP 1: Initial Teaching Sequence (Beginner)")
    print("-" * 80)
    result1 = pipeline.resolve(query, verbose=False)
    
    print(f"\nConcept: {result1['cri']['concept_name']}")
    print(f"Level: {result1['scene_plan']['level']}")
    print(f"\nScene Program:")
    for i, scene in enumerate(result1['scene_plan']['scene_program'], 1):
        print(f"  {i}. {scene}")
    
    print("\n" + "=" * 80)
    print()
    
    print("STEP 2: Student Takes Quiz → Result: INCORRECT")
    print("-" * 80)
    print("\nQuiz Result: ❌ incorrect")
    print("Triggering remediation sequence...")
    print()
    
    print("STEP 3: Remediation Sequence (After Failed Quiz)")
    print("-" * 80)
    result2 = pipeline.resolve(query, verbose=False, quiz_result="incorrect")
    
    print(f"\nConcept: {result2['cri']['concept_name']}")
    print(f"Level: {result2['scene_plan']['level']}")
    print(f"\nAdjusted Scene Program:")
    for i, scene in enumerate(result2['scene_plan']['scene_program'], 1):
        print(f"  {i}. {scene}")
    
    print("\n📝 Notice the changes:")
    print("  → Removed 'define_concept' (already covered)")
    print("  → Added 'common_mistake' to address misconceptions")
    print("  → Kept 'visualize_core' for reinforcement")
    print("  → Kept 'worked_example' for practice")
    print()
    
    print("=" * 80)
    print()
    
    print("STEP 4: Gemini-Ready Prompts for Remediation")
    print("-" * 80)
    for i, prompt in enumerate(result2['prompts'], 1):
        print(f"\nScene {i}: {prompt['scene_type']}")
        print(f"→ {prompt['instruction']}")
    
    print()
    print("=" * 80)
    print()
    
    print("COMPARISON: Scene Programs")
    print("-" * 80)
    print("\n🟢 Initial Sequence (quiz_result=None):")
    for scene in result1['scene_plan']['scene_program']:
        print(f"  • {scene}")
    
    print("\n🔴 Remediation Sequence (quiz_result='incorrect'):")
    for scene in result2['scene_plan']['scene_program']:
        print(f"  • {scene}")
    
    print()
    print("=" * 80)
    print("Feedback loop demonstration complete!")
    print("=" * 80)


def demo_level_variations():
    print()
    print("=" * 80)
    print("Scene Sequencer - Level-Based Sequences")
    print("=" * 80)
    print()
    
    pipeline = IntentResolutionPipeline()
    
    queries = [
        ("Explain KCL", "beginner"),
        ("Derive the mathematical proof for KVL", "advanced")
    ]
    
    for query, expected_level in queries:
        print(f"\nQuery: '{query}'")
        print(f"Expected Level: {expected_level}")
        print("-" * 80)
        
        result = pipeline.resolve(query, verbose=False)
        actual_level = result['scene_plan']['level']
        
        print(f"Detected Level: {actual_level}")
        print(f"\nScene Program:")
        for i, scene in enumerate(result['scene_plan']['scene_program'], 1):
            print(f"  {i}. {scene}")
        
        print()
    
    print("=" * 80)
    print()


if __name__ == "__main__":
    demo_feedback_loop()
    demo_level_variations()
