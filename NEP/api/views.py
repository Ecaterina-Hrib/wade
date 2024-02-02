from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Article
from .serializers import ArticleSerializer
from .RDFLibGraph import CreateRDFGraph
from django.shortcuts import render
from .SparqlHandler import SparqlHandler


def articles():
    json_file = "C:/Users/Alex/Desktop/MLC/De refacut/DAW/Proiect/NEP/api/example.json"
    rdf_graph = CreateRDFGraph(json_file)
    rdf_graph.open_json_file()
    aarticles = rdf_graph.create_graph()
    articles = rdf_graph.query()
    return articles


class ArticleSearchView(APIView):
    @staticmethod
    def get(request):
        someArticles = articles()
        if not someArticles:
            return Response({'error': 'No articles found'}, status=status.HTTP_404_NOT_FOUND)
        return render(request, 'articles_list.html', {'articles': someArticles}, status=status.HTTP_200_OK)


class AllArticlesView(APIView):
    @staticmethod
    def get(request):
        allArticles = articles()
#         query = """
#     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# SELECT * WHERE {
#   ?sub ?pred ?obj .
# } LIMIT 10
# """
#         sparqlQuery = SparqlHandler()
#         results = sparqlQuery.execute_query(query)

        if not allArticles:
            return Response({'error': 'No articles found'}, status=status.HTTP_404_NOT_FOUND)
        return render(request, 'articles_list.html', {'articles': allArticles}, status=status.HTTP_200_OK)
