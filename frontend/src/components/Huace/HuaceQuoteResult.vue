<template>
  <div class="huace-result" v-if="result">
    <!-- 成本明细 -->
    <div class="cost-breakdown">
      <h4>成本明细（{{ result.quantity }}本）</h4>
      <table class="detail-table">
        <tbody>
          <tr>
            <th>纸款</th>
            <td>¥{{ result.cost_breakdown.paper_cost.toFixed(2) }}</td>
          </tr>
          <tr>
            <th>印刷费</th>
            <td>¥{{ result.cost_breakdown.printing_cost.toFixed(2) }}</td>
          </tr>
          <tr v-if="result.cost_breakdown.surface_cost > 0">
            <th>表面处理</th>
            <td>¥{{ result.cost_breakdown.surface_cost.toFixed(2) }}</td>
          </tr>
          <tr>
            <th>装订费</th>
            <td>¥{{ result.cost_breakdown.binding_cost.toFixed(2) }}</td>
          </tr>
          <tr v-if="result.cost_breakdown.other_post_cost > 0">
            <th>其他后道</th>
            <td>¥{{ result.cost_breakdown.other_post_cost.toFixed(2) }}</td>
          </tr>
          <tr class="row-total">
            <th>生产成本合计</th>
            <td>¥{{ result.cost_breakdown.total_cost.toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 各客户类型报价 -->
    <div class="tier-prices" v-if="result.tier_prices && result.tier_prices.length > 0">
      <h4>各客户类型报价</h4>
      <table class="detail-table">
        <thead>
          <tr>
            <th>客户类型</th>
            <th>倍率</th>
            <th>单价</th>
            <th>总价</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in result.tier_prices" :key="t.code">
            <td>{{ t.name }}</td>
            <td>×{{ t.multiplier.toFixed(2) }}</td>
            <td>¥{{ t.unit_price.toFixed(4) }}</td>
            <td>¥{{ t.total_price.toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 多数量阶梯 -->
    <div class="ladder-prices" v-if="result.ladder_prices && result.ladder_prices.length > 1">
      <h4>多数量报价</h4>
      <table class="detail-table">
        <thead>
          <tr>
            <th>数量(本)</th>
            <th>成本</th>
            <th v-for="t in result.ladder_prices[0].tier_prices" :key="t.code">
              {{ t.name }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lp in result.ladder_prices" :key="lp.quantity">
            <td>{{ lp.quantity }}</td>
            <td>¥{{ lp.cost_breakdown.total_cost.toFixed(2) }}</td>
            <td v-for="t in lp.tier_prices" :key="t.code">
              ¥{{ t.total_price.toFixed(2) }}
              <span class="unit-price">（¥{{ t.unit_price.toFixed(4) }}/本）</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { HuaceQuoteResponse } from '@/types/huace'

interface Props {
  result: HuaceQuoteResponse | null
  loading?: boolean
}

defineProps<Props>()
</script>

<style scoped>
.huace-result {
  background: white;
  border-radius: var(--border-radius-md);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
}

.cost-breakdown,
.tier-prices,
.ladder-prices {
  margin-top: 20px;
}

.cost-breakdown:first-child {
  margin-top: 0;
}

.cost-breakdown h4,
.tier-prices h4,
.ladder-prices h4 {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.detail-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.detail-table th,
.detail-table td {
  padding: 6px 12px;
  border-bottom: 1px solid #f0f0f0;
  text-align: left;
}

.detail-table thead th {
  background: #fafafa;
  font-weight: 600;
}

.detail-table tbody th {
  font-weight: 400;
  color: var(--text-secondary);
}

.row-total th,
.row-total td {
  font-weight: 600;
  color: var(--text-primary);
  border-top: 1px solid var(--border-color);
}

.unit-price {
  font-size: 11px;
  color: var(--text-secondary);
}
</style>
