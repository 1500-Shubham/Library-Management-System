from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
path('language/',csrf_exempt(views.LanguageViews.as_view())),
path('author/',csrf_exempt(views.AuthorViews.as_view())),
path('publisher/',csrf_exempt(views.PublisherViews.as_view())),
path('book/',csrf_exempt(views.BookViews.as_view())),
path('ebook/',csrf_exempt(views.EBookViews.as_view())),
path('user/',csrf_exempt(views.UserViews.as_view())),
path('hardcopy/',csrf_exempt(views.HardCopyViews.as_view())),

]