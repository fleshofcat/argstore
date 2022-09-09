from fastapi import FastAPI
from starlette.responses import RedirectResponse

from argstore.parameters.router import router

from .database import engine
from .parameters import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router, prefix="/parameters", tags=["parameters"])


@app.get("/")
def redirect_to_docs_from_root():
    return RedirectResponse(url="/docs")
