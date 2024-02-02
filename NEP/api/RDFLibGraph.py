from rdflib import Graph, URIRef, Literal, Namespace, RDFS, RDF, XSD, SKOS
import json
from rdflib.plugins.sparql import prepareQuery


class CreateRDFGraph:
    def __init__(self, json_file_path):
        self.data = None
        self.graph_serialized = None
        self.json_file_path = json_file_path

    def open_json_file(self):
        with open(self.json_file_path, 'r') as json_file:
            self.data = json.load(json_file)

    def create_graph(self):
        g = Graph()

        prov = Namespace("http://www.w3.org/ns/prov#")
        schema = Namespace("http://www.schema.org/")
        dbpedia = Namespace("https://dbpedia.org/page/")

        for articles in self.data:
            for article_key, article_data in articles.items():
                # URI Resources
                article_uri = URIRef(schema + str(article_data['articleId']))

                # Information about article
                g.add((article_uri, RDF.type, schema.Article))
                g.add((article_uri, schema.name, Literal(article_data['articleName'])))
                g.add((article_uri, schema.articleBody, Literal(article_data['articleBody'])))
                g.add((article_uri, schema.datePublished, Literal(article_data['articleDatePublished'])))
                g.add((article_uri, schema.description, Literal(article_data['articleDescription'])))
                g.add((article_uri, schema.inLanguage, Literal(article_data['articleLanguage'])))
                g.add((article_uri, schema.url, Literal(article_data['articleUrl'])))
                g.add((article_uri, schema.genre, Literal(article_data['genre'])))
                g.add((article_uri, schema.wordCount, Literal(article_data['wordCount'])))
                g.add((article_uri, prov.generatedAtTime, Literal(article_data['generatedAtTime'], datatype=XSD.date)))

                keywordList = article_data['keywords'].split(', ')
                for keyword in keywordList:
                    print(keyword)
                    keywords_uri = URIRef(dbpedia + keyword)
                    g.add((keywords_uri, RDF.type, SKOS.Concept))
                    g.add((article_uri, schema.keywords, keywords_uri))
                    g.add((keywords_uri, SKOS.related, article_uri))

                if len(article_data["multimedia_content"]) > 1:
                    for multimedia_key, multimedia_data in article_data["multimedia_content"].items():
                        if "image" in multimedia_key:
                            multimedia_uri = URIRef(schema + str(multimedia_data['imageId']))
                            g.add((multimedia_uri, schema.contentUrl, Literal(multimedia_data['imageUrl'])))
                            g.add((multimedia_uri, schema.description, Literal(multimedia_data['imageDescription'])))
                        else:
                            multimedia_uri = URIRef(schema + str(multimedia_data['videoId']))
                            g.add((multimedia_uri, schema.contentUrl, Literal(multimedia_data['videoUrl'])))
                            g.add((multimedia_uri, RDF.type, schema.VideoObject))

                        # Information about Multimedia
                        g.add((article_uri, schema.associatedMedia, multimedia_uri))
                        g.add((multimedia_uri, schema.associatedArticle, article_uri))
                        g.add((multimedia_uri, schema.height, Literal(multimedia_data['height'])))
                        g.add((multimedia_uri, schema.width, Literal(multimedia_data['width'])))
                        g.add((multimedia_uri, schema.encodingFormat, Literal(multimedia_data['encodingFormat'])))

                # Information about author
                author_uri = URIRef(schema + str(article_data["author"]['authorId']))

                g.add((article_uri, prov.wasAttributedTo, author_uri))
                g.add((author_uri, schema.name, Literal(article_data["author"]['authorName'])))
                g.add((author_uri, schema.nationality, Literal(article_data["author"]['authorNationality'])))

                g.add((author_uri, RDF.type, schema.Person))
                g.add((author_uri, RDF.type, prov.Agent))

                organization_uri = URIRef(prov + str(article_data["organization"]["organizationId"]))
                g.add((organization_uri, RDF.type, prov.Organization))
                g.add((organization_uri, schema.name, Literal(article_data["organization"]["organizationName"])))

                g.add((author_uri, prov.actedOnBehalfOf, organization_uri))

                turtle_file_path = "output.ttl"
                self.graph_serialized = g.serialize(destination=turtle_file_path, format='turtle')
                self.graph_serialized = g.serialize(format='turtle')
        return self.graph_serialized
    def query(self):
        prepareQuery = """
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT * WHERE {
          ?sub ?pred ?obj .
        } LIMIT 10
        """
        results = self.graph_serialized.query(prepareQuery)
        return results