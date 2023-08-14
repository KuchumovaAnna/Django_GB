from django.db import models
from django.conf import settings

#категории
class ParentCategory(models.Model):
	name = models.CharField(
		verbose_name = 'имя категории', 
		max_length=50,  
		blank=False)
	idx = models.PositiveIntegerField(
		default=0,
		unique=True)
	color = models.CharField(
		verbose_name = 'цвет категории', 
		max_length=6,
		default = '000000')

	def __str__(self):
		return f'{self.name}. idx = {self.idx}'	

	class Meta():
		ordering = ['idx']

#категории
class ItemCategory(models.Model):
	parent_name = models.ForeignKey(
		ParentCategory,
		on_delete=models.CASCADE)
	name = models.CharField(
		verbose_name = 'имя подкатегории', 
		max_length=50, 
		unique=True, 
		blank=False)
	idx = models.PositiveIntegerField(
		default=0)

	def __str__(self):
		return f'{self.parent_name} -> {self.name}. idx = {self.idx}'	

	class Meta():
		ordering = ['parent_name','idx']

#основное описание товара
class Item(models.Model):
	category = models.ForeignKey(
		ItemCategory, 
		on_delete=models.CASCADE)
	name = models.CharField(
		verbose_name = 'имя', 
		max_length=100, 
		unique=True, 
		blank=False)
	img_big = models.ImageField(
		verbose_name = 'изображение (большое)', 
		upload_to=settings.BIG_IMG_DIR,
		blank=True)
	img_small= models.ImageField(
		verbose_name = 'изображение (маленькое)', 
		upload_to=settings.PREVIEW_IMG_DIR,
		blank=True)
	short_desc = models.TextField(
		verbose_name = 'краткое описание', 
		blank=True)
	vendor_code = models.CharField(
		verbose_name = 'артикул', 
		max_length=25, 
		unique=True, 
		blank=False)
	price = models.DecimalField(
		verbose_name='цена',
		max_digits=8,
		decimal_places=2, 
		default = 0,
		blank=0)
	price_unit = models.CharField(
		verbose_name = 'валюта', 
		max_length=5,
		default = 'руб',
		blank=False)
	instock = models.BooleanField(default = False)

	def __str__(self):
		return '{},v_code-{}'.format(self.name,self.vendor_code)

	class Meta:
		indexes = [
			models.Index(fields=['vendor_code',]),
		]

	@property
	def find_last_price(self):
		try:			
			price_ = Price.objects.filter(vendor_code=self.vendor_code)[0]
			return price_
		except:
			price_ = None
		return price_

	@staticmethod
	def find_item_by_vendor_code(vendor_code):
		try: 
			item = Item.objects.get(vendor_code=vendor_code)
		except ObjectDoesNotExist:
			item = None
		return item

#тполное описание товара
class Full_description(models.Model):
	item = models.ForeignKey(
		Item, 
		on_delete=models.CASCADE)
	description = models.TextField(
		verbose_name = 'полное описание', 
		blank=False)

#отдельная таблица с ценами товаров. связь идет по артикулу. 
#фактически не связана с таблицей товаров item. 
#необходимо для отдельной загрузки цен из прайс листов на дату по артикулу
class Price(models.Model):
	vendor_code = models.CharField(
		verbose_name = 'артикул', 
		max_length=25, 
		unique=True)
	price = models.DecimalField(
		verbose_name='цена',
		max_digits=8,
		decimal_places=2, 
		blank=0)
	price_unit = models.CharField(
		verbose_name = 'валюта', 
		max_length=5, 
		blank=False)
	date = models.DateField(
		verbose_name='дата присвоения цены',
		auto_now_add=True)

	class Meta():
		ordering = ['-date']
		unique_together = ("vendor_code", "date")
		indexes = [
			models.Index(fields=['vendor_code',]),
		]

#отдельная таблица с количеством товаров. связь идет по артикулу. 
#фактически не связана с таблицей товаров item. 
#необходимо для отдельной загрузки остатков на дату по артикулу
#так же зависима от проданых товаров. Количество изменяется в момет окончания оформления покупки
class Quantity(models.Model):
	vendor_code = models.CharField(
		verbose_name = 'артикул', 
		max_length=25, 
		unique=True)
	quantity = models.DecimalField(
		verbose_name='количество',
		max_digits=8,
		decimal_places=0, 
		blank=0)
	datetime = models.TimeField(
		verbose_name='дата и время изменения количества',
		auto_now_add=True)

	class Meta():
		ordering = ['-datetime']
		unique_together = ("vendor_code", "datetime")
		indexes = [
			models.Index(fields=['vendor_code',]),
		]
