$exclude = @("venv", "front_office.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "front_office.zip" -Force