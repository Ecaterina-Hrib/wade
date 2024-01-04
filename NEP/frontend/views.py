# frontend/views.py
from django.shortcuts import render
from api.models import Article

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'frontend/articles_list.html', {'articles': articles})
