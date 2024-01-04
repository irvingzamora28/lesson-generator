import sys
import os
import json
from lesson_generator.i18n_setup import setup_i18n
from lesson_generator.openai_api import generate_content
from lesson_generator.json_loader import process_json_file
from lesson_generator.embed_components import embed_components_in_sections
from lesson_generator.log import logger
from lesson_generator.error_handling import LessonGenerationError



def generate_lessons(json_file_path, output_directory):
    try:
        language = 'en'
        setup_i18n(language)
        lessons_data = process_json_file(json_file_path)
        for lesson in lessons_data:
            print(f"Generating content for lesson: {lesson['title']}")
            for section in lesson['sections']:
                try:
                    prompt = section['content']
                    generated_content = generate_content(prompt)
                    section['generated_content'] = generated_content
                    print(f"Generated section: {section['title']}")
                    print(f"Generated content: {section['generated_content']}")
                except Exception as e:
                    print(f"Error generating content for section: {section['title']}. Error: {e}")
        lessons_data_with_components = embed_components_in_sections(lessons_data)
        save_to_directory(lessons_data_with_components, output_directory)
    except LessonGenerationError as e:
        logger.error(f"Lesson generation failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)
    logger.info("Lesson generation task completed.")

def save_to_directory(lessons_data_with_components, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for lesson in lessons_data_with_components:
        from lesson_generator.mdx_converter import save_mdx_file
        save_mdx_file(lesson, output_directory)

def main():
    from lesson_generator.cli_interface import main as cli_interface_main
    cli_interface_main(generate_lessons)

if __name__ == "__main__":
    main()
