# api/create_articles.py
from django.core.management.base import BaseCommand
from api.models import Article  # Adjust the import path
from datetime import datetime


class Command(BaseCommand):
    help = 'Create example articles in the database'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Article.objects.all().delete()

        # Create example articles
        Article.objects.create(
            title='Breaking',
            content='Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
            published_on=datetime.now(),
            source_name='News Agency A',
            author_name='Journalist A',
            language='English',
            topic='Politics',
        )

        Article.objects.create(
            title='Sports Update: Championship Finals',
            content='Lorem ipsum dolor sit amet, consectetur adipiscing elit...',
            published_on=datetime.now(),
            source_name='Sports Network',
            author_name='Reporter B',
            language='English',
            topic='Sports',
        )

        # Add more articles as needed
