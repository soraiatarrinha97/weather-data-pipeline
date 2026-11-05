@echo off
setlocal
cd /d "%~dp0\.."
if not exist ".venv\Scripts\python.exe" (
    echo Missing .venv environment. Follow the Quick start in README.md.
    exit /b 1
)
".venv\Scripts\python.exe" -m scripts.run_pipeline --ref-city "Peniche" --cities "Tomar" "Coimbra" "Braga" "Castelo Branco" "Beja" "Sabugal" "Lisboa" "Viseu" "Aljustrel" "Leiria" --out-dir data/runs
if errorlevel 1 echo Pipeline failed. Check your .env API key and terminal output.
pause
