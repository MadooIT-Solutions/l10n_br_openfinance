# Manual de Configuração — Pessoa Física com Certificado CNPJ

Este guia mostra como usar o certificado A1 da sua empresa (CNPJ) para acessar os dados da sua conta bancária de pessoa física via Open Finance.

## Visão Geral

```
  Sua Empresa (CNPJ)                  Banco (ex: Itaú)
  ┌─────────────────────┐            ┌──────────────────────┐
  │ Certificado A1 CNPJ │──mTLS─────▶│ API Open Finance     │
  │ Odoo + Open Finance │            │                      │
  │                     │            │  "quem está          │
  │ Consentimento PF    │──payload──▶│   consultando?"      │
  │ loggedUser = CPF    │            │  → CNPJ da empresa   │
  │ businessEntity = CPF│            │                      │
  └─────────────────────┘            │  "de quem são os     │
                                     │   dados?"            │
       ┌──────────────────┐          │  → CPF do titular    │
       │ App do Banco     │          └──────────────────────┘
       │ Escaneia QR Code │
       │ Autoriza como PF │
       └──────────────────┘
```

O certificado identifica **quem pergunta** (sua empresa). O consentimento define **de quem** (seu CPF).

---

## Pré-requisitos

Antes de começar, tenha em mãos:

- [ ] Certificado A1 da sua empresa (arquivo .pfx ou .p12)
- [ ] Senha do certificado
- [ ] Client ID e Client Secret fornecidos pelo banco para sua empresa
- [ ] Seu CPF (sem pontuação, apenas números)
- [ ] App do banco instalado no celular (para autorizar o consentimento)

---

## Passo 1: Cadastrar o Certificado A1

1. No Odoo, vá para **Contabilidade → Configuração → Certificado Fiscal**
2. Clique em **Criar**
3. Preencha:

   | Campo | Valor |
   |-------|-------|
   | Nome | Certificado A1 Empresa |
   | Tipo | A1 |
   | Arquivo | Selecione o arquivo .pfx/.p12 |
   | Senha | Senha do certificado |
   | Empresa | Sua empresa (CNPJ) |

4. Clique em **Salvar**
5. Verifique se a situação está como **Válido**

---

## Passo 2: Configurar a Instituição Financeira

1. Vá para **Open Finance → Instituições Financeiras**
2. Selecione uma das instituições pré-cadastradas (ex: Banco do Brasil, Itaú, Bradesco) ou clique em **Criar** para adicionar manualmente
3. Preencha:

   | Campo | Valor |
   |-------|-------|
   | Instituição | Nome do banco (ex: Itaú Unibanco) |
   | CNPJ | CNPJ do banco (já preenchido) |
   | Ambiente | **Sandbox** para testes / **Produção** quando estiver pronto |
   | Certificado | Selecione o certificado cadastrado no Passo 1 |
   | Client ID | Fornecido pelo banco |
   | Client Secret | Fornecido pelo banco |
   | URL Base API | Endpoint da API (ex: `https://api.itau.com.br/open-banking`) |

4. Clique em **Salvar**
5. Clique em **Testar Conexão** para verificar se as credenciais estão corretas

> **Dica:** Para obter Client ID/Secret, sua empresa precisa estar credenciada como receptora no Open Finance junto ao banco desejado. Cada banco tem seu portal de desenvolvedores (ex: developers.bb.com.br, devsantander.itau.com.br).

---

## Passo 3: Criar o Consentimento para Pessoa Física

1. Vá para **Open Finance → Consentimentos**
2. Clique em **Criar**
3. Preencha:

   | Campo | Valor |
   |-------|-------|
   | Configuração | Instituição configurada no Passo 2 |
   | Tipo de Pessoa | **Pessoa Física (PF)** |
   | Escopo | **Leitura de Extrato (PF)** (ou outro desejado) |
   | CPF/CNPJ | **Seu CPF** (apenas números, sem pontos/traço) |
   | Cliente/Titular | Seu contato no Odoo (opcional) |
   | Diários | Selecione o diário bancário onde os extratos serão importados |

4. Clique em **Salvar**

---

## Passo 4: Solicitar e Autorizar o Consentimento

1. Com o consentimento em estado **Rascunho**, clique no botão **Solicitar Consentimento**
2. Um **QR Code** será gerado na tela:

   ```
   ┌─────────────────────────┐
   │                         │
   │     ██ ██████ ██        │
   │     ██ ██████ ██        │
   │     ██ ██████ ██        │
   │     QR CODE              │
   │                         │
   └─────────────────────────┘
   ```

3. **No seu celular**, abra o **aplicativo do banco** (o mesmo banco configurado)
4. Escaneie o QR Code com o leitor do próprio app
5. O banco exibirá as permissões solicitadas — revise e clique em **Autorizar**
6. Autentique-se no app (biometria/senha) para confirmar

---

## Passo 5: Verificar e Ativar

1. Volte ao Odoo e clique em **Verificar Status**
2. O status mudará para **Autorizado**
3. O token de acesso será obtido automaticamente
4. Pronto! O consentimento agora pode ser usado para buscar extratos

---

## Passo 6: Buscar Extrato da Conta PF

1. Vá para **Open Finance → Extratos**
2. Clique em **Criar**
3. Selecione:
   - **Configuração** → a instituição
   - **Consentimento** → o consentimento PF autorizado
   - **Diários** → diário bancário
   - **Data Início / Data Fim** → período desejado (ex: hoje)
4. Clique em **Buscar Extrato**
5. As transações da sua conta PF serão importadas automaticamente

---

## Solução de Problemas

### "Erro ao processar certificado"

- Verifique se a senha do certificado está correta
- Confirme se o certificado está válido (não expirado)
- O arquivo deve estar no formato PKCS#12 (.p12/.pfx)

### "Erro na comunicação com Open Finance"

- Confirme se Client ID e Client Secret estão corretos
- Verifique se a URL Base API corresponde ao ambiente (sandbox vs produção)
- Teste a conexão no formulário da instituição

### "Consentimento rejeitado"

- Confirme que o CPF informado é de uma conta que você possui no banco
- Verifique se o escopo escolhido é compatível com o banco
- Tente com escopo menor (ex: apenas "Leitura de Extrato")

### "Nenhuma transação encontrada"

- Verifique se há movimento no período selecionado
- Confirme se o consentimento tem permissão para leitura de extratos
- Contas de crédito podem não aparecer no extrato de conta corrente

---

## Exemplo Real

```
Empresa: Minha Empresa Ltda (CNPJ: 12.345.678/0001-90)
Certificado: A1 da Minha Empresa Ltda

Banco: Itaú Unibanco (CNPJ: 60.701.190/0001-04)
Client ID: cliente_iti_1234abcd
Client Secret: segredo_abc123

Consentimento PF:
  Tipo: Pessoa Física
  CPF: 123.456.789-00 (CPF do sócio)
  Escopo: Leitura de Extrato (PF)
  Status: Autorizado ✓

Resultado: O Odoo consegue ler o extrato bancário da 
           conta PF do sócio usando o certificado A1 da empresa.
```

Para mais detalhes técnicos, consulte a documentação do Open Finance Brasil:
https://openfinancebrasil.atlassian.net/wiki/spaces/OF/pages/17367659/Especifica+es+de+APIs
