<template>
  <div class="breadcrumb">
    <div class="breadcrumb-container">
      <a
        v-for="(item, index) in breadcrumbs"
        :key="index"
        :href="item.path"
        :class="['breadcrumb-item', { active: index === breadcrumbs.length - 1 }]"
        @click.prevent="handleClick(item.path, index)"
      >
        {{ item.label }}
        <span v-if="index < breadcrumbs.length - 1" class="separator">></span>
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

interface BreadcrumbItem {
  label: string
  path: string
}

const route = useRoute()
const router = useRouter()

const breadcrumbs = computed<BreadcrumbItem[]>(() => {
  const items: BreadcrumbItem[] = [{ label: '首页', path: '/' }]
  if (route.path !== '/') {
    const title = (route.meta.title as string) || '报价'
    items.push({ label: title, path: route.path })
  }
  return items
})

const handleClick = (path: string, index: number) => {
  if (index < breadcrumbs.value.length - 1) {
    router.push(path)
  }
}
</script>

<style scoped>
.breadcrumb {
  background-color: white;
  border-bottom: 1px solid var(--border-color);
  padding: var(--spacing-md) 0;
}

.breadcrumb-container {
  max-width: 1920px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.breadcrumb-item {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: var(--font-size-sm);
  transition: color 0.2s;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.breadcrumb-item:not(.active):hover {
  color: var(--primary-color);
}

.breadcrumb-item.active {
  color: var(--text-primary);
  font-weight: 500;
  cursor: default;
}

.separator {
  color: var(--text-disabled);
  margin: 0 var(--spacing-xs);
}

@media (max-width: 768px) {
  .breadcrumb-container {
    padding: 0 var(--spacing-md);
  }

  .breadcrumb-item {
    font-size: var(--font-size-xs);
  }
}
</style>
