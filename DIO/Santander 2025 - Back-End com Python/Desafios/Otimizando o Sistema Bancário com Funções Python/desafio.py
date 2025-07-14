
import textwrap


def menu():
    menu = """

        [c] Criar Conta
        [u] Criar Usuario
        [lc] Listar Contas
        [lu] Listar Usuarios
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [q] Sair

    => """
    return input(textwrap.dedent(menu))

def deposito(saldo, extrato):
    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

def saque(*, saldo, limite, extrato, numero_saques, limite_saques):
    valor = float(input("Informe o valor do saque: "))
    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques

def extratos(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def verifica_usuario(cpf, usuarios):
    return any(usuario["cpf"] == cpf for usuario in usuarios)

def criar_usuario(usuarios):
    usuario_existe = None
    while usuario_existe == True or usuario_existe == None:
        cpf = input("Informe o CPF ou precione Q para voltar: ")
        usuario_existe = verifica_usuario(cpf, usuarios)
        if cpf == "q":
            return usuarios
        if usuario_existe == True:
            print("Usuario já existe!!\n")

    nome = input("Informe o Nome: ")
    dt_nascimento = input("Informe o Data Nascimento: ")
    endereco = input("Informe o Endereço: ")

    usuarios.append({"nome": nome, "dt_nascimento": dt_nascimento, "endereco": endereco, "cpf": cpf})
    return usuarios

def criar_conta(agencia, contas, numero_conta, usuarios):
    usuario_existe = None
    while usuario_existe == False or usuario_existe == None:
        cpf = input("Informe o CPF ou precione Q para voltar: ")
        usuario_existe = verifica_usuario(cpf, usuarios)
        if cpf == "q":
            return numero_conta, contas
        if usuario_existe == False:
            print("Usuario não existe!!\n")
    print("Conta Criada com Sucesso!!")
    numero_conta += 1
    return numero_conta, contas.append({"agencia": agencia, "conta": numero_conta, "usuario": cpf})

def print_lista_dict(lista):
    print("===========================")
    for i, item in enumerate(lista, start=1):
        for chave, valor in item.items():
            print(f"  {chave}: {valor}")
        print("--------------------")
    print("===========================")

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    usuarios = []
    contas = []
    usuario_logado = ""
    agencia = "0001"
    numero_conta = 0

    while True:
        opcao = menu()

        if(opcao == "q"):
            break
        
        elif(opcao == "u"):
            usuarios = criar_usuario(usuarios)

        elif(opcao == "c"):
            print(contas)
            numero_conta, contas = criar_conta(agencia, contas, numero_conta, usuarios)
        
        elif(opcao == "lc"):
            print_lista_dict(contas)

        elif(opcao == "lu"):
            print_lista_dict(usuarios)
        elif opcao == "d":
            saldo, extrato = deposito(saldo, extrato)

        elif opcao == "s":
            saldo, extrato, numero_saques = saque(
                saldo = saldo,
                limite = limite,
                extrato = extrato,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUES
            )

        elif opcao == "e":
            extratos(saldo, extrato = extrato)

main()