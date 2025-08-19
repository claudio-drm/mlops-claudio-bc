# Claudio BC API

## 1) Entrenamiento
```powershell
py .\train_bc.py
```

## 2) Ejecución local
```powershell
.\scripts\run_local.ps1
```

## 3) Docker
```powershell
docker build -t claudio-bc-api:latest .
docker run -p 8080:8080 claudio-bc-api:latest
```

## 4) Despliegue Fly.io
```powershell
flyctl auth login
.\scripts\deploy_fly.ps1 -AppName "claudio-bc-api"
```

## 5) CI/CD GitHub Actions
```powershell
git init
git add --all
git commit -m "Claudio BC API"
git branch -M main
git remote add origin https://github.com/tu_usuario/tu_repo.git
git push -u origin main
```

## Enlaces
- API (salud): https://claudio-bc-api-01.fly.dev/health
- Documentación (Swagger): https://claudio-bc-api-01.fly.dev/docs
- Esquema de features: https://claudio-bc-api-01.fly.dev/schema
- Repositorio: https://github.com/claudio-drm/mlops-claudio-bc

