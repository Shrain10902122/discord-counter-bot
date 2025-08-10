import threading
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
@app.head("/")
def read_root():
    return {"status": "bot is running"}

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=10000)