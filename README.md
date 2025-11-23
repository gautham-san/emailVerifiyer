# FastAPI Email Verification Service (Hunter API)

This small FastAPI app exposes an endpoint to verify any email address using  
**Hunter's Email Verifier API** (`/v2/email-verifier`).

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
```

And finally

```bash
python code.py
```


