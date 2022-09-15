from cProfile import label
from re import U
from turtle import pd
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from .responses import *
from .exceptions import *
from django.core.exceptions import *
from .constants import *
import json

class LanguageViews(View):
	def __init__(self):
		self.response=init_response()

	def validate_schema(self, params, required_key=['name']):
		keys = params.keys()
		key_len = 0
		for key in required_key:
			if key in keys:
				key_len += 1
		if len(required_key) != key_len:
			raise ValidationError("Invalid data")

	def get(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			name=params.get('name')
			if name :
				self.validate_schema(params)
				if Language.objects.get(name=name.lower()):
					self.response['res_data']=Language.objects.get(name=params.get('name').lower()).as_dict()
				else:
					raise ObjectDoesNotExist("Requested language does not exist")
			else:
				res={}
				count=0
				lan=Language.objects.all()
				for item in lan:
					res[item.name]=item.as_dict()
					count=count+1
					if count >= LIMIT :
						break
				self.response['res_data']=res

			return send_200(self.response)
		
		except ValidationError as ex:
			self.response['res_str'] = str(ex)
			
		except ObjectDoesNotExist as e:
			self.response['Error Msg']=str(e)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)
			
	def post(self, request, *args, **kwargs):
		try:
			#import pdb; pdb.set_trace()
			params=request.POST.dict()
			self.validate_schema(params) #checks if name toh hai hi na

			name = params.get('name').lower()

			if Language.objects.filter(name=name).exists():
				raise ObjectAlreadyExist("Language with this name already exist")
			
			script = params.get('script')
			about = params.get('about')
			language_obj = Language.objects.create(name=name,script=script,about=about)
			language_obj.status='A'
			language_obj.save()
			self.response['res_data'] = language_obj.as_dict()
			self.response['res_str'] = "Language Successfully Created"
			return send_201(self.response)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)
		
		except ObjectAlreadyExist as ex:
			self.response['res_str'] = str(ex)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)
			
	def delete(self, request, *args, **kwargs):
		#import pdb; pdb.set_trace()
		try:
			params=request.GET.dict()
			self.validate_schema(params)
			name = params.get('name').lower()

			if Language.objects.filter(name=name).exists():
				language_obj=Language.objects.get(name=name)
				language_obj.status='D'
				language_obj.save()
				self.response['res_data'] = language_obj.as_dict()
				self.response['res_str'] = "Language Status Changed To Deleted"
				return send_201(self.response)

			else:
				raise ObjectDoesNotExist("Language not found")
			
		except ValidationError as ex:
			self.response['res_str'] = str(ex)

		except ObjectDoesNotExist as e:
			self.response['Error Msg']=str(e)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_404(self.response)
	
	def put (self, request, *args, **kwargs):
		try:
			#import pdb; pdb.set_trace()
			params=request.GET.dict()
			self.validate_schema(params) #checks if name toh hai hi na

			name = params.get('name').lower()

			if not Language.objects.filter(name=name).exists():
				raise ObjectDoesNotExist("Requested language does not exist")
			
			script = params.get('script')
			about = params.get('about')
			language_obj = Language.objects.get(name=name)

			language_obj.script=script
			language_obj.about=about
			language_obj.save()
			self.response['res_data'] = language_obj.as_dict()
			self.response['res_str'] = "Language Updated Successfully"
			return send_201(self.response)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)
		
class AuthorViews(View):

	def __init__(self):
		self.response=init_response()

	def validate_schema(self, params, required_key=['name']):

		keys = params.keys()
		key_len = 0
		for key in required_key:
			if key in keys:
				key_len += 1
		if len(required_key) != key_len:
			raise ValidationError("Invalid data")

	def is_json(self,myjson):
		try:
			json.loads(myjson)
		except ValueError as e:
			return False
		return True

	def get(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			name=params.get('name')
			limit=params.get('limit',LIMIT)
			offset=params.get('offset',OFFSET)
			if name :
				#self.validate_schema(params)
				if Author.objects.filter(name=name.lower()).exists():
					self.response['res_data']=Author.objects.get(name=params.get('name').lower()).as_dict()
				else:
					raise ObjectDoesNotExist("Requested Author does not exist")

			else:
			
				ath=Author.objects.all()
				res={}
				count=0
				for item in ath:
					res[item.name]=item.as_dict()
					count=count+1
					if count >=limit :
						break
				self.response['res_data']=res

			return send_200(self.response)
		
		except ValidationError as ex:
			self.response['res_str'] = str(ex)
			
		except ObjectDoesNotExist as e:
			self.response['Error Msg']=str(e)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)

	def post(self, request, *args, **kwargs):
		try:
			#import pdb; pdb.set_trace()
			params=request.POST.dict()
			self.validate_schema(params) 
			name = params.get('name').lower()
			description = params.get('description')
			meta_data = params.get('meta_data')

			if Author.objects.filter(name=name).exists():
				raise ObjectAlreadyExist("Language with this name already exist")

			if meta_data and not self.is_json(meta_data):
				raise ValueError("meta-data is not in JSON form")

			author_obj = Author.objects.create(name=name,meta_data=meta_data,description=description)
			author_obj.status='A'
			author_obj.save()
			self.response['res_data'] = author_obj.as_dict()
			self.response['res_str'] = "Author Successfully Created"
			return send_201(self.response)

		except ValueError as ex:
			self.response['res_str']= str(ex)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)
		
		except ObjectAlreadyExist as ex:
			self.response['res_str'] = str(ex)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)
	def delete(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			self.validate_schema(params)
			name = params.get('name').lower()

			if Author.objects.filter(name=name).exists():
				auth_obj=Author.objects.get(name=name)
				res=auth_obj.as_dict()
				auth_obj.status='D'
				auth_obj.save()
				self.response['res_data'] = res
				self.response['res_str'] = "Author Deleted Successfully"
				return send_201(self.response)

			else:
				raise ObjectDoesNotExist("Author not found")
			
		except ValidationError as ex:
			self.response['res_str'] = str(ex)

		except ObjectDoesNotExist as e:
			self.response['Error Msg']=str(e)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_404(self.response)
	
	def put (self, request, *args, **kwargs):
		try:
			#import pdb; pdb.set_trace()
			params=request.GET.dict()
			self.validate_schema(params) #checks if name toh hai hi na

			name = params.get('name').lower()

			if not Author.objects.filter(name=name).exists():
				raise ObjectDoesNotExist("Requested author does not exist")
			
			description = params.get('description')
			meta_data = params.get('meta_data')

			if meta_data and not self.is_json(meta_data):
				raise ValueError("meta-data is not in JSON form")

			author_obj = Author.objects.get(name=name)
			author_obj.description=description
			author_obj.meta_data=meta_data
			author_obj.save()
			self.response['res_data'] = author_obj.as_dict()
			self.response['res_str'] = "Author Updated Successfully"
			return send_201(self.response)

		except ObjectDoesNotExist as ex:
			self.response['res_str'] = str(ex)
		
		except ValueError as ex:
			self.response['res_str']= str(ex)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)	

class PublisherViews(View):
	def __init__(self):
		self.response=init_response()
	
	def validate_schema(self, params, required_key=['name']):

		keys = params.keys()
		key_len = 0
		for key in required_key:
			if key in keys:
				key_len += 1
		if len(required_key) != key_len:
			raise ValidationError("Invalid data")

	def is_json(self,myjson):
		try:
			json.loads(myjson)
		except ValueError as e:
			return False
		return True

	def get(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			name=params.get('name')
			if name :
				self.validate_schema(params)
				if Publisher.objects.filter(name=name.lower()).exists():
					self.response['res_data']=Publisher.objects.get(name=params.get('name').lower()).as_dict()
				else:
					raise ObjectDoesNotExist("Requested Publisher does not exist")

			else:
				limit=5
				ath=Publisher.objects.all()
				res={}
				count=0
				for item in ath:
					res[item.name]=item.as_dict()
					count=count+1
					if count >=limit :
						break
				self.response['res_data']=res

			return send_200(self.response)
		
		except ValidationError as ex:
			self.response['res_str'] = str(ex)
			
		except ObjectDoesNotExist as e:
			self.response['Error Msg']=str(e)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)

	def post(self, request, *args, **kwargs):
		try:
			params=request.POST.dict()
			self.validate_schema(params) 
			name = params.get('name').lower()
			meta_data = params.get('meta_data')

			if Publisher.objects.filter(name=name).exists():
				raise ObjectAlreadyExist("Language with this name already exist")

			if meta_data and not self.is_json(meta_data):
				raise ValueError("meta-data is not in JSON form")

			pub_obj = Publisher.objects.create(name=name,meta_data=meta_data)
			pub_obj.status='A'
			pub_obj.save()
			self.response['res_data'] = pub_obj.as_dict()
			self.response['res_str'] = "Publisher Successfully Created"
			return send_201(self.response)

		except ValueError as ex:
			self.response['res_str']= str(ex)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)
		
		except ObjectAlreadyExist as ex:
			self.response['res_str'] = str(ex)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)

	def delete(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			self.validate_schema(params)
			name = params.get('name').lower()

			if Publisher.objects.filter(name=name).exists():
				pub_obj=Publisher.objects.get(name=name)
				res=pub_obj.as_dict()
				pub_obj.delete()
				pub_obj.save()
				self.response['res_data'] = res
				self.response['res_str'] = "Publisher Deleted Successfully"
				return send_201(self.response)

			else:
				raise ObjectDoesNotExist("Publisher not found")
			
		except ValidationError as ex:
			self.response['res_str'] = str(ex)

		except ObjectDoesNotExist as e:
			self.response['Error Msg']=str(e)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_404(self.response)

	def put (self, request, *args, **kwargs):
		try:
			#import pdb; pdb.set_trace()
			params=request.GET.dict()
			self.validate_schema(params) #checks if name toh hai hi na

			name = params.get('name').lower()

			if not Publisher.objects.filter(name=name).exists():
				raise ObjectDoesNotExist("Requested author does not exist")
	
			meta_data = params.get('meta_data')

			if meta_data and not self.is_json(meta_data):
				raise ValueError("meta-data is not in JSON form")

			pub_obj = Publisher.objects.get(name=name)
			pub_obj.meta_data=meta_data
			pub_obj.save()
			self.response['res_data'] = pub_obj.as_dict()
			self.response['res_str'] = "Publisher Updated Successfully"
			return send_201(self.response)

		except ObjectDoesNotExist as ex:
			self.response['res_str'] = str(ex)
		
		except ValueError as ex:
			self.response['res_str']= str(ex)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)

class BookViews(View):
	def __init__(self):
		self.response=init_response()

	def validate_schema(self, params, required_key=['name']):

		keys = params.keys()
		key_len = 0
		for key in required_key:
			if key in keys:
				key_len += 1
		if len(required_key) != key_len:
			raise ValidationError("Invalid Data")
	
	def is_json(self,myjson):
		try:
			json.loads(myjson)
		except ValueError as e:
			return False
		return True
	
	def get(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			book_id=params.get('book_id')
			if book_id :
				if Book.objects.filter(book_id=book_id).exists():
					self.response['res_data']=Book.objects.get(book_id=book_id).as_dict()
				else:
					raise ObjectDoesNotExist("Requested BOOK does not exist")
			elif params.get('name'):
				if Book.objects.filter(name=params.get('name').lower()).exists():
					res=[book.as_dict() for book in Book.objects.filter(name=params.get('name').lower())]
					self.response['res_data']=res
				else:
					raise ObjectDoesNotExist("Requested BOOK does not exist")
			else:
				limit=5
				ath=Book.objects.all()
				res={}
				count=0
				for item in ath:
					res[item.name]=item.as_dict()
					count=count+1
					if count >=limit :
						break
				self.response['res_data']=res

			return send_200(self.response)
		except ValidationError as ex:
			self.response['res_str'] = str(ex)
			
		except ObjectDoesNotExist as e:
			self.response['Error Msg']=str(e)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)
	
	def post(self, request, *args, **kwargs):
		try:
			#import pdb; pdb.set_trace()
			params=request.POST.dict()
			self.validate_schema(params,['name','author','publisher','language'])
			name = params.get('name').lower()

			author_name = params.get('author') #can be list multiple atlease one create
			author_list=[auth.strip() for auth in author_name.split(',')]

			if(len(author_list)==0):
				raise ValidationError("Need at least one author")
			
			language=params.get('language')
			lan_list=[_lang.strip() for _lang in language.split(',')]

			if(len(lan_list)==0):
				raise ValidationError("Need at least one language")

			publisher_name = params.get('publisher')
			if not Publisher.objects.filter(name=publisher_name.lower()).exists():
				raise ObjectDoesNotExist("Publisher with "+publisher_name + " name not exist")
			publisher_obj=Publisher.objects.get(name=publisher_name.lower())
			

			extra_details = params.get('extra_details')
			if extra_details and not self.is_json(extra_details):
				raise ValueError("extra_details is not in JSON form")

			book_type = None
			book_param=params.get('book_type')
			if book_param and book_param.lower()=='true':
				book_type=True
			elif book_param and book_param.lower()=='false':
				book_type=False

			book_obj = Book.objects.create(name=name,publisher=publisher_obj,book_type=book_type,extra_details=extra_details)
			book_obj.status='A'
			for ath in author_list:
				if not Author.objects.filter(name=ath.lower()).exists():
					raise ObjectDoesNotExist("Author with " +ath+ " name does not exist")
				else:
					book_obj.author.add(Author.objects.get(name=ath.lower()))
			for lan in lan_list:
				if not Language.objects.filter(name=lan.lower()).exists():
					raise ObjectDoesNotExist("Language with " +lan+ " name does not exist")
				else:
					book_obj.language.add(Language.objects.get(name=lan.lower()))
			book_obj.save()
			self.response['res_data'] = book_obj.as_dict()
			self.response['res_str'] = "Book Successfully Created"
			return send_201(self.response)

		except ObjectDoesNotExist as ex:
			self.response['res_str'] = str(ex)
		
		except ValueError as ex:
			self.response['res_str']= str(ex)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)

	def delete(self, request, *args, **kwargs):

		try:
			params=request.GET.dict()
			self.validate_schema(params,['book_id'])
			book_id = params.get('book_id')
			if not Book.objects.filter(book_id=book_id).exists():
				raise ObjectDoesNotExist("Requested BOOK does not exist")

			book_obj=Book.objects.get(book_id=book_id)
			res=book_obj.as_dict()
			book_obj.status='D'
			book_obj.save()
			self.response['res_data'] = res
			self.response['res_str'] = "Book Status Change to Deleted Successfully"
			return send_201(self.response)

		except ObjectDoesNotExist as ex:
			self.response['res_str'] = str(ex)
		
		except ValueError as ex:
			self.response['res_str']= str(ex)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)

		except Exception as e:
			self.response['res_str'] = "Something Went Wrong"

		return send_400(self.response)

	def put(self, request, *args, **kwargs):
		try:
			#import pdb; pdb.set_trace()
			params=request.GET.dict()
			self.validate_schema(params,['book_id'])
			book_id = params.get('book_id')
			if book_id and not Book.objects.filter(book_id=book_id).exists():
				raise ObjectDoesNotExist("Requested BOOK does not exist")
			#needed book_id
			book_obj=Book.objects.get(book_id=book_id)
		
			author_name = params.get('author') #can be list multiple 
			author_list=[]
			if author_name:
				author_list=[auth.strip() for auth in author_name.split(',')]
			
			language=params.get('language')
			lan_list=[]
			if language:
				lan_list=[_lang.strip() for _lang in language.split(',')]

			extra_details=book_obj.extra_details #by default
			extra_param = params.get('extra_details')
			if extra_param and not self.is_json(extra_param):
				raise ValueError("extra_details is not in JSON form")
			elif extra_param:
				extra_details=extra_param

			book_type = book_obj.book_type #by default 
			book_param=params.get('book_type')
			if book_param and book_param.lower()=='true':
				book_type=True
			elif book_param and book_param.lower()=='false':
				book_type=False

			book_obj.book_type=book_type
			book_obj.extra_details=extra_details

			for ath in author_list:
				if not Author.objects.filter(name=ath.lower()).exists():
					raise ObjectDoesNotExist("Author with " +ath+ " name does not exist")
				else:
					book_obj.author.add(Author.objects.get(name=ath.lower()))
			for lan in lan_list:
				if not Language.objects.filter(name=lan.lower()).exists():
					raise ObjectDoesNotExist("Language with " +lan+ " name does not exist")
				else:
					book_obj.language.add(Language.objects.get(name=lan.lower()))
			book_obj.save()
			self.response['res_data'] = book_obj.as_dict()
			self.response['res_str'] = "Book Updated Successfully"
			return send_201(self.response)

		except ObjectDoesNotExist as ex:
			self.response['res_str'] = str(ex)
		
		except ValueError as ex:
			self.response['res_str']= str(ex)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)

class EBookViews(View):
	def __init__(self):
		self.response=init_response()
	def validate_schema(self, params, required_key=['name'],msg=""):

		keys = params.keys()
		key_len = 0
		for key in required_key:
			if key in keys:
				key_len += 1
		if len(required_key) != key_len:
			raise ValidationError("Invalid Data "+msg)

	def get(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			limit=params.get('limit',LIMIT)
			offset=params.get('offset',OFFSET)
			if params.get('ebook_id'):
				if EBook.objects.filter(ebook_id=params.get('ebook_id')).exists():
					self.response['res_data']=EBook.objects.get(ebook_id=params.get('ebook_id')).as_dict()
				else:
					raise ObjectDoesNotExist("Requested Ebook does not exist")
			else:
				ebooks=EBook.objects.all()
				res={}
				for index in range(offset,limit):
					if index >= len(ebooks):
						break
					res[str(ebooks[index].ebook_id)]=ebooks[index].as_dict()
				self.response['res_data']=res

			return send_201(self.response)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)
			
		except ObjectDoesNotExist as e:
			self.response['Error Msg']=str(e)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)

	def post(self, request, *args, **kwargs):
		try:
			params=request.POST.dict() 
			self.validate_schema(params,['book_id'],"Mandatory Book Key is needed")
			if Book.objects.filter(book_id=params.get('book_id')).exists():
				book = Book.objects.get(book_id=params.get('book_id'))
			else:
				raise ObjectDoesNotExist("Book with given id doesnot exist "+params.get('book_id'))
			book_location = params.get('book_location')
			ebook_obj = EBook.objects.create( book=book, book_location=book_location)
			self.response['res_data'] = ebook_obj.as_dict()
			self.response['res_str'] = "EBook Successfully Created"
			return send_201(self.response)
		
		except ObjectDoesNotExist as ex:
			self.response['res_str'] = str(ex)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)

	def delete(self, request, *args, **kwargs):
		try:
			#import pdb; pdb.set_trace()
			params=request.GET.dict()
			self.validate_schema(params,['ebook_id'],"Ebook id is needed")
			if EBook.objects.filter(ebook_id=params.get('ebook_id')).exists():
				ebook_obj = EBook.objects.get(ebook_id=params.get('ebook_id'))
			else:
				raise ObjectDoesNotExist("EBook with given id doesnot exist "+params.get('ebook_id'))
			res=ebook_obj.as_dict()
			ebook_obj.delete()
			ebook_obj.save()
			self.response['res_data'] = res
			self.response['res_str'] = "EBook Deleted Successfully"
			return send_201(self.response)

		except ValueError as ex:
			self.response['res_str']= str(ex)

		except ObjectDoesNotExist as ex:
			self.response['res_str'] = str(ex)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)
		
		except Exception as e:
			self.response['res_data'] = e.msg
			self.response['res_str'] = "Something Went Wrong"
		return send_404(self.response)

	def put (self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			self.validate_schema(params,['ebook_id'],":Ebook id is needed")
			if EBook.objects.filter(ebook_id=params.get('ebook_id')).exists():
				ebook_obj = EBook.objects.get(ebook_id=params.get('ebook_id'))
			else:
				raise ObjectDoesNotExist("EBook with given id doesnot exist "+params.get('ebook_id'))
			ebook_obj.book_location=params.get('book_location')
			ebook_obj.save()
			res=ebook_obj.as_dict()
			self.response['res_data'] = res
			self.response['res_str'] = "EBook Location Updated Successfully"
			return send_201(self.response)

		except ObjectDoesNotExist as ex:
			self.response['res_str'] = str(ex)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)
		
		except Exception as e:
			self.response['res_data'] = e.msg
			self.response['res_str'] = "Something Went Wrong"
		return send_404(self.response)	

class UserViews(View):
	def __init__(self):
		self.response=init_response()
	
	def validate_schema(self, params, required_key=['name']):

		keys = params.keys()
		key_len = 0
		for key in required_key:
			if key in keys:
				key_len += 1
		if len(required_key) != key_len:
			raise ValidationError("Invalid data")

	def is_json(self,myjson):
		try:
			json.loads(myjson)
		except ValueError as e:
			return False
		return True

	def get(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			self.validate_schema(params,['email_id'])
			if not User.objects.filter(email_id=params.get('email_id')).exists():
				raise ValidationError("User with this email id does not exist")
			self.response['res_data']=User.objects.get(email_id=params.get('email_id')).as_dict()
			return send_201(self.response)
			
		except ValidationError as ex:
			self.response['res_str'] = str(ex)	
		
		except Exception as e:
			self.response['res_str'] = "Something Went Wrong"

		return send_404(self.response)
	
	def post(self, request, *args, **kwargs):
		try:
			#import pdb; pdb.set_trace()
			import re
			params=request.POST.dict()
			self.validate_schema(params,['first_name','mobile','email_id'])
			first_name = params.get('first_name').lower()
			middle_name = params.get('middle_name').lower()
			last_name = params.get('last_name').lower()
			mobile=params.get('mobile')

			email_id=params.get('email_id')
			regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
			if not re.fullmatch(regex, email_id):
				raise ValidationError("Email Id is not correct")
			if User.objects.filter(email_id=email_id).exists():
				raise ValidationError("Email Id Already Exist")
			
			meta_data = params.get('meta_data')
			if meta_data and not self.is_json(meta_data):
				raise ValueError("meta_data is not in JSON form")

			subscribed=False
			subscription=params.get('subscription')
			if subscription and subscription.lower()=='true':
				subscribed=True

			favourited = params.get('favourited') #can be empty
			fav_book=[]
			if favourited:
				fav_book=[book.strip() for book in favourited.split(',')]
		
			user_obj = User.objects.create(first_name=first_name,middle_name=middle_name,last_name=last_name,mobile=mobile,email_id=email_id,meta_data=meta_data,subscription=subscribed)
			user_obj.status='A'

			for book in fav_book:
				if not Book.objects.filter(book_id=book).exists():
					raise ObjectDoesNotExist("Book with ID: " +book+ " does not exist")
				else:
					user_obj.favourited.add(Book.objects.get(book_id=book))
			
			user_obj.save()
			self.response['res_data'] = user_obj.as_dict()
			self.response['res_str'] = "User Successfully Created"
			return send_201(self.response)

		except ObjectDoesNotExist as ex:
			self.response['res_str'] = str(ex)
		
		except ValueError as ex:
			self.response['res_str']= str(ex)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)

	def delete(self, request, *args, **kwargs):

		try:
			params=request.GET.dict()
			self.validate_schema(params,['email_id'])
			if not User.objects.filter(email_id=params.get('email_id')).exists():
				raise ValidationError("User with this email id doesnot exist")
			user_obj=User.objects.get(email_id=params.get('email_id'))
			user_obj.status='D'
			user_obj.save()
			self.response['res_data'] = user_obj.as_dict()
			self.response['res_str'] = "User Status Change To Deleted Successfully"
			return send_201(self.response)
			
		except ValidationError as ex:
			self.response['res_str'] = str(ex)	
		
		except Exception as e:
			self.response['res_str'] = "Something Went Wrong"
		
		return send_404(self.response)

	def put (self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			self.validate_schema(params,['email_id'])
			if not User.objects.filter(email_id=params.get('email_id')).exists():
				raise ValidationError("User with this email id doesnot exist")
			user_obj=User.objects.get(email_id=params.get('email_id'))
			mobile=params.get('mobile')
			meta_data = params.get('meta_data')
			if meta_data and not self.is_json(meta_data):
				raise ValueError("meta_data is not in JSON form")

			subscribed=False
			subscription=params.get('subscription')
			if subscription and subscription.lower()=='true':
				subscribed=True

			role=params.get('role')
			role_status='U'
			if role=='S':
				role_status='S'
			elif role=='L':
				role_status='L'

			user_obj.mobile=mobile
			user_obj.meta_data=meta_data
			user_obj.subscription=subscribed
			user_obj.role=role_status
			user_obj.save()
		
			self.response['res_data'] = user_obj.as_dict()
			self.response['res_str'] = "User Updated Successfully"
			return send_201(self.response)

		except ObjectDoesNotExist as ex:
			self.response['res_str'] = str(ex)
		
		except ValueError as ex:
			self.response['res_str']= str(ex)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)

class HardCopyViews(View):
	def __init__(self):
		self.response=init_response()
	
	def validate_schema(self, params, required_key=['name']):

		keys = params.keys()
		key_len = 0
		for key in required_key:
			if key in keys:
				key_len += 1
		if len(required_key) != key_len:
			raise ValidationError("Invalid data")


	def get(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			self.validate_schema(params,['hard_copy_id'])
			hard_copy_id=params.get('hard_copy_id')
			if HardCopy.objects.filter(hard_copy_id=hard_copy_id).exists():
					self.response['res_data']=HardCopy.objects.get(hard_copy_id=hard_copy_id).as_dict()
			else:
				raise ObjectDoesNotExist("Requested HardCopy does not exist")

			return send_201(self.response)
				
		except ValidationError as ex:
			self.response['res_str'] = str(ex)
			
		except ObjectDoesNotExist as e:
			self.response['Error Msg']=str(e)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)
	
	def post(self, request, *args, **kwargs):
		try:
			#import pdb; pdb.set_trace()
			params=request.POST.dict()
			self.validate_schema(params,['book_id'])
			book_id = params.get('book_id')
			if not Book.objects.filter(book_id=book_id).exists():
				raise ObjectDoesNotExist("Book with this"+str(book_id)+"does not exist")
			book_obj=Book.objects.get(book_id=book_id)

			is_lent=False
			lent=params.get('is_lent')
			if lent and lent.lower()=='true':
				is_lent=True
			
			lent_to=params.get('lent_to')
			user_obj=None
			if lent_to and User.objects.filter(email_id=lent_to).exists():
				user_obj=User.objects.get(email_id=lent_to)

			hardcopy_obj = HardCopy.objects.create( book_id=book_obj, is_lent=is_lent,lent_to=user_obj)

			self.response['res_data'] = hardcopy_obj.as_dict()
			self.response['res_str'] = "HardCopy Successfully Created"

			return send_201(self.response)
		
		except ValidationError as ex:
			self.response['res_str'] = str(ex)

		except ObjectDoesNotExist as ex:
			self.response['res_str'] = str(ex)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)

	def delete(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			self.validate_schema(params,['hard_copy_id'])
			hard_copy_id=params.get('hard_copy_id')
			if not HardCopy.objects.filter(hard_copy_id=hard_copy_id).exists():
				raise ObjectDoesNotExist("Requested HardCopy does not exist")

			hardcopy_obj=HardCopy.objects.get(hard_copy_id=hard_copy_id)
			self.response['res_data'] = hardcopy_obj.as_dict()
			hardcopy_obj.delete()
			hardcopy_obj.save()
			self.response['res_str'] = "HardCopy Deleted Successfully"
			return send_201(self.response)
				
		except ValidationError as ex:
			self.response['res_str'] = str(ex)
			
		except ObjectDoesNotExist as e:
			self.response['Error Msg']=str(e)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)

	def put (self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			self.validate_schema(params,['hard_copy_id'])
			hard_copy_id=params.get('hard_copy_id')
			if not HardCopy.objects.filter(hard_copy_id=hard_copy_id).exists():
				raise ObjectDoesNotExist("Requested HardCopy does not exist")
			hardcopy_obj=HardCopy.objects.get(hard_copy_id=hard_copy_id)

			is_lent=False
			lent=params.get('is_lent')
			if lent and lent.lower()=='true':
				is_lent=True

			lent_to=params.get('lent_to')
			user_obj=None
			if lent_to and not User.objects.filter(email_id=lent_to).exists():
				raise ObjectDoesNotExist("User with this "+str(lent_to)+" does not exist")
			elif lent_to:
				user_obj=User.objects.get(email_id=lent_to)
			
			hardcopy_obj.is_lent=is_lent
			hardcopy_obj.lent_to=user_obj
			hardcopy_obj.save()
			self.response['res_data'] = hardcopy_obj.as_dict()
			self.response['res_str'] = "HardCopy Updated Successfully"
	
			return send_201(self.response)

		except ObjectDoesNotExist as ex:
			self.response['res_str'] = str(ex)
		
		except ValueError as ex:
			self.response['res_str']= str(ex)

		except ValidationError as ex:
			self.response['res_str'] = str(ex)

		except Exception as e:
			self.response['Error Msg']="Something is Wrong"

		return send_400(self.response)


		






		


