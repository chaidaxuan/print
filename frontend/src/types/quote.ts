export interface ProductSize {
  id: number
  name: string
  width: number
  height: number
  code: string | null
}

export interface PrintingColor {
  id: number
  name: string
  code: string
  plate_count: number
}

export interface PostProcessing {
  id: number
  name: string
  code: string
  description: string | null
}

export interface LiandanQuoteRequest {
  size_id: number
  quantity: number
  sheet_count: number
  pages_per_book: number
  color_code: string
  gram_weight: number
  post_processing: string[]
  custom_width?: number | null
  custom_height?: number | null
  profit_rate?: number | null
  customer_name?: string
  product_name?: string
}

export interface CostBreakdown {
  paper_cost: number
  printing_cost: number
  post_processing_cost: number
  production_cost: number
  cost_addon: number
  total_cost: number
}

export interface MachineInfo {
  name: string
  printing_size: string
  plates: number
  pieces_per_plate: number
  sheets_to_print: number
  paper_sheets: number
}

export interface LadderPrice {
  quantity: number
  unit_price: number
  total_price: number
}

export interface LiandanQuoteResponse {
  quantity: number
  unit_price: number
  total_price: number
  cost_breakdown: CostBreakdown
  machine_info: MachineInfo
  ladder_prices: LadderPrice[]
}
