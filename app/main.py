from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from pathlib import Path
import json, pickle, pandas as pd

ART = Path("artifacts")

class ClaudioBCInput(BaseModel):
    features: Dict[str, Any]

app = FastAPI(title="Claudio BC API", version="1.0.0")

_model = None
_scaler = None
_order = None

def load_artifacts():
    global _model, _scaler, _order
    if _model is None:
        with open(ART / "claudio_bc_model.pkl", "rb") as f:
            _model = pickle.load(f)
    if _scaler is None:
        with open(ART / "claudio_bc_scaler.pkl", "rb") as f:
            _scaler = pickle.load(f)
    if _order is None:
        _order = json.loads((ART / "claudio_bc_feature_order.json").read_text())
    return _model, _scaler, _order

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/schema")
def schema():
    _, _, order = load_artifacts()
    return {"feature_order": order}

@app.post("/predict")
def predict(inp: ClaudioBCInput):
    try:
        model, scaler, order = load_artifacts()
        missing = [c for c in order if c not in inp.features]
        if missing:
            raise HTTPException(status_code=400, detail=f"missing: {missing}")
        df = pd.DataFrame([{c: inp.features[c] for c in order}])
        Xs = scaler.transform(df)
        y = model.predict(Xs)[0]
        proba = float(model.predict_proba(Xs)[0,1]) if hasattr(model, "predict_proba") else None
        return {"prediction": int(y), "proba_1": proba}
    except HTTPException:
        raise
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"error: {e}")
