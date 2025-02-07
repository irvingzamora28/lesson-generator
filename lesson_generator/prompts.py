"""
This module contains all the prompts used by different AI providers in the lesson generator.
"""

# System message for content generation
CONTENT_SYSTEM_MESSAGE = """
You are an educator tasked with creating engaging and educational content formatted in MDX. Use JSX components and MDX elements to enhance the lesson.
"""

# Common components instructions for content generation
COMPONENTS_INSTRUCTIONS = """
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

IMPORTANT: Each component MUST be used correctly into the content, appropriately and naturally. Avoid misuse or incorrect parameterization of these components These are the only JSX componets that exist so avoid using any other components.
"""

def get_content_generation_prompt(lesson_title, section_title, section_components, section_elements, prompt):
    components_string = ", ".join(section_components)
    elements_string = ", ".join(section_elements)
    
    user_message = f"""
    Generate content for the lesson titled "{lesson_title}", specifically the section titled "{section_title}". 
    {CONTENT_INSTRUCTION.format(prompt=prompt)}
    """

    if components_string:
        user_message += f"{COMPONENTS_INSTRUCTIONS}The JSX components that MUST be used are: {components_string}. "
    if elements_string:
        user_message += f"{ELEMENTS_INSTRUCTIONS}The MDX elements that MUST be incorporated are: {elements_string}. In this case a {elements_string} was told to be used. So you MUST incorporate {elements_string} into the generated content."

    user_message += CONTENT_ADDITIONAL_INSTRUCTIONS
    
    return user_message

# System message for audio text generation
AUDIO_TEXT_SYSTEM_MESSAGE = """You are a great educator and know very well how to teach in easy steps. 
The output you are generating is in mostly in spanish."""

# Prompt for generating lesson sections
LESSON_SECTIONS_PROMPT = """Your task is to generate a JSON lesson structure based on the provided input data. The output must strictly follow the specified JSON format. The key difference from a typical JSON schema is in how the vocabulary is handled.

Input:

The input will be a JSON object containing the following fields:

name: The name of the lesson.
lesson_number: The lesson's number.
description: A brief description of the lesson.
goals: An array of strings representing the learning goals of the lesson (e.g., "Fundamentals", "Vocabulary").

Output Format:

The output must be a valid JSON object with the following structure:

{
    "title": "Lesson Title",
    "description": "Lesson Description",
    "sections": [
        {
            "title": "Section Title",
            "about": "Section Description",
            "components": ["Component1", "Component2"],
            "elements": ["Element1", "Element2"]
        },
        ...
    ],
    "vocabulary": {
        "words": ["word1", "word2", ...],
        "properties": ["translation", "exampleSentence", "exampleTranslation", "gender"]
    }
}

Detailed Instructions:

title: Create the lesson title by prepending "Lesson [lesson_number]: " to the name field from the input.

description: Use the description field from the input directly.

sections:

Create an "Introduction" section with a generic welcome message in the about field. This section should have empty components and elements arrays.

Based on the goals array in the input, create between 4 and 6 additional sections. Each section should have:

title: A descriptive title for the section.

about: A brief explanation of the section's content.

components: An array of strings representing relevant components (see "Components" below). Choose components that are appropriate for the section's content.

elements: An array of strings representing interactive elements (see "Elements" below).

vocabulary: This is the most crucial part. There is only one vocabulary object in the lesson. The vocabulary must be an object with exactly two keys:

words: An array of strings. These strings should be the vocabulary words themselves (e.g., "hola", "adiós"). Do not create objects for each word. Just list the words as strings.

properties: An array of strings representing the names of the properties that will be associated with each word in a separate data structure (which is not part of this JSON output). This array should always be: ["translation", "exampleSentence", "exampleTranslation", "gender"]. Do not include the actual translations, example sentences, etc., in this JSON.

Components:

Use the following components where appropriate within the sections:

TextToSpeechPlayer: For audio examples.
TipBox: For important notes or tips.
Mnemonic: For memory aids.
VoiceRecorder: For pronunciation practice.
SentenceBreakdown: For analyzing complex sentences.
HighlightableText: To highlight key terms.
WordBuilder: For vocabulary practice (unscrambling letters).

Elements:

Use the following elements where appropriate within the sections:

table
list

Strict Rules:

1. The output MUST be valid, well-formatted JSON.
2. The vocabulary.words array MUST contain only strings (the words themselves), NOT objects.
3. The vocabulary.properties must be exactly ["translation", "exampleSentence", "exampleTranslation", "gender"]
4. Adhere to all structural requirements outlined above.

Now, using the following input, generate the corresponding JSON lesson:

{input_json}
"""

# Audio text generation prompt template with examples
AUDIO_TEXT_GENERATION_PROMPT = """You are going to generate a json string, this is going to have two properties, text and audio_file_name.
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

The output should be the following:

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
Do not format the output with ```markdown, ```mdx or anything like that."""

# System message for vocabulary generation
VOCABULARY_SYSTEM_MESSAGE = """You are a great educator and know very well how to teach in easy steps. 
You know very well how to output format in MDX. 
The output you are generating is in English."""

# Vocabulary generation prompt template with example
# MDX elements instructions
ELEMENTS_INSTRUCTIONS = """
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

# Content instruction template
CONTENT_INSTRUCTION = """Generate the section content based on the prompt: {prompt}. Ensure the content is instructional and engaging. The content should be directly relevant to the lesson subject and formatted in MDX."""

# Additional content generation instructions
CONTENT_ADDITIONAL_INSTRUCTIONS = """\n\nNote: Remember to provide only the generated content in MDX format without unnecessary explanations or meta-commentary.
Examples are very important to help students understand concepts. When you see pertinent the use of examples, use clear, concise examples to explain the key points and most importanly USE MANY examples, MORE THAN 6, THIS IS VERY IMPORTANT, USE MORE THAN 6 examples ALWAYS.
Generate the content and only the content in an MDX format. 
Do not include text about what you did, your thought process or any other messages, just the generated content in MDX format. 
Also omit the title of the lesson and the title of the section, just provide the content. 
Do not format the output with ```markdown, ```mdx or anything like that."""

VOCABULARY_GENERATION_PROMPT = """You are going to generate vocabulary for the lesson with the title {lesson_title},
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
Also omit the title of the lesson and the title of the section."""
