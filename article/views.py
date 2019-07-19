from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ArticleColumn
from django.views.decorators.csrf import csrf_exempt
from .forms import ArticleColumnForm,ArticlePost,ArticlePostForm
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.

@login_required(login_url="/account/login/")
@csrf_exempt
def article_column(request):
    if request.method == "GET":
        column = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request,"article/article-column.html",{"column":column,"column_form":column_form})
    else:
        column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user_id=request.user.id,column=request.column_name)
        if columns:
            return HttpResponse("2")
        else:
            ArticleColumn.objects.create(user=request.user,column=column_name)
            return HttpResponse("1")

@login_required(login_url="/account/login/")
@require_POST
@csrf_exempt
def rename_article_column(request):
    column_name = request.POST['column_name']
    column_id = require_POST['column_id']

    try:
        line = ArticleColumn.objects.filter(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")



@login_required(login_url="/account/login/")
@require_POST
@csrf_exempt
def del_article_column(request):
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.filter(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")

@login_required(login_url="/account/login/")
@csrf_exempt
def article_post(request):
    if request.method == "POST":
        article_post_form = ArticlePostForm(request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        return render(request,"article/article_post.html",{"article_post_form":article_post_form,"article_columns":article_columns})

@login_required(login_url="/account/login")
def article_list(request):
        articles = ArticlePost.objects.filter(author=request.user)
        pagintor = Paginator(articles,2)
        page = request.GET.get('page')
        try:
            current_page = pagintor.page(page)
            arts = current_page.object_list
        except PageNotAnInteger:
             current_page = pagintor.page(1)
             arts = current_page.object_list
        except EmptyPage:
             current_page = pagintor.page(pagintor.num_pages)
             arts = current_page.object_list
        return render(request,"article/article_list.html",{"articles":arts,"page":current_page})


