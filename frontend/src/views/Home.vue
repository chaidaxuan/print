<template>
  <div class="home-page">
    <ul class="product-grid">
      <li
        v-for="item in products"
        :key="item.code"
        class="product-item"
        :class="{ disabled: !item.enabled }"
        @click="handleClick(item)"
      >
        <div class="product-thumb">
          <img :src="item.img" :alt="item.label" loading="lazy" />
        </div>
        <p class="product-name">{{ item.label }}</p>
      </li>
    </ul>

    <div class="promo-banner">
      <p class="promo-line-1">告别手工算价、告别报价慢、告别错漏频出！</p>
      <p class="promo-line-2">优效报价软件，一键精准核算印刷成本，</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

interface Product {
  label: string
  code: string
  img: string
  enabled: boolean
  path?: string
}

const router = useRouter()

// 按参考站首页顺序排列，缩略图取自演示系统的真实产品图，联单已接通真实报价
const products: Product[] = [
  { label: '表格便笺', code: 'biaoge', img: '/products/14.jpg', enabled: false },
  { label: '彩盒彩箱', code: 'caihe', img: '/products/6.jpg', enabled: false },
  { label: '专版不干胶', code: 'buganjiao', img: '/products/4.jpg', enabled: false },
  { label: '纸盒纸箱', code: 'zhihe', img: '/products/10.jpg', enabled: false },
  { label: '纸袋', code: 'zhidai', img: '/products/22.jpg', enabled: false },
  { label: '特价不干胶', code: 'tj-buganjiao', img: '/products/107.jpg', enabled: false },
  { label: '精品盒', code: 'jingpin', img: '/products/17.jpg', enabled: false },
  { label: '特价精品盒', code: 'tj-jingpin', img: '/products/121.jpg', enabled: false },
  { label: '专版画册', code: 'huace', img: '/products/2.jpg', enabled: true, path: '/quote/huace' },
  { label: '特价单张', code: 'danzhang', img: '/products/101.jpg', enabled: false },
  { label: '特价画册', code: 'tj-huace', img: '/products/108.jpg', enabled: false },
  { label: '信封', code: 'xinfeng', img: '/products/15.jpg', enabled: false },
  { label: '手提袋', code: 'shouti', img: '/products/3.jpg', enabled: false },
  { label: '专版单页', code: 'danye', img: '/products/1.jpg', enabled: false },
  { label: '彩卡吊牌', code: 'caika', img: '/products/7.jpg', enabled: false },
  { label: '封套', code: 'fengtao', img: '/products/5.jpg', enabled: false },
  { label: '游戏卡牌', code: 'kapai', img: '/products/19.jpg', enabled: false },
  { label: '小批量彩盒', code: 'xpl-caihe', img: '/products/115.jpg', enabled: false },
  { label: '环保纸袋', code: 'hb-zhidai', img: '/products/20.jpg', enabled: false },
  { label: '特价信封', code: 'tj-xinfeng', img: '/products/116.jpg', enabled: false },
  { label: '数码打印', code: 'shuma', img: '/products/122.jpg', enabled: false },
  { label: '软包装', code: 'ruanbaozhuang', img: '/products/21.jpg', enabled: false },
  { label: '无纺布袋', code: 'wfb', img: '/products/114.jpg', enabled: false },
  { label: 'PVC卡', code: 'pvc', img: '/products/103.jpg', enabled: false },
  { label: '特价纸抽盒', code: 'tj-zhichou', img: '/products/117.jpg', enabled: false },
  { label: '特价环保纸袋', code: 'tj-hbzd', img: '/products/123.jpg', enabled: false },
  { label: '无碳联单', code: 'liandan', img: '/products/16.jpg', enabled: false },
  { label: '特价联单', code: 'tj-liandan', img: '/products/105.jpg', enabled: true, path: '/quote/liandan' },
  { label: '对联', code: 'duilian', img: '/products/24.jpg', enabled: false },
  { label: '笔记本', code: 'biji', img: '/products/23.jpg', enabled: false },
  { label: '防伪标', code: 'fangwei', img: '/products/12.jpg', enabled: false },
  { label: '专业喷绘', code: 'penhui', img: '/products/130.jpg', enabled: false },
  { label: '专业不干胶', code: 'zy-buganjiao', img: '/products/18.jpg', enabled: false },
  { label: '食品袋', code: 'shipindai', img: '/products/25.jpg', enabled: false }
]

const handleClick = (item: Product) => {
  if (item.enabled && item.path) {
    router.push(item.path)
  }
}
</script>

<style scoped>
.home-page {
  width: 100%;
}

.product-grid {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(10, 1fr);
  gap: var(--spacing-md);
  padding: var(--spacing-sm);
}

.product-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) 0;
  cursor: pointer;
}

.product-item.disabled {
  cursor: default;
}

.product-thumb {
  width: 80px;
  height: 80px;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-sm);
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  transition: box-shadow 0.2s, transform 0.2s;
}

.product-thumb img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.product-item:not(.disabled):hover .product-thumb {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.product-name {
  font-size: var(--font-size-sm);
  color: var(--text-primary);
  text-align: center;
}

.promo-banner {
  margin: var(--spacing-md) var(--spacing-sm) var(--spacing-sm);
  background: linear-gradient(120deg, #c0140a 0%, #e2241a 45%, #a01008 100%);
  border-radius: var(--border-radius-sm);
  padding: var(--spacing-xl);
  min-height: 150px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: var(--spacing-md);
}

.promo-line-1,
.promo-line-2 {
  margin: 0;
  color: #ffe14d;
  font-weight: 700;
  font-size: 30px;
  letter-spacing: 2px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

@media (max-width: 1024px) {
  .product-grid {
    grid-template-columns: repeat(7, 1fr);
  }
}
</style>
