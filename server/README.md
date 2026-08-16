# 🌐 Módulo Server (`server`)

O módulo `server` provê a API REST HTTP backend do jogo, desenvolvida com o framework **FastAPI**. Ele expõe todas as operações do motor de jogo para a interface Web e outros clientes, com validação de dados via Pydantic.

---

## 📂 Arquivos do Módulo

- **`app.py`**: Configuração do FastAPI, middlewares CORS, injeção de dependências, endpoints REST e roteamento de arquivos estáticos do frontend.
- **`dto.py`**: Data Transfer Objects (DTOs) com schemas Pydantic tipados para requisições e respostas.

---

## 📡 Principais Endpoints da API

### 1. Campanhas
- **`GET /api/campaigns`**: Lista todas as campanhas existentes com metadados e status mais recente.
- **`POST /api/campaigns`**: Cria uma nova campanha com raça, soberano e nome do reino.
- **`GET /api/campaigns/{id}`**: Retorna os detalhes e o último turno da campanha.
- **`DELETE /api/campaigns/{id}`**: Exclui uma campanha e limpa todos os dados associados em cascata.
- **`GET /api/campaigns/{id}/export`**: Exporta o save da campanha em formato JSON.
- **`POST /api/campaigns/import`**: Importa uma campanha a partir de um JSON estruturado.

### 2. Turnos e Ações
- **`POST /api/turns`**: Envia a decisão do jogador e processa o próximo turno com a IA.
- **`POST /api/turns/rollback`**: Reverte o jogo para um turno específico do histórico.
- **`POST /api/actions/estimate`**: Consulta a IA para estimar impactos previstos (ouro, tropas, população) de uma ação antes de executá-la.

### 3. Estado Detalhado do Reino
- **`GET /api/campaigns/{id}/state`**: Retorna os dados consolidados do reino (status, patrimônio, tarefas e diplomacia).
- **`GET /api/campaigns/{id}/items`**: Lista construções, estruturas, postos avançados e itens ativos.
- **`GET /api/campaigns/{id}/tasks`**: Lista projetos e incidentes em andamento com progresso.
- **`GET /api/campaigns/{id}/allies`**: Lista os impérios vizinhos e o status diplomático.

---

## 🚀 Como Executar o Servidor

```bash
# Executar diretamente via Uvicorn na porta 8000
uvicorn server.app:app --host 0.0.0.0 --port 8000 --reload

# Ou através do script central de execução
python run.py --server
```
Acesse a documentação interativa OpenAPI em: `http://localhost:8000/docs`
