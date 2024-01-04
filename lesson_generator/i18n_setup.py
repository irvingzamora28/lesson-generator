from i18n import config, load_path

def setup_i18n(language='en'):
    config.set('locale', language)
    config.set('fallback', 'en')
    config.set('skip_locale_root_data', True)
    config.set('filename_format', '{locale}.{format}')
    
    # Load path where translation files are stored
    load_path.append('i18n')
