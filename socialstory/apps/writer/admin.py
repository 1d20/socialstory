from django.contrib import admin
from models import *
from models import UserSettings

admin.site.register(Writer)
admin.site.register(WriterRead)
admin.site.register(WriterVote)
admin.site.register(WriterFavorite)
admin.site.register(Comments)
admin.site.register(Notes)
admin.site.register(Marks)
admin.site.register(Setting)
admin.site.register(SettingValue)
admin.site.register(UserSettings)
