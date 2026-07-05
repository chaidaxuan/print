<template>
  <div class="liandan-quote-page">
    <!-- 上半区：左产品图 + 右表单 -->
    <div class="quote-top">
      <!-- 左侧产品图区 -->
      <div class="gallery-section">
        <div class="main-image">
          <button
            class="nav-arrow nav-prev"
            type="button"
            aria-label="上一张"
            @click="prevImage"
          >
            ‹
          </button>
          <img :src="activeImage" alt="无碳联单" />
          <button
            class="nav-arrow nav-next"
            type="button"
            aria-label="下一张"
            @click="nextImage"
          >
            ›
          </button>
        </div>
        <div class="thumb-list">
          <button
            v-for="(img, idx) in productImages"
            :key="idx"
            :class="['thumb', { active: activeImage === img }]"
            type="button"
            @click="activeImage = img"
          >
            <img :src="img" alt="缩略图" />
          </button>
        </div>
      </div>

      <!-- 右侧表单区 -->
      <div class="form-section">
        <QuoteForm
          v-model="formData"
          :loading="loading"
          @submit="handleCalculate"
        />
      </div>
    </div>

    <!-- 下方整宽价格区 -->
    <div class="price-section">
      <QuoteResult
        v-if="quoteResult"
        :result="quoteResult"
        :spec="quoteSpec"
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

// 产品图：主图 + 缩略图列表，缩略图取自演示系统真实产品图
const productImages = ['/products/2.jpg', '/products/23.jpg']
const activeImage = ref(productImages[0])

// 大图左右箭头切换
const prevImage = () => {
  const idx = productImages.indexOf(activeImage.value)
  const next = (idx - 1 + productImages.length) % productImages.length
  activeImage.value = productImages[next]
}

const nextImage = () => {
  const idx = productImages.indexOf(activeImage.value)
  const next = (idx + 1) % productImages.length
  activeImage.value = productImages[next]
}

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

/* 上半区：左图 + 右表单 */
.quote-top {
  display: flex;
  gap: var(--spacing-lg);
  align-items: flex-start;
  margin-bottom: var(--spacing-lg);
}

/* 左侧产品图区 */
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

.thumb-list {
  display: flex;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-sm);
  flex-wrap: wrap;
}

.thumb {
  width: 72px;
  height: 72px;
  padding: 2px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  background: white;
  cursor: pointer;
  overflow: hidden;
  transition: border-color 0.2s;
}

.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 2px;
}

.thumb.active {
  border-color: var(--primary-color);
}

.thumb:hover {
  border-color: var(--primary-hover);
}

/* 右侧表单区 */
.form-section {
  flex: 1;
  min-width: 0;
}

/* 下方整宽价格区 */
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
