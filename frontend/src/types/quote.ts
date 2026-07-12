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
  spoilage?: number
}

export interface LadderPrice {
  quantity: number
  unit_price: number
  total_price: number
}

export interface MachineCostDetail {
  name: string
  printing_size: string
  plates: number
  pieces_layout: string
  sheets_to_print: number
  paper_sheets: number
  paper_cost: number
  printing_cost: number
  post_processing_cost: number
  production_cost: number
  cost_addon: number
  total_cost: number
  is_recommended: boolean
}

export interface LiandanQuoteResponse {
  quantity: number
  unit_price: number
  total_price: number
  cost_breakdown: CostBreakdown
  machine_info: MachineInfo
  ladder_prices: LadderPrice[]
  all_machines: MachineCostDetail[]
  // —— 成本明细弹窗新增 ——
  calc_trace?: CalcTrace
  post_processing_items?: PostProcItem[]
  weight_kg?: number
  volume_m3?: number
  paper_series?: string
  cut_type?: string
  quote_id?: string
  quote_time?: string
}

export interface CalcStep {
  key: string
  label: string
  formula: string
  substituted: string
  result: number | string
  unit?: string
}

export interface CutLevel {
  per_full: number
  level_name: string
  cut_w: number
  cut_h: number
  fits: boolean
  selected: boolean
}

export interface ImpositionTrace {
  press_w: number
  press_h: number
  cut_levels: CutLevel[]
  selected_cut: string
  per_full: number
  layout_cols: number
  layout_rows: number
  pieces_per_plate: number
  layout_expr: string
  reason: string
}

export interface PostProcItem {
  name: string
  unit_price: number
  unit_label: string
  qty_basis: string
  qty: number
  raw_cost: number
  min_charge: number
  cost: number
}

export interface CalcTrace {
  formula_chain: CalcStep[]
  imposition: ImpositionTrace
  post_processing_items: PostProcItem[]
}

export interface CostAddonTier {
  id: number
  category_id: number
  min_cost: number
  max_cost: number | null
  rate: number
  fixed_addon: number
  sort_order: number
}

export interface CostAddonTierInput {
  min_cost: number
  max_cost: number | null
  rate: number
  fixed_addon: number
  sort_order: number
}

export interface CostAddonTierSaveRequest {
  category_id: number
  tiers: CostAddonTierInput[]
}

export interface PostProcessingParam {
  id: number
  name: string
  code: string
  group_code: string | null
  price_type: string
  unit_price: number
  min_charge: number
  min_kai: number | null
  max_kai: number | null
  sort_order: number
  is_active: boolean
}

export interface PostProcessingParamInput {
  name: string
  code: string
  group_code: string | null
  price_type: string
  unit_price: number
  min_charge: number
  min_kai: number | null
  max_kai: number | null
  sort_order: number
  is_active: boolean
}

export interface PostProcessingParamSaveRequest {
  params: PostProcessingParamInput[]
}

export interface UnionPaperPrice {
  id: number
  weight: number
  dadu_upper_price: number
  dadu_middle_price: number
  dadu_lower_price: number
  zhengdu_upper_price: number
  zhengdu_middle_price: number
  zhengdu_lower_price: number
  is_active: boolean
}

export interface UnionPaperPriceInput {
  weight: number
  dadu_upper_price: number
  dadu_middle_price: number
  dadu_lower_price: number
  zhengdu_upper_price: number
  zhengdu_middle_price: number
  zhengdu_lower_price: number
  is_active: boolean
}

export interface UnionPaperPriceSaveRequest {
  papers: UnionPaperPriceInput[]
}
