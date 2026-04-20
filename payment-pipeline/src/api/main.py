from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import predict, statistics
from src.database import init_db

app = FastAPI(title="Payment Pipeline API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router, prefix="", tags=["predict"])
app.include_router(statistics.router, prefix="", tags=["statistics"])

@app.on_event("startup")
def startup():
    init_db()
    print("Database initialized")

@app.get("/")
def root():
    return {"status": "running", "message": "Payment Pipeline API"}
