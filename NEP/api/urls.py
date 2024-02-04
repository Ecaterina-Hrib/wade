from django.urls import path
from .views import ArticleSearchView, AllArticlesView

urlpatterns = [
    path('search/', ArticleSearchView.as_view(), name='search'),
    path('mainpage/', AllArticlesView.as_view(), name='mainpage')
]