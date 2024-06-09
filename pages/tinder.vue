<template>
  <div v-if="error" class="w-full flex justify-center">
    <AlertError title="An error occurred" :errors="errorMessages" class="w-4/5"/>
  </div>
  <div v-else class="w-full">
    <div class="h-full flex justify-center items-center flex-col">
      <img :src="'https://image.tmdb.org/t/p/original' + movies[index].image.value" :alt="movies[index].title.value" class="w-96 h-96 " />
      <h1 class="mb-5 mt-5 font-bold text-xl w-96 text-white">{{ movies[index].title.value }}</h1>
      <p class="w-96 text-white">{{ movies[index].overview.value }}</p>
      <div class="w-96 flex justify-between mt-5">
        <p class="text-white">{{ movies[index].releaseDate.value }}</p>
        <p class="text-white">{{ movies[index].popularity.value }} <Icon name="mdi:fire"></Icon> </p>
      </div>
      <div class="w-96 flex justify-between mt-5">
        <button @click="choice(false)" type="button" class="rounded-full bg-red-600 p-2 text-white shadow-sm hover:bg-red-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
          <XMarkIcon class="h-10 w-10" aria-hidden="true" />
        </button>
        <button @click="choice(true)" type="button" class="rounded-full bg-indigo-600 p-2 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
          <HeartIcon class="h-10 w-10" aria-hidden="true" />
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>

import { PlusIcon, HeartIcon, XMarkIcon } from '@heroicons/vue/20/solid'
import AlertError from "~/components/AlertError.vue";

useHead({
  htmlAttrs: {
    class: 'h-full bg-white dark:bg-gray-900'
  },
  bodyAttrs: {
    class: 'h-full'
  }
})

const config = useConfigStore()
const runtimeConfig = useRuntimeConfig()
const requestError = ref<boolean>(false)
const movies = ref<Record<string, any>[]>([])
const index = ref<number>(0)

let body = ""

if (config.type === 'popularity') {
  body = `
      PREFIX movie: <http://www.semanticweb.org/quentin/ontologies/2024/5/movie/>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
      PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

      SELECT ?movie ?id ?title ?image ?imdbID ?overview ?releaseDate ?adult ?popularity
      WHERE {
        ?movie rdf:type movie:Movie .
        ?movie movie:id ?id .
        ?movie movie:title ?title .
        ?movie movie:image ?image .
        ?movie movie:imdbID ?imdbID .
        ?movie movie:overview ?overview .
        ?movie movie:releaseDate ?releaseDate .
        ?movie movie:adult ?adult .
        ?movie movie:popularity ?popularity .
      }
      ORDER BY DESC(?popularity)
      LIMIT 20
  `;
} else if (config.type === 'random') {
  body = `
      PREFIX movie: <http://www.semanticweb.org/quentin/ontologies/2024/5/movie/>
      PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
      PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

      SELECT ?movie ?id ?title ?image ?imdbID ?overview ?releaseDate ?adult ?popularity
      WHERE {
        ?movie rdf:type movie:Movie .
        ?movie movie:id ?id .
        ?movie movie:title ?title .
        ?movie movie:image ?image .
        ?movie movie:imdbID ?imdbID .
        ?movie movie:overview ?overview .
        ?movie movie:releaseDate ?releaseDate .
        ?movie movie:adult ?adult .
        ?movie movie:popularity ?popularity .
      }
      ORDER BY RAND()
      LIMIT 20
    `;
}

const { data, pending, error, refresh } = await useFetch(runtimeConfig.public.fusekiEndpoint, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/sparql-results+json'
  },
  body: new URLSearchParams({
    query: body
  })
})

const errorMessages = ref<string[]>([])

if (error && error.value) {
  console.error(error.value.data)
  requestError.value = true
  errorMessages.value[0] = error.value.data
  errorMessages.value[1] = "Verify that the Fuseki server is running at " + runtimeConfig.public.fusekiEndpoint
  errorMessages.value[2] = "Verify the dataset is named 'movie' and the ontology is loaded."
  errorMessages.value[3] = "Try refreshing the page or go back to the home page."
  errorMessages.value[4] = "If the problem persists, contact the administrator."
} else {
  if (data.value && data.value.results) {
    movies.value = data.value.results.bindings
  }
}

const choice = (like: boolean) => {
  if (like) {
    config.addLikedMovie(movies.value[index.value].id.value)
  } else {
    config.addDislikedMovie(movies.value[index.value].id.value)
  }
  if (index.value === movies.value.length - 1) {
    const router = useRouter()
    router.push("/recommendations")
  } else {
    index.value++
  }
}



</script>
