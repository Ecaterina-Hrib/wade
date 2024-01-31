from django.db import models
from rdflib import Literal, BNode, Namespace, URIRef, Graph, Dataset, RDF, RDFS, XSD
from rdflib.namespace import FOAF
from rdflib.serializer import Serializer
import rdflib.resource
import uuid


# TODO better structure of the models
class Article(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    datePublished = models.DateTimeField()
    source_name = models.CharField(max_length=255)
    inLanguage = models.CharField(max_length=255)
    language = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    wordCount = models.CharField(max_length=255)
    articleSection = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    # def __dict__(self):
    #     dict_object = {
    #         "name": self.name,
    #
    #     }


class Multimedia(models.Model):
    url = models.CharField(max_length=255)
    about = models.CharField(max_length=255)
    hasThumbnail = models.CharField(max_length=255)


class Author(models.Model):
    wasAttributedTo = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
