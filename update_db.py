import redis
import re
import requests
from threading import Thread
import threading
import pymorphy2
from queue import Queue
from nltk.corpus import stopwords

r = redis.StrictRedis()
base_url = 'http://howtogreen.ru'
_stopwords = set(stopwords.words('russian'))
regex = re.compile('[а-яё]+', re.M | re.I)
morph = pymorphy2.MorphAnalyzer()

q = Queue(2000)
to_redis = Queue(1000000)


def get_main_themes():
    resp = requests.get(base_url).content.decode('utf8')
    main_themes = re.findall('<a class="main-nav__link" href="(.*?)"><div><span>', resp)
    return main_themes


def collect_recipies(theme_url):
    for p in range(1, 1000):
        resp = requests.get(theme_url+'?page=' + str(p)).content.decode('utf8')
        recipies = re.findall('<a class="pub-item__heading-link" href="(.*?)">(.*?)</a>', resp)
        if len(recipies) > 0:
            for recipie in recipies:
                q.put(recipie)
        else:
            break


def parse_recipe_and_save():
    while True:
        if not q.empty():
            url, article_name = q.get()
            url = base_url + url
            req = requests.get(url).content.decode('utf8')
            words = regex.findall(req)
            clean_words = set(map(lambda x: x.lower(), words)) - set(_stopwords)
            normal_words = set(map(lambda x: morph.parse(x)[0].normal_form, clean_words))
            for w in normal_words:
                r.lpush(w, (url, article_name))
        elif q.empty():
            for thread in threading.enumerate():
                if thread.name.startswith('/') and not thread.is_alive():
                    break



for theme in get_main_themes():
    url = base_url + theme
    t = Thread(target=collect_recipies, name=theme, args=(url,))
    t.start()

for i in range(10):
    print(threading.enumerate())
    Thread(target=parse_recipe_and_save, name='parse and save ' + str(i)).start()

