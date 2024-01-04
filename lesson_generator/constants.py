from dotenv import dotenv_values

config = dotenv_values(".env")

# Provide default value if key not defined
OPENAI_API_KEY = config.get('OPENAI_API_KEY', '')  

