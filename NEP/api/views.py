from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .RDFLibGraph import CreateRDFGraph
from django.shortcuts import render
from .SparqlHandler import SparqlHandler
from django.http import JsonResponse
from .sparql_generic_queries import sparql_generic_entries, prefixes, generic

articlequery = """
        SELECT DISTINCT ?articlename ?authorname ?keyword  WHERE {
  ?article <http://www.schema.org/keywords> ?keyword .
  ?article <http://www.schema.org/name> ?articlename .
  ?article <http://www.w3.org/ns/prov#wasAttributedTo> ?author .
  ?author <http://www.schema.org/name> ?authorname .
} 
        """


def articles():
    json_file = "C:/Users/Alex/Desktop/MLC/De refacut/DAW/Proiect/NEP/api/libertatea.json"
    rdf_graph = CreateRDFGraph(json_file)
    rdf_graph.open_json_file()
    articles_graph = rdf_graph.create_graph()
    return articles_graph


class FilterKeywordView(APIView):
    def get(self, request, *args, **kwargs):
        sparqlQuery = SparqlHandler()
        resultsKeyword = sparqlQuery.execute_query(prefixes + sparql_generic_entries['in_keywords'])

        keywordList = list()
        for result in resultsKeyword:
            if result['keywords']['value'].split('/')[-1] is not '':
                keywordList.append(result['keywords']['value'].split('/')[-1])

        resultsArticles = sparqlQuery.execute_query(articlequery)

        articlesList = list()
        for result in resultsArticles:
            articleName = result['articlename']['value']
            articlesList.append(articleName)

        if request.GET.get('selectedOption') in keywordList:
            keyword = request.GET.get('selectedOption')

            relatedArticlesQuery = """
            SELECT ?related_article ?imageUrl WHERE {
            ?articleId ns1:keywords <https://dbpedia.org/page/""" + keyword + """> .
            ?articleId ns1:associatedMedia ?imageId .
            ?imageId ns1:contentUrl ?imageUrl .
            <https://dbpedia.org/page/""" + keyword + """> a skos:Concept;
                    skos:related ?related_article.
            }"""
            resultsRelatedArticles = sparqlQuery.execute_query(prefixes + relatedArticlesQuery)
            print(keyword)
            return JsonResponse({'relatedArticles': resultsRelatedArticles})
        if not resultsArticles:
            return JsonResponse({'error': 'No articles found'}, status=status.HTTP_404_NOT_FOUND)

        return render(request, 'filter_by_keyword_articles.html',
                      {'keywords': keywordList, 'articles': articlesList}
                      , status=status.HTTP_200_OK)


class FilterAuthorKeywordView(APIView):

    def get(self, request, *args, **kwargs):
        global keyword
        global authorsList
        sparqlQuery = SparqlHandler()
        resultsKeyword = sparqlQuery.execute_query(prefixes + sparql_generic_entries['in_keywords'])

        keywordList = list()
        for result in resultsKeyword:
            if result['keywords']['value'].split('/')[-1] is not '':
                keywordList.append(result['keywords']['value'].split('/')[-1])

        resultsArticles = sparqlQuery.execute_query(articlequery)
        articlesList = list()
        for result in resultsArticles:
            authorsList = list()
            articleName = result['articlename']['value']
            articlesList.append(articleName)

        if request.GET.get('selectedOption') in keywordList:
            keyword = request.GET.get('selectedOption')

            resultsAuthors = sparqlQuery.execute_query(
                prefixes + sparql_generic_entries['in_author'].replace('{}',
                                                                       "<https://dbpedia.org/page/" + keyword + ">"))
            for result in resultsAuthors:
                authorsList.append(result['authorname']['value'])

            return JsonResponse({'authors': resultsAuthors})
        if request.GET.get('selectedAuthor'):
            print(request.GET.get('selectedAuthor'))
            relatedArticlesQuery = """
                        SELECT ?related_article ?imageUrl WHERE {
                        ?articleId ns1:keywords <https://dbpedia.org/page/""" + keyword + """> .
                        ?articleId ns1:associatedMedia ?imageId .
                        ?imageId ns1:contentUrl ?imageUrl .
                        <https://dbpedia.org/page/""" + keyword + """> a skos:Concept;
                                skos:related ?related_article .
                        ?articleId prov:wasAttributedTo ?author .
                        ?author ns1:name \"""" + request.GET.get('selectedAuthor') + """\" .
                        }"""
            resultsRelatedArticles = sparqlQuery.execute_query(prefixes + relatedArticlesQuery)
            return JsonResponse({'relatedArticles': resultsRelatedArticles})

        if not resultsArticles:
            return JsonResponse({'error': 'No articles found'}, status=status.HTTP_404_NOT_FOUND)

        return render(request, 'filter_by_author_keyword_articles.html',
                      {'keywords': keywordList}
                      , status=status.HTTP_200_OK)


class FilterByGenre(APIView):
    def get(self, request, *args, **kwargs):
        sparqlQuery = SparqlHandler()
        resultsGenres = sparqlQuery.execute_query(prefixes + sparql_generic_entries['all_genres'])
        genresList = list()
        for result in resultsGenres:
            if result['genre']['value'].split('/')[-1] is not '':
                genresList.append(result['genre']['value'].split('/')[-1])

        if request.GET.get('selectedOption') in genresList:
            genre = request.GET.get('selectedOption')
            resultsRelatedArticles = sparqlQuery.execute_query(
                prefixes + sparql_generic_entries['in_genre'].replace('{}', "\"" + genre + "\""))
            return JsonResponse({'relatedArticles': resultsRelatedArticles})
        print(genresList)
        if not genresList:
            return Response({'error': 'No articles found'}, status=status.HTTP_404_NOT_FOUND)
        return render(request, 'filter_by_genre_articles.html', {'genres': genresList}, status=status.HTTP_200_OK)


class AllArticlesView(APIView):
    @staticmethod
    def get(request):
        sparqlQuery = SparqlHandler()
        results = sparqlQuery.execute_query(prefixes + sparql_generic_entries['all_articles'])
        if not results:
            return Response({'error': 'No articles found'}, status=status.HTTP_404_NOT_FOUND)
        return render(request, 'mainpage.html', {'articles': results}, status=status.HTTP_200_OK)
