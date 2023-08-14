import argparse
import os, sys
import json
sys.path.insert(0,'..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'geekshop.settings'

import django
from django.core.files.images import ImageFile
django.setup()
#from django.contrib.auth.models import User

from mainapp.models import ItemCategory,Item,Full_description,Price,Quantity,ParentCategory
from geekshop import settings

class loadData():

	def loadData(self):
		if self.filename is None:
			raise ValueError('filename error')
			return

		with open(self.filename) as f:
			vendor_codes = json.load(f)

		for code in vendor_codes:
			data_ = vendor_codes[code]
			data_ItemCategory = data_.copy()
			category = ItemCategory.objects.filter(parent_name__idx = data_['category'][0], idx = data_['category'][1])[0]
			data_ItemCategory['category'] = category
			try:
				data_ItemCategory['img_big'] = ImageFile(open(data_['img_big'] , "rb"))
				data_ItemCategory['img_small'] = ImageFile(open(data_['img_small'] , "rb"))
			except:
				pass
				continue
			data_ItemCategory.pop('price')
			data_ItemCategory.pop('price_unit')
			data_ItemCategory.pop('description')
			data_ItemCategory.pop('quantity')
			newitem = Item.objects.create(**data_ItemCategory)
			newitem.save()

			data_Full_description = {
				'item':newitem,
				'description':data_['description']
			}
			newfull_description = Full_description.objects.create(**data_Full_description)
			newfull_description.save()			
			
			data_Price = {
				'vendor_code':data_['vendor_code'],
				'price':data_['price'],
				'price_unit':data_['price_unit'],
			}
			newprice = Price.objects.create(**data_Price)
			newprice.save()			

			data_Quantity = {
				'vendor_code':data_['vendor_code'],
				'quantity':data_['quantity'],
			}
			newquantity = Quantity.objects.create(**data_Quantity)
			newquantity.save()	
		

	def __init__(self,filename=None):
		self.filename = filename
		self.loadData()

	@staticmethod
	def argParse():

		parser = argparse.ArgumentParser(prog='sort CSV', description='Parsing settings...')
		parser.add_argument("filename", type = str, nargs='+', help ="filename, str")	

		args = parser.parse_args()
		filename = args.filename[1]
		return loadData(filename)	

class loadCategory():

	def loadCategory(self):
		if self.filename is None:
			raise ValueError('filename error')
			return

		with open(self.filename) as f:
			category_tree = json.load(f)

		ParentCategorys = category_tree['ParentCategory']
		for item in ParentCategorys:
			newitem = ParentCategory.objects.create(**item)	
			newitem.save()

		ItemCategorys = category_tree['ItemCategory']
		for item in ItemCategorys:
			newitem = ItemCategory.objects.create(**item)	
			newitem.save()

	def __init__(self,filename=None):
		self.filename = filename
		self.loadCategory()

#loadData().argParse()
#loadCategory('category.json')
loadData('items_28032018.json')
