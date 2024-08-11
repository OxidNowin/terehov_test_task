from pydantic import BaseModel


class CurrencyRate(BaseModel):
    Id: str
    NumCode: str
    CharCode: str
    Nominal: str
    Name: str
    Value: str
    VunitRate: str
