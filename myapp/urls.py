from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
  
app_name = 'myapp'
  
urlpatterns = [
    path('', views.index, name='index'),
 
    # ログイン、ログアウト
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('regist', views.regist, name='regist'),
    path('regist_save', views.regist_save, name='regist_save'),
 
    # お問い合わせ
    path('contact', views.contact.as_view(), name='contact'),
    path('contact_confirm', views.contact_confirm.as_view(), name='contact_confirm'),
    path('contact_send', views.contact_send.as_view(), name='contact_send'),
 
]