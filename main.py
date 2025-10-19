from fastapi import FastAPI
from routers import orders, work_results

app = FastAPI(title="MES Copilot Demo")

app.include_router(orders.router)
app.include_router(work_results.router)

@app.get("/")
def read_root():
    return {"message": "MES Copilot API is running"}