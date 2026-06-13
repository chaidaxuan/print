<template>
  <div class="app-container">
    <Header />
    <MainNav />
    <div class="main-content">
      <Breadcrumb />
      <div class="content-wrapper">
        <router-view />
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import Header from './components/Layout/Header.vue'
import MainNav from './components/Layout/MainNav.vue'
import Breadcrumb from './components/Layout/Breadcrumb.vue'
import Footer from './components/Layout/Footer.vue'
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-width: 1024px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.content-wrapper {
  flex: 1;
  padding: var(--spacing-lg);
  max-width: 1920px;
  margin: 0 auto;
  width: 100%;
}

@media (max-width: 768px) {
  .app-container {
    min-width: 100%;
  }

  .content-wrapper {
    padding: var(--spacing-md);
  }
}
</style>
