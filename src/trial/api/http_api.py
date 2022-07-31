from fastapi import APIRouter, Depends
from trial.application import Quote, QuoteRepo
from trial.application.foundation import Pair
from trial.wiring import init_db

router = APIRouter()


@router.get("/", response_model=Quote)
async def get(pair: Pair = Pair("USDTRUB"), quote_repo: QuoteRepo = Depends(init_db)):
    return await quote_repo.get_last_quote(pair)
