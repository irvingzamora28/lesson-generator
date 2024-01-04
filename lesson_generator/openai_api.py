import requests
from i18n import t
from .constants import OPENAI_API_KEY
from lesson_generator.log import logger
from lesson_generator.error_handling import LessonGenerationError

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

def generate_content(prompt, max_tokens=150):
    ai_assistant_message = t('message.ai_assistant_message')
    user_instruction = t('message.instruction', prompt=prompt)

    data = {
        "model": "gpt-3.5-turbo-1106",
        "messages": [
            {
                "role": "system",
                "content": "You are a great educator and know very well how to teach difficult concepts in easy steps. You know very well how to output format in MDX"
            },
            {
                "role": "user",
                "content": "Generate in MDX format " + prompt
            }
        ]
    }
    try:
        response = requests.post(OPENAI_API_URL, headers=HEADERS, json=data)
        response.raise_for_status()
        response_data = response.json()
        generated_text = response_data.get("choices")[0]['message']['content'].strip()
        return generated_text
    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        raise LessonGenerationError("OpenAI API request failed: HTTP error occurred")
    except requests.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        raise LessonGenerationError("OpenAI API request failed: Request error occurred")
    except Exception as e:
        logger.error(f"Error during OpenAI API call: {e}")
        raise LessonGenerationError("OpenAI API request failed: Unexpected error occurred")