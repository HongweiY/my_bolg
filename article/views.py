from django.shortcuts import render, redirect
from django.http import HttpResponse
from article.models import Article
from datetime import datetime
from django.http import Http404
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

# 主页
def home(request):
    posts = Article.objects.all()
    paginator = Paginator(posts, 1)  # 每页显示两个
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.paginator(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list})


# 详情
def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post': post})


# 归档
def archives(request):
    try:
        archives_list = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'archives.html', {'archives_list': archives_list, 'error': False}, )


# about me
def about_me(request):
    return render(request, 'about_me.html')


# 标签分类
def search_tag(request, tag):
    try:
        article_list = Article.objects.filter(category=tag)
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'tag.html', {'article_list': article_list})


def blog_search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if not keyword:
            post_list = Article.objects.all()
            return render(request, 'home.html', {'archives_list': post_list})
        else:
            post_list = Article.objects.filter(title__icontains=keyword)
            if len(post_list) == 0:
                return render(request, 'archives.html', {'archives_list': post_list, 'error': True})
            else:
                return render(request, 'archives.html', {'archives_list': post_list,
                                                         'error': False})
    return redirect('/')


class RSSFeed(Feed) :
    title = "RSS feed - article"
    link = "feeds/posts/"
    description = "RSS feed - blog posts"

    def items(self):
        return Article.objects.order_by('-date_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.date_time

    def item_description(self, item):
        return item.content
