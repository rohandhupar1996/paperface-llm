import uvicorn
from fastapi import FastAPI

from src.controller import routes
# from src.exception.exception_handler import add_exception_handler

app = FastAPI(debug=False)
# add_exception_handler(app)

app.include_router(routes.router, tags=["OG-OCR-LLM"], responses={404: {"description": "Not found"}})
@app.get("/health")
def read_root():
    return {"status_code": 200,
            "status_message": "The service is up"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",port=9001)
