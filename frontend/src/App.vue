<template>
  <div class="app-container">
    <BrandBar />
    <div class="app-window">
      <DemoBar />
      <div class="window-tabs">
        <div class="tab active">
          <span>首页</span>
          <span class="tab-close">×</span>
        </div>
        <button class="contact-btn" @click.prevent>点击联系客服</button>
      </div>
      <div class="window-body">
        <SideNav />
        <main class="window-content">
          <router-view />
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import BrandBar from './components/Layout/BrandBar.vue'
import DemoBar from './components/Layout/DemoBar.vue'
import SideNav from './components/Layout/SideNav.vue'
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  min-width: 1024px;
  background: #ffffff;
}

.app-window {
  max-width: 1180px;
  width: 100%;
  margin: 0 auto var(--spacing-xl);
  border: 1px solid #9ec3e0;
  border-top: none;
  display: flex;
  flex-direction: column;
  background: #ffffff;
}

.window-tabs {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  background: #f4f4f4;
  border-bottom: 1px solid #9ec3e0;
  padding: var(--spacing-sm) var(--spacing-md) 0;
}

.tab {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  background: #ffffff;
  border: 1px solid #9ec3e0;
  border-bottom: none;
  border-radius: var(--border-radius-sm) var(--border-radius-sm) 0 0;
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-sm);
  color: var(--text-primary);
}

.tab.active {
  color: var(--primary-color);
}

.tab-close {
  color: var(--text-disabled);
  cursor: pointer;
}

.contact-btn {
  margin-bottom: var(--spacing-sm);
  background: linear-gradient(180deg, #fbb040 0%, #f59e1b 100%);
  color: #ffffff;
  border: none;
  border-radius: var(--border-radius-sm);
  padding: var(--spacing-sm) var(--spacing-lg);
  font-size: var(--font-size-sm);
  cursor: pointer;
}

.contact-btn:hover {
  filter: brightness(1.05);
}

.window-body {
  display: flex;
  align-items: stretch;
  min-height: 560px;
}

.window-content {
  flex: 1;
  padding: var(--spacing-md);
  overflow: auto;
}

@media (max-width: 768px) {
  .app-container {
    min-width: 100%;
  }
}
</style>
