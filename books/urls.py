from django.urls import path
from . import views


app_name = 'books'


urlpatterns = [
path('', views.home, name='home'),
path('categories/', views.category_list, name='category_list'),
path('categories/<slug:category_slug>/', views.subcategory_list, name='subcategory_list'),
path('categories/<slug:category_slug>/<slug:subcategory_slug>/', views.book_list, name='book_list'),
path('book/<int:pk>/', views.book_detail, name='book_detail'),
path('book/<int:pk>/download/', views.book_download, name='book_download'),
path('upload/', views.upload_book, name='upload_book'),
 path('search/', views.search_results, name='search_results'),
]