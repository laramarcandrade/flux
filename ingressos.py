import json

def buscar_venda_ativa(vendas, numero_pedido):
    for venda in vendas:
        if venda["pedido"] == numero_pedido and venda["status"] == "ativa":
            return venda
    return None

def pedido_disponivel(vendas, numero_pedido):
    venda = buscar_venda_ativa(vendas, numero_pedido)
    return venda is None

def buscar_ingresso(vendas, codigo):
    ingresso_cancelado = None
    for venda in vendas:
        for ingresso in venda["ingressos"]:
            if ingresso["codigo"] == codigo:
                if venda["status"] == "ativa":
                    return ingresso
                if ingresso_cancelado is None:
                    ingresso_cancelado = ingresso
    return ingresso_cancelado

def gerar_codigo(numero_pedido, posicao):
    return f"M{numero_pedido}-{posicao:02d}"


def registrar_venda(vendas, numero_pedido, comprador, empresa, titulares):
    if numero_pedido <= 0:
        return False, "Número do pedido inválido."
    if not pedido_disponivel(vendas, numero_pedido):
        return False, "Mesa já vendida."
    if comprador.strip() == "":
        return False, "Nome do comprador vazio."
    if empresa.strip() == "":
        return False, "Nome da empresa vazio."
    if len(titulares) == 0:
        return False, "Informe ao menos um titular."
    for nome in titulares:
        if nome.strip() == "":
            return False, "Há titular com nome vazio."

    ingressos = []
    posicao = 1
    for nome in titulares:
        ingressos.append({
            "titular": nome.strip(),
            "codigo": gerar_codigo(numero_pedido, posicao),
            "status": "nao_utilizado",
        })
        posicao += 1

    venda = {
        "pedido": numero_pedido,
        "status": "ativa",
        "comprador": comprador.strip(),
        "empresa": empresa.strip(),
        "pagamento": "pendente",
        "ingressos": ingressos,
    }
    vendas.append(venda)
    return True, "Venda registrada."


def confirmar_pagamento(vendas, numero_pedido):
    venda = buscar_venda_ativa(vendas, numero_pedido)
    if venda is None:
        return False, "Mesa sem venda ativa."
    if venda["pagamento"] != "pendente":
        return False, "Pagamento não está pendente."
    venda["pagamento"] = "pago"
    return True, "Pagamento confirmado."


def cancelar_pedido(vendas, numero_pedido):
    venda = buscar_venda_ativa(vendas, numero_pedido)
    if venda is None:
        return False, "Mesa sem venda ativa."

    for ingresso in venda["ingressos"]:
        if ingresso["status"] == "utilizado":
            return False, "Mesa com ingresso já utilizado."

    venda["status"] = "cancelada"
    for ingresso in venda["ingressos"]:
        ingresso["status"] = "cancelado"

    if venda["pagamento"] == "pago":
        venda["pagamento"] = "reembolso_pendente"
    else:
        venda["pagamento"] = "cancelado"
    return True, "Mesa cancelada."


def registrar_reembolso(vendas, numero_pedido):
    for venda in vendas:
        if venda["pedido"] == numero_pedido and venda["pagamento"] == "reembolso_pendente":
            venda["pagamento"] = "reembolsado"
            return True, "Reembolso registrado."
    return False, "Mesa sem reembolso pendente."

def validar_entrada(vendas, codigo):
    codigo = codigo.strip().upper()
    ingresso = buscar_ingresso(vendas, codigo)

    if ingresso is None:
        return False, "Código inexistente."
    if ingresso["status"] == "utilizado":
        return False, "Ingresso já utilizado."
    if ingresso["status"] == "cancelado":
        return False, "Ingresso cancelado."

    ingresso["status"] = "utilizado"
    return True, "Entrada liberada: " + ingresso["titular"]

def salvar_vendas(vendas, caminho):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(vendas, arquivo, ensure_ascii=False, indent=2)


def carregar_vendas(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            vendas = json.load(arquivo)
    except FileNotFoundError:
        return True, []
    except json.JSONDecodeError:
        return False, "Arquivo de vendas corrompido."
    return True, vendas

def emitir_ingresso(venda, ingresso, nome_evento, tipo="MESA"):
    linhas = [
        f"INGRESSO - {nome_evento}",
        f"Titular: {ingresso['titular']}",
    ]
    if tipo == "MESA":
        linhas.append(f"Mesa: {venda['pedido']}")
    else:
        linhas.append(f"Pedido: {venda['pedido']}")

    linhas.append(f"Código: {ingresso['codigo']}")
    return "\n".join(linhas)