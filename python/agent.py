from openai import OpenAI

class AIAgent:
    """Gerencia interações com um modelo de IA com suporte a ferramentas"""
    
    def __init__(self, base_url, api_key, modelo):
        """
        Inicializa o agente
        
        Args:
            base_url: URL da API (ex: 'http://localhost:11434/v1')
            api_key: Chave da API
            modelo: Nome do modelo a usar (ex: 'llama3.2')
        """
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.modelo = modelo
        self.historico_messagens = []
        self.ferramentas = []
    
    def adicionar_role(self, content):
        """Adiciona uma mensagem de sistema (role)"""
        self.historico_messagens.append({'role': 'system', 'content': content})
    
    def registrar_ferramentas(self, ferramentas_lista):
        """Registra a lista de ferramentas disponíveis"""
        self.ferramentas = ferramentas_lista
    
    def adicionar_mensagem_usuario(self, msg):
        """Adiciona uma mensagem do usuário ao histórico"""
        self.historico_messagens.append({'role': 'user', 'content': msg})
    
    def adicionar_mensagem_assistente(self, msg):
        """Adiciona uma mensagem do assistente ao histórico"""
        self.historico_messagens.append({'role': 'assistant', 'content': msg})
    
    def adicionar_chamada_ferramenta(self, call_id, func_name, func_args):
        """Adiciona uma chamada de ferramenta ao histórico"""
        self.historico_messagens.append({
            'role': 'assistant',
            'tool_calls': [{
                'id': call_id,
                'type': 'function',
                'function': {'name': func_name, 'arguments': func_args}
            }]
        })
    
    def adicionar_resultado_ferramenta(self, call_id, func_name, result):
        """Adiciona o resultado de uma ferramenta ao histórico"""
        self.historico_messagens.append({
            'role': 'tool',
            'tool_call_id': call_id,
            'name': func_name,
            'content': result
        })
    
    def obter_completion(self):
        """Obtém um completion do modelo"""
        response = self.client.chat.completions.create(
            model=self.modelo,
            messages=self.historico_messagens,
            stream=True,
            tools=self.ferramentas if self.ferramentas else None,
            temperature=0
        )
        return response
    
    def processar_streaming(self, response):
        """Processa a resposta em streaming e retorna conteúdo + info de ferramentas"""
        full_response = ''
        call_id = None
        func_name = ''
        func_args = ''
        
        for chunk in response:
            delta = chunk.choices[0].delta
            
            if delta.content:
                print(delta.content, end='', flush=True)
                full_response += delta.content
            
            if delta.tool_calls:
                tc = delta.tool_calls[0]
                if tc.id:
                    call_id = tc.id
                if tc.function.name:
                    func_name = tc.function.name
                if tc.function.arguments:
                    func_args += tc.function.arguments
        
        return full_response, call_id, func_name, func_args
    
    def limitar_historico(self, max_turns=20):
        """Limita o histórico de mensagens, mantendo sempre as system messages"""
        system = []
        resto = []
        
        for m in self.historico_messagens:
            if m['role'] == 'system':
                system.append(m)
            else:
                resto.append(m)
        
        limite = max_turns * 2
        self.historico_messagens = system + resto[len(resto) - limite:] if len(resto) > limite else system + resto
    
    def obter_historico(self):
        """Retorna o histórico completo de mensagens"""
        return self.historico_messagens
    
    def limpar_historico(self):
        """Limpa o histórico mas mantém as roles (system messages)"""
        system = [m for m in self.historico_messagens if m['role'] == 'system']
        self.historico_messagens = system
