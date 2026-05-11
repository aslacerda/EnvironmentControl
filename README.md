# EnvironmentControl

Projeto de controle de ambiente com agente de IA e leitura de sensores (ESP32), desenvolvido para estudos de LLM + integração com hardware.

## Visão Geral

O projeto possui dois blocos principais:

- `python/`: agente conversacional que usa modelo local via endpoint OpenAI-compatible e chama ferramenta para consultar o ESP32.
- `esp32/`: firmware com PlatformIO (Arduino) que publica endpoint HTTP `/status` com temperatura e luminosidade.

## Estrutura

```
EnvironmentControl/
├─ esp32/
│  ├─ include/
│  │  ├─ secrets.example.h
│  │  └─ secrets.h (local, não versionado)
│  ├─ src/
│  │  └─ main.cpp
│  └─ platformio.ini
├─ python/
│  ├─ EnvironmentAgent.py
│  ├─ agent.py
│  └─ tools.py
└─ README.md
```

## Pré-requisitos

- Python 3.10+
- Ambiente virtual criado em `.venv`
- Dependências Python instaladas (ex.: `openai`, `requests`)
- PlatformIO disponível via `.venv` (`python -m platformio`)
- Endpoint de modelo ativo em `http://localhost:11434/v1` (ex.: Ollama compatível com API OpenAI)
- ESP32 acessível na rede (endpoint configurado em `python/tools.py`)

## Configuração do ESP32 (credenciais)

As credenciais de Wi-Fi não devem ir para o GitHub.

1. Copie `esp32/include/secrets.example.h` para `esp32/include/secrets.h`
2. Preencha SSID e senha no `secrets.h`

O arquivo `secrets.h` está no `.gitignore` e não é versionado.

## Hardware - Sensores

O projeto usa dois sensores conectados ao ESP32:

- **LM35**: Sensor de temperatura (pino GPIO 34, 10mV/°C)
- **LDR GL5528**: Sensor de luminosidade (pino GPIO 35, resistência variável)

Para pinagem completa, diagrama de divisor de tensão e calibração, veja [assets/HARDWARE.md](assets/HARDWARE.md).

## ESP32 com PlatformIO

Comandos na raiz do projeto (PowerShell):

```powershell
# Build
& ".venv/Scripts/python.exe" -m platformio run --project-dir "esp32"

# Upload
& ".venv/Scripts/python.exe" -m platformio run --project-dir "esp32" --target upload --upload-port COM4

# Monitor serial
& ".venv/Scripts/python.exe" -m platformio device monitor --project-dir "esp32" --port COM4 --baud 115200
```

O firmware expõe:

- `GET /status`: retorna JSON com `temperatura`, `luminosidade`, `rawLuz`, `tensao`, `ldrMin`, `ldrMax`.
- Logs no serial para cada requisição HTTP (método, IP de origem, resposta e tempo de processamento).

## Como Executar

No PowerShell, a partir da raiz do projeto:

```powershell
& ".venv/Scripts/python.exe" "python/EnvironmentAgent.py"
```

Para sair do agente, digite:

```text
sair
```

## Configuração Atual

- Modelo padrão: `llama3.2`
- Tool registrada: `call_esp32_api`
- Regras de sistema orientam quando chamar a tool (apenas perguntas sobre ambiente/sensores)

## Próximos Passos Sugeridos

- Adicionar validação de argumentos das tools
- Melhorar tratamento de falhas de rede do ESP32
- Criar testes para `agent.py` e `tools.py`
