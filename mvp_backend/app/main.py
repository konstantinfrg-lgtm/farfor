from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.db.models import Base
from app.db.session import engine
from app.routes.auth import router as auth_router
from app.routes.items import router as items_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
app.mount('/media', StaticFiles(directory='media'), name='media')

app.include_router(auth_router, prefix='/api')
app.include_router(items_router, prefix='/api')


@app.get('/health')
def healthcheck():
    return {'status': 'ok'}
