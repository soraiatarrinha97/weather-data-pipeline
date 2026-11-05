@echo off
cd /d "%~dp0\.."

.\.venv\Scripts\python.exe -m scripts.run_pipeline --ref-city "Peniche" --cities "Tomar" "Coimbra" "Braga" "Castelo Branco" "Beja" "Sabugal" "Lisboa" "Viseu" "Aljustrel" "Leiria" --out-dir data\runs

pause