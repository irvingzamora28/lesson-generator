from i18n import config, load_path
import os

def setup_i18n(language='en'):
    # Set i18n configuration
    config.set('domain', 'lesson_content')
    config.set('locale', language)
    config.set('fallback', 'en')
    config.set('skip_locale_root_data', True)
    config.set('filename_format', '{locale}.{format}')
    
    # Set the correct path to the translation files; it might depend on the run context
    base_path = os.path.dirname(os.path.realpath(__file__))
    translations_path = os.path.abspath(os.path.join(base_path, '..', 'i18n'))
    
    if translations_path not in load_path:
        load_path.append(translations_path)

# INPUT_REQUIRED: Ensure that the i18n directory exists and contains the translation files.
