<template>
  <div class="huace-quote-page">
    <div class="quote-top">
      <div class="gallery-section">
        <div class="main-image">
          <img src="/products/2.jpg" alt="专版画册" />
        </div>
      </div>
      <div class="form-section">
        <HuaceQuoteForm
          :loading="loading"
          @submit="handleCalculate"
        />
      </div>
    </div>

    <div class="price-section">
      <HuaceQuoteResult
        v-if="quoteResult"
        :result="quoteResult"
        :loading="loading"
      />
      <div v-else class="no-result">
        <p>请填写上方表单并点击"自助报价"按钮，结果将显示在此处</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import HuaceQuoteForm from '@/components/Huace/HuaceQuoteForm.vue'
import HuaceQuoteResult from '@/components/Huace/HuaceQuoteResult.vue'
import { calculateHuaceQuote } from '@/api/huace'
import type { HuaceQuoteRequest, HuaceQuoteResponse } from '@/types/huace'

const loading = ref(false)
const quoteResult = ref<HuaceQuoteResponse | null>(null)

const handleCalculate = async (data: HuaceQuoteRequest) => {
  loading.value = true
  try {
    const result = await calculateHuaceQuote(data)
    quoteResult.value = result
  } catch (error) {
    console.error('计算报价失败:', error)
    alert('计算报价失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.huace-quote-page {
  width: 100%;
}

.quote-top {
  display: flex;
  gap: var(--spacing-lg);
  align-items: flex-start;
  margin-bottom: var(--spacing-lg);
}

.gallery-section {
  flex: 0 0 360px;
  max-width: 360px;
}

.main-image {
  background: white;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  overflow: hidden;
  aspect-ratio: 1 / 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.form-section {
  flex: 1;
  min-width: 0;
}

.price-section {
  width: 100%;
}

.no-result {
  background-color: white;
  border-radius: var(--border-radius-md);
  padding: var(--spacing-xl);
  text-align: center;
  color: var(--text-secondary);
  box-shadow: var(--shadow-sm);
}

@media (max-width: 1024px) {
  .quote-top {
    flex-direction: column;
  }
  .gallery-section {
    flex: 1;
    max-width: 100%;
    width: 100%;
  }
  .form-section {
    width: 100%;
  }
}
</style>
