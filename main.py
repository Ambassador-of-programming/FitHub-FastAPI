from fastapi import FastAPI
from routes.auth import auth_router
from routes.account_user import user_router
from routes.account_trainer import trainer_router
from routes.account_admin import admin_router
import uvicorn

app = FastAPI(debug=False)

# Register routes
app.include_router(auth_router,  prefix="/auth")
app.include_router(user_router, prefix="/user")
app.include_router(trainer_router, prefix="/trainer")
app.include_router(admin_router, prefix="/admin")

# if __name__ == "__main__":
#     uvicorn.run("main:app", port=8000, reload=True)
#     docker run -d --name mycontainer -p 80:80 myimage