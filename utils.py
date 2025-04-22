import re
from typing import Tuple, List, Dict

# Define PII patterns for masking
PII_PATTERNS = {
    "full_name": r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",
    "email": r"[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+",
    "phone_number": r"(\+?\d{1,3}[\-\s]?)?\d{10}",
    "dob": r"\b\d{2}[\/\-]\d{2}[\/\-]\d{4}\b",
    "aadhar_num": r"\b\d{4} \d{4} \d{4}\b",
    "credit_debit_no": r"\b(?:\d[ -]*?){13,16}\b",
    "cvv_no": r"\b\d{3}\b",
    "expiry_no": r"\b(0[1-9]|1[0-2])\/(?:\d{2}|\d{4})\b"
}


def mask_pii(text: str) -> Tuple[str, List[Dict], Dict]:
    """
    Mask all occurrences of PII in the text.
    Returns:
      masked_text: str
      entities: List of dicts with position, classification, and original entity
      pii_data: mapping from label to list of original values
    """
    masked_text = text
    entities: List[Dict] = []
    pii_data: Dict[str, List[str]] = {}

    # Iterate each pattern and replace matches
    for label, pattern in PII_PATTERNS.items():
        for match in re.finditer(pattern, text):
            entity = match.group()
            start, end = match.span()
            placeholder = f"[{label}]"
            # Replace the specific occurrence
            masked_text = masked_text[:start] + placeholder + masked_text[end:]
            entities.append({
                "position": [start, start + len(placeholder)],
                "classification": label,
                "entity": entity
            })
            pii_data.setdefault(label, []).append(entity)

    return masked_text, entities, pii_data


def demask_pii(masked_text: str, pii_data: Dict[str, List[str]]) -> str:
    """
    Restore masked PII placeholders back to original values in order.
    """
    demasked = masked_text
    for label, values in pii_data.items():
        placeholder = f"[{label}]"
        for val in values:
            demasked = demasked.replace(placeholder, val, 1)
    return demasked