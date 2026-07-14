from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.huace import (
    HuaceQuoteRequest,
    HuaceQuoteResponse,
    HuacePaperResponse,
    HuaceColorResponse,
    HuaceBindingResponse,
    HuacePostProcessingResponse,
    HuaceClientTierResponse,
    HuaceSizeResponse,
)
from app.services.huace_engine import HuaceQuoteEngine
from app.models import ProductSize, ProductCategory
from app.models.huace_paper import HuacePaperPrice
from app.models.huace_color import HuaceColorPrice
from app.models.huace_binding import HuaceBinding
from app.models.huace_post_processing import HuacePostProcessing
from app.models.huace_client_tier import HuaceClientTier

router = APIRouter(prefix="/api/quote/huace", tags=["画册报价"])


@router.get("/sizes", response_model=List[HuaceSizeResponse])
def get_huace_sizes(db: Session = Depends(get_db)):
    """获取画册成品尺寸列表"""
    cat = db.query(ProductCategory).filter(ProductCategory.code == "huace").first()
    if not cat:
        return []
    sizes = db.query(ProductSize).filter(
        ProductSize.category_id == cat.id,
        ProductSize.is_active == True
    ).order_by(ProductSize.sort_order).all()
    return sizes


@router.get("/papers", response_model=List[HuacePaperResponse])
def get_huace_papers(db: Session = Depends(get_db)):
    """获取画册纸张列表"""
    papers = db.query(HuacePaperPrice).filter(
        HuacePaperPrice.is_active == True
    ).order_by(HuacePaperPrice.sort_order).all()
    return papers


@router.get("/colors", response_model=List[HuaceColorResponse])
def get_huace_colors(component: str = None, db: Session = Depends(get_db)):
    """获取画册印刷颜色列表"""
    q = db.query(HuaceColorPrice).filter(HuaceColorPrice.is_active == True)
    if component:
        q = q.filter(HuaceColorPrice.component == component)
    return q.order_by(HuaceColorPrice.component, HuaceColorPrice.sort_order).all()


@router.get("/bindings", response_model=List[HuaceBindingResponse])
def get_huace_bindings(db: Session = Depends(get_db)):
    """获取画册装订方式列表"""
    return db.query(HuaceBinding).filter(
        HuaceBinding.is_active == True
    ).order_by(HuaceBinding.sort_order).all()


@router.get("/post-processing", response_model=List[HuacePostProcessingResponse])
def get_huace_post_processing(proc_group: str = None, db: Session = Depends(get_db)):
    """获取画册后道工序列表"""
    q = db.query(HuacePostProcessing).filter(HuacePostProcessing.is_active == True)
    if proc_group:
        q = q.filter(HuacePostProcessing.proc_group == proc_group)
    return q.order_by(HuacePostProcessing.sort_order).all()


@router.get("/client-tiers", response_model=List[HuaceClientTierResponse])
def get_huace_client_tiers(db: Session = Depends(get_db)):
    """获取客户加价倍率列表"""
    return db.query(HuaceClientTier).filter(
        HuaceClientTier.is_active == True
    ).order_by(HuaceClientTier.sort_order).all()


@router.post("/calculate", response_model=HuaceQuoteResponse)
def calculate_huace_quote(
    request: HuaceQuoteRequest,
    db: Session = Depends(get_db)
):
    """计算画册报价"""
    try:
        engine = HuaceQuoteEngine(db)
        result = engine.calculate(request.model_dump())
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算画册报价失败: {str(e)}")
