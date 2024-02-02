from SPARQLWrapper import SPARQLWrapper, JSON


class SparqlHandler:
    database_name = "nep"
    localhost = f"http://localhost:3030/{database_name}"

    def execute_query(self, query):
        sparql = SPARQLWrapper(self.localhost + "/query")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results["results"]["bindings"]

    def update_data(self):
        # todo
        pass
