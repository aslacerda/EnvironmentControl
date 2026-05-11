# EnvironmentControl

Projeto de controle de ambiente com agente de IA e leitura de sensores (ESP32), desenvolvido para estudos de LLM + integração com hardware.

## Visão Geral

O projeto possui dois blocos principais:

- `python/`: agente conversacional que usa modelo local via endpoint OpenAI-compatible e pode chamar ferramentas.
- `esp32/`: código embarcado para disponibilizar status de sensores (temperatura/luminosidade) via HTTP.

## Estrutura

```
EnvironmentControl/
├─ esp32/
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
- Endpoint de modelo ativo em `http://localhost:11434/v1` (ex.: Ollama compatível com API OpenAI)
- ESP32 acessível na rede (endpoint configurado em `python/tools.py`)

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
