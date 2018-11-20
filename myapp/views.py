from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import (
  LoginForm,
  RegisterForm,
  UserPasswordChangeForm
)
from django.urls import reverse_lazy
from .forms import  ContactForm
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth import login as auth_login
from users.backends import EmailModelBackend
 
User = get_user_model()
 
 
def index(request):
  context = {
    'myapp':request.user,
  }
  return render(request, 'index.html', context)
 
def login(request):
    context = {
        'template_name': 'login.html',
        'authentication_form': LoginForm
    }
    return auth_views.login(request, **context)
  
  
def logout(request):
    context = {
        'template_name': 'index.html',
    }
    return auth_views.logout(request, **context)
 
 
def regist(request):
  form = RegisterForm(request.POST or None)
  context = {
    'form':form,
  }
  return render(request, 'regist.html', context)
 
 
＠require_POST
def regist_save(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('users:index')
  
    context = {
        'form': form,
    }
    return render(request, 'regist.html', context)
 
class contact(generic.FormView):
    """お問い合わせフォームページ"""
 
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('myapp:contact_confirm')
 
    def get_form(self, form_class=None):
        # contact.hmltで、データを送信した場合
        if 'name' in self.request.POST:
            form_data = self.request.POST
  
        # お問い合わせフォーム確認画面から「戻る」リンクを押した場合や
        # 初回の入力欄表示は以下の表示。
        # セッションにユーザーデータがあれば、それをフォームに束縛
        else:
            form_data = self.request.session.get('form_data', None)
  
        return self.form_class(form_data)
  
    def form_valid(self, form):
        # 入力した値を、セッションに保存
        self.request.session['form_data'] = self.request.POST
        return super().form_valid(form)
 
 
class contact_confirm(generic.TemplateView):
    """お問い合わせフォーム確認ページ"""
 
    template_name = 'contact_confirm.html'
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_data = self.request.session.get('form_data', None)
        context['form'] = ContactForm(form_data)
        return context
 
 
class contact_send(generic.FormView):
    """お問い合わせ送信"""
 
    form_class = ContactForm
    success_url = reverse_lazy('myapp:index')
  
    def get_form(self, form_class=None):
        # popで、セッションに入れたユーザーデータ自体取り出し
        form_data = self.request.session.pop('form_data', None)
 
        #メール送信
        subject = form_data['name']
        message = form_data['message']
        from_email = form_data['email']
        to = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to)
 
        return self.form_class(form_data)
