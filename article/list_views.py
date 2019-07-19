from django.shortcuts import render,get_object_or_404
from .models import ArticlePost,ArticleColumn
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.contrib.auth.models import User

def article_titles(request,username=None):
    if username:
           user = User.objects.get(username=username)
           article_titles = ArticlePost.objects.filter(author=user)
    else:
           article_titles = ArticlePost.objects.all()

    pagintor = Paginator(article_titles,2)
    page = request.GET.get('page')
    try:
        curr_page = pagintor.page(page)
        articles = curr_page.object_list
    except PageNotAnInteger:
        curr_page = pagintor.page(1)
        articles = curr_page.object_list
    except EmptyPage:
        curr_page = pagintor.page(pagintor.num_pages)
        articles = curr_page.object_list

    return render(request,"article/list/article_titles.html",{"articles":articles,"page":curr_page})


def article_detail(request,id,slug):
    article = get_object_or_404(ArticlePost,id=id,slug=slug)
    return render(request,"article/list/article_titles.html",{"article":article})


