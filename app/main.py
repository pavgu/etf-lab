from fastapi import FastAPI

app = FastAPI(title="ETF Lab")

@app.get("/health")
def health():
    return {"status": "ok"}
