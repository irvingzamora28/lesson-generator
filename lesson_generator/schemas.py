LESSON_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "sections": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "about": {"type": "string"},
                        "components": {"type": "array", "items": {"type": "string"}},
                        "elements": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["title", "about", "components", "elements"],
                },
            },
            "vocabulary": {
                "type": "object",
                "properties": {
                    "words": {"type": "array", "items": {"type": "string"}},
                    "properties": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["words", "properties"],
            },
        },
        "required": ["title", "description", "sections"],
    },
}
