@echo off
echo ========================================
echo   Iniciando Aplicativo CGA
echo ========================================
echo.

:: Navegar a la carpeta del proyecto
cd /d "%~dp0"

:: Verificar si existe entorno virtual
if exist "Entorno_V\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call Entorno_V\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call .venv\Scripts\activate.bat
) else (
    echo No se encontro entorno virtual, usando Python global...
)

echo.
echo Iniciando servidor con Waitress...
echo.

:: Ejecutar la aplicación
python App.py

:: Si se cierra, pausar para ver mensajes
pause