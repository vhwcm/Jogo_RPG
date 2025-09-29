import google.generativeai as genai
import os
import time

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'

#############################################Configurando o Gemini#############################################
API_KEY = 'API'

genai.configure(api_key=API_KEY)

generation_config = {
  "candidate_count": 1,
  "temperature": 0.
}

safety_settings={
    'HATE': 'BLOCK_NONE',
    'HARASSMENT': 'BLOCK_NONE',
    'SEXUAL' : 'BLOCK_NONE',
    'DANGEROUS' : 'BLOCK_NONE'
    }
system_instruction =  "Estamos em um jogo de rpg.\n\ninicialmente eu poderei escolher um nome para o meu reino, meu  nome e espécie. gostaria que o rpg fosse de estratégia, contento quizes, perguntas e desiões de estratégia. Eu serei o rei, e tomarei desições economicas, religiosas e militares. Quero que no INICIO de cada resposta tenha um menu básico indicando o estatus do meu reino de: Felicidade[0-100%], Poder militar[0 - 100000], atual religião do reino[no jogo existira religioes que não exitem na vida real, como por exemplo uma religiao de orcs.], Dinheiro[0 - 100000],\nnome do meu reino. minhas deçisoes afetaram os status do meu reino. Durante o jogo poderei fazer aliados e inimigos mortais, sendo que eles podem me atacar ou me proteger. O jogo funcionará como se voce fosse um servo do reino que me explicasse o que está acontecendo e me pedisse para escolher o que fazer. Eu posso fazer perguntas para vc para vc me detalhar algo. Sempre que um novo império entrar em contato, mostra os status de tal império como a barra de menu básica. Normalmente me de opções de numeradas para eu fazer uma decisão. no inicio voce sempre receberá um contexto na forma cronológica, só manter o contexto."
system_instruction_h = "eu quero que com os dados que eu te dei vc guarde as informações, sem tópicos e em único paragrafo, como se fosse um livro com todas as informações que eu te dei, sem ser em formato de jogo, como se vc fosse um narrador oniciente.Guarde os status do reino. Ignora o que lhe for dado em que esteja numerado(pois seria as opçoes do jogador, mas ele não executara todas) Sempre que eu te mandar algo, escreva a continução da sua respostada dada anteriormente, com os novos dados. Escreva no máximo 3 linhas e não coloque nada que não coloque caracteres especias.LEMBRE=SE DE ESCREVER OS STATUS DO REINO"
#O chat_history é usado para guardar as informações do jogo de forma resumida e impessoal(para o jogo multiplayer), para economizar recursos do Gemini
# Usando gemini-2.5-pro (modelo estável e atualizado)
model_h = genai.GenerativeModel(model_name='gemini-2.5-pro',generation_config=generation_config,system_instruction=system_instruction_h, safety_settings=safety_settings,)
chat_history = model_h.start_chat(history=[])
model = genai.GenerativeModel(model_name='gemini-2.5-pro',generation_config=generation_config,system_instruction=system_instruction, safety_settings=safety_settings,)
chat = model.start_chat(history=[])
###############################################################################################################
#pedindo informações para o usuário para iniciar o jogo
try:
    mundos = os.listdir("mundos/")
    print("Aventuras já criadas: ")
    if mundos:
        for mundo in mundos:
            mundo = mundo.replace(".txt", "")
            print(f"- {mundo}")
    else:
        print("- Nenhuma aventura encontrada")
except FileNotFoundError:
    print("- Pasta mundos/ não encontrada, será criada automaticamente")
    os.makedirs("mundos/", exist_ok=True)

print("\n")
nome_avetura = input("Qual o nome da aventura? ")
nome = input("Qual é o seu nome? ")
reino = input("Qual é o nome do reino? ")
raça = input("Qual é a raça do seu reino? ")
#perguntando se o usuário já possui um reino
while(1):
  con = input("Já possui um reino? ")
  if (con == "não"):
      pergunta = "Quero Criar um reino chamado "+reino+". Meu nome é "+nome+" e a raça do reino será de "+raça+".Para Iniciar, gostaria de discutir a religião do reino."
      break
  elif (con == "sim"):
      pergunta = "Eu sou o rei de "+reino+" e meu nome é "+nome+" da "+raça+", gostaria de saber como está e o que está acontecendo em meu reino."
      break
  else:
    print("Responda sim ou não")
#loop principal do jogo
#o conteudo é usado para 'salvar' o jogo, para que o usuário possa continuar de onde parou. é possivel que se outra pessoa jogar ao mesmo tempo, tenha meio que um jogo multiplayer, mas sempre verificando para não requerir muito do Gemini
arquivo_mundo = f'mundos/{nome_avetura}.txt'

# Carregar conteúdo existente uma vez
try:
    with open(arquivo_mundo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
except FileNotFoundError:
    conteudo = ""

while(pergunta != "fim"):
    try:
        mensagem = conteudo + "\n\n" + pergunta
        chat.send_message(mensagem)
        print("\n",chat.last.text,"\n")         
        continuacao = chat.last.text
        time.sleep(2)
        
        # Salvar histórico
        chat_history.send_message(continuacao + " guarde os status do reino, como religiao, poder militar, dinheiro e felicidade.")
        novo_conteudo = chat_history.last.text
        
        # Atualizar arquivo de forma mais eficiente
        with open(arquivo_mundo, 'a', encoding='utf-8') as f:
            f.write(novo_conteudo + "\n")
        
        # Atualizar conteúdo em memória
        conteudo += novo_conteudo + "\n"
        
        pergunta = input(f'PROMPT: ')
        
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg and "models/" in error_msg:
            print(f"❌ Erro: Modelo Gemini não encontrado!")
            print(f"🔧 Solução: O modelo foi atualizado. Verifique o código.")
        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
            print(f"⚠️ Cota da API excedida. Aguarde alguns minutos.")
        elif "api" in error_msg.lower():
            print(f"🔑 Erro de API: Verifique sua chave de API.")
        else:
            print(f"❌ Erro durante o jogo: {e}")
        
        print("Tentando continuar...")
        pergunta = input(f'PROMPT: ')

print("\nFim do jogo\n")

