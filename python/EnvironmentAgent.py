from agent import AIAgent
from tools import ToolRegistry, call_esp32_api

# Inicializa o registro de ferramentas
ferramentas_agent = ToolRegistry()

# Registra as ferramentas
ferramentas_agent.registrar(
    nome='call_esp32_api',
    descricao='Obtém a temperatura real (LM35) e luminosidade (LDR) da bancada via ESP32.',
    funcao=call_esp32_api
)

# Inicializa o agente IA
agent = AIAgent(
    base_url='http://localhost:11434/v1',
    api_key='ollama',
    modelo='llama3.2'
)

# Registra as ferramentas no agente
agent.registrar_ferramentas(ferramentas_agent.obter_ferramentas())

# Adiciona as roles (system messages)
agent.adicionar_role('Chame call_esp32_api APENAS quando o usuário perguntar sobre temperatura, luminosidade ou estado da bancada.')
agent.adicionar_role('Se a luminosidade estiver baixa, sugira ligar a luz.')
agent.adicionar_role('Se a temperatura estiver alta, avise.')

msg = ''
while msg != 'sair':
    # Solicita a mensagem ao usuário e encerra graciosamente com Ctrl+C/Ctrl+D
    try:
        msg = input('\nuser: ')
    except (KeyboardInterrupt, EOFError):
        print('\nEncerrando o agente...')
        break

    if msg.strip().lower() == 'sair':
        print('Encerrando o agente...')
        break

    #adiciona a msg ao histórico
    agent.adicionar_mensagem_usuario(msg)
    #solicita o completion
    response = agent.obter_completion()
    #imprime na tela
    full_response, call_id, func_name, func_args = agent.processar_streaming(response)
    #se houve uma chamada de ferramente
    if call_id: 
        #adiciona a chamada no histórico
        agent.adicionar_chamada_ferramenta(call_id, func_name, func_args)
        #verifica qual a função que foi chamada
        if func_name == 'call_esp32_api':
            #executa a função através do registro de ferramentas
            resultado = ferramentas_agent.executar(func_name)
            #adiciona o resultado no histórico de mensagens
            agent.adicionar_resultado_ferramenta(call_id, func_name, resultado)
            #cria um novo completion com o resultado da chamada de ferramenta
            response = agent.obter_completion()
            #stream da resposta na tela.
            full_response, call_id, func_name, func_args = agent.processar_streaming(response)
        #adiciona a resposta final ao histórico de mensagens!
        agent.adicionar_mensagem_assistente(full_response)
    else:
        #salva a msg do assistant no histórico
        agent.adicionar_mensagem_assistente(full_response)
    
    #limite o histórico de mensagens
    agent.limitar_historico()