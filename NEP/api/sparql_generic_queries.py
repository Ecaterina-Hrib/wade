generic = None
prefixes = """ PREFIX ns1: <http://www.schema.org/> 
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"""
sparql_generic_entries = {
    "Return all articles on an author": """

SELECT ?article 
WHERE {
  ?article rdf:type ns1:Article .
  ?author rdf:type ns1:Person .
  ?author ns1:name {} .
}
""".format(generic),
    "in_language":
        """
SELECT ?topic
WHERE {
  ?topic ns1:inLanguage "ro_RO" .
}""",
    "in_topic": """SELECT ?genre
WHERE {
  ?genre ns1:genre {} .
}""".format(generic),
    "in_genre":
"""SELECT ?article_name ?article_body ?name_author
WHERE {
  ?article a ns1:Article ;
  		ns1:genre {} ;
  		ns1:name ?article_name ;
  		ns1:articleBody ?article_body ;
    	prov:wasAttributedTo ?person .
  ?person a ns1:Person;
     ns1:name ?name_author;
}""".format(generic),
    "return_organization":
    """SELECT ?person ?organization
WHERE {
  ?person a ns1:Person;
  			ns1:name {} ;
          	prov:actedOnBehalfOf ?organization .

}""".format(generic)



}
