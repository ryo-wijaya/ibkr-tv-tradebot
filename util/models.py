from pydantic import BaseModel


class TradeRequest(BaseModel):
    key: str
    symbol: str
    quantity: int


class FetchPortfolioRequest(BaseModel):
    key: str
