<template>
  <div class="home-page">
    <div class="category-section">
      <h2 class="section-title">报价系统功能演示</h2>
      <p class="section-tip">
        演示用的报价参数与实际数据不同，计算结果与手算存在差异属正常现象。
      </p>
      <ul class="category-grid">
        <li
          v-for="cat in categories"
          :key="cat.code"
          class="category-item"
          :class="{ disabled: !cat.enabled }"
          @click="handleCategoryClick(cat)"
        >
          <div class="category-icon" :style="{ background: cat.color }">
            {{ cat.label.slice(0, 1) }}
          </div>
          <p class="category-name">{{ cat.label }}</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

interface Category {
  label: string
  code: string
  color: string
  enabled: boolean
  path?: string
}

const router = useRouter()

// 品类列表参考行业通用印刷品类，联单已接通报价功能，其余为占位
const categories: Category[] = [
  { label: '表格便笺', code: 'biaoge', color: '#5b8def', enabled: false },
  { label: '彩盒彩箱', code: 'caihe', color: '#f4845f', enabled: false },
  { label: '专版不干胶', code: 'buganjiao', color: '#48c79c', enabled: false },
  { label: '纸盒纸箱', code: 'zhihe', color: '#9b8cff', enabled: false },
  { label: '纸袋', code: 'zhidai', color: '#f4b740', enabled: false },
  { label: '特价不干胶', code: 'tj-buganjiao', color: '#56ccf2', enabled: false },
  { label: '精品盒', code: 'jingpin', color: '#f47fb0', enabled: false },
  { label: '专版画册', code: 'huace', color: '#7ec8a0', enabled: false },
  { label: '特价单张', code: 'danzhang', color: '#6ba4f0', enabled: false },
  { label: '信封', code: 'xinfeng', color: '#f49a5f', enabled: false },
  { label: '手提袋', code: 'shouti', color: '#52c4b8', enabled: false },
  { label: '专版单页', code: 'danye', color: '#a98cff', enabled: false },
  { label: '彩卡吊牌', code: 'caika', color: '#f4c040', enabled: false },
  { label: '封套', code: 'fengtao', color: '#5fc6f0', enabled: false },
  { label: '游戏卡牌', code: 'kapai', color: '#f47f97', enabled: false },
  { label: '笔记本', code: 'biji', color: '#7ec88a', enabled: false },
  { label: '无碳联单', code: 'liandan', color: '#e74c3c', enabled: true, path: '/quote/liandan' },
  { label: '特价联单', code: 'tj-liandan', color: '#6ba4f0', enabled: false },
  { label: '数码打印', code: 'shuma', color: '#f49a5f', enabled: false }
]

const handleCategoryClick = (cat: Category) => {
  if (cat.enabled && cat.path) {
    router.push(cat.path)
  }
}
</script>

<style scoped>
.home-page {
  width: 100%;
}

.category-section {
  background: white;
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-xl);
}

.section-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.section-tip {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-md);
  background: #fff8e6;
  border-left: 3px solid var(--warning-color);
  border-radius: var(--border-radius-sm);
}

.category-grid {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: var(--spacing-lg);
}

.category-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-lg) var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  transition: all 0.2s;
}

.category-item:not(.disabled):hover {
  border-color: var(--primary-color);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.category-item.disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.category-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--border-radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: var(--font-size-xl);
  font-weight: 600;
}

.category-name {
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  text-align: center;
}

@media (max-width: 768px) {
  .category-section {
    padding: var(--spacing-lg);
  }

  .category-grid {
    grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
    gap: var(--spacing-md);
  }

  .category-icon {
    width: 44px;
    height: 44px;
    font-size: var(--font-size-md);
  }
}
</style>
