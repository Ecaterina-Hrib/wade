generic = None
prefixes = """ PREFIX ns1: <http://www.schema.org/> 
PREFIX prov: <http://www.w3.org/ns/prov#> 
PREFIX skos: <http://www.w3.org/2004/02/skos/core#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"""
sparql_generic_entries = {
    "in_author": """

SELECT ?authorname 
WHERE {
  ?articles ns1:keywords {} .
  ?articles prov:wasAttributedTo ?author .
  ?author rdf:type ns1:Person .
  ?author ns1:name ?authorname.
}
""",

    "in_language":
        """
SELECT ?topic
WHERE {
  ?topic ns1:inLanguage "ro_RO" .
}""",
    "in_keywords":
        """ SELECT DISTINCT ?keywords
    WHERE {
        ?article ns1:keywords ?keywords .
} 
""",
    "all_genres":
    """
    SELECT DISTINCT ?genre WHERE {
    ?article ns1:genre ?genre
    }
    """
    ,
    "in_genre":
        """SELECT ?related_article ?imageUrl
WHERE {
  ?related_article a ns1:Article ;
  		ns1:genre {} ;
  		ns1:name ?article_name ;
  		ns1:articleBody ?article_body ;
    	prov:wasAttributedTo ?person ;
    	ns1:associatedMedia ?imageId .
    ?imageId ns1:contentUrl ?imageUrl .
  ?person a ns1:Person;
     ns1:name ?name_author;
}""",
    "return_organization":
        """SELECT ?person ?organization
WHERE {
  ?person a ns1:Person;
  			ns1:name {} ;
          	prov:actedOnBehalfOf ?organization .

}""",
    "all_articles":
    """SELECT ?article ?articlename ?authorname 
    WHERE{
    ?article ns1:name ?articlename .
    ?article ns1:wordCount ?wordCount .
    ?article prov:wasAttributedTo ?author .
    ?author ns1:name ?authorname .
} """
}
