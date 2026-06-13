<template>
  <div class="liandan-quote-page">
    <div class="quote-container">
      <!-- 左侧表单区 -->
      <div class="form-section">
        <QuoteForm
          v-model="formData"
          :loading="loading"
          @submit="handleCalculate"
        />
      </div>

      <!-- 右侧结果区 -->
      <div class="result-section">
        <QuoteResult
          v-if="quoteResult"
          :result="quoteResult"
          :loading="loading"
        />
        <div v-else class="no-result">
          <p>请填写左侧表单并点击"自助报价"按钮</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import QuoteForm from '@/components/Quote/QuoteForm.vue'
import QuoteResult from '@/components/Quote/QuoteResult.vue'
import { calculateLiandanQuote } from '@/api/quote'
import type { LiandanQuoteRequest, LiandanQuoteResponse } from '@/types/quote'

const loading = ref(false)
const formData = ref<LiandanQuoteRequest>({
  size_id: 1,
  quantity: 100,
  sheet_count: 3,
  pages_per_book: 99,
  color_code: 'single_black',
  gram_weight: 50,
  post_processing: ['binding_left'],
  customer_name: '',
  product_name: ''
})

const quoteResult = ref<LiandanQuoteResponse | null>(null)

const handleCalculate = async () => {
  loading.value = true
  try {
    const result = await calculateLiandanQuote(formData.value)
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
.liandan-quote-page {
  width: 100%;
}

.quote-container {
  display: flex;
  gap: var(--spacing-lg);
  align-items: flex-start;
}

.form-section {
  flex: 0 0 45%;
  max-width: 500px;
}

.result-section {
  flex: 1;
  min-width: 0;
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
  .quote-container {
    flex-direction: column;
  }

  .form-section {
    flex: 1;
    max-width: 100%;
    width: 100%;
  }

  .result-section {
    width: 100%;
  }
}
</style>
