from ingressos import (pedido_disponivel, registrar_venda, confirmar_pagamento,
                       cancelar_pedido, registrar_reembolso, validar_entrada,
                       emitir_ingresso, salvar_vendas, carregar_vendas)


INGRESSOS_POR_MESA = 4


def texto_do_modo(mensagem, tipo_evento):
    if tipo_evento == "MESA":
        return mensagem
    if mensagem == "Mesa já vendida.":
        return "Pedido já vendido."
    if mensagem == "Mesa sem venda ativa.":
        return "Pedido sem venda ativa."
    if mensagem == "Mesa cancelada.":
        return "Pedido cancelado."
    if mensagem == "Mesa com ingresso já utilizado.":
        return "Pedido com ingresso já utilizado."
    if mensagem == "Mesa sem reembolso pendente.":
        return "Pedido sem reembolso pendente."
    return mensagem


def ler_numero(rotulo):
    try:
        numero = int(input(f"Número {rotulo}: "))
        if numero <= 0:
            print(f"Número {rotulo} deve ser maior que zero.")
            return None
        return numero
    except ValueError:
        print(f"Número {rotulo} inválido.")
        return None


def ler_quantidade():
    try:
        qtd = int(input("Quantidade de ingressos: "))
        if qtd <= 0:
            print("A quantidade deve ser maior que zero.")
            return None
        return qtd
    except ValueError:
        print("Quantidade inválida.")
        return None


def realizar_venda(vendas, tipo_evento, nome_evento, arquivo):
    if tipo_evento == "MESA":
        numero = ler_numero("da mesa")
        if numero is None:
            return
        if not pedido_disponivel(vendas, numero):
            print("Mesa já vendida.")
            return
        quantidade = INGRESSOS_POR_MESA
    else:
        numero = len(vendas) + 1
        print(f"Novo pedido nº {numero}")
        quantidade = ler_quantidade()
        if quantidade is None:
            return

    comprador = input("Comprador: ").strip()
    while comprador == "":
        print("O comprador não pode ficar vazio.")
        comprador = input("Comprador: ").strip()

    empresa = input("Empresa vendedora: ").strip()
    while empresa == "":
        print("A empresa não pode ficar vazia.")
        empresa = input("Empresa vendedora: ").strip()

    titulares = []
    for posicao in range(1, quantidade + 1):
        nome = input(f"Titular do ingresso {posicao}: ")
        if nome.strip() == "":
            nome = comprador
        titulares.append(nome)

    ok, mensagem = registrar_venda(vendas, numero, comprador, empresa, titulares, tipo=tipo_evento)
    print(texto_do_modo(mensagem, tipo_evento))
    if ok:
        salvar_vendas(vendas, arquivo)
        venda = vendas[-1]
        for ingresso in venda["ingressos"]:
            print()
            print(emitir_ingresso(venda, ingresso, nome_evento, tipo_evento))


def listar_vendas(vendas, tipo_evento):
    if len(vendas) == 0:
        print("\nNenhuma venda registrada.")
        return

    rotulo = "Mesa " if tipo_evento == "MESA" else "Pedido #"
    print(f"\n=== Histórico de Vendas ({tipo_evento}) ===")
    for venda in vendas:
        print(f"\n{rotulo}{venda['pedido']} | Status: {venda['status'].upper()} | Pagamento: {venda['pagamento']}")
        print(f"Comprador: {venda['comprador']} ({venda['empresa']})")
        for ing in venda["ingressos"]:
            print(f"  - [{ing['codigo']}] {ing['titular']} -> {ing['status']}")


def main():
    nome_evento = input("Nome do evento: ").strip()
    while nome_evento == "":
        print("O nome do evento não pode ficar vazio.")
        nome_evento = input("Nome do evento: ").strip()

    while True:
        tipo_evento = input("Tipo de evento - MESA ou INGRESSO: ").strip().upper() or "MESA"
        if tipo_evento == "MESA" or tipo_evento == "INGRESSO":
            break
        print("Opção inválida. Digite MESA ou INGRESSO.")

    arquivo = f"{nome_evento}_{tipo_evento}.json".replace(" ", "_")
    ok, vendas = carregar_vendas(arquivo)
    if not ok:
        print(vendas)
        return
    print(f"Arquivo do evento: {arquivo} ({len(vendas)} venda(s) registrada(s))")

    if tipo_evento == "MESA":
        rotulo_menu = "mesa"
        de_rotulo = "da mesa"
    else:
        rotulo_menu = "pedido"
        de_rotulo = "do pedido"

    while True:
        print(f"\n=== {nome_evento} (Modo: {tipo_evento}) ===")
        if tipo_evento == "MESA":
            print("1 - Comprar mesa")
        else:
            print("1 - Comprar ingressos")
        print(f"2 - Confirmar pagamento {de_rotulo}")
        print(f"3 - Cancelar {rotulo_menu}")
        print(f"4 - Registrar reembolso {de_rotulo}")
        print("5 - Portaria (validar entrada)")
        print("6 - Listar vendas")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            realizar_venda(vendas, tipo_evento, nome_evento, arquivo)
            continue
        elif opcao == "2":
            numero = ler_numero(de_rotulo)
            if numero is None:
                continue
            ok, mensagem = confirmar_pagamento(vendas, numero)
        elif opcao == "3":
            numero = ler_numero(de_rotulo)
            if numero is None:
                continue
            ok, mensagem = cancelar_pedido(vendas, numero)
        elif opcao == "4":
            numero = ler_numero(de_rotulo)
            if numero is None:
                continue
            ok, mensagem = registrar_reembolso(vendas, numero)
        elif opcao == "5":
            ok, mensagem = validar_entrada(vendas, input("Código do ingresso: "))
        elif opcao == "6":
            listar_vendas(vendas, tipo_evento)
            continue
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")
            continue

        print(texto_do_modo(mensagem, tipo_evento))
        if ok:
            salvar_vendas(vendas, arquivo)


if __name__ == "__main__":
    main()