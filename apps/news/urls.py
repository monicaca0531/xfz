# encoding: utf-8

from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('<int:news_id>/', views.detail_news,name='detail_news'),
    path('news_list/', views.news_list,name='news_list'),
    path('comment/', views.public_comment,name='comment'),
]