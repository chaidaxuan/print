from app.models.category import ProductCategory
from app.models.size import ProductSize
from app.models.machine import PrintingMachine
from app.models.paper import PaperSpec
from app.models.processing import PostProcessing
from app.models.color import PrintingColor
from app.models.param import SystemParam
from app.models.quote import QuoteRecord

__all__ = [
    "ProductCategory",
    "ProductSize",
    "PrintingMachine",
    "PaperSpec",
    "PostProcessing",
    "PrintingColor",
    "SystemParam",
    "QuoteRecord",
]
