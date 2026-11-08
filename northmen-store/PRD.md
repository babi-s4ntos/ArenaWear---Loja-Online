# PRD — NORTHMEN | Sistema de Gestão

## 1. Visão do produto
Sistema web responsivo para apoiar a operação de uma loja de moda masculina, centralizando catálogo, estoque por variação, vendas, clientes e indicadores gerenciais.

## 2. Objetivos
- Registrar vendas e calcular o total com desconto.
- Baixar automaticamente o estoque após uma venda.
- Controlar entradas e saídas por produto, tamanho e cor.
- Acompanhar faturamento, volume de vendas e lucro bruto estimado.
- Identificar produtos e variações com estoque baixo.

## 3. Público-alvo
Proprietário e equipe de atendimento/estoque de uma pequena ou média loja de moda masculina.

## 4. Módulos e requisitos funcionais
| Módulo | Requisitos |
|---|---|
| Dashboard | Exibir faturamento mensal, vendas do dia, lucro estimado, produtos ativos, alerta de estoque baixo e vendas recentes. |
| Produtos | Criar, listar, buscar, editar e arquivar produtos; armazenar categoria, descrição, preço, custo e imagem. |
| Estoque | Consultar quantidade por tamanho/cor; registrar entrada e saída; impedir saldo negativo. |
| Vendas | Registrar itens, cliente, desconto e forma de pagamento; validar saldo e baixar estoque automaticamente. |
| Clientes | Cadastrar e listar clientes; apresentar quantidade de compras e valor total gasto. |
| Relatórios | Listar unidades vendidas, lucro bruto por produto e variações com até três unidades. |

## 5. Regras de negócio
1. Preço de venda deve ser maior que zero; custo não pode ser negativo.
2. Quantidade movimentada e quantidade vendida devem ser inteiros positivos.
3. O estoque nunca pode ficar negativo.
4. Desconto não pode superar o subtotal da venda.
5. O lucro exibido é uma estimativa calculada pela diferença entre preço e custo cadastrados, multiplicada pelas unidades vendidas. Não considera despesas operacionais, impostos ou taxas de pagamento.
6. Exclusão de produto é lógica (arquivamento), preservando o histórico.
7. Uma venda pode ser associada a um cliente cadastrado ou registrada como cliente de balcão.

## 6. Rotas da API
| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/health` | Verificação de saúde |
| GET | `/api/dashboard` | Indicadores e vendas recentes |
| GET/POST | `/api/products` | Listar/buscar e cadastrar produtos |
| PUT/DELETE | `/api/products/{id}` | Editar e arquivar produto |
| GET | `/api/stock` | Consultar estoque por variação |
| POST | `/api/stock/movements` | Registrar entrada ou saída |
| GET/POST | `/api/customers` | Listar/buscar e cadastrar clientes |
| GET/POST | `/api/sales` | Consultar e registrar vendas |
| GET | `/api/reports` | Relatórios de produtos e estoque crítico |

## 7. Requisitos não funcionais
- Python 3.12+, FastAPI e Pydantic 2.
- Interface HTML/CSS/JavaScript responsiva.
- Persistência local com SQLite.
- Validação de dados na API e mensagens de erro compreensíveis.
- Testes de integração automatizados com Pytest e TestClient.
- Gerenciamento de dependências e execução com uv.

## 8. Fora do escopo inicial
Integração com marketplaces, emissão fiscal, leitor de código de barras, gateway real de pagamento, autenticação multiusuário, upload de imagens para nuvem e sincronização entre filiais.

## 9. Critérios de aceite
- CRUD de produtos funciona.
- Entradas/saídas atualizam a quantidade correta.
- Venda válida registra total e reduz o estoque.
- Venda sem saldo ou com desconto inválido é recusada.
- Dashboard e relatórios refletem os dados persistidos.
- Testes de integração passam com `uv run pytest`.

## Expansão — Loja virtual integrada (novembro/2026)

### Objetivo
Disponibilizar uma vitrine NORTHMEN responsiva para clientes, integrada ao mesmo FastAPI/SQLite do painel administrativo, preservando o sistema de gestão já existente.

### Experiência do cliente
- Página inicial editorial, catálogo pesquisável e filtro por categoria.
- Detalhe de produto com variações de tamanho/cor e saldo de estoque por variação.
- Sacola no navegador, atualização de quantidade, remoção e subtotal.
- Cadastro, login, sessão assinada e área de conta com histórico de pedidos.
- Checkout com endereço, CEP, cotação Melhor Envio e escolha de serviço.
- Checkout Pro Mercado Pago com Pix/cartão; pagamento na entrega como alternativa operacional.

### Pedidos e integração
O backend recalcula subtotal e estoque no SQLite, cota frete no Melhor Envio e valida a modalidade escolhida no servidor. O pagamento online é iniciado por preferência criada no backend. O webhook do Mercado Pago tem assinatura HMAC validada e o pagamento é consultado diretamente no gateway antes de aprovar pedido. A aprovação cria venda e itens e baixa o estoque dentro da operação SQLite. Pedido na entrega pode ser aprovado pelo administrador após confirmação operacional.

### Segurança e limites
- A loja pública recebe apenas campos comerciais, sem custo ou lucro.
- Cadastro/login usa hash PBKDF2-HMAC-SHA256 com salt aleatório.
- Rotas administrativas e APIs internas exigem HTTP Basic configurável por variáveis de ambiente.
- Tokens de cliente são assinados e expiram em sete dias.
- Segredos são lidos de `.env`/ambiente; `.env.example` contém apenas marcadores.
- Em `APP_ENV=production`, a inicialização exige credenciais e URL HTTPS.
- O retorno do navegador não confirma pagamento; somente webhook assinado + consulta ao gateway.

### Rotas
Ver tabela completa no README. Rotas novas sob `/api/store`; rotas administrativas existentes continuam disponíveis e protegidas.

### Dependências operacionais ainda externas
A ativação real depende de conta/token do Mercado Pago, assinatura de webhook, token e cadastro de remetente Melhor Envio, domínio, hospedagem HTTPS, dados comerciais/fiscais e configuração de privacidade. A cotação de frete está integrada; compra de etiqueta/rastreamento automático e emissão fiscal exigem etapas adicionais da conta logística/fiscal.
