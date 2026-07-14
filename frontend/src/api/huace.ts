import request from '@/utils/request'
import type {
  HuacePaper,
  HuaceColor,
  HuaceBinding,
  HuacePostProcessing,
  HuaceClientTier,
  HuaceSize,
  HuaceQuoteRequest,
  HuaceQuoteResponse
} from '@/types/huace'

export function getHuaceSizes(): Promise<HuaceSize[]> {
  return request.get('/quote/huace/sizes')
}

export function getHuacePapers(): Promise<HuacePaper[]> {
  return request.get('/quote/huace/papers')
}

export function getHuaceColors(): Promise<HuaceColor[]> {
  return request.get('/quote/huace/colors')
}

export function getHuaceBindings(): Promise<HuaceBinding[]> {
  return request.get('/quote/huace/bindings')
}

export function getHuacePostProcessing(): Promise<HuacePostProcessing[]> {
  return request.get('/quote/huace/post-processing')
}

export function getHuaceClientTiers(): Promise<HuaceClientTier[]> {
  return request.get('/quote/huace/client-tiers')
}

export function calculateHuaceQuote(data: HuaceQuoteRequest): Promise<HuaceQuoteResponse> {
  return request.post('/quote/huace/calculate', data)
}
