from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from .api import tasks, analytics

# Создаем таблицы в БД
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Todo API",
    description="Умный менеджер задач с аналитикой",
    version="0.1.0",
)

# Настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

@app.get("/")
async def root():
    return {"message": "Smart Todo API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)