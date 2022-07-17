from collections import Counter

import requests
from bs4 import BeautifulSoup


def wiki_animals_parser(input_url: str):
    """Вернуть ссылку на следующую страницу, список животных на странице, маркер остановки парсинга -> dict"""
    response = requests.get(input_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    _animals = []
    stop = False
    for a in soup.find_all('a'):
        if a.get_text() == 'Следующая страница':
            next_page = f'https://ru.wikipedia.org{a.get("href")}'
        a_text = a.get_text()
        if a.get('title') == a_text:
            if a_text.startswith('A') or a_text.startswith('a'):
                stop = True
                break
            _animals.append(a_text)
    return {'next_page': next_page, 'animals': _animals, 'stop': stop}


def wiki_animals_cleaner(input_animals: list):
    """Вернуть список животных, очищенный от невалидных значений -> list"""
    clean_list_animal = []
    taxons = ['род', 'семейство', 'отряд']
    endings_1 = ['ы', 'и']
    endings_2 = ['ые', 'ие', 'ый', 'ой', 'ий', 'ая', 'ое']
    en_alphabet = 'AaEeIiOoUuBbCcDdFfGgHhJjKkLlMmNnPpQqRrSsTtVvWwXxYyZz()'
    for animal in input_animals:
        if len(set(animal) & set(taxons)) > 0 or len(set(animal) & set(en_alphabet)) > 0 \
                or len(set([animal[-2:]]) & set(endings_2)) > 0 or len(set([animal[-1:]]) & set(endings_1)) > 0:
            continue
        if animal.find(' ') > 0:
            for slice in animal.split():
                if len(set([slice[-2:]]) & set(endings_2)) > 0 or len(set([slice[-1:]]) & set(endings_1)) > 0:
                    continue
                clean_list_animal.append(slice.capitalize())
        else:
            clean_list_animal.append(animal)
    return clean_list_animal


if __name__ == '__main__':
    url = 'https://inlnk.ru/jElywR'
    result_animals = []
    content = wiki_animals_parser(url)
    pages_count = int(40450 / 200)
    for i in range(pages_count):
        print(f'\rПарсинг страницы с помощью BeautifulSoup: {i}', end='')
        result_animals.extend(wiki_animals_cleaner(content['animals']))
        url = content['next_page']
        if content['stop']:
            print('\r---Парсинг с помощью BeautifulSoup окончен---', end='\n')
            break
        content = wiki_animals_parser(url)
    result_unique_animals = [unique_animal for unique_animal in set(result_animals)]
    alphabet_count = sorted(Counter((_[:1] for _ in result_unique_animals)).items())
    for letter in alphabet_count:
        print(f'{letter[0]}: {letter[1]}')
