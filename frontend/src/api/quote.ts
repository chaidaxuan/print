import request from '@/utils/request'
import type {
  ProductSize,
  PrintingColor,
  PostProcessing,
  LiandanQuoteRequest,
  LiandanQuoteResponse,
  CostAddonTier,
  CostAddonTierSaveRequest,
  PostProcessingParam,
  PostProcessingParamSaveRequest,
  UnionPaperPrice,
  UnionPaperPriceSaveRequest
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

/**
 * 获取成本附加阶梯档位
 */
export function getCostAddonTiers(categoryId: number = 1): Promise<CostAddonTier[]> {
  return request.get('/quote/cost-addon-tiers', { params: { category_id: categoryId } })
}

/**
 * 整表保存成本附加阶梯档位
 */
export function saveCostAddonTiers(data: CostAddonTierSaveRequest): Promise<CostAddonTier[]> {
  return request.put('/quote/cost-addon-tiers', data)
}

/**
 * 获取后工参数全表
 */
export function getPostProcessingParams(): Promise<PostProcessingParam[]> {
  return request.get('/quote/post-processing-params')
}

/**
 * 整表保存后工参数
 */
export function savePostProcessingParams(data: PostProcessingParamSaveRequest): Promise<PostProcessingParam[]> {
  return request.put('/quote/post-processing-params', data)
}

/**
 * 获取联单纸张分层价格
 */
export function getUnionPaperPrices(): Promise<UnionPaperPrice[]> {
  return request.get('/quote/union-paper-prices')
}

/**
 * 整表保存联单纸张分层价格
 */
export function saveUnionPaperPrices(data: UnionPaperPriceSaveRequest): Promise<UnionPaperPrice[]> {
  return request.put('/quote/union-paper-prices', data)
}
