import requests
from i18n import t
from .constants import OPENAI_API_KEY
from lesson_generator.log import logger
from lesson_generator.error_handling import LessonGenerationError

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json",
}


def generate_content(lesson_title, section_title, prompt, max_tokens=150):
    ai_assistant_message = t("message.ai_assistant_message")
    user_instruction = t("message.instruction", prompt=prompt)

    data = {
        "model": "gpt-3.5-turbo-1106",
        "messages": [
            {
                "role": "system",
                "content": f"You are a great educator and know very well how to teach in easy steps. You know very well how to output format in MDX. The output you are generatting is in english.",
            },
            {
                "role": "user",
                "content": f"You are going to generate content for the lesson with the title {lesson_title}, but you are going to generate only a section, the section you are going to generate is {section_title}. Generate the content for this section based on the prompt {prompt}. Generate the content and only the content in an MDX format. Do not include text about what you did, your thought proccess or any other messages, just the generated content in MDX format. Also omit the title of the lesson and the title of the section, just provide the content.",
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
