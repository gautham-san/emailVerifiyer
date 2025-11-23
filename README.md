# FastAPI Email Verification Service (Hunter API and Verafalia API)

This small FastAPI app exposes an endpoint to verify any email address using  
**Hunter's Email Verifier API** (`/v2/email-verifier`) and **Verafalia's Email Verifier API** (`/v2.7/email-validations`)

It also redirects `/` → `/docs` for an easy Swagger UI.

---

## Requirements

- Python 3.10+
- A Hunter.io API key
- FastAPI
- Uvicorn
- httpx
- python-dotenv

---

## Installation

```bash
pip install fastapi uvicorn httpx python-dotenv
```

## Environment Variables
```bash
HUNTER_API_KEY=your_api_key_here
VERIFALIA_USERNAME=..
VERIFALIA_PASSWORD=..
```

And finally

```bash
python code.py
```


