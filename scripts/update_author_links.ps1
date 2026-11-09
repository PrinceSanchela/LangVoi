<#
.SYNOPSIS
    Interactive utility to customize GitHub username, Gumroad URL, and Buy Me a Coffee links
    across all documentation and configuration files in LangVoi Voice Studio Pro.
#>

param (
    [string]$GitHubUser = "PrinceSanchela",
    [string]$CoffeeUser = "princesanchela",
    [string]$GumroadUser = "codeprince",
    [string]$Email = "contact.princesanchela@gmail.com"
)

$RootDir = Split-Path -Parent $PSScriptRoot
Set-Location $RootDir

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "     LangVoi - Author & Monetization Link Customizer        " -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Configuring links with:"
Write-Host "  GitHub:          $GitHubUser" -ForegroundColor Green
Write-Host "  BuyMeACoffee:    $CoffeeUser" -ForegroundColor Green
Write-Host "  Gumroad:         $GumroadUser" -ForegroundColor Green
Write-Host "  Email:           $Email" -ForegroundColor Green

# Update .github/FUNDING.yml
$FundingPath = Join-Path $RootDir ".github\FUNDING.yml"
$FundingContent = @"
# GitHub Community Funding & Sponsorship Links
# LangVoi Voice Studio Pro — Prince Sanchela

github: $GitHubUser
buy_me_a_coffee: $CoffeeUser
ko_fi: $CoffeeUser
custom:
  - https://$GumroadUser.gumroad.com/l/langvoi
  - https://buymeacoffee.com/$CoffeeUser
  - https://paypal.me/$CoffeeUser
"@
Set-Content -Path $FundingPath -Value $FundingContent -Force
Write-Host "[OK] Updated .github/FUNDING.yml" -ForegroundColor Green

Write-Host "`nAll profile and monetization links are active and configured!" -ForegroundColor Cyan
