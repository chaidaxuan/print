<template>
  <aside class="side-nav">
    <a
      v-for="item in items"
      :key="item.path"
      :href="item.path"
      :class="['side-item', { active: isActive(item) }]"
      @click.prevent="go(item.path)"
    >
      {{ item.label }}
    </a>
    <div class="side-arrow" @click="goHome">›</div>
    <div class="side-spacer"></div>
    <a
      href="/notification"
      :class="['side-item', { active: currentPath === '/notification' }]"
      @click.prevent="go('/notification')"
    >通知</a>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

interface SideItem {
  label: string
  path: string
  match?: string
}

const items: SideItem[] = [
  { label: '首页', path: '/' },
  { label: '报价', path: '/quote/liandan', match: '/quote' },
  { label: '彩盒', path: '/caihe' },
  { label: '管理', path: '/manage' },
  { label: '参数', path: '/params' }
]

const route = useRoute()
const router = useRouter()

const currentPath = computed(() => route.path)

const isActive = (item: SideItem) => {
  if (item.path === '/') return route.path === '/'
  if (item.match) return route.path.startsWith(item.match)
  return route.path === item.path
}

const go = (path: string) => router.push(path)
const goHome = () => router.push('/')
</script>

<style scoped>
.side-nav {
  width: 56px;
  flex-shrink: 0;
  background: #767676;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.side-item {
  color: #ffffff;
  text-decoration: none;
  font-size: var(--font-size-sm);
  text-align: center;
  padding: var(--spacing-md) 0;
  cursor: pointer;
  transition: background-color 0.2s;
}

.side-item:hover {
  background: #5f5f5f;
}

.side-item.active {
  background: var(--primary-color);
}

.side-arrow {
  color: #ffffff;
  text-align: center;
  font-size: 22px;
  line-height: 1;
  padding: var(--spacing-sm) 0;
  cursor: pointer;
  font-weight: 700;
}

.side-spacer {
  flex: 1;
}
</style>
