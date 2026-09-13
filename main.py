from fastapi import FastAPI

import models, database
from routers import task, user, auth

# Create FastAPI application
app = FastAPI()


# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Register API routers
app.include_router(task.router)
app.include_router(user.router)
app.include_router(auth.router)
    
    
