import sys
import os
import json
from lesson_generator.i18n_setup import setup_i18n
from lesson_generator.api_provider import get_ai_provider
from lesson_generator.json_loader import process_json_file
from lesson_generator.embed_components import embed_components_in_sections
from lesson_generator.log import logger
from lesson_generator.error_handling import LessonGenerationError


def generate_lessons(json_file_path, output_directory, ai_provider_name):
    try:
        language = "en"
        setup_i18n(language)
        lessons_data = process_json_file(json_file_path)
        for lesson in lessons_data:
            lesson_title = lesson["title"]
            vocabulary = lesson["vocabulary"]
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


def main():
    from lesson_generator.cli_interface import main as cli_interface_main

    cli_interface_main(generate_lessons)


if __name__ == "__main__":
    main()
