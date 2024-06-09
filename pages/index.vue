<template>
  <div class="h-100 mt-52 flex justify-center items-center mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <!-- We've used 3xl here, but feel free to try other max-widths based on your needs -->
    <div class="mx-auto max-w-3xl flex gap-20">
      <button @click="goTo('popularity')" type="button" class="inline-flex items-center gap-x-2 rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
        Popularity
        <FireIcon class="-mr-0.5 h-5 w-5" aria-hidden="true" />
      </button>
      <button @click="goTo('random')" type="button" class="inline-flex items-center gap-x-2 rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
        Random
        <ArrowPathIcon class="-mr-0.5 h-5 w-5" aria-hidden="true" />
      </button>
    </div>
  </div>
</template>

<script lang="ts" setup>

import { CheckCircleIcon, FireIcon, ArrowPathIcon  } from '@heroicons/vue/20/solid'
import { useConfigStore } from '~/stores/config'

useHead({
  htmlAttrs: {
    class: 'h-full bg-white dark:bg-gray-900'
  },
  bodyAttrs: {
    class: 'h-full'
  }
})


const goTo = (route: string) => {
  const config = useConfigStore()

  config.setType(route)

  const router = useRouter()
  router.push("/tinder")
}

</script>
