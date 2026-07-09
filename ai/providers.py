import os
import requests
import logging
from django.conf import settings
from .exceptions import AIProviderException

logger = logging.getLogger(__name__)

class OpenRouterProvider:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.url = "https://openrouter.ai/api/v1/chat/completions"
        self.primary_model = "qwen/qwen-2.5-coder-32b-instruct"
        self.fallback_model = "meta-llama/llama-3.1-8b-instruct"
        
    def generate(self, messages, use_fallback=False, temperature=0.7):
        if not self.api_key:
            raise AIProviderException("OPENROUTER_API_KEY is not configured")
            
        model = self.fallback_model if use_fallback else self.primary_model
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "HerSakhi",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(self.url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            logger.error(f"OpenRouter API error: {e}")
            if not use_fallback:
                logger.info("Attempting fallback model...")
                return self.generate(messages, use_fallback=True, temperature=temperature)
            raise AIProviderException(f"AI provider failed after fallback: {e}")

# Factory function to get the configured provider
def get_ai_provider():
    return OpenRouterProvider()
