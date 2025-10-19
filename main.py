from fastapi import FastAPI
from database import engine, Base
from routers import orders, work_results

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MES Copilot Demo")

app.include_router(orders.router)
app.include_router(work_results.router)

@app.get("/")
def read_root():
    return {"message": "MES Copilot API is running"}