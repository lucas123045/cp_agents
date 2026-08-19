"""
Banco Multiagente - Ponto de entrada.

Requer a variável de ambiente OPENAI_API_KEY configurada.

Uso:
    python main.py
"""

import asyncio

from agents import Runner

from bank_agents import agente_atendimento
from data import CONTA


async def main() -> None:
    print("=== Banco Fictício - Atendimento Inteligente (multiagente) ===")
    print(f"Titular: {CONTA['titular']} | Saldo inicial: R$ {CONTA['saldo']:.2f}")
    print("Contatos disponíveis para PIX: Ana, Bruno, Carla, Diego, Eduarda")
    print("Digite 'sair' para encerrar.\n")

    # `historico` guarda a conversa em formato aceito pelo Runner (to_input_list),
    # permitindo que o contexto persista entre turnos e entre agentes após handoffs.
    historico = []
    agente_atual = agente_atendimento

    while True:
        entrada = input("Você: ").strip()
        if not entrada:
            continue
        if entrada.lower() in ("sair", "exit", "quit"):
            print("Atendimento encerrado. Até logo!")
            break

        historico.append({"role": "user", "content": entrada})

        resultado = await Runner.run(agente_atual, historico)

        print(f"\n[{resultado.last_agent.name}]: {resultado.final_output}\n")

        # Atualiza histórico e mantém o mesmo agente ativo no próximo turno,
        # já refletindo qualquer handoff que tenha ocorrido nesta rodada.
        historico = resultado.to_input_list()
        agente_atual = resultado.last_agent


if __name__ == "__main__":
    asyncio.run(main())
