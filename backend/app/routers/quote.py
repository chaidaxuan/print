from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.quote import (
    LiandanQuoteRequest,
    LiandanQuoteResponse,
    ProductSizeResponse,
    PrintingColorResponse,
    PostProcessingResponse
)
from app.services.quote_engine import LiandanQuoteEngine
from app.models import ProductSize, PrintingColor, PostProcessing, QuoteRecord
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

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算报价失败: {str(e)}")


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
