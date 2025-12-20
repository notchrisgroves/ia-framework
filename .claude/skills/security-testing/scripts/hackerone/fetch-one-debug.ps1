#!/usr/bin/env pwsh
# Debug fetching a single program to see data structure

# Load credentials
$envPath = "$env:USERPROFILE\.claude\.env"
$envContent = Get-Content $envPath
$username = ($envContent | Select-String 'HACKERONE_USERNAME=' | ForEach-Object { $_.ToString().Split('=', 2)[1].Trim('"').Trim("'") })
$token = ($envContent | Select-String 'HACKERONE_API_TOKEN=' | ForEach-Object { $_.ToString().Split('=', 2)[1].Trim('"').Trim("'") })

# Create auth
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${username}:${token}"))

Write-Host "[+] Fetching cloudflare program..."
$handle = "cloudflare"
$programUrl = "https://api.hackerone.com/v1/hackers/programs/$handle"

# Use curl
$detailsJson = curl.exe -s -H "Authorization: Basic $auth" -H "Accept: application/json" $programUrl
Write-Host "[+] Response length: $($detailsJson.Length) chars"

# Parse
$details = $detailsJson | ConvertFrom-Json

Write-Host "`n[+] Checking data structure..."
Write-Host "  - details.data exists: $($null -ne $details.data)"
Write-Host "  - details.data.attributes exists: $($null -ne $details.data.attributes)"
Write-Host "  - details.data.attributes.policy exists: $($null -ne $details.data.attributes.policy)"
Write-Host "  - Policy length: $($details.data.attributes.policy.Length) chars"

Write-Host "`n[+] Checking structured scopes..."
Write-Host "  - details.data.relationships exists: $($null -ne $details.data.relationships)"
Write-Host "  - details.data.relationships.structured_scopes exists: $($null -ne $details.data.relationships.structured_scopes)"
Write-Host "  - details.data.relationships.structured_scopes.data exists: $($null -ne $details.data.relationships.structured_scopes.data)"

if ($details.data.relationships.structured_scopes.data) {
    Write-Host "  - Count: $($details.data.relationships.structured_scopes.data.Count)"
    Write-Host "`nFirst scope:"
    $first = $details.data.relationships.structured_scopes.data[0]
    Write-Host "  - Type: $($first.type)"
    Write-Host "  - ID: $($first.id)"
    Write-Host "  - Has attributes: $($null -ne $first.attributes)"
    if ($first.attributes) {
        Write-Host "  - Asset Type: $($first.attributes.asset_type)"
        Write-Host "  - Asset Identifier: $($first.attributes.asset_identifier)"
    } else {
        Write-Host "  - Attributes object is NULL!"
    }
}
