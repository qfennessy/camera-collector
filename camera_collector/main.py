import uvicorn
from fastapi import FastAPI


app = FastAPI(
    title="Vintage Camera Collection API",
    description="API for managing a collection of vintage cameras",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Vintage Camera Collection API"}


if __name__ == "__main__":
    uvicorn.run("camera_collector.main:app", host="0.0.0.0", port=8000, reload=True)