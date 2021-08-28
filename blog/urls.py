from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('blogs/', BlogListView.as_view(), name='blog-list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blogger/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]
