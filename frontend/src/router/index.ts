import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '首页' }
  },
  {
    path: '/quote/liandan',
    name: 'liandan',
    component: () => import('@/views/LiandanQuote.vue'),
    meta: { title: '专版联单报价' }
  },
  // 兼容旧入口：/quote 直接跳到联单
  {
    path: '/quote',
    redirect: '/quote/liandan'
  },
  // 未实现的品类统一回首页
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

router.afterEach((to) => {
  const title = (to.meta?.title as string) || '印刷报价系统'
  document.title = `${title} - 印刷报价系统`
})

export default router
