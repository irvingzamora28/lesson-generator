from abc import ABC, abstractmethod
from typing import List, Optional
from lesson_generator.error_handling import LessonGenerationError

class AIProvider(ABC):
    """Base class for AI providers"""
    
    @abstractmethod
    def generate_content(
        self,
        lesson_title: str,
        section_title: str,
        section_components: List[str],
        section_elements: List[str],
        prompt: str,
        max_tokens: Optional[int] = 150,
    ) -> str:
        """Generate content for a lesson section"""
        pass

    @abstractmethod
    def generate_json_audio_text(self, section_content: str) -> str:
        """Generate JSON format for audio text"""
        pass

    @abstractmethod
    def generate_vocabulary(
        self,
        lesson_title: str,
        vocabulary_words: List[str],
        properties: List[str]
    ) -> str:
        """Generate vocabulary content"""
        pass

class OpenAIProvider(AIProvider):
    """OpenAI implementation"""
    
    def __init__(self):
        from lesson_generator.openai_api import (
            generate_content as openai_generate_content,
            generate_json_audio_text as openai_generate_audio,
            generate_vocabulary as openai_generate_vocabulary,
        )
        self._generate_content = openai_generate_content
        self._generate_audio = openai_generate_audio
        self._generate_vocabulary = openai_generate_vocabulary

    def generate_content(self, *args, **kwargs) -> str:
        return self._generate_content(*args, **kwargs)

    def generate_json_audio_text(self, section_content: str) -> str:
        return self._generate_audio(section_content)

    def generate_vocabulary(self, *args, **kwargs) -> str:
        return self._generate_vocabulary(*args, **kwargs)

class GeminiProvider(AIProvider):
    """Google Gemini implementation"""
    
    def __init__(self):
        from lesson_generator.gemini_api import (
            generate_content as gemini_generate_content,
            generate_json_audio_text as gemini_generate_audio,
            generate_vocabulary as gemini_generate_vocabulary,
        )
        self._generate_content = gemini_generate_content
        self._generate_audio = gemini_generate_audio
        self._generate_vocabulary = gemini_generate_vocabulary

    def generate_content(self, *args, **kwargs) -> str:
        return self._generate_content(*args, **kwargs)

    def generate_json_audio_text(self, section_content: str) -> str:
        return self._generate_audio(section_content)

    def generate_vocabulary(self, *args, **kwargs) -> str:
        return self._generate_vocabulary(*args, **kwargs)

def get_ai_provider(provider_name: str) -> AIProvider:
    """Factory function to get the appropriate AI provider"""
    providers = {
        'openai': OpenAIProvider,
        'gemini': GeminiProvider,
    }
    
    provider_class = providers.get(provider_name.lower())
    if not provider_class:
        raise LessonGenerationError(f"Unknown AI provider: {provider_name}")
    
    return provider_class()
