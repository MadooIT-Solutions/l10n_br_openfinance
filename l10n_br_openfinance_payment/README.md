# Open Finance Brasil - Pagamentos

Iniciação de pagamentos via Open Finance Brasil. Suporte a Pix e boletos de cobrança com registro, consulta de status e conciliação contábil.

## Dependências

- `l10n_br_openfinance` — módulo base do Open Finance
- `l10n_br_openfinance_consent` — gerenciamento de consentimentos

## Instalação

```bash
./odoo-bin -d meu_db -i l10n_br_openfinance_payment
```

## Configuração

### 1. Pré-requisitos

- Módulo base `l10n_br_openfinance` instalado com ao menos uma instituição configurada
- Módulo `l10n_br_openfinance_consent` instalado com um consentimento autorizado e com escopo de pagamento

### 2. Consentimento para Pagamentos

Para realizar pagamentos (Pix ou boleto), é necessário um consentimento com um dos seguintes escopos:

- **Pagamento Pix** — apenas iniciação de Pix
- **Pagamento Boleto** — apenas emissão de boletos
- **Extrato + Pagamento Pix** — leitura de extrato + Pix
- **Leitura Completa (PF/PJ)** — inclui permissão de pagamento

## Uso

### Pix

Vá para *Open Finance → Pix* e clique em *Novo*.

| Campo | Descrição |
|-------|-----------|
| Configuração | Instituição financeira |
| Consentimento | Consentimento autorizado com permissão Pix |
| Tipo | Recebido / Enviado / Devolução |
| Valor | Valor da transação |
| Contraparte | Cliente/fornecedor (opcional) |
| CPF/CNPJ | Documento da contraparte |
| Chave Pix | Chave Pix do recebedor |
| Tipo da Chave | CPF, CNPJ, e-mail, telefone ou chave aleatória |

**Fluxo de envio:**

1. Preencha os dados e clique em **Enviar Pix**
2. A transação será enviada via API Open Finance
3. Acompanhe o status com **Verificar Status**
4. Quando concluído, clique em **Criar Pagamento Contábil** para gerar o registro no Odoo

**QR Code de pagamento:**

Se possuir o payload EMV, clique em **Gerar QR Code** para exibir a imagem.

### Boletos

Vá para *Open Finance → Boletos* e clique em *Novo*.

| Campo | Descrição |
|-------|-----------|
| Configuração | Instituição financeira emissora |
| Pagador | Cliente (obrigatório) |
| Valor | Valor do boleto |
| Data de Emissão | Data de emissão |
| Data de Vencimento | Data de vencimento |
| Taxa de Juros | % de juros após vencimento |
| Taxa de Multa | % de multa após vencimento |
| Instruções | Texto livre (ex: "Não receber após o vencimento") |

**Fluxo de emissão:**

1. Preencha os dados e clique em **Registrar Boleto**
2. O boleto será registrado via API e o PDF será gerado
3. Use **Imprimir Boleto** para visualizar/download
4. O status é atualizado automaticamente a cada 12 horas pelo cron **Open Finance - Verificar Status Boletos**

**Criar a partir de fatura:**
Na fatura do cliente, utilize a ação *Criar Boleto Open Finance* no menu contextual.

## Agendamentos

| Cron | Intervalo | Descrição |
|------|-----------|-----------|
| Verificar Status Boletos | 12 horas | Atualiza status de boletos em aberto |

## Modelos

| Modelo | Descrição |
|--------|-----------|
| `open.finance.pix` | Transação Pix |
| `open.finance.boleto` | Boleto bancário |

## Segurança

| Grupo | Pix | Boleto |
|-------|-----|--------|
| Faturamento | Leitura, criação, edição | Leitura, criação, edição |
| Contábil (usuário) | Leitura, criação, edição | Leitura, criação, edição |
| Contábil (gerente) | Total | Total |
