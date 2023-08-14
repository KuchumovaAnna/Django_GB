from django import template
from basketapp.models import ItemInBasket
from django.db.models import Sum
register = template.Library()


@register.filter('get_price')
def get_price(dict_data, key = ''):
		try:
			return dict_data.get(key,'').get('price')
		except:
			return ''

@register.filter('get_price_unit')
def get_price_unit(dict_data, key = ''):
		try:
			return dict_data.get(key,'').get('price_unit')
		except:
			return ''

@register.filter('get_sum_of_basket')
def get_sum_of_basket(basket):
	return sum([i.price*i.quantity for i in basket])

@register.filter('get_sum_of_basket_by_user')
def get_sum_of_basket_by_user(user, is_authenticated):
	if is_authenticated:
		inBasket = ItemInBasket.objects.filter(user=user)
		return get_sum_of_basket(inBasket)
	return 0

@register.filter('get_quantity_of_basket_by_user')
def get_quantity_of_basket_by_user(user, is_authenticated):
	if is_authenticated:
		inBasket = ItemInBasket.objects.filter(user = user)
		result = inBasket.aggregate(Sum('quantity'))['quantity__sum']
		return 0 if result is None else result
	else:
		return 0

	
