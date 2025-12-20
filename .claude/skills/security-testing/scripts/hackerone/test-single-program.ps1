#!/usr/bin/env pwsh
# Test fetching a single program to see response structure

# Load credentials
$envPath = "$env:USERPROFILE\.claude\.env"
$envContent = Get-Content $envPath
$username = ($envContent | Select-String 'HACKERONE_USERNAME=' | ForEach-Object { $_.ToString().Split('=', 2)[1].Trim('"').Trim("'") })
$token = ($envContent | Select-String 'HACKERONE_API_TOKEN=' | ForEach-Object { $_.ToString().Split('=', 2)[1].Trim('"').Trim("'") })

# Create auth
$pair = "${username}:${token}"
$bytes = [System.Text.Encoding]::ASCII.GetBytes($pair)
$base64 = [System.Convert]::ToBase64String($bytes)

Write-Host "[+] Testing program: cloudflare"

# Test with curl
$response = curl.exe -s -H "Authorization: Basic $base64" "https://api.hackerone.com/v1/hackers/programs/cloudflare"

# Save to file
$response | Out-File "test-cloudflare-response.json" -Encoding UTF8

# Try to parse and show structure
try {
    $json = $response | ConvertFrom-Json

    Write-Host "`n[+] Response structure:"
    Write-Host "  - data.type: $($json.data.type)"
    Write-Host "  - data.attributes keys: $($json.data.attributes.PSObject.Properties.Name -join ', ')"

    if ($json.data.attributes.policy) {
        Write-Host "  - Policy length: $($json.data.attributes.policy.Length) chars"
    } else {
        Write-Host "  - Policy: null or empty"
    }

    if ($json.included) {
        Write-Host "  - Included items: $($json.included.Count)"
        $json.included | ForEach-Object {
            Write-Host "    - Type: $($_.type)"
        }
    } else {
        Write-Host "  - Included: null or empty"
    }

    Write-Host "`n[+] Full response saved to test-cloudflare-response.json"
} catch {
    Write-Host "[!] Error parsing JSON: $_"
    Write-Host "`nRaw response:"
    Write-Host $response
}
