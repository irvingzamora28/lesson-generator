from jsonschema import validate
from lesson_generator.schemas import LESSON_SCHEMA

def validate_schema(data):
    """Validate input data against the lesson JSON schema."""
    validate(instance=data, schema=LESSON_SCHEMA)
    # If no exceptions are raised by validate(), the data conforms to the schema
