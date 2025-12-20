#!/usr/bin/env pwsh
# Debug script to test API calls

# Load credentials
$envPath = "$env:USERPROFILE\.claude\.env"
$envContent = Get-Content $envPath
$username = ($envContent | Select-String 'HACKERONE_USERNAME=' | ForEach-Object { $_.ToString().Split('=', 2)[1].Trim('"').Trim("'") })
$token = ($envContent | Select-String 'HACKERONE_API_TOKEN=' | ForEach-Object { $_.ToString().Split('=', 2)[1].Trim('"').Trim("'") })

Write-Host "[+] Username: $username"
Write-Host "[+] Token: $($token.Substring(0, 10))..."

# Create auth
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${username}:${token}"))

Write-Host "`n[+] Testing programs list API (no parameters)..."
$url = "https://api.hackerone.com/v1/hackers/programs"

$response = curl.exe -s -H "Authorization: Basic $auth" -H "Accept: application/json" $url
if ($response) {
    Write-Host "[+] Raw response length: $($response.Length) chars"
    Write-Host "[+] First 500 chars:"
    Write-Host $response.Substring(0, [Math]::Min(500, $response.Length))
} else {
    Write-Host "[-] Response is empty/null"
}

try {
    $json = $response | ConvertFrom-Json
    Write-Host "`n[+] Parsed successfully"
    Write-Host "  - Program count: $($json.data.Count)"
    if ($json.data) {
        Write-Host "`nFirst program:"
        Write-Host "  - Name: $($json.data[0].attributes.name)"
        Write-Host "  - Handle: $($json.data[0].attributes.handle)"
    }
} catch {
    Write-Host "`n[-] Failed to parse JSON: $_"
}
