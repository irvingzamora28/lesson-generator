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
-   Google Cloud account and project
-   Internet access

### Installation

1. Clone the repository to your local machine.
2. Install necessary Python packages specified in `requirements.txt`.
3. Set up an `.env` file with your OpenAI API key.
4. Set up Google Cloud Text-to-Speech (see below).

### Google Cloud Text-to-Speech Setup

To use the Google Cloud Text-to-Speech functionality, follow these steps:

1. Install the Google Cloud SDK:
   ```bash
   # Download the SDK
   curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-454.0.0-linux-x86_64.tar.gz
   
   # Extract the archive
   tar -xf google-cloud-sdk-454.0.0-linux-x86_64.tar.gz
   
   # Run the installer
   ./google-cloud-sdk/install.sh
   ```

2. Initialize the Google Cloud SDK:
   ```bash
   gcloud init
   ```
   This will:
   - Open a browser window for you to log in to your Google account
   - Let you select or create a Google Cloud project
   - Set up your default project

3. Set up application default credentials:
   ```bash
   # Login and set up credentials
   gcloud auth application-default login
   
   # Set the quota project (replace with your project ID)
   gcloud auth application-default set-quota-project YOUR_PROJECT_ID
   ```

4. Enable the Text-to-Speech API:
   ```bash
   gcloud services enable texttospeech.googleapis.com
   ```

#### Troubleshooting Google Cloud Setup

1. If you get a "quota project not set" error:
   ```bash
   gcloud auth application-default set-quota-project YOUR_PROJECT_ID
   ```

2. If you get a "service not enabled" error:
   ```bash
   gcloud services enable texttospeech.googleapis.com
   ```

3. To verify your setup:
   ```bash
   # Check if you're properly authenticated
   gcloud auth list
   
   # Check your current project
   gcloud config list project
   
   # Test the Text-to-Speech API
   curl -X GET \
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     -H "Content-Type: application/json" \
     "https://texttospeech.googleapis.com/v1/voices"
   ```

#### Notes

- The Google Cloud SDK installation files are added to `.gitignore` to prevent them from being committed
- The authentication credentials are stored in `~/.config/gcloud/`
- Make sure your Google Cloud project has billing enabled to use the Text-to-Speech API

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
