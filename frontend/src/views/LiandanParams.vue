<template>
  <div class="params-page">
    <!-- 二级面包屑：专版联单设置 -->
    <div class="params-crumb">
      <span class="crumb-item">首页</span>
      <span class="crumb-sep">/</span>
      <span class="crumb-item active">专版联单设置</span>
    </div>

    <!-- 5 个参数 Tab -->
    <div class="params-tabs">
      <a
        v-for="tab in tabs"
        :key="tab.key"
        href="#"
        :class="['params-tab', { active: activeTab === tab.key }]"
        @click.prevent="activeTab = tab.key"
      >{{ tab.label }}</a>
    </div>

    <div class="params-body">
      <!-- Tab1：专版其它参数设置 -->
      <section v-show="activeTab === 'base'" class="panel">
        <div class="panel-head">
          <span class="panel-title">专版其它参数设置</span>
          <a href="#" class="btn btn-save" @click.prevent>保存</a>
        </div>
        <table class="form-table">
          <tbody>
            <tr>
              <th>交货周期：</th>
              <td><input class="ipt" type="text" v-model="base.deliveryCycle" /></td>
            </tr>
            <tr>
              <th>设计：</th>
              <td>
                <label class="ck">
                  <input type="radio" name="designMode" value="1" v-model="base.designMode" /> 方式一（单选）
                </label>
                <div class="sub-line">
                  模板设计（简单）：
                  <input class="ipt ipt-sm" type="text" v-model="base.tplSimple" />
                  <span class="unit-group">
                    (单位:
                    <label class="ck"><input type="radio" name="tplUnit" value="p" v-model="base.tplUnit" /> 元/P (A4面积)</label>、
                    <label class="ck"><input type="radio" name="tplUnit" value="kuan" v-model="base.tplUnit" /> 元/款</label>
                    )
                  </span>
                </div>
                <div class="sub-line">
                  来样设计（一般）：<input class="ipt ipt-sm" type="text" v-model="base.sampleNormal" />
                </div>
                <div class="sub-line">
                  创意设计（复杂）：<input class="ipt ipt-sm" type="text" v-model="base.creativeComplex" />
                </div>

                <label class="ck">
                  <input type="radio" name="designMode" value="2" v-model="base.designMode" /> 方式二（多选）
                </label>
                <div class="sub-line">来样设计：<input class="ipt ipt-sm" type="text" v-model="base.m2Sample" /> 元/款</div>
                <div class="sub-line">创意设计：<input class="ipt ipt-sm" type="text" v-model="base.m2Creative" /> 元/款</div>
                <div class="sub-line">逆向设计：<input class="ipt ipt-sm" type="text" v-model="base.m2Reverse" /> 元/款</div>
                <div class="sub-line">小改文件：<input class="ipt ipt-sm" type="text" v-model="base.m2SmallFix" /> 元/款</div>
                <div class="sub-line">大改文件：<input class="ipt ipt-sm" type="text" v-model="base.m2BigFix" /> 元/款</div>

                <label class="ck"><input type="radio" name="designMode" value="none" v-model="base.designMode" /> 不设计</label>
                <label class="ck"><input type="radio" name="designMode" value="self" v-model="base.designMode" /> 自填设计费</label>
              </td>
            </tr>
            <tr>
              <th>显示重量体积：</th>
              <td>
                <label class="ck"><input type="checkbox" v-model="base.showWeightVolume" /> 报价显示重量体积</label>
              </td>
            </tr>
            <tr>
              <th>启用运费：</th>
              <td>
                <label class="ck"><input type="checkbox" v-model="base.freightSelf" /> 启用自填运费</label>
                <label class="ck"><input type="checkbox" v-model="base.freightPost" /> 启用后工设置里的运费</label>
                <label class="ck"><input type="checkbox" v-model="base.freightSummary" /> 汇总显示运费</label>
              </td>
            </tr>
            <tr>
              <th>价格明细模切：</th>
              <td>
                <label class="ck"><input type="checkbox" v-model="base.diecutToPost" /> 价格明细的模切移到后加工</label>
              </td>
            </tr>
          </tbody>
        </table>
        <p class="service-tip">软件使用客服：19200444307</p>
      </section>

      <!-- Tab2：彩印印刷机参数设置 -->
      <section v-show="activeTab === 'machine'" class="panel">
        <div class="panel-head">
          <span class="panel-title">彩印印刷机参数设置</span>
          <div class="btn-group">
            <a href="#" class="btn" @click.prevent>编辑</a>
            <a href="#" class="btn" @click.prevent>复制</a>
            <a href="#" class="btn" @click.prevent>删除</a>
          </div>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>使用</th>
              <th>项目印刷机</th>
              <th>类型</th>
              <th>机器名称</th>
              <th>咬口(mm)</th>
              <th>长(mm)</th>
              <th>宽(mm)</th>
              <th>最小长(mm)</th>
              <th>最小宽(mm)</th>
              <th>最小克纸</th>
              <th>最大克纸</th>
              <th>是否UV机</th>
              <th>项目重定义价格</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(m, i) in machines" :key="i">
              <td><input type="checkbox" /></td>
              <td><input type="checkbox" /></td>
              <td>{{ m.type }}</td>
              <td><a href="#" class="link" @click.prevent>{{ m.name }}</a></td>
              <td>{{ m.bite }}</td>
              <td>{{ m.length }}</td>
              <td>{{ m.width }}</td>
              <td>{{ m.minLength }}</td>
              <td>{{ m.minWidth }}</td>
              <td>{{ m.minGram }}</td>
              <td>{{ m.maxGram }}</td>
              <td></td>
              <td></td>
              <td class="op">
                <a href="#" class="link" @click.prevent>修改</a>
                <a href="#" class="link" @click.prevent>删除</a>
                <a v-if="m.restore" href="#" class="link" @click.prevent>恢复使用通用价格</a>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="pager">
          <span>每页显示:</span>
          <select><option>5</option><option>10</option><option>20</option><option>25</option><option>50</option><option selected>100</option><option>200</option><option>500</option></select>
          <span>当前显示: 1 - {{ machines.length }}</span>
          <span>共: {{ machines.length }}</span>
          <button>首 页</button><button>上一页</button>
          <span>1 / 1</span>
          <button>下一页</button><button>末 页</button>
          <input class="ipt ipt-xs" type="text" /><button>跳 转</button><button>刷 新</button>
        </div>
        <p class="hint">*建议印刷机咬口设置不超过5毫米</p>
      </section>

      <!-- Tab3：纸张设置 -->
      <section v-show="activeTab === 'paper'" class="panel">
        <div class="panel-head">
          <span class="panel-title">专版无碳联单纸张设置</span>
          <div class="btn-group">
            <a href="#" class="btn btn-save" @click.prevent="savePapers">
              {{ paperSaving ? '保存中...' : '保存' }}
            </a>
            <a href="#" class="btn" @click.prevent="addPaperRow">增加行</a>
          </div>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>克重</th>
              <th>大度上纸单价(元/令)</th>
              <th>大度中纸单价(元/令)</th>
              <th>大度下纸单价(元/令)</th>
              <th>正度上纸单价(元/令)</th>
              <th>正度中纸单价(元/令)</th>
              <th>正度下纸单价(元/令)</th>
              <th>使用大度</th>
              <th>使用正度</th>
              <th>使用特规</th>
              <th>默认</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(p, i) in papers" :key="i">
              <td><input class="ipt ipt-xs" type="text" v-model="p.gram" /></td>
              <td><input class="ipt ipt-xs" type="text" v-model="p.duUp" /></td>
              <td><input class="ipt ipt-xs" type="text" v-model="p.duMid" /></td>
              <td><input class="ipt ipt-xs" type="text" v-model="p.duDown" /></td>
              <td><input class="ipt ipt-xs" type="text" v-model="p.zhengUp" /></td>
              <td><input class="ipt ipt-xs" type="text" v-model="p.zhengMid" /></td>
              <td><input class="ipt ipt-xs" type="text" v-model="p.zhengDown" /></td>
              <td><input type="checkbox" v-model="p.useDu" /></td>
              <td><input type="checkbox" v-model="p.useZheng" /></td>
              <td><input type="checkbox" v-model="p.useSpecial" /></td>
              <td><input type="checkbox" v-model="p.isDefault" /></td>
              <td class="op">
                <a href="#" class="link" @click.prevent>设定特规纸规格</a>
                <a href="#" class="link" @click.prevent="removePaperRow(i)">删除</a>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Tab4：后工参数设置 -->
      <section v-show="activeTab === 'post'" class="panel">
        <div class="panel-head">
          <span class="panel-title">后工参数设置</span>
          <div class="btn-group">
            <a href="#" class="btn btn-save" @click.prevent="savePostParams">
              {{ postSaving ? '保存中...' : '保存' }}
            </a>
          </div>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>名称</th>
              <th>单价</th>
              <th></th>
              <th>最低消费(开机费)（元）</th>
              <th>状态</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, i) in postParams" :key="i">
              <td>{{ row.name }}</td>
              <td><input class="ipt ipt-xs" type="text" v-model="row.unit_price" /></td>
              <td class="unit">{{ unitLabel(row.price_type) }}</td>
              <td><input class="ipt ipt-xs" type="text" v-model="row.min_charge" /></td>
              <td>
                <select v-model="row.is_active">
                  <option :value="true">可用</option>
                  <option :value="false">禁用</option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>
        <p class="service-tip">模切 / 其他后工 / 打包 / 运费为明细项，本期不参与算价。</p>
      </section>

      <!-- Tab5：成本附加设置 -->
      <section v-show="activeTab === 'cost'" class="panel">
        <div class="panel-head">
          <span class="panel-title">成本附加设置</span>
          <div class="btn-group">
            <a href="#" class="btn btn-save" @click.prevent="saveCostTiers">
              {{ costSaving ? '保存中...' : '保存' }}
            </a>
            <a href="#" class="btn" @click.prevent="addCostRow">增加行</a>
          </div>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th></th>
              <th>
                范围(
                <label class="ck"><input type="checkbox" v-model="cost.byAmount" /> 金额</label> /
                <label class="ck"><input type="checkbox" v-model="cost.byQty" /> 数量</label> )
                (<label class="ck"><input type="checkbox" v-model="cost.excludePaper" /> 金额不含纸款</label>)(单位：元)
              </th>
              <th>附加比率<br /><span class="th-sub">百分比</span></th>
              <th><span class="th-sub">固定值</span></th>
              <th>说明</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(seg, i) in costSegments" :key="i">
              <td>{{ seg.label }}</td>
              <td>
                <input class="ipt ipt-xs" type="text" v-model="seg.start" disabled />
                ～
                <input class="ipt ipt-xs" type="text" v-model="seg.end" :disabled="seg.endLocked" />
              </td>
              <td><input class="ipt ipt-xs" type="text" v-model="seg.rate" /> %</td>
              <td><input class="ipt ipt-xs" type="text" v-model="seg.fixed" /></td>
              <td>{{ seg.desc }}</td>
              <td class="op">
                <a v-if="seg.removable" href="#" class="link" @click.prevent="removeCostRow(i)">删除</a>
              </td>
            </tr>
          </tbody>
        </table>
        <h3 class="cost-formula">说明： 成本附加计算， 成本 = ( 材料 + 人工 ) × ( 1 + 百分比(%)) + 固定值。</h3>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import {
  getCostAddonTiers,
  saveCostAddonTiers,
  getPostProcessingParams,
  savePostProcessingParams,
  getUnionPaperPrices,
  saveUnionPaperPrices
} from '@/api/quote'
import type { CostAddonTierInput, PostProcessingParam } from '@/types/quote'

const CATEGORY_ID = 1

const tabs = [
  { key: 'base', label: '专版无碳联单参数' },
  { key: 'machine', label: '专版无碳联单印刷机' },
  { key: 'paper', label: '专版无碳联单纸张' },
  { key: 'post', label: '专版无碳联单后工' },
  { key: 'cost', label: '专版无碳联单成本附加' }
]
const activeTab = ref('base')

// Tab1 —— 专版其它参数
const base = reactive({
  deliveryCycle: '1-2日',
  designMode: '1',
  tplSimple: '80',
  tplUnit: 'p',
  sampleNormal: '100',
  creativeComplex: '200',
  m2Sample: '0',
  m2Creative: '0',
  m2Reverse: '0',
  m2SmallFix: '0',
  m2BigFix: '0',
  showWeightVolume: false,
  freightSelf: false,
  freightPost: false,
  freightSummary: false,
  diecutToPost: false
})

// Tab2 —— 印刷机
const machines = reactive([
  { type: '六开机', name: '海德堡6开四色机', bite: 8, length: 520, width: 360, minLength: 270, minWidth: 190, minGram: 0, maxGram: 0, restore: true },
  { type: '对开机', name: '小森920B对开机', bite: 10, length: 920, width: 620, minLength: 480, minWidth: 340, minGram: 0, maxGram: 0, restore: false },
  { type: '全开机', name: '1320全开', bite: 10, length: 1320, width: 1000, minLength: 720, minWidth: 500, minGram: 0, maxGram: 0, restore: false },
  { type: '全开机', name: '1620全开', bite: 10, length: 2100, width: 1600, minLength: 880, minWidth: 580, minGram: 0, maxGram: 0, restore: false }
])

// Tab3 —— 纸张（接后端）
interface PaperRow {
  gram: string
  duUp: string
  duMid: string
  duDown: string
  zhengUp: string
  zhengMid: string
  zhengDown: string
  useDu: boolean
  useZheng: boolean
  useSpecial: boolean
  isDefault: boolean
}
const papers = reactive<PaperRow[]>([])
const paperSaving = ref(false)

async function loadPapers() {
  try {
    const rows = await getUnionPaperPrices()
    papers.splice(0, papers.length, ...rows.map((r, i) => ({
      gram: String(r.weight),
      duUp: String(r.dadu_upper_price),
      duMid: String(r.dadu_middle_price),
      duDown: String(r.dadu_lower_price),
      zhengUp: String(r.zhengdu_upper_price),
      zhengMid: String(r.zhengdu_middle_price),
      zhengDown: String(r.zhengdu_lower_price),
      useDu: true,
      useZheng: true,
      useSpecial: false,
      isDefault: i === 0
    })))
  } catch (e: any) {
    console.error('加载纸张价格失败:', e?.message || e)
  }
}

async function savePapers() {
  if (paperSaving.value) return
  paperSaving.value = true
  try {
    const data = papers.map(p => ({
      weight: Number(p.gram) || 0,
      dadu_upper_price: Number(p.duUp) || 0,
      dadu_middle_price: Number(p.duMid) || 0,
      dadu_lower_price: Number(p.duDown) || 0,
      zhengdu_upper_price: Number(p.zhengUp) || 0,
      zhengdu_middle_price: Number(p.zhengMid) || 0,
      zhengdu_lower_price: Number(p.zhengDown) || 0,
      is_active: true
    }))
    await saveUnionPaperPrices({ papers: data })
    alert('纸张价格已保存')
    await loadPapers()
  } catch (e: any) {
    alert('保存失败：' + (e?.message || e))
  } finally {
    paperSaving.value = false
  }
}

function addPaperRow() {
  papers.push({
    gram: '', duUp: '0', duMid: '0', duDown: '0',
    zhengUp: '0', zhengMid: '0', zhengDown: '0',
    useDu: true, useZheng: true, useSpecial: false, isDefault: false
  })
}

function removePaperRow(index: number) {
  papers.splice(index, 1)
}

// Tab4 —— 后工参数（接后端）
const postParams = reactive<PostProcessingParam[]>([])
const postSaving = ref(false)

// 计价单位 -> 中文标签
const UNIT_LABELS: Record<string, string> = {
  per_book: '元/本',
  per_plate: '元/版',
  per_page: '元/页',
  per_sheet_count: '元/联',
  per_unit: '元/个',
  per_thousand: '元/千',
  fixed: '元/次'
}
function unitLabel(priceType: string): string {
  return UNIT_LABELS[priceType] || priceType
}

async function loadPostParams() {
  try {
    const rows = await getPostProcessingParams()
    postParams.splice(0, postParams.length, ...rows)
  } catch (e: any) {
    console.error('加载后工参数失败:', e?.message || e)
  }
}

async function savePostParams() {
  if (postSaving.value) return
  postSaving.value = true
  try {
    // 单价/最低消费在输入框里可能变成字符串，落库前转数字
    const params = postParams.map((r) => ({
      name: r.name,
      code: r.code,
      group_code: r.group_code,
      price_type: r.price_type,
      unit_price: Number(r.unit_price) || 0,
      min_charge: Number(r.min_charge) || 0,
      min_kai: r.min_kai,
      max_kai: r.max_kai,
      sort_order: r.sort_order,
      is_active: r.is_active
    }))
    const saved = await savePostProcessingParams({ params })
    postParams.splice(0, postParams.length, ...saved)
    alert('后工参数已保存')
  } catch (e: any) {
    alert('保存失败：' + (e?.message || e))
  } finally {
    postSaving.value = false
  }
}

// Tab5 —— 成本附加
const cost = reactive({
  byAmount: true,
  byQty: false,
  excludePaper: false
})

interface CostSegment {
  label: string
  start: string   // 区间下限，仅展示（= 上一段 end）
  end: string     // 区间上限，唯一可编辑边界；最后一段为无限大
  endLocked: boolean
  rate: string    // 附加比率，百分比字符串（如 '10.0'）
  fixed: string   // 固定值（元）
  desc: string
  removable: boolean
}

const costSegments = reactive<CostSegment[]>([])
const costSaving = ref(false)

// 后端档位 -> 界面段。后端为半开区间 [min_cost, max_cost)，
// 界面 start 显示为该段下限，end 显示为上限（无上限段显示“无限大”）。
function tiersToSegments(tiers: { min_cost: number; max_cost: number | null; rate: number; fixed_addon: number }[]): CostSegment[] {
  if (!tiers.length) return [defaultSegment(1, true)]
  return tiers.map((t, i) => {
    const isLast = t.max_cost === null || t.max_cost === undefined
    return {
      label: `第${i + 1}段`,
      start: String(t.min_cost),
      end: isLast ? '无限大' : String(t.max_cost),
      endLocked: isLast,
      rate: (t.rate * 100).toFixed(1),
      fixed: String(t.fixed_addon ?? 0),
      desc: `第${i + 1}段金额范围利率`,
      removable: i > 0 && !isLast
    }
  })
}

function defaultSegment(index: number, isLast = false): CostSegment {
  return {
    label: `第${index}段`,
    start: '0',
    end: isLast ? '无限大' : '0',
    endLocked: isLast,
    rate: '10.0',
    fixed: '0',
    desc: `第${index}段金额范围利率`,
    removable: index > 1 && !isLast
  }
}

// 界面段 -> 后端档位。以每段 end 作为唯一边界源：
// 第 i 段 min_cost = 上一段 end（首段为 0），max_cost = 本段 end（末段为 null），
// 从根本上规避“1001 vs 1000”这种边界缝隙。
function segmentsToTiers(): CostAddonTierInput[] {
  const tiers: CostAddonTierInput[] = []
  let prevEnd = 0
  costSegments.forEach((seg, i) => {
    const isLast = seg.endLocked
    const rate = parseFloat(seg.rate)
    const fixed = parseFloat(seg.fixed)
    tiers.push({
      min_cost: prevEnd,
      max_cost: isLast ? null : Number(seg.end),
      rate: isNaN(rate) ? 0 : rate / 100,
      fixed_addon: isNaN(fixed) ? 0 : fixed,
      sort_order: i + 1
    })
    if (!isLast) prevEnd = Number(seg.end)
  })
  return tiers
}

function relabelSegments() {
  costSegments.forEach((seg, i) => {
    seg.label = `第${i + 1}段`
    seg.desc = `第${i + 1}段金额范围利率`
    // 下限跟随上一段上限，保持展示一致
    seg.start = i === 0 ? '0' : costSegments[i - 1].end
    seg.removable = i > 0 && !seg.endLocked
  })
}

function addCostRow() {
  // 在“无限大”末段之前插入一行
  const lastLocked = costSegments.length && costSegments[costSegments.length - 1].endLocked
  const insertAt = lastLocked ? costSegments.length - 1 : costSegments.length
  costSegments.splice(insertAt, 0, defaultSegment(insertAt + 1))
  relabelSegments()
}

function removeCostRow(index: number) {
  costSegments.splice(index, 1)
  relabelSegments()
}

async function loadCostTiers() {
  try {
    const tiers = await getCostAddonTiers(CATEGORY_ID)
    costSegments.splice(0, costSegments.length, ...tiersToSegments(tiers))
    // 确保存在无限大末段
    if (!costSegments.some(s => s.endLocked)) {
      costSegments.push(defaultSegment(costSegments.length + 1, true))
    }
    relabelSegments()
  } catch (e: any) {
    console.error('加载成本附加档位失败:', e?.message || e)
  }
}

async function saveCostTiers() {
  if (costSaving.value) return
  const tiers = segmentsToTiers()

  // 基本校验：非末段的 end 必须递增且为正数
  let prev = 0
  for (const t of tiers) {
    if (t.max_cost !== null) {
      if (t.max_cost <= prev) {
        alert(`区间上限必须递增：${t.max_cost} 应大于 ${prev}`)
        return
      }
      prev = t.max_cost
    }
  }

  costSaving.value = true
  try {
    const saved = await saveCostAddonTiers({ category_id: CATEGORY_ID, tiers })
    costSegments.splice(0, costSegments.length, ...tiersToSegments(saved))
    if (!costSegments.some(s => s.endLocked)) {
      costSegments.push(defaultSegment(costSegments.length + 1, true))
    }
    relabelSegments()
    alert('成本附加档位已保存')
  } catch (e: any) {
    alert('保存失败：' + (e?.message || e))
  } finally {
    costSaving.value = false
  }
}

onMounted(() => {
  loadCostTiers()
  loadPostParams()
  loadPapers()
})
</script>

<style scoped>
.params-page {
  width: 100%;
  font-size: var(--font-size-sm);
}

.params-crumb {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-xs);
  color: var(--text-secondary);
}

.crumb-item.active {
  color: var(--primary-color);
}

.crumb-sep {
  color: var(--text-disabled);
}

/* Tab 头 */
.params-tabs {
  display: flex;
  gap: 2px;
  border-bottom: 2px solid var(--primary-color);
}

.params-tab {
  padding: var(--spacing-sm) var(--spacing-lg);
  background: #eef2f5;
  border: 1px solid var(--border-color);
  border-bottom: none;
  color: var(--text-primary);
  text-decoration: none;
  border-radius: var(--border-radius-sm) var(--border-radius-sm) 0 0;
}

.params-tab:hover {
  background: #e3ebf1;
}

.params-tab.active {
  background: var(--primary-color);
  color: #fff;
  border-color: var(--primary-color);
}

.params-body {
  border: 1px solid var(--border-color);
  border-top: none;
  padding: var(--spacing-md);
  background: #fff;
}

.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--spacing-md);
}

.panel-title {
  font-size: var(--font-size-md);
  font-weight: 700;
  color: var(--table-header-text);
}

.btn-group {
  display: flex;
  gap: var(--spacing-sm);
}

.btn {
  display: inline-block;
  padding: var(--spacing-xs) var(--spacing-md);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  background: #f7f7f7;
  color: var(--text-primary);
  text-decoration: none;
}

.btn:hover {
  background: #ececec;
}

.btn-save {
  background: var(--primary-color);
  color: #fff;
  border-color: var(--primary-color);
}

.btn-save:hover {
  background: var(--primary-hover);
}

/* 表单式表格（Tab1） */
.form-table {
  border-collapse: collapse;
  width: 100%;
}

.form-table th {
  text-align: right;
  vertical-align: top;
  width: 120px;
  padding: var(--spacing-sm);
  color: var(--text-secondary);
  font-weight: 400;
  white-space: nowrap;
}

.form-table td {
  padding: var(--spacing-sm);
  border-bottom: 1px dashed #eee;
}

.sub-line {
  margin: var(--spacing-xs) 0 var(--spacing-xs) var(--spacing-lg);
  color: var(--text-secondary);
}

.unit-group {
  color: var(--text-disabled);
}

/* 数据表格（Tab2-5） */
.data-table {
  border-collapse: collapse;
  width: 100%;
}

.data-table th,
.data-table td {
  border: 1px solid var(--table-border);
  padding: var(--spacing-xs) var(--spacing-sm);
  text-align: center;
  white-space: nowrap;
}

.data-table thead th {
  background: var(--table-header-bg);
  color: var(--table-header-text);
  font-weight: 700;
}

.data-table tbody tr:hover {
  background: var(--table-hover);
}

.th-sub {
  font-weight: 400;
  color: var(--text-secondary);
}

.op {
  display: flex;
  gap: var(--spacing-sm);
  justify-content: center;
  flex-wrap: wrap;
}

.unit {
  color: var(--text-secondary);
}

.link {
  color: var(--primary-color);
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

/* 输入框 */
.ipt {
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  padding: 2px 4px;
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  width: 160px;
}

.ipt:disabled {
  background: #f2f2f2;
  color: var(--text-disabled);
}

.ipt-sm {
  width: 70px;
}

.ipt-xs {
  width: 56px;
  text-align: center;
}

.ck {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  margin-right: var(--spacing-md);
  cursor: pointer;
}

/* 分页条 */
.pager {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-md);
  color: var(--text-secondary);
  flex-wrap: wrap;
}

.pager select,
.pager button {
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  background: #f7f7f7;
  padding: 2px 6px;
  cursor: pointer;
}

.hint {
  margin-top: var(--spacing-sm);
  color: var(--danger-color);
}

.service-tip {
  margin-top: var(--spacing-lg);
  color: var(--text-disabled);
}

.cost-formula {
  margin-top: var(--spacing-md);
  font-size: var(--font-size-sm);
  font-weight: 400;
  color: var(--text-secondary);
}
</style>
