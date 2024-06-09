<template>
  <header class="bg-white dark:bg-gray-900">
    <nav class="mx-auto flex max-w-7xl items-center justify-between p-6 lg:px-8" aria-label="Global">
      <div class="flex lg:flex-1">
        <a href="#" class="-m-1.5 p-1.5 flex justify-center items-center text-center">
          <span class="sr-only">Your Company</span>
          <img class="h-8 w-auto" src="/logo.jpeg" alt="" />
          <span class="ml-2 text-lg font-semibold leading-6 text-gray-900 dark:text-white">Tinder Movies</span>
        </a>
      </div>
      <div class="flex lg:hidden">
        <button type="button" class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700 dark:text-gray-400" @click="mobileMenuOpen = true">
          <span class="sr-only">Open main menu</span>
          <Bars3Icon class="h-6 w-6" aria-hidden="true" />
        </button>
      </div>
      <div class="hidden lg:flex lg:gap-x-12">
        <a v-for="item in navigation" :key="item.name" :href="item.href" class="text-sm font-semibold leading-6 text-gray-900 dark:text-white">{{ item.name }}</a>
      </div>
      <div class="hidden lg:flex lg:flex-1 lg:justify-end">
        <Icon name="material-symbols:sunny" @click="colorMode.preference === 'light' ? colorMode.preference = 'dark' : colorMode.preference = 'light'" class="h-6 w-6 text-gray-900 dark:text-white" />
      </div>
    </nav>
    <Dialog class="lg:hidden" @close="mobileMenuOpen = false" :open="mobileMenuOpen">
      <div class="fixed inset-0 z-10" />
      <DialogPanel class="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10 dark:bg-gray-900 dark:sm:ring-white/10">
        <div class="flex items-center justify-between">
          <a href="#" class="-m-1.5 p-1.5 flex justify-center items-center text-center">
            <span class="sr-only">Your Company</span>
            <img class="h-8 w-auto" src="/logo.jpeg" alt="" />
            <span class="ml-2 text-lg font-semibold leading-6 text-gray-900 dark:text-white">Tinder Movies</span>
          </a>
          <button type="button" class="-m-2.5 rounded-md p-2.5 text-gray-700 dark:text-gray-400" @click="mobileMenuOpen = false">
            <span class="sr-only">Close menu</span>
            <XMarkIcon class="h-6 w-6" aria-hidden="true" />
          </button>
        </div>
        <div class="mt-6 flow-root">
          <div class="-my-6 divide-y divide-gray-500/10 dark:text-gray-400">
            <div class="space-y-2 py-6">
              <a v-for="item in navigation" :key="item.name" :href="item.href" class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50 dark:text-white dark:hover:bg-gray-800 dark:text-white dark:hover:bg-gray-800">{{ item.name }}</a>
            </div>
            <div class="py-6">
              <Icon name="material-symbols:sunny" @click="colorMode.preference === 'light' ? colorMode.preference = 'dark' : colorMode.preference = 'light'" class="h-6 w-6 text-gray-900 dark:text-white" />
            </div>
          </div>
        </div>
      </DialogPanel>
    </Dialog>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Dialog, DialogPanel } from '@headlessui/vue'
import { Bars3Icon, XMarkIcon } from '@heroicons/vue/24/outline'

const navigation = [
]

const mobileMenuOpen = ref(false)

const colorMode = useColorMode();
</script>
