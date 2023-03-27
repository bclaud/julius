from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

    
def main ():
    uvicorn.run(app=app, port=8000)

if __name__ == "__main__":
    main()