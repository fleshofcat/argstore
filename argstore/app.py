from fastapi import FastAPI
from starlette.responses import RedirectResponse

from argstore.parameters.api import router as parameters_router
from argstore.users.api import router as users_router

app = FastAPI()

app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(parameters_router, prefix="/api/parameters", tags=["parameters"])


@app.get("/")
def redirect_to_docs_from_root():
    return RedirectResponse(url="/docs")
