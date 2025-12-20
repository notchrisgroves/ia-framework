# HackerOne API Test Script
# PowerShell-compatible version for Windows

# Read credentials from .env file
$envPath = "$env:USERPROFILE\.claude\.env"

if (-not (Test-Path $envPath)) {
    Write-Error ".env file not found at $envPath"
    exit 1
}

# Parse .env file
$envContent = Get-Content $envPath
$username = ($envContent | Select-String 'HACKERONE_USERNAME=' | ForEach-Object { $_.ToString().Split('=', 2)[1].Trim('"').Trim("'") })
$token = ($envContent | Select-String 'HACKERONE_API_TOKEN=' | ForEach-Object { $_.ToString().Split('=', 2)[1].Trim('"').Trim("'") })

if (-not $username -or -not $token) {
    Write-Error "Could not find HACKERONE_USERNAME or HACKERONE_API_TOKEN in .env file"
    exit 1
}

Write-Host "[+] Found credentials in .env file"
Write-Host "[+] Username: $username"
Write-Host "[+] Token: $($token.Substring(0, 10))..." # Only show first 10 chars

# Create Basic Auth header
$pair = "$username`:$token"
$bytes = [System.Text.Encoding]::ASCII.GetBytes($pair)
$base64 = [System.Convert]::ToBase64String($bytes)

Write-Host "[+] Testing HackerOne API authentication..."

# Call API
try {
    $response = curl.exe -s -H "Authorization: Basic $base64" "https://api.hackerone.com/v1/hackers/programs"

    # Try to parse JSON
    $json = $response | ConvertFrom-Json

    if ($json.errors) {
        Write-Host "`n[!] API returned error:"
        $json.errors | ConvertTo-Json -Depth 5
        exit 1
    }

    if ($json.data) {
        Write-Host "`n[+] SUCCESS! API authentication working"
        Write-Host "[+] Found $($json.data.Count) programs"
        Write-Host "`nFirst 3 programs:"
        $json.data | Select-Object -First 3 | ForEach-Object {
            Write-Host "  - $($_.attributes.name) ($($_.attributes.handle))"
        }
    } else {
        Write-Host "`n[!] Unexpected response format:"
        $response
    }

} catch {
    Write-Error "API call failed: $_"
    Write-Host "`nRaw response:"
    Write-Host $response
    exit 1
}
