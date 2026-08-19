"""
Tools do sistema bancário simulado.
Cada tool é uma função Python decorada com @function_tool, que o
OpenAI Agents SDK expõe ao modelo como uma ação que ele pode chamar.
"""

from datetime import datetime

from agents import function_tool

from data import CONTATOS, CONTA, FAQ_BANCO


def _buscar_contato(nome: str):
    """Busca interna (não é tool) de um contato por nome aproximado."""
    nome_normalizado = nome.strip().lower()
    for chave, dados in CONTATOS.items():
        if nome_normalizado in chave or nome_normalizado in dados["nome"].lower():
            return dados
    return None


@function_tool
def consultar_saldo() -> str:
    """Consulta o saldo disponível na conta corrente do cliente."""
    return f"Saldo disponível: R$ {CONTA['saldo']:.2f}"


@function_tool
def buscar_destinatario(nome: str) -> str:
    """Busca um destinatário de PIX na lista de contatos do cliente pelo nome.

    Args:
        nome: Nome (ou parte do nome/apelido) do destinatário informado pelo cliente.
    """
    contato = _buscar_contato(nome)
    if contato:
        return (
            f"Destinatário encontrado: {contato['nome']} | "
            f"Chave PIX cadastrada: {contato['chave_pix']}"
        )
    disponiveis = ", ".join(d["nome"] for d in CONTATOS.values())
    return (
        f"Nenhum destinatário encontrado para '{nome}'. "
        f"Contatos disponíveis na agenda: {disponiveis}."
    )


@function_tool
def realizar_pix(nome_destinatario: str, valor: float) -> str:
    """Executa (de forma simulada) uma transferência PIX, debitando o valor do
    saldo da conta e registrando a transação no histórico. Só deve ser chamada
    depois que o cliente confirmar explicitamente a transação.

    Args:
        nome_destinatario: Nome do destinatário do PIX, já validado na agenda de contatos.
        valor: Valor em reais (R$) a ser transferido. Deve ser maior que zero.
    """
    contato = _buscar_contato(nome_destinatario)
    if not contato:
        return f"Erro: destinatário '{nome_destinatario}' não encontrado na lista de contatos."

    if valor <= 0:
        return "Erro: o valor do PIX deve ser maior que zero."

    if valor > CONTA["saldo"]:
        return (
            f"Erro: saldo insuficiente para concluir a transação. "
            f"Saldo atual: R$ {CONTA['saldo']:.2f}, valor solicitado: R$ {valor:.2f}."
        )

    CONTA["saldo"] -= valor
    transacao = {
        "destinatario": contato["nome"],
        "chave_pix": contato["chave_pix"],
        "valor": valor,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }
    CONTA["historico"].append(transacao)

    return (
        "PIX realizado com sucesso!\n"
        f"Destinatário: {contato['nome']}\n"
        f"Chave PIX: {contato['chave_pix']}\n"
        f"Valor: R$ {valor:.2f}\n"
        f"Data: {transacao['data']}\n"
        f"Novo saldo disponível: R$ {CONTA['saldo']:.2f}"
    )


@function_tool
def consultar_extrato() -> str:
    """Consulta o histórico de PIX realizados durante a sessão atual."""
    if not CONTA["historico"]:
        return "Nenhuma transação realizada nesta sessão até o momento."
    linhas = [
        f"- {t['data']}: R$ {t['valor']:.2f} para {t['destinatario']}"
        for t in CONTA["historico"]
    ]
    return "Histórico de transações da sessão:\n" + "\n".join(linhas)


@function_tool
def consultar_base_conhecimento() -> str:
    """Retorna a base de conhecimento do banco (PIX, tarifas, cartões,
    investimentos e atendimento) para responder dúvidas do cliente."""
    return FAQ_BANCO
