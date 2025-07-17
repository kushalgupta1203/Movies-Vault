# Fix API paths in frontend
$apiFile = "frontend\src\services\api.js"
$content = Get-Content $apiFile -Raw

# Replace remaining /watchlist/ with /api/watchlist/
$content = $content -replace '(?<!\bapi)/watchlist/', '/api/watchlist/'

# Replace remaining /movies/ with /api/movies/
$content = $content -replace '(?<!\bapi)/movies/', '/api/movies/'

# Save the file
Set-Content $apiFile $content

Write-Host "Fixed API paths in $apiFile"
