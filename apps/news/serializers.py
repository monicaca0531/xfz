# encoding: utf-8

from rest_framework import serializers
from .models import News, NewsCategory,Comment
from apps.xfzauth.serializers import UserSerializers
from apps.news.models import Banner

class NewsCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id','name')

class NewsSerializers(serializers.ModelSerializer):
    category = NewsCategorySerializers()
    author = UserSerializers()
    class Meta:
        model = News
        fields = ('id','title','desc','thumbnail','pub_time','author','category')

class CommentSerializers(serializers.ModelSerializer):
    author = UserSerializers()
    class Meta:
        model = Comment
        fields = ('id','content','author','pub_time')

class BannerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ('id','img_url','link_to','priority')