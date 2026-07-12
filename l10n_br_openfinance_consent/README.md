# Open Finance Brasil - Consentimento

Gerencia consentimentos para compartilhamento de dados e iniciação de pagamentos via Open Finance Brasil. Suporta pessoa física (PF) e jurídica (PJ).

## Dependências

- `l10n_br_openfinance` — módulo base do Open Finance

## Instalação

```bash
./odoo-bin -d meu_db -i l10n_br_openfinance_consent
```

## Configuração

### 1. Pré-requisitos

Certifique-se de que o módulo base `l10n_br_openfinance` está instalado e que ao menos uma instituição financeira está configurada com certificado e credenciais válidas.

### 2. Criar um Consentimento

Vá para *Open Finance → Consentimentos* e clique em *Novo*.

#### Campos do formulário

| Campo | Descrição |
|-------|-----------|
| Configuração | Instituição financeira alvo do consentimento |
| Tipo de Pessoa | **Pessoa Física (PF)** para CPF do titular / **Pessoa Jurídica (PJ)** para CNPJ |
| Escopo | Conjunto de permissões solicitadas (ver tabela abaixo) |
| CPF/CNPJ | Documento do titular da conta que autorizará o compartilhamento |
| Cliente/Titular | Parceiro vinculado (opcional, preenchido automaticamente pela busca) |
| Diários | Diários contábeis cobertos por este consentimento |

#### Escopos de Permissão

| Escopo | Descrição | PF/PJ |
|--------|-----------|-------|
| Leitura de Extrato (PF) | Saldos e transações de contas | PF |
| Leitura de Extrato (PJ) | Saldos e transações de contas | PJ |
| Leitura de Extrato Pix | Extrato + transações Pix | Ambos |
| Leitura Dados Cadastrais PF | Dados cadastrais e complementares | PF |
| Leitura Dados Cadastrais PJ | Dados cadastrais e complementares | PJ |
| Pagamento Pix | Iniciar pagamentos Pix | Ambos |
| Pagamento Boleto | Emitir boletos | Ambos |
| Extrato + Pagamento Pix | Extrato + iniciação de Pix | Ambos |
| Leitura Completa (PF) | Contas, cartões, crédito, investimentos | PF |
| Leitura Completa (PJ) | Contas, cartões, crédito, investimentos | PJ |

### 3. Fluxo de Autorização

1. Preencha os campos e clique em **Solicitar Consentimento**
2. Um QR Code será gerado na tela
3. O titular deve escanear o QR Code com o aplicativo do banco e autorizar
4. Após a autorização, clique em **Verificar Status**
5. Se o status for "Autorizado", o token de acesso estará disponível para uso nos demais módulos

### 4. Gerenciamento

- **Renovar Token** — quando o access token expirar, clique em Renovar Token para obter um novo
- **Revogar** — revoga o consentimento junto à instituição financeira
- **Buscar Extrato** — atalho para criar um extrato bancário (requer módulo `l10n_br_openfinance_account`)

### 5. Diferenças entre PF e PJ na API

- **Pessoa Física**: o `loggedUser` e o `businessEntity` são ambos o CPF do titular
- **Pessoa Jurídica**: o `loggedUser` é o CPF do representante legal e o `businessEntity` é o CNPJ da empresa

## Modelos

| Modelo | Descrição |
|--------|-----------|
| `open.finance.consent` | Consentimento do titular (PF ou PJ) |

## Segurança

| Grupo | Acesso |
|-------|--------|
| Faturamento | Leitura |
| Contábil (usuário) | Leitura, criação, edição |
| Contábil (gerente) | Total |
