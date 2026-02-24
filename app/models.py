from typing import List, Literal, Optional
from pydantic import BaseModel, Field, EmailStr, PositiveInt, PositiveFloat, conint

class ClientInfo(BaseModel):
    name: str
    contact: EmailStr
    lang: Literal["en", "ar"] = "en"          # English (en) or Arabic (ar)

class Item(BaseModel):
    sku: str
    qty: PositiveInt = Field(..., description="Quantity of the item")
    unit_cost: PositiveFloat = Field(..., description="Cost per unit in the chosen currency")
    margin_pct: PositiveFloat = Field(..., ge=0, le=100, description="Margin percent (e.g. 22 for 22%)")

class QuoteRequest(BaseModel):
    client: ClientInfo
    currency: str = Field(..., min_length=1, max_length=3)
    items: List[Item] = Field(..., min_items=1)
    delivery_terms: str
    notes: Optional[str] = None

class LineItemResponse(BaseModel):
    sku: str
    qty: int
    unit_cost: float
    margin_pct: float
    line_total: float

class QuoteResponse(BaseModel):
    line_items: List[LineItemResponse]
    grand_total: float
    email_draft: str