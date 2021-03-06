from datetime import datetime
from os import mkdir

LOWERCASE_TITLE_WORDS = {'A', 'An', 'The', 'In', 'Of', 'To', 'With', 'And', 'For'}

def hyphen_case(text):
    ILLEGAL_CHARS = {' ': '-', '/': '-', '&': 'and', '_': ''}
    text = text.lower()
    for char in ILLEGAL_CHARS:
        text = text.replace(char, ILLEGAL_CHARS[char])
    return text

def snake_case(text):
    return hyphen_case(text).replace('-', '_')

def read(file):
    with open(file, 'r') as file:
        content = file.read()
    return content

def read_if_exists(file):
    try:
        return read(file)
    except FileNotFoundError:
        return ''

def write(file, *args, **kwargs):
    with open(file, 'w') as file:
        file.write(*args, **kwargs)

def pad(num, length):
    text_num = str(num)
    return ''.join(('0' * (length - len(text_num)), text_num))

def render_list(elements, singular=None, plural=None):
    if len(elements) == 1:
        text = elements[0]
    elif len(elements) == 2:
        text = f'{elements[0]} and {elements[1]}'
    else:
        text = '{}, and {}'.format(', '.join(elements[:-1]), elements[-1])
    if singular or plural:
        assert singular and plural, 'Please specify and singular and plural base.'
        text = '{}: {}'.format(singular if len(elements) == 1 else plural, text)
    words = text.split(' ')
    for i in range(1, len(words)):
        word = words[i]
        if word in LOWERCASE_TITLE_WORDS:
            words[i] = word.lower()
    return ' '.join(words)

def get_current_week_index(weeks):
    assert weeks
    today, i = datetime.today(), -1
    while i + 1 < len(weeks) and today >= weeks[i + 1].date:
        i += 1
    return i
