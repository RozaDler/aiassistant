from fastapi import FastAPI

# Test if fastapi is running
app = FastAPI()

@app.get("/")
async def root():
    return{"message": "Hi Boybous"}