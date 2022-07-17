from collections import Counter

import requests
import requests.utils as utils
import re


def wiki_request_sender(input_url: str):
    response = requests.get(input_url, allow_redirects=True, timeout=1)
    encodings = utils.get_encoding_from_headers(response.headers)
    content = response.content.decode(encoding=encodings)
    return content


def wiki_page_cutter(input_content: str, first_call=True):
    result = {_: [] for _ in ['animals_html', 'page_switcher_html', 'pages_count', 'stop']}
    cut = input_content.split('<h2>Страницы в категории «Животные по алфавиту»</h2>')[1].split('ul>')[:-4]
    for i, slice in enumerate(cut):
        if slice.find('Следующая страница') > 0 and len(result['page_switcher_html']) == 0:
            result['page_switcher_html'].append(slice)
            if first_call:
                pages_count = int(re.search(r'Показано 200 страниц из (.+),', slice)[1].replace("&#160;", "")) / 200
                result['pages_count'].append(int(pages_count))
        if re.search(r'<h3>[а-яА-ЯёЁ]</h3>', slice):
            result['animals_html'].append([cut[i + 1]])
        if re.search(r'<h3>[a-zA-Z]</h3>', slice):
            result['stop'].append(True)
    return result


def wiki_next_page_link_re_parser(input_content: str):
    reg_next_page = r'Предыдущая страница[</a>]*\) \(<a href="(\S+)"'
    next_page_link = f'https://ru.wikipedia.org{re.search(reg_next_page, *input_content)[1].replace("&amp;", "&")}'
    return next_page_link


def wiki_animal_re_parser(input_content: list):
    finding_animals = []
    reg_animal = r'title="([а-яА-ЯёЁ\s\-?\(?\)?]{2,})"'
    for el in input_content:
        result = re.findall(reg_animal, *el)
        finding_animals.extend(result)
    return finding_animals


def wiki_animal_validator(input_result: str):
    if bool(re.search('[а-яА-ЯёЁ]', input_result[0])) and \
            not bool(re.search('\wи|\wы|ые|ие', input_result[-2:])) and \
            not bool(re.search('семейство|род|отряд', input_result)):
        return True


if __name__ == '__main__':
    url = 'https://inlnk.ru/jElywR'
    animal_name_list = []
    content = wiki_page_cutter(wiki_request_sender(url))
    for i in range(1, *content['pages_count']):
        print(f'\rПарсинг страницы с помощью re: {i}', end='')
        animal_name_list.extend([*filter(wiki_animal_validator, wiki_animal_re_parser(content['animals_html']))])
        if content['stop']:
            print('\r---Парсинг с помощью re окончен---', end='\n')
            break
        url = wiki_next_page_link_re_parser(content['page_switcher_html'])
        content = wiki_page_cutter(wiki_request_sender(url), first_call=False)
    alphabet_count = sorted(Counter((_[:1] for _ in animal_name_list)).items())
    for letter in alphabet_count:
        print(f'{letter[0]}: {letter[1]}')
