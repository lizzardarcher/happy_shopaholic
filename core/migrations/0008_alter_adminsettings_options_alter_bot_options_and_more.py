# Generated by Django 4.2.5 on 2023-09-22 09:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_user_fio_alter_user_date_time_alter_user_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adminsettings',
            options={'verbose_name': 'ID администратора TG канала', 'verbose_name_plural': 'ID администратора TG канала'},
        ),
        migrations.AlterModelOptions(
            name='bot',
            options={'verbose_name': 'Бот', 'verbose_name_plural': 'Бот'},
        ),
        migrations.AlterModelOptions(
            name='happyshopaholic',
            options={'verbose_name': 'Пересылка из ВК', 'verbose_name_plural': 'Пересылка из ВК'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователь TG бота', 'verbose_name_plural': 'Пользователи TG бота'},
        ),
        migrations.AlterField(
            model_name='bot',
            name='token',
            field=models.CharField(max_length=1000, verbose_name='Bot Token (‼️ не трогать ‼️)'),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 22, 9, 39, 41, 807441, tzinfo=datetime.timezone.utc), verbose_name='Дата и время заказа'),
        ),
    ]
