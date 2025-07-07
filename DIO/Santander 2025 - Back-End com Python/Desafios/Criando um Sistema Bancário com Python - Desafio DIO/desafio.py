from decimal import Decimal

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = Decimal(input("Iforme o valor: "))
        if valor > 0:
            saldo += valor
            extrato += f"Deposito: {valor:.2f}\n"
        else:
            print("Valor Invalido!")
    elif opcao == "s":
        valor = Decimal(input("Iforme o valor: "))

        if valor > saldo:
            print(f"\nFalha! Saldo Insuficiente!\nTentativa de saque: {valor:.2f}\nSaldo: {saldo:.2f}")
        elif valor > limite:
            print(f"\nFalha! O valor do saque supera o limite de saque!\nO seu limite de valor de saque é: {limite:.2f}")
        elif numero_saques >= LIMITE_SAQUES:
            print(f"\nFalha! Voçe atingio seu limite de saques\nO seu limite de saque é: {LIMITE_SAQUES:.2f}")
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: {valor:.2f}\n"
            numero_saques += 1
        else:
            print("Falha! O valor informado é invalido!")

    elif opcao == "e":
        print("\n====EXTRATO====")
        if not extrato:
            print("Não ouve movimentações!")
        else:
            print(extrato)
            print(f"Saldo: {saldo:.2f}")
        print("================")
    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")