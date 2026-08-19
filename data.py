"""
Dados fictícios utilizados pelo sistema bancário simulado.
Em memória apenas — reiniciam a cada execução do programa.
"""

from datetime import datetime

# Lista de contatos (destinatários possíveis de PIX)
CONTATOS = {
    "ana": {"nome": "Ana Beatriz Ferreira", "chave_pix": "ana.ferreira@email.com"},
    "bruno": {"nome": "Bruno Costa Almeida", "chave_pix": "111.222.333-44"},
    "carla": {"nome": "Carla Souza Martins", "chave_pix": "carla.souza@email.com"},
    "diego": {"nome": "Diego Lima Rocha", "chave_pix": "+55 11 98765-4321"},
    "eduarda": {"nome": "Eduarda Nogueira", "chave_pix": "eduarda.nog@email.com"},
}

# Conta corrente fictícia do cliente que está sendo atendido
CONTA = {
    "titular": "Lucas (Cliente)",
    "saldo": 1500.00,
    "historico": [],  # lista de transações realizadas na sessão
}

# Base de conhecimento simples para o Agente de Dúvidas
FAQ_BANCO = """
== Banco Fictício - Base de Conhecimento ==

PIX:
- Transferências via PIX são gratuitas e instantâneas, disponíveis 24h por dia, 7 dias por semana.
- O limite noturno padrão (entre 20h e 6h) é de R$ 1.000,00 por transação para novos dispositivos.
- É possível cadastrar até 5 chaves PIX por conta (CPF, e-mail, telefone ou chave aleatória).

Tarifas:
- Conta corrente digital: isenta de tarifa de manutenção mensal.
- Transferências TED: R$ 8,90 por operação (PIX é sempre gratuito).
- Saque em caixas eletrônicos da rede parceira: 4 saques gratuitos por mês, R$ 6,50 após esse limite.

Cartões:
- Cartão de débito: gratuito, emitido automaticamente na abertura da conta.
- Cartão de crédito: sem anuidade no primeiro ano; a partir do segundo ano, anuidade de R$ 120,00
  (isenta para clientes com gasto médio mensal acima de R$ 1.000,00).
- Limite inicial do cartão de crédito: definido conforme análise de perfil, entre R$ 500,00 e R$ 5.000,00.

Investimentos:
- CDB com liquidez diária a partir de R$ 100,00, rendendo 100% do CDI.
- Fundos de investimento com aportes a partir de R$ 50,00.

Atendimento:
- Suporte via chat disponível 24h.
- Central telefônica: 0800 123 4567, das 8h às 20h, todos os dias.
"""
