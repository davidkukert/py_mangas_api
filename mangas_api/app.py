from fastapi import FastAPI

from mangas_api.routers import users

app = FastAPI(
    title='Mangas API',
    description='API para gerenciamento de HQs, ex: Mangas, Manhua, Manhwa.',
    version='0.1.0',
)


@app.get('/')
def index_root():
    return {'message': 'Manga API esta rodando!'}


app.include_router(users.router)
