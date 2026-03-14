import re

from json_repair import repair_json

from app.schemas import PayslipData


def extract_json(text: str) -> dict:
    """Robustly extract and validate a payslip JSON object from raw LLM output.

    Handles all common LLM misbehaviours:
    - Markdown code fences (```json ... ```)
    - Extra prose / footer before or after the JSON object
    - Malformed JSON (missing quotes, trailing commas, unclosed brackets)
    - Stringified JSON wrapped in a single field: {"explanation": "{...}"}

    Uses json-repair to auto-fix broken JSON rather than manual multi-try parsing.
    Uses PayslipData (Pydantic) to coerce types and fill defaults after parsing.
    """
    # 1. Strip markdown fences
    text = re.sub(r"```(?:json)?\s*", "", text, flags=re.IGNORECASE).strip()

    # 2. Locate the outermost { ... } block (strips leading/trailing prose)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("No JSON object found in LLM response")

    candidate = text[start : end + 1]

    # 3. Repair and parse — handles malformed JSON from LLMs
    result = repair_json(candidate, return_objects=True)
    if not isinstance(result, dict):
        raise ValueError("No valid JSON object found in LLM response")

    result = _unwrap_if_needed(result)

    # 4. Validate and normalise through the Pydantic schema
    return PayslipData.model_validate(result).model_dump()


def _unwrap_if_needed(obj: dict) -> dict:
    """If the LLM wrapped real JSON as a stringified value, unwrap one level."""
    for val in obj.values():
        if isinstance(val, str) and val.strip().startswith("{"):
            inner = val.strip()
            dash_pos = inner.rfind("\n---")
            if dash_pos != -1:
                inner = inner[:dash_pos].strip()
            repaired = repair_json(inner, return_objects=True)
            if isinstance(repaired, dict):
                return repaired
    return obj
