#!/usr/bin/env pwsh
# Fetch real HackerOne program scope examples
# Purpose: Extract scope documentation from real programs to show good/bad examples

param(
    [int]$ProgramCount = 15  # Will fetch first N programs from API response
)

# Load credentials from .env
$envPath = "$env:USERPROFILE\.claude\.env"

if (-not (Test-Path $envPath)) {
    Write-Host "[-] .env file not found at $envPath" -ForegroundColor Red
    exit 1
}

# Parse .env file (using same logic as test-api.ps1)
$envContent = Get-Content $envPath
$username = ($envContent | Select-String 'HACKERONE_USERNAME=' | ForEach-Object { $_.ToString().Split('=', 2)[1].Trim('"').Trim("'") })
$token = ($envContent | Select-String 'HACKERONE_API_TOKEN=' | ForEach-Object { $_.ToString().Split('=', 2)[1].Trim('"').Trim("'") })

if (-not $username -or -not $token) {
    Write-Host "[-] Missing HackerOne credentials in .env" -ForegroundColor Red
    Write-Host "[-] Required: HACKERONE_USERNAME and HACKERONE_API_TOKEN" -ForegroundColor Yellow
    exit 1
}

Write-Host "[+] Loaded credentials from .env" -ForegroundColor Green

# Base64 encode credentials
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${username}:${token}"))
$headers = @{
    "Authorization" = "Basic $auth"
    "Accept" = "application/json"
}

Write-Host "[+] Fetching HackerOne programs..." -ForegroundColor Green

# Fetch programs using Invoke-RestMethod for proper JSON handling
$url = "https://api.hackerone.com/v1/hackers/programs"
$response = Invoke-RestMethod -Uri $url -Headers $headers -Method Get

Write-Host "[+] Retrieved $($response.data.Count) programs, fetching scopes for first $ProgramCount..." -ForegroundColor Green

$scopeExamples = @()
$count = 0

foreach ($program in $response.data) {
    # Limit to requested count
    if ($count -ge $ProgramCount) { break }
    $count++
    $handle = $program.attributes.handle
    $name = $program.attributes.name

    Write-Host "[*] Fetching scope for: $name ($handle)" -ForegroundColor Cyan

    # Fetch program details including scope
    $programUrl = "https://api.hackerone.com/v1/hackers/programs/$handle"
    try {
        # Use Invoke-RestMethod - returns data directly without .data wrapper
        $details = Invoke-RestMethod -Uri $programUrl -Headers $headers -Method Get

        $scope = @{
            ProgramName = $name
            ProgramHandle = $handle
            URL = "https://hackerone.com/$handle"
            Policy = $details.attributes.policy
            StructuredScopes = @()
        }

        # Extract structured scopes from relationships
        if ($details.relationships.structured_scopes.data) {
            foreach ($item in $details.relationships.structured_scopes.data) {
                $scope.StructuredScopes += @{
                    AssetType = $item.attributes.asset_type
                    AssetIdentifier = $item.attributes.asset_identifier
                    EligibleForBounty = $item.attributes.eligible_for_bounty
                    EligibleForSubmission = $item.attributes.eligible_for_submission
                    Instruction = $item.attributes.instruction
                    MaxSeverity = $item.attributes.max_severity
                }
            }
        }

        $scopeExamples += $scope
        Start-Sleep -Milliseconds 500  # Rate limiting
    }
    catch {
        Write-Host "[-] Failed to fetch $handle : $_" -ForegroundColor Yellow
    }
}

# Output to JSON for processing
$outputPath = "C:\Users\Chris\.claude\scratchpad\hackerone-scope-examples.json"
$scopeExamples | ConvertTo-Json -Depth 10 | Out-File $outputPath -Encoding UTF8

Write-Host "`n[+] Fetched $($scopeExamples.Count) program scopes" -ForegroundColor Green
Write-Host "[+] Saved to: $outputPath" -ForegroundColor Green

# Output summary
Write-Host "`n=== SCOPE SUMMARY ===" -ForegroundColor Cyan
foreach ($example in $scopeExamples) {
    Write-Host "`n$($example.ProgramName) ($($example.ProgramHandle))"
    Write-Host "  In-Scope Assets: $($example.StructuredScopes.Count)"
    Write-Host "  URL: $($example.URL)"
}
