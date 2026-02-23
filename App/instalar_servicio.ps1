# Script para instalar la aplicación como servicio de Windows usando NSSM
# Ejecutar como Administrador: Click derecho > "Ejecutar con PowerShell" > Seleccionar "Sí"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Instalador de Servicio - Flask App CGA" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que se ejecuta como administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: Este script debe ejecutarse como Administrador" -ForegroundColor Red
    Write-Host "Click derecho en el archivo > Ejecutar con PowerShell > Seleccionar 'Sí'" -ForegroundColor Yellow
    pause
    exit
}

# Configuración - AJUSTAR ESTAS RUTAS SEGÚN TU SISTEMA
$nssmPath = "C:\Users\atecnologia2\Downloads\nssm-2.24\nssm-2.24\win64\nssm.exe"  # Ruta a nssm.exe
$serviceName = "FlaskAppCGA"
$appDir = "C:\Visualizacion_tablas_\App"
$appFile = "C:\Visualizacion_tablas_\App\App.py"

# Buscar Python automáticamente
Write-Host "Buscando Python..." -ForegroundColor Yellow

# Intentar diferentes formas de encontrar Python
$pythonPath = $null

# 1. Buscar en PATH
$pythonPath = "C:\Visualizacion_tablas_\App\Entorno_V\Scripts\python.exe"

# 2. Si no está en PATH, buscar en ubicaciones comunes
if (-not $pythonPath) {
    $commonPaths = @(
        "$appDir\Entorno_V\Scripts\python.exe",
        "$appDir\.venv\Scripts\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "C:\Python313\python.exe",
        "C:\Python312\python.exe",
        "C:\Python311\python.exe"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            $pythonPath = $path
            Write-Host "Python encontrado en ubicación común: $pythonPath" -ForegroundColor Green
            break
        }
    }
}

# 3. Si aún no se encuentra, pedir al usuario
if (-not $pythonPath) {
    Write-Host "ERROR: Python no encontrado automáticamente" -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor, ingresa la ruta completa a python.exe:" -ForegroundColor Yellow
    Write-Host "Ejemplo: C:\Users\atecnologia2\AppData\Local\Programs\Python\Python313\python.exe" -ForegroundColor Gray
    Write-Host "O si usas entorno virtual: C:\Users\atecnologia2\Desktop\Visualización_tablas_\App\Entorno_V\Scripts\python.exe" -ForegroundColor Gray
    Write-Host ""
    $pythonPath = Read-Host "Ruta a python.exe"
    
    if (-not (Test-Path $pythonPath)) {
        Write-Host "ERROR: La ruta ingresada no existe: $pythonPath" -ForegroundColor Red
        pause
        exit
    }
}

Write-Host "Python encontrado: $pythonPath" -ForegroundColor Green

# Verificar que nssm.exe existe
if (-not (Test-Path $nssmPath)) {
    Write-Host "ERROR: nssm.exe no encontrado en: $nssmPath" -ForegroundColor Red
    Write-Host "Por favor, ajusta la variable `$nssmPath en este script" -ForegroundColor Yellow
    pause
    exit
}

# Verificar que App.py existe
if (-not (Test-Path $appFile)) {
    Write-Host "ERROR: App.py no encontrado en: $appFile" -ForegroundColor Red
    Write-Host "Por favor, ajusta la variable `$appDir en este script" -ForegroundColor Yellow
    pause
    exit
}

Write-Host ""
Write-Host "Configuración:" -ForegroundColor Cyan
Write-Host "  Servicio: $serviceName" -ForegroundColor White
Write-Host "  Python: $pythonPath" -ForegroundColor White
Write-Host "  App.py: $appFile" -ForegroundColor White
Write-Host "  Directorio: $appDir" -ForegroundColor White
Write-Host ""

# Crear carpeta de logs si no existe
$logsDir = "$appDir\logs"
if (-not (Test-Path $logsDir)) {
    New-Item -ItemType Directory -Path $logsDir | Out-Null
    Write-Host "Carpeta de logs creada: $logsDir" -ForegroundColor Green
}

# Verificar si el servicio ya existe
$serviceExists = Get-Service -Name $serviceName -ErrorAction SilentlyContinue

if ($serviceExists) {
    Write-Host "El servicio '$serviceName' ya existe." -ForegroundColor Yellow
    $response = Read-Host "¿Deseas eliminarlo y reinstalarlo? (S/N)"
    if ($response -eq "S" -or $response -eq "s") {
        Write-Host "Eliminando servicio existente..." -ForegroundColor Yellow
        & $nssmPath stop $serviceName
        Start-Sleep -Seconds 2
        & $nssmPath remove $serviceName confirm
        Start-Sleep -Seconds 2
        Write-Host "Servicio eliminado." -ForegroundColor Green
    } else {
        Write-Host "Instalación cancelada." -ForegroundColor Yellow
        pause
        exit
    }
}

# Instalar servicio
Write-Host ""
Write-Host "Instalando servicio..." -ForegroundColor Yellow
& $nssmPath install $serviceName $pythonPath "$appFile"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR al instalar servicio" -ForegroundColor Red
    pause
    exit
}

# Configurar directorio de trabajo
Write-Host "Configurando directorio de trabajo..." -ForegroundColor Yellow
& $nssmPath set $serviceName AppDirectory "$appDir"

# Configurar inicio automático
Write-Host "Configurando inicio automático..." -ForegroundColor Yellow
& $nssmPath set $serviceName Start SERVICE_AUTO_START

# Configurar descripción
& $nssmPath set $serviceName Description "Aplicativo Visualización de Tablas CGA - Servidor Flask con Waitress"

# Configurar reinicio automático si falla
& $nssmPath set $serviceName AppRestartDelay 10000
& $nssmPath set $serviceName AppExit Default Restart

# Configurar logs
& $nssmPath set $serviceName AppStdout "$logsDir\output.log"
& $nssmPath set $serviceName AppStderr "$logsDir\error.log"

# Iniciar servicio
Write-Host ""
Write-Host "Iniciando servicio..." -ForegroundColor Yellow
& $nssmPath start $serviceName

Start-Sleep -Seconds 3

# Verificar estado
$service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
if ($service) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ¡Servicio instalado exitosamente!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Estado del servicio: $($service.Status)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Comandos útiles:" -ForegroundColor Yellow
    Write-Host "  Iniciar:   nssm start $serviceName" -ForegroundColor White
    Write-Host "  Detener:   nssm stop $serviceName" -ForegroundColor White
    Write-Host "  Reiniciar: nssm restart $serviceName" -ForegroundColor White
    Write-Host "  Estado:    nssm status $serviceName" -ForegroundColor White
    Write-Host ""
    Write-Host "La aplicación está accesible en:" -ForegroundColor Cyan
    Write-Host "  http://192.168.0.66:5500" -ForegroundColor White
    Write-Host "  http://TU_IP:5500" -ForegroundColor White
    Write-Host ""
    Write-Host "Logs disponibles en:" -ForegroundColor Cyan
    Write-Host "  $logsDir\output.log" -ForegroundColor White
    Write-Host "  $logsDir\error.log" -ForegroundColor White
} else {
    Write-Host "ERROR: No se pudo verificar el servicio" -ForegroundColor Red
}

Write-Host ""
pause
