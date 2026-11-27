from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.schemas import LeadCreate, LeadOut, PlanOut

router = APIRouter(prefix="/api/v1", tags=["public"])


@router.get("/public/plans", response_model=list[PlanOut])
def list_public_plans(db: Session = Depends(get_db)) -> list[models.MembershipPlan]:
    statement = (
        select(models.MembershipPlan)
        .where(models.MembershipPlan.is_active.is_(True))
        .order_by(models.MembershipPlan.display_order, models.MembershipPlan.id)
    )
    return list(db.scalars(statement).all())


@router.post("/leads", response_model=LeadOut, status_code=status.HTTP_201_CREATED)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db)) -> models.Lead:
    lead = models.Lead(**payload.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
