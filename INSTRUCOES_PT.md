# Weather Data Pipeline — correções e execução (Windows + VS Code)

Este pacote contém **ficheiros de substituição** para o teu repositório existente:
- `notebooks/Weather_Analysis_Portfolio.ipynb` — notebook reconstruído, com modo offline e mapa Folium.
- `sample_data/historic_weather_2021_2022.csv` — 1.243 registos do teu trabalho académico original (sem credenciais).
- `src/pipeline.py` — versão corrigida da pipeline, compatível com `scripts/run_pipeline.py` atual, que força cidades portuguesas com `,PT`.
- `tests/test_pipeline.py` — 4 testes automáticos, que não precisam de internet.
- `requirements.txt`, `.gitignore`, `.env.example` — dependências, exclusões Git e modelo de configuração.

**Antes de substituir:** faz uma cópia de segurança do repositório, em especial do notebook. Não coloques o ZIP como uma subpasta dentro do repositório: copia **o conteúdo** para a pasta raiz existente, mantendo `scripts/run_pipeline.py` atual. Se já tens edições não publicadas, compara os ficheiros antes de os substituir.

## 1. Preparar Python local

No VS Code, abre a pasta raiz `weather-data-pipeline` e executa no terminal PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Não precisas de ativar scripts PowerShell para executar estes comandos. Se ainda não tens Python 3.11, instala-o primeiro ou usa uma versão 3.10+ compatível.

## 2. Testar sem acesso à OpenWeather

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Esperado: **4 passed**.

No VS Code abre `notebooks/Weather_Analysis_Portfolio.ipynb`, em `Select Kernel` escolhe o Python da pasta `.venv`, e executa **Run All**. A variável `DATA_SOURCE` está predefinida para `"sample"`: podes gerar os gráficos e o mapa sem chave API e sem recolher dados atuais.

Se vires `No module named folium`, certifica-te de que o kernel selecionado é o `.venv`; a instalação noutro Python não corrige o kernel errado.

## 3. Testar a recolha de dados atuais (com chave API)

Cria `.env` na raiz do projeto, usando `.env.example` como modelo. **Não publiques o `.env`**. Configura:

```text
OPENWEATHER_API_KEY=a_tua_chave_pessoal
```

Depois, na raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -m scripts.run_pipeline --ref-city "Peniche" --cities "Tomar" "Coimbra" "Braga" "Beja" --out-dir data/runs
```

A execução deve produzir `data/latest_weather.csv`, `data/latest_weather.json` e novos CSVs/JSONs em `data/runs/`. Uma chave nova pode demorar a ficar ativa na OpenWeather. Uma falha HTTP, rede ou chave inválida não é um problema do notebook.

Para analisar estes dados, muda no notebook:

```python
DATA_SOURCE = "runs"
```

Executa **Run All** novamente. Com uma única recolha, a análise de correlações avisa que ainda não existem dias suficientes — isso é esperado.

## 4. Verificações antes de publicares no GitHub

1. Confirma que `pytest` passa.
2. Confirma que todas as células do notebook executam sem exceção.
3. Confirma que `.env` e chaves antigas não estão no Git (incluindo commits anteriores).
4. Se alguma chave tiver sido exposta anteriormente, **revoga-a e gera uma nova** na OpenWeather.
5. Faz `git status` para verificar os ficheiros que realmente serão publicados.

## Nota sobre os dados originais

O ficheiro CSV mantém os dados académicos de 2021–2022 sem alterar as observações. No caso de **Beja**, o campo de distância original indica ~1.652 km devido à localização ambígua resolvida na Tunísia. O mapa offline usa coordenadas aproximadas de **Beja, Portugal** para ilustração, mas não reescreve a distância histórica. A pipeline corrigida força `,PT` e valida o país para as recolhas novas.

## Limites dos testes

A execução do notebook em modo `sample` e os testes unitários foram verificados offline. Não foi efetuada uma recolha real na OpenWeather porque não temos a tua chave nem acesso externo no ambiente de testes.
