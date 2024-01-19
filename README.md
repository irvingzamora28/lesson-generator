# Lesson_Generator

The Lesson Generator is a Python command-line application that assists content creators and educators in the automated creation of educational lessons. With the use of the OpenAI API, it generates lesson content in MDX format based on a predefined JSON structure. The generated lessons include interactive elements by incorporating specified React components, enriching the learning experience.

## Features

-   Automated lesson content generation in MDX format
-   Integration with OpenAI API for dynamic content creation
-   Support for various educational topics and multiple languages
-   Incorporation of interactive React components like TextToSpeechPlayer, TipBox, and Mnemonic

## Getting Started

### Prerequisites

-   Python environment
-   An OpenAI API key
-   Internet access

### Installation

1. Clone the repository to your local machine.
2. Install necessary Python packages specified in `requirements.txt`.
3. Set up an `.env` file with your OpenAI API key.

## Usage

To use the Lesson Generator, start the command-line interface which will prompt you for the necessary parameters using the Questionary library:

```bash
python -m lesson_generator.cli
```

Upon running the command, you will be asked to:

1. Choose the action you want to perform (e.g., "Generate lessons").
2. Enter the JSON file path for the lesson structure. A default value is provided which you can use or replace.
3. Specify the directory where you want the lessons to be saved. A default output directory is provided, but you can change it as needed.

### JSON Input Structure

The input JSON structure should follow the schema defined in `lesson_generator/schemas.py`. An example of a valid JSON input can be found in `tests/valid_input.json`.

## Development

### Key Files & Directories

-   `lesson_generator/`: Core application modules.
-   `tests/`: Contains JSON files for testing input validation.
-   `i18n/`: Translation files for internationalization support.

### Technologies Used

-   Python
-   MDX
-   jsonschema
-   requests
-   python-i18n
-   questionary

## Contributing

If you'd like to contribute to the Lesson Generator project, please feel free to make a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

-   This project makes use of the OpenAI API to provide valuable educational content.
-   The use of MDX allows for the integration of React components within markdown content.

## Contact

For any questions or suggestions, please reach out to the repository owner.

**Note:** This project is in active development and features may be subject to change.
