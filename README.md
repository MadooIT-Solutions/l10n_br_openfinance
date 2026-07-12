# Open Finance Brasil

Conjunto de módulos para integração com o **Open Finance Brasil** no Odoo, seguindo o padrão de modularização da OCA (Odoo Community Association).

## Módulos

| Módulo | Aplicação | Descrição |
|--------|-----------|-----------|
| `l10n_br_openfinance` | App principal | Base do Open Finance: configuração de instituições, cliente API, logs, diários e empresa |
| `l10n_br_openfinance_consent` | Complemento | Gerenciamento de consentimentos PF/PJ com autorização via QR Code |
| `l10n_br_openfinance_payment` | Complemento | Pagamentos Pix e boletos de cobrança com registro e conciliação |
| `l10n_br_openfinance_account` | Complemento | Importação e sincronização de extratos bancários |

## Dependências entre módulos

```
l10n_br_openfinance                    [account, l10n_br_fiscal_certificate]
  |
  +--- l10n_br_openfinance_consent     [l10n_br_openfinance]
  |      |
  |      +--- l10n_br_openfinance_payment  [l10n_br_openfinance, l10n_br_openfinance_consent]
  |      +--- l10n_br_openfinance_account  [l10n_br_openfinance, l10n_br_openfinance_consent]
```

## Funcionalidades

- **Configuração por Instituição** — cadastre múltiplas instituições financeiras (Banco do Brasil, Itaú, Bradesco, etc.) cada uma com seu certificado A1/A3, credenciais OAuth2 e ambiente (sandbox/produção). Dados pré-carregados dos 15 maiores bancos brasileiros.
- **Consentimento com QR Code** — solicite consentimento do titular da conta (PF ou PJ), exiba o QR Code para autorização via app do banco e gerencie o ciclo de vida (autorizar, revogar, renovar token).
- **Suporte a Pessoa Física (PF) e Jurídica (PJ)** — crie consentimentos para CPF ou CNPJ com escopos de permissão específicos para cada tipo.
- **Importação de Extratos** — busque transações bancárias automaticamente via API, visualize as linhas do extrato e importe para a contabilidade como extratos bancários do Odoo.
- **Pagamentos Pix** — inicie pagamentos Pix com chave (CPF, CNPJ, e-mail, telefone ou chave aleatória), gere QR Code para pagamento, consulte status e crie o registro contábil automaticamente.
- **Boletos de Cobrança** — registre boletos bancários via API, com cálculo de juros/multa, consulte baixa automática e imprima o boleto em PDF.
- **Importação Manual** — wizard para importar extratos a partir de arquivo JSON.
- **Agendamento Automático** — crons que sincronizam extratos e verificam status de boletos periodicamente.

## Instalação

Instale apenas o módulo `l10n_br_openfinance` para a base, ou instale todos para funcionalidade completa:

```bash
# Instalar todos os módulos
./odoo-bin -d meu_db -i l10n_br_openfinance,l10n_br_openfinance_consent,l10n_br_openfinance_payment,l10n_br_openfinance_account
```

### Dependências de sistema

- Python `requests`
- Python `qrcode[pil]` para geração de QR Codes: `pip install qrcode[pil]`

## Configuração

### 1. Certificado A1/A3

Cadastre o certificado digital em *Contabilidade → Certificado Fiscal* (módulo `l10n_br_fiscal_certificate`).

### 2. Instituições Financeiras

Vá para *Open Finance → Instituições Financeiras*. Os 15 maiores bancos brasileiros já vêm pré-cadastrados. Para cada instituição, configure:

- Certificado A1/A3
- Client ID e Client Secret (fornecidos pelo banco)
- Ambiente (Sandbox/Produção)
- URLs da API

### 3. Consentimento

Vá para *Open Finance → Consentimentos* e crie um novo registro:

1. Selecione a instituição e o tipo de pessoa (PF/PJ)
2. Escolha o escopo de permissão
3. Informe o CPF/CNPJ do titular
4. Solicite o consentimento — um QR Code será gerado para autorização via app do banco
5. Após autorização, verifique o status para obter o token de acesso

### Escopos de Permissão

| Escopo | Descrição |
|--------|-----------|
| Leitura de Extrato (PF) | Saldos e transações de contas de pessoa física |
| Leitura de Extrato (PJ) | Saldos e transações de contas de pessoa jurídica |
| Leitura de Extrato Pix | Extrato + transações Pix |
| Leitura Dados Cadastrais PF | Dados cadastrais e informações complementares PF |
| Leitura Dados Cadastrais PJ | Dados cadastrais e informações complementares PJ |
| Pagamento Pix | Iniciar pagamentos Pix |
| Pagamento Boleto | Emitir boletos de cobrança |
| Extrato + Pagamento Pix | Extrato + iniciação de pagamentos Pix |
| Leitura Completa (PF) | Todas as leituras disponíveis para PF |
| Leitura Completa (PJ) | Todas as leituras disponíveis para PJ |

## Uso

### Extratos Bancários

Disponível no módulo `l10n_br_openfinance_account`.

**Busca automática:** Crie um extrato, selecione o consentimento e período, clique em "Buscar Extrato".
**Importação contábil:** Com o extrato importado, clique em "Importar para Contabilidade".
**Sincronização automática:** Cron executa a cada 6 horas para todos os consentimentos ativos com permissão de leitura.

### Pix

Disponível no módulo `l10n_br_openfinance_payment`.

Crie uma transação Pix, informe a chave e valor, selecione o consentimento com permissão Pix e envie.

### Boletos

Disponível no módulo `l10n_br_openfinance_payment`.

Registre boletos bancários via API, com emissão de PDF. O cron verifica status a cada 12 horas.

## Segurança

| Grupo | Acesso |
|-------|--------|
| `group_account_invoice` | Leitura de config/consent/extratos; criação/edição de Pix e boletos |
| `group_account_user` | Leitura/escrita/criação nos modelos |
| `group_account_manager` | Acesso total |
| `base.group_system` | API e tokens |

## Licença

AGPL-3
