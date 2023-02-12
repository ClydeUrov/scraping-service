import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('get_work', 'get_rabota', 'get_dou', 'get_djinni')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:1.9.1.5) Gecko/20091102 Firefox/53.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]


def get_work(url):
    jobs = []
    errors = []
    domain = 'https://www.work.ua'
    url = 'https://www.work.ua/ru/jobs-kyiv-python/'
    response = requests.get(url, headers=headers[randint(0, 2)])
    if response.status_code == 200:
        soup = BS(response.content, 'html.parser')
        main_div = soup.find('div', id='pjax-job-list')
        if main_div:
            div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
            for div in div_lst:
                title = div.find('h2')
                href = title.a['href']
                content = div.p.text
                company = 'No name'
                logo = div.find('img')
                if logo:
                    company = logo['alt']
                jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': 'Div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


def get_rabota(url):
    jobs = []
    errors = []
    domain = "https://rabota.ua"
    response = requests.get(url, headers=headers[randint(0, 2)])
    if response.status_code == 200:
        if response.json()['total']:
            vacancies = response.json()['documents']
            for vacancy in vacancies:
                title = vacancy['name']
                href = 'https://rabota.ua/ua/company{}/vacancy{}'.format(vacancy['notebookId'], vacancy['id'])
                content = vacancy['shortDescription']
                company = vacancy['companyName']
                jobs.append({'title': title, 'url': href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': 'Request is empty'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


def get_dou(url):
    jobs = []
    errors = []
    response = requests.get(url, headers=headers[randint(0, 2)])
    if response.status_code == 200:
        soup = BS(response.content, 'html.parser')
        main_div = soup.find('div', id='vacancyListId')
        if main_div:
            li_lst = main_div.find_all('li', attrs={'class': 'l-vacancy'})
            for li in li_lst:
                div = li.find('div', attrs={'class': 'title'})
                title = div.find('a', attrs={'class': 'vt'})
                href = div.a['href']
                content = li.find('div', attrs={'class': 'sh-info'})
                company = 'No name'
                a = div.find('a', attrs={'class': 'company'})
                if a:
                    company = a.text
                jobs.append({'title': title.text, 'url': href, 'description': content.text, 'company': company})
        else:
            errors.append({'url': url, 'title': 'Div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


def get_djinni(url):
    jobs = []
    errors = []
    response = requests.get(url, headers=headers[randint(0, 2)])
    domain = 'https://djinni.co'
    if response.status_code == 200:
        soup = BS(response.content, 'html.parser')
        main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
        if main_ul:
            li_lst = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
            for li in li_lst:
                title = li.find('div', attrs={'class': 'list-jobs__title'})
                href = title.a['href']
                content = li.find('div', attrs={'class': 'truncated'})
                company = 'No name'
                comp = li.find('div', attrs={'class': 'list-jobs__details__info'})
                if comp:
                    company = comp.text
                jobs.append({'title': title.text, 'url': domain + href,
                             'description': content.text, 'company': company})
        else:
            errors.append({'url': url, 'title': 'Div does not exists'})
    else:
        errors.append({'url': url, 'title': 'Page do not response'})
    return jobs, errors


if __name__ == '__main__':
    url = 'https://djinni.co/jobs/?primary_keyword=Python'
    jobs, errors = get_djinni(url)
    h = codecs.open('../work.txt', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()