# Project Standards & Conventions

## Code Quality & Style
1. **Python Version**: Python 3.10+.
2. **Type Annotations**: Todas as funções, métodos e classes devem ter type hints explícitos para parâmetros e retornos.
3. **Sem Comentários**: Nunca comente o código nem com `#`, `//` ou `/* */`, a menos que o usuário solicite explicitamente.
4. **Clean Code & SOLID**:
   - Princípio da Responsabilidade Única (SRP): Funções e classes devem ter uma única razão para mudar.
   - Princípio Aberto/Fechado (OCP): Estenda o comportamento via interfaces/provedores sem modificar código já testado.
   - Inversão de Dependência (DIP): Módulos de alto nível dependem de abstrações (ex: `BaseLLMProvider`).
5. **Data Transfer vs Domain**:
   - `dataclasses` para modelos de domínio (`engine/domain/models.py`).
   - Pydantic `BaseModel` exclusivamente para DTOs na camada de API (`server/dto.py`).
6. **Defensive Parsing**:
   - Valores numéricos vindos de LLMs podem conter pontuação ou texto. Sempre sanitize e converta defensivamente (ex: população, dinheiro).
   - O campo `felicidade` é sempre representado como string com porcentagem (ex: `"75%"`).
7. **Testing**:
   - Utilize `pytest` como test runner.
   - Nunca adicione testes sem necessidade, mas garanta que qualquer nova feature possua testes unitários correspondentes sem mocks desnecessários.
