from django.contrib import admin
from models import Genre, SubGenre, Story, Language, SimilarStory, Versions

admin.site.register(Genre)
admin.site.register(SubGenre)
admin.site.register(Story)
admin.site.register(Language)
admin.site.register(SimilarStory)
admin.site.register(Versions)