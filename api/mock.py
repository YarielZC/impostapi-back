from fastapi import APIRouter

mock_router = APIRouter(prefix='/mock',
                   tags=['Mocks'],
                   )