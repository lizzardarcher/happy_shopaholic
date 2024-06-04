import traceback
from time import sleep
from threading import Thread
import ast

import requests
import telebot
from telebot.types import InputMediaPhoto

from config import url, local_db, tg_token, tg_channel
from database import write_to_db, initiate, get_not_sent, update_sent, save_media


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
                except:pass
            except:
                ...
                # print(traceback.format_exc())
            item_list.append((post_id, text, str(photo_list), 'False'))
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
                # print(len(photo_list))
                if not photo_list:
                    bot.send_message(chat_id=tg_channel, text=text)
                    update_sent(local_db, post_id)
                    print('Message sent with no photo')

                elif len(photo_list) == 1:
                    photo = photo_list[0]
                    bot.send_photo(chat_id=tg_channel, caption=text, photo=photo)
                    print('Message sent with', photo)
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
                            except:pass
                    for photo in photo_list:
                        if not media:
                            media.append(InputMediaPhoto(media=photo, caption=text))
                        else:
                            media.append(InputMediaPhoto(media=photo))

                    bot.send_media_group(chat_id=tg_channel, media=media)
                    update_sent(local_db, post_id)


                # elif len(photo_list) > 1:
                #     if len(photo_list) == 2:
                #         bot.send_media_group(chat_id=tg_channel,
                #                              media=[InputMediaPhoto(media=photo_list[0], caption=text),
                #                                     InputMediaPhoto(media=photo_list[1]),
                #                                     ]
                #                              )
                #     elif len(photo_list) == 3:
                #         bot.send_media_group(chat_id=tg_channel,
                #                              media=[InputMediaPhoto(media=photo_list[0], caption=text),
                #                                     InputMediaPhoto(media=photo_list[1]),
                #                                     InputMediaPhoto(media=photo_list[2]),
                #                                     ]
                #                              )
                #     elif len(photo_list) == 4:
                #         bot.send_media_group(chat_id=tg_channel,
                #                              media=[InputMediaPhoto(media=photo_list[0], caption=text),
                #                                     InputMediaPhoto(media=photo_list[1]),
                #                                     InputMediaPhoto(media=photo_list[2]),
                #                                     InputMediaPhoto(media=photo_list[3]),
                #                                     ]
                #                              )
                #     elif len(photo_list) == 5:
                #         bot.send_media_group(chat_id=tg_channel,
                #                              media=[InputMediaPhoto(media=photo_list[0], caption=text),
                #                                     InputMediaPhoto(media=photo_list[1]),
                #                                     InputMediaPhoto(media=photo_list[2]),
                #                                     InputMediaPhoto(media=photo_list[3]),
                #                                     InputMediaPhoto(media=photo_list[4]),
                #                                     ]
                #                              )
                #     elif len(photo_list) == 6:
                #         bot.send_media_group(chat_id=tg_channel,
                #                              media=[InputMediaPhoto(media=photo_list[0], caption=text),
                #                                     InputMediaPhoto(media=photo_list[1]),
                #                                     InputMediaPhoto(media=photo_list[2]),
                #                                     InputMediaPhoto(media=photo_list[3]),
                #                                     InputMediaPhoto(media=photo_list[4]),
                #                                     InputMediaPhoto(media=photo_list[5]),
                #                                     ]
                #                              )
                #     elif len(photo_list) == 7:
                #         bot.send_media_group(chat_id=tg_channel,
                #                              media=[InputMediaPhoto(media=photo_list[0], caption=text),
                #                                     InputMediaPhoto(media=photo_list[1]),
                #                                     InputMediaPhoto(media=photo_list[2]),
                #                                     InputMediaPhoto(media=photo_list[3]),
                #                                     InputMediaPhoto(media=photo_list[4]),
                #                                     InputMediaPhoto(media=photo_list[5]),
                #                                     InputMediaPhoto(media=photo_list[6]),
                #                                     ]
                #                              )
                #     elif len(photo_list) == 8:
                #         bot.send_media_group(chat_id=tg_channel,
                #                              media=[InputMediaPhoto(media=photo_list[0], caption=text),
                #                                     InputMediaPhoto(media=photo_list[1]),
                #                                     InputMediaPhoto(media=photo_list[2]),
                #                                     InputMediaPhoto(media=photo_list[3]),
                #                                     InputMediaPhoto(media=photo_list[4]),
                #                                     InputMediaPhoto(media=photo_list[5]),
                #                                     InputMediaPhoto(media=photo_list[6]),
                #                                     InputMediaPhoto(media=photo_list[7]),
                #                                     ]
                #                              )
                #     elif len(photo_list) == 9:
                #         bot.send_media_group(chat_id=tg_channel,
                #                              media=[InputMediaPhoto(media=photo_list[0], caption=text),
                #                                     InputMediaPhoto(media=photo_list[1]),
                #                                     InputMediaPhoto(media=photo_list[2]),
                #                                     InputMediaPhoto(media=photo_list[3]),
                #                                     InputMediaPhoto(media=photo_list[4]),
                #                                     InputMediaPhoto(media=photo_list[5]),
                #                                     InputMediaPhoto(media=photo_list[6]),
                #                                     InputMediaPhoto(media=photo_list[7]),
                #                                     InputMediaPhoto(media=photo_list[8]),
                #                                     ]
                #                              )
                #     elif len(photo_list) == 10:
                #         bot.send_media_group(chat_id=tg_channel,
                #                              media=[InputMediaPhoto(media=photo_list[0], caption=text),
                #                                     InputMediaPhoto(media=photo_list[1]),
                #                                     InputMediaPhoto(media=photo_list[2]),
                #                                     InputMediaPhoto(media=photo_list[3]),
                #                                     InputMediaPhoto(media=photo_list[4]),
                #                                     InputMediaPhoto(media=photo_list[5]),
                #                                     InputMediaPhoto(media=photo_list[6]),
                #                                     InputMediaPhoto(media=photo_list[7]),
                #                                     InputMediaPhoto(media=photo_list[8]),
                #                                     InputMediaPhoto(media=photo_list[9]),
                #                                     ]
                #                              )
                #     update_sent(local_db, post_id)
            except Exception as e:
                ...
                print(e)
            sleep(5)
        sleep(5)


if __name__ == '__main__':
    initiate(local_db)

    t1 = Thread(target=get_from_vk)
    t2 = Thread(target=send_to_tg)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
