import sys
import os
import json
from lesson_generator.i18n_setup import setup_i18n
from lesson_generator.api_provider import get_ai_provider
from lesson_generator.audio_provider import GoogleTextToSpeech
from lesson_generator.json_loader import process_json_file
from lesson_generator.embed_components import embed_components_in_sections
from lesson_generator.log import logger
from lesson_generator.error_handling import LessonGenerationError
from lesson_generator.prompts import LESSON_SECTIONS_PROMPT


def generate_lessons(json_file_path, output_directory, ai_provider_name):
    try:
        language = "en"
        setup_i18n(language)
        lessons_data = process_json_file(json_file_path)
        for lesson in lessons_data:
            lesson_title = lesson["title"]
            vocabulary = lesson["vocabulary"]
            lesson_number = lesson["lesson_number"]
            # logger.info(f"Generating content for lesson: {lesson['title']}")
            for section in lesson["sections"]:
                section_title = section["title"]
                section_components = section.get("components", [])
                section_elements = section.get("elements", [])
                # logger.info(
                #     f"Generating section: {section_title} with components: {', '.join(section_components)}"
                # )
                try:
                    prompt = section["about"]
                    # Get the AI provider instance
                    ai_provider = get_ai_provider(ai_provider_name)
                    
                    # Generate content using the selected provider
                    generated_content = ai_provider.generate_content(
                        lesson_title,
                        section_title,
                        section_components,
                        section_elements,
                        prompt,
                    )
                    section["generated_content"] = generated_content
                    # logger.info(f"Generated content: {section['generated_content']}")
                    if "TextToSpeechPlayer" in section_components:
                        generated_json_audio_text = ai_provider.generate_json_audio_text(
                            generated_content
                        )
                        section["generated_json_audio_text"] = generated_json_audio_text
                except Exception as e:
                    logger.error(
                        f"Error generating content for section: {section_title}. Error: {e}"
                    )
            # logger.info(f"Generating vocabulary : {vocabulary['words']}")
            generated_vocabulary = ai_provider.generate_vocabulary(
                lesson_title, vocabulary["words"], vocabulary["properties"]
            )
            lesson["generated_vocabulary"] = generated_vocabulary

        save_to_directory(lessons_data, output_directory)
    except LessonGenerationError as e:
        logger.error(f"Lesson generation failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)
    # logger.info("Lesson generation task completed.")


def save_to_directory(lessons_data_with_generated_content, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for lesson in lessons_data_with_generated_content:
        from lesson_generator.mdx_converter import save_mdx_file

        save_mdx_file(lesson, output_directory)

        from lesson_generator.json_processor import save_json_file

        save_json_file(lesson, output_directory)


def generate_lesson_sections(json_file_path, output_directory, ai_provider_name):
    try:
        # Read and parse the input JSON file
        with open(json_file_path, 'r') as f:
            data = json.load(f)

        # Get the AI provider instance
        ai_provider = get_ai_provider(ai_provider_name)

        # Process each level and its lessons
        for level_data in data:
            level = level_data["level"]
            lessons = level_data["lessons"]

            # Create level directory if it doesn't exist
            level_dir = os.path.join(output_directory, level)
            os.makedirs(level_dir, exist_ok=True)

            # Store all lesson sections for this level
            level_sections = []

            # Process each lesson
            for lesson in lessons:
                # Format the lesson data for the prompt
                lesson_json = json.dumps(lesson, indent=2)
                prompt = LESSON_SECTIONS_PROMPT.replace("{input_json}", lesson_json)

                # Generate sections using AI
                response = ai_provider.generate_lesson_sections(prompt)

                try:
                    # Parse the response as JSON
                    lesson_sections = json.loads(response)
                    level_sections.append(lesson_sections)

                    logger.info(f"Generated sections for lesson {lesson['lesson_number']}")

                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse AI response as JSON for lesson {lesson['lesson_number']}: {e}")
                    logger.error(f"Raw response: {response}")
                    continue

            # Save all lesson sections for this level in a single file
            if level_sections:
                output_file = f"{level}_lessons_sections.json"
                output_path = os.path.join(level_dir, output_file)
                
                with open(output_path, 'w', encoding='utf-8') as file:
                    json.dump(level_sections, file, indent=4, ensure_ascii=False)

                logger.info(f"Saved all lesson sections for level {level} in {output_path}")

    except Exception as e:
        raise LessonGenerationError(f"Error generating lesson sections: {str(e)}")


def generate_audio(json_file_path, output_directory, audio_provider_name):
    try:
        if audio_provider_name == 'google':
            audio_provider = GoogleTextToSpeech()
        else:
            raise ValueError(f"Unsupported audio provider: {audio_provider_name}")
        
        success = audio_provider.generate_audio_from_json(json_file_path, output_directory)
        if success:
            logger.info(f"Successfully generated audio files in {output_directory}")
        else:
            logger.error("Some audio files could not be generated")
    except Exception as e:
        logger.error(f"Error generating audio files: {str(e)}")
        raise LessonGenerationError(f"Failed to generate audio files: {str(e)}")


def main():
    from lesson_generator.cli_interface import main as cli_interface_main

    cli_interface_main(generate_lessons, generate_lesson_sections, generate_audio)


if __name__ == "__main__":
    main()
