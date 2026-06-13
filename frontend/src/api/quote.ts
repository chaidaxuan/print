import request from '@/utils/request'
import type {
  ProductSize,
  PrintingColor,
  PostProcessing,
  LiandanQuoteRequest,
  LiandanQuoteResponse
} from '@/types/quote'

/**
 * 获取成品尺寸列表
 */
export function getSizes(categoryId: number = 1): Promise<ProductSize[]> {
  return request.get('/quote/sizes', { params: { category_id: categoryId } })
}

/**
 * 获取印刷颜色列表
 */
export function getColors(): Promise<PrintingColor[]> {
  return request.get('/quote/colors')
}

/**
 * 获取后道工序列表
 */
export function getPostProcessing(): Promise<PostProcessing[]> {
  return request.get('/quote/post-processing')
}

/**
 * 计算无碳联单报价
 */
export function calculateLiandanQuote(data: LiandanQuoteRequest): Promise<LiandanQuoteResponse> {
  return request.post('/quote/liandan', data)
}

/**
 * 获取报价历史
 */
export function getQuoteHistory(limit: number = 20, offset: number = 0): Promise<any> {
  return request.get('/quote/history', { params: { limit, offset } })
}
