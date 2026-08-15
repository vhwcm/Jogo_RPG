#!/usr/bin/env python3
import sys
import os
from typing import Optional

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.domain.state_manager import GameEngine
from engine.domain.models import KingdomStatus, TurnResponse

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt
    from rich.markdown import Markdown
    from rich.theme import Theme

    custom_theme = Theme({
        "gold": "bold yellow",
        "king": "bold magenta",
        "military": "bold red",
        "happy": "bold green",
        "narrative": "italic bright_white"
    })
    console = Console(theme=custom_theme)
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

def render_status_hud(status: KingdomStatus, turn_num: int):
    if HAS_RICH:
        table = Table(show_header=True, header_style="bold yellow", expand=True)
        table.add_column(f"REINO: [king]{status.nome_reino}[/king]", justify="center")
        table.add_column(f"IMPERADOR: [gold]{status.imperador}[/gold]", justify="center")
        table.add_column(f"OURO: [gold]{status.dinheiro:,}[/gold]", justify="center")
        table.add_column(f"POPULAÇÃO: [blue]{status.populacao:,}[/blue]", justify="center")
        table.add_column(f"MILITAR: [military]{status.poder_militar:,}[/military]", justify="center")
        table.add_column(f"FELICIDADE: [happy]{status.felicidade}[/happy]", justify="center")
        table.add_column(f"RELIGIÃO: [cyan]{status.religião}[/cyan]", justify="center")
        table.add_column(f"TURNO: [bold white]{turn_num}[/bold white]", justify="center")
        console.print(Panel(table, border_style="yellow", title="[bold yellow]STATUS DO REINO[/bold yellow]"))
    else:
        print("\n" + "="*50)
        print(f"REINO: {status.nome_reino} | IMPERADOR: {status.imperador}")
        print(f"OURO: {status.dinheiro} | POPULAÇÃO: {status.populacao} | MILITAR: {status.poder_militar} | FELICIDADE: {status.felicidade}")
        print(f"RELIGIÃO: {status.religião} | TURNO: {turn_num}")
        print("="*50 + "\n")

def render_narrative(turn: TurnResponse):
    if HAS_RICH:
        console.print("\n")
        console.print(Panel(Markdown(turn.aventura), border_style="cyan", title="[bold cyan]CRÔNICA REAL[/bold cyan]"))
        console.print("\n")
    else:
        print("\n--- CRÔNICA REAL ---")
        print(turn.aventura)
        print("---------------------\n")

def ask_input(prompt_text: str, default: str = "") -> str:
    if HAS_RICH:
        return Prompt.ask(prompt_text, default=default)
    else:
        suffix = f" [{default}]" if default else ""
        val = input(f"{prompt_text}{suffix}: ")
        return val.strip() if val.strip() else default

def select_or_create_campaign(engine: GameEngine) -> str:
    campaigns = engine.list_campaigns()
    if campaigns:
        print("\n=== AVENTURAS DISPONÍVEIS ===")
        for idx, c in enumerate(campaigns, 1):
            kingdom = c.get('kingdom_name') or 'Desconhecido'
            ruler = c.get('ruler_name') or 'Desconhecido'
            race = c.get('race') or 'Humano'
            turn_n = c.get('turn_number') or 0
            print(f"{idx}. {c['name']} (Reino: {kingdom} | Líder: {ruler} [{race}] | Turno: {turn_n}) [ID: {c['id']}]")
        print("0. Criar Nova Aventura")
        print("i. Importar Aventura (JSON)")
        
        choice = ask_input("\nEscolha uma opção", default="1")
        if choice.lower() == "i":
            filepath = ask_input("Caminho do arquivo JSON para importar")
            import json
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    cdata = json.load(f)
                cid = engine.import_campaign(cdata)
                print(f"\n✅ Aventura importada com sucesso (ID: {cid})!")
                return cid
            except Exception as e:
                print(f"❌ Erro ao importar: {e}")
        elif choice != "0" and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(campaigns):
                return campaigns[idx]["id"]

    print("\n=== CRIAÇÃO DE NOVO REINO ===")
    c_name = ask_input("Nome da Campanha/Aventura", default="Reino de Valdrin")
    ruler = ask_input("Seu nome (Imperador)", default="Arthur Pendragon")
    kingdom = ask_input("Nome do Reino", default="Valdrin")
    race = ask_input("Raça do Reino (Humano, Elfo, Anão, etc)", default="Humano")

    print("\nConsultando os oráculos reais...\n")
    turn = engine.create_campaign(c_name, ruler, kingdom, race)
    camps = engine.list_campaigns()
    return camps[0]["id"]

def load_and_display_campaign(engine: GameEngine, campaign_id: str):
    info = engine.get_campaign_info(campaign_id)
    if info and info.latest_status:
        render_status_hud(info.latest_status, turn_num=info.turn_number)
        print(f"\n--- CARREGANDO AVENTURA: '{info.name}' (Reino: {info.latest_status.nome_reino}) ---")
        history = engine.get_campaign_history(campaign_id)
        if history:
            latest = history[-1]
            raw = latest.get("raw_state", {})
            if raw.get("user_action"):
                print(f"\nÚltima Ordem: {raw['user_action']}")
            if raw.get("aventura"):
                print(f"\nCrônica Atual:\n{raw['aventura']}\n")

def main():
    if HAS_RICH:
        console.clear()
        console.print(Panel.fit(
            "[yellow]====================================================[/yellow]\n"
            "[king]      AI RPG GAME: ESTRATÉGIA E CRÔNICAS DO REINO     [/king]\n"
            "[yellow]====================================================[/yellow]",
            border_style="yellow"
        ))
    else:
        print("====================================================")
        print("      AI RPG GAME: ESTRATÉGIA E CRÔNICAS DO REINO     ")
        print("====================================================")

    engine = GameEngine()
    campaign_id = select_or_create_campaign(engine)
    load_and_display_campaign(engine, campaign_id)

    # Main Game Loop
    while True:
        print("[Comandos: '/status', '/aventuras', '/memoria', '/undo', '/historico', '/personagens', '/quests', '/exportar', '/deletar', 'fim']")
        user_input = ask_input("\nSUA ORDEM, MAJESTADE")

        if not user_input.strip():
            continue

        cmd = user_input.strip().lower()
        if cmd == "fim" or cmd == "sair":
            print("\nJogo salvo com sucesso. Até a próxima, Majestade!\n")
            break
        elif cmd == "/aventuras" or cmd == "/trocar":
            campaign_id = select_or_create_campaign(engine)
            load_and_display_campaign(engine, campaign_id)
            continue
        elif cmd == "/status":
            info = engine.get_campaign_info(campaign_id)
            if info and info.latest_status:
                render_status_hud(info.latest_status, turn_num=info.turn_number)
            continue
        elif cmd == "/memoria":
            mems = engine.vector_store.get_recent_memories(campaign_id, limit=5)
            print("\nMEMÓRIAS RAG RECENTES:")
            for m in mems:
                print(f"- Turno {m['turn_number']} (Imp: {m['importance']:.2f}): {m['content']}")
            print("\n")
            continue
        elif cmd == "/undo" or cmd == "/rollback":
            info = engine.get_campaign_info(campaign_id)
            if not info or info.turn_number <= 1:
                print("\nAviso: Não é possível voltar além do Turno 1.")
                continue
            target_str = ask_input(f"Voltar para qual turno? (1 a {info.turn_number - 1})", default=str(info.turn_number - 1))
            if target_str.isdigit():
                t_val = int(target_str)
                try:
                    turn = engine.rollback_turn(campaign_id, t_val)
                    print(f"\nEstado do reino revertido com sucesso para o Turno {t_val}!")
                    render_status_hud(turn.status_reino, turn_num=t_val)
                    render_narrative(turn)
                except Exception as e:
                    print(f"Erro ao reverter turno: {e}")
            continue
        elif cmd == "/historico":
            hist = engine.get_campaign_history(campaign_id)
            print("\nHISTÓRICO DE TURNOS E ESTADOS DO REINO:")
            for h in hist:
                print(f"- Turno {h['turn_number']}: Ouro: {h['gold']} | População: {h.get('population', 10000)} | Militar: {h['military']} | Felicidade: {h['happiness']}")
            print("\n")
            continue
        elif cmd == "/personagens":
            entities = engine.get_campaign_entities(campaign_id)
            chars = entities.get("characters", [])
            print("\nPERSONAGENS DO REINO:")
            if not chars:
                print("Nenhum personagem registrado ainda.")
            for c in chars:
                status_str = "Vivo" if c.get("is_alive") else "Falecido"
                print(f"- {c['name']} ({c.get('role', 'NPC')}) | Lealdade: {c.get('relationship_with_player', 0)} | Status: {status_str}")
            print("\n")
            continue
        elif cmd == "/quests":
            entities = engine.get_campaign_entities(campaign_id)
            quests = entities.get("quests", [])
            print("\nMISSÕES DO REINO:")
            if not quests:
                print("Nenhuma missão ativa registrada.")
            for q in quests:
                print(f"- [{q.get('status', 'active').upper()}] {q['title']}: {q.get('description', '')}")
            print("\n")
            continue
        elif cmd == "/exportar":
            import json
            try:
                data = engine.export_campaign(campaign_id)
                filename = f"savegame_{campaign_id}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                print(f"\n💾 Campanha exportada com sucesso para '{filename}'!")
            except Exception as e:
                print(f"❌ Erro ao exportar campanha: {e}")
            continue
        elif cmd == "/deletar":
            confirm = ask_input("Tem certeza que deseja DELETAR esta campanha permanentemente? (sim/nao)", default="nao")
            if confirm.lower() in ["sim", "s", "y", "yes"]:
                engine.delete_campaign(campaign_id)
                print("\n🗑️ Campanha excluída com sucesso.")
                campaign_id = select_or_create_campaign(engine)
                load_and_display_campaign(engine, campaign_id)
            continue

        print("\nO conselho real debate as vossas ordens...\n")
        try:
            turn = engine.execute_turn(campaign_id, user_input)
            info = engine.get_campaign_info(campaign_id)
            render_status_hud(turn.status_reino, turn_num=info.turn_number if info else 1)
            render_narrative(turn)
        except Exception as e:
            print(f"Erro ao processar turno: {e}")

if __name__ == "__main__":
    main()
