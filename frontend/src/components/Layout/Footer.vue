<template>
  <footer class="app-footer">
    <div class="footer-container">
      <p class="footer-text">
        公司名称：印刷报价系统有限公司 |
        地址：中国 |
        电话：000-00000000 |
        <a href="#" class="footer-link">备案号</a>
      </p>
    </div>
  </footer>
</template>

<script setup lang="ts">
</script>

<style scoped>
.app-footer {
  background-color: #2c3e50;
  color: rgba(255, 255, 255, 0.7);
  padding: var(--spacing-lg) 0;
  margin-top: auto;
}

.footer-container {
  max-width: 1920px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
  text-align: center;
}

.footer-text {
  font-size: var(--font-size-xs);
  margin: 0;
}

.footer-link {
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  transition: color 0.2s;
}

.footer-link:hover {
  color: white;
  text-decoration: underline;
}

@media (max-width: 768px) {
  .footer-container {
    padding: 0 var(--spacing-md);
  }

  .footer-text {
    font-size: 10px;
    line-height: 1.6;
  }
}
</style>
