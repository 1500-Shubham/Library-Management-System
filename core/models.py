from django.db import models
import uuid
from .exceptions import *
from django.core.exceptions import *
#import pdb; pdb.set_trace()

class BaseModel(models.Model):
	STATUS = (
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('D', 'Deleted'),
    )
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=1, choices=STATUS,default='I')

	class Meta:
		abstract = True

class LanguageManager(models.Manager):
	#returns query set of objects of languages that matches with languages_list values
	def get_queryset_objects(self,lan_list):
		query_obj=[]
		for lan in lan_list:
			try:
				query_obj.append(Language.objects.get(name=lan.lower()))
			except:
				raise ObjectDoesNotExist("Language with " +lan+ " name does not exist")
				
		return query_obj

class Language(BaseModel):
	#readonly_fields=('language_id')
	language_id = models.UUIDField(primary_key=True, default = uuid.uuid4,editable = False)
	name = models.CharField(max_length=100,unique=True)
	script = models.CharField(max_length=100,null=True,blank=True)
	about = models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return self.name

	def as_dict(self):
		return {
				'language_id': self.language_id,
				'name':self.name,
				'scripts':self.script,
				'about':self.about,
			}
	objects = LanguageManager()

class AuthorManager(models.Manager):
	#returns query set of objects of author that matches with author_list values
	def get_queryset_objects(self,author_list):
		query_obj=[]
		for ath in author_list:
			try:
				print("hiii")
				query_obj.append(Author.objects.get(name=ath.lower()))
			except:
				raise ObjectDoesNotExist("Author with " +ath+ " name does not exist")
		return query_obj

class Author(BaseModel):
	readonly_fields=('author_id')
	author_id = models.UUIDField(primary_key=True, default = uuid.uuid4,editable = False)
	name = models.CharField(max_length=100,unique=True)
	description = models.CharField(max_length=100,null=True,blank=True)
	meta_data = models.JSONField(null=True,blank=True)

	def __str__(self):
		return self.name

	def as_dict(self):
		return  {
		'author_id':self.author_id,
		'name':self.name,
		'description':self.description,
		'meta_data':self.meta_data,
		}
	objects = AuthorManager()
	
class Publisher(BaseModel):
	readonly_fields=('publisher_id')
	publisher_id = models.UUIDField(primary_key=True, default = uuid.uuid4,editable = False)
	name = models.CharField(max_length=100,unique=True)
	meta_data = models.JSONField(null=True,blank=True)

	def __str__(self):
		return self.name

	def as_dict(self):
		return{
		'publisher_id':self.publisher_id,
		'name':self.name,
		'meta_data':self.meta_data,
		}

class BookManager(models.Manager):
	def get_queryset_objects(self,book_list):
		query_obj=[]
		for book in book_list:
			try:
				query_obj.append(Book.objects.get(book_id=book))
			except:
				raise ObjectDoesNotExist("Book with ID: " +book+ " does not exist")
		return query_obj

class Book(BaseModel):
	BOOK_TYPE = (
        (True, 'Ebook is present'),
        (False, 'Ebook is not present')
    )
	readonly_fields=('book_id')
	book_id = models.UUIDField(primary_key=True, default = uuid.uuid4,editable = False)
	name = models.CharField(max_length=100)
	language = models.ManyToManyField(Language)
	author = models.ManyToManyField(Author)
	publisher = models.ForeignKey(Publisher,on_delete=models.CASCADE)
	extra_details = models.JSONField(null=True,blank=True)
	book_type = models.BooleanField(choices=BOOK_TYPE,null=True,blank=True)

	def __str__(self):
		return self.name
	
	def as_dict(self):
		return{
		'book_id':self.book_id,
		'name':self.name,
		'language':[language.as_dict() for language in self.language.all()],
		'author':[author.as_dict() for author in self.author.all()],
		'publisher':self.publisher.as_dict(),
		'extra_details':self.extra_details,
		'book_type':self.book_type,
		}
	objects = BookManager()

class EBook(models.Model):
	readonly_fields=('ebook_id')
	ebook_id = models.UUIDField(primary_key=True, default = uuid.uuid4,editable = False)
	book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="ebook")
	book_location = models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return str(self.ebook_id)

	def as_dict(self):

		return{
		'ebook_id':self.ebook_id,
		'book':self.book.as_dict(),
		'book_location':self.book_location,
		}

class User(BaseModel):
	USER_ROLE = (
        ('S', 'SuperAdmin'),
        ('L', 'Librarian'),
        ('U', 'User'),
    )
	readonly_fields=('user_id')
	user_id = models.UUIDField(primary_key=True, default = uuid.uuid4,editable = False)
	first_name = models.CharField(max_length=100)
	middle_name = models.CharField(max_length=100,null=True,blank=True)
	last_name = models.CharField(max_length=100,null=True,blank=True)
	mobile = models.CharField(max_length=10)
	email_id = models.EmailField(max_length = 100,unique=True)
	meta_data = models.JSONField(null=True,blank=True)
	subscription = models.BooleanField(default=False)
	favourited = models.ManyToManyField(Book)
	role = models.CharField(max_length=1, choices=USER_ROLE,default='U')

	def __str__(self):
		return self.first_name

	def as_dict(self):	
		return{
		'role':self.get_role_display(),
		'user_id':self.user_id,
		'first_name':self.first_name,
		'middle_name':self.middle_name,
		'last_name':self.last_name,
		'mobile':self.mobile,
		'email_id':self.email_id,
		'meta_data':self.meta_data,
		'subscription':self.subscription,
		'favourited':[book.as_dict() for book in self.favourited.all()],
		}

class HardCopy(models.Model):
	readonly_fields=('hard_copy_id')
	hard_copy_id = models.UUIDField(primary_key=True, default = uuid.uuid4,editable = False)
	book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
	is_lent = models.BooleanField(default=False)
	lent_to = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

	def __str__(self):
		return str(self.hard_copy_id)
		
	def as_dict(self):
		lent_to=None
		if self.lent_to:
			lent_to=self.lent_to.as_dict()
		return{
		'book_id':self.book_id.as_dict(),
		'hard_copy_id':self.hard_copy_id,
		'is_lent':self.is_lent,
		'lent_to':lent_to,
		}










