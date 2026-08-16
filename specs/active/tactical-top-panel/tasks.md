# Tasks: Tactical Top Canvas & Elastic Map Layout

- [ ] 1. Estruturação do HTML (`web/index.html`):
  - [ ] 1.1 Criar container `#tactical-top-panel` na raiz de `.panel-tactical`.
  - [ ] 1.2 Integrar a toolbar no cabeçalho do painel superior e adicionar botão de colapsar/expandir (`#btn-toggle-top-panel`).
  - [ ] 1.3 Alocar o container de detalhes `#tactical-inspector-container` dentro do painel superior com cabeçalho, corpo e ações.
  - [ ] 1.4 Garantir que `#map-canvas-wrapper` seja o elemento irmão inferior, contendo o canvas e tooltips.

- [ ] 2. Estilização Flexbox e Layout Elástico (`web/css/main.css` & `web/css/components.css`):
  - [ ] 2.1 Configurar `.panel-tactical` como flex vertical (`display: flex; flex-direction: column;`).
  - [ ] 2.2 Estilizar `#tactical-top-panel` com glassmorphism, suporte a estado colapsado e transição suave.
  - [ ] 2.3 Estilizar `#tactical-inspector-container` para expansão fluida (max-height animado, layout em grid responsivo de atributos e ações).
  - [ ] 2.4 Configurar `#map-canvas-wrapper` com `flex: 1; min-height: 0; position: relative;` para adaptação elástica imediata.
  - [ ] 2.5 Ajustar posicionamento das widgets de canto para ficarem confinadas na área do mapa inferior.

- [ ] 3. Ajuste de Lógica e Eventos no Frontend (`web/js/ui.js` & `web/js/app.js`):
  - [ ] 3.1 Implementar handler para `#btn-toggle-top-panel` (colapsar/reabrir painel superior).
  - [ ] 3.2 Atualizar `UI.showNodeInspector(node)` para descolapsar o painel superior e expandir a seção de detalhes.
  - [ ] 3.3 Atualizar `UI.closeNodeInspector()` para recolher a seção de detalhes e restaurar o tamanho do mapa.
  - [ ] 3.4 Garantir que `tacticalMap.resize()` seja acionado na transição e renderize o grafo perfeitamente.

- [ ] 4. Validação e Testes:
  - [ ] 4.1 Executar suíte de testes `pytest`.
  - [ ] 4.2 Validar no navegador o comportamento do mapa elástico, abertura de nós e botão de colapsar.
  - [ ] 4.3 Executar auditoria de consistência e atualizar documentação.
