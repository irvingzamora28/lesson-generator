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

    components_instructions = """
    You are creating an MDX-JSX file for educational purposes. Make sure to use the JSX components naturally and correctly within the educational content:

    - TextToSpeechPlayer: This component embeds audio related to the lesson. Use it without any title or explicit announcement. Just insert it where the audio example is necessary. Format: <TextToSpeechPlayer mp3File="relative_path_to_audio_file" />. Ensure the path is relevant to the content discussed.

    - TipBox: This component highlights key tips or important notes within the content. It should encapsulate a list of tips or a single tip directly, without any preceding title like "Tip:". Format: <TipBox>Here goes the tip or a list of tips.</TipBox>. It should be used to emphasize crucial points or suggestions naturally within the flow of the content.

    - Mnemonic: This component provides mnemonic aids for learning. Include it directly where the mnemonic aid is relevant to the lesson content. Do not precede it with any titles or introductions. It should appear as a natural part of the educational narrative. Format: <Mnemonic content="mnemonic_phrase" />. Ensure the content is helpful and relevant to the associated topic.
    
    An example of a section that uses correctly all JSX components is the following:
    
    ## Section 2: Articles

    Articles in Spanish must agree in gender and number with the noun they accompany. There are definite articles (the) and indefinite articles (a, an).

    ### Definite Articles

    | English         | Spanish Singular | Spanish Plural | Example Sentence     |
    | --------------- | ---------------- | -------------- | -------------------- |
    | The (masculine) | El               | Los            | El libro, Los libros |
    | The (feminine)  | La               | Las            | La casa, Las casas   |

    ### Indefinite Articles

    | English       | Spanish Singular | Spanish Plural | Example Sentence      |
    | ------------- | ---------------- | -------------- | --------------------- |
    | A (masculine) | Un               | Unos           | Un libro, Unos libros |
    | A (feminine)  | Una              | Unas           | Una casa, Unas casas  |

    <TextToSpeechPlayer mp3File="/src/assets/courses/spanish/_shared/lessons/lesson5/audio/articles.mp3" />

    Explanation on How to Form Articles:

    The articles in Spanish change based on the gender (masculine or feminine) and number (singular or plural) of the noun they precede. Definite articles are used for specific items known to the speaker ('the' in English), while indefinite articles are used for nonspecific items ('a,' 'an,' or 'some' in English). To form the correct article, first, identify the gender and number of the noun, then choose the corresponding article:

    Use "el" for masculine singular, "los" for masculine plural.
    Use "la" for feminine singular, "las" for feminine plural.
    Use "un" for masculine singular, "unos" for masculine plural.
    Use "una" for feminine singular, "unas" for feminine plural.

    <Mnemonic title="Definite Articles" content="El is E for masculine singular, La is L for feminine singular, Los is plural masculine, Las is plural feminine" />

    <TipBox>
    Remember:
    - Pronouns replace nouns in a sentence
    </TipBox>

    ___
    
    IMPORTANT: Each component MUST be used correctly into the content, appropriately and naturally. Avoid misuse or incorrect parameterization of these components.
    """

    user_message = f"""
    Generate content for the lesson titled "{lesson_title}", specifically the section titled "{section_title}". 
    The content should be clear, instructional, and engaging, formatted in MDX with natural integration of the specified JSX components and MDX elements. 
    Avoid creating content as a React component or any form of software code. Instead, focus on the narrative and educational material suitable for students. 
    {components_instructions if components_string else ''}
    Remember, the content should not include explicit titles or annotations for the components, and avoid redundancy or unnecessary repetition. Provide only the generated content in MDX format.
    """

    elements_instructions = """
    MDX elements refer to markdown elements like headers, lists, and tables used to structure the content. Use the specified elements to organize the content clearly and effectively.
    For instance, use tables to compare words or show translation and concise examples. When using tables use more than 3 columns and 3 rows for meaningful content.
    A good example of the table use is the following:
    | Noun (English)  | Noun (Spanish) | Gender    | Example Sentence                  |
    | --------------- | -------------- | --------- | --------------------------------- |
    | Friend          | Amigo          | Masculine | Mi amigo es alto.                 |
    | Book            | Libro          | Masculine | El libro está en la mesa.         |
    | Friend (female) | Amiga          | Feminine  | Mi amiga es inteligente.          |
    | House           | Casa           | Feminine  | La casa es grande.                |
    | Table           | Mesa           | Feminine  | Hay una mesa en la cocina.        |
    | Chair           | Silla          | Feminine  | Hay una silla en la sala.         |
    | Desk            | Escritorio     | Masculine | El escritorio está en la oficina. |
    
    Use list items for steps or tips, and ensure that the usage of these elements is directly relevant to the educational material. If an element like a table or list is mentioned, it must be used accordingly. Ensure each element enhances the lesson's educational value and readability.
    """

    content_instruction = f"""Generate the section content based on the prompt: {prompt}. Ensure the content is instructional and engaging. The content should be directly relevant to the lesson subject and formatted in MDX."""

    user_message = f"""
    You are going to generate content for the lesson titled "{lesson_title}", specifically the section titled "{section_title}". 
    {content_instruction}
    """

    if components_string:
        user_message += f"{components_instructions}The JSX components that MUST be used are: {components_string}. "
    if elements_string:
        user_message += f"{elements_instructions}The MDX elements that MUST be incorporated are: {elements_string}. In this case a {elements_string} was told to be used. So you MUST incorporate  {elements_string} into the generated content."

    user_message += f"""Note: Remember to provide only the generated content in MDX format without unnecessary explanations or meta-commentary.
                        Examples are very important to help students understand concepts. When you see pertinent the use of examples, use clear, concise examples to explain the key points and most importanly USE MANY examples, MORE THAN 6, THIS IS VERY IMPORTANT, USE MORE THAN 6 examples ALWAYS.
                        Generate the content and only the content in an MDX format. 
                        Do not include text about what you did, your thought process or any other messages, just the generated content in MDX format. 
                        Also omit the title of the lesson and the title of the section, just provide the content. 
                        Do not format the output with ```markdown, ```mdx or anything like that."""

    data = {
        "model": "gpt-3.5-turbo-1106",
        "messages": [
            {
                "role": "system",
                "content": "You are an educator tasked with creating engaging and educational content formatted in MDX. Use JSX components and MDX elements to enhance the lesson.",
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
                Notice that the text property does not contain any extra text like headings or explanations.
                Notice that the text property containts only and excluselively text or phrases in spanish.
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
