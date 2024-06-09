<script setup lang="ts">

const config = useConfigStore()
const movieIds = config.likedMovies
const dislikedMovies = config.dislikedMovies

console.log(movieIds)
//['653346', '940721', '786892', '693134', '1011985']
const valuesClause = movieIds.map((id) => `${id}`).join(' ');
const valuesClauseDisliked = dislikedMovies.map((id) => `${id}`).join(' ');

// filter need to be done on the movieIds and dislikedMovies separeted by a comma for each

console.log(valuesClause);
// Define the SPARQL query to fetch for each id movie only the collection of each movies if they have hasCollection property
const sparqlQuery = `
PREFIX movie: <http://www.semanticweb.org/quentin/ontologies/2024/5/movie/>

SELECT ?movie ?collection ?collection_id ?collection_name ?movie_id ?title ?image ?imdbID ?overview ?releaseDate ?adult ?popularity
WHERE {
  ?movie movie:hasCollection ?collection .
  ?collection movie:collectionID ?collection_id .
  ?collection movie:collectionName ?collection_name .
  ?movie movie:id ?movie_id .
  ?movie movie:title ?title .
  ?movie movie:image ?image .
  ?movie movie:imdbID ?imdbID .
  ?movie movie:overview ?overview .
  ?movie movie:releaseDate ?releaseDate .
  ?movie movie:adult ?adult .
  ?movie movie:popularity ?popularity .
  {
    SELECT ?collection
    WHERE {
      VALUES ?movie_id {
        ${valuesClause}
      }
      ?movie movie:id ?movie_id .
      ?movie movie:hasCollection ?collection .
    }
  }
}
`;


const sparqlQueryTopGenresAndMovies = `
PREFIX movie: <http://www.semanticweb.org/quentin/ontologies/2024/5/movie/>

SELECT DISTINCT ?movie ?title ?image ?imdbID ?overview ?releaseDate ?adult ?popularity
WHERE {
  {
    SELECT ?genre (COUNT(?movie) AS ?count)
    WHERE {
      VALUES ?movie_id {
        ${valuesClause}
      }
      ?movie movie:id ?movie_id .
      ?movie movie:hasGenre ?genre .
    }
    GROUP BY ?genre
    ORDER BY DESC(?count)
    LIMIT 3
  }
  ?movie movie:hasGenre ?genre .
  ?movie movie:id ?movie_id .
  FILTER (?movie_id NOT IN (${movieIds.join(', ')} , ${dislikedMovies.join(', ')}))
  ?movie movie:title ?title .
  ?movie movie:image ?image .
  ?movie movie:imdbID ?imdbID .
  ?movie movie:overview ?overview .
  ?movie movie:releaseDate ?releaseDate .
  ?movie movie:adult ?adult .
  ?movie movie:popularity ?popularity .
}
${config.type === 'popularity' ? 'ORDER BY DESC(?popularity)' : 'ORDER BY RAND()'}
LIMIT 50
`;

const runtimeConfig = useRuntimeConfig()
// Define the Fuseki endpoint
const fusekiEndpoint = runtimeConfig.public.fusekiEndpoint

// Define the headers

const headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Accept': 'application/sparql-results+json'
};


// Fetch the data

const getTopGenresAndMovies = async () => {
  const { data, pending, error, refresh } = await useFetch(fusekiEndpoint, {
    method: 'POST',
    headers: headers,
    body: new URLSearchParams({
      query: sparqlQueryTopGenresAndMovies
    })
  });

  return data;
}

const { data, pending, error, refresh } = await useFetch(fusekiEndpoint, {
  method: 'POST',
  headers: headers,
  body: new URLSearchParams({
    query: sparqlQuery
  })
});

const topGenresMovies = ref<Record<string, any>>(await getTopGenresAndMovies());

console.log(topGenresMovies.value);

const moviesByCollection = ref<Record<string, Record<string, any>>>({});

function organizeMoviesByCollection(queryResult: Record<string, any>[]) {

  queryResult.forEach(result => {
    const collectionID = result.collection_id.value;
    const movie = {
      id: result.movie_id.value,
      title: result.title.value,
      image: result.image.value,
      imdbID: result.imdbID.value,
      overview: result.overview.value,
      releaseDate: result.releaseDate.value,
      adult: result.adult.value,
      popularity: result.popularity.value
    };

    if (!moviesByCollection.value[collectionID]) {
      moviesByCollection.value[collectionID] = {
        collectionName: result.collection_name.value,
        collectionID: collectionID,
        movies: []
      };
    }

    moviesByCollection.value[collectionID].movies.push(movie);
  });

  return moviesByCollection;
}

// Create object by collection
if (data.value) {
  organizeMoviesByCollection(data.value.results.bindings);
}

const getMovieTitleLikedInCollection = (collectionId: string) => {
  const collection = moviesByCollection.value[collectionId];

  if (!collection) {
    return '';
  }

  const movies = collection.movies;

  if (!movies) {
    return '';
  }

  const movie = movies.find(movie => movieIds.includes(movie.id));

  return movie ? movie.title : '';
}

useHead({
  htmlAttrs: {
    class: 'h-full bg-white dark:bg-gray-900'
  },
  bodyAttrs: {
    class: 'h-full'
  }
})

</script>

<template>
  <div class="flex ml-5 w-90 flex-col">
    <div v-for="collection in moviesByCollection" class="mt-5">
      <h2 class="text-xl text-black dark:text-white"> {{ "Because you liked " + getMovieTitleLikedInCollection(collection.collectionID) + " you might like " + collection.collectionName }}</h2>
      <!-- create a small div with background of the movie and when the mouse is hover the title is shown in the middle of the image by fadeIn -->
      <div class="flex flex-row flex-wrap gap-4">
        <div v-for="movie in collection.movies" :key="movie.id" class="relative w-40 h-60">
          <div class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center opacity-0 transition-opacity duration-300 hover:opacity-100">
            <h3 class="text-white text-center">{{ movie.title }}</h3>
          </div>
          <img :src="'https://image.tmdb.org/t/p/original' + movie.image" :alt="movie.title" class="w-full h-full object-cover" />
        </div>
      </div>
    </div>
    <div v-if="topGenresMovies" class="flex flex-col mt-5">
      <h2 class="text-black dark:text-white">Movies based on your top genres</h2>
      <div class="flex flex-row flex-wrap gap-4">
        <div v-for="movie in topGenresMovies.results.bindings" :key="movie.imdbID.value" class="relative w-40 h-60">
          <div class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center opacity-0 transition-opacity duration-300 hover:opacity-100">
            <h3 class="text-white text-center">{{ movie.title.value }}</h3>
          </div>
          <img :src="'https://image.tmdb.org/t/p/original' + movie.image.value" :alt="movie.title.value" class="w-full h-full object-cover" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
