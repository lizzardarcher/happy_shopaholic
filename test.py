#  ----- Initialize django ORM ------
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'happy_shopaholic.settings'
django.setup()
#  ----------------------------------

from core.models import *

# users = User.objects.filter(user_id=753169055)
admin = AdminSettings.objects.all()

# print(users.last())

for i in admin:
    print(i.tg_admin_id)