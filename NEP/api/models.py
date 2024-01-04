from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_on = models.DateTimeField()
    source_name = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    language = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)

    # Add other fields as needed

    def __str__(self):
        return self.title

# Create your models here.
