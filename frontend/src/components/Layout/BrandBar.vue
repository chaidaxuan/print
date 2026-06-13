<template>
  <div class="brand-bar">
    <div class="brand-bar-inner">
      <div class="brand-left">
        <div class="brand-logo">
          <span class="logo-mark">优</span>
          <div class="logo-text">
            <span class="logo-cn">优效软件</span>
            <span class="logo-en">YOU XIAO RUAN JIAN</span>
          </div>
        </div>
        <h1 class="brand-title">印刷业务<span class="brand-title-strong">BMS</span>系统</h1>
      </div>
      <nav class="brand-nav">
        <a
          v-for="item in navItems"
          :key="item.label"
          href="#"
          class="brand-nav-item"
          @click.prevent
        >
          {{ item.label }}
        </a>
      </nav>
    </div>
  </div>
</template>

<script setup lang="ts">
interface BrandNavItem {
  label: string
}

const navItems: BrandNavItem[] = [
  { label: '首页' },
  { label: '印刷商城演示' },
  { label: '关于优效' },
  { label: 'BMS-业务管理' }
]
</script>

<style scoped>
.brand-bar {
  background: #ffffff;
  border-bottom: 3px solid #2f689f;
}

.brand-bar-inner {
  max-width: 1180px;
  margin: 0 auto;
  height: 76px;
  padding: 0 var(--spacing-md);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.logo-mark {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 3px solid #d12b1f;
  color: #d12b1f;
  font-size: 22px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.logo-cn {
  font-size: 20px;
  font-weight: 700;
  color: #d12b1f;
  letter-spacing: 1px;
}

.logo-en {
  font-size: 9px;
  color: #d12b1f;
  letter-spacing: 1px;
  transform: scaleX(0.92);
  transform-origin: left;
}

.brand-title {
  font-size: 30px;
  font-weight: 700;
  color: #d12b1f;
  margin: 0;
  letter-spacing: 2px;
}

.brand-title-strong {
  color: #d12b1f;
}

.brand-nav {
  display: flex;
  align-items: center;
  background: linear-gradient(180deg, #5b93d6 0%, #3f78bd 100%);
  border-radius: var(--border-radius-md);
  padding: 0 var(--spacing-xs);
  height: 40px;
}

.brand-nav-item {
  color: #ffffff;
  text-decoration: none;
  font-size: var(--font-size-md);
  padding: 0 18px;
  height: 100%;
  display: flex;
  align-items: center;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.brand-nav-item:hover {
  background-color: rgba(255, 255, 255, 0.18);
}
</style>
