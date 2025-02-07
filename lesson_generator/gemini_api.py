from google import genai
from google.genai import types
from i18n import t
from .constants import GEMINI_API_KEY
from lesson_generator.log import logger
from lesson_generator.error_handling import LessonGenerationError
from lesson_generator.prompts import (
    get_content_generation_prompt,
    AUDIO_TEXT_SYSTEM_MESSAGE,
    AUDIO_TEXT_GENERATION_PROMPT,
    VOCABULARY_SYSTEM_MESSAGE,
    VOCABULARY_GENERATION_PROMPT,
    CONTENT_SYSTEM_MESSAGE
)

# Configure the Gemini API
client = genai.Client(api_key=GEMINI_API_KEY)

# Initialize the model
model = 'gemini-2.0-flash'

def generate_content(
    lesson_title,
    section_title,
    section_components,
    section_elements,
    prompt,
    max_tokens=5000,
):
    """
    Generate content using Google's Gemini API
    """
    try:
        # Get the formatted prompt using the shared prompt generator
        user_message = get_content_generation_prompt(
            lesson_title=lesson_title,
            section_title=section_title,
            section_components=section_components,
            section_elements=section_elements,
            prompt=prompt
        )

        # Generate content using Gemini
        response = client.models.generate_content(
            model=model,
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=CONTENT_SYSTEM_MESSAGE,
                max_output_tokens= max_tokens,
                temperature= 0.7,
            ),
        )

        # Check if the response is valid
        if not response.text:
            raise LessonGenerationError("Empty response received from Gemini API")

        return response.text

    except Exception as e:
        logger.error(f"Error generating content with Gemini: {str(e)}")
        raise LessonGenerationError(f"Failed to generate content: {str(e)}")

def generate_json_audio_text(section_content, max_tokens=5000):
    """
    Generate JSON format for audio text using Gemini
    """
    try:
        response = client.models.generate_content(
            model=model,
            contents=AUDIO_TEXT_GENERATION_PROMPT.format(section_content=section_content),
            config=types.GenerateContentConfig(
                system_instruction=AUDIO_TEXT_SYSTEM_MESSAGE,
                max_output_tokens= max_tokens,
                response_mime_type= 'application/json',
                temperature= 0.7,
            ),
        )
        
        if not response.text:
            raise LessonGenerationError("Empty response received from Gemini API")
            
        return response.text

    except Exception as e:
        logger.error(f"Error generating audio text with Gemini: {str(e)}")
        raise LessonGenerationError(f"Failed to generate audio text: {str(e)}")

def generate_vocabulary(lesson_title, vocabulary_words, properties, max_tokens=5000):
    """
    Generate vocabulary content using Gemini
    """
    try:
        vocabulary_string = ", ".join(vocabulary_words)
        properties_string = ", ".join(properties)

        response = client.models.generate_content(
            model=model,
            contents=VOCABULARY_GENERATION_PROMPT.format(
                    lesson_title=lesson_title,
                    vocabulary_string=vocabulary_string,
                    properties_string=properties_string
                ),
            config=types.GenerateContentConfig(
                system_instruction=VOCABULARY_SYSTEM_MESSAGE,
                max_output_tokens= max_tokens,
                temperature= 0.7,
            ),
        )
        
        if not response.text:
            raise LessonGenerationError("Empty response received from Gemini API")
            
        return response.text

    except Exception as e:
        logger.error(f"Error generating vocabulary with Gemini: {str(e)}")
        raise LessonGenerationError(f"Failed to generate vocabulary: {str(e)}")
