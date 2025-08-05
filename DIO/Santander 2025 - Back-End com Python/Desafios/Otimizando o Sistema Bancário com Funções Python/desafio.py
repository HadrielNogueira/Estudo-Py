from abc import ABC, abstractclassmethod, abstractproperty
import textwrap


class Account:
    def __init__(self, account_number, client):
     self._balance = 0.00
     self._account_number = account_number
     self._agency_number = "0001"
     self._client = client
     self._history = History()
    
    @classmethod
    def new_account(cls, account_number, client):
       return cls(account_number, client)
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def account_number(self):
        return self._account_number
    
    @property
    def agency_number(self):
        return self._agency_number
    
    @property
    def client(self):
        return self._client
    
    @property
    def history(self):
        return self._history

    def withdraw(self, value):
        exceeded_balance = value > self.balance

        if exceeded_balance:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif value > 0:
            self._balance -= value
            print("Saque realizado com Sucesso!")
            return True
        else:
            print("Operação falhou! O valor informado é inválido.")
        return False
    
    def deposit(self, value):
        if value > 0:
            self._balance += value
            print("Deposito realizado com Sucesso!")
        else:
            print("Valor de deposito invalido")
            return False
        return True

class History:
    def __init__(self):
        self._transactions = []
    
    @property
    def transactions(self):
        return self._transactions

    def add_transaction(self, transaction):
       self._transactions.append(
           {
               "type": transaction.__class__.__name__,
               "value": transaction.value
           }
       )
    
class CheckingAccount(Account):
    def __init__(self, account_number, client, withdrawal_limit = 3, cash_withdrawal_limit = 500):
        super().__init__(account_number, client)
        self.withdrawal_limit = withdrawal_limit
        self.cash_withdrawal_limit = cash_withdrawal_limit

    def withdraw(self, value):
        withdrawal_number = len([
            transaction for transaction in self.history.transactions 
            if transaction["type"] == Withdrawal.__name__
        ])

        exceeded_balance = value > self.balance
        exceeded_withdrawal_limit = withdrawal_number > self.withdrawal_limit

        if exceeded_balance:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif exceeded_withdrawal_limit:
            print("Operação falhou! Seu limite de saques foi excedido!.")
        else:
            return super().withdraw(value)
        
        return False
    def __str__(self):
        return f"""
                ========================================
                Numero da conta:    {self.account_number}
                Numero da Agencia:  {self.agency_number}
                Saldo:              {self.balance}
                Client da conta:    {self.client}
                ========================================
                """

class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def process_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)

class NaturalPerson(Client):
    def __init__(self, address, cpf, name, birth_date):
        super().__init__(address)
        self.cpf = cpf
        self.name = name
        self.birth_date = birth_date

    def __str__(self):
        super().__str__()
        return f"""
                ====================================== 
                Nome: {self.name}
                Cpf: {self.cpf}
                Data de Nascimento: {self.birth_date}
                Endereço: {self.address}
                ======================================
                """

class Transaction(ABC):
    @property
    @abstractproperty
    def value(self):
        pass
    
    @abstractclassmethod
    def register(self, account):
        pass

class Withdrawal(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
    
    def register(self, account):
        sucess_transaction = account.withdraw(self.value)
        if sucess_transaction:
            account.history.add_transaction(self)


class Deposit(Transaction):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
    
    def register(self, account):
        sucess_transaction = account.deposit(self.value)
        if sucess_transaction:
            account.history.add_transaction(self)

def menu():
    menu = """

        [c] Criar Conta
        [u] Criar Cliente
        [lc] Listar Contas
        [lu] Listar clientes
        [d] Depositar
        [s] Sacar
        [e] Extrato
        [q] Sair

    => """
    return input(textwrap.dedent(menu))

def filter_client(cpf, clients):
    client = next((client for client in clients if client.cpf == cpf), None)
    return client

def create_client(clients):
    cpf = input("Informe o CPF: ")
    client = filter_client(cpf, clients)

    if client != None:
        print("Usuario já existe!!\n")
    else:
        name = input("Informe o Nome: ")
        birth_date = input("Informe o Data Nascimento: ")
        address = input("Informe o Endereço: ")

        clients.append(NaturalPerson(address, cpf, name, birth_date))
        print("Sucesso!!")

def search_account(client):
    if not client.accounts:
        print("Cliente não possui conta")
    else:
        i = 1 
        for account in client.accounts:
            print(f"{i} - {account}")
            i = i  + 1
        selected_account = int(input("Selecione a conta: "))
        if(i - 1 != selected_account):
            print("Ação invalida!!")
        else:
            return client.accounts[selected_account - 1]

def create_account(clients, accounts):
    account_number = len(accounts) + 1
    cpf = input("Informe o CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("Usuario não existe!!\n")
    else:
        account = CheckingAccount(account_number, client)
        accounts.append(account)
        client.add_account(account)
        print("Conta criada com sucesso!")

def deposit(clients):
    cpf = input("Informe o seu cpf: ")
    client = filter_client(cpf, clients)
    
    if not client:
        print("Usuario não existe!")
    else:
        account = search_account(client)
        if not account:
            print("Retornando!")
            return
        value = float(input("Informe o valor do deposito:"))
        if value > 0:
            transaction = Deposit(value)
            client.process_transaction(account, transaction)
        else:
            print("Valor invalido")

def withdrawal(clients):
    cpf = input("Informe o seu cpf: ")
    client = filter_client(cpf, clients)
    
    if not client:
        print("Usuario não existe!")
    else:
        account = search_account(client)
        if not account:
            print("Retornando!")
            return
        value = float(input("Informe o valor do saque:"))
        if value > 0:
            transaction = Withdrawal(value)
            client.process_transaction(account, transaction)
        else:
            print("Valor invalido")

def bank_statement(clients):
    cpf = input("Informe o seu cpf: ")
    client = filter_client(cpf, clients)
    
    if not client:
        print("Usuario não existe!")
    else:
        account = search_account(client)
        if not account:
            print("Retornando!")
            return
        transactions = account.history.transactions

        if not transactions:
            print("Erro!")
        else:
            print("==============================")
            for transaction in transactions:
                print(f"|Tipo: {transaction["type"]}    Valor: {transaction["value"]} |")
            print(f"|Numero da conta: {account.account_number}   Saldo: {account.balance} |")
            print("==============================")

def main():
    clients = []
    accounts = []

    while True:
        opcao = menu()

        if(opcao == "q"):
            break
        
        elif(opcao == "u"):
            create_client(clients)

        elif(opcao == "c"):
            create_account(clients, accounts)
        
        elif(opcao == "lu"):
            for client in clients:
                print(client)
        
        elif(opcao == "lc"):
            for account in accounts:
                print(account)
        
        elif(opcao == "d"):
            deposit(clients)
        
        elif(opcao == "s"):
            withdrawal(clients)
        
        elif(opcao == "e"):
            bank_statement(clients)

main()