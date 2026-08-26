"""
Banco Multiagente - Ponto de entrada.

Requer a variável de ambiente OPENAI_API_KEY configurada.

Uso:
    python main.py
"""

import asyncio
import os
import sys

from dotenv import load_dotenv

load_dotenv()

# Garante saída em UTF-8 no console do Windows, evitando caracteres acentuados
# corrompidos (cp1252/cp850 não cobrem todos os caracteres usados nas mensagens).
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")

from agents import Runner

from bank_agents import agente_atendimento
from data import CONTA


async def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        print(
            "Erro: variável de ambiente OPENAI_API_KEY não encontrada.\n"
            "Defina-a no arquivo .env (OPENAI_API_KEY=sua-chave-aqui) ou exporte-a "
            "no terminal antes de rodar o programa."
        )
        sys.exit(1)

    print("=== Banco Fictício - Atendimento Inteligente (multiagente) ===")
    print(f"Titular: {CONTA['titular']} | Saldo inicial: R$ {CONTA['saldo']:.2f}")
    print("Contatos disponíveis para PIX: Ana, Bruno, Carla, Diego, Eduarda")
    print("Digite 'sair' para encerrar.\n")

    # `historico` guarda a conversa em formato aceito pelo Runner (to_input_list),
    # permitindo que o contexto persista entre turnos e entre agentes após handoffs.
    historico = []
    agente_atual = agente_atendimento

    while True:
        try:
            entrada = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAtendimento encerrado. Até logo!")
            break

        if not entrada:
            continue
        if entrada.lower() in ("sair", "exit", "quit"):
            print("Atendimento encerrado. Até logo!")
            break

        historico.append({"role": "user", "content": entrada})

        try:
            resultado = await Runner.run(agente_atual, historico)
        except Exception as erro:
            print(f"\n[Erro] Não foi possível processar sua mensagem: {erro}\n")
            historico.pop()
            continue

        print(f"\n[{resultado.last_agent.name}]: {resultado.final_output}\n")

        # Atualiza histórico e mantém o mesmo agente ativo no próximo turno,
        # já refletindo qualquer handoff que tenha ocorrido nesta rodada.
        historico = resultado.to_input_list()
        agente_atual = resultado.last_agent


if __name__ == "__main__":
    asyncio.run(main())
