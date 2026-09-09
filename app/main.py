from fastapi import FastAPI

app = FastAPI(title="Financial Transaction Analytics API")


@app.get("/")
def read_root():
    return {"status": "ok", "message": "Financial Transaction Analytics API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}