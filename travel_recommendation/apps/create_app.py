from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app():
    app = FastAPI(docs_url="/")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
        expose_headers=['*',]
    )
    return app
