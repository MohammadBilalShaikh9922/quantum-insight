
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.core.config import settings

from app.api.routes_analysis import router as analysis_router
from app.api.routes_health import router as health_router
from app.api.routes_optimizer import router as optimizer_router
from app.api.routes_debugger import router as debugger_router
from app.api.routes_reports import router as reports_router
from app.api.routes_auth import router as auth_router
from app.api.routes_history import router as history_router

# Temporary simulator testing route
from app.api.routes_simulation_test import (
    router as simulation_test_router,
)


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS CONFIGURATION
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# EXISTING API ROUTES
# ---------------------------------------------------------

app.include_router(analysis_router, prefix="/api")
app.include_router(health_router, prefix="/api")
app.include_router(optimizer_router, prefix="/api")
app.include_router(debugger_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(history_router, prefix="/api")

# Temporary simulator testing route
app.include_router(
    simulation_test_router,
    prefix="/api",
)


# ---------------------------------------------------------
# CUSTOM OPENAPI CONFIGURATION
# ---------------------------------------------------------

def custom_openapi():

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.app_name,
        version="1.0.0",
        description="QuantumInsight API",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    app.openapi_schema = openapi_schema

    return app.openapi_schema


app.openapi = custom_openapi


# ---------------------------------------------------------
# ROOT ENDPOINT
# ---------------------------------------------------------

@app.get("/")
def root():

    return {
        "name": settings.app_name,
        "status": "ok",
    }


# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/api/healthcheck")
def healthcheck():

    return {
        "status": "healthy",
    }


@app.head("/api/healthcheck")
def healthcheck_head():

    return Response(
        status_code=200
    )
