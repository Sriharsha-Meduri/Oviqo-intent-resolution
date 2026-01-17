import json
import os
import re
from typing import Dict, List, Optional
from pathlib import Path


class ConceptNotFoundError(Exception):
    pass


class ConceptResolver:
    def __init__(self, ontology_path: Optional[str] = None):
        if ontology_path is None:
            current_dir = Path(__file__).parent
            ontology_path = current_dir / "ontology" / "concepts.json"
        
        self.ontology_path = ontology_path
        self.concepts = self._load_ontology()
        self._build_lookup_index()
    
    def _load_ontology(self) -> List[Dict]:
        with open(self.ontology_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('concepts', [])
    
    def _build_lookup_index(self):
        self.alias_to_id = {}
        
        for concept in self.concepts:
            concept_id = concept['id']
            
            normalized_name = self._normalize_text(concept['name'])
            self.alias_to_id[normalized_name] = concept_id
            
            for alias in concept.get('aliases', []):
                normalized_alias = self._normalize_text(alias)
                self.alias_to_id[normalized_alias] = concept_id
    
    def _normalize_text(self, text: str) -> str:
        return re.sub(r'\s+', ' ', text.lower().strip())
    
    def extract_candidates(self, query: str) -> List[str]:
        query_normalized = self._normalize_text(query)
        candidates = []
        
        for alias in self.alias_to_id.keys():
            if alias in query_normalized:
                candidates.append(alias)
        
        candidates.sort(key=len, reverse=True)
        
        return candidates
    
    def resolve(self, query: str) -> Dict[str, any]:
        candidates = self.extract_candidates(query)
        
        if not candidates:
            raise ConceptNotFoundError(
                f"No matching concept found for query: '{query}'"
            )
        
        matched_alias = candidates[0]
        concept_id = self.alias_to_id[matched_alias]
        
        concept = self._get_concept_by_id(concept_id)
        
        return {
            "concept_id": concept_id,
            "concept": concept,
            "matched_alias": matched_alias
        }
    
    def _get_concept_by_id(self, concept_id: str) -> Dict:
        for concept in self.concepts:
            if concept['id'] == concept_id:
                return concept
        
        raise ValueError(f"Concept ID {concept_id} not found in ontology")
    
    def get_all_concepts(self) -> List[Dict]:
        return self.concepts.copy()


def resolve_concept(query: str, ontology_path: Optional[str] = None) -> Dict[str, any]:
    resolver = ConceptResolver(ontology_path)
    return resolver.resolve(query)
