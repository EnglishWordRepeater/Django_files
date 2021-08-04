from .models import Note, eng_ru_word
from django.forms import ModelForm 

# ----------
# For save in Note table in DB
class NoteForm(ModelForm):
    class Meta: 
        model = Note 
        fields = ["name"]


# ----------
# For save in Note table in DB
# class NoteForm(ModelForm):
#     class Meta: 
#         model = Note 
#         fields = ["name"]