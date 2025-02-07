import requests
from i18n import t
from .constants import OPENAI_API_KEY
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

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}

# model = "gpt-4o-mini"
model = "gpt-3.5-turbo-1106"


def generate_content(
    lesson_title,
    section_title,
    section_components,
    section_elements,
    prompt,
    max_tokens=150,
):
    user_message = get_content_generation_prompt(
        lesson_title=lesson_title,
        section_title=section_title,
        section_components=section_components,
        section_elements=section_elements,
        prompt=prompt
    )
    logger.info(f"Generating content: {user_message} \n\n\n")
    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": CONTENT_SYSTEM_MESSAGE,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ],
    }

    try:
        response = requests.post(OPENAI_API_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        response_data = response.json()
        generated_text = response_data.get("choices")[0]["message"]["content"].strip()
        return generated_text
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise LessonGenerationError("OpenAI API request failed: HTTP error occurred")
    except requests.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        raise LessonGenerationError("OpenAI API request failed: Request error occurred")
    except Exception as e:
        logger.error(f"Error during OpenAI API call: {e}")
        raise LessonGenerationError(
            "OpenAI API request failed: Unexpected error occurred"
        )


def generate_json_audio_text(section_content):
    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": AUDIO_TEXT_SYSTEM_MESSAGE,
            },
            {
                "role": "user",
                "content": AUDIO_TEXT_GENERATION_PROMPT.format(section_content=section_content),
            },
        ],
    }

    try:
        response = requests.post(OPENAI_API_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        response_data = response.json()
        generated_text = response_data.get("choices")[0]["message"]["content"].strip()
        return generated_text
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise LessonGenerationError("OpenAI API request failed: HTTP error occurred")
    except requests.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        raise LessonGenerationError("OpenAI API request failed: Request error occurred")
    except Exception as e:
        logger.error(f"Error during OpenAI API call: {e}")
        raise LessonGenerationError(
            "OpenAI API request failed: Unexpected error occurred"
        )


def generate_vocabulary(lesson_title, vocabulary_words, properties):
    vocabulary_string = ", ".join(vocabulary_words)
    properties_string = ", ".join(properties)
    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": VOCABULARY_SYSTEM_MESSAGE,
            },
            {
                "role": "user",
                "content": VOCABULARY_GENERATION_PROMPT.format(
                    lesson_title=lesson_title,
                    vocabulary_string=vocabulary_string,
                    properties_string=properties_string
                ),
            },
        ],
    }

    try:
        response = requests.post(OPENAI_API_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        response_data = response.json()
        generated_text = response_data.get("choices")[0]["message"]["content"].strip()
        return generated_text
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise LessonGenerationError("OpenAI API request failed: HTTP error occurred")
    except requests.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        raise LessonGenerationError("OpenAI API request failed: Request error occurred")
    except Exception as e:
        logger.error(f"Error during OpenAI API call: {e}")
        raise LessonGenerationError(
            "OpenAI API request failed: Unexpected error occurred"
        )


def generate_lesson_sections(prompt):
    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a language learning expert who specializes in creating structured lesson content. You will generate JSON lesson sections based on the provided input.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.7,
        "max_tokens": 2000,  # Increased token limit for generating full lesson structure
        "response_format": { "type": "json_object" }  # Ensure response is valid JSON
    }

    try:
        response = requests.post(OPENAI_API_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        response_data = response.json()
        generated_text = response_data.get("choices")[0]["message"]["content"].strip()
        return generated_text
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise LessonGenerationError("OpenAI API request failed: HTTP error occurred")
    except requests.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        raise LessonGenerationError("OpenAI API request failed: Request error occurred")
    except Exception as e:
        logger.error(f"Error during OpenAI API call: {e}")
        raise LessonGenerationError(
            "OpenAI API request failed: Unexpected error occurred"
        )
