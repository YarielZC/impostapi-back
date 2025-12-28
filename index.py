from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='ImpostAPI', 
              description=' A high-performance, asynchronous Mock API generator built with FastAPI and MongoDB. It allows developers to design and deploy custom JSON endpoints in seconds, featuring dynamic routing, configurable HTTP status codes, and simulated network latency to streamline frontend development and testing. ',
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get('/', response_model=dict, status_code=status.HTTP_200_OK)
async def health():
  return {'message': 'server running'}