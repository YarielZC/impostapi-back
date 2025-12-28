from fastapi import APIRouter

manage_router = APIRouter(prefix='/dashboard',
                   tags=['Manage'],
                   )