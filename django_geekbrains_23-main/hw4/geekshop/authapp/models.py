from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist

class ShopUser(AbstractUser):
	
	sex_choices = (
		('1', 'мужчина'),
		('2', 'женщина'),
		('3', 'гик'),)

	avatar = models.ImageField(
		verbose_name = 'аватар',
		upload_to=settings.AVATAR_DIR,
		blank=True)
	sex = models.CharField(
		verbose_name = 'пол',
		max_length=1,
		choices=sex_choices,
		default = '3',
		blank=False)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		newUserEmail = UserEmail.get_obj_by_username(self)
		if not newUserEmail:
			print('not_find {}'.format(self))
			data = {
			'user':self,
			'email':self.email
			}
			newUserEmail = UserEmail.objects.create(**data)
		else:
			print('not_find {}'.format(self))
			newUserEmail.email = self.email
		newUserEmail.save()

class UserEmail(models.Model):

	@staticmethod
	def get_username_by_email(email):
		try:
			obj = UserEmail.objects.get(email=email)
			return obj.user.username
		except ObjectDoesNotExist:
			return ''

	@staticmethod
	def get_obj_by_username(user):
		try:
			return UserEmail.objects.get(user=user)
		except ObjectDoesNotExist:
			return ''

	def __str__(self):
		return f'{self.user.username}. email = {self.email}'	

	user = models.ForeignKey(
		ShopUser,
		on_delete = models.CASCADE)
	email = models.EmailField(
		verbose_name='email address')