import requests

# Classe para gerenciar ferramentas
class ToolRegistry:
    def __init__(self):
        self.ferramentas = []
        self.funcoes = {}
    
    def registrar(self, nome, descricao, funcao, parametros=None):
        """Registra uma nova ferramenta"""
        self.ferramentas.append({
            'type': 'function',
            'function': {
                'name': nome,
                'description': descricao,
                'parameters': parametros or {'type': 'object', 'properties': {}}
            }
        })
        self.funcoes[nome] = funcao
    
    def obter_ferramentas(self):
        """Retorna a lista de ferramentas para o modelo"""
        return self.ferramentas
    
    def executar(self, nome_funcao):
        """Executa uma ferramenta registrada"""
        if nome_funcao not in self.funcoes:
            raise ValueError(f"Ferramenta '{nome_funcao}' não encontrada")
        return self.funcoes[nome_funcao]()


# Definição das ferramentas

def call_esp32_api():
    print('\n[TOOL_CALL] call_esp32_api foi chamada. Tentando obter dados do ESP32...')
    try:
        # IP padrão do ESP32 no modo SoftAP (fornecido pelo hotspot do notebook)
        url = "http://192.168.137.123/status"
        response = requests.get(url, timeout=2) # Timeout curto para não travar o chat
        dados = response.json()
        
        # Formata a string que a IA lerá como contexto
        return f"A temperatura na bancada é de {dados['temperatura']}°C e a luminosidade está em {dados['luminosidade']}%."
    except Exception as e:
        print(f"\n[TOOL_CALL] Erro ao tentar conectar ao ESP32: {e}")
        return f"Erro: Não foi possível conectar ao hardware do ESP32 na rede 'Agente_IA_Anderson'."

