from django.contrib import admin
from core.models import *
from django.contrib.auth.models import User as DjangoUser, Group

admin.site.site_url = ''
admin.site.site_header = "HappyShopaholic Админ Панель"
admin.site.site_title = "HappyShopaholic"
admin.site.index_title = "Добро пожаловать в HappyShopaholic Админ Панель"

# admin.site.unregister(DjangoUser)
admin.site.unregister(Group)

class UserAdmin(admin.ModelAdmin):
    list_display = ('date_time',
                    'username',
                    'first_name',
                    'last_name',
                    'phone_number',
                    'fio',
                    'size',
                    'amount',
                    'price',
                    'is_ordered',)
    list_display_links = ('username', 'first_name', 'last_name')
    search_fields = ('username',
                     'first_name',
                     'last_name',
                     'phone_number',
                     'fio',
                     'user_id')
    list_filter = ('date_time', 'is_ordered')
    # search_help_text = 'Поиск'
    fields = ['date_time',
              'user_id',
              'username',
              'first_name',
              'last_name',
              'phone_number',
              'fio',
              'size',
              'amount',
              'price',
              'is_ordered',
              'free_order',
              'photo']
    empty_value_display = ""
    ordering = ['date_time', 'is_ordered']

class BotAdmin(admin.ModelAdmin):
    list_display = ('token',)
    fields = ['token']


class AdminSettingsAdmin(admin.ModelAdmin):
    list_display = ('tg_admin_id',)
    fields = ['tg_admin_id']


class HappyshopaholicAAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'is_sent')
    fields = ['post_id', 'text', 'photo_list', 'is_sent']
    search_fields = ('post_id', 'text')
    # search_help_text = 'Поиск'
    list_filter = ('is_sent',)
    ordering = ['post_id']


admin.site.register(Bot, BotAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Happyshopaholic, HappyshopaholicAAdmin)
admin.site.register(AdminSettings, AdminSettingsAdmin)
