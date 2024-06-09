export const useConfigStore = defineStore('config', () => {
  const likedMovies = ref<string[]>([])
  const dislikedMovies = ref<string[]>([])
  const type = ref<string>('') // <--- Add this line

  const addLikedMovie = (movie: string) => {
    likedMovies.value.push(movie)
  }

  const addDislikedMovie = (movie: string) => {
    dislikedMovies.value.push(movie)
  }

  const setType = (tinderType: string) => {
    type.value = tinderType
  }

  return {
    likedMovies,
    dislikedMovies,
    type,
    addLikedMovie,
    addDislikedMovie,
    setType
  }
})
