# ==============================================================================
# DEÜ KİTAP SATIŞ - OTOMATİK POSTGRESQL YEDEKLEME VE E-POSTA SCRIPTİ
# ==============================================================================
# Bu script, veritabanını pg_dump ile yedekler, zip olarak sıkıştırır,
# 14 günden eski yedekleri siler ve başarılı/başarısız durumunu mail atar.
# ==============================================================================

# --- 1. KONFİGÜRASYON AYARLARI ---
$DbHost = ""
$DbPort = ""
$DbName = ""
$DbUser = ""
$DbPassword = ""

# Yedeklerin saklanacağı klasör
$BackupDir = "C:\BookStore_Backups"
$RetentionDays = 14

# E-posta (SMTP) Ayarları
$SmtpHost = ""
$SmtpPort = 
$SmtpUser = ""
$SmtpPassword = ""
$SmtpFrom = ""
$SmtpTo = ""
$UseSsl = $true

# pg_dump.exe'nin yolu (Boş bırakılırsa sistem PATH değişkeninde veya standart yollarda aranır)
$PgDumpPath = ""

# ==============================================================================
# --- 2. ÇALIŞMA MANTIĞI (DOKUNMAYIN) ---
# ==============================================================================

# Tarih ve saat formatı
$DateStr = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$BackupFileName = "bookstore_backup_$DateStr"
$SqlPath = Join-Path $BackupDir "$BackupFileName.sql"
$BackupPath = Join-Path $BackupDir "$BackupFileName.backup"
$ZipPath = Join-Path $BackupDir "$BackupFileName.zip"
$LogPath = Join-Path $BackupDir "backup_log.txt"

# Log yazma fonksiyonu
function Write-Log($message, $level = "INFO") {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logLine = "[$timestamp] [$level] $message"
    Write-Output $logLine
    Add-Content -Path $LogPath -Value $logLine -ErrorAction SilentlyContinue
}

try {
    # 1. Klasör Kontrolü
    if (-not (Test-Path $BackupDir)) {
        New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
        Write-Output "Yedekleme dizini oluşturuldu: $BackupDir"
    }

    Write-Log "Yedekleme işlemi başlatıldı..."

    # 2. pg_dump.exe'nin Yolu Tespiti
    if ([string]::IsNullOrEmpty($PgDumpPath)) {
        $PgDumpPath = Get-Command pg_dump -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source
    }

    if (-not $PgDumpPath -or -not (Test-Path $PgDumpPath)) {
        # Standart PostgreSQL kurulum yollarını kontrol et (Örn: v16, v15, v14, v13)
        $progFiles = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::ProgramFiles)
        $standardPaths = @(
            "$progFiles\PostgreSQL\16\bin\pg_dump.exe",
            "$progFiles\PostgreSQL\15\bin\pg_dump.exe",
            "$progFiles\PostgreSQL\14\bin\pg_dump.exe",
            "$progFiles\PostgreSQL\13\bin\pg_dump.exe"
        )
        foreach ($path in $standardPaths) {
            if (Test-Path $path) {
                $PgDumpPath = $path
                break
            }
        }
    }

    if (-not $PgDumpPath -or -not (Test-Path $PgDumpPath)) {
        throw "pg_dump.exe bulunamadı. Lütfen PostgreSQL kurulum dizinini PATH değişkenine ekleyin veya script içindeki `$PgDumpPath değişkenini düzenleyin."
    }

    Write-Log "Kullanılan pg_dump yolu: $PgDumpPath"

    # 3. pg_dump Çalıştırma (Parola geçici çevre değişkeninden okunur)
    $env:PGPASSWORD = $DbPassword
    
    # 3.1 Düz SQL Yedek Alma
    $dumpArgsSql = @(
        "--host=$DbHost",
        "--port=$DbPort",
        "--username=$DbUser",
        "--no-password",
        "--format=plain",
        "--file=$SqlPath",
        $DbName
    )
    Write-Log "SQL Dökümü alınıyor (Plain Text SQL)..."
    $processSql = Start-Process -FilePath $PgDumpPath -ArgumentList $dumpArgsSql -NoNewWindow -PassThru -Wait
    
    # 3.2 İkili pgAdmin Uyumlu Backup Alma
    $dumpArgsBackup = @(
        "--host=$DbHost",
        "--port=$DbPort",
        "--username=$DbUser",
        "--no-password",
        "--format=custom",
        "--file=$BackupPath",
        $DbName
    )
    Write-Log "Binary yedek dökümü alınıyor (pgAdmin Custom format)..."
    $processBackup = Start-Process -FilePath $PgDumpPath -ArgumentList $dumpArgsBackup -NoNewWindow -PassThru -Wait
    
    # Şifreyi çevre değişkeninden hemen temizle
    $env:PGPASSWORD = $null

    if ($processSql.ExitCode -ne 0 -or $processBackup.ExitCode -ne 0) {
        throw "pg_dump başarısız oldu. SQL Çıkış Kodu: $($processSql.ExitCode), Backup Çıkış Kodu: $($processBackup.ExitCode)"
    }

    if (-not (Test-Path $SqlPath) -or (Get-Item $SqlPath).Length -eq 0) {
        throw "Yedek SQL dosyası oluşturulamadı veya boş."
    }

    if (-not (Test-Path $BackupPath) -or (Get-Item $BackupPath).Length -eq 0) {
        throw "Yedek Backup dosyası oluşturulamadı veya boş."
    }

    Write-Log "Yedekler alındı. SQL: $(( (Get-Item $SqlPath).Length / 1KB ).ToString('F2')) KB, Backup: $(( (Get-Item $BackupPath).Length / 1KB ).ToString('F2')) KB"

    # 4. Zip formatında sıkıştırma (Her iki dosyayı birden ekle)
    Write-Log "Yedek dosyaları sıkıştırılıyor..."
    Compress-Archive -Path $SqlPath, $BackupPath -DestinationPath $ZipPath -Force
    
    # Ham dosyaları temizle
    Remove-Item $SqlPath, $BackupPath -Force

    $ZipSizeMB = (Get-Item $ZipPath).Length / 1MB
    Write-Log "Sıkıştırma tamamlandı. ZIP boyutu: $($ZipSizeMB.ToString('F2')) MB"

    # 5. Eski yedeklerin temizlenmesi (Retention)
    Write-Log "Eski yedekler taranıyor..."
    $LimitDate = (Get-Date).AddDays(-$RetentionDays)
    $OldFiles = Get-ChildItem -Path $BackupDir -Filter "*.zip" | Where-Object { $_.LastWriteTime -lt $LimitDate }

    foreach ($file in $OldFiles) {
        Write-Log "Eski yedek siliniyor: $($file.Name) (Oluşturma Tarihi: $($file.LastWriteTime))"
        Remove-Item $file.FullName -Force
    }

    # 6. E-posta Gönderimi
    Write-Log "E-posta gönderiliyor..."
    
    # Güvenli şifre objesi
    $SecurePassword = ConvertTo-SecureString $SmtpPassword -AsPlainText -Force
    $Credentials = New-Object System.Management.Automation.PSCredential ($SmtpUser, $SecurePassword)

    $MailSubject = "[DEÜ Kitap Satış] DB Yedekleme Başarılı - $DateStr"
    $MailBody = @"
Merhaba Yönetici,

DEÜ Kitap Satış veritabanı başarıyla yedeklenmiştir.

İşlem Detayları:
----------------------------------------
Veritabanı Adı : $DbName
Sunucu Host    : $DbHost
Tarih / Saat   : $(Get-Date -Format "dd.MM.yyyy HH:mm:ss")
Yedek Boyutu   : $($ZipSizeMB.ToString('F2')) MB
Dosya Adı      : $($BackupFileName).zip
Log Durumu     : Sorunsuz tamamlandı.
----------------------------------------

Yedek dosyası bu e-postaya eklenmiştir.

İyi çalışmalar.
"@

    # 20 MB kontrolü (E-posta ek limiti)
    if ($ZipSizeMB -lt 20) {
        Send-MailMessage -From $SmtpFrom -To $SmtpTo -Subject $MailSubject -Body $MailBody -SmtpServer $SmtpHost -Port $SmtpPort -Credential $Credentials -UseSsl -Attachments $ZipPath -Encoding UTF8 -ErrorAction Stop
        Write-Log "Yedek dosyası ek olarak e-postaya eklendi ve gönderildi."
    } else {
        $MailBody += "`n`nUYARI: Yedek boyutu 20 MB sınırını aştığı için e-postaya eklenmemiştir. Sunucudan manuel olarak '$ZipPath' adresinden erişebilirsiniz."
        Send-MailMessage -From $SmtpFrom -To $SmtpTo -Subject "$MailSubject (BÜYÜK BOYUT - EK DIŞI)" -Body $MailBody -SmtpServer $SmtpHost -Port $SmtpPort -Credential $Credentials -UseSsl -Encoding UTF8 -ErrorAction Stop
        Write-Log "Yedek boyutu 20 MB üzerinde olduğu için ek koyulmadan mail gönderildi."
    }

    Write-Log "Yedekleme işlemi başarıyla sonlandırıldı."

} catch {
    $ErrorMsg = $_.Exception.Message
    Write-Log "HATA OLUŞTU: $ErrorMsg" "ERROR"

    # Hata durumunda acil mail gönder
    try {
        $SecurePassword = ConvertTo-SecureString $SmtpPassword -AsPlainText -Force
        $Credentials = New-Object System.Management.Automation.PSCredential ($SmtpUser, $SecurePassword)
        $MailSubject = "[KRİTİK HATA] [DEÜ Kitap Satış] DB Yedekleme Başarısız! - $DateStr"
        $MailBody = @"
DİKKAT!

DEÜ Kitap Satış veritabanı otomatik yedekleme işlemi BAŞARISIZ olmuştur!

Hata Detayı:
----------------------------------------
$ErrorMsg
----------------------------------------
Tarih: $(Get-Date -Format "dd.MM.yyyy HH:mm:ss")

Lütfen en kısa sürede canlı sunucuyu ve yedekleme ayarlarını kontrol ediniz.
"@
        Send-MailMessage -From $SmtpFrom -To $SmtpTo -Subject $MailSubject -Body $MailBody -SmtpServer $SmtpHost -Port $SmtpPort -Credential $Credentials -UseSsl -Encoding UTF8 -ErrorAction Stop
    } catch {
        Write-Log "Hata bildirim maili gönderilirken de hata oluştu: $($_.Exception.Message)" "ERROR"
    }
}
