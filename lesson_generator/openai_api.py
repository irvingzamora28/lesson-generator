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


def generate_content(
    lesson_title,
    section_title,
    section_components,
    section_elements,
    prompt,
    max_tokens=150,
):
    ai_assistant_message = t("message.ai_assistant_message")
    user_instruction = t("message.instruction", prompt=prompt)
    components_string = ", ".join(section_components)
    elements_string = ", ".join(section_elements)

    components_prompt = f"""
    When generating the content you have a few components that you can incorporate, these components are useful building blocks for explanations and are used differently depending on the lesson content and context.
    I' will give you the list of components available and what their use is for:
    1. TextToSpeechPlayer
    Purpose: The TextToSpeechPlayer component is used to incorporate an audio player in the lesson content. This component plays a pronunciation guide or the examples shown in the lesson.
    Usage: It requires a parameter indicating the source of the audio file, usually a path to the audio file relative to the lesson content directory.
    Example usage: <TextToSpeechPlayer mp3File={{/src/assets/courses/spanish/_shared/lessons/lesson2/audio/tricky-j.mp3}} />
    2. TipBox
    Purpose: The TipBox component is used to highlight tips, notes, or important information in a visually distinct box. It's used to draw the learner's attention to key points, suggestions, or additional information that can aid understanding or retention of the lesson material.
    Usage: It encloses a piece of text or a list of items that are presented as bullet points. This component helps in breaking the monotony of the lesson text and making the content more engaging.
    Example usage: <TipBox>
        - **Pronunciation Practice**: Listen to native speakers and try to imitate the sounds.
        - **Patience**: Some sounds take time to master, so keep practicing regularly. 
        - **Record Yourself**: Recording and listening to yourself can be a great way to notice and correct your pronunciation.
        </TipBox>
    3. Mnemonic
    Purpose: The Mnemonic component is used to provide mnemonic devices or memory aids. Mnemonics are techniques a person can use to help them improve their ability to remember something, making it easier for learners to remember terms, grammar rules, or concepts.
    Usage: It contains a title and a text or phrase that makes learning and recalling specific information easier. This component is especially useful in language learning for memorizing vocabulary, verb conjugations, and other grammar rules.
    Example usage: <Mnemonic title={{A suitable title}} content={{Think of the sound you make when you're trying to fog up a mirror with your breath but make it harsher.}} />

    In the content of this lesson, you must use the following components: {components_string}, and remember how they are used, the parameters expected and the correct format.
    """

    elements_prompt = f"""MDX supports different components like ordered lists, unordered lists, tables, etc. In this section, you must incorporate the following elements: {elements_string}.
    """
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
                    {elements_prompt if elements_string else ''}
                    {components_prompt if components_string else ''}
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


def generate_json_audio_text(section_content):
    data = {
        "model": "gpt-3.5-turbo-1106",
        "messages": [
            {
                "role": "system",
                "content": f"""You are a great educator and know very well how to teach in easy steps. 
                           The output you are generating is in mostly in spanish.""",
            },
            {
                "role": "user",
                "content": f"""You are going to generate a json string, this is going to have two properties, text and audio_file_name.
                The text is going to be the text from the examples of the lesson, the audio_file_name is going to be the name of the file name. I will show you an example:
                If the input is the following:
                ## Section 1: The Tricky 'J' Sound
                The letter 'j' in Spanish is pronounced like the 'h' in "hot" in English but stronger and comes from deep in the throat. It's a guttural sound that is distinct in words like "jirafa" (giraffe).
                Practice words:

                | Word   | Pronunciation |
                | ------ | ------------- |
                | Jirafa | hee-rah-fah   |
                | Jugo   | hoo-goh       |
                | Joven  | hoh-vehn      |
                | Jardín | hahr-deen     |
                | Caja   | kah-hah       |

                <Mnemonic title={{Mnemonic}} content={{Think of the sound you make when you're trying to fog up a mirror with your breath but make it harsher.}} />

                <TextToSpeechPlayer mp3File={{/src/assets/courses/spanish/_shared/lessons/lesson2/audio/tricky-j.mp3}} />
                
                The output should be the following:
                
                {{
                    'text': 'Jirafa ... Jugo ... Joven ... Jardín ... Caja',
                    'audio_file_name': 'tricky-j.mp3'
                }}
                
                Another example, if the input is the following:
                ## Section 3: Pronouns

                Pronouns replace nouns and are used frequently in everyday conversation. They must match the gender and number of the noun they replace.

                ### Subject Pronouns

                | Pronoun (English) | Pronoun (Spanish) | Example Sentence                        |
                | ----------------- | ----------------- | --------------------------------------- |
                | I                 | Yo                | Yo soy estudiante.                      |
                | You (informal)    | Tú                | ¿Tú eres el profesor?                   |
                | He/She/           | Él/Ella           | Él es mi hermano. Ella es mi hermana.   |
                | You formal        | Usted             | ¿Cómo está usted?                       |
                | You plural        | Ustedes           | Ustedes son amables.                    |
                | We                | Nosotros/Nosotras | Nosotros estudiamos español.            |
                | They              | Ellos/Ellas       | Ellos hablan español. Ellas también.    |
                | It                | Eso/Esa           | Eso es interesante. Esa casa es bonita. |

                <TextToSpeechPlayer mp3File={{/src/assets/courses/spanish/_shared/lessons/lesson5/audio/subject-pronouns.mp3}} />

                Explanation on How to Use Pronouns:

                Pronouns in Spanish replace nouns and agree with the gender and number of the noun they replace. Understanding subject pronouns is essential for constructing sentences as they often come at the beginning. Subject pronouns indicate who is doing the action.

                To form subject pronouns, simply use them in place of the person's name or the noun.
                
                The output shoudl be the following:
                
                {{
                    'text': 'Yo soy estudiante ... ¿Tú eres el profesor? ... Él es mi hermano. Ella es mi hermana ... ¿Cómo está usted? ... Ustedes son amables ... Nosotros estudiamos español ... Ellos hablan español. Ellas también ... Eso es interesante. Esa casa es bonita',
                    'audio_file_name': 'subject-pronouns.mp3'
                }}
                
                Notice that the text property contains the text of the concepts the learner needs to understand concatenated with ' ... ' in between to separate the examples.
                The audio_file_name contains the name of the audio file for that section.
                
                
                Generate the json for this section based on the following content: 
                {section_content}. 
                Generate the json string and only the json string in json format. 
                Do not include text about what you did, your thought process or any other messages, 
                just the generated string in json format. 
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
