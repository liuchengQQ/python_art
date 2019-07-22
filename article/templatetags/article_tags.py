from django import template
register = template.Library()
from article.models import ArticlePost


@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()

@register.simple_tag
def author_total_articles(user):
    return user.article.count()

@register.inclusion_tag('article/latest_articles.html')
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by("-created")[:n]
    return {"latest_articles":latest_articles}


def most_comments_artiles(n=5):
    return ArticlePost.objects.annotate(total_count=Count('comments')).order_by("-total_comments")[:n]