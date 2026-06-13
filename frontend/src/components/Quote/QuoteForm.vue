<template>
  <div class="quote-form">
    <div class="form-card">
      <table class="form-table">
        <tbody>
          <!-- 成品尺寸 -->
          <tr>
            <th>成品尺寸</th>
            <td>
              <select v-model="localData.size_id" class="form-select">
                <option v-for="size in sizes" :key="size.id" :value="size.id">
                  {{ size.name }}
                </option>
              </select>
              <label class="checkbox-label">
                <input type="checkbox" v-model="customSize" />
                自定义尺寸
              </label>
              <div v-if="customSize" class="custom-size-row">
                <input
                  type="number"
                  v-model.number="localData.custom_width"
                  class="form-input small"
                  placeholder="宽"
                  min="1"
                />
                <span class="unit">×</span>
                <input
                  type="number"
                  v-model.number="localData.custom_height"
                  class="form-input small"
                  placeholder="高"
                  min="1"
                />
                <span class="unit">mm</span>
              </div>
            </td>
          </tr>

          <!-- 订单数量 -->
          <tr>
            <th>订单数量</th>
            <td>
              <input
                type="number"
                v-model.number="localData.quantity"
                class="form-input"
                min="1"
              />
              <span class="unit">本</span>
            </td>
          </tr>

          <!-- 联数 -->
          <tr>
            <th>联数</th>
            <td>
              <select v-model.number="localData.sheet_count" class="form-select">
                <option :value="2">二联</option>
                <option :value="3">三联</option>
                <option :value="4">四联</option>
                <option :value="5">五联</option>
                <option :value="6">六联</option>
              </select>
              <label class="checkbox-label">
                <input type="checkbox" v-model="showSheetDetail" />
                显示每联详情
              </label>
            </td>
          </tr>

          <!-- 每本页数 -->
          <tr>
            <th>每本页数</th>
            <td>
              <input
                type="number"
                v-model.number="localData.pages_per_book"
                class="form-input"
                min="1"
              />
              <span class="unit">页( {{ pagesPerSheet }}份)</span>
            </td>
          </tr>

          <!-- 印刷颜色 -->
          <tr>
            <th>印刷颜色</th>
            <td>
              <div class="color-row">
                <span class="label">正面:</span>
                <select v-model="localData.color_code" class="form-select">
                  <option v-for="color in colors" :key="color.code" :value="color.code">
                    {{ color.name }}
                  </option>
                </select>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="backSide" />
                  背面:
                </label>
              </div>
              <div class="color-options">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="frontSolid" />
                  正面大实地
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="backSolid" />
                  背面大实地
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="frontHighQuality" />
                  正面高品质
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="backHighQuality" />
                  背面高品质
                </label>
              </div>
            </td>
          </tr>

          <!-- 纸张克重 -->
          <tr>
            <th>纸张克重</th>
            <td>
              <select v-model.number="localData.gram_weight" class="form-select">
                <option :value="50">50克</option>
                <option :value="80">80克</option>
                <option :value="108">108克</option>
              </select>
            </td>
          </tr>

          <!-- 后道工序 -->
          <tr>
            <th>后道工序</th>
            <td>
              <div class="post-processing">
                <table class="processing-table">
                  <tr>
                    <td>
                      <label class="checkbox-label">
                        <input type="checkbox" value="design" v-model="postProcessingLocal" />
                        我要设计
                      </label>
                    </td>
                    <td>
                      <label class="checkbox-label">
                        <input type="checkbox" value="binding" v-model="bindingChecked" />
                        装订
                      </label>
                      <span v-if="bindingChecked">(
                        <label class="checkbox-label inline">
                          <input type="checkbox" value="binding_left" v-model="localData.post_processing" />
                          胶左
                        </label>
                        /
                        <label class="checkbox-label inline">
                          <input type="checkbox" value="binding_top" v-model="localData.post_processing" />
                          胶头
                        </label>
                      )</span>
                      <label class="checkbox-label">
                        <input type="checkbox" value="sheet_delivery" v-model="postProcessingLocal" />
                        印张交货
                      </label>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <label class="checkbox-label">
                        <input type="checkbox" value="add_card" v-model="postProcessingLocal" />
                        加卡纸
                      </label>
                    </td>
                    <td>
                      <label class="checkbox-label">
                        <input type="checkbox" value="numbering" v-model="localData.post_processing" />
                        打号码
                      </label>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <label class="checkbox-label">
                        <input type="checkbox" value="creasing" v-model="localData.post_processing" />
                        压痕压点线
                      </label>
                    </td>
                    <td>
                      <label class="checkbox-label">
                        <input type="checkbox" value="add_cover" v-model="localData.post_processing" />
                        加封面
                      </label>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <label class="checkbox-label">
                        <input type="checkbox" value="print_cover" v-model="postProcessingLocal" />
                        印封面
                      </label>
                    </td>
                    <td>
                      <label class="checkbox-label">
                        <input type="checkbox" value="edge_words" v-model="postProcessingLocal" />
                        换边联字
                      </label>
                    </td>
                  </tr>
                  <tr>
                    <td colspan="2">
                      <label class="checkbox-label">
                        <input type="checkbox" value="packing" v-model="postProcessingLocal" />
                        打包
                      </label>
                    </td>
                  </tr>
                  <tr>
                    <td colspan="2">
                      <span class="text-secondary">其他后工:无</span>
                    </td>
                  </tr>
                </table>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 底部操作区 -->
      <div class="form-actions">
        <div class="input-group">
          <label>客户:</label>
          <input
            type="text"
            v-model="localData.customer_name"
            placeholder="请选择或输入客户"
            class="form-input"
          />
        </div>
        <div class="input-group">
          <label>产品名:</label>
          <input
            type="text"
            v-model="localData.product_name"
            placeholder="请输入产品名"
            class="form-input"
          />
        </div>
        <div class="action-buttons">
          <a href="#" class="text-link">多数量</a>
          <label class="checkbox-label">
            <input type="checkbox" v-model="customProfit" />
            自填利润率
          </label>
          <input
            v-if="customProfit"
            type="number"
            v-model.number="profitPercent"
            class="form-input small"
            placeholder="%"
            min="0"
            step="1"
          />
          <span v-if="customProfit" class="unit">%</span>
          <button
            type="button"
            class="btn-primary"
            :disabled="loading"
            @click="handleSubmit"
          >
            {{ loading ? '计算中...' : '自助报价' }}
          </button>
          <span v-if="calculated" class="status-text">计算完成！</span>
          <button type="button" class="btn-secondary" disabled>ERP下单</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import type { LiandanQuoteRequest, ProductSize, PrintingColor } from '@/types/quote'
import { getSizes, getColors } from '@/api/quote'

interface Props {
  modelValue: LiandanQuoteRequest
  loading?: boolean
}

interface Emits {
  (e: 'update:modelValue', value: LiandanQuoteRequest): void
  (e: 'submit'): void
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const emit = defineEmits<Emits>()

const localData = ref<LiandanQuoteRequest>({ ...props.modelValue })
const sizes = ref<ProductSize[]>([])
const colors = ref<PrintingColor[]>([])
const customSize = ref(false)
const showSheetDetail = ref(false)
const backSide = ref(false)
const frontSolid = ref(false)
const backSolid = ref(false)
const frontHighQuality = ref(false)
const backHighQuality = ref(false)
const customProfit = ref(false)
const profitPercent = ref<number | null>(null)
const calculated = ref(false)
const bindingChecked = ref(true)
const postProcessingLocal = ref<string[]>([])

const pagesPerSheet = computed(() => {
  return Math.floor(localData.value.pages_per_book / localData.value.sheet_count)
})

// 取消自定义尺寸时清空宽高
watch(customSize, (on) => {
  if (!on) {
    localData.value.custom_width = null
    localData.value.custom_height = null
  }
})

// 取消自填利润率时清空
watch(customProfit, (on) => {
  if (!on) {
    profitPercent.value = null
    localData.value.profit_rate = null
  }
})

// 利润率百分比 → 小数同步到提交数据
watch(profitPercent, (pct) => {
  localData.value.profit_rate =
    pct === null || pct === undefined || isNaN(pct) ? null : pct / 100
})

watch(localData, (newVal) => {
  emit('update:modelValue', newVal)
}, { deep: true })

const handleSubmit = () => {
  emit('submit')
  calculated.value = true
}

onMounted(async () => {
  try {
    sizes.value = await getSizes()
    colors.value = await getColors()
  } catch (error) {
    console.error('加载基础数据失败:', error)
  }
})
</script>

<style scoped>
.quote-form {
  width: 100%;
}

.form-card {
  background: white;
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-lg);
}

.form-table {
  width: 100%;
  border-collapse: collapse;
}

.form-table tr {
  border-bottom: 1px solid var(--border-color);
}

.form-table tr:last-child {
  border-bottom: none;
}

.form-table th {
  text-align: left;
  padding: var(--spacing-md);
  font-weight: 600;
  color: var(--text-primary);
  vertical-align: top;
  width: 100px;
}

.form-table td {
  padding: var(--spacing-md);
}

.form-select,
.form-input {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-sm);
  outline: none;
  transition: border-color 0.2s;
}

.form-select {
  min-width: 200px;
}

.form-input {
  width: 120px;
}

.form-input.small {
  width: 70px;
}

.custom-size-row {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  margin-top: var(--spacing-sm);
}

.form-select:focus,
.form-input:focus {
  border-color: var(--primary-color);
}

.unit {
  margin-left: var(--spacing-sm);
  color: var(--text-secondary);
}

.checkbox-label {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  margin-left: var(--spacing-md);
  cursor: pointer;
  user-select: none;
}

.checkbox-label.inline {
  margin-left: var(--spacing-xs);
}

.checkbox-label input[type="checkbox"] {
  cursor: pointer;
}

.color-row {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-sm);
}

.color-row .label {
  color: var(--text-secondary);
}

.color-options {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.post-processing {
  width: 100%;
}

.processing-table {
  width: 100%;
  border-collapse: collapse;
}

.processing-table td {
  padding: var(--spacing-xs) 0;
  vertical-align: top;
}

.form-actions {
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-color);
}

.input-group {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.input-group label {
  min-width: 60px;
  color: var(--text-secondary);
}

.input-group .form-input {
  flex: 1;
  width: auto;
}

.action-buttons {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.text-link {
  color: var(--primary-color);
  text-decoration: none;
  font-size: var(--font-size-sm);
}

.text-link:hover {
  text-decoration: underline;
}

.btn-primary,
.btn-secondary {
  padding: var(--spacing-sm) var(--spacing-lg);
  border: none;
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
  font-weight: 500;
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
}

.btn-primary:disabled {
  background-color: var(--text-disabled);
  cursor: not-allowed;
}

.btn-secondary {
  background-color: var(--bg-gray);
  color: var(--text-secondary);
}

.btn-secondary:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.status-text {
  color: var(--success-color);
  font-size: var(--font-size-sm);
  font-weight: 500;
}

@media (max-width: 768px) {
  .form-table th {
    width: 80px;
    font-size: var(--font-size-xs);
  }

  .form-select {
    min-width: 150px;
  }

  .color-row {
    flex-direction: column;
    align-items: flex-start;
  }

  .action-buttons {
    flex-direction: column;
    align-items: stretch;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }
}
</style>
