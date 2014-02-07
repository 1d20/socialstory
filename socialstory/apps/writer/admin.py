from django.contrib import admin
from models import Writer, WriterRead, WriterVote, WriterFavorite, Comments, Friends, Messages, Setting, SettingValue
from models import UserSettings

admin.site.register(Writer)
admin.site.register(WriterRead)
admin.site.register(WriterVote)
admin.site.register(WriterFavorite)
admin.site.register(Comments)
admin.site.register(Friends)
admin.site.register(Messages)
admin.site.register(Setting)
admin.site.register(SettingValue)
admin.site.register(UserSettings)
