#!/usr/bin/env python3
"""
Diagnostic Script to probe and verify LLM API providers (Gemini, Grok/xAI, OpenAI, Ollama).
Performs automatic model discovery, tests live requests, and reports active model details.
"""

import sys
import time
import os
import config

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from engine.providers.gemini_provider import GeminiProvider
from engine.providers.grok_provider import GrokProvider
from engine.providers.openai_provider import OpenAIProvider
from engine.providers.ollama_provider import OllamaProvider

def test_provider(provider):
    name = provider.name.upper()
    print(f"\n🔍 Testando Provedor: {name}...")

    if not provider.is_available():
        print(f"❌ {name}: Não configurado ou chave de API ausente.")
        return {
            "name": name,
            "model": getattr(provider, "model_name", "N/A"),
            "status": "Não Configurado",
            "latency": "N/A",
            "json_support": "N/A",
            "embedding": "N/A"
        }

    start_time = time.time()
    try:
        # Test Text Generation Probe Request
        test_prompt = "Diga 'Conexão OK!' em uma palavra."
        text_resp = provider.generate_text(test_prompt, temperature=0.1)
        latency = f"{(time.time() - start_time) * 1000:.0f} ms"
        
        # Test JSON Generation Probe Request
        json_resp = provider.generate_json(
            "Retorne JSON com campo 'status': 'ok'",
            system_instruction="Responda em JSON.",
            temperature=0.1
        )
        has_json = "Sim" if isinstance(json_resp, dict) and len(json_resp) > 0 else "Falhou"

        # Test Embedding Generation Probe Request
        emb = provider.generate_embedding("Teste de vetor")
        has_emb = f"Sim ({len(emb)} dims)" if emb and len(emb) > 0 else "Falhou"

        active_model = getattr(provider, "model_name", "Padrao")
        print(f"✅ {name} (Modelo Ativo: {active_model}): Conexão bem-sucedida! Latência: {latency}")
        print(f"   Response snippet: {text_resp.strip()[:60]}")

        return {
            "name": name,
            "model": active_model,
            "status": "Online ✅",
            "latency": latency,
            "json_support": has_json,
            "embedding": has_emb
        }

    except Exception as e:
        print(f"❌ {name}: Erro de Conexão - {e}")
        return {
            "name": name,
            "model": getattr(provider, "model_name", "N/A"),
            "status": f"Erro: {str(e)[:30]}",
            "latency": "N/A",
            "json_support": "Falhou",
            "embedding": "Falhou"
        }

def main():
    if HAS_RICH:
        console.print(Panel.fit("[bold yellow]AI RPG GAME - DIAGNÓSTICO DE DESCOBERTA DE MODELOS & APIS[/bold yellow]"))
    else:
        print("=========================================================")
        print("   AI RPG GAME - DIAGNÓSTICO DE DESCOBERTA DE MODELOS   ")
        print("=========================================================")

    providers = [
        GeminiProvider(),
        GrokProvider(),
        OpenAIProvider(),
        OllamaProvider()
    ]

    results = []
    for p in providers:
        results.append(test_provider(p))

    if HAS_RICH:
        table = Table(title="[bold yellow]Status & Descoberta de Modelos de IA[/bold yellow]")
        table.add_column("Provedor", style="bold cyan")
        table.add_column("Modelo Descoberto / Ativo", style="bold yellow")
        table.add_column("Status", style="bold white")
        table.add_column("Latência", style="magenta")
        table.add_column("Suporte JSON", style="green")
        table.add_column("Embeddings Vetoriais", style="blue")

        for r in results:
            table.add_row(r["name"], r["model"], r["status"], r["latency"], r["json_support"], r["embedding"])

        console.print("\n")
        console.print(table)
    else:
        print("\n=== STATUS & MODELOS DESCOBERTOS DA IA ===")
        for r in results:
            print(f"- {r['name']} [Modelo: {r['model']}]: {r['status']} (Latência: {r['latency']}, JSON: {r['json_support']}, Embeddings: {r['embedding']})")

    print("\nDica: O sistema testa automaticamente todos os modelos disponíveis ao iniciar e seleciona o mais recente com resposta válida.\n")

if __name__ == "__main__":
    main()
