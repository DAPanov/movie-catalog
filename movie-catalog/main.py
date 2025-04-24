from fastapi import FastAPI, Request

app = FastAPI(
    title="Movie catalog",
)

@app.get("/")
async def root(request: Request,):
    docs_url = request.url.replace(path="/docs")
    return {"message": "Hello World",
            "docs": str(docs_url),}