from typing import Dict

SCENE_LIBRARY = {
    "define_concept": {
        "scene_id": "S1",
        "scene_type": "define_concept",
        "purpose": "What is the idea",
        "description": "Introduce the concept with clear definition"
    },
    "visualize_core": {
        "scene_id": "S2",
        "scene_type": "visualize_core",
        "purpose": "Main diagram / visual",
        "description": "Show the concept through visual representation"
    },
    "worked_example": {
        "scene_id": "S3",
        "scene_type": "worked_example",
        "purpose": "Step-by-step example",
        "description": "Demonstrate concept application with detailed example"
    },
    "common_mistake": {
        "scene_id": "S4",
        "scene_type": "common_mistake",
        "purpose": "Show & correct misconception",
        "description": "Address and correct common misunderstandings"
    },
    "mini_quiz": {
        "scene_id": "S5",
        "scene_type": "mini_quiz",
        "purpose": "Quick check",
        "description": "Assess understanding with targeted question"
    }
}


def get_scene_info(scene_type: str) -> Dict:
    return SCENE_LIBRARY.get(scene_type, {})


def get_all_scene_types():
    return list(SCENE_LIBRARY.keys())
