import uvicorn
import os
from apps.create_app import create_app
from apps import router

app = create_app()
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, port=os.environ.get("PORT", 7860))
