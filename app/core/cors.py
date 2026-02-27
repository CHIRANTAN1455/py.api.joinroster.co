from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def configure_cors(app: FastAPI) -> None:
    """
    Configure CORS to be completely open, matching the requirement:
    - allow_origins = "*"
    - allow_methods = "*"
    - allow_headers = "*"
    - expose_headers = "*"
    - allow_credentials = True
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

