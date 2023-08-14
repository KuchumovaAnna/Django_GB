from functools import wraps
from urllib.parse import urlparse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.contrib.auth.views import redirect_to_login
from django.template.loader import render_to_string

from basketapp.models import ItemInBasket,UserOrder
from mainapp.models import Item

def update_basket(request):
	post_data = request.POST
	items = dict((key.replace('count__',''),value) for key,value in post_data.items() if key.startswith("count__"))

	for key, quantity in items.items():
		item = Item.find_item_by_vendor_code(key)
		if not ItemInBasket.add_item_in_ItemInBasket(request.user,item,int(quantity),False):
			break 
			return False
	return True

#@login_required(redirect_field_name='ref')
#def update_row(request, *args, **kwargs):
#	print("update_row")
#	if request.is_ajax():
#		content = {
#			'basket': basket,
#		}
#		result = render_to_string('basketapp/basket.html', content)
#	else:
#		raise Http404("price search error")

def advance_redirect_to_login(function):
	def wrapper(request, *args, **kwargs):
		real_ref = urlparse(request.META.get('HTTP_REFERER')).path
		if not request.user.is_authenticated:
			return redirect_to_login(real_ref, redirect_field_name='ref')
		else:
			return function(request, *args, **kwargs)
	return wrapper

@advance_redirect_to_login
def add_item(request,*args,**kwargs):

	if request.method == 'POST':
		user = request.user
		vendor_code = request.POST['vendor_code']
		count = int(request.POST['count'])
		item_obj = Item.find_item_by_vendor_code(vendor_code)
		if item_obj is not None and count>0:
			if not ItemInBasket.add_item_in_ItemInBasket(user,item_obj,count):
				raise Http404("price search error")
			return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		raise Http404("error vendor code or count")

@login_required(redirect_field_name='ref')
def del_item(request,v_code,*args,**kwargs):
	context = {
	'title':'Добавление товара',
	}
	if request.method == 'GET':
		user = request.user
		item = Item.find_item_by_vendor_code(v_code)
		if not ItemInBasket.del_item_in_ItemInBasket(user,item):
			return HttpResponse('object delete error')
		else:
			return HttpResponseRedirect(reverse('basket:basket'))	
	else:
		return HttpResponse('object delete error')

@login_required(redirect_field_name='ref')
def basket(request,*args,**kwargs):
	context = {
	'title':'Товары в корзине',
	}

	inBasket = ItemInBasket.objects.filter(user = request.user)
	context['inBasket'] = inBasket 
	context['total_quantity'] = inBasket[0].total_quantity if inBasket else 0
	context['total_price']= inBasket[0].total_price	 if inBasket else 0
	return render(request, 'basketapp/basket.html',context)

@login_required(redirect_field_name='ref')
def buy(request,*args,**kwargs):

	if request.method == 'POST':
		if request.POST.get('save',None) is not None:
			if not update_basket(request):
				return HttpResponse('Ошибка обновления корзины')	
		elif  request.POST.get('saveAndSend',None) is not None:
			if update_basket(request):
				neworder = UserOrder.createOrder(request.user)
				if neworder is not None:
					return HttpResponse(f'Номер вашего заказа: {neworder.order}')	
				else:
					return HttpResponse('Ошибка формирование покупки')	
		return HttpResponseRedirect(reverse('basket:basket'))	
	else:
		raise Http404("buy error")