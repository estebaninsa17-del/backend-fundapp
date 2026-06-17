from fastapi import APIRouter

from app.api.v1 import actividades, admin, auth, certificados, donaciones, voluntarios

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(actividades.router)
router.include_router(donaciones.router)
router.include_router(voluntarios.router)
router.include_router(certificados.router)
router.include_router(admin.router)


