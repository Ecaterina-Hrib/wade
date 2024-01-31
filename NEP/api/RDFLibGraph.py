from rdflib import Graph, URIRef, Literal, Namespace, RDFS, RDF
import json
from rdflib.plugins.sparql import prepareQuery


class CreateRDFGraph:
    def __init__(self, json_file_path):
        self.data = None
        self.json_file_path = json_file_path
        
    def open_json_file(self):    
        with open(self.json_file_path, 'r') as json_file:
            self.data = json.load(json_file)

    def create_graph(self):
        global graph_serialized
        g = Graph()

        prov = Namespace("http://www.w3.org/ns/prov#")
        schema = Namespace("http://www.schema.org/")
        ex = Namespace("http://www.example.org/")
        
        for row in self.data:
            # URI Resources
            article_uri = URIRef(schema + row['articleName'].replace(" ", "_"))
            author_uri = URIRef(schema + row['authorName'].replace(" ", "_"))
            image_uri = URIRef(schema + row['imageDescription'].replace(" ", "_"))
        
            # Information about article
            g.add((article_uri, RDF.type,schema.Article))
            g.add((article_uri, schema.name, Literal(row['articleName'])))
            g.add((article_uri, schema.datePublished, Literal(row['articleDatePublished'])))
            g.add((article_uri, schema.description, Literal(row['articleDescription'])))
            g.add((article_uri, schema.inLanguage, Literal(row['articleLanguage'])))
            g.add((article_uri, schema.url, Literal(row['articleUrl'])))
            g.add((article_uri, schema.articleSection, Literal(row['articleSection'])))
            g.add((article_uri, schema.wordCount, Literal(row['wordCount'])))
        
            # Information about Multimedia
            g.add((article_uri, schema.hasThumbnail, image_uri))
            g.add((image_uri, schema.contentUrl, Literal(row['imagelink'])))
            g.add((image_uri, schema.about, Literal(row['imageDescription'])))
        
            # Information about author
            g.add((article_uri, prov.wasAttributedTo, author_uri))
            g.add((author_uri, schema.name, Literal(row['authorName'])))
            g.add((author_uri, schema.nationality, Literal(row['authorNationality'])))
        
            g.add((author_uri, RDF.type, schema.Person))
            g.add((author_uri, RDF.type, prov.Entity))

            graph_serialized = g.serialize(format='nt')
        return graph_serialized

# provide the articles under 4000 words
# written in English or Spanish about the
# international IT contests
# sparql_query = prepareQuery(
#     """
#     SELECT ?article ?name ?inLanguage ?articleSection ?wordCount
#     WHERE {
#         ?article <http://www.schema.org/name> ?name .
#         ?article <http://www.schema.org/inLanguage> ?language .
#         ?article <http://www.schema.org/articleSection> ?section .
#         ?article <http://www.schema.org/wordCount> ?wordCount .
#         ?article <http://www.w3.org/ns/prov#wasAttributedTo> ?author .
#         ?author <http://www.schema.org/name> ?name .
#
#         FILTER ((?language = 'en' || ?language = 'es') && ?wordCount < 4000 &&
#         ?articleSection =='Contest')}"""
# )
# results = g.query(sparql_query)
#
# # Print the results
# for row in results:
#     # print("Article:", row.article)
#     print("Title:", row.title)
#     # print("Author:",row.author)
#     print("Name:", row.name)
#     print("\n")
