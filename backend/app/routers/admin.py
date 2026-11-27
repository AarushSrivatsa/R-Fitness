from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.schemas import LeadOut, LeadStatusUpdate, PlanCreate, PlanOut, PlanUpdate
from app.security import require_admin

router = APIRouter(prefix="/api/v1/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@router.get("/overview")
def get_overview(db: Session = Depends(get_db)) -> dict[str, int]:
    return {
        "total_leads": db.scalar(select(func.count()).select_from(models.Lead)) or 0,
        "new_leads": db.scalar(
            select(func.count()).select_from(models.Lead).where(models.Lead.status == "new")
        ) or 0,
        "active_plans": db.scalar(
            select(func.count()).select_from(models.MembershipPlan).where(models.MembershipPlan.is_active.is_(True))
        ) or 0,
    }


@router.get("/leads", response_model=list[LeadOut])
def list_leads(db: Session = Depends(get_db)) -> list[models.Lead]:
    statement = select(models.Lead).order_by(models.Lead.created_at.desc()).limit(500)
    return list(db.scalars(statement).all())


@router.patch("/leads/{lead_id}", response_model=LeadOut)
def update_lead_status(
    lead_id: int,
    payload: LeadStatusUpdate,
    db: Session = Depends(get_db),
) -> models.Lead:
    lead = db.get(models.Lead, lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Enquiry not found.")
    lead.status = payload.status
    db.commit()
    db.refresh(lead)
    return lead


@router.get("/plans", response_model=list[PlanOut])
def list_all_plans(db: Session = Depends(get_db)) -> list[models.MembershipPlan]:
    statement = select(models.MembershipPlan).order_by(models.MembershipPlan.display_order, models.MembershipPlan.id)
    return list(db.scalars(statement).all())


@router.post("/plans", response_model=PlanOut, status_code=status.HTTP_201_CREATED)
def create_plan(payload: PlanCreate, db: Session = Depends(get_db)) -> models.MembershipPlan:
    plan = models.MembershipPlan(**payload.model_dump())
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.patch("/plans/{plan_id}", response_model=PlanOut)
def update_plan(plan_id: int, payload: PlanUpdate, db: Session = Depends(get_db)) -> models.MembershipPlan:
    plan = db.get(models.MembershipPlan, plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Membership plan not found.")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(plan, key, value)
    db.commit()
    db.refresh(plan)
    return plan


@router.delete("/plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(plan_id: int, db: Session = Depends(get_db)) -> None:
    plan = db.get(models.MembershipPlan, plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Membership plan not found.")
    db.delete(plan)
    db.commit()
