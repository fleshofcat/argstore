from fastapi import FastAPI
from starlette.responses import RedirectResponse

from argstore.parameters.api import json_api_router
from argstore.parameters.api import router as parameters_router
from argstore.users.api import router as users_router

app = FastAPI()

app.include_router(users_router, prefix="/users_api/users", tags=["users"])
app.include_router(parameters_router, prefix="/api/parameters", tags=["parameters"])
app.include_router(json_api_router, prefix="/api", tags=["json api"])


@app.get("/")
def redirect_to_docs_from_root():
    return RedirectResponse(url="/docs")
