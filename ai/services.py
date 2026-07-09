from .providers import get_ai_provider
from .validators import validate_json_response
import logging

logger = logging.getLogger(__name__)

def generate_ai_response(system_prompt: str, user_prompt: str) -> dict:
    """
    Core function to communicate with AI provider and return parsed JSON.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    provider = get_ai_provider()
    try:
        response_text = provider.generate(messages)
        return validate_json_response(response_text)
    except Exception as e:
        logger.error(f"AI Service Failure: {e}")
        # Always return structured failure instead of crashing
        return {
            "success": False,
            "message": "AI service is currently unavailable.",
            "error": str(e)
        }
