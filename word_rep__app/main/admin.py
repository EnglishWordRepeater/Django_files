from django.contrib import admin
from .models import *


class NoteView(admin.ModelAdmin):
    list_display = ['id', 'name', 'user']
    search_fields = ['name']
admin.site.register(Note, NoteView)


class eng_ru_wordView(admin.ModelAdmin):
    list_display = [ 'id', 'note', 'english_word', 'russian_word']
    list_filter = ['note']
admin.site.register(eng_ru_word, eng_ru_wordView)
