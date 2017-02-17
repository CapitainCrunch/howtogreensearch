from telegram.ext import Updater, CommandHandler, RegexHandler, MessageHandler, Filters, ConversationHandler
from config import ALLTESTS, KIT
import logging
import sys
import os
import re
import redis
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


def start(bot, update):
    uid = update.message.from_user.id
    bot.sendMessage(uid, 'Ку-ку :)')



def search(bot, update):
    uid = update.message.from_user.id
    message = update.message.text.strip().lower()
    word = morph.parse(message)[0].normal_form
    r = redis.StrictRedis()
    d = dict()
    count = r.llen(word)
    if count == 0:
        bot.sendMessage(uid, 'Такого нет что-то :(')
    else:
        res = list(r.lrange(word, 0, count))
        for a in res:
            url, article = a.decode('utf8').strip('\'()').split('\', \'')
            num = re.findall('posts/(\d+)', url)[0]
            d[int(num)] = ((url, article))
    msg = ''
    for k, v in sorted(d.items(), key=lambda x: x[0], reverse=True)[:20]:
        msg += '{}\n{}\n--------\n'.format(v[0], v[1])
    bot.sendMessage(uid, msg, disable_web_page_preview=True)




if __name__ == '__main__':
    updater = None
    token = None
    if len(sys.argv) > 1:
        token = sys.argv[-1]
        if token.lower() == 'kit':
            updater = Updater(KIT)
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            logging.basicConfig(filename=BASE_DIR + '/out.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    else:
        updater = Updater(ALLTESTS)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, search))
    updater.start_polling()
    updater.idle()