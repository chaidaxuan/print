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
            <a href="#" class="btn btn-save" @click.prevent>保存</a>
            <a href="#" class="btn" @click.prevent>增加行</a>
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
              <td><input class="ipt ipt-xs" type="text" v-model="p.gram" disabled /></td>
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
                <a href="#" class="link" @click.prevent>删除</a>
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
            <a href="#" class="btn btn-save" @click.prevent>保存</a>
            <a href="#" class="btn" @click.prevent>初始化参数</a>
          </div>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>名称</th>
              <th>单价</th>
              <th></th>
              <th>最低消费(开机费)（元）</th>
              <th>每张(个)最低单价（元）</th>
              <th></th>
              <th>模板费最低收费(元)</th>
              <th>模板费每拼最低收费(元)</th>
              <th>计算次数</th>
              <th>状态</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, i) in postProcessing" :key="i">
              <td>{{ row.name }}</td>
              <!-- 特殊行：仅有明细链接 -->
              <template v-if="row.detailOnly">
                <td colspan="7">
                  <template v-if="row.diecut">
                    模切费计算方式:
                    <label class="ck"><input type="radio" name="diecut" value="1" v-model="diecutMode" /> 一(按张计算)</label>
                    <label class="ck"><input type="radio" name="diecut" value="2" v-model="diecutMode" /> 二(按千张计算)</label>
                  </template>
                  <a href="#" class="link" @click.prevent>查看收费明细</a>
                </td>
              </template>
              <template v-else>
                <td><input class="ipt ipt-xs" type="text" v-model="row.price" /></td>
                <td class="unit">{{ row.unit }}</td>
                <td><input class="ipt ipt-xs" type="text" v-model="row.minCharge" /></td>
                <td>
                  <template v-if="row.perMin !== undefined">
                    <input class="ipt ipt-xs" type="text" v-model="row.perMin" />
                    <span v-if="row.perMinSuffix"> {{ row.perMinSuffix }}</span>
                  </template>
                </td>
                <td>
                  <template v-if="row.freeQty !== undefined">
                    <input class="ipt ipt-xs" type="text" v-model="row.freeQty" /> 个免收费
                  </template>
                </td>
                <td><input v-if="row.tplMin !== undefined" class="ipt ipt-xs" type="text" v-model="row.tplMin" /></td>
                <td><input v-if="row.tplPerMin !== undefined" class="ipt ipt-xs" type="text" v-model="row.tplPerMin" /></td>
                <td>{{ row.calcCount }}</td>
              </template>
              <td>
                <select :disabled="row.statusLocked">
                  <option selected>可用</option>
                  <option>禁用</option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Tab5：成本附加设置 -->
      <section v-show="activeTab === 'cost'" class="panel">
        <div class="panel-head">
          <span class="panel-title">成本附加设置</span>
          <div class="btn-group">
            <a href="#" class="btn btn-save" @click.prevent>保存</a>
            <a href="#" class="btn" @click.prevent>增加行</a>
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
                <a v-if="seg.removable" href="#" class="link" @click.prevent>删除</a>
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
import { ref, reactive } from 'vue'

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

// Tab3 —— 纸张
const papers = reactive([
  { gram: '50', duUp: '350', duMid: '470', duDown: '350', zhengUp: '280', zhengMid: '350', zhengDown: '280', useDu: true, useZheng: true, useSpecial: false, isDefault: true },
  { gram: '80', duUp: '450', duMid: '570', duDown: '450', zhengUp: '380', zhengMid: '450', zhengDown: '380', useDu: true, useZheng: true, useSpecial: false, isDefault: false },
  { gram: '108', duUp: '480', duMid: '590', duDown: '480', zhengUp: '300', zhengMid: '4900', zhengDown: '300', useDu: true, useZheng: true, useSpecial: false, isDefault: false }
])

// Tab4 —— 后工
const diecutMode = ref('1')
const postProcessing = reactive<any[]>([
  { name: '加卡纸(10开-8开)', price: '0.4', unit: '元/本', minCharge: '30', calcCount: '0', statusLocked: false },
  { name: '加卡纸(11开-18开)', price: '0.2', unit: '元/本', minCharge: '30', calcCount: '0', statusLocked: true },
  { name: '加卡纸(20开-50开)', price: '0.2', unit: '元/本', minCharge: '30', calcCount: '0', statusLocked: true },
  { name: '加卡纸(50开以上)', price: '0.2', unit: '元/本', minCharge: '30', calcCount: '0', statusLocked: true },
  { name: '加封面', price: '0.3', unit: '元/本', minCharge: '30', calcCount: '0', statusLocked: false },
  { name: '印封面', price: '0.3', unit: '元/本', minCharge: '30', calcCount: '0', statusLocked: false },
  { name: '压点线', price: '0.01', unit: '元/版', minCharge: '30', tplMin: '30', calcCount: '0', statusLocked: false },
  { name: '彩色联单加号码', price: '0.02', unit: '元/页', minCharge: '0', perMin: '0', perMinSuffix: '单黑', freeQty: '0', calcCount: '0', statusLocked: false },
  { name: '装订(10开-8开)', price: '0.3', unit: '元/本', minCharge: '20', calcCount: '0', statusLocked: true },
  { name: '装订(11开-18开)', price: '0.3', unit: '元/本', minCharge: '20', calcCount: '0', statusLocked: true },
  { name: '装订(20开-50开)', price: '0.1', unit: '元/本', minCharge: '20', calcCount: '9', statusLocked: true },
  { name: '装订(50开以上)', price: '0.1', unit: '元/本', minCharge: '20', calcCount: '0', statusLocked: true },
  { name: '换边联字', price: '10', unit: '元/联', minCharge: '30', perMin: '0', calcCount: '0', statusLocked: false },
  { name: '模切', detailOnly: true, diecut: true, statusLocked: true },
  { name: '其他后工', detailOnly: true, statusLocked: false },
  { name: '打包', detailOnly: true, statusLocked: false },
  { name: '运费', detailOnly: true, statusLocked: true }
])

// Tab5 —— 成本附加
const cost = reactive({
  byAmount: true,
  byQty: false,
  excludePaper: false
})
const costSegments = reactive([
  { label: '第1段', start: '0', end: '1000', endLocked: false, rate: '10.0', fixed: '200', desc: '第1段金额范围利率', removable: false },
  { label: '第2段', start: '1001', end: '3000', endLocked: false, rate: '10.0', fixed: '150', desc: '第2段金额范围利率', removable: true },
  { label: '第3段', start: '3001', end: '5000', endLocked: false, rate: '10.0', fixed: '0', desc: '第3段金额范围利率', removable: true },
  { label: '第4段', start: '5001', end: '10000', endLocked: false, rate: '10.0', fixed: '0', desc: '第4段金额范围利率', removable: true },
  { label: '第5段', start: '10001', end: '0', endLocked: false, rate: '10.0', fixed: '0', desc: '第5段金额范围利率', removable: true },
  { label: '第6段', start: '1', end: '0', endLocked: false, rate: '10.0', fixed: '0', desc: '第6段金额范围利率', removable: true },
  { label: '第7段', start: '1', end: '0', endLocked: false, rate: '10.0', fixed: '0', desc: '第7段金额范围利率', removable: true },
  { label: '第8段', start: '1', end: '0', endLocked: false, rate: '10.0', fixed: '0', desc: '第8段金额范围利率', removable: true },
  { label: '第9段', start: '1', end: '0', endLocked: false, rate: '10.0', fixed: '0', desc: '第9段金额范围利率', removable: true },
  { label: '第10段', start: '最大结束数量', end: '无限大', endLocked: true, rate: '10.0', fixed: '0', desc: '第10段金额范围利率', removable: false }
])
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
