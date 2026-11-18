from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, ConfigDict, Field, StringConstraints


app = FastAPI(title="Price Quote API")
PRODUCTS = {"notebook": 450, "pen": 175}


class QuoteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    unit_cents: Annotated[int, Field(strict=True, gt=0, le=100_000)]
    quantity: Annotated[int, Field(strict=True, ge=1, le=100)]
    label: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=60)]


class Quote(BaseModel):
    label: str
    total_cents: int


@app.get("/products")
def products(max_cents: Annotated[int, Query(ge=0)] = 1000):
    return {name: cents for name, cents in PRODUCTS.items() if cents <= max_cents}


@app.get("/shipping/{quantity}")
def shipping(quantity: Annotated[int, Path(ge=1, le=100)]):
    return {"shipping_cents": 250 + 50 * quantity}


@app.post("/quotes", response_model=Quote)
def quote(request: QuoteRequest):
    return Quote(label=request.label, total_cents=request.unit_cents * request.quantity)
