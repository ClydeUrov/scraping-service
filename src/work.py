import requests
import codecs
from bs4 import BeautifulSoup as BS

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

domain = 'https://www.work.ua'
url = 'https://www.work.ua/ru/jobs-kyiv-python/'
response = requests.get(url, headers=headers)
jobs = []
errors = []
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
    a = 1

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()