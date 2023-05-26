from fastapi import FastAPI
from controllers import book_controller, user_controller
import uvicorn


app = FastAPI()

app.include_router(book_controller.router, prefix="/api", tags=["book"])
app.include_router(user_controller.router, prefix="/users", tags=["users"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
