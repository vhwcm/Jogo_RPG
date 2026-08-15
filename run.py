#!/usr/bin/env python3
"""
Main Entry Point Launcher for AI RPG Game.
Usage:
  python run.py [web|cli|test|check]
"""

import sys
import os
import site
import subprocess

# Ensure user site-packages (e.g. ~/.local/lib/python3.12/site-packages) are in sys.path
user_site = site.getusersitepackages()
if user_site and user_site not in sys.path:
    sys.path.insert(0, user_site)

# Auto-activate venv if present in workspace and valid
VENV_PYTHON = os.path.join(os.path.dirname(__file__), "venv", "bin", "python")
if os.path.exists(VENV_PYTHON) and os.path.isfile(VENV_PYTHON) and sys.executable != VENV_PYTHON:
    os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)

import config

def show_api_key_warning_if_needed():
    if not config.is_any_api_key_configured():
        print("\n" + "=" * 45)
        print(" [AVISO DE CONFIGURAÇÃO] Nenhuma Chave de API de IA foi detectada!")
        print(" O jogo iniciará em modo de demonstração/offline com respostas simuladas.")
        print("")
        print(" COMO CONFIGURAR SUA CHAVE DE API:")
        print(" 1. Um arquivo '.env' foi gerado no diretório raiz do projeto.")
        print(" 2. Abra o arquivo '.env' e insira sua chave em uma das opções:")
        print("    • GEMINI_API_KEY=sua_chave (Grátis em: https://aistudio.google.com/app/apikey)")
        print("    • GROK_API_KEY=sua_chave   (Obtenha em: https://console.x.ai/)")
        print("    • OPENAI_API_KEY=sua_chave (Obtenha em: https://platform.openai.com/api-keys)")
        print(" 3. Salve o arquivo e reinicie a aplicação!")
        print("=" * 45 + "\n")

def main():
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "web"
    
    show_api_key_warning_if_needed()

    if mode == "web":
        try:
            import uvicorn
        except ImportError:
            print("Erro: Pacote 'uvicorn' ou dependências web não encontradas.")
            print("Por favor, instale executando: ./install.sh ou pip install -r requirements.txt")
            sys.exit(1)
        print(f"Iniciando Servidor Web do RPG em http://{config.WEB_HOST}:{config.WEB_PORT} ...")
        print(f"Acesse no navegador: http://localhost:{config.WEB_PORT} ou http://127.0.0.1:{config.WEB_PORT}\n")
        uvicorn.run("server.app:app", host=config.WEB_HOST, port=config.WEB_PORT, reload=True)
    elif mode == "cli":
        print("Iniciando RPG no Terminal...")
        from cli.main import main as cli_main
        cli_main()
    elif mode == "test":
        print("Executando Bateria de Testes...")
        res = subprocess.run([sys.executable, "-m", "pytest", "-v"])
        if res.returncode != 0:
            subprocess.run([sys.executable, "tests/test_compilation.py"])
    elif mode == "check":
        print("Executando Verificação de Diagnóstico das APIs...")
        from check_api import main as check_main
        check_main()
    else:
        print("Modo desconhecido. Use: python run.py [web|cli|test|check]")

if __name__ == "__main__":
    main()
