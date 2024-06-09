import time
import requests
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, XSD, OWL

# Define namespaces
movie_ns = Namespace("http://www.semanticweb.org/quentin/ontologies/2024/5/movie/")
owl_ns = OWL
rdf_ns = RDF
rdfs_ns = RDFS
xsd_ns = XSD

# Create a new graph
g = Graph()

# Bind namespaces to prefixes
g.bind("movie", movie_ns)
g.bind("owl", owl_ns)
g.bind("rdf", rdf_ns)
g.bind("xml", URIRef("http://www.w3.org/XML/1998/namespace"))
g.bind("xsd", xsd_ns)
g.bind("rdfs", rdfs_ns)

# Add class declarations
classes = [
    "Collection", "Genre", "Movie", "Person"
]
for c in classes:
    g.add((movie_ns[c], RDF.type, OWL.Class))

# Add object property declarations
object_properties = [
    "hasCollection", "hasGenre", "hasPerson"
]
for p in object_properties:
    g.add((movie_ns[p], RDF.type, OWL.ObjectProperty))

# Add data property declarations
data_properties = [
    "adult", "collectionID", "collectionImage", "collectionName", "id", "image",
    "imdbID", "overview", "releaseDate", "title", "popularity",  # Added popularity here
    "gender", "knownForDepartment", "name", "originalName", "popularity", "profilePath",
    "castID", "character", "creditID", "order"
]
for p in data_properties:
    g.add((movie_ns[p], RDF.type, OWL.DatatypeProperty))

# Add data property domains
data_property_domains = {
    "adult": "Movie",
    "collectionID": "Collection",
    "collectionImage": "Collection",
    "collectionName": "Collection",
    "id": ["Movie", "Person"],  # Shared by Movie and Person
    "image": "Movie",
    "imdbID": "Movie",
    "overview": "Movie",
    "releaseDate": "Movie",
    "title": "Movie",
    "popularity": "Movie",  # Added popularity here
    "gender": "Person",
    "knownForDepartment": "Person",
    "name": "Person",
    "originalName": "Person",
    "moviePopularity": "Person",
    "profilePath": "Person",
    "castID": "Person",
    "character": "Person",
    "creditID": "Person",
    "order": "Person"
}
for prop, domain in data_property_domains.items():
    if isinstance(domain, list):
        for d in domain:
            g.add((movie_ns[prop], RDFS.domain, movie_ns[d]))
    else:
        g.add((movie_ns[prop], RDFS.domain, movie_ns[domain]))

# Add data property ranges
data_property_ranges = {
    "adult": XSD.boolean,
    "collectionID": XSD.integer,
    "collectionImage": XSD.string,
    "collectionName": XSD.string,
    "id": XSD.integer,
    "image": XSD.string,
    "imdbID": XSD.string,
    "overview": XSD.string,
    "releaseDate": XSD.date,
    "title": XSD.string,
    "moviePopularity": XSD.float,  # Added popularity here
    "gender": XSD.integer,
    "knownForDepartment": XSD.string,
    "name": XSD.string,
    "originalName": XSD.string,
    "popularity": XSD.float,
    "profilePath": XSD.string,
    "castID": XSD.integer,
    "character": XSD.string,
    "creditID": XSD.string,
    "order": XSD.integer
}
for prop, range_ in data_property_ranges.items():
    g.add((movie_ns[prop], RDFS.range, range_))


def person_exists(graph, person_id):
    query = f"""
    PREFIX movie: <http://www.semanticweb.org/quentin/ontologies/2024/5/movie/>
    ASK WHERE {{
        ?person rdf:type movie:Person .
        ?person movie:id {person_id} .
    }}
    """
    return bool(graph.query(query))


def add_person(graph, person_data):
    person_id = person_data['id']
    if not person_exists(graph, person_id):
        person_uri = URIRef(movie_ns[f'Person{person_id}'])
        graph.add((person_uri, RDF.type, movie_ns.Person))
        graph.add((person_uri, movie_ns.id, Literal(person_id, datatype=XSD.integer)))
        graph.add((person_uri, movie_ns.name, Literal(person_data['name'], datatype=XSD.string)))
        graph.add((person_uri, movie_ns.originalName, Literal(person_data['original_name'], datatype=XSD.string)))
        graph.add((person_uri, movie_ns.gender, Literal(person_data['gender'], datatype=XSD.integer)))
        graph.add((person_uri, movie_ns.knownForDepartment,
                   Literal(person_data['known_for_department'], datatype=XSD.string)))
        graph.add((person_uri, movie_ns.popularity, Literal(person_data['popularity'], datatype=XSD.float)))
        graph.add((person_uri, movie_ns.profilePath, Literal(person_data['profile_path'], datatype=XSD.string)))
        graph.add((person_uri, movie_ns.castID, Literal(person_data['cast_id'], datatype=XSD.integer)))
        graph.add((person_uri, movie_ns.character, Literal(person_data['character'], datatype=XSD.string)))
        graph.add((person_uri, movie_ns.creditID, Literal(person_data['credit_id'], datatype=XSD.string)))
        graph.add((person_uri, movie_ns.order, Literal(person_data['order'], datatype=XSD.integer)))
    return URIRef(movie_ns[f'Person{person_id}'])


def add_credits(graph, movie_id):
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=en-US"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json;charset=utf-8',
    }

    try:
        response = requests.get(credits_url, headers=headers)
    except requests.exceptions.ConnectionError:
        time.sleep(10)
        response = requests.get(credits_url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.json()}")
        time.sleep(10)
        response = requests.get(credits_url, headers=headers)

    credits_data = response.json()

    movie_uri = URIRef(movie_ns[f'Movie{movie_id}'])
    for person_data in credits_data['cast']:
        person_uri = add_person(graph, person_data)
        graph.add((movie_uri, movie_ns.hasPerson, person_uri))


def movie_exists(graph, movie_id):
    query = f"""
    PREFIX movie: <http://www.semanticweb.org/quentin/ontologies/2024/5/movie/>
    ASK WHERE {{
        ?movie rdf:type movie:Movie .
        ?movie movie:id {movie_id} .
    }}
    """
    return bool(graph.query(query))


def collection_exists(graph, collection_id):
    query = f"""
    PREFIX movie: <http://www.semanticweb.org/quentin/ontologies/2024/5/movie/>
    ASK WHERE {{
        ?collection rdf:type movie:Collection .
        ?collection movie:collectionID {collection_id} .
    }}
    """
    return bool(graph.query(query))


def genre_exists(graph, genre_id):
    query = f"""
    PREFIX movie: <http://www.semanticweb.org/quentin/ontologies/2024/5/movie/>
    ASK WHERE {{
        ?genre rdf:type movie:Genre .
        ?genre movie:id {genre_id} .
    }}
    """
    return bool(graph.query(query))


def add_all_movies_from_collection(collection_id):
    collection_url = f"https://api.themoviedb.org/3/collection/{collection_id}?language=en-US"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json;charset=utf-8',
    }

    try:
        response = requests.get(collection_url, headers=headers)
    except requests.exceptions.ConnectionError:
        time.sleep(10)
        response = requests.get(collection_url, headers=headers)

    for movie in response.json()['parts']:
        add_movie(g, get_movie_details(movie['id']))

    print(f"Movies from collection {collection_id} added.")


def add_collection(graph, collection_data):
    collection_id = collection_data['id']
    collection_uri = URIRef(movie_ns[f'Collection{collection_id}'])
    if not collection_exists(graph, collection_id):
        graph.add((collection_uri, RDF.type, movie_ns.Collection))
        graph.add((collection_uri, movie_ns.collectionID, Literal(collection_id, datatype=XSD.integer)))
        graph.add((collection_uri, movie_ns.collectionName, Literal(collection_data['name'], datatype=XSD.string)))
        graph.add(
            (collection_uri, movie_ns.collectionImage, Literal(collection_data['poster_path'], datatype=XSD.string)))
        add_all_movies_from_collection(collection_id)
        print(f"Collection {collection_data["name"]} added.")
    return collection_uri


def add_movie(graph, movie_data):
    movie_id = movie_data['id']
    if not movie_exists(graph, movie_id):
        movie_uri = URIRef(movie_ns[f'Movie{movie_id}'])
        graph.add((movie_uri, RDF.type, movie_ns.Movie))
        graph.add((movie_uri, movie_ns.id, Literal(movie_id, datatype=XSD.integer)))
        graph.add((movie_uri, movie_ns.title, Literal(movie_data['title'], datatype=XSD.string)))
        graph.add((movie_uri, movie_ns.image, Literal(movie_data['poster_path'], datatype=XSD.string)))
        graph.add((movie_uri, movie_ns.imdbID, Literal(movie_data['imdb_id'], datatype=XSD.string)))
        graph.add((movie_uri, movie_ns.overview, Literal(movie_data['overview'], datatype=XSD.string)))
        if movie_data['release_date'] != '':
            graph.add((movie_uri, movie_ns.releaseDate, Literal(movie_data['release_date'], datatype=XSD.date)))
        graph.add((movie_uri, movie_ns.adult, Literal(movie_data['adult'], datatype=XSD.boolean)))
        graph.add((movie_uri, movie_ns.popularity, Literal(movie_data['popularity'], datatype=XSD.float)))

        if 'belongs_to_collection' in movie_data and movie_data['belongs_to_collection'] is not None:
            collection_data = movie_data['belongs_to_collection']
            collection_uri = add_collection(graph, collection_data)
            graph.add((movie_uri, movie_ns.hasCollection, collection_uri))  # Link movie to collection here

        for genre in movie_data['genres']:
            genre_uri = URIRef(movie_ns[f'Genre{genre["id"]}'])
            if not genre_exists(graph, genre['id']):
                graph.add((genre_uri, RDF.type, movie_ns.Genre))
                graph.add((genre_uri, movie_ns.id, Literal(genre['id'], datatype=XSD.integer)))
                graph.add((genre_uri, movie_ns.name, Literal(genre['name'], datatype=XSD.string)))
            graph.add((movie_uri, movie_ns.hasGenre, genre_uri))

        add_credits(graph, movie_id)
        print(f"Movie {movie_data['title']} added.")


ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YTk3ZmJhNjI4NzE5YzA1NDA1NDljYjc0MGI2Njk5ZSIsInN1YiI6IjY2NjAzYWI0NWFhNzY1ZmQxOWU5OTA4ZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.drVq5gu4Wq9x_-wVUJQ_IFSXuECK43a4oZizK1JHQ9w"


def get_movie_by_year(year, page=1):
    for i in range(0, 10):
        print(f"Getting movies from {year - i}...")
        discover_url = f"https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=en-US&page={page}&sort_by=popularity.desc&year={year - i}"
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}',
            'Content-Type': 'application/json;charset=utf-8',
        }
        try:
            response = requests.get(discover_url, headers=headers)
        except requests.exceptions.ConnectionError:
            time.sleep(10)
            response = requests.get(discover_url, headers=headers)

        if response.status_code != 200:
            print(f"Error: {response.json()}")
            time.sleep(10)
            response = requests.get(discover_url, headers=headers)
        else:
            for movie in response.json()['results']:
                add_movie(g, get_movie_details(movie['id']))

        discover_url = f"https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=en-US&sort_by=popularity.desc&year={year - i}"

        max = 0

        if response.json()['total_pages'] > 20:
            max = 20
        else:
            max = response.json()['total_pages']

        for j in range(2, max):
            print(f"Getting page {j} / {response.json()['total_pages']}...")
            try:
                response = requests.get(f"{discover_url}&page={j}", headers=headers)
            except requests.exceptions.ConnectionError:
                time.sleep(10)
                response = requests.get(f"{discover_url}&page={j}", headers=headers)

            if response.status_code != 200:
                print(f"Error: {response.json()}")
                time.sleep(10)
                response = requests.get(f"{discover_url}&page={j}", headers=headers)
            else:
                print(f"Got page {j} / {len(response.json()['results'])}...")
                for movie in response.json()['results']:
                    add_movie(g, get_movie_details(movie['id']))


def get_movie_details(id):
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json;charset=utf-8',
    }
    movie_details_url = f'https://api.themoviedb.org/3/movie/{id}'
    try:
        response = requests.get(movie_details_url, headers=headers)
    except requests.exceptions.ConnectionError:
        time.sleep(10)
        response = requests.get(movie_details_url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.json()}")
        time.sleep(10)
        response = requests.get(movie_details_url, headers=headers)
    return response.json()


get_movie_by_year(2024)

# Serialize the graph to RDF/XML format and save it to a file
g.serialize(destination='movies.owl', format='xml')

print("Ontology saved to 'movies.owl'")
