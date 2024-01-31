from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Article
from .serializers import ArticleSerializer
from .RDFLibGraph import CreateRDFGraph


class ArticleSearchView(APIView):
    @staticmethod
    def get(request):
        json_file = "C:/Users/Alex/Desktop/MLC/De refacut/DAW/Proiect/NEP/api/example.json"
        rdf_graph = CreateRDFGraph(json_file)
        rdf_graph.open_json_file()
        articles = rdf_graph.create_graph()

        if not articles:
            return Response({'error': 'No articles found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(articles, status=status.HTTP_200_OK)
