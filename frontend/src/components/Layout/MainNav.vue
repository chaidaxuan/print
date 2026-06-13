<template>
  <nav class="main-nav">
    <div class="nav-container">
      <div class="nav-items">
        <a
          v-for="item in navItems"
          :key="item.path"
          :href="item.path"
          :class="['nav-item', { active: currentPath === item.path }]"
          @click.prevent="handleNavClick(item.path)"
        >
          {{ item.label }}
        </a>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

interface NavItem {
  label: string
  path: string
}

const navItems: NavItem[] = [
  { label: '首页', path: '/' },
  { label: '报价', path: '/quote/liandan' },
  { label: '彩盒', path: '/caihe' },
  { label: '管理', path: '/manage' },
  { label: '参数', path: '/params' },
  { label: '通知', path: '/notification' }
]

const route = useRoute()
const router = useRouter()

const currentPath = computed(() => route.path)

const handleNavClick = (path: string) => {
  router.push(path)
}
</script>

<style scoped>
.main-nav {
  background-color: var(--nav-bg);
  height: 34px;
}

.nav-container {
  max-width: 100%;
  margin: 0 auto;
  height: 100%;
  padding: 0;
}

.nav-items {
  display: flex;
  align-items: stretch;
  height: 100%;
  gap: 0;
}

.nav-item {
  color: var(--nav-text);
  text-decoration: none;
  padding: 0 var(--spacing-lg);
  font-size: var(--font-size-sm);
  display: flex;
  align-items: center;
  transition: background-color 0.2s;
  cursor: pointer;
}

.nav-item:hover {
  background-color: var(--nav-bg-hover);
  color: #fff;
}

.nav-item.active {
  background-color: var(--nav-active-bg);
  color: #fff;
}

@media (max-width: 768px) {
  .nav-container {
    padding: 0 var(--spacing-md);
  }

  .nav-items {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }

  .nav-items::-webkit-scrollbar {
    display: none;
  }

  .nav-item {
    padding: var(--spacing-xs) var(--spacing-md);
    white-space: nowrap;
  }
}
</style>
