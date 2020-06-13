'''

1) Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайта
superjob.ru и hh.ru. Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:

    *Наименование вакансии
    *Предлагаемую зарплату (отдельно мин. и отдельно макс.)
    *Ссылку на саму вакансию
    *Сайт откуда собрана вакансия
По своему желанию можно добавить еще работодателя и расположение. Данная структура должна быть одинаковая для вакансий
с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.

!!!В первую очередь делаем сайт hh.ru - его обязательно. sj.ru можно попробовать сделать вторым. Он находится в очень
странном состоянии и возможна некорректная работа.!!!

'''

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re

main_link = 'https://hh.ru/'

# user_vacancy = input(str('Введите название вакансии'))

params = {'L_is_autosearch': 'false',
          'area': '1', 'clusters': 'true',
          'enable_snippets': 'true',
          'text': 'Python программист',
          }

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Accept': '*/*'}

response = requests.get(main_link + 'search/vacancy', params=params, headers=headers)
soup = bs(response.text, 'lxml')

vacancy_block = soup.find('div', {'class': 'vacancy-serp'})

vacancy_list = vacancy_block.findChildren('div', {'class': 'vacancy-serp-item'}, recursive=False)

vacancies = []
# # #
for vac in vacancy_list:
    vacancy_data = {}
    vacancy_link = vac.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
    name = vacancy_link.text
    link = vacancy_link['href']

    if vac.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}):
        zp_all = vac.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
        zp = re.split(r'-', zp_all)
        # print(zp, len(zp))
        zp_val = re.findall(r'\w+.$', zp_all)  # Валюта
        # print(zp_val)
        # print('aaaaaaaaaaaa', re.findall(r'^от', zp[0]))
        if len(zp) > 1:
            zp_min = int(zp[0].replace(u'\xa0', ''))
            zp_max = re.findall(r'^\d*\s\d\d*[\w+$]', zp[1])
            # print(zp_max[0].replace(u'\xa0', ''))
            zp_max = int(zp_max[0].replace(u'\xa0', ''))
            # print(f"zp_min = {zp_min}, zp_max = {zp_max}, {zp_val[0]}")
        elif re.findall(r'^от', zp[0]):
            zp_min = re.findall(r'[^от\s]\w*\s\d*', zp[0])
            zp_min = int(zp_min[0].replace(u'\xa0', ''))
            zp_max = None
            # print(f"zp_min = {zp_min}, zp_max = {zp_max}, {zp_val[0]}")
        elif re.findall(r'^до', zp[0]):
            zp_max = re.findall(r'[^до\s]\w*\s\d*', zp[0])
            zp_max = int(zp_max[0].replace(u'\xa0', ''))
            zp_min = None
        # print(f"zp_min = {zp_min}, zp_max = {zp_max}, {zp_val[0]}")
        # zp_max = vac.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
        # vacancy_data['zp_min'] = zp_min
        # vacancy_data['zp_max'] = zp_max
        # print(vac.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text)
        print(f"zp_min = {zp_min}, zp_max = {zp_max}, {zp_val[0]}")

        vacancy_data['zp_min'] = zp_min
        vacancy_data['zp_max'] = zp_max
        vacancy_data['zp_val'] = zp_val[0]
        vacancies.append(vacancy_data)
    else:
        zp_min = None
        zp_max = None
        zp_val = None
        vacancy_data['zp_min'] = zp_min
        vacancy_data['zp_max'] = zp_max
        vacancy_data['zp_val'] = zp_val
        vacancies.append(vacancy_data)

    vacancy_data['name'] = name
    vacancy_data['from'] = main_link
    vacancy_data['link'] = link

    vacancies.append(vacancy_data)

pprint(vacancies)


# Если есть кнопка продолжить делаем новый запрос на страничку
# <a class="bloko-button HH-Pager-Controls-Next HH-Pager-Control" data-qa="pager-next" data-page="1" rel="nofollow" href="/search/vacancy?L_is_autosearch=false&amp;area=1&amp;clusters=true&amp;enable_snippets=true&amp;text=Python+%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82&amp;page=1">дальше</a>
