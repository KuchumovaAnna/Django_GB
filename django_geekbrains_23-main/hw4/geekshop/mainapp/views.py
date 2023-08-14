from functools import wraps
import json
import os
import random
from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import AnonymousUser
from mainapp.models import ParentCategory,ItemCategory,Item,Price,Quantity,Full_description

def user_login(func):
	@wraps(func)
	def wrap(request, *args,**kwargs):
		print(f'request = {request}')
		print(f'request.user = {request.user}')
		print(f'args = {args}')
		print(f'kwargs = {kwargs}')
		user = request.user
		user_login_dict = {
			'user':user,
			'is_authenticated':user.is_authenticated
		}
		setattr(wrap,'context',user_login_dict)
		return func(request, *args,**kwargs)
	return wrap

def makeCategoryList():
	result_list = []
	parentlist = ParentCategory.objects.all()
	p = parentlist[0]
	for parent in parentlist:
		if p != parent:
			result_list[-1][2] = True
		result_list.append([parent,None,False])
		categorylist = ItemCategory.objects.filter(parent_name__idx = parent.idx)
		for category in categorylist:
			result_list.append([None,category,False])
	return result_list

def getHotItem():
	items_all = Item.objects.all()
	return  random.sample(list(items_all), 1)[0]

def getNewItems(samples=5, hotitem = None):
	items_all = Item.objects.all()
	if hotitem is not None:
		items_all = items_all.exclude(pk=hotitem.pk)
	return random.sample(list(items_all), samples)	

@user_login
def main(request,*args,**kwargs):
	hotitem = getHotItem()
	items = getNewItems(3,hotitem)
	
	context_data = {
	'title':'Главная',
	'items':items,
	'hotitem':hotitem,
	'categorylist':makeCategoryList(),
	}
	main.context.update(context_data)
	return render(request, 'mainapp/main.html',main.context)

@user_login
def delivery(request,*args,**kwargs):
	context_data = {
	'title':'Доставка'
	}
	delivery.context.update(context_data)
	return render(request, 'mainapp/delivery.html',delivery.context)

@user_login
def help(request,*args,**kwargs):
	context_data = {
	'title':'Помощь'
	}
	delivery.context.update(context_data)
	return render(request, 'mainapp/help.html',delivery.context)

@user_login
def catalog(request, *args, **kwargs):
	dir1 = kwargs.get('dir1',None)
	dir2 = kwargs.get('dir2',None)
	try:
		cat = ItemCategory.objects.filter(parent_name__idx = dir1, idx = dir2)[0]
	except:
		cat = ItemCategory.objects.filter(parent_name__idx = 2, idx = 1)[0]
	items = Item.objects.filter(category = cat)
	prices = Price.objects.filter(vendor_code__in = [i.vendor_code for i in items])
	price_dict = {}
	for price in prices:
		price_dict[price.vendor_code] = {'price':price.price,'price_unit':price.price_unit}
	context_data = {
	'title':'Каталог',
	'category':cat,
	'categorylist':makeCategoryList(),
	'items':items,
	'price_dict':price_dict,
	}
	catalog.context.update(context_data)
	return render(request, 'mainapp/catalog.html',catalog.context)

@user_login
def item(request, *args, **kwargs):
	dir1 = kwargs.get('dir1',None)
	dir2 = kwargs.get('dir2',None)
	vend = kwargs.get('vend',None) 
	item_ = Item.objects.get(vendor_code = vend)
	price_ =  item_.find_last_price
	description =  Full_description.objects.get(item = item_)
	context_data = {
	'title':'Каталог',
	'categorylist':makeCategoryList(),
	'item':item_,
	'price':price_,
	'description':description,
	}
	item.context.update(context_data)
	return render(request, 'mainapp/item.html',item.context)
