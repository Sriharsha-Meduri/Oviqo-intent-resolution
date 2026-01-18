import json
from main import resolve_query


def demo_personalization():
    print("=" * 80)
    print("Scene Sequencer - Personalization Demo")
    print("=" * 80)
    print()
    
    test_query = "Explain Kirchhoff's Current Law"
    
    print("Scenario 1: Standard beginner sequence (no user_state)")
    print("-" * 80)
    result1 = resolve_query(test_query, verbose=False)
    print(f"Scene Program: {result1['scene_plan']['scene_program']}")
    print(f"Reason: {result1['scene_plan'].get('personalization_reason', 'N/A')}")
    print()
    
    print("Scenario 2: Student with recent quiz failure")
    print("-" * 80)
    user_state_failed = {
        "recent_quiz_result": "incorrect"
    }
    result2 = resolve_query(test_query, verbose=False, user_state=user_state_failed)
    print(f"Scene Program: {result2['scene_plan']['scene_program']}")
    print(f"Reason: {result2['scene_plan'].get('personalization_reason', 'N/A')}")
    print()
    
    print("Scenario 3: Student with weak mastery of KCL")
    print("-" * 80)
    user_state_weak = {
        "concept_mastery": {
            "KCL-001": "weak"
        }
    }
    result3 = resolve_query(test_query, verbose=False, user_state=user_state_weak)
    print(f"Scene Program: {result3['scene_plan']['scene_program']}")
    print(f"Reason: {result3['scene_plan'].get('personalization_reason', 'N/A')}")
    print()
    
    print("Scenario 4: Both recent failure AND weak mastery")
    print("-" * 80)
    user_state_both = {
        "recent_quiz_result": "incorrect",
        "concept_mastery": {
            "KCL-001": "weak"
        }
    }
    result4 = resolve_query(test_query, verbose=False, user_state=user_state_both)
    print(f"Scene Program: {result4['scene_plan']['scene_program']}")
    print(f"Reason: {result4['scene_plan'].get('personalization_reason', 'N/A')}")
    print()
    
    print("Scenario 5: Strong mastery (no personalization needed)")
    print("-" * 80)
    user_state_strong = {
        "recent_quiz_result": "correct",
        "concept_mastery": {
            "KCL-001": "strong"
        }
    }
    result5 = resolve_query(test_query, verbose=False, user_state=user_state_strong)
    print(f"Scene Program: {result5['scene_plan']['scene_program']}")
    print(f"Reason: {result5['scene_plan'].get('personalization_reason', 'N/A')}")
    print()
    
    print("=" * 80)
    print("Key Observations:")
    print("  • Without user_state: standard level-based sequence")
    print("  • With recent failure or weak mastery:")
    print("    - Skips 'define_concept' (already covered)")
    print("    - Inserts 'common_mistake' (addresses misconceptions)")
    print("  • With strong mastery: falls back to standard sequence")
    print("  • Backward compatible: existing code without user_state still works")
    print("=" * 80)


if __name__ == "__main__":
    demo_personalization()
