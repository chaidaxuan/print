<template>
  <div class="demo-bar">
    <div class="demo-bar-inner">
      <div class="demo-bar-left">
        <span class="demo-bar-title">报价软件功能演示报价系统</span>
        <span class="demo-bar-tip">
          给您<span class="tip-strike">免费</span><span class="tip-strike">试用</span>的软件，内设置的报价参数和您的实际数据不同，所以计算结果和你手算的会有不同是正常的
        </span>
      </div>
      <div class="demo-bar-right">
        <span class="demo-user">1708888</span>
        <a href="#" class="demo-link" @click.prevent>修改密码</a>
        <a href="#" class="demo-link" @click.prevent>安全退出</a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.demo-bar {
  background: linear-gradient(180deg, #2f9ad1 0%, #1f7fb8 100%);
  color: #ffffff;
}

.demo-bar-inner {
  max-width: 1180px;
  margin: 0 auto;
  height: 30px;
  padding: 0 var(--spacing-md);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.demo-bar-left {
  display: flex;
  align-items: baseline;
  gap: var(--spacing-md);
  overflow: hidden;
}

.demo-bar-title {
  font-size: var(--font-size-sm);
  font-weight: 700;
  color: #fff14d;
  white-space: nowrap;
}

.demo-bar-tip {
  font-size: var(--font-size-xs);
  color: rgba(255, 255, 255, 0.92);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tip-strike {
  color: #fff14d;
  text-decoration: line-through;
}

.demo-bar-right {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  white-space: nowrap;
}

.demo-user {
  font-size: var(--font-size-xs);
}

.demo-link {
  color: #ffffff;
  text-decoration: none;
  font-size: var(--font-size-xs);
}

.demo-link:hover {
  text-decoration: underline;
}
</style>
