import pygame
import pygame.freetype
import os
from pygame import mixer
import pygame_gui
import google.generativeai as genai
import json
import time

# Silenciar warnings do Google Cloud (opcional)
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'

##############################################################################
# CONFIGURAÇÃO GEMINI (OTIMIZADA)
##############################################################################
API_KEY = 'SUA_API_KEY_AQUI'  # <--- COLOQUE SUA CHAVE AQUI
genai.configure(api_key=API_KEY)

# Configuração para forçar resposta em JSON (Crucial para evitar erros)
generation_config_json = {
  "candidate_count": 1,
  "temperature": 0.4,
  "response_mime_type": "application/json"
}

# Configuração para o historiador (Texto normal)
generation_config_text = {
  "candidate_count": 1,
  "temperature": 0.2,
}

safety_settings = {
    'HATE': 'BLOCK_NONE',
    'HARASSMENT': 'BLOCK_NONE',
    'SEXUAL': 'BLOCK_NONE',
    'DANGEROUS': 'BLOCK_NONE'
}

# Prompt do Jogo (Game Master)
system_instruction = """
VOCÊ É O CONSELHEIRO REAL EM UM RPG DE ESTRATÉGIA MEDIEVAL/FANTASIA.
SUA MISSÃO É NARRAR EVENTOS E GERENCIAR OS DADOS DO REINO.

### REGRAS DE FORMATAÇÃO (OBRIGATÓRIO)
Sua resposta deve ser APENAS um JSON seguindo exatamente este esquema:
{
  "aventura": "Texto narrativo aqui (máximo 600 caracteres). Descreva o cenário, o conflito e apresente SEMPRE 3 opções numeradas de ação ao final em linhas separadas.",
  "clima": "aventura | calmo | frenetico | harmonia | desenvolvimento | desespero (Escolha obrigatoriamente a opção que melhor reflete a atmosfera do momento narrativo)",
  "opcoes": [
    "1. Primeira opção de ação",
    "2. Segunda opção de ação",
    "3. Terceira opção de ação"
  ],
  "status_reino": {
    "nome_reino": "Nome do Reino (String)",
    "imperador": "Nome do Jogador (String)",
    "dinheiro": 5000 (Inteiro, sem pontos),
    "populacao": 10000 (Inteiro, sem pontos),
    "religião": "Nome da Religião (String)",
    "poder_militar": 1000 (Inteiro),
    "felicidade": "70%" (String com %)
  }
}

### EXEMPLOS DE FORMATO (SMALL SHOTS / FEW-SHOT)
Exemplo:
{
  "aventura": "Vossa Majestade, o reino prospera com a paz recém-alcançada. Os conselheiros solicitam vossas ordens sobre os investimentos prioritários do próximo ano.\\n\\n1. Expandir as rotas comerciais marítimas.\\n2. Recrutar novos soldados para a guarda imperial.\\n3. Construir um grande templo para fortalecer a fé do povo.",
  "clima": "desenvolvimento",
  "opcoes": [
    "1. Expandir as rotas comerciais marítimas.",
    "2. Recrutar novos soldados para a guarda imperial.",
    "3. Construir um grande templo para fortalecer a fé do povo."
  ],
  "status_reino": {
    "nome_reino": "Aurelia",
    "imperador": "Arthur",
    "dinheiro": 5000,
    "populacao": 10000,
    "religião": "Nenhuma",
    "poder_militar": 2000,
    "felicidade": "75%"
  }
}

### REGRAS DE JOGO
1. **Início:** Se for criar um novo reino, defina Felicidade: 70%, Dinheiro: 5000, Militar: 1000-5000 (variando pela espécie).
2. **Consequências:** As escolhas do usuário devem alterar os números no próximo turno logicamente (ex: guerra gasta dinheiro e militar).
3. **Clima Musical:** Defina o campo 'clima' dinamicamente baseado na narrativa do momento ('frenetico', 'desespero', 'harmonia', 'desenvolvimento', 'calmo' ou 'aventura').
4. **Tom:** Use linguagem formal ("Vossa Majestade").
5. **Inputs:** O usuário enviará comandos ou escolhas. Interprete-os e avance a história.
6. **Opções:** Você DEVE fornecer a lista 'opcoes' com exatamente 3 alternativas.
"""

# Prompt do Historiador (Save Game)
system_instruction_h = """
ATUE COMO O CRONISTA REAL.
Sua função é manter um registro conciso e cronológico em um ÚNICO parágrafo denso.
1. Atualize o resumo anterior com os novos eventos.
2. Ignore opções que o jogador NÃO escolheu.
3. Mantenha os status numéricos finais no texto.
4. NÃO use tópicos, apenas texto corrido.
"""

# Inicializando Modelos
model_h = genai.GenerativeModel(
    model_name='gemini-2.5-flash', 
    generation_config=generation_config_text,
    system_instruction=system_instruction_h,
    safety_settings=safety_settings
)
chat_history = model_h.start_chat(history=[])

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    generation_config=generation_config_json, 
    system_instruction=system_instruction,
    safety_settings=safety_settings
)
chat = model.start_chat(history=[])


#################################################
# GAME LOOP & UI
#################################################

global prompt

# Função para quebra de linha automática (Word Wrap)
def blit_text(surface, text, pos, font, max_width, start_pos, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    x, y = pos
    y += start_pos
    max_height = 0
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
            max_height = max(max_height, y)
        x = pos[0]
        y += word_height
        max_height = max(max_height, y)
    return max_height - start_pos

clock = pygame.time.Clock()

MUSICAS_CLIMA = {
    "aventura": "musicas/clima de aventura.mp3",
    "calmo": "musicas/clima de calmo.mp3",
    "frenetico": "musicas/clima frenetico.mp3",
    "harmonia": "musicas/clima de harmonia.mp3",
    "desenvolvimento": "musicas/clima de desenvolvimento.mp3",
    "desespero": "musicas/clima de desespero.mp3"
}
musica_atual = None

def atualizar_musica_clima(clima):
    global musica_atual
    if not clima:
        clima = "aventura"
    norm_clima = str(clima).strip().lower()
    target_file = "musicas/clima de aventura.mp3"
    for key, file_path in MUSICAS_CLIMA.items():
        if key in norm_clima:
            target_file = file_path
            break
    if target_file != musica_atual:
        try:
            if not mixer.get_init():
                mixer.init()
            if os.path.exists(target_file):
                mixer.music.load(target_file)
                mixer.music.play(-1)
                musica_atual = target_file
        except Exception as e:
            print(f"Aviso áudio: {e}")

def game_screen():
    # UI Setup
    text_entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((16*screen_width/100, 97*screen_height/100), (81.5*screen_width/100, 30)), 
        manager=manager
    )
    text_entry.hide()
    screen.fill((0, 0, 0))
    
    # Carregamento de Assets com Fallback
    try:
        background = pygame.image.load(f"reinos/reino {especie}.png")
    except:
        background = pygame.Surface(screen.get_size())
        background.fill((50, 50, 50)) # Cinza se não achar imagem
        
    screen_size = screen.get_size()
    background = pygame.transform.scale(background, screen_size)
    
    os.makedirs('aventuras/', exist_ok=True)
    
    # Carregar Save ou Iniciar
    try:
        file = open(f"aventuras/{aventura}.txt", "r")
        conteudo = file.read()
        file.close()
    except FileNotFoundError:
        conteudo = ""
    
    file = open(f"aventuras/{aventura}.txt", "a+")

    if possui_reino.lower() == "sim":
        prompt_inicial = f"{conteudo}. CONTINUAÇÃO: Eu sou o imperador(a) {nome} do reino {reino} (raça {especie}). Relate a situação atual."
    else:      
        prompt_inicial = f"CRIAR NOVO REINO: Raça '{especie}', Nome '{reino}', Imperador '{nome}'. Vamos discutir a religião inicial."
    
    # Primeiro envio para a IA
    try:
        chat.send_message(prompt_inicial)
        respost = chat.last.text
    except Exception as e:
        print(f"Erro API Inicial: {e}")
        pygame.quit()
        return

    # Configuração de Fontes
    try:
        font_text = pygame.font.Font("Cinzel/Cinzel-VariableFont_wght.ttf", 22)
        fons = pygame.font.Font("Cinzel/Cinzel-VariableFont_wght.ttf", 22)
    except:
        font_text = pygame.font.Font(None, 22)
        fons = pygame.font.Font(None, 22)

    try:
        dados = json.loads(respost)
    except json.JSONDecodeError:
        dados = {"aventura": "Erro ao processar dados do reino. Tente novamente.", "status_reino": {"dinheiro":0, "religião": "Erro", "poder_militar": 0, "nome_reino": "Erro", "imperador": "Erro", "felicidade": "0%"}}

    if 'clima' in dados:
        atualizar_musica_clima(dados.get('clima'))

    aventure = dados.get('aventura', '')
    status = dados.get('status_reino', {})
    
    # Extração segura
    religião = status.get('religião', 'N/A')
    dinheiro = status.get('dinheiro', 0)
    populacao = status.get('populacao', status.get('população', 10000))
    poder_militar = status.get('poder_militar', 0)
    nome_reino = status.get('nome_reino', 'N/A')
    imperador = status.get('imperador', 'N/A')
    felicidade = status.get('felicidade', '0%')

    status_texto_formatado = f"###### REINO ######\n{nome_reino}\n\n#### DINHEIRO ####\n{dinheiro}\n\n### POPULAÇÃO ###\n{populacao}\n\n##### RELIGIÃO #####\n{religião}\n\n## PODER MILITAR ##\n{poder_militar}\n\n#### FELICIDADE ####\n{felicidade}\n\n### IMPERADOR ###\n{imperador}\n\n##################"
    informacoes = status_texto_formatado + "\n" + str(aventure)
    textl = f"{aventure}"

    clip_rect = pygame.Rect(17.5*screen_width/100, 3.7*screen_height/100, 93*screen_width/100, 93*screen_height/100)
    clip_rects = pygame.Rect(1, 8*screen_height/100, 15*screen_width/100, 83*screen_height/100)

    total_scroll = 0
    start_pos = 0
    running = True
    waiting_for_input = False
    needs_history_update = False
    
    prompt_usuario = ""

    # LOOP PRINCIPAL DA TELA DE JOGO
    while running and prompt_usuario != "fim":
        time_delta = clock.tick(30)/1000.0 # Aumentei para 30FPS para fluidez
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.process_events(event)
            
            # Evento de input do usuário
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and waiting_for_input:
                prompt_usuario = text_entry.get_text()
                if prompt_usuario and prompt_usuario != "fim":
                    text_entry.set_text("") # Limpa input
                    text_entry.hide()
                    waiting_for_input = False
                    
                    # Enviar para IA
                    try:
                        # Feedback visual simples
                        textl = "O Conselheiro está pensando..."
                        chat.send_message(prompt_usuario)
                        respostaa = chat.last.text
                        
                        # Parse JSON
                        respostaj = json.loads(respostaa)
                        if 'clima' in respostaj:
                            atualizar_musica_clima(respostaj.get('clima'))
                        status = respostaj.get('status_reino', {})
                        
                        religião = status.get('religião', 'N/A')
                        dinheiro = status.get('dinheiro', 0)
                        populacao = status.get('populacao', status.get('população', 10000))
                        poder_militar = status.get('poder_militar', 0)
                        nome_reino = status.get('nome_reino', 'N/A')
                        imperador = status.get('imperador', 'N/A')
                        felicidade = status.get('felicidade', '0%')
                        
                        status_texto_formatado = f"###### REINO ######\n{nome_reino}\n\n#### DINHEIRO ####\n{dinheiro}\n\n### POPULAÇÃO ###\n{populacao}\n\n##### RELIGIÃO #####\n{religião}\n\n## PODER MILITAR ##\n{poder_militar}\n\n#### FELICIDADE ####\n{felicidade}\n\n### IMPERADOR ###\n{imperador}\n\n##################"
                        aventure = respostaj.get('aventura', '')
                        textl = f"{aventure}"
                        
                        informacoes = status_texto_formatado + "\n" + aventure
                        
                        # Flag para atualizar histórico no próximo frame (evita travar input)
                        needs_history_update = True
                        
                        # Resetar scroll
                        start_pos = 0
                        total_scroll = 0
                        
                    except Exception as e:
                        print(f"Erro na rodada: {e}")
                        textl = "Erro de comunicação com os deuses (API Error)."

        screen.blit(background, (0, 0))
        
        # Desenhar Status
        screen.set_clip(clip_rects)    
        blit_text(screen, status_texto_formatado, (1, 25*screen_height/100), fons, 83*screen_width/100, 0, (255,255,255))    
        
        # Desenhar Aventura (Texto Principal)
        screen.set_clip(clip_rect)
        total_height = blit_text(screen, textl, (17.5*screen_width/100, 3.7*screen_height/100), font_text, 95*screen_width/100, start_pos, (255,255,255))
        
        # Lógica de Scroll Automático
        if not waiting_for_input:
            if total_scroll <= total_height - clip_rect.height:
                start_pos -= 1.0 # Aumentei velocidade
                total_scroll += 1.0
            else:
                screen.set_clip(None)
                text_entry.show()
                text_entry.focus()
                waiting_for_input = True

        # Atualização do Historiador (Sem travar 8s, apenas um delay pequeno se necessário)
        if needs_history_update:
            try:
                chat_history.send_message(informacoes)
                file.write(chat_history.last.text + "\n")
                file.flush() # Garante gravação
            except:
                pass
            needs_history_update = False

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

    # Encerrando
    try:
        chat_history.send_message(informacoes)
        file.write(chat_history.last.text) 
        file.close()
    except:
        pass
    print("\nFIM DA SESSÃO\n")
    pygame.quit()


##############################
# INICIALIZANDO O JOGO
##############################

pygame.init()
pygame.display.set_mode()

screen = pygame.display.get_surface()
if screen is not None:
    screen_width, screen_height = screen.get_size()
    screen_height = screen_height * 0.9 # Ajuste leve
    screen_width = screen_width * 0.9
    screen = pygame.display.set_mode((int(screen_width), int(screen_height)))
else:
    screen = pygame.display.set_mode((1280, 720))
    screen_width, screen_height = 1280, 720

manager = pygame_gui.UIManager((int(screen_width), int(screen_height)))

# Tenta carregar música
atualizar_musica_clima("harmonia")

# Fonte para menus
try:
    FONT = pygame.freetype.Font("Cinzel/Cinzel-VariableFont_wght.ttf", 24)
except:
    FONT = pygame.freetype.SysFont("Arial", 24)

# Perguntas Iniciais
questions = ["Qual o nome da aventura? ", "Qual o nome do seu reino? ", "Qual é seu nome? ", "Já possui um reino(sim ou nao)? "]
answers = [""] * len(questions)
active_index = 0

# Menu de Texto Inicial
menu_running = True
while menu_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(questions)):
                if pygame.Rect(10, i * 100 + 50, screen_width - 20, 32).collidepoint(event.pos):
                    active_index = i
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                active_index = (active_index + 1) % len(questions)
                # Se preencheu tudo, tenta sair
                if all(answers) and active_index == 0:
                    menu_running = False
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

# Seleção de Raça 
IMAGES_PER_ROW = 7
try:
    image_files = [f for f in os.listdir('lideres') if f.endswith(('.png', '.jpg'))]
    images = [pygame.image.load('lideres/' + file) for file in image_files]
    images = [pygame.transform.scale(img, (200, 200)) for img in images]
    buttons = [pygame.Rect((i % IMAGES_PER_ROW) * 210, 100 + (i // IMAGES_PER_ROW) * 210, 200, 200) for i in range(len(images))]
    has_images = True
except:
    has_images = False
    especie = "Humano" # Default se não houver imagens
    print("Pasta 'lideres' vazia ou inexistente. Raça definida como Humano.")
    game_screen()

# Loop Seleção Raça
if has_images:
    font_race = pygame.font.Font(None, 60)
    text_race = font_race.render("Escolha uma raça:", True, (255, 255, 255))
    
    race_running = True
    while race_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                race_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        especie = os.path.splitext(image_files[i])[0]
                        game_screen() # Inicia o jogo
                        race_running = False # Sai do loop ao voltar

        screen.fill((0, 0, 0))
        screen.blit(text_race, (0, 50))
        for i, button in enumerate(buttons):
            pygame.draw.rect(screen, (255, 255, 255), button)
            screen.blit(images[i], ((i % IMAGES_PER_ROW) * 210, 100 + (i // IMAGES_PER_ROW) * 210))
        pygame.display.flip()

pygame.quit()