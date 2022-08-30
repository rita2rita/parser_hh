import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import csv


def get_page_count(text, items):
    url = f"https://hh.ru/search/vacancy?search_field=name&text={text}&items_on_page={items}"

    user_agent = fake_useragent.UserAgent()

    headers = {
        "User-Agent": user_agent.random,
        'Accept-Encoding': 'identity'
    }

    data = requests.get(url, headers=headers)

    if data.status_code != 200:
        return

    soup = BeautifulSoup(data.text, 'lxml')

    try:
        max_page_count = int(
            soup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find(
                "span").text)
    except Exception:
        max_page_count = 1

    return max_page_count


def get_info_about_one_lob(div):
    link = div.find('a')['href'].split('?')[0]
    vacancy_name = div.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text
    company = div.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).text.split()
    company = " ".join(company)
    city = div.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text.split(',')[0]

    info_about_job = [vacancy_name, company, city, link]

    return info_about_job


def get_search_page_soup(page_count, text, items):
    url_page = f"https://hh.ru/search/vacancy?search_field=name&text={text}&items_on_page={items}&page={page_count}"

    user_agent = fake_useragent.UserAgent()

    headers = {
        "User-Agent": user_agent.random,
        'Accept-Encoding': 'identity'
    }

    data = requests.get(url_page, headers=headers)

    soup = BeautifulSoup(data.text, 'lxml')

    time.sleep(1)

    return soup


def save_to_csv(job):
    with open('jobs.csv', 'a') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(job)
    return


def ggg():
    items = 20
    jobs = []
    all_vacancy = 0
    text = 'python+разработчик'
    max_page_count = get_page_count(text, items)

    print(f"Now search: {' '.join(text.split('+'))}")

    for page_count in range(max_page_count):
        soup = get_search_page_soup(page_count, text, items)
        block_of_one_vacancy = soup.find_all('div', {"class": "vacancy-serp-item__layout"})

        for div in block_of_one_vacancy:
            info_about_job = get_info_about_one_lob(div)
            jobs.append(info_about_job)
            all_vacancy += 1

    with open('jobs.csv', 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['Название вакансии', 'Компания', 'Город', 'Ссылка'])

    for i in jobs:
        save_to_csv(i)

    print('Count of jobs = ', all_vacancy)

    return


ggg()
