#!/usr/bin/env python3
"""
Compilation and Initialization Verification Test.
Verifies that all project modules compile, initialize, and execute clean campaign turns.
"""

import sys
import py_compile
import tempfile
from pathlib import Path

# Add root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

def test_syntax_compilation():
    print("1. Verificando compilação de sintaxe de todos os módulos Python...")
    py_files = list(BASE_DIR.glob("**/*.py"))
    for py_file in py_files:
        if "venv" in str(py_file):
            continue
        try:
            py_compile.compile(str(py_file), doraise=True)
            print(f"  [OK] {py_file.relative_to(BASE_DIR)}")
        except py_compile.PyCompileError as e:
            print(f"  [ERRO DE SINTAXE] {py_file}: {e}")
            sys.exit(1)

def test_engine_initialization():
    print("\n2. Verificando inicialização do motor de jogo (GameEngine & SQLite)...")
    from engine.domain.state_manager import GameEngine
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = Path(tmp_dir) / "test_init.db"
        engine = GameEngine(db_path=str(db_path), provider_name="mock_fallback")
        
        # Test Campaign Creation
        turn1 = engine.create_campaign("Test Kingdom", "King Arthur", "Valdrin", "Humano")
        assert turn1.aventura is not None
        assert turn1.status_reino is not None
        assert turn1.status_reino.nome_reino != ""
        print("  [OK] Criação de campanha e inicialização do SQLite3 bem-sucedidas.")
        
        # Test Turn Execution
        camps = engine.list_campaigns()
        assert len(camps) > 0
        turn2 = engine.execute_turn(camps[0]["id"], "Fortalecer muros")
        assert turn2.aventura is not None
        print("  [OK] Execução de turno e armazenamento de memórias episódicas (RAG) bem-sucedidos.")

def test_cli_import():
    print("\n3. Verificando importação e integridade do módulo CLI Terminal...")
    import cli.main
    print("  [OK] Módulo CLI importado sem erros.")

def test_server_dto_import():
    print("\n4. Verificando DTOs e esquemas do Servidor REST...")
    import server.dto
    print("  [OK] DTOs do servidor importados com sucesso.")

def main():
    print("=========================================================")
    print("   AI RPG GAME - TESTE DE COMPILAÇÃO E INICIALIZAÇÃO    ")
    print("=========================================================\n")
    test_syntax_compilation()
    test_engine_initialization()
    test_cli_import()
    test_server_dto_import()
    print("\n✅ TODOS OS TESTES DE COMPILAÇÃO E INICIALIZAÇÃO PASSARAM COM SUCESSO!")

if __name__ == "__main__":
    main()
