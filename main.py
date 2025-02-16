from fastapi import FastAPI
import models
from database import engine
import empresa_controller, obrigacao_acessoria_controller

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Incluindo as rotas
app.include_router(empresa_controller.router)
app.include_router(obrigacao_acessoria_controller.router)
