from django.contrib import admin

# Register your models here.
#from .models import Crud #import our class
from .models import *

# Register your models here.
admin.site.register(Language)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(EBook)
admin.site.register(User)
admin.site.register(HardCopy)

