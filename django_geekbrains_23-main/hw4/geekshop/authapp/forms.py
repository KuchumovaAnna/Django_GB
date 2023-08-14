from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
import django.forms as forms
from authapp.models import UserEmail, ShopUser


class GenForm(forms.Form):

	newpass = forms.CharField(max_length=150)
	newpass.label = 'Новый пароль'
	newpass.required = False

	class Meta:
		model = ShopUser
		fields = ['newpass']

	def __init__(self, *args, **kwargs):
		new_pass = kwargs.get('new_pass',None)
		try:
			kwargs.pop('new_pass')
		except:
			pass
		super().__init__(*args, **kwargs)
		if new_pass is not None:
			self.fields['newpass'].widget.attrs['value'] = new_pass

class LoginForm(forms.Form):

	identity = forms.CharField(max_length=300)
	identity.localize = True
	identity.label = 'Email'
	identity.help_text = 'Введите адрес своей зарегистрированной почты'

	password = forms.CharField(max_length=30, min_length=5,widget=forms.PasswordInput)
	password.localize = True
	password.label = 'Пароль'
	password.help_text = 'Введите свой пароль, указанный при регистрации'

	remember = forms.BooleanField(required=False)
	remember.localized = True
	remember.label = 'Запомнить меня'

	ref = forms.CharField(max_length=50,required=False)
	ref.label = ''

	class Meta:
		model = ShopUser
		fields = ['identity', 'password', 'remember']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['ref'].widget.attrs['hidden'] = "true"
		self.fields['ref'].widget.attrs['value'] = "/"

class RegisterForm(UserCreationForm):

	
	class Meta:
		model = ShopUser
		fields = ['email','username','first_name', 'password1', 'password2',  'sex', 'avatar']

	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)
		
		self.fields['username'].label = 'Login:'
		self.fields['first_name'].label = 'Имя:'
		self.fields['password1'].label = 'Пароль:'
		self.fields['password2'].label = 'Пароль еще раз:'
		self.fields['email'].label = 'Эл. почта:'
		self.fields['email'].required = True
		self.fields['sex'].label = 'Пол:'
		self.fields['avatar'].label = 'Аватар:'


	def clean_username(self):
		data = self.cleaned_data['username']
		if len(data) < 6:
			raise forms.ValidationError("Login слишком короткий. Длина должна быть 6 символов минимум")
		return data

class EditForm(UserChangeForm):
	def __init__(self, *args, **kwargs):
		super(EditForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'
			field.help_text = ''
			if field_name == 'password':
				field.widget = forms.HiddenInput()

	class Meta:
		model = ShopUser
		fields = ['username', 'first_name', 'email', 'sex', 'avatar', 'password']
