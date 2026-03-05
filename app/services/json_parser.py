import json
import re


def extract_json(text: str) -> dict:
    """Robustly extract a JSON object from raw LLM output.

    Handles all common LLM misbehaviours:
    - Markdown code fences (```json ... ```)
    - Stringified JSON wrapped in a single field: {"explanation": "{...}"}
    - Extra prose / viral footer before or after the JSON object
    """
    # 1. Strip markdown fences
    text = re.sub(r"```(?:json)?\s*", "", text, flags=re.IGNORECASE).strip()

    # 2. Try direct parse
    try:
        obj = json.loads(text)
        return _unwrap_if_needed(obj)
    except json.JSONDecodeError:
        pass

    # 3. Locate the outermost { ... } and try again
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            obj = json.loads(text[start : end + 1])
            return _unwrap_if_needed(obj)
        except json.JSONDecodeError:
            pass

    raise ValueError("No valid JSON object found in LLM response")


def _unwrap_if_needed(obj: dict) -> dict:
    """If the LLM wrapped real JSON as a stringified value, unwrap it."""
    if not isinstance(obj, dict):
        return obj
    # Pattern: {"explanation": "{...}", ...} or any single-key wrapper
    for val in obj.values():
        if isinstance(val, str) and val.strip().startswith("{"):
            inner = val.strip()
            # Strip any trailing footer (e.g. "---\n💡...")
            dash_pos = inner.rfind("\n---")
            if dash_pos != -1:
                inner = inner[:dash_pos].strip()
            try:
                return json.loads(inner)
            except json.JSONDecodeError:
                pass
    return obj
