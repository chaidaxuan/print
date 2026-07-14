<template>
  <div class="huace-form">
    <table class="form-table">
      <tbody>
        <!-- 成品尺寸 -->
        <tr>
          <th>成品尺寸</th>
          <td>
            <select v-model="form.size_id" class="form-select">
              <option v-for="s in sizes" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </td>
        </tr>
        <!-- 封面纸张 -->
        <tr>
          <th>封面纸张</th>
          <td>
            <select v-model="coverPaperKey" class="form-select">
              <option v-for="p in papers" :key="paperKey(p)" :value="paperKey(p)">
                {{ p.paper_name }} {{ p.weight }}克 (¥{{ p.ton_price }}/吨)
              </option>
            </select>
          </td>
        </tr>
        <!-- 封面P数 -->
        <tr>
          <th>封面P数</th>
          <td>
            <select v-model.number="form.cover_pages" class="form-select">
              <option :value="4">4P</option>
              <option :value="8">8P</option>
            </select>
          </td>
        </tr>
        <!-- 封面颜色 -->
        <tr>
          <th>封面印刷颜色</th>
          <td>
            <select v-model="form.cover_color_code" class="form-select">
              <option v-for="c in coverColors" :key="c.color_code" :value="c.color_code">
                {{ c.color_name }}
              </option>
            </select>
          </td>
        </tr>
        <!-- 封面双面印 -->
        <tr>
          <th>封面双面印</th>
          <td>
            <label class="checkbox-label">
              <input type="checkbox" v-model="form.cover_both_sides" />
              封面双面印刷（自反版）
            </label>
          </td>
        </tr>
        <!-- 内页纸张 -->
        <tr>
          <th>内页纸张</th>
          <td>
            <select v-model="innerPaperKey" class="form-select">
              <option v-for="p in papers" :key="paperKey(p)" :value="paperKey(p)">
                {{ p.paper_name }} {{ p.weight }}克 (¥{{ p.ton_price }}/吨)
              </option>
            </select>
          </td>
        </tr>
        <!-- 内页P数 -->
        <tr>
          <th>内页P数</th>
          <td>
            <select v-model.number="form.inner_pages" class="form-select">
              <option v-for="p in innerPageOptions" :key="p" :value="p">{{ p }}P</option>
            </select>
          </td>
        </tr>
        <!-- 内页颜色 -->
        <tr>
          <th>内页印刷颜色</th>
          <td>
            <select v-model="form.inner_color_code" class="form-select">
              <option v-for="c in innerColors" :key="c.color_code" :value="c.color_code">
                {{ c.color_name }}
              </option>
            </select>
          </td>
        </tr>
        <!-- 表面处理 -->
        <tr>
          <th>表面处理</th>
          <td>
            <select v-model="form.surface_treatment" class="form-select">
              <option value="">不需要</option>
              <option v-for="s in surfaceOptions" :key="s.code" :value="s.code">
                {{ s.name }}
              </option>
            </select>
          </td>
        </tr>
        <!-- 装订方式 -->
        <tr>
          <th>装订方式</th>
          <td>
            <select v-model="form.binding_code" class="form-select">
              <option v-for="b in bindings" :key="b.code" :value="b.code">
                {{ b.name }}
              </option>
            </select>
          </td>
        </tr>
        <!-- 其他后道工序 -->
        <tr>
          <th>其他工序</th>
          <td>
            <div class="checkbox-group">
              <label v-for="op in otherOptions" :key="op.code" class="checkbox-label">
                <input
                  type="checkbox"
                  :value="op.code"
                  v-model="form.other_processing"
                />
                {{ op.name }}
              </label>
            </div>
          </td>
        </tr>
        <!-- 数量 -->
        <tr>
          <th>印刷数量(本)</th>
          <td>
            <input
              type="number"
              v-model.number="form.quantity"
              class="form-input"
              min="1"
            />
          </td>
        </tr>
        <!-- 多数量(可选) -->
        <tr>
          <th>多数量报价</th>
          <td>
            <input
              type="text"
              v-model="multiQtyText"
              class="form-input"
              placeholder="用逗号分隔，如 500,1000,2000"
            />
          </td>
        </tr>
        <!-- 客户类型 -->
        <tr>
          <th>客户类型</th>
          <td>
            <select v-model="form.client_tier_code" class="form-select">
              <option v-for="t in clientTiers" :key="t.code" :value="t.code">
                {{ t.name }} (×{{ t.multiplier }})
              </option>
            </select>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="form-actions">
      <button
        type="button"
        class="btn-primary"
        :disabled="loading"
        @click="handleSubmit"
      >
        {{ loading ? '计算中...' : '自助报价' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { getHuaceSizes, getHuacePapers, getHuaceColors, getHuaceBindings, getHuacePostProcessing, getHuaceClientTiers } from '@/api/huace'
import type { HuacePaper, HuaceColor, HuaceBinding, HuacePostProcessing as HuacePostProc, HuaceClientTier, HuaceSize, HuaceQuoteRequest } from '@/types/huace'

interface Props {
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), { loading: false })
const emit = defineEmits<{ submit: [data: HuaceQuoteRequest] }>()

const sizes = ref<HuaceSize[]>([])
const papers = ref<HuacePaper[]>([])
const coverColors = ref<HuaceColor[]>([])
const innerColors = ref<HuaceColor[]>([])
const bindings = ref<HuaceBinding[]>([])
const postProcs = ref<HuacePostProc[]>([])
const clientTiers = ref<HuaceClientTier[]>([])

const surfaceOptions = computed(() => postProcs.value.filter(p => p.proc_group === 'surface'))
const otherOptions = computed(() => postProcs.value.filter(p => p.proc_group === 'other'))

const innerPageOptions = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 48, 56, 64, 72, 80, 96, 112, 128]

const form = ref({
  size_id: 0,
  cover_pages: 4,
  cover_color_code: 'cmyk',
  cover_both_sides: true,
  inner_pages: 16,
  inner_color_code: 'cmyk',
  surface_treatment: 'film_gloss',
  binding_code: 'saddle_stitch',
  other_processing: [] as string[],
  quantity: 1000,
  client_tier_code: 'cost',
})

const coverPaperKey = ref('')
const innerPaperKey = ref('')
const multiQtyText = ref('')

const paperKey = (p: HuacePaper) => `${p.paper_name}|${p.weight}|${p.ton_price}`

const parsePaperKey = (key: string) => {
  const [name, weight, ton_price] = key.split('|')
  return { paper_name: name, weight: parseInt(weight), ton_price: parseFloat(ton_price) }
}

const handleSubmit = () => {
  const cover = parsePaperKey(coverPaperKey.value)
  const inner = parsePaperKey(innerPaperKey.value)

  const multiQtys = multiQtyText.value
    .split(/[,，]/)
    .map(s => parseInt(s.trim()))
    .filter(n => n > 0)

  const data: HuaceQuoteRequest = {
    size_id: form.value.size_id,
    quantity: form.value.quantity,
    cover_paper_name: cover.paper_name,
    cover_paper_weight: cover.weight,
    cover_paper_ton_price: cover.ton_price,
    cover_pages: form.value.cover_pages,
    cover_color_code: form.value.cover_color_code,
    cover_both_sides: form.value.cover_both_sides,
    inner_paper_name: inner.paper_name,
    inner_paper_weight: inner.weight,
    inner_paper_ton_price: inner.ton_price,
    inner_pages: form.value.inner_pages,
    inner_color_code: form.value.inner_color_code,
    binding_code: form.value.binding_code,
    surface_treatment: form.value.surface_treatment || undefined,
    other_processing: form.value.other_processing,
    client_tier_code: form.value.client_tier_code,
    multi_quantities: multiQtys.length > 0 ? multiQtys : undefined,
  }

  emit('submit', data)
}

onMounted(async () => {
  const [sizesData, papersData, colorsData, bindingsData, postData, tiersData] = await Promise.all([
    getHuaceSizes(),
    getHuacePapers(),
    getHuaceColors(),
    getHuaceBindings(),
    getHuacePostProcessing(),
    getHuaceClientTiers(),
  ])

  sizes.value = sizesData
  papers.value = papersData
  coverColors.value = colorsData.filter(c => c.component === 'cover')
  innerColors.value = colorsData.filter(c => c.component === 'inner')
  bindings.value = bindingsData
  postProcs.value = postData
  clientTiers.value = tiersData

  if (sizesData.length) form.value.size_id = sizesData[0].id

  const defaultPaper = papersData.find(p => p.paper_name === '双铜纸' && p.weight === 80)
  if (defaultPaper) {
    coverPaperKey.value = paperKey(defaultPaper)
    innerPaperKey.value = paperKey(defaultPaper)
  } else if (papersData.length) {
    coverPaperKey.value = paperKey(papersData[0])
    innerPaperKey.value = paperKey(papersData[0])
  }
})
</script>

<style scoped>
.huace-form {
  width: 100%;
}

.form-table {
  width: 100%;
  border-collapse: collapse;
}

.form-table th {
  text-align: right;
  padding: 8px 12px 8px 0;
  white-space: nowrap;
  font-weight: 500;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  width: 120px;
  vertical-align: middle;
}

.form-table td {
  padding: 6px 0;
}

.form-select,
.form-input {
  width: 100%;
  max-width: 320px;
  padding: 6px 10px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-sm);
  background: white;
}

.form-select:focus,
.form-input:focus {
  outline: none;
  border-color: var(--primary-color);
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 16px;
}

.checkbox-label {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--font-size-sm);
  cursor: pointer;
}

.form-actions {
  margin-top: 16px;
  text-align: center;
}

.btn-primary {
  padding: 10px 48px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--border-radius-sm);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-hover);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
