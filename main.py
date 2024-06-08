import traceback
from time import sleep
from threading import Thread
import ast

import requests
import telebot
from telebot.types import InputMediaPhoto

from config import url, local_db, tg_token, tg_channel
from database import write_to_db, initiate, get_not_sent, update_sent, save_media

text_link = '''Для самостоятельного оформления заказа перейдите по ссылке ниже️'''


def link_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    url = telebot.types.InlineKeyboardButton(text='Сделать заказ', url='https://t.me/helperwishesbot')
    markup.add(url)
    return markup


def get_items(vk_url) -> list:
    try:
        response = requests.get(vk_url)
        src = response.json()
        del response
        item_list = []
        photo_list = []
        posts = src['response']['items']
        for detail in posts:
            # print(detail)
            try:
                post_id = detail['id']
                text = detail['text']
                photo_list = []
                try:
                    attachments = detail['attachments']
                    for i in attachments:
                        if i['type'] == 'photo':
                            photo = i['photo']['sizes'][-1]['url']
                            photo_list.append(photo)
                            # save_media(photo)  # Сохраняем фото на сервер
                except:
                    pass
            except:
                print(traceback.format_exc())
            item_list.append((post_id, text, str(photo_list), 0))
        del photo_list
    except:
        item_list = []
    return item_list


def get_from_vk():
    print("get_items('https://vk.com/....')")
    while True:
        for val in get_items(vk_url=url):
            write_to_db(local_db, val)
        sleep(60)


def send_to_tg():
    bot = telebot.TeleBot(tg_token)
    print(bot)
    while True:
        for i in get_not_sent(local_db):
            try:
                post_id = i[0]
                text = i[1]
                photo_list = ast.literal_eval(i[2])
                is_sent = i[3]
                print(post_id, is_sent)
                # print(len(photo_list))
                if not photo_list:
                    bot.send_message(chat_id=tg_channel, text=text)
                    bot.send_message(chat_id=tg_channel, text=text_link, reply_markup=link_markup())
                    update_sent(local_db, post_id)
                    print('MESSAGE SEND WITHOUT ANY MEDIA')
                elif len(photo_list) == 1:
                    photo = photo_list[0]
                    bot.send_photo(chat_id=tg_channel, caption=text, photo=photo)
                    bot.send_message(chat_id=tg_channel, text=text_link, reply_markup=link_markup())
                    print('MESSAGE SEND WITH PHOTO', photo)
                    update_sent(local_db, post_id)
                else:
                    print(f'[POST ID] [{post_id}]')
                    media = []
                    for photo in photo_list:
                        p = requests.get(photo).status_code
                        print(f'[STATUS] [200] [{photo[:50]}]')
                        if p != 200:
                            try:
                                photo_list.remove(photo)
                                print(f'[REMOVED] [{photo[:50]}]')
                            except:
                                pass
                    for photo in photo_list:
                        if not media:
                            media.append(InputMediaPhoto(media=photo, caption=text))
                        else:
                            media.append(InputMediaPhoto(media=photo))

                    bot.send_media_group(chat_id=tg_channel, media=media)
                    bot.send_message(chat_id=tg_channel, text=text_link, reply_markup=link_markup())
                    print(f'[MESSAGE SEND WITH MEDIA_GROUP] [{media}]')
                    update_sent(local_db, post_id)
            except Exception as e:
                print(e)
            sleep(6.5)
        sleep(30)


if __name__ == '__main__':
    # initiate(local_db)

    t1 = Thread(target=get_from_vk)
    t2 = Thread(target=send_to_tg)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
