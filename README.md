# Sample FastAPI App

This minimal project demonstrates a FastAPI app with one GET and one POST endpoint.

## Run Instructions (PowerShell)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run with uvicorn:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /hello` — returns `{ "message": "Hello, world!" }`
- `POST /items/` — accepts JSON `{ "name": str, "description"?: str, "price": float }`

Open the interactive docs at `http://127.0.0.1:8000/docs`.
