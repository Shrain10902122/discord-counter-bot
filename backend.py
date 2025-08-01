import threading
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.head("/")
def read_root():
    return {"status": "bot is running"}

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_api).start()

@app.get("/")
def read_root():
    return {"status": "bot is running"}

def run_api():
    uvicorn.run(app, host="0.0.0.0", port=10000)

if __name__ == "__main__":
    threading.Thread(target=run_api).start()