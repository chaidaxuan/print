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
          :spec="quoteSpec"
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
import { calculateLiandanQuote, getSizes, getColors } from '@/api/quote'
import type {
  LiandanQuoteRequest,
  LiandanQuoteResponse,
  ProductSize,
  PrintingColor
} from '@/types/quote'

interface QuoteSpec {
  sizeName?: string
  material?: string
  colorName?: string
  processing?: string
}

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
const quoteSpec = ref<QuoteSpec>({})

// 基础数据，用于把表单里的 id/code 翻译成可读规格摘要
const sizes = ref<ProductSize[]>([])
const colors = ref<PrintingColor[]>([])

// 后道工序代码 → 中文标签
const processingLabels: Record<string, string> = {
  binding_left: '装订(胶左)',
  binding_top: '装订(胶头)',
  numbering: '打号码',
  creasing: '压痕压点线',
  add_cover: '加封面'
}

const buildSpec = (data: LiandanQuoteRequest): QuoteSpec => {
  // 规格：自定义尺寸优先，否则取尺寸名
  let sizeName: string
  if (data.custom_width && data.custom_height) {
    sizeName = `自定义 ${data.custom_width}×${data.custom_height}`
  } else {
    sizeName = sizes.value.find((s) => s.id === data.size_id)?.name || '—'
  }

  const colorName = colors.value.find((c) => c.code === data.color_code)?.name || '—'

  const procText =
    data.post_processing
      .map((code) => processingLabels[code] || code)
      .join('、') || '无'

  return {
    sizeName,
    material: `${data.gram_weight}克 无碳纸`,
    colorName,
    processing: procText
  }
}

const handleCalculate = async () => {
  loading.value = true
  try {
    const result = await calculateLiandanQuote(formData.value)
    quoteResult.value = result
    quoteSpec.value = buildSpec(formData.value)
  } catch (error) {
    console.error('计算报价失败:', error)
    alert('计算报价失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 预加载尺寸/颜色，用于规格摘要翻译
;(async () => {
  try {
    sizes.value = await getSizes()
    colors.value = await getColors()
  } catch (error) {
    console.error('加载基础数据失败:', error)
  }
})()
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
