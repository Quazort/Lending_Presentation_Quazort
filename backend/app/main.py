from fastapi import FastAPI

from backend.app.endpoints.general import general_router

main_app = FastAPI(title="Quazort_Lending")


main_app.include_router(general_router)
