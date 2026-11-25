from ingressos import emitir_ingresso, pedido_disponivel, gerar_codigo, registrar_venda, confirmar_pagamento, cancelar_pedido, registrar_reembolso, validar_entrada, salvar_vendas, carregar_vendas

registro = []


def conferir(caso, entrada, esperado, obtido):
    conclusao = "OK" if esperado == obtido else "FALHA"
    registro.append((caso, entrada, esperado, obtido, conclusao))
    print(f"[{conclusao}] {caso}")
    if conclusao == "FALHA":
        print(f"    esperado: {esperado}")
        print(f"    obtido:   {obtido}")


# MESA DISPONIVEL PARA VENDA AQUI
vendas_a = [
    {"pedido": 12, "status": "ativa"},
    {"pedido": 5, "status": "cancelada"},
]
conferir("normal: mesa com venda ativa",
         "mesa 12", False, pedido_disponivel(vendas_a, 12))
conferir("limite: mesa com venda cancelada",
         "mesa 5", True, pedido_disponivel(vendas_a, 5))

vendas_b = [
    {"pedido": 12, "status": "ativa"},
    {"pedido": 5, "status": "ativa"},
]
conferir("limite: mesa ativa que não é a primeira da lista",
         "mesa 5", False, pedido_disponivel(vendas_b, 5))

# GERAR CODIGO AQUI
conferir("normal: 4º ingresso da mesa 12",
         "mesa 12, posição 4", "M12-04", gerar_codigo(12, 4))
conferir("limite: posição com dois dígitos",
         "mesa 5, posição 10", "M5-10", gerar_codigo(5, 10))

# REGISTRO DE VENDA
vendas = []
conferir("normal: venda com 2 titulares",
         "mesa 12, Elizabeth Bennet, Empresa A",
         (True, "Venda registrada."),
         registrar_venda(vendas, 12, "Elizabeth Bennet", "Empresa A",
                         ["Elizabeth Bennet", "Mr. Darcy"]))
conferir("inválido: mesa já vendida por outra empresa",
         "mesa 12, Anakin Skywalker, Empresa B",
         (False, "Mesa já vendida."),
         registrar_venda(vendas, 12, "Anakin Skywalker", "Empresa B", ["Anakin Skywalker"]))
conferir("inválido: comprador só com espaços",
         "mesa 7, comprador '   '",
         (False, "Nome do comprador vazio."),
         registrar_venda(vendas, 7, "   ", "Empresa A", ["Capitu"]))
conferir("limite: mesa com um único titular",
         "mesa 3, Dean Winchester",
         (True, "Venda registrada."),
         registrar_venda(vendas, 3, "Dean Winchester", "Empresa B", ["Dean Winchester"]))
registrar_venda(vendas, 4, "Sheldon Cooper", "Empresa A", ["  Sheldon Cooper  "])
conferir("limite: espaços das pontas removidos do nome",
         "titular '  Sheldon Cooper  '", "Sheldon Cooper",
         vendas[2]["ingressos"][0]["titular"])

# CONFIRMAR SE PAGOU
vendas_pagamento = []
registrar_venda(vendas_pagamento, 20, "Daenerys Targaryen", "Empresa A",
                ["Daenerys Targaryen", "Jon Snow"])

conferir("normal: confirmar pagamento pendente",
         "mesa 20", (True, "Pagamento confirmado."),
         confirmar_pagamento(vendas_pagamento, 20))
conferir("normal: pagamento ficou como pago",
         "venda da mesa 20", "pago", vendas_pagamento[0]["pagamento"])
conferir("inválido: confirmar pagamento já confirmado",
         "mesa 20 novamente", (False, "Pagamento não está pendente."),
         confirmar_pagamento(vendas_pagamento, 20))
conferir("inválido: mesa não foi vendida",
         "mesa 99", (False, "Mesa sem venda ativa."),
         confirmar_pagamento(vendas_pagamento, 99))

# CANCELAR MESA
vendas_cancelamento = []
registrar_venda(vendas_cancelamento, 30, "Natasha Romanoff", "Empresa A",
                 ["Natasha Romanoff", "Bucky Barnes"])
confirmar_pagamento(vendas_cancelamento, 30)
registrar_venda(vendas_cancelamento, 31, "Morticia Addams", "Empresa B", ["Morticia Addams"])
registrar_venda(vendas_cancelamento, 32, "Lara Jean", "Empresa A",
                ["Lara Jean", "Peter Kavinsky"])
confirmar_pagamento(vendas_cancelamento, 32)
vendas_cancelamento[2]["ingressos"][0]["status"] = "utilizado"  

conferir("normal: cancelar mesa que foi paga",
         "mesa 30", (True, "Mesa cancelada."), cancelar_pedido(vendas_cancelamento, 30))
conferir("normal: pagamento foi para reembolso pendente",
         "venda da mesa 30", "reembolso_pendente", vendas_cancelamento[0]["pagamento"])
conferir("normal: ingressos da mesa cancelada ficaram cancelados",
         "ingresso 1 da mesa 30", "cancelado", vendas_cancelamento[0]["ingressos"][0]["status"])
conferir("normal: mesa cancelada voltou a ficar disponível",
         "mesa 30", True, pedido_disponivel(vendas_cancelamento, 30))
conferir("limite: cancelar mesa que não foi paga",
         "mesa 31", (True, "Mesa cancelada."), cancelar_pedido(vendas_cancelamento, 31))
conferir("limite: pagamento não pago vira cancelado, sem reembolso",
         "venda da mesa 31", "cancelado", vendas_cancelamento[1]["pagamento"])
conferir("inválido: cancelar mesa com ingresso já utilizado",
         "mesa 32", (False, "Mesa com ingresso já utilizado."), cancelar_pedido(vendas_cancelamento, 32))
conferir("inválido: a recusa não alterou a venda",
         "status da venda da mesa 32", "ativa", vendas_cancelamento[2]["status"])
conferir("inválido: cancelar mesa que não existe",
         "mesa 99", (False, "Mesa sem venda ativa."), cancelar_pedido(vendas_cancelamento, 99))

# REEMBOLSO
vendas_reembolso = []
registrar_venda(vendas_reembolso, 40, "Tony Stark", "Empresa A", ["Tony Stark"])
confirmar_pagamento(vendas_reembolso, 40)
cancelar_pedido(vendas_reembolso, 40)                      
registrar_venda(vendas_reembolso, 41, "Pepper Pots", "Empresa B", ["Pepper Pots"])
cancelar_pedido(vendas_reembolso, 41)                     

conferir("normal: registrar reembolso pendente",
         "mesa 40", (True, "Reembolso registrado."), 
         registrar_reembolso(vendas_reembolso, 40))
conferir("inválido: reembolsar a mesma mesa duas vezes",
         "mesa 40 de novo", (False, "Mesa sem reembolso pendente."),
         registrar_reembolso(vendas_reembolso, 40))
conferir("inválido: reembolsar mesa cancelada que não foi paga",
         "mesa 41", (False, "Mesa sem reembolso pendente."),
         registrar_reembolso(vendas_reembolso, 41))

vendas_l = []
registrar_venda(vendas_l, 50, "Frodo", "Empresa A", ["Frodo"])
confirmar_pagamento(vendas_l, 50)
cancelar_pedido(vendas_l, 50)                       # venda antiga: reembolso pendente
registrar_venda(vendas_l, 50, "Ayrton Senna", "Empresa B", ["Ayrton Senna"])   # revenda

conferir("limite: reembolso de mesa já revendida",
         "mesa 50", (True, "Reembolso registrado."), registrar_reembolso(vendas_l, 50))
conferir("limite: venda antiga ficou reembolsada",
         "1ª venda da mesa 50", "reembolsado", vendas_l[0]["pagamento"])
conferir("limite: a venda nova não foi afetada",
         "2ª venda da mesa 50", "pendente", vendas_l[1]["pagamento"])

# VALIDAR ENTRADA
vendas_entrada = []
registrar_venda(vendas_entrada, 60, "Hermione Granger", "Empresa A",
                ["Hermione Granger", "Ron Weasley"])
registrar_venda(vendas_entrada, 61, "Leia Organa", "Empresa B", ["Leia Organa"])
cancelar_pedido(vendas_entrada, 61)
registrar_venda(vendas_entrada, 62, "Harry Potter", "Empresa A", ["Harry Potter"])

conferir("normal: liberar ingresso não utilizado",
         "código M60-01", (True, "Entrada liberada: Hermione Granger"),
         validar_entrada(vendas_entrada, "M60-01"))
conferir("inválido: ler o mesmo código duas vezes",
         "código M60-01 de novo", (False, "Ingresso já utilizado."),
         validar_entrada(vendas_entrada, "M60-01"))
conferir("limite: outro ingresso da mesma mesa continua liberado",
         "código M60-02", (True, "Entrada liberada: Ron Weasley"),
         validar_entrada(vendas_entrada, "M60-02"))
conferir("limite: código em minúsculas e com espaços",
         "código '  m62-01 '", (True, "Entrada liberada: Harry Potter"),
         validar_entrada(vendas_entrada, "  m62-01 "))
conferir("inválido: ingresso de mesa cancelada",
         "código M61-01", (False, "Ingresso cancelado."),
         validar_entrada(vendas_entrada, "M61-01"))
conferir("inválido: código que não existe",
         "código M99-01", (False, "Código inexistente."),
         validar_entrada(vendas_entrada, "M99-01"))
conferir("inválido: código vazio",
         "código ''", (False, "Código inexistente."),
         validar_entrada(vendas_entrada, ""))
conferir("integração: mesa com ingresso utilizado não pode ser cancelada",
         "mesa 60", (False, "Mesa com ingresso já utilizado."),
         cancelar_pedido(vendas_entrada, 60))

# SALVAR E CARREGAR
vendas_salvas = []
registrar_venda(vendas_salvas, 70, "Thor", "Empresa A", 
                ["Thor", "Loki"])
confirmar_pagamento(vendas_salvas, 70)
salvar_vendas(vendas_salvas, "vendas_teste.json")

conferir("normal: salvar e carregar devolve as mesmas vendas",
         "arquivo vendas_teste.json", (True, vendas_salvas),
         carregar_vendas("vendas_teste.json"))
conferir("limite: arquivo ainda não existe (primeira execução)",
         "arquivo sem_arquivo_teste.json", (True, []),
         carregar_vendas("sem_arquivo_teste.json"))

salvar_vendas([], "vendas_vazio_teste.json")
conferir("limite: salvar e carregar lista vazia",
         "arquivo vendas_vazio_teste.json", (True, []),
         carregar_vendas("vendas_vazio_teste.json"))

with open("corrompido_teste.json", "w", encoding="utf-8") as arquivo:
    arquivo.write("isto não é json {")
conferir("inválido: arquivo corrompido",
         "arquivo corrompido_teste.json",
         (False, "Arquivo de vendas corrompido."),
         carregar_vendas("corrompido_teste.json"))

# EMISSÃO DO INGRESSO 
vendas_ingresso = []
registrar_venda(vendas_ingresso, 80, "Hermione Granger", "Empresa A",
                ["Hermione Granger", "Ron Weasley"])
venda_i = vendas_ingresso[0]

conferir("normal: ingresso do 1º titular",
         "mesa 80, 1º ingresso",
         "INGRESSO - Festa Teste\nTitular: Hermione Granger\nMesa: 80\nCódigo: M80-01",
         emitir_ingresso(venda_i, venda_i["ingressos"][0], "Festa Teste"))
conferir("normal: ingresso do 2º titular",
         "mesa 80, 2º ingresso",
         "INGRESSO - Festa Teste\nTitular: Ron Weasley\nMesa: 80\nCódigo: M80-02",
         emitir_ingresso(venda_i, venda_i["ingressos"][1], "Festa Teste"))

# NOVAS VALIDAÇÕES DO REGISTRO DE VENDA
vendas_novas = []
conferir("inválido: número do pedido zero",
         "pedido 0", (False, "Número do pedido inválido."),
         registrar_venda(vendas_novas, 0, "Tony Stark", "Empresa A", ["Tony Stark"]))
conferir("inválido: empresa vendedora vazia",
         "pedido 1, empresa '   '", (False, "Nome da empresa vazio."),
         registrar_venda(vendas_novas, 1, "Tony Stark", "   ", ["Tony Stark"]))

# CÓDIGO DA MESA REVENDIDA NA PORTARIA
conferir("limite: código da mesa revendida vale para a venda nova",
         "código M50-01 (venda antiga cancelada, nova ativa)",
         (True, "Entrada liberada: Ayrton Senna"),
         validar_entrada(vendas_l, "M50-01"))

# EMISSÃO DO INGRESSO NO MODO INGRESSO
conferir("normal: ingresso no modo INGRESSO mostra Pedido",
         "pedido 80, modo INGRESSO",
         "INGRESSO - Festa Teste\nTitular: Hermione Granger\nPedido: 80\nCódigo: M80-01",
         emitir_ingresso(venda_i, venda_i["ingressos"][0], "Festa Teste", "INGRESSO"))

# RESUMO
falhas = 0
for item in registro:
    if item[4] == "FALHA":
        falhas += 1
print(f"\n{len(registro)} casos, {falhas} falha(s).")

with open("registro_testes.txt", "w", encoding="utf-8") as arquivo:
    for caso, entrada, esperado, obtido, conclusao in registro:
        arquivo.write(f"Caso: {caso}\n")
        arquivo.write(f"Entrada: {entrada}\n")
        arquivo.write(f"Esperado: {esperado}\n")
        arquivo.write(f"Obtido: {obtido}\n")
        arquivo.write(f"Conclusão: {conclusao}\n\n")