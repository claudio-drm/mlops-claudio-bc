param([string] = "claudio-bc-api-01")

# Edita fly.toml de forma robusta
 = Get-Content fly.toml -Raw
 =  -replace 'app = ".*"', "app = """
 =  -replace 'primary_region = "scl"', 'primary_region = "gru"'
 | Set-Content fly.toml

flyctl apps create 
flyctl deploy --remote-only

Write-Host ("https://{0}.fly.dev/health" -f )
Write-Host ("https://{0}.fly.dev/docs"   -f )
