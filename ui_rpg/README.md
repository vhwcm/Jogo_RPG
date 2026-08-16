# 🎮 Módulo UI RPG Desktop (`ui_rpg`)

O diretório `ui_rpg` contém a interface gráfica para desktop desenvolvida com **Pygame** e **Pygame GUI**, oferecendo uma experiência visual e sonora imersiva em janela nativa.

---

## 📂 Estrutura do Módulo

```
ui_rpg/
├── Cinzel/                 # Tipografia estilizada medieval (Cinzel Font Family)
├── lideres/                # Retratos artísticos dos soberanos de cada raça
├── reinos/                 # Cenários e castelos ilustrados dos reinos
├── musicas/                # Arquivos MP3 de trilha sonora adaptativa
├── aventuras/              # Histórico e logs de textos de aventuras salvas
├── rpg_grafico.py          # Aplicação principal Pygame com loop de renderização e eventos
├── run.sh                  # Script de execução rápida
├── check_env.sh            # Script de verificação de ambiente
├── install_dependencies.sh # Instalador de dependências Pygame
└── requirements.txt        # Dependências exclusivas do módulo desktop
```

---

## ✨ Principais Recursos

1. **Interface Gráfica Nativa**: Janela interativa com painéis de texto rolantes e caixas de diálogo estilizadas.
2. **Áudio Dinâmico com Pygame Mixer**: Transição suave de trilha sonora de fundo de acordo com a tensão e o clima da cena.
3. **Ilustrações Temáticas**: Exibição automática do retrato do soberano e da arte do castelo baseada na raça escolhida pelo jogador.

---

## 🚀 Como Executar

```bash
cd ui_rpg
./run.sh
```
Ou diretamente:
```bash
python ui_rpg/rpg_grafico.py
```
