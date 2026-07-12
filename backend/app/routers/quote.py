from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.quote import (
    LiandanQuoteRequest,
    LiandanQuoteResponse,
    ProductSizeResponse,
    PrintingColorResponse,
    PostProcessingResponse,
    CostAddonTierResponse,
    CostAddonTierSaveRequest,
    PostProcessingParamResponse,
    PostProcessingParamSaveRequest,
    UnionPaperPriceResponse,
    UnionPaperPriceSaveRequest,
)
from app.services.quote_engine import LiandanQuoteEngine
from app.models import ProductSize, PrintingColor, PostProcessing, QuoteRecord, CostAddonTier, UnionPaperPrice
import json

router = APIRouter(prefix="/api/quote", tags=["报价"])


@router.get("/sizes", response_model=List[ProductSizeResponse])
def get_sizes(category_id: int = 1, db: Session = Depends(get_db)):
    """获取成品尺寸列表"""
    sizes = db.query(ProductSize).filter(
        ProductSize.category_id == category_id,
        ProductSize.is_active == True
    ).order_by(ProductSize.sort_order).all()
    return sizes


@router.get("/colors", response_model=List[PrintingColorResponse])
def get_colors(db: Session = Depends(get_db)):
    """获取印刷颜色列表"""
    colors = db.query(PrintingColor).filter(
        PrintingColor.is_active == True
    ).order_by(PrintingColor.sort_order).all()
    return colors


@router.get("/post-processing", response_model=List[PostProcessingResponse])
def get_post_processing(db: Session = Depends(get_db)):
    """获取后道工序列表"""
    processing = db.query(PostProcessing).filter(
        PostProcessing.is_active == True
    ).all()
    return processing


@router.post("/liandan", response_model=LiandanQuoteResponse)
def calculate_liandan_quote(
    request: LiandanQuoteRequest,
    db: Session = Depends(get_db)
):
    """计算无碳联单报价"""
    try:
        engine = LiandanQuoteEngine(db)
        result = engine.calculate(request.model_dump())

        # 保存报价记录
        quote_record = QuoteRecord(
            category_id=1,  # 无碳联单
            customer_name=request.customer_name,
            product_name=request.product_name,
            form_data=request.model_dump(),
            cost_breakdown=result["cost_breakdown"],
            unit_price=result["unit_price"],
            total_price=result["total_price"],
            quantity=request.quantity
        )
        db.add(quote_record)
        db.commit()
        db.refresh(quote_record)

        # 注入报价ID与时间(后端真实记录，不用前端随机数)
        result["quote_id"] = f"{quote_record.id:08d}"
        result["quote_time"] = quote_record.created_at.isoformat() if quote_record.created_at else None

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算报价失败: {str(e)}")


@router.get("/cost-addon-tiers", response_model=List[CostAddonTierResponse])
def get_cost_addon_tiers(category_id: int = 1, db: Session = Depends(get_db)):
    """获取成本附加阶梯档位（按排序）"""
    tiers = db.query(CostAddonTier).filter(
        CostAddonTier.category_id == category_id,
        CostAddonTier.is_active == True
    ).order_by(CostAddonTier.sort_order).all()
    return tiers


@router.put("/cost-addon-tiers", response_model=List[CostAddonTierResponse])
def save_cost_addon_tiers(
    request: CostAddonTierSaveRequest,
    db: Session = Depends(get_db)
):
    """整表保存成本附加阶梯档位。

    编辑器语义为整表覆盖：先软删该品类现有档位，再按传入顺序重建。
    区间为半开区间 [min_cost, max_cost)，引擎按此查档
    （详见 quote_engine._calculate_cost_addon）。
    """
    try:
        # 软删该品类现有档位
        db.query(CostAddonTier).filter(
            CostAddonTier.category_id == request.category_id
        ).update({CostAddonTier.is_active: False})

        created = []
        for idx, tier in enumerate(request.tiers):
            row = CostAddonTier(
                category_id=request.category_id,
                min_cost=tier.min_cost,
                max_cost=tier.max_cost,
                rate=tier.rate,
                fixed_addon=tier.fixed_addon,
                sort_order=tier.sort_order if tier.sort_order else idx + 1,
                is_active=True,
            )
            db.add(row)
            created.append(row)

        db.commit()
        for row in created:
            db.refresh(row)
        return created
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"保存成本附加阶梯失败: {str(e)}")


@router.get("/post-processing-params", response_model=List[PostProcessingParamResponse])
def get_post_processing_params(db: Session = Depends(get_db)):
    """获取后工参数全表（含禁用行，供参数页编辑），按 sort_order 排序。"""
    rows = db.query(PostProcessing).order_by(PostProcessing.sort_order).all()
    return rows


@router.put("/post-processing-params", response_model=List[PostProcessingParamResponse])
def save_post_processing_params(
    request: PostProcessingParamSaveRequest,
    db: Session = Depends(get_db)
):
    """整表保存后工参数。

    编辑器语义为整表覆盖。注意 post_processing.code 有 UNIQUE 约束，不能用软删
    （软删后重插同 code 会撞唯一键），因此采用硬删 + 重插（同事务）。
    引擎按 group_code + 成品开数(kai) 选档，见 quote_engine._resolve_processing。
    """
    try:
        db.query(PostProcessing).delete()
        created = []
        for idx, item in enumerate(request.params):
            row = PostProcessing(
                name=item.name,
                code=item.code,
                group_code=item.group_code,
                price_type=item.price_type,
                unit_price=item.unit_price,
                min_charge=item.min_charge,
                min_kai=item.min_kai,
                max_kai=item.max_kai,
                sort_order=item.sort_order if item.sort_order else idx + 1,
                is_active=item.is_active,
            )
            db.add(row)
            created.append(row)
        db.commit()
        for row in created:
            db.refresh(row)
        return created
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"保存后工参数失败: {str(e)}")


@router.get("/union-paper-prices", response_model=List[UnionPaperPriceResponse])
def get_union_paper_prices(db: Session = Depends(get_db)):
    """获取联单纸张分层价格全表"""
    rows = db.query(UnionPaperPrice).order_by(UnionPaperPrice.weight).all()
    return rows


@router.put("/union-paper-prices", response_model=List[UnionPaperPriceResponse])
def save_union_paper_prices(
    request: UnionPaperPriceSaveRequest,
    db: Session = Depends(get_db)
):
    """整表保存联单纸张分层价格。按 weight 做 upsert。"""
    try:
        incoming_weights = {p.weight for p in request.papers}
        db.query(UnionPaperPrice).filter(
            ~UnionPaperPrice.weight.in_(incoming_weights)
        ).delete(synchronize_session=False)

        saved = []
        for item in request.papers:
            existing = db.query(UnionPaperPrice).filter(
                UnionPaperPrice.weight == item.weight
            ).first()
            if existing:
                existing.dadu_upper_price = item.dadu_upper_price
                existing.dadu_middle_price = item.dadu_middle_price
                existing.dadu_lower_price = item.dadu_lower_price
                existing.zhengdu_upper_price = item.zhengdu_upper_price
                existing.zhengdu_middle_price = item.zhengdu_middle_price
                existing.zhengdu_lower_price = item.zhengdu_lower_price
                existing.is_active = item.is_active
                saved.append(existing)
            else:
                row = UnionPaperPrice(
                    weight=item.weight,
                    dadu_upper_price=item.dadu_upper_price,
                    dadu_middle_price=item.dadu_middle_price,
                    dadu_lower_price=item.dadu_lower_price,
                    zhengdu_upper_price=item.zhengdu_upper_price,
                    zhengdu_middle_price=item.zhengdu_middle_price,
                    zhengdu_lower_price=item.zhengdu_lower_price,
                    is_active=item.is_active,
                )
                db.add(row)
                saved.append(row)
        db.commit()
        for row in saved:
            db.refresh(row)
        return saved
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"保存联单纸价失败: {str(e)}")


@router.get("/history")
def get_quote_history(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """获取报价历史记录"""
    records = db.query(QuoteRecord).order_by(
        QuoteRecord.created_at.desc()
    ).offset(offset).limit(limit).all()

    return {
        "total": db.query(QuoteRecord).count(),
        "records": [
            {
                "id": r.id,
                "quote_no": r.quote_no,
                "customer_name": r.customer_name,
                "product_name": r.product_name,
                "quantity": r.quantity,
                "total_price": float(r.total_price) if r.total_price else 0,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in records
        ]
    }
