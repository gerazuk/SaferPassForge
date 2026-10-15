# Registro Histórico de Prompts — SaferPassForge 📋

> **Auditoria e Rastreabilidade do Desenvolvimento Assistido por Inteligência Artificial**  
> *Projeto acadêmico no âmbito da Especialização em Engenharia de Software (2026).*

---

## 1. Visão Geral e Metodologia

Este documento registra integralmente a sequência de prompts submetidos durante todo o ciclo de vida de desenvolvimento (SDLC) do **SaferPassForge**.

### Pilares Metodológicos:
- **Engenharia de Prompt Estruturada (CO-STAR)**: Os prompts principais das etapas do SDLC foram concebidos com a metodologia CO-STAR (*Context, Objective, Style, Tone, Audience, Response*) gerados via **Gemini 4 Argon** (Nível Máximo de Detalhe).
- **Pair Programming e Implementação Autônoma**: A execução técnica, criação dos arquivos, resolução de dependências, implementação dos algoritmos CSPRNG, testes e comandos Git foram conduzidos no **VS Code + Antigravity com Gemini 3.8 Flash**.

---

## 2. Índice Cronológico dos Prompts

| # | Fase / Categoria | Descrição Sumária | Timestamp (UTC) |
| :-: | :--- | :--- | :--- |
| **01** | Configuração de Ambiente | Dúvida sobre sintaxe heredoc em PowerShell | 2026-10-15T01:30:16Z |
| **02** | Configuração de Ambiente | Criação do arquivo .env inicial | 2026-10-15T01:31:36Z |
| **03** | SDLC 1 - Governança & Setup | Criação de AGENTS.md, .gitignore, .env.example, LICENSE, requirements.txt e app/config.py | 2026-10-15T01:32:29Z |
| **04** | Git & Dependências | Instalação de dependências e primeiro commit de governança | 2026-10-15T01:37:34Z |
| **05** | Engenharia de Software | Validação sobre versionamento da pasta de testes | 2026-10-15T01:40:59Z |
| **06** | Git & Versionamento | Configuração de identidade e push inicial para o GitHub | 2026-10-15T01:45:25Z |
| **07** | SDLC 2 - Domínio & Regras de Negócio | Modelagem do domínio: PasswordGeneratorService, EntropyCalculator e schemas Pydantic v2 | 2026-10-15T01:48:09Z |
| **08** | Git & Versionamento | Commit da camada de domínio (app/domain) | 2026-10-15T01:50:16Z |
| **09** | SDLC 3 - Persistência de Dados | Modelagem da infraestrutura: SQLAlchemy 2.0, PasswordAuditLog e PasswordAuditRepository | 2026-10-15T01:51:57Z |
| **10** | Git & Versionamento | Commit da camada de infraestrutura (app/infrastructure) | 2026-10-15T01:54:15Z |
| **11** | SDLC 4 - API & Interface Web | Criação das rotas RESTful FastAPI, index.html em Tailwind CSS e app.js | 2026-10-15T01:55:29Z |
| **12** | Troubleshooting & Execução | Diagnóstico de conexão recusada no Uvicorn | 2026-10-15T02:01:43Z |
| **13** | Git & Versionamento | Commit da camada de apresentação (app/api, app/static, app/main.py) | 2026-10-15T02:05:48Z |
| **14** | SDLC 5 - QA & Testes Automatizados | Criação da suíte de testes com conftest.py, test_generator.py e test_api.py (AAA) | 2026-10-15T02:06:35Z |
| **15** | QA & Verificação | Execução da bateria de testes com pytest -v | 2026-10-15T02:09:01Z |
| **16** | Git & Versionamento | Commit da suíte de testes (tests/) | 2026-10-15T02:09:25Z |
| **17** | SDLC 6 - Documentação | Elaboração do README.md completo com diagramas Mermaid.js | 2026-10-15T02:10:37Z |
| **18** | Git & Versionamento | Commit do README.md | 2026-10-15T02:13:24Z |
| **19** | Revisão de Qualidade | Revisão e validação do requirements.txt para novos usuários | 2026-10-15T02:16:29Z |
| **20** | Conformidade Jurídica | Verificação do texto da licença MIT | 2026-10-15T02:24:06Z |
| **21** | Entrega & Versionamento | Consulta sobre existência de Release/Tag v1.0.0 | 2026-10-15T22:58:45Z |
| **22** | Entrega & Versionamento | Criação e publicação da Tag anotada v1.0.0 no GitHub | 2026-10-15T23:04:47Z |
| **23** | Documentação & IA | Solicitação de inclusão das ferramentas de IA utilizadas no README.md | 2026-10-15T23:16:10Z |
| **24** | Git & Versionamento | Confirmação para comitar, enviar e atualizar tag v1.0.0 | 2026-10-15T23:18:04Z |
| **25** | Auditoria & Rastreabilidade | Solicitação de criação do log de prompts do projeto | 2026-10-15T23:24:15Z |

---

## 3. Detalhamento dos Prompts

### Prompt 01 — Dúvida sobre sintaxe heredoc em PowerShell
- **Fase do SDLC / Contexto**: Configuração de Ambiente
- **Timestamp UTC**: 2026-10-15T01:30:16Z

`markdown
Por que está dando erro quando executo o comando: cat << 'EOF' > .env
"Especificação de arquivo ausente após o operador de redirecionamento."
`

---

### Prompt 02 — Criação do arquivo .env inicial
- **Fase do SDLC / Contexto**: Configuração de Ambiente
- **Timestamp UTC**: 2026-10-15T01:31:36Z

`markdown
Criar o arquivo .env com o setuinte conteudo:
APP_NAME="SaferPassForge"
APP_ENV="development"
APP_SECRET_KEY="chave-secreta-local-gerada-com-alta-entropia-nao-versionar"
DATABASE_URL="sqlite:///./saferpassforge.db"
DEFAULT_PASSWORD_LENGTH=16
EOF
`

---

### Prompt 03 — Criação de AGENTS.md, .gitignore, .env.example, LICENSE, requirements.txt e app/config.py
- **Fase do SDLC / Contexto**: SDLC 1 - Governança & Setup
- **Timestamp UTC**: 2026-10-15T01:32:29Z

`markdown
# [C] Context (Contexto)
Estou iniciando o projeto MVP "SaferPassForge", um gerador de senhas criptograficamente seguras com auditoria de entropia, desenvolvido como projeto de Especialização em Engenharia de Software. O sistema usará Python 3.11+, FastAPI, SQLite (SQLAlchemy) e interface web integrada. Antes de escrever o código de negócio, precisamos estabelecer a governança do repositório, o arquivo AGENTS.md, o gerenciamento de dependências, a licença e o carregamento seguro de variáveis de ambiente.

# [O] Objective (Objetivo)
Criar a estrutura inicial de diretórios e os seguintes arquivos na raiz e no pacote `app/`:
1. `AGENTS.md`: Diretrizes estritas para agentes de IA contendo:
   - Comandos oficiais do projeto (instalação, execução do servidor Uvicorn, execução do Pytest).
   - Princípios obrigatórios de Engenharia de Código aplicados ao projeto:
     * KISS (Keep It Simple, Stupid): Soluções diretas, sem over-engineering.
     * YAGNI (You Aren't Gonna Need It): Implementar apenas o escopo do MVP sem dependências ociosas.
     * DRY (Don't Repeat Yourself): Centralizar validações, configurações e cálculos de entropia.
     * SOLID: Separação clara entre domínio (`app/domain`), infraestrutura (`app/infrastructure`) e apresentação (`app/api`), com inversão de dependência via `Depends` do FastAPI.
   - Regra estrita de Git: "Conventional Commits One-Liner" (formato `tipo(escopo): descrição concisa em uma única linha, em inglês, letras minúsculas, sem ponto final e no máximo 72 caracteres`).
   - Regra de Segurança: Proibição absoluta de chaves, senhas ou segredos hardcoded no código ou histórico Git; tudo deve vir de variáveis de ambiente via `.env`.
2. `.gitignore`: Configurado para Python (`.venv/`, `__pycache__/`, `.pytest_cache/`, `*.pyc`), banco SQLite (`*.db`, `*.sqlite3`), arquivos temporários de IDE (`.vscode/`, `.idea/`, `.DS_Store`) e estritamente arquivos de ambiente (`.env`, `.env.*`, exceto `!.env.example`).
3. `.env.example`: Template seguro documentando `APP_NAME`, `APP_ENV`, `APP_SECRET_KEY`, `DATABASE_URL` e `DEFAULT_PASSWORD_LENGTH`.
4. `LICENSE`: Texto completo da licença MIT para o ano atual.
5. `requirements.txt`: Dependências com versões fixadas (`fastapi`, `uvicorn[standard]`, `sqlalchemy`, `pydantic`, `pydantic-settings`, `python-dotenv`, `pytest`, `httpx`).
6. `app/__init__.py` e `app/config.py`: Módulo utilizando `pydantic-settings` (`BaseSettings`) para carregar e validar as variáveis do `.env` de forma tipada e centralizada (DRY).

# [S] Style (Estilo)
Clean Code, modular, aderente à PEP 8, com tipagem estática (Type Hints) em todo código Python e Markdown técnico estruturado.

# [T] Tone (Tom)
Profissional, objetivo, focado em segurança (Security-by-Design) e rigor acadêmico.

# [A] Audience (Audiência)
Avaliadores da Especialização em Engenharia de Software e desenvolvedores seniores revisando o repositório no GitHub.

# [R] Response (Formato de Resposta)
Gere todos os arquivos solicitados diretamente no workspace e exiba no final um resumo curto da árvore de arquivos criada.
`

---

### Prompt 04 — Instalação de dependências e primeiro commit de governança
- **Fase do SDLC / Contexto**: Git & Dependências
- **Timestamp UTC**: 2026-10-15T01:37:34Z

`markdown
Executar:
pip install -r requirements.txt
git status
git add AGENTS.md .gitignore .env.example LICENSE requirements.txt app/
git commit -m "chore: initialize project governance, AGENTS.md, license, and env setup"
`

---

### Prompt 05 — Validação sobre versionamento da pasta de testes
- **Fase do SDLC / Contexto**: Engenharia de Software
- **Timestamp UTC**: 2026-10-15T01:40:59Z

`markdown
É correto fazer o commit da pasta testes e seu conteudo?
`

---

### Prompt 06 — Configuração de identidade e push inicial para o GitHub
- **Fase do SDLC / Contexto**: Git & Versionamento
- **Timestamp UTC**: 2026-10-15T01:45:25Z

`markdown
Fazer o commit para meu repositorio publico: https://github.com/gerazuk/SaferPassForge.git
`

---

### Prompt 07 — Modelagem do domínio: PasswordGeneratorService, EntropyCalculator e schemas Pydantic v2
- **Fase do SDLC / Contexto**: SDLC 2 - Domínio & Regras de Negócio
- **Timestamp UTC**: 2026-10-15T01:48:09Z

`markdown
# [C] Context (Contexto)
Com a fundação e o `AGENTS.md` configurados no projeto "SaferPassForge", estamos na fase de Modelagem de Domínio e Regras de Negócio do SDLC. Precisamos construir o motor de geração de senhas e cálculo de entropia seguindo estritamente as diretrizes do `AGENTS.md` (KISS, YAGNI, DRY e SOLID - especialmente Single Responsibility Principle e Open/Closed Principle).

# [O] Objective (Objetivo)
Criar a camada de domínio em `app/domain/`:
1. `app/domain/__init__.py`
2. `app/domain/schemas.py`: Modelos Pydantic v2 para entrada e saída:
   - `PasswordGenerateRequest`: `length` (int, entre 8 e 128, padrão vindo da config), `use_uppercase` (bool), `use_lowercase` (bool), `use_digits` (bool), `use_symbols` (bool), `exclude_ambiguous` (bool, ex: `l`, `1`, `I`, `O`, `0`), e `context_label` (str opcional, ex: "GitHub", "Banco", máx 50 chars). Validar que pelo menos um grupo de caracteres esteja ativo.
   - `PasswordStrengthResponse`: `password` (str), `length` (int), `entropy_bits` (float), `strength_category` (Literal["Weak", "Fair", "Strong", "Very Strong"]), `masked_preview` (str, ex: `aB******9!`), `context_label` (Optional[str]), `created_at` (datetime).
   - `PasswordAuditItem`: Esquema de leitura do histórico de auditoria (sem expor a senha completa em texto puro, exibindo apenas `id`, `context_label`, `length`, `entropy_bits`, `strength_category`, `masked_preview` e `created_at`).
3. `app/domain/services.py`:
   - Classe `EntropyCalculator`: Calcula os bits de entropia reais usando a fórmula $E = L \times \log_2(R)$ (onde $L$ é o comprimento e $R$ o tamanho do pool de caracteres utilizado) e classifica a força da senha.
   - Classe `PasswordGeneratorService`: Utiliza exclusivamente a biblioteca padrão `secrets` (CSPRNG) do Python (nunca `random`) para gerar a senha garantindo a presença de ao menos um caractere de cada categoria selecionada pelo usuário, embaralhando o resultado de forma criptograficamente segura e gerando a máscara de visualização (`masked_preview`).

# [S] Style (Estilo)
Pythonico, orientado a objetos com responsabilidade única (SRP), funções puras quando aplicável, Type Hints completos e docstrings concisas.

# [T] Tone (Tom)
Técnico, preciso e orientado a boas práticas de criptografia aplicada.

# [A] Audience (Audiência)
Engenheiros de software e auditores de segurança avaliando a qualidade algorítmica do gerador.

# [R] Response (Formato de Resposta)
Crie os arquivos em `app/domain/` sem adicionar dependências externas desnecessárias (YAGNI) e confirme a criação.
`

---

### Prompt 08 — Commit da camada de domínio (app/domain)
- **Fase do SDLC / Contexto**: Git & Versionamento
- **Timestamp UTC**: 2026-10-15T01:50:16Z

`markdown
Executar:
git status
git add app/domain/
git commit -m "feat(core): implement cryptographic password generator and entropy calculator"
`

---

### Prompt 09 — Modelagem da infraestrutura: SQLAlchemy 2.0, PasswordAuditLog e PasswordAuditRepository
- **Fase do SDLC / Contexto**: SDLC 3 - Persistência de Dados
- **Timestamp UTC**: 2026-10-15T01:51:57Z

`markdown
# [C] Context (Contexto)
Já possuímos a configuração (`app/config.py`) e o domínio (`app/domain/`) do "SaferPassForge". Agora estamos na etapa de Persistência de Dados do SDLC. Para manter um gerador de senhas verdadeiramente seguro (Security-by-Design), o banco de dados persistirá o histórico de auditoria das senhas geradas (rótulo de contexto, comprimento, bits de entropia, classificação de força, máscara parcial e hash SHA-256 com salt da chave secreta da aplicação para verificação de unicidade), jamais salvando a senha em texto puro no disco.

# [O] Objective (Objetivo)
Criar a camada de infraestrutura em `app/infrastructure/`:
1. `app/infrastructure/__init__.py`
2. `app/infrastructure/database.py`: Configuração do engine SQLAlchemy 2.0 consumindo `settings.DATABASE_URL`, `SessionLocal`, classe `Base` declarativa e o gerador de dependência `get_db()`.
3. `app/infrastructure/models.py`: Modelo ORM `PasswordAuditLog` mapeando a tabela `password_audit_logs` com os campos: `id` (Integer PK), `context_label` (String), `length` (Integer), `entropy_bits` (Float), `strength_category` (String), `masked_preview` (String), `password_hash` (String, HMAC-SHA256 usando `APP_SECRET_KEY` do `.env`), e `created_at` (DateTime UTC).
4. `app/infrastructure/repository.py`: Classe `PasswordAuditRepository` aplicando o padrão Repository (SOLID - Dependency Inversion) com métodos para:
   - `create_log(...)`: Registra uma geração de senha no SQLite.
   - `list_recent_logs(limit: int = 10)`: Retorna os últimos registros ordenados do mais recente para o mais antigo.
   - `clear_logs()`: Limpa o histórico de auditoria.

# [S] Style (Estilo)
SQLAlchemy 2.0 moderno, código enxuto (KISS), sem duplicação de conexão (DRY) e desacoplado da camada HTTP.

# [T] Tone (Tom)
Objetivo, seguro e alinhado à arquitetura limpa.

# [A] Audience (Audiência)
Avaliadores de arquitetura de software e banco de dados.

# [R] Response (Formato de Resposta)
Gere os arquivos no diretório `app/infrastructure/` prontos para integração com o FastAPI.
`

---

### Prompt 10 — Commit da camada de infraestrutura (app/infrastructure)
- **Fase do SDLC / Contexto**: Git & Versionamento
- **Timestamp UTC**: 2026-10-15T01:54:15Z

`markdown
Executar:
git status
git add app/infrastructure/
git commit -m "feat(db): add sqlite persistence layer for password generation audit logs"
`

---

### Prompt 11 — Criação das rotas RESTful FastAPI, index.html em Tailwind CSS e app.js
- **Fase do SDLC / Contexto**: SDLC 4 - API & Interface Web
- **Timestamp UTC**: 2026-10-15T01:55:29Z

`markdown
# [C] Context (Contexto)
No projeto "SaferPassForge", as camadas de domínio e persistência SQLite estão prontas. Estamos na etapa de Integração de API e Interface de Usuário do SDLC. Precisamos expor os recursos via FastAPI e entregar uma interface web limpa, responsiva e intuitiva diretamente integrada à aplicação.

# [O] Objective (Objetivo)
Criar a camada de apresentação e interface web:
1. `app/api/__init__.py` e `app/api/routes.py`:
   - `GET /api/v1/health`: Healthcheck retornando status e ambiente.
   - `POST /api/v1/passwords/generate`: Recebe `PasswordGenerateRequest`, gera a senha via `PasswordGeneratorService`, persiste o registro de auditoria no SQLite via `PasswordAuditRepository` e retorna `PasswordStrengthResponse` (status 201).
   - `GET /api/v1/passwords/history`: Retorna ` list[PasswordAuditItem]` com os últimos registros persistidos no banco.
   - `DELETE /api/v1/passwords/history`: Limpa o histórico de auditoria (status 204).
2. `app/static/index.html` e `app/static/app.js`:
   - Interface web moderna (utilizando Tailwind CSS via CDN para manter o projeto KISS/YAGNI sem exigir Node.js) com tema escuro elegante.
   - Controles interativos: Slider de comprimento (8 a 64), checkboxes para Maiúsculas, Minúsculas, Números, Símbolos e Exclusão de Ambíguos, além de campo opcional para "Contexto/Serviço" (ex: AWS, E-mail).
   - Exibição da senha gerada com botão "Copiar para Área de Transferência" (com feedback visual), barra de progresso dinâmica de Entropia/Força e tabela de "Histórico de Auditoria Persistido" atualizada automaticamente via Fetch API, incluindo botão de limpar histórico.
3. `app/main.py`: Inicialização do FastAPI, criação automática das tabelas no startup (`lifespan`), inclusão das rotas da API e montagem da interface web na rota raiz `/` e arquivos estáticos em `/static`.

# [S] Style (Estilo)
RESTful nas rotas FastAPI (com injeção de dependência `Depends`), HTML5 semântico e JavaScript moderno (`async/await`) limpo e bem estruturado.

# [T] Tone (Tom)
Prático, focado em experiência do usuário (UX) e boas práticas de engenharia web.

# [A] Audience (Audiência)
Usuários finais testando a aplicação no navegador e avaliadores inspecionando o Swagger (`/docs`).

# [R] Response (Formato de Resposta)
Gere os arquivos em `app/api/`, `app/static/` e `app/main.py`.
`

---

### Prompt 12 — Diagnóstico de conexão recusada no Uvicorn
- **Fase do SDLC / Contexto**: Troubleshooting & Execução
- **Timestamp UTC**: 2026-10-15T02:01:43Z

`markdown
Executei o comando uvicorn app.main:app --reload para testar a interface e recebi o erro:
Failed to Load Page
ERR_CONNECTION_REFUSED (-102)
URL: http://127.0.0.1:8000/
O que há de errado?
`

---

### Prompt 13 — Commit da camada de apresentação (app/api, app/static, app/main.py)
- **Fase do SDLC / Contexto**: Git & Versionamento
- **Timestamp UTC**: 2026-10-15T02:05:48Z

`markdown
Executar:
git status
git add app/api/ app/static/ app/main.py
git commit -m "feat(api,ui): build FastAPI endpoints and interactive web interface"
`

---

### Prompt 14 — Criação da suíte de testes com conftest.py, test_generator.py e test_api.py (AAA)
- **Fase do SDLC / Contexto**: SDLC 5 - QA & Testes Automatizados
- **Timestamp UTC**: 2026-10-15T02:06:35Z

`markdown
# [C] Context (Contexto)
O MVP do "SaferPassForge" está funcional com domínio, banco SQLite, API FastAPI e interface web. Agora estamos no estágio de Garantia de Qualidade (QA) e Testes Automatizados do SDLC. Todos os testes devem rodar de forma isolada, rápida e determinística, sem sujar o banco de dados local de desenvolvimento.

# [O] Objective (Objetivo)
Criar a suíte de testes automatizados no diretório `tests/`:
1. `tests/__init__.py`
2. `tests/conftest.py`: Configuração de fixtures do `pytest`, criando um banco SQLite em memória (`sqlite:///:memory:` com `StaticPool`) e sobrescrevendo a dependência `get_db` do FastAPI via `app.dependency_overrides` para fornecer um `TestClient` totalmente isolado.
3. `tests/test_generator.py`: Testes unitários cobrindo:
   - Respeito exato ao comprimento solicitado.
   - Inclusão obrigatória das categorias de caracteres selecionadas.
   - Funcionamento do filtro `exclude_ambiguous` (garantindo ausência de `l`, `1`, `I`, `O`, `0`).
   - Cálculo matemático correto de bits de entropia e classificação de força.
   - Erro de validação quando nenhum grupo de caracteres é selecionado.
4. `tests/test_api.py`: Testes de integração cobrindo:
   - `GET /api/v1/health` retornando 200 OK.
   - `POST /api/v1/passwords/generate` retornando 201, validando payload e verificando que a senha retornada não é salva em texto puro no histórico.
   - `GET /api/v1/passwords/history` comprovando a persistência no banco de dados.
   - `DELETE /api/v1/passwords/history` comprovando a limpeza dos registros.
   - `GET /` servindo a interface web HTML com sucesso.

# [S] Style (Estilo)
Padrão AAA (Arrange, Act, Assert), nomes de funções descritivos (`test_should_...`), aderente ao DRY através do uso de fixtures no `conftest.py`.

# [T] Tone (Tom)
Rigoroso e orientado à confiabilidade de software.

# [A] Audience (Audiência)
Engenheiros de QA e avaliadores acadêmicos que executarão o comando `pytest` ao clonar o repositório.

# [R] Response (Formato de Resposta)
Crie os arquivos em `tests/` e execute a bateria de testes via terminal para comprovar 100% de aprovação.
`

---

### Prompt 15 — Execução da bateria de testes com pytest -v
- **Fase do SDLC / Contexto**: QA & Verificação
- **Timestamp UTC**: 2026-10-15T02:09:01Z

`markdown
Executar:
pytest -v
`

---

### Prompt 16 — Commit da suíte de testes (tests/)
- **Fase do SDLC / Contexto**: Git & Versionamento
- **Timestamp UTC**: 2026-10-15T02:09:25Z

`markdown
Executar:
git status
git add tests/
git commit -m "test: add unit and integration test suites with pytest"
`

---

### Prompt 17 — Elaboração do README.md completo com diagramas Mermaid.js
- **Fase do SDLC / Contexto**: SDLC 6 - Documentação
- **Timestamp UTC**: 2026-10-15T02:10:37Z

`markdown
# [C] Context (Contexto)
Estamos na etapa final de Documentação e Entrega do SDLC do projeto "SaferPassForge". Todos os requisitos de código, segurança de variáveis de ambiente, persistência SQLite, interface web e testes automatizados estão prontos. Agora precisamos de um `README.md` completo, executivo e acadêmico que documente todo o projeto e sua arquitetura utilizando diagramas `Mermaid.js`.

# [O] Objective (Objetivo)
Criar o arquivo `README.md` na raiz do projeto contendo:
1. **Cabeçalho e Badges**: Título "SaferPassForge", descrição executiva e badges (Python, FastAPI, SQLite, Pytest, License: MIT, Conventional Commits).
2. **Sobre o Projeto e Estágios do SDLC**: Explicação de como o MVP explora cada fase do ciclo de vida (Requisitos/Governança com IA, Design e Domínio, Persistência Segura, API/UI, Testes Automatizados e Documentação).
3. **Princípios de Engenharia Aplicados**: Seção detalhando exatamente onde e como **KISS**, **YAGNI**, **DRY** e **SOLID** foram implementados no código do SaferPassForge.
4. **Arquitetura do Sistema (Mermaid.js)**:
   - Um **Diagrama de Componentes (Arquitetura em Camadas)** em bloco `mermaid` (`graph TD` ou `flowchart LR`) demonstrando o fluxo entre Interface Web, FastAPI Router, Domain Services (`PasswordGeneratorService`, `EntropyCalculator`), Repository Pattern e SQLite.
   - Um **Diagrama de Sequência** em bloco `mermaid` (`sequenceDiagram`) detalhando o fluxo completo de geração de senha, cálculo de entropia, hashing HMAC-SHA256 com `APP_SECRET_KEY` e gravação do log de auditoria no SQLite.
5. **Estrutura de Diretórios**: Árvore visual limpa dos arquivos do repositório.
6. **Configuração de Variáveis de Ambiente e Segurança**: Explicação do uso do `.env` baseado no `.env.example` e garantia de ausência de credenciais no histórico Git.
7. **Como Executar o Projeto (Passo a Passo)**: Comandos de clone, criação da `venv`, `pip install -r requirements.txt`, configuração do `.env` e inicialização com `uvicorn app.main:app --reload` (incluindo links para a Web UI em `http://localhost:8000` e Swagger em `http://localhost:8000/docs`).
8. **Como Executar os Testes Automatizados**: Comandos para rodar `pytest -v` e o que cada suíte valida.
9. **Governança com Agentes de IA (`AGENTS.md`) e Licença**: Referência ao arquivo `AGENTS.md` e à licença MIT (`LICENSE`).

# [S] Style (Estilo)
Markdown rico, escaneável, com tabelas bem formatadas, blocos de código copiáveis e diagramas Mermaid sintaticamente válidos para renderização nativa no GitHub.

# [T] Tone (Tom)
Acadêmico, técnico e altamente profissional.

# [A] Audience (Audiência)
Banca avaliadora da Especialização em Engenharia de Software e comunidade open-source no GitHub.

# [R] Response (Formato de Resposta)
Gere o arquivo `README.md` completo na raiz do projeto.
`

---

### Prompt 18 — Commit do README.md
- **Fase do SDLC / Contexto**: Git & Versionamento
- **Timestamp UTC**: 2026-10-15T02:13:24Z

`markdown
executar:
git status
git add README.md
git commit -m "docs: add comprehensive README with Mermaid architecture diagrams"
`

---

### Prompt 19 — Revisão e validação do requirements.txt para novos usuários
- **Fase do SDLC / Contexto**: Revisão de Qualidade
- **Timestamp UTC**: 2026-10-15T02:16:29Z

`markdown
Revisar se o arquivo requirements está de acordo para um usuario executar o projeto
`

---

### Prompt 20 — Verificação do texto da licença MIT
- **Fase do SDLC / Contexto**: Conformidade Jurídica
- **Timestamp UTC**: 2026-10-15T02:24:06Z

`markdown
A licença esta correta?
`

---

### Prompt 21 — Consulta sobre existência de Release/Tag v1.0.0
- **Fase do SDLC / Contexto**: Entrega & Versionamento
- **Timestamp UTC**: 2026-10-15T22:58:45Z

`markdown
Release ou Tag: Uma Release ou Tag (ex: v1.0.0) foi criada no GitHub® para marcar a versão final do projeto? Isso facilita a identificação da versão submetida.
`

---

### Prompt 22 — Criação e publicação da Tag anotada v1.0.0 no GitHub
- **Fase do SDLC / Contexto**: Entrega & Versionamento
- **Timestamp UTC**: 2026-10-15T23:04:47Z

`markdown
Criar e publicar a Tag v1.0.0
`

---

### Prompt 23 — Solicitação de inclusão das ferramentas de IA utilizadas no README.md
- **Fase do SDLC / Contexto**: Documentação & IA
- **Timestamp UTC**: 2026-10-15T23:16:10Z

`markdown
Adicionar no README.MD uma seção citando as IAs utilizadas no projeto, exemplo:
1- AI Gemini 4 Argon - Nível detalhe Máximo : Prompt inicial que geraram os prompts de implementação no padrão CO-STAR.
2- VS Code + Antigravity com Gemini 3.8 Flash Nível Médio : Implementação do projeto
`

---

### Prompt 24 — Confirmação para comitar, enviar e atualizar tag v1.0.0
- **Fase do SDLC / Contexto**: Git & Versionamento
- **Timestamp UTC**: 2026-10-15T23:18:04Z

`markdown
Sim, eu quero que você execute
`

---

### Prompt 25 — Solicitação de criação do log de prompts do projeto
- **Fase do SDLC / Contexto**: Auditoria & Rastreabilidade
- **Timestamp UTC**: 2026-10-15T23:24:15Z

`markdown
Criar um arquivo com o log dos prompts utilizados no projeto.
`

---
