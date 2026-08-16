# Requirements: Tactical Top Canvas & Inspector Split

## 🎯 Goal
Desacoplar os detalhes de nós e controles de comandos do mapa tático, alocando-os em um painel/canvas superior independente e expansível, acima do mapa do grafo. O mapa deve ser elástico (ocupar o espaço restante ou 100% da altura quando o painel superior estiver colapsado/ocultado), sem que as janelas de detalhes fiquem flutuando por cima do grafo cobrindo os nós e conexões.

## 📋 Requisitos Funcionais

- **R1 - Estrutura de Painel Superior Dedicado**: Criar uma seção superior (`#tactical-top-panel`) acima da área do mapa dentro de `.panel-tactical`, dividindo verticalmente a coluna direita em Painel Superior (controles + detalhes) e Área do Mapa (canvas elástico).
- **R2 - Toolbar Superior Integrada**: A barra com botões de Música, Novo Reino, Aventuras, Ativos, Quests, Eventos, Controles de Zoom, Filtro de Camada e Contagem de Nós deve residir no cabeçalho do painel superior.
- **R3 - Inspector de Detalhes do Nó no Painel Superior**: Ao clicar em qualquer nó do mapa tático (capital, obra, tropa, reino vizinho, bioma, etc.), as informações detalhadas (ícone, nome, tipo, status, grid de atributos, barras diplomáticas/saúde, lore narrativo e botões de ação rápida de ordens) devem ser exibidas dentro do painel superior, em vez de um drawer ou modal flutuante cobrindo o mapa.
- **R4 - Elasticidade e Redimensionamento do Mapa**: O container do canvas do mapa (`#map-canvas-wrapper`) deve ser flexível (`flex: 1`, altura dinâmica). Quando o painel superior abrir ou expandir seus detalhes, o mapa retrai para acomodar; quando os detalhes forem fechados ou o painel colapsado, o mapa expande suavemente para ocupar o espaço total disponível.
- **R5 - Controle de Colapso e Abertura (Toggle)**: O painel superior deve ter um botão de colapso/expansão intuitivo para ocultar a área superior (deixando apenas uma barra mínima com botão de reabrir) ou restaurá-la para o modo ativo.
- **R6 - Auto-abertura ao Selecionar Nó**: Se o painel superior estiver colapsado e o jogador clicar em um nó no mapa, o painel deve se descolapsar e expandir automaticamente para exibir os detalhes do nó selecionado.
- **R7 - Fechamento de Detalhes**: O usuário pode fechar os detalhes do nó através do botão "✖" ou clicando fora, retornando o painel superior ao seu estado padrão compacto e liberando mais espaço vertical para o mapa.

## ⚙️ Requisitos Não-Funcionais
- **RNF1 - Performance e Redesenho do Canvas**: O redimensionamento do canvas do mapa deve ser tratado de forma reativa pelo `ResizeObserver` no `tactical_map.js`, garantindo que não ocorram distorções de aspecto nem quedas de framerate.
- **RNF2 - Responsividade**: O layout deve se comportar perfeitamente em telas desktop e dispositivos móveis/telas menores (<900px).
- **RNF3 - Design Visual Premium**: Manter o padrão de glassmorphism, bordas douradas sutis, tipografia Cinzel/Outfit e efeitos de transição suaves.

## ✅ Critérios de Aceite
- [ ] O mapa e os detalhes não se sobrepõem: a área de nós/grafo fica 100% visível abaixo do painel de detalhes.
- [ ] A toolbar superior está perfeitamente integrada no painel superior.
- [ ] Clicar em um nó do mapa exibe imediatamente todos os seus atributos, diplomacia e ações no painel superior.
- [ ] O botão de colapsar oculta/recolhe o painel superior e o mapa ocupa a área vertical máxima.
- [ ] O botão de reabrir restaura o painel superior.
- [ ] Fechar a visualização do nó retrai os detalhes e reajusta a altura do mapa.
- [ ] Nenhuma quebra de testes ou regressão no ciclo de jogo.
