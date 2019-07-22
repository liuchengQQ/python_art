from django.shortcuts import render,get_object_or_404,HttpResponse
from .models import ArticlePost,ArticleColumn,Comment
from .forms import CommentForm
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import redis
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)

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
    total_views = r.incr("article:{}:views".format(article.id))
    r.zincrby('article_ranking',article.id,1)
    article_ranking = r.zrange('article_ranking',0,-1,desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x:article_ranking_ids.index(x.id))
    return render(request,"article/list/article_detail.html",{"article":article,"total_views":total_views,"most_views":most_viewed})


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

def read_article(request,id,slug):
      article = get_object_or_404(ArticlePost,id=id,slug=slug)
      total_views = r.incr("article:{}:views".format(article.id))
      r.zincrby('article_rangking',article.id,1)
      article_rangking = r.zrange('article_rangking',0,-1,desc=True)[:10]
      article_ranking_ids = [int(id) for id in article_rangking]
      most_viewed = list(ArticlePost.objects.filter(id__in=article_rangking_ids))
      most_viewed.sort(key=lambda x:article_ranking_ids.index(x.id))

      if request.method == "POST":
          comment_form = CommentForm(data=request.POST)
          if comment_form.is_valid():
              new_comment = comment_form.save(commit=False)
              new_comment.article = article
              new_comment.save()
      else:
          comment_form = CommentForm()
          return render(request,"article/list/article_detail.html",{"article":article,"total_views":total_views,"comment_form":comment_form})