$exclude = @("venv", "theAuctionSniper.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "theAuctionSniper.zip" -Force