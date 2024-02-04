from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .RDFLibGraph import CreateRDFGraph
from django.shortcuts import render
from .SparqlHandler import SparqlHandler
from django.http import JsonResponse

articlequery = """
        SELECT DISTINCT ?articlename ?authorname ?keyword  WHERE {
  ?article <http://www.schema.org/keywords> ?keyword .
  ?article <http://www.schema.org/name> ?articlename .
  ?article <http://www.w3.org/ns/prov#wasAttributedTo> ?author .
  ?author <http://www.schema.org/name> ?authorname .
} 
        """
keywordQuery = """
            SELECT DISTINCT ?keyword  WHERE {
  ?article <http://www.schema.org/keywords> ?keyword .
} 
        """


def articles():
    json_file = "C:/Users/Alex/Desktop/MLC/De refacut/DAW/Proiect/NEP/api/libertatea.json"
    rdf_graph = CreateRDFGraph(json_file)
    rdf_graph.open_json_file()
    articles_graph = rdf_graph.create_graph()
    return articles_graph


class ArticleSearchView(APIView):
    def get(self, request, *args, **kwargs):
        sparqlQuery = SparqlHandler()
        resultsKeyword = sparqlQuery.execute_query(keywordQuery)

        keywordList = list()
        for result in resultsKeyword:
            if result['keyword']['value'].split('/')[-1] is not '':
                keywordList.append(result['keyword']['value'].split('/')[-1])

        resultsArticles = sparqlQuery.execute_query(articlequery)

        articlesList = list()
        for result in resultsArticles:
            authorName = result['authorname']['value']
            articleName = result['articlename']['value']
            if result['keyword']['value'].split('/')[-1] is not '':
                keywordName = result['keyword']['value'].split('/')[-1]
            articlesList.append((authorName, articleName, keywordName))

        if request.GET.get('selectedOption') in keywordList:
            keyword = request.GET.get('selectedOption')
            relatedArticlesQuery = """
            SELECT ?articleId WHERE {
            ?articleId <http://www.schema.org/keywords> <https://dbpedia.org/page/""" + keyword + """> .
            }"""
            resultsRelatedArticles = sparqlQuery.execute_query(relatedArticlesQuery)
            return JsonResponse({'relatedArticles': resultsRelatedArticles})

        if not resultsArticles:
            return JsonResponse({'error': 'No articles found'}, status=status.HTTP_404_NOT_FOUND)

        return render(request, 'specific_articles.html',
                      {'keywords': keywordList, 'articles': articlesList}
                      , status=status.HTTP_200_OK)


class AllArticlesView(APIView):
    @staticmethod
    def get(request):
        # allArticles = articles()
        query = """
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX prov: <http://www.w3.org/ns/prov#>
SELECT ?article ?articlename ?authorname ?wordCount WHERE {
  ?article <http://www.schema.org/name> ?articlename .
  ?article <http://www.schema.org/wordCount> ?wordCount .
  ?article <http://www.w3.org/ns/prov#wasAttributedTo> ?author .
  ?author <http://www.schema.org/name> ?authorname .
} 
"""
        sparqlQuery = SparqlHandler()
        results = sparqlQuery.execute_query(query)
        # print(results)
        if not results:
            return Response({'error': 'No articles found'}, status=status.HTTP_404_NOT_FOUND)
        return render(request, 'mainpage.html', {'articles': results}, status=status.HTTP_200_OK)
