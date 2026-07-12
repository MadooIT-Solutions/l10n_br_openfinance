# Credenciamento Open Finance Brasil

Guia completo de credenciamento para acesso às APIs Open Finance nos principais bancos brasileiros.

---

## 1. Visão Geral

O credenciamento no Open Finance Brasil segue o fluxo abaixo:

1. **Autorização BACEN** → A instituição precisa estar autorizada pelo Banco Central como participante do Open Finance.
2. **Cadastro no Portal do Desenvolvedor** → Cada banco possui seu próprio portal onde você se registra como desenvolvedor.
3. **DCR (Dynamic Client Registration)** → Registro dinâmico do cliente para obter credenciais de acesso (Client ID / Client Secret).
4. **Sandbox** → Ambiente de testes para validação das integrações.
5. **Produção** → Migração para o ambiente produtivo após homologação.

> **Pré-requisitos legais:** Sua empresa precisa ser uma instituição autorizada BACEN (banco, fintech, cooperativa, etc.) ou uma instituição transmissora de dados registrada no Diretório Central de Participantes do Open Finance Brasil.

---

## 2. Tabela Resumo

| Banco | Portal Desenvolvedor | Tipo DCR | Sandbox | Correntista? |
|-------|---------------------|----------|---------|-------------|
| Banco do Brasil | [developers.bb.com.br](https://developers.bb.com.br) | Manual | Sim | Sim |
| Caixa Econômica Federal | [desenvolvedores.caixa.gov.br](https://desenvolvedores.caixa.gov.br) | Manual | Sim | Sim |
| Bradesco | [developers.bradesco.com.br](https://developers.bradesco.com.br) | Manual | Sim | Sim |
| Itaú | [devportal.itau.com.br](https://devportal.itau.com.br) | Automático (API) | Sim | Sim |
| Santander | [developer.santander.com.br](https://developer.santander.com.br) | Automático (API) | Sim | Sim |
| BTG Pactual | [developer.btgpactual.com](https://developer.btgpactual.com) | Automático (portal) | Sim | Sim |
| Nubank | Agregadores (Pluggy, Belvo, etc.) | Não possui portal próprio | N/A | Apenas transmissor |
| Inter | [developers.inter.co](https://developers.inter.co) | Automático (API) | Sim | Sim |
| C6 Bank | [developers.c6bank.com.br](https://developers.c6bank.com.br) | Manual | Sim | Sim |
| Safra | [developer.luxhub.com](https://developer.luxhub.com) | Manual | Sim | Sim |
| Original | [portal-bancooriginal.sensedia.com](https://portal-bancooriginal.sensedia.com) | Manual | Sim | Sim |
| Mercado Pago | [developers.mercadopago.com.br](https://developers.mercadopago.com.br) | Automático (dashboard) | Sim | Meio de pagamento |
| PicPay | [developers-business.picpay.com](https://developers-business.picpay.com) | Automático (dashboard) | Sim | Pix próprio |
| Stone | [devcenter.stone.com.br](https://devcenter.stone.com.br) | Manual | Sim | Sim |
| PagBank | [developer.pagbank.com.br](https://developer.pagbank.com.br) | Automático (dashboard) | Sim | Sim |

---

## 3. Seções Detalhadas por Banco

---

### 3.1. Banco do Brasil

**Portal:** [developers.bb.com.br](https://developers.bb.com.br)
**Página Open Finance:** [bb.com.br/site/developers/apis-open-finance](https://www.bb.com.br/site/developers/apis-open-finance/)

**Processo de credenciamento:**
1. Acesse o portal e crie sua conta de desenvolvedor.
2. Solicite acesso às APIs Open Finance através do **Fórum de discussão** no portal.
3. O BB analisa a solicitação e libera o acesso manualmente.
4. Após aprovação, obtenha **Client ID** e **Client Secret** no fórum.

**Sandbox:** Disponível no portal. Endpoints de teste separados.
**Produção:** Necessário certificado A1 (ICP-Brasil) para mTLS.
**Suporte:** Fórum do portal / Central de relacionamento.

> **⚠️ Processo manual:** O DCR não é automatizado. Pode levar alguns dias úteis.

---

### 3.2. Caixa Econômica Federal

**Portal:** [desenvolvedores.caixa.gov.br](https://desenvolvedores.caixa.gov.br)

**Processo de credenciamento:**
1. Cadastre-se no portal de desenvolvedores da Caixa.
2. Solicite acesso às APIs desejadas através do catálogo de APIs.
3. A Caixa analisa e libera o acesso manualmente.
4. Credenciais são fornecidas pelo portal após aprovação.

**Sandbox:** Ambiente disponível para testes.
**Produção:** Certificado A1 ICP-Brasil obrigatório para mTLS.
**Observação:** Processo de homologação manual e burocrático.

> **⚠️ Processo manual:** Solicitação analisada caso a caso.

---

### 3.3. Bradesco

**Portal:** [developers.bradesco.com.br](https://developers.bradesco.com.br)

**Processo de credenciamento:**
1. Acesse o portal e cadastre sua empresa via **Bradesco Marketplace**.
2. Navegue até o catálogo de APIs Open Finance e solicite acesso.
3. O Bradesco analisa a solicitação e aprova manualmente.
4. Obtenha Client ID e Client Secret no portal.

**Sandbox:** Ambiente disponível no portal.
**Produção:** Certificado A1 ICP-Brasil para mTLS.
**Suporte:** Central de relacionamento / Marketplace.

> **⚠️ Processo manual:** Aprovação via marketplace pode levar dias.

---

### 3.4. Itaú

**Portal:** [devportal.itau.com.br](https://devportal.itau.com.br)
**Documentação API:** [devportal.itau.com.br/api-open-finance](https://devportal.itau.com.br/api-open-finance)

**Processo de credenciamento:**
1. Cadastre-se no DevPortal Itaú.
2. Crie um aplicativo no portal.
3. Utilize a **API de DCR automática** para registrar seu cliente dinamicamente.
4. Client ID e Client Secret gerados automaticamente via DCR.

**Sandbox:** Totalmente funcional, endpoints dedicados.
**Produção:** Certificado A1 ou A3 ICP-Brasil para mTLS.
**Diferencial:** DCR automático via API REST — sem intervenção manual.

> **✅ DCR Automático:** Processo mais rápido do mercado.

---

### 3.5. Santander

**Portal:** [developer.santander.com.br](https://developer.santander.com.br)

**Processo de credenciamento:**
1. Cadastre-se no portal Santander Developer.
2. Crie uma aplicação no dashboard.
3. O DCR é feito automaticamente via API.
4. Credenciais geradas automaticamente.

**Sandbox:** Disponível.
**Produção:** Certificado A1 ICP-Brasil.
**Suporte:** Portal / Central de relacionamento.

> **✅ DCR Automático:** Registro via API sem intervenção manual.

---

### 3.6. BTG Pactual

**Portal:** [developer.btgpactual.com](https://developer.btgpactual.com)

**Processo de credenciamento:**
1. Cadastre-se no portal BTG Developer.
2. Solicite acesso às APIs Open Finance pelo painel.
3. O DCR é processado automaticamente pelo portal.
4. Client ID e Client Secret fornecidos no dashboard.

**Sandbox:** Ambiente dedicado.
**Produção:** Certificado A1 ICP-Brasil.
**Observação:** BTG utiliza a plataforma Luxoft (LuxHub) como gateway.

> **✅ DCR Automático:** Registro automático via portal.

---

### 3.7. Nubank

**Portal:** Não possui portal de desenvolvedores próprio para Open Finance.

**Processo de credenciamento:**
1. Nubank é **apenas instituição transmissora** de dados (não receptora).
2. Para acessar dados via Nubank, é necessário utilizar **agregadores** como Pluggy, Belvo ou similar.
3. O credenciamento é feito através do agregador, que atua como intermediário.
4. O Nubank não oferece DCR direto para receptores.

**Alternativa:** Integração via Open Finance Indireto (agregadores).

**Suporte:** Não há portal específico para Open Finance.

> **⚠️ Restrição:** Apenas transmissor. Use agregadores para acesso.

---

### 3.8. Inter

**Portal:** [developers.inter.co](https://developers.inter.co)

**Processo de credenciamento:**
1. Cadastre-se no portal Inter Developers.
2. Acesse o catálogo de APIs e solicite acesso ao Open Finance.
3. O DCR é automático via API.
4. Credenciais geradas no portal.

**Sandbox:** Disponível.
**Produção:** Certificado A1 ICP-Brasil.
**Diferencial:** API moderna e bem documentada.

> **✅ DCR Automático:** Processo rápido e documentado.

---

### 3.9. C6 Bank

**Portal:** [developers.c6bank.com.br](https://developers.c6bank.com.br)

**Processo de credenciamento:**
1. Cadastre-se no portal C6 Developers.
2. Solicite acesso às APIs Open Finance.
3. O C6 analisa a solicitação manualmente.
4. Credenciais fornecidas após aprovação manual.

**Sandbox:** Disponível.
**Produção:** Certificado A1 ICP-Brasil.
**Observação:** Processo manual, embora o portal seja moderno.

> **⚠️ Processo manual:** Análise caso a caso pelo banco.

---

### 3.10. Safra

**Portal:** [developer.luxhub.com](https://developer.luxhub.com)

**Processo de credenciamento:**
1. Cadastre-se no portal LuxHub (plataforma de APIs do Safra).
2. Solicite acesso às APIs Open Finance.
3. Processo manual de aprovação.
4. Credenciais fornecidas no portal após aprovação.

**Sandbox:** Disponível via LuxHub.
**Produção:** Certificado ICP-Brasil.
**Observação:** Utiliza plataforma LuxHub como gateway de APIs.

> **⚠️ Processo manual:** Análise via plataforma LuxHub.

---

### 3.11. Original

**Portal:** [portal-bancooriginal.sensedia.com](https://portal-bancooriginal.sensedia.com)

**Processo de credenciamento:**
1. Cadastre-se no portal Sensedia do Banco Original.
2. Solicite acesso às APIs Open Finance.
3. Processo manual de aprovação.
4. Credenciais fornecidas após liberação.

**Sandbox:** Disponível via Sensedia.
**Produção:** Certificado ICP-Brasil.
**Observação:** Utiliza Sensedia como plataforma de APIs.

> **⚠️ Processo manual:** Aprovação via Sensedia.

---

### 3.12. Mercado Pago

**Portal:** [developers.mercadopago.com.br](https://developers.mercadopago.com.br)

**Processo de credenciamento:**
1. Cadastre-se no portal Mercado Pago Developers.
2. Crie um aplicativo no dashboard.
3. O DCR é automático via dashboard.
4. Credenciais geradas automaticamente.

**Sandbox:** Disponível (mercado pago sandbox).
**Produção:** Certificado próprio (não obrigatório ICP-Brasil).
**Observação:** Atua como meio de pagamento, não como banco tradicional.

> **✅ DCR Automático:** Dashboard completo com credenciais automáticas.

---

### 3.13. PicPay

**Portal:** [developers-business.picpay.com](https://developers-business.picpay.com)

**Processo de credenciamento:**
1. Cadastre-se no PicPay Business Developers.
2. Solicite acesso às APIs desejadas.
3. O DCR é automático via dashboard.
4. Credenciais fornecidas automaticamente.

**Sandbox:** Disponível.
**Produção:** Certificado ICP-Brasil.
**Observação:** APIs Pix próprias além do Open Finance padrão.

> **✅ DCR Automático:** Processo rápido via dashboard.

---

### 3.14. Stone

**Portal:** [devcenter.stone.com.br](https://devcenter.stone.com.br)

**Processo de credenciamento:**
1. Cadastre-se no DevCenter da Stone.
2. Solicite acesso às APIs Open Finance.
3. Processo manual de análise e aprovação.
4. Credenciais fornecidas no portal.

**Sandbox:** Disponível.
**Produção:** Certificado ICP-Brasil.
**Observação:** Adquirente, mas participante do Open Finance.

> **⚠️ Processo manual:** Análise de credenciamento manual.

---

### 3.15. PagBank

**Portal:** [developer.pagbank.com.br](https://developer.pagbank.com.br)

**Processo de credenciamento:**
1. Cadastre-se no portal PagBank Developers.
2. Crie um aplicativo no dashboard.
3. DCR automático via dashboard.
4. Credenciais geradas automaticamente.

**Sandbox:** Disponível.
**Produção:** Certificado próprio.
**Observação:** Banco digital completo com Open Finance.

> **✅ DCR Automático:** Dashboard completo.

---

## 4. Checklist Genérico de Credenciamento

### Pré-requisitos
- [ ] Instituição autorizada BACEN ou registrada como transmissora
- [ ] Certificado digital **ICP-Brasil** A1 (ou A3) para mTLS
- [ ] Conta corrente no banco alvo (quando aplicável)
- [ ] Cadastro de pessoa jurídica no portal do desenvolvedor

### Documentos necessários
- [ ] CNPJ da instituição
- [ ] Contrato social ou documento equivalente
- [ ] Certificado digital ICP-Brasil (CNPJ)
- [ ] Comprovante de conta bancária

### Passos no portal
- [ ] Criar conta de desenvolvedor
- [ ] Solicitar acesso às APIs Open Finance
- [ ] Aguardar aprovação (manual ou automática)
- [ ] Obter Client ID e Client Secret
- [ ] Configurar redirect URIs
- [ ] Testar no ambiente sandbox

### Configuração no Odoo
- [ ] Acessar **Open Finance → Configuração → Instituições Financeiras**
- [ ] Cadastrar a instituição com CNPJ, nome e dados de API
- [ ] Inserir Client ID e Client Secret obtidos no portal
- [ ] Configurar certificado digital nas **Configurações da Empresa**
- [ ] Associar conta bancária (diário) à instituição
- [ ] Realizar teste de conexão via **Logs de API**

---

## 5. Testes com Sandbox

### 5.1. Conceito

O **sandbox** é um ambiente de homologação isolado do ambiente produtivo. Cada banco disponibiliza endpoints específicos para testes, que simulam o comportamento real das APIs Open Finance sem movimentar valores ou dados reais.

### 5.2. Fluxo de Testes no Sandbox

```
1. Cadastro no portal do desenvolvedor
2. Obter Client ID / Client Secret (sandbox)
3. Configurar certificado A1 (teste) no Odoo
4. Configurar instituição com URL do sandbox
5. Solicitar consentimento de teste
6. Buscar extratos / realizar pagamentos
7. Validar respostas e logs
8. Migrar para produção
```

### 5.3. Configuração no Odoo

1. Acesse **Open Finance → Configuração → Instituições Financeiras**
2. Selecione a instituição desejada ou crie uma nova
3. No campo **Ambiente**, escolha **Sandbox (Homologação)**
4. Insira o **Client ID** e **Client Secret** fornecidos pelo portal de desenvolvedores (ambiente sandbox)
5. Em **URL Base API**, insira o endpoint de sandbox do banco (ex: `https://api.sandbox.banco.com.br`)
6. Configure o **certificado digital** (pode ser um certificado A1 de testes ICP-Brasil)
7. Associe a instituição a um **diário bancário**

### 5.4. Testar a Conexão

Após configurar a instituição no sandbox:

1. Abra o formulário da instituição
2. Clique em **Testar Conexão**
3. O sistema tentará uma requisição `health check` para a API
4. Sucesso: notificação verde com mensagem de conexão estabelecida
5. Erro: notificação vermelha com a mensagem de erro detalhada

Caso o teste falhe, verifique nos **Logs de API** a resposta completa do servidor.

### 5.5. Fluxo Completo de Teste

**Passo 1 — Consentimento:**
1. Crie um consentimento com o escopo desejado (ex: `read_extrato_pf`)
2. Clique em **Solicitar Consentimento**
3. Um QR Code será gerado — use o app do banco no ambiente sandbox para autorizar
4. Após autorizar, clique em **Verificar Status**
5. O status deve mudar para `authorized` ou `active`

**Passo 2 — Extrato:**
1. Com o consentimento ativo, crie um **Extrato Bancário**
2. Defina o período (data início / data fim)
3. Clique em **Buscar Extrato**
4. As transações serão importadas do sandbox
5. Verifique os dados importados na lista de linhas do extrato

**Passo 3 — Pagamento:**
1. Crie um **Pix** ou **Boleto** no ambiente sandbox
2. Preencha os dados do pagamento
3. Confirme a transação
4. Verifique o status e o retorno da API nos logs

### 5.6. Endpoints de Sandbox por Banco

| Banco | URL Base Sandbox (exemplo) |
|-------|---------------------------|
| Banco do Brasil | `https://api.sandbox.bb.com.br/open-finance` |
| Caixa | `https://openfinance-sandbox.caixa.gov.br` |
| Bradesco | `https://api.hml.bradesco.com.br/open-banking` |
| Itaú | `https://sandbox.devportal.itau.com.br/api` |
| Santander | `https://api-sandbox.santander.com.br/open-finance` |
| Inter | `https://apis.inter.co/sandbox/open-finance` |
| C6 Bank | `https://api.sandbox.c6bank.com.br/open-finance` |
| BTG | `https://api.sandbox.btgpactual.com/open-finance` |
| Safra | `https://api.sandbox.luxhub.com/open-finance` |
| Original | `https://api.sandbox.original.com.br/open-finance` |
| Mercado Pago | `https://api.mercadopago.com/open-finance/sandbox` |
| PicPay | `https://api.sandbox.picpay.com/open-finance` |
| Stone | `https://api.sandbox.stone.com.br/open-finance` |
| PagBank | `https://api.sandbox.pagbank.com.br/open-finance` |

> **Nota:** As URLs acima são ilustrativas. Consulte o portal do desenvolvedor de cada instituição para obter os endpoints exatos do ambiente sandbox.

### 5.7. Dicas para Testes

- **Certificado de teste:** Utilize um certificado A1 ICP-Brasil de testes (válido, mas não necessariamente de produção)
- **Dados fictícios:** No sandbox, use CPFs e CNPJs fictícios ou fornecidos pelo banco
- **Consentimento:** Alguns bancos oferecem um app específico de sandbox para autorizar consentimentos
- **Rate limiting:** Ambientes sandbox podem ter limites de requisição mais restritivos
- **Reset periódico:** Dados do sandbox podem ser resetados periodicamente — não use dados importantes

### 5.8. Erros Comuns no Sandbox

| Erro | Possível Causa | Solução |
|------|---------------|---------|
| `Certificate not found` | Certificado não configurado ou expirado | Verifique o certificado em **Configurações da Empresa** |
| `Invalid client_id` | Client ID do ambiente errado (sandbox vs produção) | Confirme se o Client ID é do sandbox |
| `Consent not authorized` | Consentimento não foi aprovado no app do banco | Abra o QR Code e autorize no app de teste |
| `Token expired` | Access token expirou | Use **Renovar Token** ou solicite novo consentimento |
| `Scope not allowed` | Escopo não liberado para seu Client ID | Verifique as permissões no portal do desenvolvedor |
| `HTTP 401` | Credenciais inválidas ou mTLS incorreto | Verifique Client ID, Secret e certificado |
| `HTTP 403` | Sem permissão para o recurso solicitado | Verifique escopos e autorização BACEN |
| `HTTP 429` | Muitas requisições | Aguarde e tente novamente |

---

## 6. Glossário

| Termo | Descrição |
|-------|-----------|
| **DCR** | Dynamic Client Registration — processo de registro dinâmico do cliente para obter credenciais OAuth2 |
| **mTLS** | Mutual TLS — autenticação mútua via certificado digital entre cliente e servidor |
| **OAuth2** | Protocolo de autorização utilizado pelo Open Finance |
| **JWT** | JSON Web Token — formato de token utilizado nas autenticações |
| **Authorization Server** | Servidor de autorização responsável pela emissão de tokens |
| **Client ID** | Identificador público da aplicação cliente |
| **Client Secret** | Chave secreta da aplicação cliente |
| **Sandbox** | Ambiente de testes isolado do ambiente produtivo |
| **ICP-Brasil** | Infraestrutura de Chaves Públicas Brasileira — padrão oficial de certificação digital |
| **Diretório Central** | Repositório central de participantes do Open Finance Brasil |
| **Agregador** | Terceiro que consolida dados de múltiplas instituições (ex: Pluggy, Belvo) |
| **Transmissor** | Instituição que fornece dados via Open Finance |
| **Receptor** | Instituição que consome dados via Open Finance |
| **Consent** | Consentimento do usuário para compartilhamento de dados |
| **Scope** | Escopo de permissões solicitadas (dados cadastrais, contas, cartões, etc.) |

---

## 7. Referências

- [Open Finance Brasil — Especificações Técnicas](https://openfinancebrasil.org.br)
- [Diretório Central de Participantes](https://web.directory.opinion.tecban.com.br)
- [BACEN — Open Finance](https://www.bcb.gov.br/estabilidadefinanceira/openfinance)
- [Manual de Segurança do Open Finance Brasil](https://openfinancebrasil.org.br/seguranca)
