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

## 5. Glossário

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

## 6. Referências

- [Open Finance Brasil — Especificações Técnicas](https://openfinancebrasil.org.br)
- [Diretório Central de Participantes](https://web.directory.opinion.tecban.com.br)
- [BACEN — Open Finance](https://www.bcb.gov.br/estabilidadefinanceira/openfinance)
- [Manual de Segurança do Open Finance Brasil](https://openfinancebrasil.org.br/seguranca)
