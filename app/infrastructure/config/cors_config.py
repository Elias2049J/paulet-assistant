from fastapi.middleware.cors import CORSMiddleware


def configure_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://paulet-assistant.pages.dev"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
