import codecs
import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django
django.setup()

from scraping.parsers import *
from scraping.models import Vacancy, City, Language

parsers = (
    (get_work, 'https://www.work.ua/ru/jobs-kyiv-python/'),
    (get_dou, 'https://jobs.dou.ua/vacancies/?category=Python'),
    (get_rabota, 'https://api.rabota.ua/vacancy/search?keyWords=Python'),
    (get_djinni, 'https://djinni.co/jobs/?primary_keyword=Python')
)

city = City.objects.filter(slug='kiev')
jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e


h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()
