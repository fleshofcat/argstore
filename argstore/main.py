from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI()


@app.get("/")
def redirect_to_docs_from_root():
    return RedirectResponse(url="/docs")
