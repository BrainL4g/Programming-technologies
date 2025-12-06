from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from src.api.dependecies.database import get_db_session
from src.db.models import Store, Offer, PriceHistory
from sqlalchemy import select, func

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/price-changes/")
async def price_changes_report(
    days: int = Query(7, ge=1, le=90),
    db: AsyncSession = Depends(get_db_session),
):
    since = datetime.utcnow() - timedelta(days=days)
    stmt = (
        select(
            Offer.id,
            Offer.product_name,
            Offer.price.label("current_price"),
            func.min(PriceHistory.price).label("min_price"),
            func.max(PriceHistory.price).label("max_price"),
            func.count(PriceHistory.id).label("changes_count"),
        )
        .join(PriceHistory)
        .where(PriceHistory.recorded_at >= since)
        .group_by(Offer.id, Offer.product_name, Offer.price)
        .having(func.min(PriceHistory.price) != func.max(PriceHistory.price))
        .order_by(func.count(PriceHistory.id).desc())
    )
    result = await db.execute(stmt)
    return result.all()


@router.get("/availability/")
async def availability_report(db: AsyncSession = Depends(get_db_session)):
    total = await db.scalar(select(func.count(Offer.id)))
    available = await db.scalar(select(func.count(Offer.id)).where(Offer.available == True))
    return {
        "total": total or 0,
        "available": available or 0,
        "unavailable": (total or 0) - (available or 0),
    }


@router.get("/sync-status/")
async def sync_status(db: AsyncSession = Depends(get_db_session)):
    result = await db.execute(
        select(
            Store.id,
            Store.name,
            Store.is_active,
            Store.last_sync,
        ).order_by(Store.last_sync.desc().nulls_last())
    )
    return [
        {
            "id": row.id,
            "name": row.name,
            "is_active": row.is_active,
            "last_sync": row.last_sync,
        }
        for row in result.all()
    ]