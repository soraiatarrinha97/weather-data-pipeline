@echo off
REM Run Weather Data Pipeline using the conda env "weather"
REM Ensure you created the conda env:
REM   conda create -n weather python=3.10 -y
REM   conda activate weather
REM   pip install -r requirements.txt
REM and created a .env file with OPENWEATHER_API_KEY=...

cd /d %~dp0\..

conda run -n weather python -m scripts.run_pipeline --ref-city "Peniche" --cities "Tomar" "Coimbra" "Braga" "Castelo Branco" "Beja" "Sabugal" "Lisboa" "Viseu" "Aljustrel" "Leiria" --out-dir data\runs

pause
