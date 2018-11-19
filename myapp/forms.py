from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from users.models import  User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
 
class LoginForm(AuthenticationForm):
 
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
 
    self.fields['username'].widget.attrs['class'] = 'form-control'
    self.fields['username'].widget.attrs['placeholder'] = 'メールアドレス'
  
    self.fields['password'].widget.attrs['class'] = 'form-control'
    self.fields['password'].widget.attrs['placeholder'] = 'パスワード'
 
 
class RegisterForm(UserCreationForm):
 
  # 入力を必須にするため、required=Trueで上書き
  email = forms.EmailField(required=True)
  nick_name = forms.CharField(required=True)
 
  class Meta:
    model = User
 
    fields = (
      "email", "password1", "password2", 
      "nick_name",
    )
 
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
 
    self.fields['nick_name'].widget.attrs['class'] = 'form-control'
    self.fields['nick_name'].widget.attrs['placeholder'] = 'お名前'
 
    self.fields['email'].widget.attrs['class'] = 'form-control'
    self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'
 
    self.fields['password1'].widget.attrs['class'] = 'form-control'
    self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'
  
    self.fields['password2'].widget.attrs['class'] = 'form-control'
    self.fields['password2'].widget.attrs['placeholder'] = 'パスワード（確認）'
 
class ContactForm(forms.Form):
    name = forms.CharField(max_length=20) # 名前
    email = forms.CharField(max_length=40)
    message = forms.CharField(widget=forms.Textarea, max_length=100) #問い合わせ内容
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前'
        self.fields['name'].widget.attrs['maxlength'] = '20'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレス'
        self.fields['name'].widget.attrs['maxlength'] = '40'
        self.fields['message'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージ'
        self.fields['message'].widget.attrs['maxlength'] = '200'
        self.fields['message'].widget.attrs['rows'] = '6'
 
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("正しいメールアドレスを指定して下さい。")