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
                "content": f"""You are a great educator and know very well how to teach in easy steps. 
                           You know very well how to output format in MDX. 
                           The output you are generating is in English.""",
            },
            {
                "role": "user",
                "content": f"""You are going to generate content for the lesson with the title {lesson_title}, 
                           but you are going to generate only a section, the section you are going to generate is {section_title}. 
                           Generate the content for this section based on the prompt {prompt}. 
                           Generate the content and only the content in an MDX format. 
                           Do not include text about what you did, your thought process or any other messages, 
                           just the generated content in MDX format. 
                           Also omit the title of the lesson and the title of the section, just provide the content. 
                           You can generate tables if you think the section needs one for better structure of the explanation or examples you give.
                           Do not format the output with ```markdown, ```mdx or anything like that.""",
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
        "model": "gpt-3.5-turbo-1106",
        "messages": [
            {
                "role": "system",
                "content": f"""You are a great educator and know very well how to teach in easy steps. 
                            You know very well how to output format in MDX. 
                            The output you are generating is in English.""",
            },
            {
                "role": "user",
                "content": f"""You are going to generate vocabulary for the lesson with the title {lesson_title},
                            The vocabulary words are {vocabulary_string}.
                            The vocabulary you are going to generate in an MDX format and will have the following properties {properties_string}.
                            Here is an example of the vocabulary in MDX format generated with the words: jirafa, huevo, guerra, cielo, año, and the properties: word, translation, exampleSentence, exampleTranslation, gender, challenge:
                            vocabulary:
                                - word: "jirafa"
                                translation: "giraffe"
                                exampleSentence: "La jirafa tiene un cuello largo."
                                exampleTranslation: "The giraffe has a long neck."
                                gender: "fem"
                                challenge: "The 'j' is pronounced like an English 'h'."
                                - word: "huevo"
                                translation: "egg"
                                exampleSentence: "Quiero un huevo frito."
                                exampleTranslation: "I want a fried egg."
                                gender: "masc"
                                challenge: "Remember that 'h' is always silent."
                                - word: "guerra"
                                translation: "war"
                                exampleSentence: "La guerra no es la solución."
                                exampleTranslation: "War is not the solution."
                                gender: "fem"
                                challenge: "'G' before 'u' and 'e' can be tricky."
                                - word: "cielo"
                                translation: "sky"
                                exampleSentence: "El cielo es azul."
                                exampleTranslation: "The sky is blue."
                                gender: "masc"
                                challenge: "'C' before 'i' and 'e' sounds like 'th' in Spain and 's' in Latin America."
                                - word: "año"
                                translation: "year"
                                exampleSentence: "Cada año vamos a la playa."
                                exampleTranslation: "Every year we go to the beach."
                                gender: "masc"
                                challenge: "The 'ñ' sound doesn't exist in English."
                                
                            Generate the content and only the content in an MDX format. 
                            Do not include text about what you did, your thought process or any other messages, 
                            just the generated content in MDX format. 
                            Also omit the title of the lesson and the title of the section, just provide the content.
                            Do not format the output with ```markdown, ```mdx or anything like that.""",
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
