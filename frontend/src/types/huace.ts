export interface HuaceSize {
  id: number
  name: string
  width: number
  height: number
  code: string | null
}

export interface HuaceSize {
  id: number
  name: string
  width: number
  height: number
  code: string | null
}

export interface HuacePaper {
  id: number
  paper_category: string
  paper_name: string
  weight: number
  ton_price: number
}

export interface HuaceColor {
  id: number
  component: string
  color_code: string
  color_name: string
  price_per_version: number
}

export interface HuaceBinding {
  id: number
  code: string
  name: string
  price_type: string
  unit_price: number
  min_charge: number
}

export interface HuacePostProcessing {
  id: number
  code: string
  name: string
  proc_group: string
  price_type: string
  unit_price: number
  min_charge: number
}

export interface HuaceClientTier {
  id: number
  code: string
  name: string
  multiplier: number
  remark: string | null
}

export interface HuaceQuoteRequest {
  size_id: number
  quantity: number
  cover_paper_name: string
  cover_paper_weight: number
  cover_paper_ton_price: number
  cover_pages: number
  cover_color_code: string
  cover_both_sides?: boolean
  inner_paper_name: string
  inner_paper_weight: number
  inner_paper_ton_price: number
  inner_pages: number
  inner_color_code: string
  binding_code: string
  surface_treatment?: string
  other_processing?: string[]
  client_tier_code?: string
  multi_quantities?: number[]
  customer_name?: string
  product_name?: string
}

export interface HuaceCostBreakdown {
  paper_cost: number
  printing_cost: number
  surface_cost: number
  binding_cost: number
  other_post_cost: number
  total_cost: number
}

export interface HuaceTierPrice {
  code: string
  name: string
  multiplier: number
  total_price: number
  unit_price: number
}

export interface HuaceLadderPrice {
  quantity: number
  cost_breakdown: HuaceCostBreakdown
  tier_prices: HuaceTierPrice[]
}

export interface HuaceQuoteResponse {
  quantity: number
  cost_breakdown: HuaceCostBreakdown
  tier_prices: HuaceTierPrice[]
  ladder_prices: HuaceLadderPrice[]
  quote_id?: string
  quote_time?: string
}
