
from app.schemas.matrix import MatrixRequest
from app.schemas.linear_system import LinearSystemRequest
from app.schemas.vector_space import VectorSpaceRequest
from app.schemas.vector_geometry import VectorGeometryRequest
from app.schemas.eigenanalysis import EigenanalysisRequest
from app.schemas.decomposition import DecompositionRequest

from app.services.solver_service import solve_matrix
from app.services.linear_system_service import solve_system
from app.services.vector_space_service import solve_space
from app.services.vector_geometry_service import solve_geometry
from app.services.eigenanalysis_service import solve_eigenanalysis
from app.services.decomposition_service import solve_decomposition


SOLVER_REGISTRY = {
    "matrices": (
        MatrixRequest,
        solve_matrix,
    ),
    "linear_systems": (
        LinearSystemRequest,
        solve_system,
    ),
    "vector_spaces": (
        VectorSpaceRequest,
        solve_space,
    ),
    "vector_geometry": (
        VectorGeometryRequest,
        solve_geometry,
    ),
    "eigenanalysis": (
        EigenanalysisRequest,
        solve_eigenanalysis,
    ),
    "decompositions": (
        DecompositionRequest,
        solve_decomposition,
    ),
}
