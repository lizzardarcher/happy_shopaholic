import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'happy_shopaholic.settings'
django.setup()
import traceback

from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.models import *
import config

#  initialize settings
TOKEN = Bot.objects.get(pk=1).token
SIZE = config.SIZE
greetings = config.greetings

bot = TeleBot(TOKEN)


def start_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("🚀 Начать оформление заказа", callback_data="start"),
    )
    return markup


def request_markup(photo='', size='', amount=0, price='', free_order='', phone_number='', fio=''):
    if photo:
        _photo = '✅'
    else:
        _photo = ''
    if size:
        _size = '✅'
    else:
        _size = ''

    if amount:
        _amount = '✅'
    else:
        _amount = ''

    if price:
        _price = '✅'
    else:
        _price = ''

    if free_order:
        _free_order = '✅'
    else:
        _free_order = ''

    if phone_number:
        _phone_number = '✅'
    else:
        _phone_number = ''

    if fio:
        _fio = '✅'
    else:
        _fio = ''

    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton(f"{_fio} 👤 Имя (то же что в VK) ", callback_data="fio"),
        InlineKeyboardButton(f"{_phone_number} 📱 Номер Телефона ", callback_data="phone_number"),
        InlineKeyboardButton(f"{_photo} 📸 Фото товара ", callback_data="photo"),
        InlineKeyboardButton(f"{_size} 👕 Размер {str(size).upper()}", callback_data="size"),
        InlineKeyboardButton(f"{_amount} 📋 Количество {amount}", callback_data="amount"),
        InlineKeyboardButton(f"{_price} 💲 Цена {price}", callback_data="price"),
        InlineKeyboardButton(f"{_free_order} 🆓    Заказ в свободной форме ", callback_data="free_order"),
        InlineKeyboardButton("Закончить", callback_data="finish"),
    )
    return markup


def confirm_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("Подтвердить ✅ ", callback_data=f"confirm"),
        InlineKeyboardButton("Отказаться ❌", callback_data=f"refuse"),
    )
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private':
        #  Создаем пользователя TG
        User.objects.create(
            user_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name)
        bot.send_photo(message.chat.id,
                       photo=open(greetings, 'rb'),
                       caption='Здравствуйте! Ботик-котик приветствует вас! Здесь вы сможете сделать заказ в сервисе HappyShopaholic',
                       reply_markup=start_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query_handlers(call):
    print(call.data)

    def delete_message(_id):
        try: bot.delete_message(call.message.chat.id, _id)
        except: print(traceback.format_exc())

    def clear_current_user(obj):
        obj.photo = None
        obj.size = None
        obj.amount = 0
        obj.price = None
        obj.free_order = None

    def create_user():
        User.objects.create(
            user_id=call.from_user.id,
            username=call.from_user.username,
            first_name=call.from_user.first_name,
            last_name=call.from_user.last_name)

    admin = AdminSettings.objects.all()

    current_user = User.objects.filter(user_id=call.from_user.id, is_ordered=False).last()
    # print(current_user)

    username = User.objects.filter(user_id=call.from_user.id).last().username
    if not username:
        username = ''
    else:
        username = '@' + username

    first_name = User.objects.filter(user_id=call.from_user.id).last().first_name
    if not first_name: first_name = ''

    last_name = User.objects.filter(user_id=call.from_user.id).last().last_name
    if not last_name: last_name = ''

    fio = User.objects.filter(user_id=call.from_user.id).last().fio
    if not fio: fio = ''

    phone_number = User.objects.filter(user_id=call.from_user.id).last().phone_number
    if not phone_number: phone_number = ''

    photo = User.objects.filter(user_id=call.from_user.id).last().photo

    size = User.objects.filter(user_id=call.from_user.id).last().size
    if not size: size = ''

    amount = User.objects.filter(user_id=call.from_user.id).last().amount
    if not amount: amount = ''

    price = User.objects.filter(user_id=call.from_user.id).last().price
    if not price: price = ''

    free_order = User.objects.filter(user_id=call.from_user.id).last().free_order
    if not free_order: free_order = ''

    if call.message.chat.type == 'private':
        if 'start' in call.data:
            delete_message(call.message.id)

            #  Очищаем транзакцию пользователь-заказ
            try:
                clear_current_user(obj=current_user)
            except:
                create_user()

            bot.send_photo(call.message.chat.id,
                           photo=open(greetings, 'rb'),
                           caption='Для оформления заказа необходимо указать следующие данные:',
                           reply_markup=request_markup())

        elif 'photo' in call.data:
            delete_message(call.message.id)

            def get_photo(message):
                if message.content_type == 'photo':
                    photo = message.photo[-1].file_id

                    #  Сохраняем URL фото в БД
                    current_user.photo = photo
                    current_user.save()

                    bot.send_message(call.message.chat.id, text='Продолжаем оформление ... ',
                                     reply_markup=request_markup(photo=photo, size=size, amount=amount, price=price,
                                                                 free_order=free_order, fio=fio,
                                                                 phone_number=phone_number))
                else:
                    bot.send_message(call.message.chat.id, text='Неверный формат. Попробуйте отправить фото снова.',
                                     reply_markup=request_markup(size=size, amount=amount, price=price,
                                                                 free_order=free_order, fio=fio,
                                                                 phone_number=phone_number))

            msg = bot.send_message(call.message.chat.id, text='Пришлите фото товара (можно скопировать из канала): ')
            bot.register_next_step_handler(msg, get_photo)

        elif 'size' in call.data:
            delete_message(call.message.id)

            def get_size(message):
                if str(message.text).upper().replace(',', '.') in SIZE:
                    size = message.text

                    #  Сохраняем размер в БД
                    current_user.size = size
                    current_user.save()

                    bot.send_message(call.message.chat.id, text='Продолжаем оформление ... ',
                                     reply_markup=request_markup(photo=photo, size=size, amount=amount, price=price,
                                                                 free_order=free_order, fio=fio,
                                                                 phone_number=phone_number))
                else:
                    bot.send_message(call.message.chat.id, text='Неверно указан размер',
                                     reply_markup=request_markup(photo=photo, amount=amount, price=price,
                                                                 free_order=free_order, fio=fio,
                                                                 phone_number=phone_number))

            msg = bot.send_message(call.message.chat.id,
                                   text='Укажите размер️ (Одежда: XS, S, M, L, XL, XXL) (Обувь: 4-16 US): ')
            bot.register_next_step_handler(msg, get_size)

        elif 'amount' in call.data:
            delete_message(call.message.id)

            def get_amount(message):
                try:
                    amount = int(message.text)

                    #  Сохраняем размер в БД
                    current_user.amount = amount
                    current_user.save()

                    bot.send_message(call.message.chat.id, text='Продолжаем оформление ... ',
                                     reply_markup=request_markup(photo=photo, size=size, amount=amount, price=price,
                                                                 free_order=free_order, fio=fio,
                                                                 phone_number=phone_number))
                except:
                    bot.send_message(call.message.chat.id, text='Неверно указано количество. Укажите число...',
                                     reply_markup=request_markup(photo=photo, size=size, price=price,
                                                                 free_order=free_order, fio=fio,
                                                                 phone_number=phone_number))

            msg = bot.send_message(call.message.chat.id, text='Укажите количество товара(цифрой): ')
            bot.register_next_step_handler(msg, get_amount)

        elif 'price' in call.data:
            delete_message(call.message.id)

            def get_price(message):
                price = message.text

                #  Сохраняем цену в БД
                current_user.price = price
                current_user.save()

                bot.send_message(call.message.chat.id, text='Продолжаем оформление ... ',
                                 reply_markup=request_markup(photo=photo, size=size, amount=amount, price=price,
                                                             free_order=free_order, fio=fio, phone_number=phone_number))

            msg = bot.send_message(call.message.chat.id, text='Укажите цену товара: ')
            bot.register_next_step_handler(msg, get_price)

        elif 'fio' in call.data:
            delete_message(call.message.id)

            def get_fio(message):
                fio = message.text

                #  Сохраняем цену в БД
                current_user.fio = fio
                current_user.save()

                bot.send_message(call.message.chat.id, text='Продолжаем оформление ... ',
                                 reply_markup=request_markup(photo=photo, size=size, amount=amount, price=price,
                                                             free_order=free_order, fio=fio, phone_number=phone_number))

            msg = bot.send_message(call.message.chat.id, text='Укажите ФИО: ')
            bot.register_next_step_handler(msg, get_fio)

        elif 'phone_number' in call.data:
            delete_message(call.message.id)

            def get_phone_number(message):
                phone_number = message.text

                #  Сохраняем цену в БД
                current_user.phone_number = phone_number
                current_user.save()

                bot.send_message(call.message.chat.id, text='Продолжаем оформление ... ',
                                 reply_markup=request_markup(photo=photo, size=size, amount=amount, price=price,
                                                             free_order=free_order, fio=fio, phone_number=phone_number))

            msg = bot.send_message(call.message.chat.id, text='Укажите номер телефона: ')
            bot.register_next_step_handler(msg, get_phone_number)

        elif 'free_order' in call.data:
            delete_message(call.message.id)

            def get_free_order(message):
                free_order = message.text

                #  Сохраняем цену в БД
                current_user.free_order = free_order
                current_user.save()

                bot.send_message(call.message.chat.id, text='Продолжаем оформление ... ',
                                 reply_markup=request_markup(photo=photo, size=size, amount=amount, price=price,
                                                             free_order=free_order, fio=fio, phone_number=phone_number))

            msg = bot.send_message(call.message.chat.id, text='Можете указать всё, что вам необходимо: ')
            bot.register_next_step_handler(msg, get_free_order)

        elif 'finish' in call.data:
            delete_message(call.message.id)
            text = f'*** Ваш заказ ***' \
                   f'\nФИО: {str(fio).capitalize()}' \
                   f'\nТелефон: {phone_number}' \
                   f'\nРазмер: {size}' \
                   f'\nКол-во: {amount}' \
                   f'\nЦена: {price}' \
                   f'\nСвоё сообщение: {free_order}' \
                   f'\n******************'
            if photo:
                bot.send_photo(call.message.chat.id,
                               photo=photo,
                               caption=text,
                               reply_markup=confirm_markup())
            else:
                bot.send_message(call.message.chat.id,
                                 text=text,
                                 reply_markup=confirm_markup())

        elif 'confirm' in call.data:
            delete_message(call.message.id)
            if current_user.size and current_user.amount and current_user.fio and current_user.phone_number:
                text = f'*** Новый Заказ ***' \
                       f'\nПользователь: {username} {first_name} {last_name}' \
                       f'\nФИО: {str(fio).capitalize()}' \
                       f'\nТелефон: {phone_number}' \
                       f'\nРазмер: {size}\nКол-во: {amount}' \
                       f'\nЦена: {price}' \
                       f'\nСвоё сообщение: {free_order}' \
                       f'\n******************'
                for i in admin:
                    if photo:
                        bot.send_photo(i.tg_admin_id, photo=photo, caption=text)
                    else:
                        bot.send_message(i.tg_admin_id, text=text)

                #  Заказ от пользователя принят
                current_user.is_ordered = True
                current_user.save()

                bot.send_message(call.message.chat.id, text='Спасибо, наш менеджер в скором времени свяжется с вами!',
                                 reply_markup=start_markup())
            else:
                bot.send_message(call.message.chat.id,
                                 text='Заполнены не все обязательные поля. Просьба заполнить все пункты',
                                 reply_markup=request_markup(photo=photo, size=size, amount=amount, price=price,
                                                             free_order=free_order, fio=fio, phone_number=phone_number))

        elif 'refuse' in call.data:
            delete_message(call.message.id)

            #  Очищаем транзакцию пользователь-заказ
            try: current_user.delete()
            except: print(traceback.format_exc())

            bot.send_message(call.message.chat.id, text='До свидания! Спасибо за визит!', reply_markup=start_markup())


bot.infinity_polling(skip_pending=False)
