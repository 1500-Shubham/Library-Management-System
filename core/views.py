from .models import *
from django.views import View
from .responses import *
from .exceptions import *
from django.core.exceptions import *
from .constants import *
from .utils import *

class LanguageViews(View):
	def __init__(self):
		self.response=init_response()

	def get(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			limit=params.get('limit',LIMIT)
			offset=params.get('offset',OFFSET)
			if params.get('name') :
				validate_schema(params)
				try:
					self.response['res_data']=Language.objects.get(name=params.get('name').lower()).as_dict()
				except:
					raise ObjectDoesNotExist("Requested language does not exist")
			else:
				res=[]
				lan=Language.objects.all()
				for index in range(offset,limit):
					if index >= len(lan):
						break
					res.append(lan[index].as_dict())	
				self.response['res_data']=res
			return send_200(self.response)
		
		except (ValidationError,ObjectDoesNotExist) as ex:
			self.response['res_str'] = str(ex)	
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)		
	
	def post(self, request, *args, **kwargs):
		try:
			params=request.POST.dict()
			validate_schema(params)
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

		except (ValidationError,ObjectDoesNotExist,ObjectAlreadyExist) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)
			
	def delete(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params)
			name = params.get('name').lower()
			try:
				language_obj=Language.objects.get(name=name)
				language_obj.status='D'
				language_obj.save()
				self.response['res_data'] = language_obj.as_dict()
				self.response['res_str'] = "Language Status Changed To Deleted"
				return send_201(self.response)
			except:
				raise ObjectDoesNotExist("Language not found")
			
		except (ValidationError,ObjectDoesNotExist) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_404(self.response)
	
	def put (self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params)
			try:
				language_obj = Language.objects.get(name=params.get('name').lower())	
				script = params.get('script')
				about = params.get('about')
				language_obj.script=script
				language_obj.about=about
				language_obj.save()
				self.response['res_data'] = language_obj.as_dict()
				self.response['res_str'] = "Language Updated Successfully"
			except:
				raise ObjectDoesNotExist("Requested language does not exist")
			return send_201(self.response)

		except (ValidationError,ObjectDoesNotExist) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)
		
class AuthorViews(View):
	def __init__(self):
		self.response=init_response()

	def get(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			name=params.get('name')
			limit=params.get('limit',LIMIT)
			offset=params.get('offset',OFFSET)
			if name :
				try:
					self.response['res_data']=Author.objects.get(name=params.get('name').lower()).as_dict()
				except:
					raise ObjectDoesNotExist("Requested Author does not exist")
			else:
				ath=Author.objects.all()
				res=[]
				for index in range(offset,limit):
					if index >= len(ath):
						break
					res.append(ath[index].as_dict())
				self.response['res_data']=res
			return send_200(self.response)
		
		except (ValidationError,ObjectDoesNotExist) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

	def post(self, request, *args, **kwargs):
		try:
			params=request.POST.dict()
			validate_schema(params) 
			name = params.get('name').lower()
			description = params.get('description')
			meta_data = params.get('meta_data')

			if Author.objects.filter(name=name).exists():
				raise ObjectAlreadyExist("Author with this name already exist")

			if meta_data and not is_json(meta_data):
				raise ValueError("meta-data is not in JSON form")

			author_obj = Author.objects.create(name=name,meta_data=meta_data,description=description)
			author_obj.status='A'
			author_obj.save()
			self.response['res_data'] = author_obj.as_dict()
			self.response['res_str'] = "Author Successfully Created"
			return send_201(self.response)

		except (ValidationError,ObjectDoesNotExist,ValueError,ObjectAlreadyExist) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

	def delete(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params)
			name = params.get('name').lower()
			try:
				auth_obj=Author.objects.get(name=name)
				res=auth_obj.as_dict()
				auth_obj.status='D'
				auth_obj.save()
				self.response['res_data'] = res
				self.response['res_str'] = "Author Deleted Successfully"
				return send_201(self.response)
			except:
				raise ObjectDoesNotExist("Author not found")
			
		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)
	
	def put (self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params) 
			name = params.get('name').lower()
			try:	
				author_obj = Author.objects.get(name=name)
				description = params.get('description')
				meta_data = params.get('meta_data')
				if meta_data and not is_json(meta_data):
					raise ValueError("meta-data is not in JSON form")
				author_obj.description=description
				author_obj.meta_data=meta_data
				author_obj.save()
				self.response['res_data'] = author_obj.as_dict()
				self.response['res_str'] = "Author Updated Successfully"
			except:
				raise ObjectDoesNotExist("Requested author does not exist")
			return send_201(self.response)

		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)	

class PublisherViews(View):
	def __init__(self):
		self.response=init_response()

	def get(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			name=params.get('name')
			limit=params.get('limit',LIMIT)
			offset=params.get('offset',OFFSET)
			if name :
				validate_schema(params)
				try:
					self.response['res_data']=Publisher.objects.get(name=params.get('name').lower()).as_dict()
				except:
					raise ObjectDoesNotExist("Requested Publisher does not exist")
			else:
				pub=Publisher.objects.all()
				res=[]
				for index in range(offset,limit):
					if index >= len(pub):
						break
					res.append(pub[index].as_dict())
				self.response['res_data']=res
			return send_200(self.response)
		
		except (ValidationError,ObjectDoesNotExist,ValueError,ObjectAlreadyExist) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

	def post(self, request, *args, **kwargs):
		try:
			params=request.POST.dict()
			validate_schema(params) 
			name = params.get('name').lower()
			meta_data = params.get('meta_data')

			if Publisher.objects.filter(name=name).exists():
				raise ObjectAlreadyExist("Publisher with this name already exist")

			if meta_data and not is_json(meta_data):
				raise ValueError("meta-data is not in JSON form")

			pub_obj = Publisher.objects.create(name=name,meta_data=meta_data)
			pub_obj.status='A'
			pub_obj.save()
			self.response['res_data'] = pub_obj.as_dict()
			self.response['res_str'] = "Publisher Successfully Created"
			return send_201(self.response)

		except (ValidationError,ObjectDoesNotExist,ValueError,ObjectAlreadyExist) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

	def delete(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params)
			name = params.get('name').lower()
			try:
				pub_obj=Publisher.objects.get(name=name)
				res=pub_obj.as_dict()
				pub_obj.delete()
				pub_obj.save()
				self.response['res_data'] = res
				self.response['res_str'] = "Publisher Deleted Successfully"
				return send_201(self.response)
			except:
				raise ObjectDoesNotExist("Publisher not found")
			
		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

	def put (self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params)
			name = params.get('name').lower()
			if not Publisher.objects.filter(name=name).exists():
				raise ObjectDoesNotExist("Requested Publisher does not exist")
			meta_data = params.get('meta_data')
			if meta_data and not is_json(meta_data):
				raise ValueError("meta-data is not in JSON form")
			pub_obj = Publisher.objects.get(name=name)
			pub_obj.meta_data=meta_data
			pub_obj.save()
			self.response['res_data'] = pub_obj.as_dict()
			self.response['res_str'] = "Publisher Updated Successfully"
			return send_201(self.response)

		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

class BookViews(View):
	def __init__(self):
		self.response=init_response()

	def get(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			book_id=params.get('book_id')
			limit=params.get('limit',LIMIT)
			offset=params.get('offset',OFFSET)
			if book_id :
				try:
					self.response['res_data']=Book.objects.get(book_id=book_id).as_dict()
				except:
					raise ObjectDoesNotExist("Requested BOOK does not exist")
			elif params.get('name'):
				try:
					res=[book.as_dict() for book in Book.objects.filter(name=params.get('name').lower())]
					self.response['res_data']=res
				except:
					raise ObjectDoesNotExist("Requested BOOK does not exist")
			else:
				ath=Book.objects.all()
				res=[]
				for index in range(offset,limit):
					if index >= len(ath):
						break
					res.append(ath[index].as_dict())
				self.response['res_data']=res
			return send_200(self.response)

		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)
	
	def post(self, request, *args, **kwargs):
		try:
			params=request.POST.dict()
			validate_schema(params,['name','author','publisher','language'])
			name = params.get('name').lower()

			author_list=[auth.strip() for auth in params.get('author').split(',') if auth != '']
			if(len(author_list)==0):
				raise ValidationError("Need at least one author")	
			lan_list=[_lang.strip() for _lang in params.get('language').split(',') if _lang != '']
			if(len(lan_list)==0):
				raise ValidationError("Need at least one language")

			publisher_name = params.get('publisher')
			try:
				publisher_obj=Publisher.objects.get(name=publisher_name.lower())
			except:
				raise ObjectDoesNotExist("Publisher with "+publisher_name + " name not exist")
			extra_details = params.get('extra_details')
			if extra_details and not is_json(extra_details):
				raise ValueError("extra_details is not in JSON form")

			book_type = None
			book_param=params.get('book_type')
			if book_param and (book_param.lower()=='true' or book_param.lower()=='false') :
				book_type=eval(book_param.capitalize())

			book_obj = Book.objects.create(name=name,publisher=publisher_obj,book_type=book_type,extra_details=extra_details)
			book_obj.status='A'
			book_obj.author.add(*(Author.objects.get_queryset_objects(author_list)))
			book_obj.language.add(*(Language.objects.get_queryset_objects(lan_list)))
			book_obj.save()
			self.response['res_data'] = book_obj.as_dict()
			self.response['res_str'] = "Book Successfully Created"
			return send_201(self.response)

		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

	def delete(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params,['book_id'])
			book_id = params.get('book_id')
			try:
				book_obj=Book.objects.get(book_id=book_id)
				res=book_obj.as_dict()
				book_obj.status='D'
				book_obj.save()
				self.response['res_data'] = res
				self.response['res_str'] = "Book Status Change to Deleted Successfully"
			except:
				raise ObjectDoesNotExist("Requested BOOK does not exist")
			return send_201(self.response)

		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

	def put(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params,['book_id'])
			book_id = params.get('book_id')
			try:
				book_obj=Book.objects.get(book_id=book_id)
			except:
				raise ObjectDoesNotExist("Requested BOOK does not exist")
	
			author_list=[auth.strip() for auth in params.get('author') .split(',') if auth != '']
			lan_list=[_lang.strip() for _lang in params.get('language').split(',') if _lang != '']

			extra_details=book_obj.extra_details 
			extra_param = params.get('extra_details')
			if extra_param and not is_json(extra_param):
				raise ValueError("extra_details is not in JSON form")
			elif extra_param:
				extra_details=extra_param

			book_type = book_obj.book_type 
			book_param=params.get('book_type')
			if book_param and (book_param.lower()=='true' or book_param.lower()=='false') :
				book_type=eval(book_param.capitalize())

			book_obj.book_type=book_type
			book_obj.extra_details=extra_details
			book_obj.author.add(*(Author.objects.get_queryset_objects(author_list)))
			book_obj.language.add(*(Language.objects.get_queryset_objects(lan_list)))
			book_obj.save()
			self.response['res_data'] = book_obj.as_dict()
			self.response['res_str'] = "Book Updated Successfully"
			return send_201(self.response)

		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

class EBookViews(View):
	def __init__(self):
		self.response=init_response()

	def get(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			limit=params.get('limit',LIMIT)
			offset=params.get('offset',OFFSET)
			if params.get('ebook_id'):
				try:
					self.response['res_data']=EBook.objects.get(ebook_id=params.get('ebook_id')).as_dict()
				except:
					raise ObjectDoesNotExist("Requested Ebook does not exist")
			else:
				ebooks=EBook.objects.all()
				res=[]
				for index in range(offset,limit):
					if index >= len(ebooks):
						break
					res.append(ebooks[index].as_dict())
				self.response['res_data']=res
			return send_201(self.response)

		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

	def post(self, request, *args, **kwargs):
		try:
			params=request.POST.dict() 
			validate_schema(params,['book_id'],"Mandatory Book Key is needed")
			try:
				book = Book.objects.get(book_id=params.get('book_id'))
			except:
				raise ObjectDoesNotExist("Book with given id doesnot exist "+params.get('book_id'))
			book_location = params.get('book_location')
			ebook_obj = EBook.objects.create( book=book, book_location=book_location)
			self.response['res_data'] = ebook_obj.as_dict()
			self.response['res_str'] = "EBook Successfully Created"
			return send_201(self.response)
		
		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

	def delete(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params,['ebook_id'],"Ebook id is needed")
			try:
				ebook_obj = EBook.objects.get(ebook_id=params.get('ebook_id'))
			except:
				raise ObjectDoesNotExist("EBook with given id doesnot exist "+params.get('ebook_id'))
			res=ebook_obj.as_dict()
			ebook_obj.delete()
			ebook_obj.save()
			self.response['res_data'] = res
			self.response['res_str'] = "EBook Deleted Successfully"
			return send_201(self.response)

		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

	def put (self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params,['ebook_id'],":Ebook id is needed")
			try:
				ebook_obj = EBook.objects.get(ebook_id=params.get('ebook_id'))
			except:
				raise ObjectDoesNotExist("EBook with given id doesnot exist "+params.get('ebook_id'))
			ebook_obj.book_location=params.get('book_location')
			ebook_obj.save()
			res=ebook_obj.as_dict()
			self.response['res_data'] = res
			self.response['res_str'] = "EBook Location Updated Successfully"
			return send_201(self.response)

		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)	

class UserViews(View):
	def __init__(self):
		self.response=init_response()

	def get(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params,['email_id'])
			try:
				self.response['res_data']=User.objects.get(email_id=params.get('email_id')).as_dict()
			except:
				raise ValidationError("User with this email id does not exist")
			return send_201(self.response)
			
		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)
	
	def post(self, request, *args, **kwargs):
		try:
			import re
			params=request.POST.dict()
			validate_schema(params,['first_name','mobile','email_id'])
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
			if meta_data and not is_json(meta_data):
				raise ValueError("meta_data is not in JSON form")

			subscribed=False
			subscription=params.get('subscription')
			if subscription and subscription.lower()=='true':
				subscribed=True

			fav_book=[book.strip() for book in params.get('favourited').split(',') if book != '']
		
			user_obj = User.objects.create(first_name=first_name,middle_name=middle_name,last_name=last_name,mobile=mobile,email_id=email_id,meta_data=meta_data,subscription=subscribed)
			user_obj.status='A'
			user_obj.favourited.add(*(Book.objects.get_queryset_objects(fav_book)))
			user_obj.save()
			self.response['res_data'] = user_obj.as_dict()
			self.response['res_str'] = "User Successfully Created"
			return send_201(self.response)

		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

	def delete(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params,['email_id'])
			try:	
				user_obj=User.objects.get(email_id=params.get('email_id'))
				user_obj.status='D'
				user_obj.save()
				self.response['res_data'] = user_obj.as_dict()
				self.response['res_str'] = "User Status Change To Deleted Successfully"
			except:
				raise ValidationError("User with this email id doesnot exist")
			return send_201(self.response)
			
		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

	def put (self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params,['email_id'])
			try:	
				user_obj=User.objects.get(email_id=params.get('email_id'))
			except:
				raise ValidationError("User with this email id doesnot exist")
			mobile=params.get('mobile')
			meta_data = params.get('meta_data')
			if meta_data and not is_json(meta_data):
				raise ValueError("meta_data is not in JSON form")

			subscribed=user_obj.subscription
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

		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

class HardCopyViews(View):
	def __init__(self):
		self.response=init_response()

	def get(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params,['hard_copy_id'])
			hard_copy_id=params.get('hard_copy_id')
			try:
				self.response['res_data']=HardCopy.objects.get(hard_copy_id=hard_copy_id).as_dict()
			except:
				raise ObjectDoesNotExist("Requested HardCopy does not exist")
			return send_201(self.response)
				
		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)
	
	def post(self, request, *args, **kwargs):
		try:
			params=request.POST.dict()
			validate_schema(params,['book_id'])
			book_id = params.get('book_id')
			try:	
				book_obj=Book.objects.get(book_id=book_id)
			except:
				raise ObjectDoesNotExist("Book with this"+str(book_id)+"does not exist")
			is_lent=False
			lent=params.get('is_lent')
			if lent and lent.lower()=='true':
				is_lent=True
			
			lent_to=params.get('lent_to')
			user_obj=None
			if lent_to and not User.objects.filter(email_id=lent_to).exists():
				user_obj=User.objects.get(email_id=lent_to)

			hardcopy_obj = HardCopy.objects.create( book_id=book_obj, is_lent=is_lent,lent_to=user_obj)
			self.response['res_data'] = hardcopy_obj.as_dict()
			self.response['res_str'] = "HardCopy Successfully Created"
			return send_201(self.response)
		
		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

	def delete(self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params,['hard_copy_id'])
			hard_copy_id=params.get('hard_copy_id')
			try:
				hardcopy_obj=HardCopy.objects.get(hard_copy_id=hard_copy_id)
			except:
				raise ObjectDoesNotExist("Requested HardCopy does not exist")
			self.response['res_data'] = hardcopy_obj.as_dict()
			hardcopy_obj.delete()
			hardcopy_obj.save()
			self.response['res_str'] = "HardCopy Deleted Successfully"
			return send_201(self.response)
				
		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)

	def put (self, request, *args, **kwargs):
		try:
			params=request.GET.dict()
			validate_schema(params,['hard_copy_id'])
			hard_copy_id=params.get('hard_copy_id')
			try:
				hardcopy_obj=HardCopy.objects.get(hard_copy_id=hard_copy_id)
			except:
				raise ObjectDoesNotExist("Requested HardCopy does not exist")

			is_lent=hardcopy_obj.is_lent
			lent=params.get('is_lent')
			if lent and (lent.lower()=='true' or lent.lower()=='false') :
				is_lent=eval(lent.capitalize())
				
			lent_to=params.get('lent_to')
			user_obj=hardcopy_obj.lent_to
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

		except (ValidationError,ObjectDoesNotExist,ValueError) as ex:
			self.response['res_str'] = str(ex)
		except Exception as e:
			self.response['Error Msg']="Something is Wrong"
		return send_400(self.response)







		


