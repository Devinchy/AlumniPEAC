@echo off
echo =========================================
echo Compilando documento LaTeX a PDF
echo =========================================
echo.

REM Cambiar al directorio de trabajo
cd /d "c:\Users\devin\OneDrive\AlumniPEAC"

REM Verificar si existe pdflatex
where pdflatex >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: pdflatex no encontrado en el PATH
    echo.
    echo Por favor, instala una distribución de LaTeX como:
    echo - MiKTeX: https://miktex.org/download
    echo - TeX Live: https://www.tug.org/texlive/
    echo.
    pause
    exit /b 1
)

echo Compilando el documento (primera pasada)...
pdflatex -interaction=nonstopmode charlas_completas_autogenerado.tex

echo.
echo Compilando el documento (segunda pasada para referencias)...
pdflatex -interaction=nonstopmode charlas_completas_autogenerado.tex

echo.
echo Compilando el documento (tercera pasada para tabla de contenidos)...
pdflatex -interaction=nonstopmode charlas_completas_autogenerado.tex

echo.
echo =========================================
echo Compilación completada
echo =========================================
echo.
echo El archivo PDF se encuentra en:
echo charlas_completas_autogenerado.pdf
echo.

REM Limpiar archivos auxiliares
echo Limpiando archivos temporales...
del *.aux *.log *.toc *.out 2>nul

pause
