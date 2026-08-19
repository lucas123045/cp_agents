# Banco Multiagente — OpenAI Agents SDK

Sistema de atendimento inteligente para um banco fictício, construído com o
[OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), usando
**Agents**, **Tools** e **Handoffs**.

## Arquitetura

```
Cliente
   |
   v
Agente de Atendimento  (triagem: identifica a intenção e faz handoff)
   |                \
   | handoff         \ handoff
   v                  v
Agente PIX        Agente de Dúvidas
   ^                    |
   |____________________|
      handoff (se o assunto mudar no meio da conversa)
```

- **Agente de Atendimento** — ponto de entrada. Não executa nada sozinho; apenas
  entende a intenção do cliente e delega via `handoff` para o agente especializado.
- **Agente PIX** — usa as tools `consultar_saldo`, `buscar_destinatario`,
  `realizar_pix` e `consultar_extrato`. Segue um fluxo de **confirmação obrigatória**:
  encontra o destinatário e o valor, apresenta um resumo da transação e só chama
  `realizar_pix` depois que o cliente confirmar explicitamente.
- **Agente de Dúvidas** — usa a tool `consultar_base_conhecimento` para responder
  perguntas sobre PIX, tarifas, cartões, investimentos e atendimento, com base em
  uma FAQ fictícia (`data.py`).

Os três agentes têm handoffs entre si, então a conversa pode migrar de assunto
(ex.: o cliente pergunta uma tarifa no meio de um PIX) sem perder o contexto.

## Arquivos

| Arquivo          | Conteúdo                                                          |
|-------------------|--------------------------------------------------------------------|
| `data.py`          | Dados fictícios: agenda de contatos, saldo da conta, FAQ do banco |
| `tools.py`         | Tools (`@function_tool`) que os agentes podem chamar               |
| `bank_agents.py`   | Definição dos 3 `Agent` e das regras de `handoffs`                 |
| `main.py`          | Loop de chat no terminal, mantendo o estado entre turnos           |

> O arquivo dos agentes se chama `bank_agents.py` (e não `agents.py`) de propósito,
> para não conflitar com o pacote `agents` do SDK.

## Como rodar

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="sua-chave-aqui"
python main.py
```

## Exemplo de conversa

```
Você: Faça um PIX de R$ 50 para a Ana

[Agente PIX]: Encontrei a destinatária Ana Beatriz Ferreira (chave PIX:
ana.ferreira@email.com). Posso confirmar o envio de R$ 50,00 para ela?

Você: sim, pode confirmar

[Agente PIX]: PIX realizado com sucesso!
Destinatário: Ana Beatriz Ferreira
Chave PIX: ana.ferreira@email.com
Valor: R$ 50,00
Novo saldo disponível: R$ 1.450,00

Você: qual a tarifa do cartão de crédito?

[Agente de Dúvidas]: O cartão de crédito não tem anuidade no primeiro ano...
```

Note que, na segunda pergunta, o próprio Agente PIX identifica que o assunto
mudou e faz handoff automaticamente para o Agente de Dúvidas.

## Observações

- Todos os dados (saldo, contatos, histórico) são fictícios e vivem em memória
  (`data.py`); reiniciam a cada execução do programa.
- O `realizar_pix` nunca é chamado sem confirmação explícita do cliente — essa
  regra está nas instruções do Agente PIX.
- Para testar sem gastar chamadas de API reais, você pode inspecionar
  `bank_agents.py` e `tools.py` isoladamente — a lógica das tools (saldo,
  busca de contato, débito) é Python puro e testável sem o SDK.
