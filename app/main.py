import uvicorn
from fastapi import FastAPI
from app.routers import organization, building, activity

app = FastAPI()
app.include_router(activity.router)
app.include_router(building.router)
app.include_router(organization.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True)
