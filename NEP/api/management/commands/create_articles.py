# api/create_articles.py
from django.core.management.base import BaseCommand
from api.models import Article  # Adjust the import path
from datetime import datetime
from api.RDFLibGraph import CreateRDFGraph

class Command(BaseCommand):
    help = 'Create example articles in the database'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Article.objects.all().delete()
        json_file = "C:/Users/Alex/Desktop/MLC/De refacut/DAW/Proiect/NEP/api/example.json"
        rdf_graph = CreateRDFGraph(json_file)
        rdf_graph.open_json_file()
        articles = rdf_graph.create_graph()
        print(articles)
        Article.object.create("Hello")
        # Create example articles

        # Add more articles as needed
