from fastapi import APIRouter


manage_user_router = APIRouter(prefix='/me',
                   tags=['Manage User'],
                   )

