<template>
  <div class="quote-result">
    <!-- 顶部工具栏 -->
    <div class="toolbar">
      <!-- 货币切换 -->
      <div class="currency-buttons">
        <button
          v-for="currency in currencies"
          :key="currency.code"
          :class="['currency-btn', { active: selectedCurrency === currency.code }]"
          @click="selectedCurrency = currency.code"
        >
          {{ currency.name }}
        </button>
      </div>

      <!-- 客户类型切换 -->
      <div class="customer-types">
        <button
          v-for="type in customerTypes"
          :key="type.code"
          :class="['type-btn', { active: selectedType === type.code }]"
          @click="selectedType = type.code"
        >
          {{ type.name }}
        </button>
      </div>

      <!-- 报表导出 -->
      <div class="export-actions">
        <a href="#" class="export-link" @click.prevent="handleExport('cost')">成本明细</a>
        <a href="#" class="export-link" @click.prevent="handleExport('quote')">报价单</a>
        <a href="#" class="export-link" @click.prevent="handleExport('contract')">合同单</a>
        <a href="#" class="export-link" @click.prevent="handleExport('process')">生产流程单</a>
      </div>
    </div>

    <!-- 阶梯价格表 -->
    <div class="price-table-container">
      <table class="price-table">
        <thead>
          <tr>
            <th>数量</th>
            <th>单价（元）</th>
            <th>总价（元）</th>
            <th>备注</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in result.ladder_prices" :key="item.quantity">
            <td>{{ item.quantity }}</td>
            <td>{{ formatPrice(item.unit_price) }}</td>
            <td>{{ formatPrice(item.total_price) }}</td>
            <td></td>
          </tr>
        </tbody>
      </table>

      <!-- 表格下方操作 -->
      <div class="table-footer">
        <div class="footer-row">
          <label>备注</label>
          <textarea
            v-model="remark"
            placeholder="客户公司+产品名+备注"
            class="remark-input"
          ></textarea>
        </div>
        <div class="footer-row">
          <label>总价</label>
          <input
            type="text"
            :value="formatPrice(result.total_price)"
            readonly
            class="total-price-input"
          />
          <button class="btn-save" @click="handleSave">保存</button>
        </div>
      </div>
    </div>

    <!-- 企业信息展示 -->
    <div class="company-info">
      <table class="info-table">
        <tr>
          <td class="label">可送货区域：</td>
          <td></td>
          <td class="label">质量宣言：</td>
          <td></td>
        </tr>
        <tr>
          <td class="label">交货周期：</td>
          <td>1-2日</td>
          <td class="label">优惠活动1：</td>
          <td></td>
        </tr>
        <tr>
          <td class="label">结款方式：</td>
          <td></td>
          <td class="label">加我好友：</td>
          <td>
            <button class="btn-wechat">微信付款</button>
            <button class="btn-mobile">手机端报价</button>
          </td>
        </tr>
      </table>

      <table class="info-table contact-table">
        <tr>
          <td class="label">联系电话：</td>
          <td>000-00000000</td>
          <td class="label">联系人：</td>
          <td>客服</td>
        </tr>
        <tr>
          <td class="label">联系QQ：</td>
          <td>
            <a href="#" class="contact-link">联系我们</a>
          </td>
          <td class="label">地址：</td>
          <td>中国</td>
        </tr>
      </table>
    </div>

    <!-- 成本明细摘要 -->
    <div class="cost-summary">
      <div class="summary-title">直接计算出来的成本</div>
      <div class="summary-content">
        <p><strong>【专版联单】报价ID:</strong>{{ quoteId }}</p>
        <p><strong>规格：</strong>{{ spec?.sizeName || result.machine_info.printing_size }}</p>
        <p><strong>材质：</strong>{{ spec?.material || '无碳纸' }}</p>
        <p><strong>数量：</strong>{{ result.quantity }}本</p>
        <p><strong>印刷：</strong>{{ spec?.colorName || '—' }}</p>
        <p><strong>印后工艺：</strong>{{ spec?.processing || '无' }}</p>
        <p><strong>计算结果：</strong>{{ formatPrice(result.total_price) }}元 [{{ formatPrice(result.unit_price) }}元/本]</p>
        <p class="promo-text">印刷报价系统：提高报价效率，降低业务成本，展现实力优势，赢得更多订单。</p>
        <div class="summary-actions">
          <a href="#" class="action-link" @click.prevent="handleMultiSummary">多数量汇总</a>
          <a href="#" class="action-link" @click.prevent="handleCopy">点击复制</a>
        </div>
      </div>
    </div>

    <!-- 成本明细弹窗 -->
    <div v-if="showCostDetail" class="modal-overlay" @click="showCostDetail = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>成本明细</h3>
          <button class="modal-close" @click="showCostDetail = false">×</button>
        </div>
        <div class="modal-body">
          <table class="detail-table">
            <tr>
              <td class="label">纸款：</td>
              <td>{{ formatPrice(result.cost_breakdown.paper_cost) }}元</td>
            </tr>
            <tr>
              <td class="label">印刷费：</td>
              <td>{{ formatPrice(result.cost_breakdown.printing_cost) }}元</td>
            </tr>
            <tr>
              <td class="label">后加工费用：</td>
              <td>{{ formatPrice(result.cost_breakdown.post_processing_cost) }}元</td>
            </tr>
            <tr class="total-row">
              <td class="label">生产成本：</td>
              <td><strong>{{ formatPrice(result.cost_breakdown.production_cost) }}元</strong></td>
            </tr>
            <tr>
              <td class="label">成本附加：</td>
              <td>{{ formatPrice(result.cost_breakdown.cost_addon) }}元</td>
            </tr>
            <tr class="total-row highlight">
              <td class="label">总成本：</td>
              <td><strong>{{ formatPrice(result.cost_breakdown.total_cost) }}元</strong></td>
            </tr>
          </table>

          <div class="machine-info">
            <h4>机器信息</h4>
            <p>机器名称：{{ result.machine_info.name }}</p>
            <p>印刷尺寸：{{ result.machine_info.printing_size }}</p>
            <p>版数：{{ result.machine_info.plates }}</p>
            <p>每版拼数：{{ result.machine_info.pieces_per_plate }}</p>
            <p>印张数：{{ result.machine_info.sheets_to_print }}</p>
            <p>买纸数：{{ result.machine_info.paper_sheets }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { LiandanQuoteResponse } from '@/types/quote'

interface QuoteSpec {
  sizeName?: string
  material?: string
  colorName?: string
  processing?: string
}

interface Props {
  result: LiandanQuoteResponse
  loading?: boolean
  spec?: QuoteSpec
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const currencies = [
  { code: 'CNY', name: '人民币' },
  { code: 'DISCOUNT', name: '优惠价' },
  { code: 'USD', name: '美金USD' },
  { code: 'PHP', name: '菲律宾比索PHP' },
  { code: 'EUR', name: '欧元EUR' },
  { code: 'HKD', name: '港元HKD' },
  { code: 'JPY', name: '日元JPY' },
  { code: 'TWD', name: '台币TWD' },
  { code: 'GBP', name: '英镑GBP' },
  { code: 'CAD', name: '加拿大元(CAD)' },
  { code: 'VND', name: '越南盾VND' },
  { code: 'THB', name: '泰国铢THB' },
  { code: 'IDR', name: '印尼卢比盾IDR' }
]

const customerTypes = [
  { code: 'cost', name: '成本价' },
  { code: 'cash', name: '现金客户' },
  { code: 'cash_invoice', name: '现金开票客户' },
  { code: 'monthly_30', name: '30天月结客户' },
  { code: 'agent', name: '中介客户' },
  { code: 'monthly_invoice', name: '月结开票客户' }
]

const selectedCurrency = ref('CNY')
const selectedType = ref('cost')
const remark = ref('')
const showCostDetail = ref(false)

// 报价ID：进入结果页时生成一次，避免每次渲染都变化
const quoteId = ref(Math.floor(Math.random() * 90000000) + 10000000)

const formatPrice = (price: number) => {
  return price.toFixed(2)
}

const summaryText = computed(() => {
  const r = props.result
  const s = props.spec
  return [
    `【专版联单】报价ID:${quoteId.value}`,
    `规格：${s?.sizeName || r.machine_info.printing_size}`,
    `材质：${s?.material || '无碳纸'}`,
    `数量：${r.quantity}本`,
    `印刷：${s?.colorName || '—'}`,
    `印后工艺：${s?.processing || '无'}`,
    `计算结果：${formatPrice(r.total_price)}元 [${formatPrice(r.unit_price)}元/本]`,
  ].join('\n')
})

const handleExport = (type: string) => {
  if (type === 'cost') {
    showCostDetail.value = true
  } else {
    console.log('导出:', type)
  }
}

const handleSave = () => {
  console.log('保存报价', remark.value)
  alert('报价已保存')
}

const handleMultiSummary = () => {
  console.log('多数量汇总')
}

const handleCopy = () => {
  navigator.clipboard.writeText(summaryText.value)
  alert('已复制到剪贴板')
}
</script>

<style scoped>
.quote-result {
  background: white;
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
  padding: var(--spacing-lg);
}

.toolbar {
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
}

.currency-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
  margin-bottom: var(--spacing-md);
}

.currency-btn {
  padding: var(--spacing-xs) var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  background: white;
  color: var(--text-secondary);
  font-size: var(--font-size-xs);
  cursor: pointer;
  transition: all 0.2s;
}

.currency-btn.active,
.currency-btn:hover {
  background: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}

.customer-types {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.type-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  cursor: pointer;
  padding: var(--spacing-xs) 0;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}

.type-btn.active {
  color: var(--primary-color);
  border-bottom-color: var(--primary-color);
}

.export-actions {
  display: flex;
  gap: var(--spacing-lg);
}

.export-link {
  color: var(--primary-color);
  text-decoration: none;
  font-size: var(--font-size-sm);
  cursor: pointer;
}

.export-link:hover {
  text-decoration: underline;
}

.price-table-container {
  margin-bottom: var(--spacing-lg);
}

.price-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: var(--spacing-md);
}

.price-table thead {
  background: var(--table-header-bg);
  color: var(--table-header-text);
}

.price-table th,
.price-table td {
  padding: var(--spacing-md);
  text-align: left;
  border: 1px solid var(--table-border);
}

.price-table th {
  font-weight: 600;
}

.price-table tbody tr:hover {
  background: var(--table-hover);
}

.price-table td:nth-child(2),
.price-table td:nth-child(3) {
  text-align: right;
  font-family: var(--font-mono);
}

.table-footer {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.footer-row {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
}

.footer-row label {
  min-width: 60px;
  color: var(--text-secondary);
}

.remark-input {
  flex: 1;
  padding: var(--spacing-sm);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-sm);
  resize: vertical;
  min-height: 60px;
}

.total-price-input {
  width: 150px;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  font-size: var(--font-size-md);
  font-weight: 600;
  text-align: right;
  background: var(--bg-gray);
  font-family: var(--font-mono);
}

.btn-save {
  padding: var(--spacing-sm) var(--spacing-lg);
  background: var(--success-color);
  color: white;
  border: none;
  border-radius: var(--border-radius-sm);
  cursor: pointer;
  font-size: var(--font-size-sm);
  transition: background 0.2s;
}

.btn-save:hover {
  background: var(--success-hover);
}

.company-info {
  margin-bottom: var(--spacing-lg);
  padding: var(--spacing-md);
  background: var(--bg-gray);
  border-radius: var(--border-radius-sm);
}

.info-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: var(--spacing-md);
}

.info-table td {
  padding: var(--spacing-xs) var(--spacing-sm);
  font-size: var(--font-size-sm);
}

.info-table td.label {
  color: var(--text-secondary);
  text-align: right;
  width: 100px;
}

.contact-table {
  margin-bottom: 0;
}

.btn-wechat,
.btn-mobile {
  padding: var(--spacing-xs) var(--spacing-md);
  margin-right: var(--spacing-sm);
  border: none;
  border-radius: var(--border-radius-sm);
  background: linear-gradient(135deg, #09bb07 0%, #07c160 100%);
  color: white;
  font-size: var(--font-size-xs);
  cursor: pointer;
}

.btn-mobile {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
}

.contact-link {
  color: var(--primary-color);
  text-decoration: none;
}

.cost-summary {
  padding: var(--spacing-md);
  background: var(--bg-gray);
  border-radius: var(--border-radius-sm);
}

.summary-title {
  font-weight: 600;
  margin-bottom: var(--spacing-md);
  color: var(--text-primary);
}

.summary-content p {
  margin: var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
  line-height: var(--line-height-lg);
}

.promo-text {
  color: var(--text-secondary);
  font-style: italic;
  margin-top: var(--spacing-md) !important;
}

.summary-actions {
  margin-top: var(--spacing-md);
  display: flex;
  gap: var(--spacing-lg);
}

.action-link {
  color: var(--primary-color);
  text-decoration: none;
  font-size: var(--font-size-sm);
}

.action-link:hover {
  text-decoration: underline;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: var(--border-radius-lg);
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
}

.modal-header h3 {
  margin: 0;
  font-size: var(--font-size-lg);
}

.modal-close {
  background: none;
  border: none;
  font-size: 28px;
  color: var(--text-secondary);
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 30px;
  height: 30px;
}

.modal-body {
  padding: var(--spacing-lg);
}

.detail-table {
  width: 100%;
  margin-bottom: var(--spacing-lg);
}

.detail-table tr {
  border-bottom: 1px solid var(--border-color);
}

.detail-table td {
  padding: var(--spacing-md) var(--spacing-sm);
  font-size: var(--font-size-sm);
}

.detail-table td:last-child {
  text-align: right;
  font-family: var(--font-mono);
}

.detail-table .total-row td {
  padding-top: var(--spacing-md);
  font-size: var(--font-size-md);
}

.detail-table .highlight {
  background: var(--bg-gray);
}

.machine-info {
  padding: var(--spacing-md);
  background: var(--bg-gray);
  border-radius: var(--border-radius-sm);
}

.machine-info h4 {
  margin: 0 0 var(--spacing-md) 0;
  font-size: var(--font-size-md);
}

.machine-info p {
  margin: var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
}

@media (max-width: 768px) {
  .toolbar {
    padding: var(--spacing-md);
  }

  .currency-buttons {
    gap: var(--spacing-xs);
  }

  .currency-btn {
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: 11px;
  }

  .customer-types {
    flex-wrap: wrap;
  }

  .export-actions {
    flex-wrap: wrap;
    gap: var(--spacing-md);
  }

  .price-table {
    font-size: var(--font-size-xs);
  }

  .price-table th,
  .price-table td {
    padding: var(--spacing-sm);
  }

  .footer-row {
    flex-direction: column;
    align-items: stretch;
  }

  .total-price-input {
    width: 100%;
  }
}
</style>
