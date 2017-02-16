import redis
import re
import requests
from multiprocessing import Pool
import pymorphy2

base_url = 'http://howtogreen.ru'


def get_main_themes():
    resp = requests.get(base_url).content.decode('utf8')
    main_themes = re.findall('<a class="main-nav__link" href="(.*?)"><div><span>', resp)
    return main_themes

def collect_recipies(theme_url):
    for p in range(1000):
        pass
    resp = requests.get(theme_url+'?page=1').content.decode('utf8')
    recipies = re.findall('<a class="pub-item__heading-link" href="(.*?)">(.*?)</a>', resp)
    print(recipies)


def parse_recipe(url):
    pass

for theme in get_main_themes():
    collect_recipies(base_url+theme)
    break

# morph = pymorphy2.MorphAnalyzer()
# print(morph.parse('бабушке')[0].normal_form)