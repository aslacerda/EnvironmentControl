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



