# Tasks: [Feature Name]

## Checklist de Implementação

- [ ] **1. Persistência & Schema**:
  - [ ] 1.1 Atualizar `engine/db/schema.py`
  - [ ] 1.2 Implementar métodos em `engine/db/repository.py`
- [ ] **2. Domínio & Orquestração**:
  - [ ] 2.1 Criar dataclasses em `engine/domain/models.py`
  - [ ] 2.2 Implementar lógica na `GameEngine` (`engine/domain/state_manager.py`)
- [ ] **3. API & DTOs**:
  - [ ] 3.1 Criar DTOs em `server/dto.py`
  - [ ] 3.2 Criar rotas em `server/app.py`
- [ ] **4. Interface & Apresentação**:
  - [ ] 4.1 Atualizar HTML/CSS em `web/`
  - [ ] 4.2 Integrar JavaScript em `web/js/`
- [ ] **5. Testes & Qualidade**:
  - [ ] 5.1 Adicionar testes unitários em `tests/`
  - [ ] 5.2 Executar `pytest` e garantir 100% de sucesso
- [ ] **6. Documentação & Review**:
  - [ ] 6.1 Executar skill `review-consistency`
  - [ ] 6.2 Executar skill `update-docs`
  - [ ] 6.3 Mover spec para `specs/completed/`
