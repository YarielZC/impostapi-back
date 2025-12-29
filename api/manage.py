from fastapi import APIRouter
from api.manage_routes.endpoint_manage import manage_endpoint_router
manage_router = APIRouter(prefix='/dashboard',
                   tags=['Manage'],
                   )

manage_router.include_router(manage_endpoint_router)