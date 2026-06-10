# Lab 3.3 (Claude-native) - REAL local CI pipeline.
#
# The same job a CI pipeline runs, but on your machine using the ANTHROPIC_API_KEY
# from the repo .env. Steps:
#   1. Load the API key from agentic-labs/.env into this process.
#   2. Run the test suite (red/green gate).
#   3. Run headless Claude Code to review calc.py and emit STRUCTURED JSON.
#   4. Parse that JSON into a pass/fail gate (exit code 0 = pass, 1 = fail).
#
# Run from this folder:   .\run_review.ps1
# Requires: the `claude` CLI on PATH, `py` + pytest, and ANTHROPIC_API_KEY in ../../.env

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# --- 1. load the key from the repo .env (agentic-labs/.env, two levels up) ----------
$envFile = Join-Path $PSScriptRoot "..\..\.env"
if (-not (Test-Path $envFile)) {
    Write-Error "No .env found at $envFile - add ANTHROPIC_API_KEY there first."
    exit 2
}
$line = Get-Content $envFile | Where-Object { $_ -match '^\s*ANTHROPIC_API_KEY\s*=' } | Select-Object -First 1
if (-not $line) {
    Write-Error "ANTHROPIC_API_KEY not found in $envFile"
    exit 2
}
$env:ANTHROPIC_API_KEY = ($line -split '=', 2)[1].Trim().Trim('"')
Write-Host "[1/4] Loaded ANTHROPIC_API_KEY from .env (len=$($env:ANTHROPIC_API_KEY.Length))."

# --- 2. tests gate -------------------------------------------------------------------
Write-Host "[2/4] Running tests..."
py -m pytest -q
if ($LASTEXITCODE -ne 0) {
    Write-Host "GATE: FAIL (tests red) - skipping review."
    exit 1
}

# --- 3. headless Claude Code review -> structured JSON -------------------------------
Write-Host "[3/4] Running headless Claude review (claude -p, JSON out)..."
$prompt = 'Review calc.py in this folder for correctness and missing edge cases. Reply with ONLY a JSON object: {"verdict": "pass" | "fail", "issues": ["..."]}. No prose.'
claude -p $prompt --output-format json | Out-File -Encoding utf8 review.json
Get-Content review.json

# --- 4. parse JSON into a pass/fail gate ---------------------------------------------
Write-Host "[4/4] Parsing review into a gate..."
py parse_output.py review.json
exit $LASTEXITCODE
