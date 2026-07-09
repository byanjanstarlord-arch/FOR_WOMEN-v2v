import json
from .exceptions import AIValidationException

def validate_json_response(response_text: str) -> dict:
    """Extracts and validates JSON from AI response."""
    try:
        # Sometimes AI returns markdown code blocks, try to strip them
        text = response_text.strip()
        if text.startswith('```json'):
            text = text[7:]
        elif text.startswith('```'):
            text = text[3:]
        
        if text.endswith('```'):
            text = text[:-3]
            
        text = text.strip()
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise AIValidationException(f"Failed to parse AI response as JSON: {e}")
