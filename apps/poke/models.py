from __future__ import unicode_literals
from django.db import models
from django.db.models import F
import re, bcrypt

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
	def register(self, data):
		errors = []
		if len(data['first_name']) < 2 or len(data['name']) < 2:
			errors.append("Name and/or alias must be longer than two characters.")
		if not email_regex.match(data['email']):
			errors.append("Valid email is required.")
		if len(data['password']) < 8 or data['password'] != data['confirmpassword']:
			errors.append("Passwords must match and be at least 8 characters.")
		
		response = {}

		if errors:
			response["registered"] = False
			response["errors"] = errors
		else:
			hashpassword = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt() )
			user = self.create(name = data['name'], alias = data['first_name'], email = data['email'], password = hashpassword, date_of_birth = data['date'])
			response["registered"] = True
			response["user"] = user
		return response

	def login(self, data):
		user = User.objects.filter(email=data['email'])
		if not user:
			return False
		else:
			user = user[0]
		if bcrypt.hashpw(data['password'].encode(), user.password.encode()) == user.password.encode():
			return user
		else:
			return False
	def pokeupdate(self, data):
		counter = User.objects.filter(id =data).update(poke_count = F('poke_count')+1)
		print counter
		

class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=50)
	date_of_birth = models.DateTimeField(auto_now_add=False)
	poke_count = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	objects = UserManager()

	