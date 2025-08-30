from fastapi import FastAPI

app = FastAPI(title="Minimal Test API")

@app.get("/test")
def test():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
