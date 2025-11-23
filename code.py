
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import httpx
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")  # store the API key in env variable

VERIFALIA_USERNAME = os.getenv("VERIFALIA_USERNAME")
VERIFALIA_PASSWORD = os.getenv("VERIFALIA_PASSWORD")

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



@app.post("/verifalia/validate")
async def verifalia_validate(email: str):
    """
    Calls Verifalia Email Validation API via:
    curl -u username:password \
        --compressed \
        -H "Content-Type: application/json" \
        -d '{ "entries": [ { "inputData": "batman@gmail.com" } ] }' \
        https://api.verifalia.com/v2.7/email-validations
    """

    if not VERIFALIA_USERNAME or not VERIFALIA_PASSWORD:
        raise HTTPException(status_code=500, detail="VERIFALIA_USERNAME or VERIFALIA_PASSWORD not set.")

    url = "https://api.verifalia.com/v2.7/email-validations"

    payload = {
        "entries": [
            {"inputData": email}
        ]
    }

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            response = await client.post(
                url,
                json=payload,
                auth=(VERIFALIA_USERNAME, VERIFALIA_PASSWORD),
                headers={"Content-Type": "application/json", "Accept-Encoding": "gzip"}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    if response.status_code not in (200, 202):
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