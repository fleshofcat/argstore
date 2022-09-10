from fastapi import FastAPI
from starlette.responses import RedirectResponse

from argstore.database import Base, engine
from argstore.parameters.router import router

# TODO Remove it
Base.metadata.create_all(bind=engine)  # type: ignore


app = FastAPI()

app.include_router(router, prefix="/parameters", tags=["parameters"])


@app.get("/")
def redirect_to_docs_from_root():
    return RedirectResponse(url="/docs")
