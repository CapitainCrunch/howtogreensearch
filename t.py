__author__ = 'evstrat'
__email__ = 'evstrat.bg@gmail.com'

import re
import requests


url = 'http://howtogreen.ru/posts/1298-pancake'

regex = re.compile('<div class="b-recipe__body">.*?</div>', re.M | re.I)

page = requests.get(url).content.decode('utf8')

regex_words = re.compile('[а-яё]+', re.M | re.I)

print(regex_words.findall(regex.findall(page)[0]))
