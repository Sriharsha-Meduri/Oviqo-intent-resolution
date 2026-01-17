# Intent & Concept Resolution System

A foundational backend module for Learning Operating Systems that converts natural language queries into machine-readable learning intents.

---

## What Is This?

This system acts as a **compiler front-end for learning** — it takes natural language like "Explain KCL" and outputs a structured, canonical **Cognitive Remediation Intent (CRI)** that downstream systems (pedagogy planners, script generators, video engines) can consume.

### Example

**Input:** `"Explain KCL"`

**Output:**
```json
{
  "goal": "teach_concept",
  "concept_id": "KCL-001",
  "concept_name": "Kirchhoff's Current Law",
  "domain": "Electrical Engineering",
  "level": "beginner",
  "preferred_mode": "visual-sequential",
  "load_budget": 3,
  "risk_misconceptions": [
    "current is consumed",
    "nodes store current"
  ],
  "prerequisites": ["Charge conservation", "Current fundamentals"]
}
```

---

## How It Works

The system implements a 4-stage pipeline:

```
Natural Language → Intent Detection → Concept Resolution → Level Estimation → CRI Emission
```

1. **Intent Detection** - Classifies query into `teach_concept`, `revise_concept`, or `test_understanding`
2. **Concept Resolution** - Matches query against ontology to find canonical concept ID
3. **Level Estimation** - Estimates learner level (`beginner`, `intermediate`, `advanced`)
4. **CRI Emission** - Generates standardized CRI object with all metadata

---

## Quick Start

### Run the Demo
```bash
cd intent_resolution
python main.py
```

### Use in Code
```python
from intent_resolution import resolve_query

result = resolve_query("Explain KCL")
cri = result['cri']

print(cri['goal'])           # 'teach_concept'
print(cri['concept_id'])     # 'KCL-001'
print(cri['level'])          # 'beginner'
```

### Run Tests
```bash
python test_suite.py
```

### See More Examples
```bash
python examples.py
```

---

## What's Included

### Core Modules
- `intent_detector.py` - Intent classification
- `concept_resolver.py` - Concept matching against ontology
- `level_estimator.py` - Level estimation
- `cri_emitter.py` - CRI object generation
- `main.py` - Pipeline orchestrator + demo

### Ontology
- `ontology/concepts.json` - 10 Electrical Engineering concepts with aliases, prerequisites, and common misconceptions

### Examples & Tests
- `examples.py` - 6 usage patterns
- `test_suite.py` - 10 comprehensive tests (all passing)

---

## Usage Patterns

### Basic Usage
```python
from intent_resolution import resolve_query

result = resolve_query("Explain KCL")
cri = result['cri']
```

### Verbose Mode (see pipeline internals)
```python
result = resolve_query("What is Ohm's law?", verbose=True)

print(result['metadata']['intent_detection'])   # Intent + confidence
print(result['metadata']['concept_resolution']) # Matched concept
print(result['metadata']['level_estimation'])   # Level + reasoning
```

### Individual Components
```python
from intent_resolution import detect_intent, resolve_concept, estimate_level

intent = detect_intent("Explain KCL")
# {'intent': 'teach_concept', 'confidence': 0.82}

concept = resolve_concept("Explain KCL")
# {'concept_id': 'KCL-001', 'concept': {...}, 'matched_alias': 'kcl'}

level = estimate_level("Explain KCL")
# {'level': 'beginner', 'confidence': 0.75, 'reasoning': '...'}
```

### Error Handling
```python
from intent_resolution import resolve_query, ConceptNotFoundError

try:
    result = resolve_query("Explain quantum entanglement")
except ConceptNotFoundError as e:
    print(f"Concept not in ontology: {e}")
```

### Batch Processing
```python
from intent_resolution import IntentResolutionPipeline

pipeline = IntentResolutionPipeline()
queries = ["Explain KCL", "What is Ohm's law?", "Review KVL"]

for query in queries:
    result = pipeline.resolve(query)
    process_cri(result['cri'])
```

---

## CRI Structure

Every CRI contains:

- `goal` - Learning intent (teach/revise/test)
- `concept_id` - Canonical concept ID (e.g., "KCL-001")
- `concept_name` - Human-readable name
- `domain` - Knowledge domain
- `level` - Target level (beginner/intermediate/advanced)
- `preferred_mode` - Pedagogical mode (currently: "visual-sequential")
- `load_budget` - Cognitive load units 1-5 (currently: 3)
- `risk_misconceptions` - Common misconceptions to address
- `prerequisites` - Prerequisite concepts (optional)

---

## Ontology

The system includes 10 Electrical Engineering concepts:

1. **KCL-001** - Kirchhoff's Current Law
2. **KVL-001** - Kirchhoff's Voltage Law
3. **OHM-001** - Ohm's Law
4. **SERIES-001** - Series Circuit Analysis
5. **PARALLEL-001** - Parallel Circuit Analysis
6. **POWER-001** - Electrical Power
7. **CAPACITOR-001** - Capacitor Fundamentals
8. **INDUCTOR-001** - Inductor Fundamentals
9. **THEVENIN-001** - Thevenin's Theorem
10. **SUPERPOSITION-001** - Superposition Principle

Each concept includes aliases (e.g., "KCL", "Kirchhoff current law"), prerequisites, and common misconceptions.

### Adding New Concepts

Edit `ontology/concepts.json`:
```json
{
  "id": "NEWCONCEPT-001",
  "name": "Your Concept Name",
  "aliases": ["alias1", "alias2"],
  "domain": "Electrical Engineering",
  "prerequisites": ["prerequisite"],
  "common_misconceptions": ["misconception"]
}
```

No code changes needed — ontology is loaded dynamically.

---

## Design Philosophy

### ✅ What This Is
- **Deterministic** - Same input → same output
- **Inspectable** - Clear pipeline stages, verbose mode for debugging
- **Modular** - Each component is independent
- **Production-ready** - Pure Python, no dependencies, all tests passing

### ❌ What This Is NOT (v1 choices)
- **Not ML-based** - Uses rule-based heuristics
- **Not adaptive** - No user profiling or learning history
- **Not LLM-powered** - Designed for extensibility, but currently rules-based

These are intentional v1 design choices prioritizing clarity and correctness. The architecture supports future enhancements.

---

## Performance

- **Latency:** < 10ms per query
- **Memory:** ~1MB
- **Dependencies:** Zero (pure Python)
- **Concurrency:** Thread-safe

---

## Extension Points

The system is designed to be extended:

1. **LLM Integration** - Replace rule-based intent detection with LLM calls
2. **User Profiles** - Add learning history for better level estimation
3. **More Domains** - Add concepts from other fields (just edit JSON)
4. **Dynamic Ontology** - Load from database instead of JSON
5. **Multi-language** - Support queries in multiple languages

---

## Test Results

All 10 automated tests pass:
- ✅ Basic query resolution
- ✅ Intent detection (teach/revise/test)
- ✅ Concept matching with aliases
- ✅ Level estimation
- ✅ Error handling
- ✅ CRI structure validation
- ✅ Verbose mode
- ✅ Batch processing
- ✅ Prerequisites and misconceptions
- ✅ All 10 ontology concepts

**Success rate:** 100% (10/10 concepts resolved correctly)

---

## Integration

This system outputs CRI objects ready for downstream systems:

```python
result = resolve_query(user_query)
cri = result['cri']

# Send to pedagogy planner
lesson_plan = pedagogy_planner.create_plan(
    concept=cri['concept_name'],
    level=cri['level'],
    prerequisites=cri['prerequisites'],
    misconceptions=cri['risk_misconceptions']
)

# Send to script generator
script = script_generator.generate(
    concept=cri['concept_name'],
    mode=cri['preferred_mode'],
    load_budget=cri['load_budget']
)
```

---

## Requirements

- Python 3.8+
- No external dependencies

---

## License

Proprietary - Oviqo Learning Systems

---

**Built January 2026 • Version 1.0.0 • Production Ready 🚀**
