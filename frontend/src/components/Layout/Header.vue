<template>
  <header class="app-header">
    <div class="header-container">
      <div class="header-left">
        <h1 class="system-title">印刷报价系统</h1>
      </div>
      <div class="header-right">
        <span class="user-id">{{ userId }}</span>
        <a href="#" class="header-link" @click.prevent="handleChangePassword">修改密码</a>
        <a href="#" class="header-link" @click.prevent="handleLogout">安全退出</a>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const userId = ref('DEMO-USER')

const handleChangePassword = () => {
  console.log('修改密码')
  // TODO: 实现修改密码逻辑
}

const handleLogout = () => {
  console.log('安全退出')
  // TODO: 实现退出逻辑
}
</script>

<style scoped>
.app-header {
  background: var(--header-bg);
  color: var(--header-text);
  height: 34px;
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-container {
  max-width: 100%;
  margin: 0 auto;
  height: 100%;
  padding: 0 var(--spacing-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
}

.system-title {
  font-size: var(--font-size-xl);
  font-weight: 400;
  margin: 0;
  letter-spacing: 1px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.user-id {
  font-size: var(--font-size-sm);
  padding: 1px var(--spacing-sm);
}

.header-link {
  color: var(--header-text);
  text-decoration: none;
  font-size: var(--font-size-sm);
  transition: opacity 0.2s;
}

.header-link:hover {
  opacity: 0.85;
  text-decoration: underline;
}

@media (max-width: 768px) {
  .header-container {
    padding: 0 var(--spacing-sm);
  }

  .system-title {
    font-size: var(--font-size-md);
  }

  .header-right {
    gap: var(--spacing-sm);
  }
}
</style>
