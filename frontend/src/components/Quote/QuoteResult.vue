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

    <!-- 成本明细弹窗 → 完整报价明细打印单 -->
    <div v-if="showCostDetail" class="modal-overlay" @click="showCostDetail = false">
      <div class="modal-content print-modal" @click.stop id="print-area">
        <div class="modal-header no-print">
          <h3>报价价格明细</h3>
          <button class="btn-print" @click="handlePrint">打印</button>
          <button class="modal-close" @click="showCostDetail = false">×</button>
        </div>
        <div class="modal-body">
          <!-- ① 标题栏 -->
          <div class="print-title">
            <span class="title-text">报价软件功能演示报价系统</span>
            <span class="demo-notice">给您了解功能演示用的软件，内设置的报价参数和您的实际数据不同，所以计算结果和您手算的会有不同是正常的</span>
          </div>

          <!-- ② 报价参数区 -->
          <table class="param-table">
            <tr>
              <td class="label-cell">报价项目：</td>
              <td>专版联单报价</td>
              <td class="label-cell">报价Id：</td>
              <td>{{ result.quote_id || '—' }}</td>
              <td class="label-cell">报价时间：</td>
              <td>{{ result.quote_time ? new Date(result.quote_time).toLocaleString('zh-CN') : '—' }}</td>
            </tr>
            <tr>
              <td class="label-cell" rowspan="2">报价参数：</td>
              <td>印刷颜色：{{ spec?.colorName || '—' }}</td>
              <td colspan="4">单 双 面：—</td>
            </tr>
            <tr>
              <td>其它参数：联数({{ formData.sheet_count || 1 }})</td>
              <td colspan="4">后道工序：{{ spec?.processing || '无' }}</td>
            </tr>
          </table>

          <!-- ③ 专版联单成品 -->
          <table class="product-table">
            <tr>
              <td class="label-cell" rowspan="2">专版联单成品：</td>
              <td class="sub-label">尺寸</td>
              <td class="sub-label">数量</td>
              <td class="sub-label">材料</td>
            </tr>
            <tr>
              <td>{{ spec?.sizeName || '—' }}</td>
              <td>{{ result.quantity }}</td>
              <td>{{ spec?.material || '—' }}</td>
            </tr>
          </table>

          <!-- ④ 合计(重量/体积留空) -->
          <table class="summary-table">
            <tr>
              <td class="label-cell">合计：</td>
              <td>重量：{{ result.weight_kg ? `约${result.weight_kg.toFixed(2)}公斤` : '—' }}</td>
              <td>体积：{{ result.volume_m3 ? `约${result.volume_m3.toFixed(2)}立方米` : '—' }}</td>
            </tr>
          </table>

          <!-- ⑤ 成本汇总(2行3列) -->
          <table class="cost-summary-table">
            <tr>
              <td class="label-cell">纸款：</td>
              <td>{{ cb.paper_cost }}</td>
              <td class="label-cell">印刷费：</td>
              <td>{{ cb.printing_cost }}</td>
              <td class="label-cell">后加工费用：</td>
              <td>{{ cb.post_processing_cost }}</td>
            </tr>
            <tr>
              <td class="label-cell">生产成本：</td>
              <td>{{ cb.production_cost }}</td>
              <td class="label-cell">成本附加：</td>
              <td>{{ cb.cost_addon }}</td>
              <td class="label-cell">总成本：</td>
              <td class="total-cost">¥{{ cb.total_cost }}</td>
            </tr>
            <tr>
              <td class="label-cell">报价单价：</td>
              <td>{{ result.unit_price.toFixed(2) }}</td>
              <td class="label-cell">报价总价：</td>
              <td colspan="3">{{ result.total_price }}</td>
            </tr>
          </table>

          <!-- ⑤.1 纸张分层成本明细 -->
          <div v-if="paperDetail" class="paper-layer-section">
            <h4 class="paper-layer-title">纸张分层成本明细</h4>
            <table class="paper-layer-table">
              <thead>
                <tr>
                  <th>纸层</th>
                  <th>页数</th>
                  <th>令价（元/令）</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(layer, i) in paperDetail.layers" :key="i">
                  <td>{{ layer.label }}</td>
                  <td>{{ layer.pages }}</td>
                  <td>{{ layer.ream_price.toFixed(2) }}</td>
                </tr>
              </tbody>
              <tfoot>
                <tr class="weighted-row">
                  <td colspan="2">加权令价</td>
                  <td>{{ paperDetail.weighted_ream_price.toFixed(2) }} 元/令</td>
                </tr>
                <tr class="result-row">
                  <td colspan="2">纸款 = 买纸数({{ paperDetail.paper_sheets }}全张) × 加权令价 / 500</td>
                  <td><strong>¥{{ paperDetail.paper_cost.toFixed(2) }}</strong></td>
                </tr>
              </tfoot>
            </table>
            <p class="paper-meta">
              {{ paperDetail.weight }}克 {{ paperDetail.paper_type_label }}无碳纸 · {{ paperDetail.union_count }}联 · 每本{{ paperDetail.pages_per_book }}页
            </p>
          </div>

          <!-- ⑤.5 整体计算公式说明(大公式) -->
          <div class="overall-formula">
            <h4 class="formula-title">📐 整体计算公式</h4>
            <div class="formula-flow">
              <div class="formula-step">
                <span class="step-num">1</span>
                <div class="step-content">
                  <strong>总页数</strong> = 数量 × 每本页数
                  <div class="step-example">{{ result.quantity }} × {{ trace ? trace.formula_chain.find(s=>s.key==='total_pages')?.result || '?' : '?' }} 页</div>
                </div>
              </div>
              <div class="formula-arrow">↓</div>
              <div class="formula-step">
                <span class="step-num">2</span>
                <div class="step-content">
                  <strong>每版印数</strong> = ⌈总页数 ÷ 每版拼数⌉
                  <div class="step-example">⌈ 总页 ÷ {{ mi.pieces_per_plate }} ⌉ = {{ mi.sheets_to_print }} 张</div>
                </div>
              </div>
              <div class="formula-arrow">↓</div>
              <div class="formula-step">
                <span class="step-num">3</span>
                <div class="step-content">
                  <strong>买纸数</strong> = ⌈(每版印数 + 放数) ÷ 每全张可开数⌉
                  <div class="step-example">⌈({{ mi.sheets_to_print }} + {{ mi.spoilage || 100 }}) ÷ {{ trace ? trace.imposition.per_full : '?' }}⌉ = {{ mi.paper_sheets }} 全张</div>
                </div>
              </div>
              <div class="formula-arrow">↓</div>
              <div class="formula-step">
                <span class="step-num">4</span>
                <div class="step-content">
                  <strong>纸款</strong> = 全张单价 × 买纸数
                  <div class="step-example">{{ cb.paper_cost }} 元</div>
                </div>
              </div>
              <div class="formula-arrow">➕</div>
              <div class="formula-step">
                <span class="step-num">5</span>
                <div class="step-content">
                  <strong>印刷费</strong> = 版数 × (开机费 + 每版印数÷1000 × 千印价)
                  <div class="step-example">{{ mi.plates }} 版 × (...) = {{ cb.printing_cost }} 元</div>
                </div>
              </div>
              <div class="formula-arrow">➕</div>
              <div class="formula-step">
                <span class="step-num">6</span>
                <div class="step-content">
                  <strong>后加工费</strong> = Σ max(单价×数量, 最低消费)
                  <div class="step-example">{{ postItemsText }}</div>
                </div>
              </div>
              <div class="formula-arrow">=</div>
              <div class="formula-step highlight">
                <span class="step-num">7</span>
                <div class="step-content">
                  <strong>生产成本</strong> = 纸款 + 印刷费 + 后加工
                  <div class="step-example">{{ cb.paper_cost }} + {{ cb.printing_cost }} + {{ cb.post_processing_cost }} = <strong>{{ cb.production_cost }} 元</strong></div>
                </div>
              </div>
              <div class="formula-arrow">➕</div>
              <div class="formula-step">
                <span class="step-num">8</span>
                <div class="step-content">
                  <strong>成本附加</strong> = 生产成本 × 阶梯附加率
                  <div class="step-example">{{ cb.production_cost }} × {{ addonRate }} = <strong>{{ cb.cost_addon }} 元</strong></div>
                </div>
              </div>
              <div class="formula-arrow">=</div>
              <div class="formula-step highlight final">
                <span class="step-num">9</span>
                <div class="step-content">
                  <strong>总成本</strong> = 生产成本 + 成本附加
                  <div class="step-example">{{ cb.production_cost }} + {{ cb.cost_addon }} = <strong class="final-price">¥{{ cb.total_cost }}</strong></div>
                </div>
              </div>
              <div class="formula-arrow">÷</div>
              <div class="formula-step highlight">
                <span class="step-num">10</span>
                <div class="step-content">
                  <strong>报价单价</strong> = 总成本 ÷ 数量
                  <div class="step-example">{{ cb.total_cost }} ÷ {{ result.quantity }} = <strong>{{ result.unit_price.toFixed(3) }} 元/本</strong></div>
                </div>
              </div>
            </div>
          </div>

          <!-- ⑥ 工序明细大表 -->
          <div class="process-detail">
            <table class="process-table">
              <thead>
                <tr>
                  <th>工序</th>
                  <th>机器名称</th>
                  <th>开纸尺寸</th>
                  <th>印刷方式</th>
                  <th>版数</th>
                  <th>每版拼数</th>
                  <th>每版印数</th>
                  <th>印刷纸</th>
                  <th>纸款</th>
                  <th>印工费</th>
                  <th>小计</th>
                  <th>买纸尺寸</th>
                  <th>开纸类型</th>
                  <th>买纸数</th>
                  <th>说明</th>
                </tr>
              </thead>
              <tbody>
                <!-- 印刷行 -->
                <tr>
                  <td>印刷1</td>
                  <td>{{ mi.name }}</td>
                  <td>{{ mi.printing_size }}</td>
                  <td>—</td>
                  <td>{{ mi.plates }}</td>
                  <td>{{ mi.pieces_per_plate }}</td>
                  <td>{{ mi.sheets_to_print }}</td>
                  <td>{{ mi.sheets_to_print }}+{{ mi.spoilage || 100 }}</td>
                  <td>¥{{ cb.paper_cost }}</td>
                  <td>¥{{ cb.printing_cost }}</td>
                  <td>¥{{ (cb.paper_cost + cb.printing_cost).toFixed(2) }}</td>
                  <td>{{ result.paper_series || '大度' }}</td>
                  <td>{{ result.cut_type || '—' }}</td>
                  <td>{{ mi.paper_sheets }}</td>
                  <td></td>
                </tr>
                <!-- 后加工行 -->
                <tr v-if="cb.post_processing_cost > 0">
                  <td>后加工</td>
                  <td colspan="9">{{ postItemsText }}</td>
                  <td>¥{{ cb.post_processing_cost }}</td>
                  <td colspan="4"></td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- ⑦ 计算过程(有 calc_trace 才显示) -->
          <div v-if="trace" class="calc-trace">
            <h4>计算过程</h4>

            <!-- 公式链 -->
            <table class="formula-table">
              <thead>
                <tr><th>步骤</th><th>公式</th><th>代入</th><th>结果</th></tr>
              </thead>
              <tbody>
                <tr v-for="step in trace.formula_chain" :key="step.key">
                  <td>{{ step.label }}</td>
                  <td>{{ step.formula }}</td>
                  <td>{{ step.substituted }}</td>
                  <td>{{ step.result }} {{ step.unit || '' }}</td>
                </tr>
              </tbody>
            </table>

            <!-- 拼版选择过程 -->
            <div class="imposition-trace">
              <h5>拼版选择过程</h5>
              <p>机器幅面：{{ imp.press_w }}×{{ imp.press_h }} mm</p>
              <table class="cut-levels-table">
                <thead>
                  <tr><th>级别</th><th>尺寸</th><th>能否上机</th></tr>
                </thead>
                <tbody>
                  <tr v-for="lv in imp.cut_levels" :key="lv.per_full" :class="{ selected: lv.selected }">
                    <td>{{ lv.level_name }}</td>
                    <td>{{ lv.cut_w }}×{{ lv.cut_h }}</td>
                    <td>{{ lv.fits ? '✓' : '✗' }}</td>
                  </tr>
                </tbody>
              </table>
              <p class="reason">{{ imp.reason }}</p>
            </div>

            <!-- 后加工逐项 -->
            <div v-if="trace.post_processing_items.length" class="post-items-trace">
              <h5>后加工明细</h5>
              <table class="post-items-table">
                <thead>
                  <tr><th>名称</th><th>单价</th><th>数量</th><th>原始费用</th><th>最低消费</th><th>实收费用</th></tr>
                </thead>
                <tbody>
                  <tr v-for="(item, i) in trace.post_processing_items" :key="i">
                    <td>{{ item.name }}</td>
                    <td>{{ item.unit_price }} {{ item.unit_label }}</td>
                    <td>{{ item.qty }} {{ item.qty_basis }}</td>
                    <td>{{ item.raw_cost }}</td>
                    <td>{{ item.min_charge }}</td>
                    <td>{{ item.cost }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
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

// 报价ID：由后端注入,删掉前端随机数(已改为后端真实记录)

// —— 成本明细弹窗新增计算属性 ——
const cb = computed(() => props.result.cost_breakdown)
const mi = computed(() => props.result.machine_info)
const trace = computed(() => props.result.calc_trace)
const imp = computed(() => trace.value?.imposition)
const paperDetail = computed(() => props.result.paper_layer_detail)
const formData = computed(() => ({ sheet_count: 3 })) // 临时兼容,待父组件传入

const postItemsText = computed(() => {
  const items = props.result.post_processing_items
  if (!items || !items.length) return '无'
  return items.map(i => `${i.name}(${i.cost})`).join(', ')
})

// 阶梯附加率：优先从计算轨迹的 cost_addon 步骤解析(与后端表格一致),
// 取不到则用 成本附加 ÷ 生产成本 反算
const addonRate = computed(() => {
  const step = trace.value?.formula_chain?.find(s => s.key === 'cost_addon')
  if (step?.substituted) {
    const m = step.substituted.match(/×\s*([\d.]+)/)
    if (m) return m[1]
  }
  const prod = cb.value.production_cost
  return prod ? (cb.value.cost_addon / prod).toFixed(4) : '0'
})

const handlePrint = () => {
  window.print()
}

const formatPrice = (price: number) => {
  return price.toFixed(2)
}

const summaryText = computed(() => {
  const r = props.result
  const s = props.spec
  return [
    `【专版联单】报价ID:${r.quote_id || '—'}`,
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
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: var(--border-radius-lg);
  width: 90%;
  max-width: 960px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
  position: relative;
  z-index: 10000;
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

.all-machines {
  margin-top: var(--spacing-lg);
}

.all-machines h4 {
  margin: 0 0 var(--spacing-md) 0;
  font-size: var(--font-size-md);
}

.machines-table-wrap {
  overflow-x: auto;
}

.machines-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--font-size-xs);
  white-space: nowrap;
}

.machines-table th,
.machines-table td {
  padding: 6px 8px;
  border: 1px solid var(--table-border);
  text-align: center;
}

.machines-table thead {
  background: var(--table-header-bg);
  color: var(--table-header-text);
}

.machines-table td:first-child {
  text-align: left;
}

.machines-table tbody tr.recommended {
  background: #fff7e6;
  font-weight: 600;
}

.machines-table .total-cell {
  color: var(--danger-color, #e4393c);
  font-weight: 600;
}

.rec-tag {
  display: inline-block;
  margin-left: 4px;
  padding: 1px 6px;
  font-size: 11px;
  font-weight: 400;
  color: white;
  background: var(--danger-color, #e4393c);
  border-radius: 3px;
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

/* ============== 打印单样式 ============== */
.modal-body {
  padding: var(--spacing-lg);
  overflow-y: auto;
  max-height: calc(90vh - 80px);
}

.total-cost {
  color: #e63946;
  font-weight: bold;
  font-size: 16px;
}

/* ======== 整体计算公式样式 ======== */
.overall-formula {
  margin: var(--spacing-lg) 0;
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  border: 2px solid #4a90e2;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.formula-title {
  font-size: 18px;
  font-weight: bold;
  color: #2c3e50;
  margin: 0 0 var(--spacing-md) 0;
  text-align: center;
  padding-bottom: var(--spacing-sm);
  border-bottom: 2px solid #4a90e2;
}

.formula-flow {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.formula-step {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 16px;
  background: white;
  border-radius: 8px;
  border-left: 4px solid #4a90e2;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: all 0.2s;
}

.formula-step:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.formula-step.highlight {
  border-left-color: #28a745;
  background: linear-gradient(90deg, #f0fff4 0%, white 100%);
}

.formula-step.final {
  border-left-color: #e63946;
  background: linear-gradient(90deg, #fff5f5 0%, white 100%);
  border: 2px solid #e63946;
}

.step-num {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #4a90e2, #357abd);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 13px;
  box-shadow: 0 2px 4px rgba(74, 144, 226, 0.3);
}

.formula-step.highlight .step-num {
  background: linear-gradient(135deg, #28a745, #1e7e34);
}

.formula-step.final .step-num {
  background: linear-gradient(135deg, #e63946, #c82333);
}

.step-content {
  flex: 1;
}

.step-content strong {
  color: #2c3e50;
  font-size: 15px;
  display: block;
  margin-bottom: 4px;
}

.step-example {
  color: #6c757d;
  font-size: 13px;
  margin-top: 4px;
  padding-left: 8px;
  border-left: 2px solid #dee2e6;
}

.formula-step.highlight .step-example strong,
.formula-step.final .step-example strong {
  color: #28a745;
  font-size: 15px;
}

.final-price {
  color: #e63946 !important;
  font-size: 20px !important;
}

.formula-arrow {
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  color: #4a90e2;
  padding: 4px 0;
}

/* ======== 纸张分层成本明细 ======== */
.paper-layer-section {
  margin: var(--spacing-lg) 0;
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, #fffdf7 0%, #fef9e7 100%);
  border-radius: 10px;
  border: 2px solid #f0c040;
  box-shadow: 0 3px 10px rgba(240, 192, 64, 0.15);
}

.paper-layer-title {
  font-size: 16px;
  font-weight: bold;
  color: #856404;
  margin: 0 0 var(--spacing-md) 0;
  padding-bottom: var(--spacing-sm);
  border-bottom: 2px solid #f0c040;
}

.paper-layer-table {
  width: 100%;
  border-collapse: collapse;
  margin: var(--spacing-sm) 0;
  font-size: 14px;
  background: white;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.paper-layer-table th,
.paper-layer-table td {
  border: 1px solid #dee2e6;
  padding: 10px 14px;
  text-align: center;
}

.paper-layer-table th {
  background: linear-gradient(135deg, #f0c040, #e0a800);
  color: white;
  font-weight: bold;
}

.paper-layer-table tbody tr:hover {
  background: #fffde6;
}

.paper-layer-table tfoot td {
  background: #fef9e7;
  font-weight: bold;
}

.paper-layer-table .weighted-row td {
  border-top: 2px solid #f0c040;
  color: #856404;
}

.paper-layer-table .result-row td {
  color: #e63946;
  font-size: 15px;
}

.paper-meta {
  margin-top: var(--spacing-sm);
  font-size: 13px;
  color: #856404;
  text-align: right;
  font-style: italic;
}

/* ======== 打印单整体美化 ======== */
.print-modal .modal-content {
  max-width: 1200px;
  width: 95%;
  max-height: 90vh;
  box-shadow: 0 10px 40px rgba(0,0,0,0.15);
  border-radius: 8px;
}

.print-title {
  text-align: center;
  padding: var(--spacing-md) 0;
  border-bottom: 3px solid #2c3e50;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin: calc(var(--spacing-md) * -1) calc(var(--spacing-md) * -1) var(--spacing-md);
  border-radius: 8px 8px 0 0;
}

.title-text {
  font-size: 22px;
  font-weight: bold;
  display: block;
  margin-bottom: var(--spacing-xs);
  text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.demo-notice {
  font-size: 12px;
  color: #ffe0e0;
  display: block;
}

.param-table,
.product-table,
.summary-table,
.cost-summary-table {
  width: 100%;
  border-collapse: collapse;
  margin: var(--spacing-md) 0;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  border-radius: 8px;
  overflow: hidden;
}

.param-table td,
.product-table td,
.summary-table td,
.cost-summary-table td {
  border: 1px solid #dee2e6;
  padding: 10px 14px;
}

.label-cell {
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  font-weight: bold;
  text-align: right;
  width: 120px;
  color: #495057;
}

.sub-label {
  background: linear-gradient(135deg, #e8f4f8, #d1ecf1);
  font-weight: bold;
  text-align: center;
  color: #0c5460;
}

.process-detail {
  margin: var(--spacing-md) 0;
  overflow-x: auto;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

.process-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  min-width: 1000px;
  background: white;
}

.process-table th,
.process-table td {
  border: 1px solid #dee2e6;
  padding: 10px 8px;
  text-align: center;
}

.process-table th {
  background: linear-gradient(135deg, #4a90e2, #357abd);
  color: white;
  font-weight: bold;
  font-size: 14px;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
  position: sticky;
  top: 0;
  z-index: 10;
}

.process-table tbody tr:hover {
  background: #f8f9fa;
  transition: background 0.2s;
}

.calc-trace {
  margin-top: var(--spacing-xl);
  border-top: 3px solid #4a90e2;
  padding-top: var(--spacing-lg);
  background: linear-gradient(135deg, #f8f9fa 0%, white 100%);
  padding: var(--spacing-lg);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.calc-trace h4 {
  font-size: 20px;
  margin-bottom: var(--spacing-md);
  color: #2c3e50;
  padding-bottom: var(--spacing-sm);
  border-bottom: 2px solid #4a90e2;
}

.calc-trace h5 {
  font-size: 16px;
  margin: var(--spacing-lg) 0 var(--spacing-sm);
  color: #495057;
  padding-left: var(--spacing-sm);
  border-left: 4px solid #28a745;
}

.formula-table,
.cut-levels-table,
.post-items-table {
  width: 100%;
  border-collapse: collapse;
  margin: var(--spacing-sm) 0;
  font-size: 13px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  border-radius: 6px;
  overflow: hidden;
}

.formula-table th,
.formula-table td,
.cut-levels-table th,
.cut-levels-table td,
.post-items-table th,
.post-items-table td {
  border: 1px solid #dee2e6;
  padding: 10px;
}

.formula-table th,
.cut-levels-table th,
.post-items-table th {
  background: linear-gradient(135deg, #6c757d, #5a6268);
  color: white;
  font-weight: bold;
  text-align: center;
}

.formula-table tbody tr:hover,
.cut-levels-table tbody tr:hover,
.post-items-table tbody tr:hover {
  background: #f8f9fa;
}

.cut-levels-table tr.selected {
  background: linear-gradient(90deg, #d4edda, #f8f9fa);
  font-weight: bold;
  border-left: 4px solid #28a745;
}

.imposition-trace .reason {
  color: #495057;
  font-style: italic;
  margin-top: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-md);
  background: #fff3cd;
  border-left: 4px solid #ffc107;
  border-radius: 4px;
}

.btn-print {
  padding: 10px 20px;
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-right: var(--spacing-sm);
  font-weight: 600;
  font-size: 14px;
  box-shadow: 0 2px 6px rgba(40, 167, 69, 0.3);
  transition: all 0.2s;
}

.btn-print:hover {
  background: linear-gradient(135deg, #218838, #1aa179);
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.4);
  transform: translateY(-1px);
}

.btn-print:active {
  transform: translateY(0);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--spacing-md);
  border-bottom: 2px solid #dee2e6;
  background: linear-gradient(135deg, #f8f9fa, white);
}

.modal-header h3 {
  margin: 0;
  font-size: 20px;
  color: #2c3e50;
  flex: 1;
}

/* 打印样式 */
@media print {
  /* 隐藏所有非打印内容 */
  body * {
    visibility: hidden;
  }

  /* 折叠打印区之外的所有内容高度,避免它们撑出多余空白页 */
  .quote-result > *:not(.modal-overlay) {
    display: none !important;
  }

  /* 只显示打印区域 */
  #print-area,
  #print-area * {
    visibility: visible;
  }

  /* 关键修复：打印时移除 fixed 定位,改为静态流式布局 */
  .modal-overlay {
    position: static !important;
    background: none !important;
    display: block !important;
    padding: 0 !important;
    overflow: visible !important;
  }

  /* #print-area 用 absolute 提到页首,叠在已隐藏(但仍占位)的表单之上,
     避免 fixed 定位在每页重复,也避免前面留出空白页 */
  .print-modal.modal-content,
  #print-area {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    box-shadow: none !important;
    max-width: 100% !important;
    width: 100% !important;
    max-height: none !important;
    margin: 0 !important;
    border-radius: 0 !important;
    overflow: visible !important;
  }

  .modal-body {
    max-height: none !important;
    overflow: visible !important;
    padding: 10mm !important;
  }

  /* 隐藏打印按钮和关闭按钮 */
  .no-print {
    display: none !important;
  }

  /* 分页优化 */
  .overall-formula {
    page-break-inside: auto;
  }

  .formula-step {
    page-break-inside: avoid;
  }

  .process-detail {
    page-break-before: auto;
    page-break-inside: auto;
  }

  .calc-trace {
    page-break-before: auto;
  }

  table {
    page-break-inside: auto;
  }

  tr {
    page-break-inside: avoid;
    page-break-after: auto;
  }

  thead {
    display: table-header-group;
  }

  /* 缩小打印时的字号和间距,让内容更紧凑 */
  .modal-body {
    font-size: 11pt !important;
  }

  h4 {
    font-size: 14pt !important;
    margin: 3mm 0 2mm 0 !important;
  }

  h5 {
    font-size: 12pt !important;
    margin: 2mm 0 1mm 0 !important;
  }

  /* 打印时优化标题栏 */
  .print-title {
    margin: 0 0 5mm 0 !important;
    border-radius: 0 !important;
  }

  /* 打印时优化表格间距 */
  .param-table,
  .product-table,
  .summary-table,
  .cost-summary-table {
    margin: 3mm 0 !important;
  }
}
</style>
