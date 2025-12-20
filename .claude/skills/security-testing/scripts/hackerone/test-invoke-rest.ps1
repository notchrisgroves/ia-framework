#!/usr/bin/env pwsh
# Test using Invoke-RestMethod for JSON handling

# Load credentials
$envPath = "$env:USERPROFILE\.claude\.env"
$envContent = Get-Content $envPath
$username = ($envContent | Select-String 'HACKERONE_USERNAME=' | ForEach-Object { $_.ToString().Split('=', 2)[1].Trim('"').Trim("'") })
$token = ($envContent | Select-String 'HACKERONE_API_TOKEN=' | ForEach-Object { $_.ToString().Split('=', 2)[1].Trim('"').Trim("'") })

# Create auth
$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${username}:${token}"))

$headers = @{
    "Authorization" = "Basic $auth"
    "Accept" = "application/json"
}

Write-Host "[+] Fetching cloudflare with Invoke-RestMethod..."
$handle = "cloudflare"
$programUrl = "https://api.hackerone.com/v1/hackers/programs/$handle"

try {
    $details = Invoke-RestMethod -Uri $programUrl -Headers $headers -Method Get

    Write-Host "`n[+] Success! Checking structure..."
    Write-Host "  - Object type: $($details.GetType().FullName)"
    Write-Host "  - Properties: $($details.PSObject.Properties.Name -join ', ')"

    Write-Host "`n[+] Direct access test:"
    Write-Host "  - details.id: $($details.id)"
    Write-Host "  - details.type: $($details.type)"

    if ($details.attributes) {
        Write-Host "`n[+] attributes exist!"
        Write-Host "  - policy length: $($details.attributes.policy.Length) chars"
    }

    if ($details.relationships) {
        Write-Host "`n[+] relationships exist!"
        if ($details.relationships.structured_scopes) {
            Write-Host "  - structured_scopes exist"
            if ($details.relationships.structured_scopes.data) {
                $scopes = $details.relationships.structured_scopes.data
                Write-Host "  - structured_scopes.data count: $($scopes.Count)"
                Write-Host "`nFirst scope:"
                Write-Host "  - Type: $($scopes[0].type)"
                Write-Host "  - ID: $($scopes[0].id)"
                Write-Host "  - Asset Type: $($scopes[0].attributes.asset_type)"
                Write-Host "  - Asset Identifier: $($scopes[0].attributes.asset_identifier)"
                Write-Host "  - Eligible for bounty: $($scopes[0].attributes.eligible_for_bounty)"
            }
        }
    }
} catch {
    Write-Host "[-] Error: $_"
}
