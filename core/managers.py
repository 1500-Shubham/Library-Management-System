from django.db import models
from .exceptions import *
from django.core.exceptions import *

class LanguageManager(models.Manager):
	#returns query set of objects of languages that matches with languages_list values
	def get_queryset_objects(self,lan_list):
		query_obj=[]
		for lan in lan_list:
			try:
				query_obj.append(self.get(name=lan.lower()))
			except:
				raise ObjectDoesNotExist("Language with " +lan+ " name does not exist")
				
		return query_obj

class AuthorManager(models.Manager):
	def get_queryset_objects(self,author_list):
		query_obj=[]
		for ath in author_list:
			try:
				print("hiii")
				query_obj.append(self.get(name=ath.lower()))
			except:
				raise ObjectDoesNotExist("Author with " +ath+ " name does not exist")
		return query_obj

class BookManager(models.Manager):
	def get_queryset_objects(self,book_list):
		query_obj=[]
		for book in book_list:
			try:
				query_obj.append(self.get(book_id=book))
			except:
				raise ObjectDoesNotExist("Book with ID: " +book+ " does not exist")
		return query_obj
