from django.shortcuts import render,get_object_or_404,HttpResponse
from .models import ArticlePost,ArticleColumn
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

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


@csrf_exempt
@require_POST
@login_required(login_url='/account/login')
def like_article(request):
     article_id = request.POST.get('id')
     action = request.POST.get('action')
     if article_id and action:
         try:
             article = ArticlePost.objects.get(id=article_id)
             if article=='like':
                       article.users_like.add(request.user)
                       return HttpResponse("1")
             else:
                 article.users_like.remove(request.user)
                 return HttpResponse("2")
         except:
              return HttpResponse("no")

