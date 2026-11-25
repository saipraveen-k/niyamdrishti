from fastapi import APIRouter, Depends
from app.core.security import AuthUser, get_current_user

router = APIRouter()

@router.get("/notifications/me")
async def get_my_notifications(current_user: AuthUser = Depends(get_current_user)):
    # Placeholder — full notification system in Phase 8
    return {"notifications": [], "unread_count": 0}
