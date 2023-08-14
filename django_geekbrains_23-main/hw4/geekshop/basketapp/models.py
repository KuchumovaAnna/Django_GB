from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from mainapp.models import Item, Price

#зарезервированный для покупки товар
class ItemInBasket(models.Model):

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE)
	item = models.ForeignKey(
		Item, 
		on_delete=models.CASCADE)
	price = models.DecimalField(
		verbose_name='цена',
		max_digits=8,
		decimal_places=2, 
		default = 0,
		blank=0)
	quantity = models.DecimalField(
		verbose_name='количество',
		max_digits=8,
		decimal_places=0, 
		blank=0)

	def __str__(self):
		return f'{self.user.username}. {self.item.name} (price = {price}, quantity={quantity}'	

	class Meta():
		ordering = ['item']

	@property
	def total_quantity(self):
		inBasket = ItemInBasket.objects.filter(user = self.user)
		result = inBasket.aggregate(models.Sum('quantity'))
		return result['quantity__sum']

	@property
	def total_price(self):
		inBasket = ItemInBasket.objects.filter(user = self.user)
		return sum([i.price*i.quantity for i in inBasket])

	@property
	def item_total_price(self):
		return self.price*self.quantity

	@staticmethod
	def add_item_in_ItemInBasket(user,item,quantity,add_quantity=True):
		price = item.find_last_price
		if price is None:
			return False
		data_dict = {
			'user':user,
			'item':item,
			'price':price.price,
			'quantity':quantity,
		}
		try:
			record = ItemInBasket.objects.get(user=user,item=item)
			if add_quantity:
				record.quantity += quantity
			else:
				record.quantity = quantity
		except ObjectDoesNotExist:
			record = ItemInBasket.objects.create(**data_dict)
		record.save()
		return True

	@staticmethod
	def del_item_in_ItemInBasket(user,item):
		try:
			record = ItemInBasket.objects.get(user=user,item=item)
			record.delete()
		except ObjectDoesNotExist:
			return False
		else:
			return True

class UserOrder(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE)	

	order = models.AutoField(
		verbose_name='номер ордера покупки',
		primary_key=True)

	def __str__(self):
		return f'{self.user}: {self.order}'	

	class Meta():
		ordering = ['user']

	@classmethod
	def createOrder(cls,user):
		InBasket = 	ItemInBasket.objects.filter(user=user)
		newUserOrder = cls(user=user)
		newUserOrder.save()
		try:
			dl = InBasket.values()
			for row in dl:
				data = {
					'user':user,
					'item': Item.objects.get(pk=row['item_id']),
					'order': newUserOrder,
					'price': row['price'],
					'quantity': row['quantity'],
				}
				newPastPurchases = PastPurchases.objects.create(**data)
				newPastPurchases.save()
			InBasket.delete()
		except:
			return None
		else:
			return newUserOrder

class PastPurchases(models.Model):

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		on_delete=models.CASCADE)
	item = models.ForeignKey(
		Item, 
		on_delete=models.CASCADE)
	order = models.ForeignKey(
		UserOrder, 
		on_delete=models.CASCADE)	
	price = models.DecimalField(
		verbose_name='цена',
		max_digits=8,
		decimal_places=2, 
		default = 0,
		blank=0)
	quantity = models.DecimalField(
		verbose_name='количество',
		max_digits=8,
		decimal_places=0, 
		blank=0)
	add_datetime = models.DateTimeField(
		verbose_name='дата/время покупки',
		auto_now_add=True)

	def __str__(self):
		return f'{self.add_datetime}: {self.user.username}. {self.item.name} (price = {self.price}, quantity={self.quantity}'	

	class Meta():
		ordering = ['-add_datetime','user']


	