from django.db import models
from django.contrib.auth.models import User
# Создаем две сущности "Запись" -|---------<- "Пара слов англ. - рус." (связь один ко многим)
# https://metanit.com/python/django/5.6.php
# Позже сущность "Заись" свяжем с ползователем, вот так: "Пользователь" -|---------<- "Запись" (связь один ко многим)
# Когда основной функционал запилим и разберемся с аунтетификацией :)))


# -------
# Создаем сущность "Запись"
class Note(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name='note_key')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'заметку'
        verbose_name_plural = 'Заметки'

# -------
# Создаем сущность "пара англ. слово - рус. слово"
class eng_ru_word(models.Model):
    note = models.ForeignKey(Note, on_delete = models.CASCADE, null=True, related_name='note_key')
    english_word = models.CharField(max_length=30)
    russian_word = models.CharField(max_length=30)

    def __str__(self):
        return self.note.name
    
    class Meta:
        verbose_name = 'слова'
        verbose_name_plural = 'Словарь'

    