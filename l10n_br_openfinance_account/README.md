# Open Finance Brasil - Extratos

Importação e sincronização de extratos bancários via Open Finance Brasil. Suporte a contas correntes, contas de pagamento e conciliação contábil automática.

## Dependências

- `l10n_br_openfinance` — módulo base do Open Finance
- `l10n_br_openfinance_consent` — gerenciamento de consentimentos

## Instalação

```bash
./odoo-bin -d meu_db -i l10n_br_openfinance_account
```

## Configuração

### 1. Pré-requisitos

- Módulo base `l10n_br_openfinance` instalado com ao menos uma instituição configurada
- Módulo `l10n_br_openfinance_consent` instalado com um consentimento autorizado com escopo de leitura

### 2. Consentimento para Leitura de Extrato

O consentimento deve ter um dos seguintes escopos:

- **Leitura de Extrato (PF)** — contas de pessoa física
- **Leitura de Extrato (PJ)** — contas de pessoa jurídica
- **Leitura de Extrato Pix** — inclui transações Pix
- **Extrato + Pagamento Pix** — leitura + pagamento
- **Leitura Completa (PF/PJ)** — todos os dados da conta

### 3. Diários Contábeis

Em *Contabilidade → Configuração → Diários*, certifique-se de que os diários bancários estão configurados e vinculados à instituição financeira na aba *Open Finance*.

## Uso

### Busca Automática

Vá para *Open Finance → Extratos* e clique em *Novo*.

| Campo | Descrição |
|-------|-----------|
| Configuração | Instituição financeira |
| Consentimento | Consentimento autorizado com permissão de leitura |
| Diários | Diários contábeis para criar os extratos |
| Data Início | Início do período |
| Data Fim | Fim do período |

1. Preencha os campos e clique em **Buscar Extrato**
2. As transações serão baixadas da API Open Finance
3. O extrato ficará no estado "Importado"

### Importação para Contabilidade

1. Com o extrato no estado **Importado**, clique em **Importar para Contabilidade**
2. Será criado um extrato bancário (`account.bank.statement`) no diário selecionado
3. As linhas do extrato poderão ser conciliadas com faturas e pagamentos no módulo de contabilidade

### Sincronização Automática

O cron **Open Finance - Sincronizar Extratos** executa a cada 6 horas e busca extratos do dia corrente para todos os consentimentos ativos com permissão de leitura.

### Importação Manual (Arquivo JSON)

Vá para *Open Finance → Importar Extrato (Manual)* e selecione:

1. Um arquivo JSON contendo as transações
2. A configuração da instituição
3. Os diários contábeis de destino

O formato esperado do JSON:
```json
{
  "transactions": [
    {
      "transactionId": "123",
      "date": "2025-01-15",
      "description": "TRANSFERENCIA PIX",
      "amount": 1500.00,
      "partnerName": "João Silva",
      "partnerDocument": "123.456.789-00"
    }
  ]
}
```

## Agendamentos

| Cron | Intervalo | Descrição |
|------|-----------|-----------|
| Sincronizar Extratos | 6 horas | Busca extratos do dia corrente |

## Modelos

| Modelo | Descrição |
|--------|-----------|
| `open.finance.statement` | Extrato bancário importado |
| `open.finance.statement.line` | Linha/transação do extrato |
| `open.finance.import.wizard` | Wizard para importação manual |

## Segurança

| Grupo | Extrato | Linhas |
|-------|---------|--------|
| Faturamento | Leitura | Leitura |
| Contábil (usuário) | Leitura, criação, edição | Leitura, criação, edição |
| Contábil (gerente) | Total | Total |
