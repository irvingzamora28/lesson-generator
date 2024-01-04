LESSON_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string"
            },
            "description": {
                "type": "string"
            },
            "sections": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string"
                        },
                        "content": {
                            "type": "string"
                        },
                        "components": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["title", "content", "components"]
                }
            },
            "vocabulary": {
                "type": "object",
                "properties": {
                    "words": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    },
                    "properties": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        }
                    }
                },
                "required": ["words", "properties"]
            }
        },
        "required": ["title", "description", "sections"]
    }
}
