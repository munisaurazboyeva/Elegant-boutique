$desktop = [Environment]::GetFolderPath("Desktop")
$s1 = Join-Path $desktop "Boutique Sayti.url"
$s2 = Join-Path $desktop "Azure Portal.url"

"[InternetShortcut]`r`nURL=https://elegant-boutique.azurewebsites.net" | Out-File -FilePath $s1 -Encoding ascii
"[InternetShortcut]`r`nURL=https://portal.azure.com" | Out-File -FilePath $s2 -Encoding ascii
