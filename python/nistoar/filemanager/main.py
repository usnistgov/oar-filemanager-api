from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Service": "NextCloud File Manager API", "Status": "Running"}
