# Open Finance Brasil - Base

Módulo base do Open Finance Brasil. Obrigatório para todos os demais módulos do ecossistema.

## Dependências

- `account` — módulo de contabilidade do Odoo
- `l10n_br_fiscal_certificate` — gestão de certificados digitais A1/A3

## Instalação

```bash
./odoo-bin -d meu_db -i l10n_br_openfinance
```

## Configuração

### 1. Certificado Digital

Antes de configurar as instituições, cadastre o certificado A1/A3 em:
*Contabilidade → Configuração → Certificado Fiscal*

O certificado deve estar válido e exportado no formato PKCS#12 (.p12).

### 2. Instituições Financeiras

Vá para *Open Finance → Instituições Financeiras*

Os 15 maiores bancos brasileiros já vêm pré-cadastrados automaticamente. Para cada instituição, preencha:

| Campo | Obrigatório | Descrição |
|-------|-------------|-----------|
| Instituição | Sim | Nome do banco (pré-preenchido) |
| CNPJ | Não | CNPJ da instituição (pré-preenchido) |
| Ambiente | Sim | Sandbox (homologação) ou Produção |
| Certificado | Sim | Certificado A1/A3 cadastrado anteriormente |
| Client ID | Sim | Fornecido pelo banco no credenciamento Open Finance |
| Client Secret | Sim | Fornecido pelo banco no credenciamento Open Finance |
| URL Base API | Sim | Endpoint da API (ex: https://api.sandbox.openfinance.com.br) |
| URL de Autorização | Não | Endpoint OAuth2 de autorização |
| URL do Token | Não | Endpoint OAuth2 de obtenção de token |

> As credenciais OAuth2 (Client ID/Secret) são obtidas junto a cada instituição financeira no momento do credenciamento como receptora no Open Finance.

### 3. Diários Contábeis

Em *Contabilidade → Configuração → Diários*, edite cada diário bancário e na aba *Open Finance* vincule as configurações das instituições e preencha os dados bancários (código do banco, carteira, agência, conta e chave Pix).

### 4. Logs de API

Todas as requisições são registradas em *Open Finance → Logs de API* (visível apenas para administradores), facilitando o debug de problemas de integração.

## Modelos

| Modelo | Descrição |
|--------|-----------|
| `open.finance.config` | Configuração por instituição financeira |
| `open.finance.api` | Cliente de API (técnico, uso interno) |
| `open.finance.api.log` | Log de requisições à API |
| `account.journal` | Extensão com campos Open Finance (banco, carteira, chave Pix) |
| `res.company` | Extensão com vínculo às configurações Open Finance |

## Segurança

| Grupo | Config | API Log |
|-------|--------|---------|
| Faturamento | Leitura | — |
| Contábil (usuário) | Leitura | — |
| Contábil (gerente) | Total | Leitura |
| Administração | — | Total |
