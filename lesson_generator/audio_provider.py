from abc import ABC, abstractmethod
import base64
import json
import os
import subprocess
import requests


class AIAudioProvider(ABC):
    """Base class for AI audio providers"""
    
    @abstractmethod
    def generate_audio(self, text: str, output_path: str, language_code: str = "es-US") -> bool:
        """Generate audio file from text

        Args:
            text (str): Text to convert to speech
            output_path (str): Path to save the audio file
            language_code (str, optional): Language code. Defaults to "es-US".

        Returns:
            bool: True if successful, False otherwise
        """
        pass

    def generate_audio_from_json(self, json_file_path: str, output_directory: str, language_code: str = "es-US") -> bool:
        """Generate audio files from a JSON file containing text and audio file names

        Args:
            json_file_path (str): Path to the JSON file
            output_directory (str): Directory to save the audio files
            language_code (str, optional): Language code. Defaults to "es-US".

        Returns:
            bool: True if all files were generated successfully, False otherwise
        """
        try:
            with open(json_file_path, 'r') as f:
                data = json.load(f)

            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            success = True
            for item in data.get('data', []):
                text = item.get('text')
                audio_file_name = item.get('audio_file_name')
                
                if not text or not audio_file_name:
                    print(f"Skipping invalid item: {item}")
                    success = False
                    continue

                output_path = os.path.join(output_directory, audio_file_name)
                if not self.generate_audio(text, output_path, language_code):
                    success = False

            return success
        except Exception as e:
            print(f"Error generating audio files: {str(e)}")
            return False


class GoogleTextToSpeech(AIAudioProvider):
    """Google Cloud Text-to-Speech implementation"""

    def __init__(self, voice_name: str = "es-US-Neural2-A", speaking_rate: float = 0.95):
        self.voice_name = voice_name
        self.speaking_rate = speaking_rate

    def _get_gcloud_token(self) -> tuple[str, str]:
        """Get access token and project ID using gcloud CLI"""
        try:
            # Get project ID
            project_cmd = "gcloud config list --format='value(core.project)'"
            project_id = subprocess.check_output(project_cmd, shell=True).decode().strip()
            
            # Get access token
            token_cmd = "gcloud auth print-access-token"
            token = subprocess.check_output(token_cmd, shell=True).decode().strip()
            
            return token, project_id
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to get Google Cloud credentials: {str(e)}. Make sure gcloud CLI is installed and you're logged in.")

    def generate_audio(self, text: str, output_path: str, language_code: str = "es-US") -> bool:
        try:
            # Get credentials using gcloud CLI
            token, project_id = self._get_gcloud_token()

            url = "https://texttospeech.googleapis.com/v1/text:synthesize"
            headers = {
                "Content-Type": "application/json",
                "X-Goog-User-Project": project_id,
                "Authorization": f"Bearer {token}"
            }
            # Best voice 
            # es-US-Journey-F
            
            data = {
                "input": {"text": text},
                "voice": {
                    "languageCode": language_code,
                    "name": self.voice_name,
                    "ssmlGender": "FEMALE"
                },
                "audioConfig": {
                    "audioEncoding": "MP3",
                    "pitch": 1,
                    "speakingRate": self.speaking_rate
                }
            }

            print("Request URL:", url)
            print("Request Headers:", headers)
            print("Request Data:", json.dumps(data, indent=2))
            
            response = requests.post(url, headers=headers, json=data)
            
            if not response.ok:
                print("Error Response:", response.text)
                response.raise_for_status()

            # The response contains the audio content in base64
            audio_content = response.json().get("audioContent")
            if not audio_content:
                raise ValueError("No audio content received")

            # Decode the base64 audio content and write to file
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(audio_content))

            return True
        except Exception as e:
            print(f"Error generating audio for text '{text}': {str(e)}")
            return False
