import pygame
import pygame.freetype
import os
from pygame import mixer
import pygame_gui
import google.generativeai as genai
import json

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'

##############################################################################Configurando Gemini#####################################################################################################################################################################
API_KEY = 'YOUR-API-KEY'
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
system_instruction =  "QUERO QUE SEU TEXTO GERADO SEJA TODO EM FORMATO JSON! Onde tera uma parte chamada 'aventura', e outra parte chamada 'status_reino'(nas partes dentro dessa, não ultrapasse 30 caracteres). dentro de status do reino terá uma parte chamada 'dinheiro'(somente o valor numérico).Uma parte chamada 'religião'(que seria a religião do meu reino).Uma parte chamada 'poder_militar'(valor numerico).Uma outra chamada 'nome_reino'.Outra chamada 'imperador'(meu nome).E por fim uma chamda 'felicidade'(0-100%).Utilize somente as partes json indicadas anterirmente. Estamos em um jogo de rpg.\\n\\ninicialmente(quando eu dicer que criarei um novo reino) eu poderei escolher um nome para o meu reino, meu  nome e espécie, a felicidade começa em 70% e o dinheiro entre 5.000, o poder militar inicial vai variar de acordo com a espécie(1000-5000). gostaria que o rpg fosse de estratégia, contento quizes, perguntas e desiões de estratégia. Eu serei o rei, e tomarei desições economicas, religiosas e militares. sempre me de opções enumeradas de escolha. minhas deçisoes afetaram os status do meu reino. Durante o jogo poderei fazer aliados e inimigos mortais, sendo que eles podem me atacar ou me proteger. O jogo funcionará como se voce fosse um servo do reino que me explicasse o que está acontecendo e me pedisse para escolher o que fazer. Eu posso fazer perguntas para vc para vc me detalhar algo. Sempre que um novo império entrar em contato, mostra os status de tal império como a barra de menu básica. Normalmente me de opções de numeradas para eu fazer uma decisão. no inicio voce sempre receberá um contexto na forma cronológica, só manter o contexto.Respoda somente em formato JSON sua resposta toda! Exemplo: \n  \"aventura\":\n\"Majestade asd, os gnomos de asd aguardam ansiosamente por sua orientação divina! As seguintes crenças ressoam com nosso povo:\\n\\n1. **A Grande Forja:** Reverencia a chama eterna como fonte de criação e engenhosidade gnômica.\\n2. **Os Espíritos da Floresta:** Busca harmonia com a natureza, venerando os espíritos ancestrais da floresta.\\n3. **O Culto à Engenhoca:** Valoriza a inteligência e a inovação, buscando aperfeiçoamento tecnológico constante.\\n\\nQual doutrina guiará as almas de asd, Majestade?\"\n ,\n  \"status_reino\": {\n    \"dinheiro\": 5000,\n    \"religião\": \"Indefinida\",\n    \"poder_militar\": 2000,\n    \"nome_reino\": \"asd\",\n    \"imperador\": \"asd\",\n    \"felicidade\": \"70%\"\n  }\n}\n"
system_instruction_h = "eu quero que com os dados que eu te dei vc guarde as informações, sem tópicos e em único paragrafo, como se fosse um livro com todas as informações que eu te dei, sem ser em formato de jogo, como se vc fosse um narrador oniciente.Guarde os status do reino. Ignora o que lhe for dado em que esteja numerado(pois seria as opçoes do jogador, mas ele não executara todas) Sempre que eu te mandar algo, escreva a continução da sua respostada dada anteriormente, com os novos dados. Escreva no máximo 3 linhas e não coloque nada que não coloque caracteres especias.LEMBRE=SE DE ESCREVER OS STATUS DO REINO"

model_h = genai.GenerativeModel(model_name='gemini-2.5-pro',generation_config=generation_config,system_instruction=system_instruction_h, safety_settings=safety_settings,)
chat_history = model_h.start_chat(history=[])
model = genai.GenerativeModel(model_name='gemini-2.5-pro',generation_config=generation_config,system_instruction=system_instruction, safety_settings=safety_settings,)
chat = model.start_chat(history=[])
#####################################################################################################################################################################################################################################################################
#################################################LOOP DO JOGO#####################################################################################################################################################################################################
global prompt

#formatando o texto
def blit_text(surface, text, pos, font, max_width, start_pos, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    x, y = pos
    y += start_pos
    max_height = 0
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
            max_height = max(max_height, y)
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
        max_height = max(max_height, y)
    return max_height - start_pos


clock = pygame.time.Clock()

#inicio do jogo
def game_screen():
    text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((16*screen_width/100, 97*screen_height/100), (81.5*screen_width/100, 30)), manager=manager)
    text_entry.hide()
    screen.fill((0, 0, 0))
    background = pygame.image.load(f"reinos/reino {especie}.png")
    screen_size = screen.get_size()
    background = pygame.transform.scale(background, screen_size)
    
    # Garantir que a pasta aventuras existe
    os.makedirs('aventuras/', exist_ok=True)
    
    file = open(f"aventuras/{aventura}.txt", "a+")
    file.seek(0)
    conteudo = file.read()
    if possui_reino.lower() == "sim":
        prompt = f"{conteudo}. Eu  estou continuando minha aventura. sou o imperador(a) do reino {reino} e gostaria de saber como ele está. Meu nome é {nome} e sou da raça{especie}."
    else:     
        prompt = f"Gostaria de criar um reino de '{especie}' chamado '{reino}'. Meu nome será '{nome}'. Para iniciar quero discutir qual será a religião do meu reino."
    chat.send_message(prompt)
    respost = chat.last.text

    #retirar possiveis respostas erradas do gemini
    respost = respost.replace("json", "")
    respost = respost.replace("```", "")
    respost = respost.replace("---", "")
    
    font_text = pygame.font.Font("Cinzel/Cinzel-VariableFont_wght.ttf", 22)
    fons = pygame.font.Font("Cinzel/Cinzel-VariableFont_wght.ttf", 22)

    #obtendo o json e armazenando em variaveis
    dados = json.loads(respost)
    aventure = dados['aventura']
    status = dados['status_reino']
    religião = status['religião']
    dinheiro = status['dinheiro']
    poder_militar = status['poder_militar']
    nome_reino = status['nome_reino']
    imperador = status['imperador']
    felicidade = status['felicidade']
    status_reino = f"######reino######\n{nome_reino}\n\n####Dinheiro######\n{dinheiro}\n\n#####Religião######\n{religião}\n\n##Poder militar###\n{poder_militar}\n\n####Felicidade####\n{felicidade}\n\n###Imperador#####\n{imperador}\n\n##################"
    informacoes = status_reino + "\n" + str(aventure)
    textl = f"{aventure}"

    clip_rect = pygame.Rect(17.5*screen_width/100, 3.7*screen_height/100, 93*screen_width/100, 93*screen_height/100)
    clip_rects = pygame.Rect(1, 8*screen_height/100, 15*screen_width/100, 83*screen_height/100)

    total_scroll = 0
    start_pos = 0
    running = True
    waiting_for_input = False
    l = 0

    #loop principal
    while running and prompt != "fim":
        #limitar os frames por segundo
        time_delta = clock.tick(5)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
            manager.process_events(event)
        screen.blit(background, (0, 0))
        screen.set_clip(clip_rects)   
        blit_text(screen, status_reino,(1 , 25*screen_height/100), fons, 83*screen_width/100, 0 , (255,255 ,255))    
        screen.set_clip(clip_rect)
        total_height = blit_text(screen, textl, (17.5*screen_width/100, 3.7*screen_height/100), font_text, 95*screen_width/100, start_pos, (255,255 ,255))
        pygame.display.flip()

        #otimizando o tempo de resposta para mandar informações ao gemini quando o novo texto já estiver sido carregado
        if l == 1:
          pygame.time.wait(8000)     
          chat_history.send_message(informacoes)
          file.write(chat_history.last.text )
          l = 0
          pygame.time.wait(8000)
    
        if total_scroll <= total_height - clip_rect.height and total_scroll >= 0:
            start_pos -= 0.3
            total_scroll += 0.3
        elif total_scroll >= total_height - clip_rect.height:
            screen.set_clip(None)
            text_entry.show()
            waiting_for_input = True
    
            #recebendo a resposta do jogador
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting_for_input = False
                    elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                            prompt = text_entry.get_text()
                            if prompt != "fim":
                                text_entry.hide()
                                pygame.display.flip()
                                chat.send_message(prompt)
                                respostaa = chat.last.text
                                respostaa = respostaa.replace("json", "")
                                respostaa = respostaa.replace("```", "")
                                respostaa = respostaa.replace("---", "")
                                respostaj = json.loads(respostaa)
                                status = respostaj['status_reino']
                                religião = status['religião']
                                dinheiro = status['dinheiro']
                                poder_militar = status['poder_militar']
                                nome_reino = status['nome_reino']
                                imperador = status['imperador']
                                felicidade = status['felicidade']
                                status_reino = f"######reino######\n{nome_reino}\n\n####Dinheiro######\n{dinheiro}\n\n#####Religião######\n{religião}\n\n##Poder militar###\n{poder_militar}\n\n####Felicidade####\n{felicidade}\n\n###Imperador#####\n{imperador}\n\n##################"
                                aventure = respostaj['aventura']
                                textl = f"{aventure}"  
                                l = 1
                                informacoes = status_reino + "\n" + aventure
                            waiting_for_input = False
                    
                    manager.process_events(event)
    
                manager.update(time_delta)
                manager.draw_ui(screen)
                pygame.display.flip()
    #encerrando e salvando
    chat_history.send_message(informacoes)
    file.write(chat_history.last.text ) 
    print ("\nFIM\n")
    pygame.quit()
        
        


 ##############################inicializando o jogo#############################################################################################################3   


pygame.init()
pygame.display.set_mode()


screen = pygame.display.get_surface()
if screen is not None:
    screen_width, screen_height = screen.get_size()
    screen_height = screen_height * 0.7
    screen_width = screen_width * 0.7

else:
    print('A tela ainda não foi inicializada')

# Configurações da tela
screen = pygame.display.set_mode((screen_width,screen_height))

manager = pygame_gui.UIManager((screen_width, screen_height))


# Configurações de fonte
FONT = pygame.font.Font(None, 32)

# Configurações de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Carrega a música
mixer.init()
mixer.music.load('musicas/clima de harmonia.mp3')
mixer.music.play()


# Configurações da fonte
FONT = pygame.freetype.Font("Cinzel/Cinzel-VariableFont_wght.ttf", 24)

questions = ["Qual o nome da aventura? ", "Qual o nome do seu reino? ", "Qual é seu nome? ", "Já possui um reino(sim ou nao)? "]
answers = [""] * len(questions)
active_index = 0

# Verificar se pasta aventuras existe, se não, criar
try:
    file_list = os.listdir('aventuras/')
except FileNotFoundError:
    os.makedirs('aventuras/', exist_ok=True)
    file_list = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(questions)):
                if pygame.Rect(10, i * 100 + 50, screen_width - 20, 32).collidepoint(event.pos):
                    active_index = i
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                active_index = (active_index + 1) % len(questions)
            elif event.key == pygame.K_BACKSPACE:
                answers[active_index] = answers[active_index][:-1]
            else:
                answers[active_index] += event.unicode
    
    screen.fill((0, 0, 0))
    for i, question in enumerate(questions):
        FONT.render_to(screen, (10, i * 100), question, (255, 255, 255))
        pygame.draw.rect(screen, (255, 255, 255), (10, i * 100 + 50, screen_width - 20, 32), 2)
        FONT.render_to(screen, (15, i * 100 + 55), answers[i], (255, 255, 255))

    
    
    pygame.display.flip()

    aventura = answers[0]
    reino = answers[1] 
    nome = answers[2]
    possui_reino = answers[3]
    if possui_reino.lower() == "sim" or possui_reino.lower() == "nao":
        if aventura != "" and reino != "" and nome != "":
            break

# Define o número de imagens por linha
IMAGES_PER_ROW = 7

# Carrega e redimensiona as imagens
image_files = os.listdir('lideres')
images = [pygame.image.load('lideres/' + file) for file in image_files]
images = [pygame.transform.scale(img, (200, 200)) for img in images]

# Cria os botões
buttons = [pygame.Rect((i % IMAGES_PER_ROW) * 210, 100 + (i // IMAGES_PER_ROW) * 210, 200, 200) for i in range(len(images))]

def button_clicked(i):
    global especie
    especie = os.path.splitext(image_files[i])[0]
    game_screen()

# Cria a fonte e o texto
font = pygame.font.Font(None, 60)
text = font.render("Escolha uma raça:", True, (255, 255, 255))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, button in enumerate(buttons):
                if button.collidepoint(event.pos):
                    button_clicked(i)

    screen.fill((0, 0, 0))
    screen.blit(text, (0, 50))  # Desenha o texto
    for i, button in enumerate(buttons):
        pygame.draw.rect(screen, (255, 255, 255), button)
        screen.blit(images[i], ((i % IMAGES_PER_ROW) * 210, 100 + (i // IMAGES_PER_ROW) * 210))
    pygame.display.flip()



pygame.quit()