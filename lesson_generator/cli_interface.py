import questionary
import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def is_valid_file_path(file_path):
    if os.path.isfile(file_path):
        return True
    elif os.path.isfile(os.path.join(ROOT_DIR, file_path)):
        return True
    else:
        return "Please enter a valid file path."


def is_valid_directory(val):
    if os.path.isdir(val):
        return True
    elif os.path.isdir(os.path.join(ROOT_DIR, val)):
        return True
    else:
        return "Please enter a valid directory."


questions = [
    {
        "type": "list",
        "name": "action",
        "message": "What do you want to do?",
        "choices": ["Generate lessons", "Exit"],
    },
    {
        "type": "list",
        "name": "ai_provider",
        "message": "Which AI provider would you like to use?",
        "choices": ["OpenAI", "Gemini"],
        "when": lambda answers: answers["action"] == "Generate lessons",
    },
    {
        "type": "input",
        "name": "file_path",
        "message": "Enter the JSON file path:",
        "when": lambda answers: answers["action"] == "Generate lessons",
        "validate": is_valid_file_path,
        "default": lambda _: "./tests/valid_input.json",
    },
    {
        "type": "input",
        "name": "output_directory",
        "message": "Enter the directory where you want the lessons to be saved:",
        "when": lambda answers: answers["action"] == "Generate lessons",
        "validate": is_valid_directory,
        "default": lambda _: "./sample_output",
    },
]


def main(generate_lessons_func):
    answers = questionary.prompt(questions)

    if answers is None or answers.get("action") == "Exit":
        print("Exiting...")
        return

    if answers.get("action") == "Generate lessons":
        file_path = answers.get("file_path")
        output_directory = answers.get("output_directory")
        ai_provider = answers.get("ai_provider").lower()

        # Handle relative paths
        if not os.path.isabs(file_path) and os.path.isfile(os.path.join(ROOT_DIR, file_path)):
            file_path = os.path.join(ROOT_DIR, file_path)
        if not os.path.isabs(output_directory) and os.path.isdir(os.path.join(ROOT_DIR, output_directory)):
            output_directory = os.path.join(ROOT_DIR, output_directory)

        generate_lessons_func(file_path, output_directory, ai_provider)
