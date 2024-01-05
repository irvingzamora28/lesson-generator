import os
import json


def generate_transformed_data(lesson_data):
    transformed_data = {
        "language_code": "es",
        "country_code": "MX",
        "lesson_number": 5,
        "voice_id": "63b4083d241a82001d51c30a",
        "data": [],
    }

    for section in lesson_data["sections"]:
        if "generated_json_audio_text" in section:
            # Ensure that section["generated_json_audio_text"] is treated as a dictionary.
            section_audio_text = section["generated_json_audio_text"]
            if isinstance(section_audio_text, str):
                # If the section data is a string, it's likely JSON-encoded.
                # Decode it back to a dictionary before appending.
                section_audio_text = json.loads(section_audio_text)
            transformed_data["data"].append(section_audio_text)

    return transformed_data


def save_json_file(lesson_data, output_directory):
    lesson_title_sanitized = (
        lesson_data["title"].replace(" ", "_").replace("/", "_").lower()
    )
    file_path = os.path.join(output_directory, f"{lesson_title_sanitized}.json")

    lesson_data = generate_transformed_data(lesson_data)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(lesson_data, file, indent=4, ensure_ascii=False)
