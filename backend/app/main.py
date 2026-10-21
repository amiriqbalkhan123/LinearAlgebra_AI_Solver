
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.systems import router as systems_router
from app.api.v1.solve import router as solver_router
from app.api.v1.eigenanalysis import router as eigenanalysis_router
from app.api.v1.vector_spaces import router as vector_spaces_router
from app.api.v1.decompositions import router as decomposition_router
from app.api.v1.vector_geometry import router as vector_geometry_router
app = FastAPI(
    title="LinearAI API",
    version="1.0.0",
    description="Intelligent Linear Algebra Solver",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(solver_router, prefix="/api/v1")
app.include_router(
    systems_router,
    prefix="/api/v1",
)
app.include_router(
    vector_spaces_router,
    prefix="/api/v1",
)
app.include_router(
    vector_geometry_router,
    prefix="/api/v1",
)
app.include_router(
    eigenanalysis_router,
    prefix="/api/v1",
)

app.include_router(
    decomposition_router,
    prefix="/api/v1",
)
@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "application": "LinearAI",
        "version": "1.0.0",
    }
