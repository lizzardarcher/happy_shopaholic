token = 'vk1.a.RV-ptw26HPEs93GZttvOIoQr_JcyogTeQzwab01bDAukPYrQ3jBeY66uZ1qm0Oe-wNDZkDdJcWr0FnHMqT5INg3HURzr68LQD1-tUOU6frZgcMW4FikrzTy17kEmmazW2ujkHh0pOw3Z5QY96fHj49jfEbUfQkBFVdsC-C27G2Hm-XMbLwq28EOXGUZ1kvr_'
group_name = 'happyshopaholic'
count = '10'
api_version = '5.131'

url = f'https://api.vk.com/method/wall.get?domain={group_name}&count={count}&access_token={token}&v={api_version}'

local_db = 'my_database.sqlite'

tg_token = '5383269929:AAHXjh9u_KUWlAH2HrD3Z6Sthul5qVC4fLI'

tg_channel = '-1001701702209'
# tg_channel = '-1001885966596'  # тестовый канал

SIZE = [
    'XS', 'S', 'M', 'L', 'XL', 'XXL',
    '4', '4.5', '5', '5.5', '6', '6.5', '7', '7.5',
    '8', '8.5', '9', '9.5', '10', '10.5', '11', '11.5',
    '12', '12.5', '13', '13.5', '14', '14.5', '15', '15.5', '16'
]

greetings = 'greetings.jpg'

def django_orm_setup():
    """
    Init django ORM for this project
    :return:
    """
    import os
    import django

    os.environ['DJANGO_SETTINGS_MODULE'] = 'happy_shopaholic.settings'
    django.setup()
