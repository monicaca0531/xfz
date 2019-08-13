from django.shortcuts import render
from .models import News,NewsCategory,Comment, Banner
from django.conf import settings
from .serializers import NewsSerializers,CommentSerializers
from utils import restful
from django.http import Http404
from.foms import PublicCommentForm
from apps.xfzauth.decorators import xfz_login_require
from django.db.models import Q


def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    newses = News.objects.select_related('author','category').all()[0:count]
    categories = NewsCategory.objects.all()
    banners = Banner.objects.all()
    context = {
        'newses':newses,
        'categories':categories,
        'banners':banners
    }
    return render(request,'news/index.html',context=context)

def news_list(request):
    page = int(request.GET.get('p',1))
    category_id = int(request.GET.get('category_id',0))

    start = (page - 1)*settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    if category_id == 0:
        newses = News.objects.select_related('author','category').all()[start:end]
    else:
        newses = News.objects.filter(category__id=category_id)[start:end]
    serializers = NewsSerializers(newses,many=True)
    data = serializers.data
    return restful.result(data=data)

def detail_news(request,news_id):
    try:
        news = News.objects.select_related('author','category').prefetch_related("comments__author").get(pk=news_id)
        context = {
            'news': news
        }
        return render(request, "news/news_detail.html", context=context)
    except:
        raise Http404

@xfz_login_require
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        news_id = form.cleaned_data.get('news_id')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content,news=news,author=request.user)
        serializer = CommentSerializers(comment)
        data = serializer.data
        return restful.result(data=data)
    else:
        return restful.params_error(message=form.get_errors())

def search(request):
    q = request.GET.get('q')
    context = {}
    if q:
        newses = News.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
        context['newses'] = newses
    return render(request,"search/search.html",context=context)