# Design: [Feature Name]

## Architecture & Overview
Descreva onde a funcionalidade se posiciona na Clean Architecture do sistema.

---

## Domain Models (`engine/domain/models.py`)
Novas dataclasses ou alterações em modelos existentes.

---

## Database Changes (`engine/db/`)
- Alterações em `engine/db/schema.py` (novas tabelas, colunas).
- Novos métodos em `engine/db/repository.py` ou `engine/db/vector_store.py`.

---

## API & DTOs (`server/`)
- Novos DTOs Pydantic em `server/dto.py`.
- Novos endpoints REST em `server/app.py`.

---

## Presentation / Web (`web/`)
Alterações de interface em HTML, CSS ou módulos JavaScript (`app.js`, `ui.js`, etc.).

---

## Error Handling & Edge Cases
Tratamento de exceções, fallbacks e validações defensivas.

---

## Testing Strategy
Plano de testes unitários em `tests/` para cobrir os fluxos principais e de erro.
