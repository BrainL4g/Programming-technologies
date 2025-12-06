from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, distinct
from datetime import datetime, timedelta

from src.api.dependecies.database import get_db_session
from src.db.models import Offer, PriceHistory, Store

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/price-changes/")
async def price_changes_report(
    days: int = 7,
    db: AsyncSession = Depends(get_db_session)
):
    since = datetime.utcnow() - timedelta(days=days)
    stmt = select(
        Offer.id,
        Offer.product_name,
        Offer.price,
        func.min(PriceHistory.price).label("min_price"),
        func.max(PriceHistory.price).label("max_price")
    ).join(PriceHistory).where(PriceHistory.recorded_at >= since).group_by(Offer.id)
    result = await db.execute(stmt)
    return result.all()


@router.get("/availability/")
async def availability_report(db: AsyncSession = Depends(get_db_session)):
    total = await db.scalar(select(func.count(Offer.id)))
    available = await db.scalar(select(func.count(Offer.id)).where(Offer.available == True))
    return {"total": total, "available": available, "unavailable": total - available}


@router.get("/sync-status/")
async def sync_status(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(
        select(Store.id, Store.name, Store.last_sync)
        .order_by(Store.last_sync.desc().nulls_last())
    )
    return result.all()