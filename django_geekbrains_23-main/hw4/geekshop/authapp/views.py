from functools import wraps
import random
import string

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from authapp.forms import LoginForm, RegisterForm, EditForm, GenForm
from authapp.models import ShopUser, UserEmail

uppercase_ = string.ascii_uppercase
lowercase_ = string.ascii_lowercase
digits_ = string.digits

def print_log(func):
	@wraps(func)
	def wrap(request, *args, **kwargs):
		print(f'>FUNC = {func.__name__}')
		print(f'request method = {request.method}')
		if request.method == 'POST':
			[print(f'{key}: {val}') for key,val in request.POST.items()]
		if request.method == 'GET':
			[print(f'{key}: {val}') for key,val in request.GET.items()]
		print(f'request.user = {request.user}')
		print(f'args = {args}')
		print(f'kwargs = {kwargs}')
		return func(request, *args, **kwargs)
	return wrap

def make_generateData(m=10):
	
	min_ = 1
	max_ = m-2
	u = random.randint(1,max_)
	
	max_ = m - u - 1
	d = random.randint(1,max_)

	l = m - u - d

	result = [random.choice(uppercase_) for i in range(u)] 
	result += [random.choice(lowercase_) for i in range(l)] 
	result += [random.choice(digits_) for i in range(d)] 
	random.shuffle(result)
	result = ''.join(result)
	return result

@print_log
def login(request, *args, **kwargs):
	login_form = LoginForm()
	if request.method == 'POST':
			login_form = LoginForm(data=request.POST)
			if login_form.is_valid():
				username = UserEmail.get_username_by_email(request.POST['identity'])
				password = request.POST['password']
				
				user = auth.authenticate(username=username, password=password)
				if user and user.is_active:
					auth.login(request, user)
					other_ref = request.POST.get('ref',None)
					return HttpResponseRedirect(other_ref)

	elif request.method == 'GET':
		ref = request.GET.get('ref',None)
		if ref is not None:
			login_form.fields['ref'].widget.attrs['value'] = ref


	context = {
		'title': "Вход",
		'login_form': login_form,
	}
	return render(request, 'authapp/login.html', context)

@print_log
def logout(request, *args, **kwargs):
	auth.logout(request)
	return HttpResponseRedirect(reverse('main')) 

@print_log
def registration(request, *args, **kwargs):
	gen_form = GenForm()
	if request.method == 'POST':
		if request.POST.get('gen',None) is not None:
			gen_form = GenForm(new_pass=make_generateData())
			register_form = RegisterForm()
		else:
			register_form = RegisterForm(request.POST, request.FILES)	
			if register_form.is_valid():
				register_form.save()
				return HttpResponseRedirect(reverse('auth:login'))
	else:
		register_form = RegisterForm()
	not_empty_list = [
		'username',
		'email',
		'password1',
		'password2']
	context = {
		'title': 'Регистрация',
		'register_form': register_form,
		'not_empty_list': not_empty_list,
		'gen_form': gen_form
	}
	return render(request, 'authapp/registration.html', context)

@print_log
def restore(request, *args, **kwargs):
	message = ''
	color = '1ba300'
	if request.method == 'POST':
		email = request.POST['email']
		username = UserEmail.get_username_by_email(email)
		if not username:
			message = f'email {email} не найден в базе'
			color = 'ff0000'
		else:
			message = f'на email {email} будет отправлено письмо с новым паролем'
	context = {
	'color' : color,
	'message' : message,
	'title':'Напомнить пароль',
	}
	return render(request, 'authapp/restore.html',context)

