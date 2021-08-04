from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponseNotFound
from django.http import HttpResponseRedirect, FileResponse

from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User

from pydub import AudioSegment
import gtts
import os
from word_rep__app.settings import BASE_DIR
import pydub

from django.conf import settings
from django.http import HttpResponse, Http404

from googletrans import Translator

from transliterate import translit
import time

import pyttsx3
import ffmpeg 
# import codecs

# --------
# Показывает главную страницу 
def main_page(request):
    if request.user.is_authenticated:
        notes = Note.objects.filter(user=request.user)
        remove_after(request)
        return render(request, 'main_templates/home_authenticated.html', {'notes' : notes })
    else:
        remove_after(request)
        return render(request, 'main_templates/home_not_authenticated.html')
    

# --------
# Отображение страницы "Добавить запись" или попробовать
def add_note(request):
    if request.user.is_authenticated:

        # Пробуем перевести слово 
        # translator = Translator() 
        # print(translator.translate('ПРИВЕТ ВСЕМ!').text)

        if request.method == "POST":
            if (request.POST['save'] == 'personal'):
                submit_words_handler_pers(request)
                return redirect("home")
                # return render(request, 'main_templates/home_authenticated.html')
            elif (request.POST['save'] == 'mp3'):
                # submit_words_handler_mp3(request)
                return submit_words_handler_mp3(request)
        return render(request, 'main_templates/add_note.html')
    else:
        if request.method == "POST":
            if (request.POST['save'] == 'mp3'):
                # submit_words_handler_mp3(request)
                return submit_words_handler_mp3(request)
        return render(request, 'main_templates/try_without_registration.html')


# --------
# Отображение страницы "Изменить запись"
def change_page(request, id):
    change = eng_ru_word.objects.all()
    true_id = Note.objects.get(id=id).id # получаю id статьи
    title = Note.objects.filter(id=id)
    print(id)

    context = {
        "change" : change,
        'true_id' : true_id,
        'title' : title,
    }

    return render(request, 'main_templates/change_page.html', context=context)

def delete_page(request, id):
    delete_note = Note.objects.get(id=id)
    print("Тут удаление")
    print(BASE_DIR)
    delete_note.delete()
    
    return HttpResponseRedirect("/")

def remove_after(request):
    # counter = 0
    # time.sleep(5)
    path = str(BASE_DIR) + f'/main/media/audio/'
    print("УДАЛЯЮ")
    
    if len(os.listdir(path)) != 0:
        for f in os.listdir(path):
            if os.stat(os.path.join(path,f)):
                os.remove(os.path.join(path, f))
        return HttpResponseRedirect("home")


# --------
# Обработчик сохранения новой страницы
def submit_words_handler(request):
    if (request.POST['save'] == 'personal'):
        submit_words_handler_pers(request)
        return redirect("home")
        # return render(request, 'main_templates/home_authenticated.html')
    elif (request.POST['save'] == 'mp3'):
        # submit_words_handler_mp3(request)
        return submit_words_handler_mp3(request)
    elif (request.POST['save'] == 'pdf'):
        submit_words_handler_pdf(request)
        return render(request, 'main_templates/home_authenticated.html')
        


# --------
# Обработчик сохранения в ЛК
def submit_words_handler_pers(request, id = ''):
    # Получение всех слов на русском
    rus_words = []
    for key in request.POST:
        if (key[:8] == 'word_ru_'):
            print(key)
            rus_words.append(request.POST[key])

    # Получене всех слов на английском 
    en_words = []
    for key in request.POST:
        if (key[:8] == 'word_en_'):
            print(key)
            en_words.append(request.POST[key])

    # Сохранаяем пустую запись в модель Note
    if request.method == 'POST':
        if id:
            note = Note.objects.get(id=id)
            words = eng_ru_word.objects.filter(note=note)
            words.delete()
        else: # 
            note = Note()
            note.name = request.POST.get("note_title")
            note.user = request.user
            note.save()

    # Сохранение английские и русские слова в пустую свежесозданную запись note
    if request.method == 'POST':
        for i in range(len(en_words)):
            words_pare = eng_ru_word()
            words_pare.note = note
            words_pare.english_word = en_words[i]
            words_pare.russian_word = rus_words[i]
            words_pare.save()

#склеивание аудио
def concat_audios(lis, file_location):
    st = ["ffmpeg"]
    for i in range(len(lis)):
        st.append("-i")
        st.append(lis[i])
    st.append("-filter_complex")
    st = ' '.join(st) + " "
    for i in range(len(lis)):
        st = st + "[" + str(i) + ":0]"

    st = st + "concat=n=" + str(len(lis)) + ":v=0:a=1[out] -map [out] " + file_location
    print(st)
    try:
        os.remove(file_location)
    except:
        pass

    os.system(st)
# concat_audios(['eng.mp3', 'rus.mp3'], 'result.mp3')


# --------
# Обработчик сохранения в mp3
def submit_words_handler_mp3(req):
    file_name = req.POST.get('note_title')
    path_to_save = str(BASE_DIR) + '/main/media/audio'
    
   
    # Получение всех слов на русском
    rus_words = []
    for key in req.POST:
        if (key[:8] == 'word_ru_'):
            rus_words.append(req.POST[key])

    # Получене всех слов на английском 
    en_words = []
    for key in req.POST:
        if (key[:8] == 'word_en_'):
            en_words.append(req.POST[key])


    #--
    # eng = ['Hello cat', 'how are you']
    # rus = ['Привет', 'кошка']

    print(en_words)
    print(rus_words)
    eng_eng = pyttsx3.init() # инифиализирую как бы первый поток
    voices = eng_eng.getProperty('voices') # добавляю голос вроде
    eng_eng.setProperty('voice', voices[1].id) # voices[1].id (можно менять от 0-4(1 - это английский голос женский))
    # eng_eng.say(en_words) # можно прослушать
 

    for i in range(len(rus_words)):
        eng_eng.save_to_file(en_words[i], f'{path_to_save}/word_en_{i}.mp3')
       

    eng_rus= pyttsx3.init()
    voices = eng_rus.getProperty('voices')
    eng_rus.setProperty('voice', voices[0].id) # voices[1].id (можно менять от 0-4(0 - это русский голос женский вроде))
    # eng_rus.say(rus_words)
   
    for i in range(len(rus_words)):
        eng_eng.save_to_file(rus_words[i], f'{path_to_save}/word_ru_{i}.mp3')

    eng_eng.runAndWait() # закрытие аудиопотока что-то такое
    eng_rus.runAndWait() 
   
    result_audio = []
    for i in range(len(rus_words)):
        result_audio.append(f'{path_to_save}/word_en_{i}.mp3')
        result_audio.append(f'{path_to_save}/word_ru_{i}.mp3')

    trnsl_filename = translit(file_name.replace(" ", ""), 'ru', reversed=True)
    print("trnsl_filename - ", trnsl_filename)
    # первым аргументом передается массив из входных файлов для склеивания
    concat_audios(result_audio, f'{path_to_save}/{trnsl_filename}.mp3')
    #--
    

    # # Генерация файлов
    # for i in range(len(rus_words)):
    #     speech1 = gtts.gTTS(text = str({en_words[i]}), lang = 'en', slow = False)
    #     speech2 = gtts.gTTS(text = str({rus_words[i]}), lang = 'ru', slow = False)
    #     speech1.save(f'{path_to_save}/word_en_{i}.mp3')
    #     speech2.save(f'{path_to_save}/word_ru_{i}.mp3')

    # # Склеиваем все мп3 в один
    # first = AudioSegment.from_mp3(f'{path_to_save}/word_en_0.mp3')
    # sec = AudioSegment.from_mp3(f'{path_to_save}/word_ru_0.mp3')
    # silent = AudioSegment.silent(duration=1500)

    # result_promezh_bulok = first + sec
    # os.remove(f'{path_to_save}/word_en_0.mp3')
    # os.remove(f'{path_to_save}/word_ru_0.mp3')

    # for i in range(1, len(rus_words)):
    #     first = AudioSegment.from_mp3(f'{path_to_save}/word_en_{i}.mp3')
    #     sec = AudioSegment.from_mp3(f'{path_to_save}/word_ru_{i}.mp3')
    #     result_promezh_bulok += silent + first + sec
    #     os.remove(f'{path_to_save}/word_en_{i}.mp3')
    #     os.remove(f'{path_to_save}/word_ru_{i}.mp3')

    
    # trnsl_filename = translit(file_name, 'ru', reversed=True)
    

    # result = result_promezh_bulok
    # result.export(f'{path_to_save}/{trnsl_filename}.mp3', format='mp3')

    
    return download(path_to_save + '/' + trnsl_filename + '.mp3')
    # return HttpResponseRedirect('/')




# --------
# Скачивание файла mp3 полсе генерации
def download(path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/force-download")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


# --------
# Обработчик сохранения в pdf
def submit_words_handler_pdf(req):
    pass


# --------
# Обработчик изменения записи
def edit_page(request, id):

    try:
        obj = Note.objects.get(id=id)
        true_id = Note.objects.get(id=id).id 
        words = eng_ru_word.objects.filter(note=obj)

        context = {
            'obj': obj,
            'words' : words,
            'true_id' : true_id,
        }
      
        if (request.method == "POST"):

            # obj.name = request.POST.get("note_title")
        
            # for i in words:
            #     if(i.note.id == true_id):
            #         i.english_word = request.POST.get(f'word_en_{i.id}')
            #         i.russian_word = request.POST.get(f'word_ru_{i.id}')
            #         i.save()
            #     obj.save()

            submit_words_handler_pers(request, id)

            if (request.POST['save'] == 'mp3'):
                return submit_words_handler_mp3(request)

            return HttpResponseRedirect("/")
        
        else:
            return render(request, "main_templates/change_page.html", context=context)

    except eng_ru_word.DoesNotExist:
        return HttpResponseNotFound("<h2>Object not found</h2>")


# --------
# Сохранение данных в бд
def save_edit(request, id):
    if request.method == "POST":
        obj = Note()
        words = eng_ru_word(note=obj)

        obj.name = request.POST.get("name")
        words.english_word = request.POST.get("word_en_0")
        words.russian_word = request.POST.get("word_ru_0")

        print(words.english_word)
        print(words.russian_word)
        
        words.save()
        
        
    return HttpResponseRedirect("/")


# --------
# Регистрация нового пользователя
def registration_user(request):
    if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if User.objects.filter(username=username).exists():
                print("Пользователь уже есть..")
            else:
                if password == password2: # если пароли верные
                    User.objects.create_user(username, email, password)
                    print("Пользователь создан", username)
                    login_user(request)
                    return redirect(reverse("home"))
                else:
                    pass # если пароли неверные, написать типо ваш пароль неверный повторите попытку
    return render(request, 'registration_templates/register.html')


# --------
# Вход в личный кабинет
def login_user(request):
    context = {}
    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active: # user.is_active: если пользователь активен, наверное
                login(request, user)
                print("Пользователь найден", user.username)
                return redirect(reverse("home"))
            else:
                print("Пользователь не найден")
    return render(request, 'registration_templates/login.html', context=context)


# --------
# Выход из личного кабинета
def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

