import os
import datetime


def json_to_mdx(lesson_data):
    """Converts lesson data in JSON format to MDX format."""
    mdx_content = []
    mdx_content.append("---\n")
    mdx_content.append(f"title: {lesson_data['title']}\n")
    mdx_content.append(f"lesson_number: {lesson_data['lesson_number']}\n")
    mdx_content.append(f"description: {lesson_data['description']}\n")
    mdx_content.append(f"date:  {datetime.datetime.now().strftime('%Y-%m-%d')}\n")
    mdx_content.append(f"{lesson_data['generated_vocabulary'].strip('`').strip().lstrip('`').lstrip('mdx').lstrip().rstrip('`')}\n")
    mdx_content.append("---\n\n")

    for section in lesson_data["sections"]:
        mdx_content.append(f"## {section['title']}\n")
        mdx_content.append(f"{section['generated_content']}\n\n")

    return "".join(mdx_content)


def save_mdx_file(lesson_data, output_directory):
    lesson_title_sanitized = (
        lesson_data["title"].replace(" ", "_").replace("/", "_").lower()
    )
    file_path = os.path.join(output_directory, f"{lesson_title_sanitized}.mdx")

    mdx_content = json_to_mdx(lesson_data)
    with open(file_path, "w", encoding="utf-8") as mdx_file:
        mdx_file.write(mdx_content)

    print(f"Lesson saved to MDX file: {file_path}")
