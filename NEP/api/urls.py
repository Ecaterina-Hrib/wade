from django.urls import path
from .views import FilterKeywordView, AllArticlesView, FilterAuthorKeywordView, FilterByGenre, buttons_page

urlpatterns = [
    path('searchkeyword/', FilterKeywordView.as_view(), name='searchkeyword'),
    path('mainpage/', AllArticlesView.as_view(), name='mainpage'),
    path('searchauthorkeyword/', FilterAuthorKeywordView.as_view(), name='searchauthorkeyword'),
    path('searchgenre/', FilterByGenre.as_view(), name='searchgenre'),
path('', buttons_page, name='home')
]
