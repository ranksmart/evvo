import re

class Extractor:
    @staticmethod
    def extract_decision(mapping):
        mapping_match = re.search(r'^(Yes|No)', mapping.strip(), re.IGNORECASE)
        return mapping_match.group(0) if mapping_match else None

    @staticmethod
    def extract_rationale(mapping):
        rationale_match = re.search(r'Rationale:\s*(.*)', mapping.strip(), re.IGNORECASE | re.DOTALL)
        return rationale_match.group(1).strip() if rationale_match else None
