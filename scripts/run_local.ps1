\
    if (-Not (Test-Path .\.venv)) { py -m venv .venv }
    .\.venv\Scripts\Activate.ps1
    py -m pip install --upgrade pip
    py -m pip install -r requirements.txt
    uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
