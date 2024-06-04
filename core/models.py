from datetime import datetime

import django.utils.timezone
from django.db import models
from django.utils.timezone import now

SIZE = [
    ('XS', 'XS',),
    ('S', 'S',),
    ('M', 'M',),
    ('L', 'L',),
    ('XL', 'XL',),
    ('XXL', 'XXL',),
    ('4', '4',),
    ('4.5', '4.5',),
    ('5', '5',),
    ('5.5', '5.5',),
    ('6', '6',),
    ('6.5', '6.5',),
    ('7', '7',),
    ('7.5', '7.5',),
    ('8', '8',),
    ('8.5', '8.5',),
    ('9', '9',),
    ('9.5', '9.5',),
    ('10', '10',),
    ('10.5', '10.5',),
    ('11', '11',),
    ('11.5', '11.5',),
    ('12', '12',),
    ('12.5', '12.5',),
    ('13', '13',),
    ('13.5', '13.5',),
    ('14', '14',),
    ('14.5', '14.5',),
    ('15', '15',),
    ('15.5', '15.5',),
    ('16', '16'),
]


class User(models.Model):
    id = models.IntegerField(auto_created=True, null=False, blank=True, primary_key=True, verbose_name='Id', editable=False)

    user_id = models.IntegerField(null=False, blank=True, verbose_name='user_id')
    username = models.CharField(null=True, blank=True, max_length=1000, verbose_name='Username')
    first_name = models.CharField(null=True, blank=True, max_length=1000, verbose_name='First_name')
    last_name = models.CharField(null=True, blank=True, max_length=1000, verbose_name='Last_name')
    fio = models.CharField(max_length=500, null=True, blank=True, verbose_name='ФИО')
    phone_number = models.CharField(null=True, blank=True, max_length=1000, verbose_name='Phone')
    photo = models.CharField(max_length=5000, null=True, blank=True, verbose_name='URL фото из TG')
    size = models.CharField(max_length=20, null=True, blank=True, choices=SIZE, verbose_name='Размер')
    amount = models.IntegerField(null=True, blank=True, verbose_name='Кол-во')
    price = models.CharField(max_length=500, null=True, blank=True, verbose_name='Цена')
    free_order = models.TextField(max_length=500, null=True, blank=True, verbose_name='Заказ в свободной форме')
    is_ordered = models.BooleanField(default=False, null=True, blank=True, verbose_name='Оформление Завершено')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время заказа')

    def __str__(self):
        if self.is_ordered:
            return '✅ ' + str(self.date_time).split('.')[0] + ' :: ' + str(self.first_name) + ' ' + str(self.last_name) + ' ' + str(self.user_id)
        else:
            return '❌' + str(self.date_time).split('.')[0] + ' :: ' + str(self.first_name) + ' ' + str(self.last_name) + ' ' + str(self.user_id)

    class Meta:
        verbose_name = 'Пользователь TG бота'
        verbose_name_plural = 'Пользователи TG бота'


class Happyshopaholic(models.Model):
    post_id = models.IntegerField(unique=True, null=False, blank=True, verbose_name='ID поста')
    text = models.TextField(max_length=1024, null=True, blank=True, verbose_name='Текст')
    photo_list = models.TextField(max_length=100000, null=True, blank=True, verbose_name='URL Фото VK')
    is_sent = models.BooleanField(default=False, null=True, blank=True, verbose_name='Отправлено')

    def __str__(self):
        return str(self.post_id) + ' | Отправлено: ' + str(self.is_sent)

    class Meta:
        db_table = 'happyshopaholic'
        verbose_name = 'Пересылка из ВК'
        verbose_name_plural = 'Пересылка из ВК'


class Bot(models.Model):
    token = models.CharField(null=False, blank=False, max_length=1000, verbose_name='Bot Token (‼️ не трогать ‼️)')

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Бот'


class AdminSettings(models.Model):
    tg_admin_id = models.CharField(null=False, blank=False, max_length=1000, verbose_name='Admin id')

    def __str__(self):
        return str(self.tg_admin_id)

    class Meta:
        verbose_name = 'ID администратора TG канала'
        verbose_name_plural = 'ID администратора TG канала'
