import codecs

from scraping.parsers import *

parsers = (
    (get_work, 'https://www.work.ua/ru/jobs-kyiv-python/'),
    (get_dou, 'https://jobs.dou.ua/vacancies/?category=Python'),
    (get_rabota, 'https://api.rabota.ua/vacancy/search?keyWords=Python'),
    (get_djinni, 'https://djinni.co/jobs/?primary_keyword=Python')
)

jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()