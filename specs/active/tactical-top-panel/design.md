# Design: Tactical Top Canvas & Elastic Map Layout

## 1. Arquitetura da Apresentação Web

### 1.1 Hierarquia de Layout Anterior vs Novo

#### Layout Anterior:
```
.panel-tactical (relative, full height)
  ├── .tactical-canvas-container (absolute inset: 0 - o mapa ficava no fundo de tudo)
  ├── .tactical-toolbar (absolute top: 10px - flutuando sobre o mapa)
  ├── .map-corner-widget (absolute corners - flutuando sobre o mapa)
  └── .inspector-panel / .inspector-drawer (absolute drawer - cobrindo o mapa à direita)
```

#### Novo Layout Elástico:
```
.panel-tactical (display: flex; flex-direction: column; overflow: hidden;)
  ├── #tactical-top-panel (flex-shrink: 0, container superior com toolbar + área de detalhes expansível)
  │     ├── .tactical-top-header (toolbar com botões de áudio, reino, drawers, zoom, filtro e botão de colapso)
  │     └── #tactical-inspector-container (área elástica de detalhes do nó com animação max-height e overflow-y auto)
  │           └── #tactical-inspector (ficha do nó, grid de atributos, barras diplomáticas, lore, ações de ordem)
  └── #map-canvas-wrapper (flex: 1; min-height: 0; position: relative; height: 100%;)
        ├── canvas#tactical-map-canvas (redimensionado via ResizeObserver)
        ├── #map-tooltip
        └── .map-corner-widget (widgets de resumo de cantos ancorados no wrapper do mapa)
```

## 2. Componentes e Interações

### 2.1 `#tactical-top-panel`
- **Estado Normal (Sem nó selecionado)**: Exibe apenas a barra de ferramentas superior (`.tactical-top-header`) compacta e elegante. O mapa ocupa ~90% da altura.
- **Estado Detalhado (Nó selecionado)**: O container `#tactical-inspector-container` se expande com transição suave, exibindo a ficha completa do nó selecionado no topo. O mapa ocupa o espaço restante inferior sem ser obstruído.
- **Estado Colapsado**: O painel superior é reduzido a uma faixa mínima de toggle com botão "▼ Reabrir Painel / Controles", permitindo que o mapa ocupe 100% da altura da coluna tática.
- **Transição Elástica**: `transition: max-height 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease`.

### 2.2 Reatividade do Canvas (`tactical_map.js`)
- Como o `#map-canvas-wrapper` tem `ResizeObserver`, qualquer mudança de tamanho do wrapper por expansão/colapso do painel superior dispara automaticamente `this.resize()`.
- O canvas atualiza sua resolução de buffer e dimensões CSS mantendo a proporção `dpr`, e o ciclo `requestAnimationFrame` do mapa redesenha o grafo perfeitamente centrado.

### 2.3 Integração no `ui.js` e `app.js`
- `UI.showNodeInspector(node)`:
  - Remove a classe `hidden`/`collapsed` do `#tactical-top-panel` (se estiver colapsado).
  - Preenche os dados do nó no `#tactical-inspector`.
  - Abre o `#tactical-inspector-container` expandindo suavemente.
- `UI.closeNodeInspector()`:
  - Recolhe o `#tactical-inspector-container`.
  - O mapa volta a ocupar a área total restante.
- Botão de toggle `#btn-toggle-top-panel`:
  - Alterna a classe `collapsed` no `#tactical-top-panel`.
  - Atualiza o ícone e tooltip de colapsar (▲) / expandir (▼).

## 3. Estilização CSS e Glassmorphism
- Uso das variáveis existentes (`--bg-glass`, `--border-gold`, `--gold-primary`, `--radius-md`).
- Sem scrollbars invasivas: barra de rolagem customizada e suave no corpo do inspector do painel superior.
- Total compatibilidade com temas e design tokens existentes.

## 4. Testes e Validação
- Teste de renderização no navegador.
- Teste de clique em nós do grafo e verificação de redimensionamento dinâmico.
- Teste de colapso/expansão manual do painel superior.
- Execução de suite `pytest` para garantir integridade do backend e DTOs.
