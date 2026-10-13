from fastapi import FastAPI, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app import models  # noqa: F401
from app.database import Base
from app.auth.router import router as auth_router
from app.routes.admin import router as admin_router
from app.routes.students import router as students_router
from app.routes.teachers import router as teachers_router

limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])

app = FastAPI(title="Електронний деканат")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

app.include_router(auth_router)
app.include_router(students_router)
app.include_router(teachers_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"message": "Electronic Dean's Office API"}

@app.get("/health")
@limiter.limit("10/minute")
def health(request: Request):
    return {
        "status": "healthy",
        "database": "SQLite",
        "tables": len(Base.metadata.tables),
    }