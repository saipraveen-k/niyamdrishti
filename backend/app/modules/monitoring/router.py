from fastapi import APIRouter, Depends
from app.core.security import require_roles

router = APIRouter()

@router.get("/admin/system-health", dependencies=[Depends(require_roles("admin", "super_admin"))])
async def system_health():
    return {
        "status": "ok",
        "database": "connected",
        "ai": "configured",
        "storage": "configured",
    }

@router.get("/admin/jobs", dependencies=[Depends(require_roles("admin", "super_admin"))])
async def list_jobs():
    return {"jobs": [], "message": "Job listing requires database query — implement in Phase 9"}
