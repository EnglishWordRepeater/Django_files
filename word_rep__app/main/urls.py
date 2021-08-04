from django.urls import path 
from . import views
from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
    path('', views.main_page, name='home'),
    path('add_note/', views.add_note, name='add_note'),
    path('submit/', views.submit_words_handler, name='submit_words_handler'),
    path('edit/<int:id>/', views.edit_page, name='change_page'),
    path('registration/', views.registration_user, name='registration'), # регистрация
    path('login/', views.login_user, name='login'), # для зареганного
    path('logout/', views.logout_user, name='logout'), # для выхода
    path('delete/<int:id>', views.delete_page, name='delete'), # для выхода
]