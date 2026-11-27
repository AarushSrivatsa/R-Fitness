<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const menuOpen = ref(false)
watch(() => route.fullPath, () => { menuOpen.value = false })
</script>

<template>
  <header class="site-header">
    <nav class="navbar navbar-expand-lg container-xl py-3" aria-label="Main navigation">
      <RouterLink class="brand-mark" to="/" aria-label="R Fitness home">
        <span class="brand-icon">R</span>
        <span class="brand-copy">R<span>FITNESS</span></span>
      </RouterLink>

      <button class="navbar-toggler custom-toggler" type="button" aria-label="Toggle navigation" @click="menuOpen = !menuOpen">
        <i class="bi" :class="menuOpen ? 'bi-x-lg' : 'bi-list'"></i>
      </button>

      <div class="collapse navbar-collapse" :class="{ show: menuOpen }">
        <ul class="navbar-nav ms-auto align-items-lg-center gap-lg-4">
          <li class="nav-item"><a class="nav-link" href="/#about">About</a></li>
          <li class="nav-item"><a class="nav-link" href="/#training">Training</a></li>
          <li class="nav-item"><a class="nav-link" href="/#membership">Membership</a></li>
          <li class="nav-item"><a class="nav-link" href="/#location">Find us</a></li>
          <li class="nav-item mt-3 mt-lg-0">
            <a class="btn btn-accent nav-cta" href="/#enquire">START YOUR JOURNEY <i class="bi bi-arrow-up-right ms-2"></i></a>
          </li>
        </ul>
      </div>
    </nav>
  </header>
</template>
