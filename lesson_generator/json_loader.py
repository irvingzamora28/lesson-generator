import json
from lesson_generator.schema_validator import validate_schema
from lesson_generator.log import logger
from lesson_generator.error_handling import LessonGenerationError

def load_json_file(file_path):
    """Load and return the content of a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def process_json_file(file_path):
    try:
        data = load_json_file(file_path)
        validate_schema(data)
        print(f"JSON file '{file_path}' is valid.")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in file {file_path}: {e}")
        raise LessonGenerationError(f"Invalid JSON format: {e}")
    except Exception as e:
        logger.error(f"Validation error in file {file_path}: {e}")
        raise LessonGenerationError(f"Validation error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python json_loader.py <path_to_json_file>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    process_json_file(json_file_path)
