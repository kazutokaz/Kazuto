from fastapi import FastAPI

from app.routes import auth as auth_routes

app = FastAPI()
app.include_router(auth_routes.router)


@app.get("/health")
def health():
    return {"ok": True}
