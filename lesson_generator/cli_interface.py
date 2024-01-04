import questionary
import os

def is_valid_file_path(file_path):
    return os.path.isfile(file_path) or 'Please enter a valid file path.'

def is_valid_directory(val):
    return os.path.isdir(val) or 'Please enter a valid directory.'

questions = [
    {
        'type': 'list',
        'name': 'action',
        'message': 'What do you want to do?',
        'choices': [
            'Generate lessons',
            'Exit'
        ]
    },
    {
        'type': 'input',
        'name': 'file_path',
        'message': 'Enter the JSON file path:',
        'when': lambda answers: answers['action'] == 'Generate lessons',
        'validate': is_valid_file_path
    },
    {
        'type': 'input',
        'name': 'output_directory',
        'message': 'Enter the directory where you want the lessons to be saved:',
        'when': lambda answers: answers['action'] == 'Generate lessons',
        'validate': is_valid_directory,
        'default': lambda _: './output'
    }
]

def main(generate_lessons_func):
    answers = questionary.prompt(questions)
    
    if answers['action'] == 'Generate lessons':
        generate_lessons_func(answers['file_path'], answers['output_directory'])
    else:
        print("Exiting...")