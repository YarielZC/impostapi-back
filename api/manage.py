from fastapi import APIRouter
from api.manage_routes.endpoint_manage import manage_endpoint_router
from api.manage_routes.project_manage import manage_project_router
from api.manage_routes.user_manage import manage_user_router

manage_router = APIRouter(prefix='/dashboard',
                   tags=['Manage'],
                   )

manage_router.include_router(manage_endpoint_router)
manage_router.include_router(manage_project_router)
manage_router.include_router(manage_user_router)