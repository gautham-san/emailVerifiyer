
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import httpx
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")  # store the API key in env variable

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/hunter/find")
async def hunter_find(email: str):
    """
    Calls Hunter People API:
    https://api.hunter.io/v2/people/find?email=<email>&api_key=<key>
    """

    if not HUNTER_API_KEY:
        raise HTTPException(status_code=500, detail="HUNTER_API_KEY not set in environment.")

    url = "https://api.hunter.io/v2/email-verifier"

    params = {
        "email": email,
        "api_key": HUNTER_API_KEY,
    }

    async with httpx.AsyncClient(timeout=20) as client:
        try:
            response = await client.get(url, params=params)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


if __name__ == "__main__":
    # This allows you to run the script directly with 'python code.py'
    uvicorn.run(
        "code:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


# To run this API:
# uvicorn main:app --reload