from fastapi import FastAPI
from starlette.responses import RedirectResponse

from . import models
from .database import engine
from .router import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, tags=["parameters"])


@app.get("/")
def redirect_to_docs_from_root():
    return RedirectResponse(url="/docs")
