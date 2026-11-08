# NORTHMEN — Loja virtual + painel administrativo

E-commerce NORTHMEN integrado ao sistema de gestão existente (FastAPI + SQLite). O painel original permanece em `app/static/index.html`; a loja pública fica em `app/static/store/`.

## Requisitos
- Python 3.12+
- `uv`
- Conta de vendedor Mercado Pago e aplicativo de integração
- Conta/aplicativo Melhor Envio com token de API
- Hospedagem com HTTPS e domínio público para webhooks de pagamento

## Instalação local (PowerShell)
```powershell
# Entre na pasta que contém pyproject.toml
uv sync --extra dev
Copy-Item .env.example .env
# Edite .env para configurar as chaves e dados da loja
uv run uvicorn app.main:app --reload
```
URLs locais: loja `http://127.0.0.1:8000/`, painel `http://127.0.0.1:8000/admin`, documentação `http://127.0.0.1:8000/docs`.

Para desenvolvimento, `SEED_DEMO_DATA=true` cria produtos de demonstração se o banco estiver vazio. Em produção, use `APP_ENV=production` e `SEED_DEMO_DATA=false`; cadastre os produtos reais no painel. O banco existente é migrado com `ALTER TABLE` aditivo, sem apagar as tabelas administrativas.

## Configuração das integrações
Copie `.env.example` para `.env`. O arquivo `.env` está no `.gitignore`; nunca envie tokens para o Git ou para conversas.

### Mercado Pago — Pix e cartão
1. Crie uma aplicação em [Mercado Pago Developers](https://www.mercadopago.com.br/developers/pt).
2. Configure `MERCADOPAGO_ACCESS_TOKEN` no ambiente.
3. Em Webhooks, cadastre `https://SEU_DOMINIO/api/store/payments/mercadopago/webhook`, habilite eventos de pagamento e copie a assinatura secreta para `MERCADOPAGO_WEBHOOK_SECRET`.
4. Configure `PUBLIC_BASE_URL=https://SEU_DOMINIO`.
5. Teste primeiro com credenciais/ambiente de teste; só depois altere o ambiente do gateway para produção.

O backend cria a preferência no servidor, envia o cliente ao Checkout Pro e só registra venda/baixa de estoque após receber webhook com assinatura válida e consultar o pagamento diretamente na API do Mercado Pago. O retorno do navegador não aprova pedidos.

### Melhor Envio — cotação
1. Crie/autorize o aplicativo no Melhor Envio e gere o token de API.
2. Configure `MELHORENVIO_TOKEN`, `STORE_ORIGIN_CEP`, `STORE_USER_AGENT` e as dimensões/peso padrão do pacote.
3. Comece com `MELHORENVIO_ENV=sandbox`; use `production` apenas depois de validar a conta e o contrato.

O servidor calcula o frete com dados dos produtos e CEP, e recalcula a cotação no momento da criação do pedido. Não aceita preço de frete informado pelo navegador. A emissão/compra de etiqueta e rastreamento automático ainda dependem da configuração logística/remetente e do fluxo de contratação da conta; o painel pode registrar código de rastreio manualmente via API administrativa.

## Operação e rotas
- `/`: loja
- `/admin`: painel administrativo (HTTP Basic)
- `/api/health`: saúde e sinalizadores de configuração, sem expor segredos
- `/api/store/products`, `/api/store/products/{id}`: catálogo público
- `/api/store/register`, `/api/store/login`, `/api/store/me`: conta do cliente
- `/api/store/shipping/quote`: cotação Melhor Envio
- `/api/store/orders`, `/api/store/orders` (GET): criar e consultar pedidos autenticados
- `/api/store/payments/mercadopago/webhook`: webhook público validado por HMAC
- `/api/store/admin/orders`: pedidos no painel
- `/api/store/admin/orders/{id}/approve|cancel`: gestão administrativa
- `PUT /api/store/admin/orders/{id}/tracking`: registrar código de rastreio

Pedidos via Mercado Pago não podem ser aprovados manualmente antes da confirmação do gateway. Pedidos com pagamento na entrega dependem da confirmação operacional da loja. O estoque é baixado apenas na aprovação, com nova validação de saldo.

## Produção — checklist obrigatório
- [ ] Domínio próprio apontado para hospedagem e HTTPS válido.
- [ ] `APP_ENV=production`, `SEED_DEMO_DATA=false` e todos os segredos preenchidos.
- [ ] `ADMIN_USERNAME` e `ADMIN_PASSWORD` fortes e exclusivos.
- [ ] `STORE_SECRET` aleatório com pelo menos 32 caracteres.
- [ ] `PUBLIC_BASE_URL` usando HTTPS.
- [ ] Access Token e assinatura de webhook do Mercado Pago configurados no modo correto.
- [ ] Token Melhor Envio, CEP de origem, peso e dimensões reais configurados.
- [ ] Produtos reais, fotos, preços, variações e estoque conferidos.
- [ ] Política de privacidade, termos, trocas/devoluções, prazos, contato e informações fiscais publicados.
- [ ] Backup automático do SQLite, monitoramento, logs e política de retenção de dados configurados.
- [ ] Testes de compra com credenciais de teste e validação final com valores baixos em produção.

A aplicação bloqueia a inicialização em modo de produção se faltarem variáveis essenciais. O ambiente de execução/host, DNS, certificado TLS e contas externas são provisionados fora do código e precisam ser configurados pelo titular.

## Testes
```powershell
uv run pytest
node --check app/static/store/assets/js/store.js
```

## Segurança
- Senhas de clientes derivadas com PBKDF2-HMAC-SHA256 e salt aleatório.
- Token de cliente assinado e com expiração de sete dias.
- APIs administrativas protegidas por HTTP Basic.
- APIs públicas não retornam custo, lucro ou dados de terceiros.
- Preços, estoque, frete e confirmação de pagamento são validados no servidor.
- Não usar o servidor de desenvolvimento `--reload` em produção. Use servidor ASGI atrás de proxy HTTPS e configure backups/monitoramento.

## Estrutura
```text
northmen-store/
├── app/main.py
├── app/integrations.py
├── app/static/index.html
├── app/static/store/
├── app/static/images/
├── tests/
├── .env.example
├── PRD.md
├── AGENTS.md
└── AI_USAGE.md
```
