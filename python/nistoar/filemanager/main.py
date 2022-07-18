from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Service": "NextCloud File Manager API", "Status": "Running"}


def main():
    import uvicorn

    uvicorn.run("nistoar.filemanager.main:app", host="0.0.0.0", port=8085, reload=True, debug=True)


if __name__ == "__main__":
    main()
